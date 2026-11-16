"""Gate 1 GPU worker: one model profile on one pinned GPU. Started by run.py only."""
from __future__ import annotations

import argparse
from pathlib import Path

from common import digest, read, write
from score import check_gpu, load_model, snapshot

HEADROOM = 12 * 1024**3


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run", type=Path, required=True)
    p.add_argument("--profile", required=True)
    p.add_argument("--gpu", type=int, required=True)
    p.add_argument("--uuid", required=True)
    p.add_argument("--native-python", required=True)
    p.add_argument("--batch-lanes", type=int, required=True)
    args = p.parse_args()
    run, out = args.run, args.run / ("model_" + args.profile)
    plan = read(run / "gate1_plan.json")
    if digest(plan) != read(run / "freeze.json")["plan_sha256"]:
        raise RuntimeError("Plan changed after freeze")
    identity = read(run / "model_identity.json")
    if identity != snapshot(read(run / "invocation.json")["cache"], args.profile):
        raise RuntimeError("Model snapshot changed after freeze")
    check_gpu(args.gpu, args.uuid)

    import torch
    import transformers
    from transformers import AutoTokenizer
    from bridge.batching import BatchEngine
    from bridge.live import run_gate1

    free, total = torch.cuda.mem_get_info()
    if free < identity["weights_bytes"] + HEADROOM:
        raise RuntimeError(f"GPU {args.gpu} has {free // 1024**3} GiB free; insufficient for the BF16 profile")
    write(out / "runtime.json", {"torch": torch.__version__, "transformers": transformers.__version__,
                                 "gpu": torch.cuda.get_device_name(), "uuid": args.uuid, "physical_gpu": args.gpu,
                                 "free_bytes": free, "total_bytes": total, "dtype": "bfloat16", "attention": "sdpa",
                                 "decoding": "greedy", "batch_lanes": args.batch_lanes})
    model = load_model(identity, "cuda:0")
    tokenizer = AutoTokenizer.from_pretrained(identity["path"], local_files_only=True, trust_remote_code=False,
                                              use_fast=True)
    engine = BatchEngine(model, tokenizer, "cuda:0", out, args.profile, args.batch_lanes)
    try:
        probe = engine.qualify_generation()
        write(out / "generation_preflight.json", probe)
        if not probe["exact_match"]:
            print("Serial and batched greedy generation differ on the preflight probe (recorded; continuing, "
                  "as in the E13/E14 bridge)", flush=True)
        run_gate1(engine, args.native_python, out, plan)
    finally:
        engine.close()
    write(out / "status.json", {"phase": "PROFILE_COMPLETE"})


if __name__ == "__main__":
    main()
