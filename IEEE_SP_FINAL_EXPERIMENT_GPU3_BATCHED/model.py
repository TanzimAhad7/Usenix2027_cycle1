"""Local scoring and an explicit interface for independently qualified guard adapters."""
from collections import Counter
from copy import deepcopy
import json
import math
import os
import select
from pathlib import Path
import re
import subprocess
from types import SimpleNamespace

from bridge.batching import BlockEngine
from bridge.historical import action_string, context_serializer
from design import MARGIN_TOLERANCE, ROOT, compact, digest, read
from prepare import action_tokenization
from score import file_hash

CONFIG = read(ROOT / "data" / "historical_guard.json")["detector"]


def parse(text):
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text.strip(), re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence[1]

    def unique(pairs):
        d = dict(pairs)
        if len(d) != len(pairs):
            raise ValueError("Duplicate JSON key")
        return d

    try:
        obj = json.loads(text, object_pairs_hook=unique)
        compact(obj)
    except (ValueError, TypeError, RecursionError):
        return None
    if not isinstance(obj, dict):
        return None
    if set(obj) == {"final"} and isinstance(obj["final"], str):
        return obj
    if set(obj) == {"function", "args"} and isinstance(obj["function"], str) and isinstance(obj["args"], dict):
        return obj
    return None


def historical(messages):
    rows = []
    for msg in messages:
        row = dict(msg)
        if "tool_calls" in row:
            row["tool_calls"] = [SimpleNamespace(**x) for x in row["tool_calls"]]
        if "tool_call" in row:
            row["tool_call"] = SimpleNamespace(**row["tool_call"])
        rows.append(row)
    return rows


def action_tokens(tokenizer, base, action):
    text = action_string(SimpleNamespace(**action))
    cursor = len(action["function"]) + 2
    spans = {}
    for key, value in sorted(action["args"].items()):
        rendered = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        start = cursor + len(json.dumps(key, ensure_ascii=False)) + 1
        end = start + len(rendered)
        cursor = end + 1
        role = "identifier" if key == base["identifier"] else "parameter" if key == base["parameter"] else None
        if role and isinstance(value, str):
            spans[role] = start + 1, end - 1
        elif role and isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
            spans[role] = start + 2, end - 2
        elif role and isinstance(value, (int, float)) and not isinstance(value, bool):
            spans[role] = start, end
    return action_tokenization(tokenizer, text, {r: (a, b) for r, (a, b) in spans.items() if a < b})


def masks(vector, roles):
    chosen = [i for i, role in enumerate(roles) if role == "identifier"]
    others = [i for i, role in enumerate(roles) if role == "other"]
    if not chosen or len(others) < len(chosen):
        return None
    distance = lambda i: (min(abs(i-j) for j in chosen), i)
    equal = sorted(others, key=distance)[:len(chosen)]
    available = set(others)
    matched = []
    for i in sorted(chosen, key=lambda j: -abs(vector[j])):
        same_sign = [j for j in available if vector[i] * vector[j] > 0 or vector[i] == vector[j] == 0]
        if not same_sign:
            break
        j = min(same_sign, key=lambda j: (abs(vector[j] - vector[i]), distance(j)))
        matched.append(j)
        available.remove(j)
    total = lambda indices: math.fsum(vector[i] for i in indices) / len(vector)
    gap = abs(total(matched) - total(chosen)) if len(matched) == len(chosen) else None
    return {"remove_id": chosen, "equal_placebo": equal,
            "margin_placebo": matched if gap is not None and gap <= MARGIN_TOLERANCE else None,
            "margin_gap": gap}


class LocalBlock(BlockEngine):
    def actor(self, messages, seed):
        prompt = context_serializer(historical(messages)).removesuffix("<ASSISTANT_ACTION>\n")
        r = yield from self.generate([{"role": "user", "content": prompt}], "actor", seed)
        return {"raw": r, "proposal": None if r["limit_reached"] else parse(r["text"])}

    def scoring(self, base, messages, proposal):
        result, = yield from self.scoring_many(base, messages, [proposal])
        return result

    def scoring_many(self, base, messages, proposals):
        indices = [i for i, m in enumerate(messages) if m["role"] == "tool" and not m.get("error")]
        if not indices:
            return [{"spans": [], "flags": [], "action": None} for _ in proposals]
        tokenizations = [action_tokens(self.tokenizer, base, proposal) for proposal in proposals]
        hist = historical(messages)
        prefixes = [context_serializer(hist), context_serializer(hist, ablate_user=True),
                    *(context_serializer(hist, ablate_tool_message_index=i) for i in indices)]
        scores = yield from self.score_actions(prefixes, [tokens["cids"] for tokens in tokenizations])
        return [self.summarize_scores(messages, indices, tokens, ids, values)
                for tokens, (ids, values) in zip(tokenizations, scores, strict=True)]

    @staticmethod
    def summarize_scores(messages, indices, tokens, ids, values):
        roles = tokens["strict_roles"]
        n = len(roles)
        u = math.fsum(a-b for a,b in zip(values[0], values[1], strict=True)) / n
        spans = []
        for idx, vector, request_id in zip(indices, values[2:], ids[2:], strict=True):
            delta = [a-b for a,b in zip(values[1], vector, strict=True)]
            scalar = math.fsum(delta) / n
            parts = {r: math.fsum(v for v,k in zip(delta, roles, strict=True) if r == k) / n
                     for r in ("identifier", "parameter", "other")}
            patch = masks(delta, roles) if messages[idx].get("primary") else None
            changed = {arm: scalar - math.fsum(delta[k] for k in patch[arm]) / n
                       if patch and patch[arm] is not None else (None if messages[idx].get("primary") else scalar)
                       for arm in ("remove_id", "equal_placebo", "margin_placebo")}
            spans.append({"index": idx, "request": request_id, "primary": bool(messages[idx].get("primary")),
                          "delta_user": u, "delta_tool": scalar+u, "scalar": scalar, "parts": parts,
                          "patch_tokens": patch, "patched": changed})
        return {"spans": spans, "flags": [s["index"] for s in spans if s["scalar"] > 0],
                "action": tokens, "full_request": ids[0], "no_user_request": ids[1]}

    def clean(self, messages, flags, seed):
        changed, receipts = deepcopy(messages), []
        for idx in flags:
            msg = changed[idx]
            prompt = CONFIG["sanitizer_user_template"].format(
                user_request=messages[1]["content"], tool_name=msg["tool_call"]["function"],
                untrusted_content=msg["content"])
            r = yield from self.generate([{"role": "user", "content": CONFIG["sanitizer_system_prompt"]
                                          + "\n\n" + prompt}], "sanitizer", None)
            receipts.append({"index": idx, "generation": r})
            if r["limit_reached"] or not r["text"].strip():
                return {"messages": None, "receipts": receipts}
            msg["content"] = r["text"]
        for msg in changed[min(flags)+1:]:
            if msg["role"] == "assistant" and msg["content"].strip():
                msg["content"] = CONFIG["cot_mask_placeholder"]
        return {"messages": changed, "receipts": receipts}


class Adapter:
    """JSON-lines process started from an explicit, content-bound argv manifest."""
    def __init__(self, config, out):
        self.spec = read(config)
        self.out = out
        self.label = "supported"
        self.stats = Counter()
        argv = self.spec["argv"]
        bound = self.spec["files"]
        if not argv or not bound or not Path(argv[0]).is_absolute():
            raise ValueError("Adapter argv must be absolute and executable sources must be hashed")
        indices = self.spec["source_argument_indices"]
        if not indices or not set(argv[i] for i in indices) <= set(bound):
            raise ValueError("At least one adapter source argument must be content-bound")
        for path, expected in bound.items():
            if not Path(path).is_absolute() or file_hash(path) != expected:
                raise ValueError(f"Adapter content hash mismatch: {path}")
        if not self.spec.get("provenance") or not self.spec.get("implementation_revision"):
            raise ValueError("Missing comparator provenance and version")
        self.log = (out / "adapter_stderr.log").open("a")
        self.stream = (out / "adapter_wire.jsonl").open("a")
        try:
            self.process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.log,
                                            encoding="utf-8", cwd=ROOT, env=os.environ)
        except BaseException:
            self.log.close()
            self.stream.close()
            raise
        try:
            self.identity = self.call("describe", {})
            required = {"implementation", "revision", "actor", "scorer", "sanitizer", "normalization",
                        "serialization", "threshold", "runtime"}
            if not required <= set(self.identity):
                raise ValueError("Adapter runtime identity is incomplete")
            if self.identity != self.spec["expected_identity"]:
                raise ValueError("Adapter runtime identity does not match the frozen receipt")
            self.qualify()
        except BaseException:
            self.close()
            raise

    def qualify(self):
        probes = self.spec["probes"]
        if not self.spec.get("reference_evidence") or {x["op"] for x in probes} != {"actor", "score", "clean"}:
            raise ValueError("Supply externally referenced actor, score and sanitizer probes")
        score_flags = {bool(x["expected"]["flags"]) for x in probes if x["op"] == "score"}
        if score_flags != {False, True}:
            raise ValueError("Provide reference score probes on both sides of the routing boundary")
        for probe in probes:
            result = self.call(probe["op"], probe["input"])
            if result != probe["expected"]:
                raise ValueError("Adapter reference probe failed: " + probe["op"])

    def call(self, op, inputs):
        nonce = self.stats["requests"]
        request = {"id": nonce, "op": op, "input": inputs}
        self.stats["requests"] += 1
        self.process.stdin.write(compact(request) + "\n")
        self.process.stdin.flush()
        # Bound silent adapters without ever retrying a model call.
        if not select.select([self.process.stdout], [], [], 180)[0]:
            raise TimeoutError(f"Adapter timed out on {op}")
        response = json.loads(self.process.stdout.readline())
        self.stream.write(compact({"request": request, "response": response}) + "\n")
        self.stream.flush()
        if response.get("id") != nonce or "result" not in response:
            raise RuntimeError("Malformed adapter response")
        return response["result"]

    def resolve(self, requests):
        return {key: self.call(req["kind"], req["input"]) for key, req in requests.items()}

    def close(self):
        try:
            self.process.stdin.close()
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()
        finally:
            self.process.stdout.close()
            self.stream.close()
            self.log.close()


class AdapterBlock:
    def __init__(self, condition):
        self.condition = condition

    def request(self, kind, **inputs):
        key = digest([kind, inputs])
        results = yield ({"id": key, "kind": kind, "condition": self.condition, "input": inputs},)
        return results[key]

    def actor(self, messages, seed):
        return (yield from self.request("actor", messages=messages, seed=seed))

    def scoring(self, base, messages, proposal):
        score = yield from self.request("score", messages=messages, proposal=proposal,
                                        roles={k: base[k] for k in ("identifier", "parameter")})
        eligible = {i for i,m in enumerate(messages) if m["role"] == "tool" and not m.get("error")}
        seen = {s["index"] for s in score["spans"]}
        if seen != eligible or len(seen) != len(score["spans"]) or not set(score["flags"]) <= seen:
            raise RuntimeError("Adapter spans do not cover the eligible tool results")
        for span in score["spans"]:
            if not math.isfinite(span["scalar"]):
                raise RuntimeError("Nonfinite adapter score")
            span["primary"] = bool(messages[span["index"]].get("primary"))
        return score

    def clean(self, messages, flags, seed):
        return (yield from self.request("clean", messages=messages, flags=flags, seed=seed))
