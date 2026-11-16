"""Shared helpers. canonical/digest/write/read and MODELS are copied verbatim from
IEEE_SP_END_TO_END_LARGE_GPU23/design.py so digests are comparable with the E13/E14 bridge."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODELS = {
    "qwen": {"hub": "Qwen/Qwen3-32B", "revision": "9216db5781bf21249d130ec9da846c4624c16137", "role": "transfer"},
    "gemma": {"hub": "google/gemma-3-27b-it", "revision": "005ad3404e59d6023443cb575daa05336842228a",
              "role": "transfer"},
}
# The only physical GPU this package may use (user instruction, 10 Nov 2026): GPU 3, pinned by UUID.
PINNED_GPUS = {3: "GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6"}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def write(path, value):
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(canonical(value) + "\n", encoding="utf-8")
    tmp.replace(path)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def action_tokenization(tokenizer, text, spans):
    """Verbatim from IEEE_SP_END_TO_END_LARGE_GPU23/prepare.py."""
    enc = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
    roles, strict = [], []
    for start, stop in enc["offset_mapping"]:
        hits = [name for name, (a, b) in spans.items() if max(a, start) < min(b, stop)]
        role = hits[0] if len(hits) == 1 else "other"
        roles.append(role)
        strict.append(role if role in spans and spans[role][0] <= start < stop <= spans[role][1] else "other")
    if spans and any(role not in roles for role in spans):
        raise ValueError("A scored value has no attributable token")
    if len(roles) != len(enc["input_ids"]) or not roles:
        raise ValueError("Invalid completion offset mapping")
    return {"completion": text, "cids": enc["input_ids"], "roles": roles, "strict_roles": strict,
            "offsets": [list(pair) for pair in enc["offset_mapping"]]}
