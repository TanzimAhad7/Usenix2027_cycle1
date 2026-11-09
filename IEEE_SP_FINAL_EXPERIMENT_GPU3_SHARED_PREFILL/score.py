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
    h = sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def padded_logprobs(model, requests, device, pad):
    """Batch ragged inputs while keeping original positions and completion boundaries."""
    if len(requests) == 1:
        return logprobs(model, requests, device)
    import torch

    completions = [len(row["cids"]) for row in requests]
    lengths = [len(row["pids"]) + n for row, n in zip(requests, completions, strict=True)]
    if not all(0 < n < length for n, length in zip(completions, lengths, strict=True)):
        raise ValueError("Each score requires a nonempty prompt and continuation")
    width, tail = max(lengths), max(completions)
    offsets = [width - length for length in lengths]
    inputs = torch.tensor([[pad] * offset + row["pids"] + row["cids"]
                           for offset, row in zip(offsets, requests, strict=True)], device=device)
    mask = torch.arange(width, device=device)[None, :] >= torch.tensor(offsets, device=device)[:, None]
    positions = (mask.long().cumsum(-1) - 1).clamp_min(0)
    with torch.inference_mode():
        logits = model(input_ids=inputs, attention_mask=mask.long(), position_ids=positions,
                       use_cache=False, logits_to_keep=tail + 1).logits
        if tuple(logits.shape[:2]) != (len(requests), tail + 1):
            raise RuntimeError("Model ignored suffix-logit contract")
        logits = logits[:, :-1].float()
        targets = inputs[:, -tail:].unsqueeze(-1)
        values = logits.gather(-1, targets).squeeze(-1) - torch.logsumexp(logits, dim=-1)
        selected = torch.arange(tail, device=device)[None, :] >= (
            tail - torch.tensor(completions, device=device)[:, None])
        if not bool(torch.isfinite(values[selected]).all()):
            raise RuntimeError("Non-finite completion log probability")
        return [row[-n:] for row, n in zip(values.cpu().tolist(), completions, strict=True)]


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


