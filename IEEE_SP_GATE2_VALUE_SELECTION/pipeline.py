"""Unattended Gate 2 pipeline on physical GPU 3 (started by RUN_GATE2.sh under setsid + nohup).

  smoke (each profile) -> smoke gate -> full run (each profile) -> cross-profile verdict
  -> evaluation bundle (all code + every run directory + logs, zipped).

Every step's output is appended to one log file. pipeline_status.json is rewritten after each step.
A failed step never deletes anything; the bundle is written whatever happened.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import traceback
import zipfile

ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {"runs", "logs", "bundles", "__pycache__", ".venv", ".venv-native"}
LIGHT_SKIP = {"requests.jsonl", "request_reuse.jsonl"}
CHATGPT_LIMIT = 450 * 1024 * 1024


def now():
    return datetime.now(timezone.utc).isoformat()


def say(msg):
    print(f"[{now()}] {msg}", flush=True)


class Pipeline:
    def __init__(self, args):
        self.args = args
        self.stamp = args.stamp
        self.status_path = ROOT / "logs" / f"{self.stamp}_pipeline_status.json"
        self.state = {"pipeline": self.stamp, "started_utc": now(), "gpu": 3, "mode": args.mode,
                      "profiles": list(args.profiles), "steps": [],
                      "runs": {}, "log": args.log}

    def save(self, phase):
        self.state.update(phase=phase, updated_utc=now())
        tmp = self.status_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=1) + "\n")
        tmp.replace(self.status_path)

    def run_profile(self, profile, smoke):
        run_id = f"{self.stamp}_{profile}{'_smoke' if smoke else ''}"
        say(f"START {'smoke' if smoke else 'full'} {profile}: runs/{run_id}")
        self.save(f"RUNNING_{'SMOKE' if smoke else 'FULL'}_{profile.upper()}")
        cmd = [sys.executable, "-u", str(ROOT / "run.py"), "--run", str(ROOT / "runs" / run_id), "--profile", profile,
               "--gpu", "3", "--cache", self.args.cache, "--native-python", self.args.native_python,
               "--wait-gpu-hours", str(self.args.wait_gpu_hours), *(["--smoke"] if smoke else [])]
        code = subprocess.run(cmd, cwd=ROOT).returncode
        resumed = 0
        status_file = ROOT / "runs" / run_id / "status.json"
        # One automatic resume, only when the GPU worker itself died (Gate 1's Gemma worker was SIGKILLed
        # by an unknown external cause; host RAM was not exhausted). Completed cells are kept.
        while code and resumed < self.args.max_resumes and status_file.exists() \
                and "GPU worker exited with" in json.loads(status_file.read_text()).get("error", ""):
            resumed += 1
            say(f"RESUME {run_id} (attempt {resumed}) after worker failure")
            self.save(f"RESUMING_{'SMOKE' if smoke else 'FULL'}_{profile.upper()}")
            code = subprocess.run([*cmd, "--resume"], cwd=ROOT).returncode
        result = {"run_id": run_id, "exit_code": code, "smoke": smoke, "resumes": resumed}
        if code:
            worker_log = ROOT / "runs" / run_id / f"model_{profile}" / "worker.log"
            tail = worker_log.read_text(errors="replace").splitlines()[-5:] if worker_log.exists() else []
            result["worker_log_tail"] = tail  # a SIGKILL (exit -9/137) leaves no traceback: check host RAM lines
            say(f"RUN FAILED {run_id} exit {code}; worker log tail: {tail}")
        analysis = ROOT / "runs" / run_id / "analysis.json"
        if analysis.exists():
            a = json.loads(analysis.read_text())
            result.update(verdict=a["verdict"], episodes=a["episodes"], expected=a["expected_episodes"],
                          max_unparsed=a["decision_inputs"]["max_unparsed_rate"])
        self.state["runs"][run_id] = result
        self.state["steps"].append({"step": f"{'smoke' if smoke else 'full'}_{profile}", "at": now(), **result})
        say(f"END {run_id}: {json.dumps(result)}")
        self.save(f"DONE_{run_id}")
        return result

    def smoke_gate(self, results):
        """Preregistered engineering gate: every smoke run completed, produced every episode, and no
        adapter x arm exceeded 1% unparsed. The smoke verdict itself is not science and is ignored."""
        problems = []
        for r in results:
            if r["exit_code"] != 0:
                problems.append(f"{r['run_id']} exited {r['exit_code']}")
            elif r.get("episodes") != r.get("expected"):
                problems.append(f"{r['run_id']} has {r.get('episodes')}/{r.get('expected')} episodes")
            elif r.get("max_unparsed", 1) > 0.01:
                problems.append(f"{r['run_id']} max unparsed rate {r.get('max_unparsed')}")
        return problems

    def verdict(self, full):
        out = ROOT / "runs" / f"gate2_verdict_{self.stamp}.json"
        subprocess.run([sys.executable, str(ROOT / "analyze.py"), "--combine",
                        *(str(ROOT / "runs" / r["run_id"]) for r in full), "--out", str(out)], cwd=ROOT, check=True)
        self.state["verdict"] = json.loads(out.read_text())
        return out

    def bundle(self):
        """Zip all package code, every run directory of this pipeline, the log and the status."""
        bundles = ROOT / "bundles"
        bundles.mkdir(exist_ok=True)
        run_dirs = [ROOT / "runs" / rid for rid in self.state["runs"] if (ROOT / "runs" / rid).is_dir()]
        extras = [p for p in (ROOT / "runs" / f"gate2_verdict_{self.stamp}.json", Path(self.args.log),
                              self.status_path) if p.exists()]

        def code_files():
            for current, dirs, files in os.walk(ROOT):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
                for f in sorted(files):
                    yield Path(current) / f

        def write(path, light):
            manifest, skipped = [], []
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
                for f in code_files():
                    arc = Path("code") / f.relative_to(ROOT)
                    z.write(f, arc)
                    manifest.append((str(arc), f))
                for d in run_dirs:
                    for f in sorted(d.rglob("*")):
                        if not f.is_file() or f.name.endswith(".tmp"):
                            continue
                        if light and f.name in LIGHT_SKIP:
                            skipped.append({"path": str(f.relative_to(ROOT)), "bytes": f.stat().st_size,
                                            "sha256": sha(f)})
                            continue
                        arc = Path("runs") / f.relative_to(ROOT / "runs")
                        z.write(f, arc)
                        manifest.append((str(arc), f))
                for f in extras:
                    arc = Path("logs") / f.name
                    z.write(f, arc)
                    manifest.append((str(arc), f))
                lines = "".join(f"{sha(f)}  {arc}\n" for arc, f in manifest)
                z.writestr("BUNDLE_SHA256SUMS", lines)
                z.writestr("BUNDLE_README.txt", readme(self.state, light, skipped))
                if skipped:
                    z.writestr("OMITTED_LARGE_FILES.json", json.dumps(skipped, indent=1))
            return path

        full = write(bundles / f"gate2_{self.stamp}_evaluation.zip", light=False)
        self.state["bundle"] = {"path": str(full), "bytes": full.stat().st_size}
        if full.stat().st_size > CHATGPT_LIMIT:
            light = write(bundles / f"gate2_{self.stamp}_evaluation_light.zip", light=True)
            self.state["bundle_light"] = {"path": str(light), "bytes": light.stat().st_size}
        say(f"BUNDLE {json.dumps({k: v for k, v in self.state.items() if k.startswith('bundle')})}")

    def main(self):
        smoke_results, full_results = [], []
        (ROOT / "logs" / f"{self.stamp}.pid").write_text(f"{os.getpgid(0)}\n")
        say(f"PIPELINE {self.stamp} pid {os.getpid()} process group {os.getpgid(0)} session {os.getsid(0)}; GPU 3 only")
        try:
            self.save("STARTED")
            if self.args.mode in ("all", "smoke"):
                smoke_results = [self.run_profile(p, smoke=True) for p in self.args.profiles]
                problems = self.smoke_gate(smoke_results)
                self.state["smoke_gate"] = {"pass": not problems, "problems": problems}
                say(f"SMOKE GATE {'PASS' if not problems else 'FAIL: ' + '; '.join(problems)}")
                if problems:
                    self.save("STOPPED_AT_SMOKE_GATE")
                    return 1
            if self.args.mode in ("all", "run"):
                full_results = [self.run_profile(p, smoke=False) for p in self.args.profiles]
                if full_results and all(r.get("verdict") for r in full_results):
                    out = self.verdict(full_results)
                    say(f"VERDICT {out}: {json.dumps(self.state['verdict'])}")
            failed = [r for r in smoke_results + full_results if r["exit_code"] != 0]
            self.save("PIPELINE_COMPLETE" if not failed else "PIPELINE_COMPLETE_WITH_FAILURES")
            return 1 if failed else 0
        except BaseException:
            self.state["error"] = traceback.format_exc()
            say("PIPELINE ERROR\n" + self.state["error"])
            self.save("PIPELINE_FAILED")
            return 1
        finally:
            try:
                self.bundle()
                self.save(self.state["phase"])
            except Exception:
                say("BUNDLE FAILED\n" + traceback.format_exc())
            say(f"PIPELINE END: {self.state['phase']}")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def readme(state, light, skipped):
    lines = [
        "Gate 2 value selection (GATE2_VALUE_SELECTION_V1) evaluation bundle",
        f"pipeline {state['pipeline']}  phase {state.get('phase')}  created {now()}",
        "",
        "code/    the complete IEEE_SP_GATE2_VALUE_SELECTION package (PROTOCOL.md = preregistration)",
        "runs/    one directory per run: gate2_plan.json, freeze.json, source/, native_qualification.json,",
        "         template_preflight.json, model_<profile>/{episodes/*.json, requests.jsonl, worker.log, runtime.json},",
        "         analysis.json, report.txt, episodes.csv, SHA256SUMS; plus gate2_verdict_*.json",
        "logs/    the pipeline log and pipeline_status.json",
        "",
        "Runs: " + json.dumps(state.get("runs"), indent=1),
        "Smoke gate: " + json.dumps(state.get("smoke_gate")),
        "Verdict: " + json.dumps(state.get("verdict")),
    ]
    if light:
        lines += ["", f"LIGHT bundle: {len(skipped)} raw request logs omitted (sizes and SHA-256 in "
                      "OMITTED_LARGE_FILES.json); the full bundle next to this one contains them."]
    return "\n".join(lines) + "\n"


def stop_requested(signum, _frame):
    raise KeyboardInterrupt(f"signal {signum}")


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, stop_requested)
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=("all", "smoke", "run"), required=True)
    p.add_argument("--profiles", nargs="+", default=["qwen", "gemma"], choices=("qwen", "gemma"))
    p.add_argument("--stamp", required=True)
    p.add_argument("--log", required=True)
    p.add_argument("--cache", required=True)
    p.add_argument("--native-python", required=True)
    p.add_argument("--wait-gpu-hours", type=float, default=12.0)
    p.add_argument("--max-resumes", type=int, default=1)
    raise SystemExit(Pipeline(p.parse_args()).main())
