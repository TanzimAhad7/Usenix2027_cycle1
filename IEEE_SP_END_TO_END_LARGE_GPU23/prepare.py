"""Compile matched, boundary-safe token requests before scoring."""
from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from hashlib import sha256
from pathlib import Path

from design import Cell, blocks, digest, grant, make_action, read, ROOT

TARGET = "<ASSISTANT_TARGET_ACTION>\n"
MAX_TOKENS = 1536


def action_tokenization(tokenizer, text, spans):
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


def wrapped(block, n):
    tag, text = block
    return f"<{tag}>\n{text}\nALIGNMENT:" + " neutral" * n + f"\n</{tag}>\n"


def balanced_blocks(tokenizer, sections):
    """Balance each position's token budget, with a shared budget for both evidence slots."""
    positions = [set() for _ in range(3)]
    mapping = (0, 1, 2, 1)
    for parts in sections:
        for index, block in enumerate(parts):
            if block is not None:
                positions[mapping[index]].add(block)
    output = []
    for variants in positions:
        candidates = {}
        for block in sorted(variants):
            texts = [wrapped(block, n) for n in range(128)]
            token_ids = tokenizer(texts, add_special_tokens=False, return_attention_mask=False,
                                  return_token_type_ids=False)["input_ids"]
            encodings = {}
            for text, ids in zip(texts, token_ids, strict=True):
                encodings.setdefault(len(ids), text)
            candidates[block] = encodings
        common = set.intersection(*(set(c) for c in candidates.values()))
        if not common:
            raise ValueError("No common tokenizer-specific block length")
        budget = min(common)
        output.append({block: (candidates[block][budget], budget) for block in candidates})
    return output, mapping


def compile_panel(manifest, tokenizer, label):
    if not tokenizer.is_fast:
        raise ValueError("Exact fast-tokenizer offsets are required")

    @lru_cache(maxsize=16384)
    def enc(text, special):
        return tuple(tokenizer.encode(text, add_special_tokens=special))

    all_cells = defaultdict(list)
    for row in manifest["cells"]:
        raw = row.copy()
        identifier = raw.pop("id")
        cell = Cell(**raw)
        if identifier != cell.id:
            raise ValueError("Cell identity changed")
        all_cells[cell.base].append(cell)
    requests, observations = {}, []

    def record(prompt, pids, action):
        if not pids or len(pids) + len(action["cids"]) > MAX_TOKENS:
            raise ValueError("Request would exceed the frozen context budget")
        key = digest([pids, action["cids"]])
        requests.setdefault(key, {"prompt": prompt, "pids": list(pids), "cids": action["cids"]})
        return key

    for base in manifest["bases"]:
        bs = all_cells[base["base"]]
        sections = {(c.id, v): blocks(base, c, v) for c in bs for v in c.variants()}
        padded, indices = balanced_blocks(tokenizer, sections.values())
        prefix = grant(base)
        prefix_tokens = enc(prefix, True)
        suffix = enc(TARGET, False)
        actions = {fmt: action_tokenization(tokenizer, *make_action(base, fmt)) for fmt in ("compact", "pretty")}
        for cell in bs:
            action = actions[cell.action_format]
            reqs = {}
            for variant in cell.variants():
                components = [padded[indices[i]][block] for i, block in enumerate(sections[cell.id, variant]) if block]
                prompt = prefix + "".join(text for text, _ in components) + TARGET
                pids = enc(prompt, True)
                if pids[:len(prefix_tokens)] != prefix_tokens or pids[-len(suffix):] != suffix:
                    raise ValueError(f"Tokenizer merged a grant or action boundary for {cell.id}/{variant}")
                seg = prefix
                expected_count = len(prefix_tokens)
                for text, size in components:
                    seg += text
                    expected_count += size
                    seg_ids = enc(seg, True)
                    if len(seg_ids) != expected_count or pids[:expected_count] != seg_ids:
                        raise ValueError(f"Tokenizer changed block boundaries for {cell.id}/{variant}")
                if len(pids) != expected_count + len(suffix):
                    raise ValueError("Measured and frozen lengths diverged")
                if cell.panel != "echo":
                    focal = str(base[cell.focal])
                    expected_literal = cell.lexical == "literal" and variant not in {
                        "mask_" + cell.source, "delete_" + cell.source
                    }
                    if prompt.count(focal) != int(expected_literal):
                        raise ValueError(f"Unexpected exact focal copy for {cell.id}/{variant}")
                reqs[variant] = record(prompt, pids, action)
            observations.append({"id": cell.id, "family": base["family"], "template": base["template"],
                                 "action": action, "requests": reqs})

    anchors = []
    for row in read(ROOT / "data" / "legacy_anchors.json")["rows"]:
        prefix_hash = sha256(row["prompt"].encode()).hexdigest()
        completion_hash = sha256(row["completion"].encode()).hexdigest()
        if (prefix_hash, completion_hash) != (row["prompt_sha256"], row["completion_sha256"]):
            raise ValueError("Archived anchor text drift")
        pids = enc(row["prompt"], True)
        action = action_tokenization(tokenizer, row["completion"], {})
        hist = row["historical"]
        prompt_match = digest(pids) == hist["prompt_token_ids_sha256"]
        completion_match = action["cids"] == hist["completion_token_ids"]
        anchors.append({"condition": row["condition"], "base": row["base"], "source": row["source"],
                        "echo": row["echo"], "variant": row["variant"], "prompt_match": prompt_match,
                        "completion_match": completion_match, "historical": hist["completion_token_logprobs"],
                        "request": record(row["prompt"], pids, action)})
    return {"label": label, "design": digest(manifest), "observations": observations, "anchors": anchors,
            "requests": requests, "context_budget": MAX_TOKENS}
