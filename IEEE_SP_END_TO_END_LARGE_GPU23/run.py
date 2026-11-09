"""Freeze local inputs, then run independently pinned GPU profiles in parallel."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import fcntl
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import traceback
from time import monotonic, sleep
import zipfile

from design import MODELS, ROOT, digest, make_manifest, read, write
from prepare import compile_panel
from score import file_hash, gpu_uuid, require_idle_gpu, snapshot
from bridge.batching import DEFAULT_LANES, MAX_LANES
from bridge.live import qualify_runtime
from bridge.plan import make_plan
from bridge.report import analyze_bridge

GPU_INDICES = {"qwen": 2, "gemma": 3}

SOURCE = ("design.py", "prepare.py", "score.py", "analyze.py", "run.py", "README.md",
          "PROTOCOL.md", "BRIDGE_PROTOCOL.md", "VALIDATION.md", "RUN_STUDY.sh", "SHOW_PROGRESS.sh", "ANALYZE.sh",
          "native.lock.txt", "data/design.json", "data/legacy_anchors.json", "data/bridge_plan.json",
          "data/historical_guard.json", "bridge/__init__.py", "bridge/plan.py", "bridge/historical.py", "bridge/native.py",
          "bridge/batching.py", "bridge/live.py", "bridge/report.py")


def status(out, phase, **kwargs):
    write(out / "status.json", {"phase": phase, "time_utc": datetime.now(timezone.utc).isoformat(), **kwargs})


def archive(run, suffix=".zip", *, profile=None):
    files = []
    for path in sorted(run.rglob("*")):
        if not path.is_file() or path.name.endswith(".tmp") or path.name == "SHA256SUMS":
            continue
        rel = path.relative_to(run)
        if profile is None or not rel.parts[0].startswith("model_") or rel.parts[0] == "model_" + profile:
            files.append((path, rel))
    checksums = "".join(f"{file_hash(path)}  {rel.as_posix()}\n" for path, rel in files)
    if profile is None:
        (run / "SHA256SUMS").write_text(checksums)
    output = run.with_suffix(suffix)
    temp = output.with_suffix(output.suffix + ".tmp")
    with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=5) as z:
        z.writestr(str(Path(run.name) / "SHA256SUMS"), checksums)
        for path, rel in files:
            z.write(path, Path(run.name) / rel)
    temp.replace(output)
    return output


def reserve_gpus(labels, locks, ownership):
    locks.mkdir(parents=True, exist_ok=True)
    bindings, descriptors = {}, {}
    for label in sorted(labels, key=GPU_INDICES.__getitem__):
        index = GPU_INDICES[label]
        uuid = gpu_uuid(index)
        if any(b["uuid"] == uuid for b in bindings.values()):
            raise RuntimeError(f"Physical GPU {index} shares the UUID of another selected GPU")
        handle = ownership.enter_context((locks / (uuid + ".lock")).open("a"))
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError(f"GPU {index} is reserved by another IEEE S&P run") from exc
        require_idle_gpu(index, uuid)
        bindings[label] = {"index": index, "uuid": uuid}
        descriptors[label] = handle.fileno()
    return bindings, descriptors


def run_profiles(run, labels, caches, bindings, descriptors, native_python, batch_lanes):
    workers, failures = {}, []
    timings = {}
    started = monotonic()
    try:
        for label in labels:
            gpu = bindings[label]
            require_idle_gpu(gpu["index"], gpu["uuid"])
        status(run, "RUNNING_PROFILES", gpu_bindings=bindings)
        for label in labels:
            out, gpu = run / ("model_" + label), bindings[label]
            status(out, "STARTING", physical_gpu=gpu["index"], gpu_uuid=gpu["uuid"])
            call = [sys.executable, "-u", str(run / "source" / "score.py"), "--model-dir", str(out),
                    "--cache", caches[label], "--gpu-index", str(gpu["index"]), "--gpu-uuid", gpu["uuid"],
                    "--native-python", native_python, "--batch-lanes", str(batch_lanes)]
            with (out / "score.log").open("w", encoding="utf-8") as log:
                worker_start = monotonic()
                process = subprocess.Popen(call, stdout=log, stderr=subprocess.STDOUT,
                                           env=os.environ | {"CUDA_VISIBLE_DEVICES": gpu["uuid"]},
                                           pass_fds=(descriptors[label],))
                workers[label] = process, worker_start
            print(f"Started {label} on physical GPU {gpu['index']} (PID {process.pid})", flush=True)
        while workers:
            for label, (process, worker_start) in tuple(workers.items()):
                code = process.poll()
                if code is None:
                    continue
                del workers[label]
                gpu = bindings[label]
                if code:
                    failures.append(label)
                timings[label] = {"elapsed_seconds": round(monotonic() - worker_start, 1),
                                  "exit_code": code, "physical_gpu": gpu["index"], "uuid": gpu["uuid"]}
                status(run / ("model_" + label), "PROFILE_FAILED" if code else "PROFILE_COMPLETE",
                       **timings[label])
                write(run / "profile_timing.json", {"profiles": timings,
                                                     "wall_seconds": round(monotonic() - started, 1)})
                if workers:
                    path = archive(run, ".after_" + label + ".zip", profile=label)
                    print(f"Checkpoint: {path}", flush=True)
            if workers:
                sleep(0.5)
        return failures
    finally:
        for process, _ in workers.values():
            if process.poll() is None:
                process.terminate()
        for process, _ in workers.values():
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def stop_requested(signum, _frame):
    raise KeyboardInterrupt(f"Received signal {signum}")


def freeze_model(run, manifest, ident):
    from transformers import AutoTokenizer

    label = ident["label"]
    out = run / ("model_" + label)
    out.mkdir()
    status(out, "TOKENIZER_PREFLIGHT")
    tokenizer = AutoTokenizer.from_pretrained(ident["path"], local_files_only=True, trust_remote_code=False,
                                              use_fast=True)
    prepared = compile_panel(manifest, tokenizer, label)
    write(out / "prepared.json", prepared)
    anchors = prepared["anchors"]
    n_prompt = sum(a["prompt_match"] for a in anchors)
    n_completion = sum(a["completion_match"] for a in anchors)
    write(out / "freeze.json", {"identity": ident, "prepared_sha256": file_hash(out / "prepared.json"),
                                "design_sha256": digest(manifest), "historical_prompt_id_matches": n_prompt,
                                "historical_completion_id_matches": n_completion})
    status(out, "FROZEN", unique_requests=len(prepared["requests"]), cells=len(prepared["observations"]))
    print(f"{ident['hub']}@{ident['revision']}: froze {len(prepared['requests'])} unique inputs "
          f"for {len(prepared['observations'])} cells", flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run", type=Path, required=True)
    p.add_argument("--cache", required=True)
    p.add_argument("--native-python", required=True)
    p.add_argument("--models", nargs="+", choices=("qwen", "gemma"), default=["qwen", "gemma"])
    p.add_argument("--gemma-revision")
    p.add_argument("--gemma-cache")
    p.add_argument("--prepare-only", action="store_true")
    p.add_argument("--batch-lanes", type=int, default=DEFAULT_LANES)
    args = p.parse_args()
    if not 1 <= args.batch_lanes <= MAX_LANES:
        p.error(f"--batch-lanes must be between 1 and {MAX_LANES}")
    if len(set(args.models)) != len(args.models):
        raise SystemExit("Each selected profile must occur once")
    run = args.run.resolve()
    run.mkdir(parents=True, exist_ok=False)
    print(f"Run directory: {run}", flush=True)
    exit_code = 1
    plan_frozen = False
    ownership = ExitStack()
    signal.signal(signal.SIGTERM, stop_requested)
    try:
        status(run, "PREPARING")
        if not args.prepare_only:
            bindings, descriptors = reserve_gpus(
                args.models, Path.home() / ".cache" / "ieee_sp" / "gpu_locks", ownership)
            write(run / "gpu_bindings.json", bindings)
        manifest = read(ROOT / "data" / "design.json")
        if manifest != make_manifest():
            raise ValueError("Source and frozen design disagree")
        write(run / "design.json", manifest)
        plan = read(ROOT / "data" / "bridge_plan.json")
        if plan != make_plan():
            raise ValueError("Source and frozen bridge schedule disagree")
        write(run / "bridge_plan.json", plan)
        write(run / "bridge_freeze.json", {"plan_sha256": digest(plan), "mechanism_sha256": digest(manifest)})
        plan_frozen = True
        write(run / "invocation.json", vars(args) | {"run": str(run), "python": sys.version,
                                                    "platform": platform.platform(), "executable": sys.executable,
                                                    "dependency_source": os.environ.get("E0_STACK_ORIGIN")})
        for name in SOURCE:
            dst = run / "source" / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, dst)
        status(run, "NATIVE_QUALIFICATION")
        qualify_runtime(args.native_python, run, plan)
        default_hub = os.environ.get("HF_HUB_CACHE") or str(
            Path(os.environ.get("HF_HOME", str(Path.home() / ".cache" / "huggingface"))) / "hub")
        caches = {"qwen": args.cache, "gemma": args.gemma_cache or args.cache}
        gemma_repo = "models--" + MODELS["gemma"]["hub"].replace("/", "--")
        gemma_revision = args.gemma_revision or MODELS["gemma"]["revision"]
        if args.gemma_cache is None and not (Path(args.cache) / gemma_repo / "snapshots" / gemma_revision).is_dir():
            caches["gemma"] = default_hub
        identities = [snapshot(caches[label], label, args.gemma_revision if label == "gemma" else None)
                      for label in args.models]
        for ident in identities:
            status(run, "FREEZING_TOKEN_INPUTS", model=ident["label"])
            try:
                freeze_model(run, manifest, ident)
            except Exception:
                status(run / ("model_" + ident["label"]), "TOKENIZER_PREFLIGHT_FAILED", error=traceback.format_exc())
                raise
        if args.prepare_only:
            status(run, "PREPARED_ONLY")
            exit_code = 0
        else:
            failures = run_profiles(run, args.models, caches, bindings, descriptors,
                                    args.native_python, args.batch_lanes)
            status(run, "ANALYZING")
            subprocess.run([sys.executable, str(run / "source" / "analyze.py"), str(run)], check=True)
            analyze_bridge(run)
            status(run, "PARTIAL_RESULTS" if failures else "END_TO_END_COMPLETE", failed_models=failures)
            exit_code = int(bool(failures))
    except (Exception, KeyboardInterrupt):
        status(run, "FAILED", error=traceback.format_exc())
        traceback.print_exc()
        if plan_frozen and not (run / "REPORT.md").exists():
            try:
                analyze_bridge(run)
            except Exception:
                traceback.print_exc()
    finally:
        ownership.close()
        setup_log = os.environ.get("E2E_SETUP_LOG")
        if setup_log and Path(setup_log).is_file():
            shutil.copy2(setup_log, run / "launcher.log")
        output = archive(run)
        print(f"Archive: {output}", flush=True)
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
