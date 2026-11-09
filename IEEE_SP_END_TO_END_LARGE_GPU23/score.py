"""Local boundary-exact teacher-forced scorer. One model per process."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
import os
import random
import re
import subprocess
from time import monotonic

from design import MODELS, digest, read, write

BATCH = 32
SCORE_TOKEN_BUDGET = 16384
SCORE_LOGIT_ROWS = 2048
HEADROOM = 12 * 1024**3


def file_hash(path):
    with Path(path).open("rb") as f:
        from hashlib import file_digest
        return file_digest(f, "sha256").hexdigest()


def cached_file(path, repo, shared_blobs):
    try:
        target = path.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise ValueError(f"Cannot resolve cached file {path}: {exc}") from exc
    if not target.is_file() or not (
        target.is_relative_to(repo) or target.is_relative_to(shared_blobs)
    ):
        raise ValueError(f"Invalid cached file {path} -> {target}; expected a regular file "
                         f"under {repo} or {shared_blobs}")
    return target


def snapshot(cache, label, revision=None):
    profile = MODELS[label]
    cache_root = Path(cache).resolve()
    base = cache_root / ("models--" + profile["hub"].replace("/", "--"))
    shared_blobs = cache_root / "blobs"
    rev = revision if label == "gemma" and revision is not None else profile["revision"]
    if not re.fullmatch(r"[a-f0-9]{40}", rev):
        raise ValueError(f"Invalid cached revision for {label}: {rev}")
    snap = base / "snapshots" / rev
    if not snap.is_dir():
        raise FileNotFoundError(f"Missing cached {profile['hub']} revision {rev} at {snap}")
    required = ["config.json", "tokenizer.json", "tokenizer_config.json"]
    index = snap / "model.safetensors.index.json"
    if index.exists() or index.is_symlink():
        shards = sorted(set(read(cached_file(index, base, shared_blobs))["weight_map"].values()))
        required.append(index.name)
    else:
        shards = ["model.safetensors"]
    if not shards or any(not re.fullmatch(r"model(?:-\d+-of-\d+)?\.safetensors", name) for name in shards):
        raise ValueError("Invalid safetensor filenames in the cached weight index")
    files = {}
    extra = ["special_tokens_map.json", "added_tokens.json", "tokenizer.model", "vocab.json", "merges.txt",
             "chat_template.jinja", "chat_template.json", "generation_config.json", "processor_config.json"]
    for name in [*required, *shards, *(name for name in extra if (snap / name).exists()
                                       or (snap / name).is_symlink())]:
        blob = cached_file(snap / name, base, shared_blobs)
        st = blob.stat()
        files[name] = {"bytes": st.st_size, "identity": blob.name, "mtime_ns": st.st_mtime_ns,
                       "cache_relative_path": blob.relative_to(cache_root).as_posix()}
        if name not in shards:
            files[name]["sha256"] = file_hash(blob)
    return {"label": label, "hub": profile["hub"], "role": profile["role"], "revision": rev,
            "path": str(snap), "files": files, "weights_bytes": sum(files[k]["bytes"] for k in shards)}


def gpu_uuid(index):
    uuid = subprocess.check_output(["nvidia-smi", "-i", str(index), "--query-gpu=uuid",
                                   "--format=csv,noheader"], text=True).strip()
    if not re.fullmatch(r"GPU-[a-fA-F0-9-]+", uuid):
        raise RuntimeError(f"Could not resolve physical GPU {index} to one UUID")
    return uuid


def require_idle_gpu(index, uuid, *, own_pid=None):
    active = subprocess.check_output(["nvidia-smi", "-i", uuid, "--query-compute-apps=pid",
                                      "--format=csv,noheader,nounits"], text=True)
    lines = [line.strip() for line in active.splitlines() if line.strip()]
    if any(not line.isdigit() and line != "No running processes found" for line in lines):
        raise RuntimeError(f"Could not verify active compute processes on GPU {index}: {active.strip()}")
    other = [int(line) for line in lines if line.isdigit() and int(line) != own_pid]
    if other:
        raise RuntimeError(f"GPU {index} already has compute processes: {other}")


def check_gpu(index, uuid):
    import torch

    if os.environ.get("CUDA_VISIBLE_DEVICES") != uuid or torch.cuda.device_count() != 1:
        raise RuntimeError("Expected one visible CUDA device and the pinned GPU UUID")
    if gpu_uuid(index) != uuid or not torch.cuda.is_bf16_supported():
        raise RuntimeError(f"GPU {index} identity or BF16 capability changed")
    require_idle_gpu(index, uuid, own_pid=os.getpid())


def logprobs(model, requests, device):
    import torch

    n = len(requests[0]["cids"])
    p = len(requests[0]["pids"])
    if not n or not p or any(len(r["cids"]) != n or len(r["pids"]) != p for r in requests):
        raise ValueError("Batch requires identical prompt and completion lengths")
    inputs = torch.tensor([r["pids"] + r["cids"] for r in requests], device=device)
    with torch.inference_mode():
        tail = model(input_ids=inputs, use_cache=False, logits_to_keep=n + 1).logits
        if tuple(tail.shape[:2]) != (len(requests), n + 1):
            raise RuntimeError("Model ignored suffix-logit contract")
        logits = tail[:, :-1, :].float()
        targets = inputs[:, p:].unsqueeze(-1)
        values = logits.gather(-1, targets).squeeze(-1) - torch.logsumexp(logits, dim=-1)
        if not bool(torch.isfinite(values).all()):
            raise RuntimeError("Non-finite completion log probability")
        return values.cpu().tolist()


def load_model(identity, device):
    import torch
    from transformers import AutoModelForCausalLM, Gemma3ForConditionalGeneration

    config = read(Path(identity["path"]) / "config.json")
    expected = {"qwen": ("qwen3", "Qwen3ForCausalLM"), "gemma": ("gemma3", "Gemma3ForConditionalGeneration")}
    model_type, architecture = expected[identity["label"]]
    if config["model_type"] != model_type or architecture not in config.get("architectures", []):
        raise RuntimeError(f"Cached model architecture is incompatible with {identity['hub']}")
    if config.get("quantization_config"):
        raise RuntimeError("Frozen profile expects unquantized BF16 weights")
    cls = AutoModelForCausalLM if identity["label"] == "qwen" else Gemma3ForConditionalGeneration
    return cls.from_pretrained(identity["path"], local_files_only=True, trust_remote_code=False,
                               use_safetensors=True, dtype=torch.bfloat16, attn_implementation="sdpa",
                               device_map={"": device}).eval()


def score_batch_limit(prompt_tokens, completion_tokens):
    return max(1, min(BATCH, SCORE_TOKEN_BUDGET // (prompt_tokens + completion_tokens),
                      SCORE_LOGIT_ROWS // (completion_tokens + 1)))


def batches(requests, seed, batch_size=BATCH):
    grouped = defaultdict(list)
    for key, request in requests.items():
        grouped[len(request["pids"]), len(request["cids"])].append(key)
    rng = random.Random(seed)
    jobs = []
    for (p, n), ids in grouped.items():
        rng.shuffle(ids)
        size = min(batch_size, score_batch_limit(p, n))
        jobs.extend(ids[i:i + size] for i in range(0, len(ids), size))
    rng.shuffle(jobs)
    return jobs


def main():
    from bridge.batching import (DEFAULT_LANES, FIXED_SCORE_WINDOW, GENERATION_TOKEN_BUDGET, MAX_LANES,
                                 REPLAY_CACHE_ENTRIES, BatchEngine, bounded_inference)
    from bridge.live import run_bridge
    from run import status

    p = argparse.ArgumentParser()
    p.add_argument("--model-dir", required=True, type=Path)
    p.add_argument("--cache", required=True)
    p.add_argument("--gpu-index", required=True, type=int, choices=(2, 3))
    p.add_argument("--gpu-uuid", required=True)
    p.add_argument("--native-python", required=True)
    p.add_argument("--batch-lanes", type=int, default=DEFAULT_LANES)
    args = p.parse_args()
    if not 1 <= args.batch_lanes <= MAX_LANES:
        p.error(f"--batch-lanes must be between 1 and {MAX_LANES}")
    out = args.model_dir
    freeze = read(out / "freeze.json")
    identity = freeze["identity"]
    binding = read(out.parent / "gpu_bindings.json")[identity["label"]]
    if binding != {"index": args.gpu_index, "uuid": args.gpu_uuid}:
        raise RuntimeError("Scorer arguments disagree with the controller's GPU binding")
    if identity != snapshot(args.cache, identity["label"], identity["revision"]):
        raise RuntimeError("Local snapshot changed after pre-outcome preparation")
    if file_hash(out / "prepared.json") != freeze["prepared_sha256"]:
        raise RuntimeError("Prepared requests changed after freeze")
    prepared = read(out / "prepared.json")
    check_gpu(args.gpu_index, args.gpu_uuid)
    import torch
    import transformers
    from transformers import AutoTokenizer

    device = "cuda:0"
    free, total = torch.cuda.mem_get_info()
    if free < identity["weights_bytes"] + HEADROOM:
        raise RuntimeError(f"GPU {args.gpu_index} has {free // 1024**3} GiB free, insufficient for this fixed BF16 profile")
    write(out / "runtime.json", {"torch": torch.__version__, "transformers": transformers.__version__,
                                 "gpu": torch.cuda.get_device_name(), "uuid": args.gpu_uuid,
                                 "physical_gpu": args.gpu_index,
                                 "free_bytes": free, "total_bytes": total,
                                 "dtype": "bfloat16", "attention": "sdpa", "batch_size_max": BATCH,
                                 "score_token_budget": SCORE_TOKEN_BUDGET, "score_logit_rows": SCORE_LOGIT_ROWS,
                                 "batch_lanes": args.batch_lanes, "generation_token_budget": GENERATION_TOKEN_BUDGET,
                                 "fixed_score_window": FIXED_SCORE_WINDOW, "replay_cache_entries": REPLAY_CACHE_ENTRIES,
                                 "batch_scheduler": "deterministic-slot-rounds-v2"})
    status(out, "LOADING_MODEL", physical_gpu=args.gpu_index, gpu_uuid=args.gpu_uuid)
    model = load_model(identity, device)
    requests = prepared["requests"]
    anchor_ids = {r["request"] for r in prepared["anchors"]}
    first = requests[next(iter(sorted(anchor_ids)))]
    self_a, self_b = (logprobs(model, [first], device)[0] for _ in range(2))
    drift = max(abs(a - b) for a, b in zip(self_a, self_b))
    score_stats = Counter()
    probe_batches = list(bounded_inference([first, first], lambda batch: logprobs(model, batch, device), score_stats))
    batch_scores = [row for _, values in probe_batches for row in values]
    batch_drift = max(abs(a - b) for row in batch_scores for a, b in zip(self_a, row))
    write(out / "numerical_preflight.json", {"same_input_max_abs_logp_drift": drift,
                                             "serial_vs_batch_max_abs_logp_drift": batch_drift,
                                             "probe_batch_sizes": [len(batch) for batch, _ in probe_batches],
                                             "first": self_a, "second": self_b, "batch": batch_scores})
    if drift > 0.002:
        raise RuntimeError("Identical-input numerical drift exceeds preflight tolerance")

    tokenizer = AutoTokenizer.from_pretrained(identity["path"], local_files_only=True, trust_remote_code=False,
                                              use_fast=True)
    bridge = out / "bridge"
    bridge.mkdir()
    engine = BatchEngine(model, tokenizer, device, bridge, identity["label"], args.batch_lanes)
    try:
        generation_probe = engine.qualify_generation()
        write(out / "generation_preflight.json", generation_probe)
        if not generation_probe["exact_match"]:
            print("Serial and batched greedy generation differ on a preflight probe; see generation_preflight.json",
                  flush=True)

        status(out, "MECHANISM_SCORING", physical_gpu=args.gpu_index)
        target = out / "batches"
        target.mkdir(exist_ok=False)
        anchor = {k: v for k, v in requests.items() if k in anchor_ids}
        holdout = {k: v for k, v in requests.items() if k not in anchor_ids}
        order = batches(anchor, 101) + batches(holdout, 20261107)
        count = 0
        started = monotonic()
        for index, keys in enumerate(order):
            batch = [requests[k] for k in keys]
            lp = []
            for actual, values in bounded_inference(batch, lambda rows: logprobs(model, rows, device), score_stats):
                lp.extend(values)
                score_stats["batches"] += 1
                score_stats["max_batch"] = max(score_stats["max_batch"], len(actual))
            write(target / f"{index:06d}.json", dict(zip(keys, lp, strict=True)))
            count += len(keys)
            elapsed = monotonic() - started
            write(out / "progress.json", {"scored": count, "total": len(requests), **dict(score_stats),
                                          "elapsed_seconds": round(elapsed),
                                          "eta_seconds": round(elapsed * (len(requests) - count) / count)
                                          if index >= 15 or count == len(requests) else None})
            if index % 20 == 0 or count == len(requests):
                print(f"{identity['label']} scored {count}/{len(requests)}", flush=True)

        status(out, "NATIVE_BRIDGE", physical_gpu=args.gpu_index)
        print(f"{identity['label']} starting the native bridge with {args.batch_lanes} batch lanes", flush=True)
        plan = read(out.parent / "bridge_plan.json")
        if digest(plan) != read(out.parent / "bridge_freeze.json")["plan_sha256"]:
            raise RuntimeError("Bridge plan changed after pre-outcome freeze")
        run_bridge(engine, args.native_python, bridge, plan)
    finally:
        engine.close()


if __name__ == "__main__":
    main()
