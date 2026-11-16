"""Gate 2 controller (CPU), derived from the Gate 1 controller. Freezes the plan, qualifies native worlds and chat templates, reserves one
pinned GPU, runs one model profile in a GPU worker, then analyzes and archives the run."""
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
import time
import traceback
import zipfile

from common import MODELS, PINNED_GPUS, ROOT, digest, read, write
from score import file_hash, gpu_uuid, require_idle_gpu, snapshot

SOURCE = ("common.py", "score.py", "run.py", "worker.py", "analyze.py", "RUN_GATE2.sh", "PROTOCOL.md",
          "native.lock.txt", "data/historical_guard.json", "data/gate2_plan.json", "bridge/__init__.py",
          "bridge/base_plan.py", "bridge/gate1_plan.py", "bridge/gate2_plan.py", "bridge/historical.py",
          "bridge/native.py", "bridge/batching.py", "bridge/adapters.py", "bridge/live.py", "tests/test_gate2.py",
          "pipeline.py", "tests/test_pipeline.py")
SMOKE_BASES = ("banking.3.0", "workspace.0.0", "slack.0.0")


def status(out, phase, **kwargs):
    write(out / "status.json", {"phase": phase, "time_utc": datetime.now(timezone.utc).isoformat(), **kwargs})


def archive(run):
    files = [(p, p.relative_to(run)) for p in sorted(run.rglob("*"))
             if p.is_file() and not p.name.endswith(".tmp") and p.name != "SHA256SUMS"]
    checksums = "".join(f"{file_hash(p)}  {rel.as_posix()}\n" for p, rel in files)
    (run / "SHA256SUMS").write_text(checksums)
    output = run.with_suffix(".zip")
    temp = output.with_suffix(".zip.tmp")
    with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=5) as z:
        z.writestr(str(Path(run.name) / "SHA256SUMS"), checksums)
        for p, rel in files:
            z.write(p, Path(run.name) / rel)
    temp.replace(output)
    return output


def select_plan(smoke):
    from bridge import base_plan
    from bridge.gate2_plan import BASE_PLAN_DIGEST, make_plan

    if digest(base_plan.make_plan()) != BASE_PLAN_DIGEST:
        raise RuntimeError("bridge/base_plan.py no longer reproduces the frozen E13/E14 bridge plan")
    plan = make_plan()
    if plan != read(ROOT / "data" / "gate2_plan.json"):
        raise RuntimeError("Source and frozen Gate 2 plan disagree")
    if smoke:  # 3 bases x 4 candidates x 2 instructions, linkage 0: 24 cells
        plan = plan | {"smoke": True, "cells": [c for c in plan["cells"] if c["base"] in SMOKE_BASES
                                                 and c["linked"] == 0]}
    return plan


def template_preflight(identity, plan):
    """Render every base's actor input for both adapters (before and after the two reads) with the
    model's own chat template. Catches template errors (e.g. Gemma role alternation) before the GPU."""
    from transformers import AutoTokenizer
    from bridge.adapters import render
    from bridge.batching import generation_request
    from bridge.gate2_plan import effective_base
    from bridge.live import initial

    tokenizer = AutoTokenizer.from_pretrained(identity["path"], local_files_only=True, trust_remote_code=False,
                                              use_fast=True)
    report = []
    qualification = {(q["base"], q["candidate"]): q for q in read(plan["_qualification"])}
    for cell in plan["cells"]:
        if cell["linked"]:
            continue
        base = effective_base(next(b for b in plan["bases"] if b["id"] == cell["base"]), cell)
        q = qualification[(cell["base"], cell["candidate"])]
        schemas = plan["_schemas"][(base["id"], cell["carrier"] == "text_only")]
        messages = initial(base, cell, schemas)
        read_call = base["primary"]
        after = [*messages, {"role": "assistant", "content": "", "tool_calls": [read_call]},
                 {"role": "tool", "content": q["primary_content"], "error": None, "tool_call": read_call,
                  "primary_delivered": True}]
        lengths = []
        for transcript in (messages, after):
            # 384-token actor limit (Gate 1 amendment A2)
            chat, tools, _ = render(identity["label"], cell["adapter"], transcript, schemas)
            lengths.append(len(generation_request(tokenizer, identity["label"], chat, "actor", 384, tools)["pids"]))
        report.append({"cell": cell["id"], "prompt_tokens": lengths})
    return report


def run_worker(args, run, uuid, handle, append):
    status(run, "RUNNING_PROFILE", profile=args.profile, gpu=args.gpu, uuid=uuid, resume=append)
    out = run / ("model_" + args.profile)
    out.mkdir(exist_ok=append)
    call = [sys.executable, "-u", str(ROOT / "worker.py"), "--run", str(run), "--profile", args.profile,
            "--gpu", str(args.gpu), "--uuid", uuid, "--native-python", args.native_python,
            "--batch-lanes", str(args.batch_lanes)]
    # Worker output goes to model_<profile>/worker.log (appended on resume) and is echoed to this log.
    with (out / "worker.log").open("a" if append else "w", encoding="utf-8") as log:
        if append:
            log.write(f"===== RESUME {datetime.now(timezone.utc).isoformat()} =====\n")
        proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
                                pass_fds=(handle.fileno(),), env=os.environ | {"CUDA_VISIBLE_DEVICES": uuid})
        for line in proc.stdout:
            log.write(line)
            log.flush()
            print(f"[{args.profile}] {line}", end="", flush=True)
        return proc.wait()


def finish(args, run, code):
    out = run / ("model_" + args.profile)
    if code:
        raise RuntimeError(f"GPU worker exited with {code}; see {out / 'worker.log'}")
    status(run, "ANALYZING")
    subprocess.run([sys.executable, str(ROOT / "analyze.py"), str(run)], check=True)
    status(run, "SMOKE_COMPLETE" if args.smoke else "GATE2_COMPLETE", profile=args.profile)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run", type=Path, required=True)
    p.add_argument("--profile", choices=tuple(MODELS), required=True)
    p.add_argument("--gpu", type=int, choices=tuple(PINNED_GPUS), required=True)
    p.add_argument("--cache", required=True)
    p.add_argument("--native-python", required=True)
    p.add_argument("--batch-lanes", type=int, default=24)
    p.add_argument("--smoke", action="store_true", help="Engineering pilot: 36 cells (3 bases); never science")
    p.add_argument("--resume", action="store_true",
                   help="Continue an existing run directory whose GPU worker died: same frozen plan and source "
                        "hashes required; completed cells are kept, the rest are rerun")
    p.add_argument("--wait-gpu-hours", type=float, default=12.0,
                   help="If GPU 3 is busy or reserved, wait up to this long (polling every 60 s) instead of failing")
    args = p.parse_args()
    run = args.run.resolve()
    if args.resume:
        freeze = read(run / "freeze.json")  # refuses a run that never froze
        changed = [n for n in SOURCE if freeze["source_sha256"].get(n) != file_hash(ROOT / n)]
        if changed:
            raise SystemExit(f"Refusing to resume {run}: source changed since freeze: {changed}")
        if digest(read(run / "gate2_plan.json")) != freeze["plan_sha256"] or freeze["smoke"] != args.smoke:
            raise SystemExit(f"Refusing to resume {run}: plan or smoke flag differs from the freeze")
    else:
        run.mkdir(parents=True, exist_ok=False)
    print(f"Run directory: {run}", flush=True)
    signal.signal(signal.SIGTERM, lambda signum, _: (_ for _ in ()).throw(KeyboardInterrupt(f"signal {signum}")))
    ownership, exit_code = ExitStack(), 1
    try:
        status(run, "RESUMING" if args.resume else "PREPARING", profile=args.profile, gpu=args.gpu, smoke=args.smoke)
        uuid = gpu_uuid(args.gpu)
        if uuid != PINNED_GPUS[args.gpu]:
            raise RuntimeError(f"GPU {args.gpu} UUID {uuid} is not the pinned device")
        locks = Path.home() / ".cache" / "ieee_sp" / "gpu_locks"
        locks.mkdir(parents=True, exist_ok=True)
        handle = ownership.enter_context((locks / (uuid + ".lock")).open("a"))
        deadline, last_note = time.monotonic() + args.wait_gpu_hours * 3600, 0.0
        while True:  # Wait for our lock and for GPU 3 to have no compute process. Never stops anyone.
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                require_idle_gpu(args.gpu, uuid)
                break
            except (BlockingIOError, RuntimeError) as exc:
                if isinstance(exc, RuntimeError):
                    fcntl.flock(handle, fcntl.LOCK_UN)
                if time.monotonic() > deadline:
                    raise RuntimeError(f"GPU {args.gpu} not available within {args.wait_gpu_hours} h: {exc}")
                if time.monotonic() - last_note > 300:
                    print(f"[{datetime.now(timezone.utc).isoformat()}] waiting for GPU {args.gpu}: {exc}", flush=True)
                    status(run, "WAITING_FOR_GPU", detail=str(exc))
                    last_note = time.monotonic()
                time.sleep(60)
        print(f"GPU {args.gpu} ({uuid}) reserved and idle", flush=True)
        plan = select_plan(args.smoke)
        if args.resume:
            if plan != read(run / "gate2_plan.json"):
                raise RuntimeError("Frozen plan differs from the run's plan")
            if read(run / "model_identity.json") != snapshot(args.cache, args.profile):
                raise RuntimeError("Model snapshot changed since the run started")
            with (run / "resume_log.jsonl").open("a") as f:
                f.write(digest({"t": time.time()}) + " " + datetime.now(timezone.utc).isoformat() + "\n")
        else:
            prepare(args, run, uuid, plan)
        finish(args, run, run_worker(args, run, uuid, handle, append=args.resume))
        exit_code = 0
    except (Exception, KeyboardInterrupt):
        status(run, "FAILED", error=traceback.format_exc())
        traceback.print_exc()
    finally:
        ownership.close()
        print(f"Archive: {archive(run)}", flush=True)
    raise SystemExit(exit_code)


def prepare(args, run, uuid, plan):
    """Freeze, snapshot the source, qualify the native worlds and the chat templates (new runs only)."""
    write(run / "gate2_plan.json", plan)
    write(run / "freeze.json", {"plan_sha256": digest(plan), "smoke": args.smoke,
                                "interface_amendments": ["A1-20261110: flat action ends at </ASSISTANT>; "
                                                         "role (Qwen) multi-call turns executed in order",
                                                         "A1b-20261110: flat output complete if its turn closed "
                                                         "before the token limit",
                                                         "A2-20261110: actor generation limit 384 tokens (was 160)",
                                                         "G2V2-20261111: Gate 2 V2 design (role adapter only; "
                                                         "candidates C0,C1,C2,C3,C3x,C4; tool/user_all; "
                                                         "linkage 0; addback/surgical arms)",
                                                         "AV2.1-20261111: analysis amendment before data "
                                                         "(eligible T0 denominator; attempt-level H-SUB; absolute "
                                                         "hijacking support >=5 B in >=4 templates, >=2 families)"],
                                "source_sha256": {n: file_hash(ROOT / n) for n in SOURCE}})
    write(run / "invocation.json", vars(args) | {"run": str(run), "python": sys.version,
                                                "platform": platform.platform(), "gpu_uuid": uuid,
                                                "stack_origin": os.environ.get("E0_STACK_ORIGIN")})
    for name in SOURCE:
        dst = run / "source" / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, dst)

    status(run, "NATIVE_QUALIFICATION")
    from bridge.live import qualify_runtime
    qualify_runtime(args.native_python, run, plan)
    identity = snapshot(args.cache, args.profile)
    write(run / "model_identity.json", identity)
    status(run, "TEMPLATE_PREFLIGHT")
    # Tool schemas per base and read-tool kind (text_only cells use plain-document reads).
    plan_ext = plan | {"_qualification": str(run / "native_qualification.json"), "_schemas": {}}
    from bridge.gate2_plan import CARRIER, effective_base
    from bridge.live import Native
    with Native(args.native_python, run / "native_schemas.log") as rt:
        for base in plan["bases"]:
            carrier = CARRIER[base["family"]]
            cell = {"carrier": carrier, "source": 1, "linked": 0, "copy": 1, "attack": 0, "flex": 0}
            plan_ext["_schemas"][(base["id"], carrier == "text_only")] = \
                rt.open(effective_base(base, cell), cell)["schemas"]
    preflight = template_preflight(identity, plan_ext)
    write(run / "template_preflight.json", preflight)
    longest = max(max(r["prompt_tokens"]) for r in preflight)
    if longest + 384 > 8192:
        raise RuntimeError(f"Actor prompt of {longest} tokens leaves no room under the 8192-token limit")



if __name__ == "__main__":
    main()
