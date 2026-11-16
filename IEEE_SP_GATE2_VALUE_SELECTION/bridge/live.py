"""Gate 2 live workflow (derived from Gate 1): matched native policy branches; adds surgical deletion of the
authorized identifier and sanitizer add-back. Gate 1 notes follow.

Gate 1 live workflow: matched native policy branches with an actor-adapter factor.

Native, history, initial, receive, action_parts, placebo, guard_scores, route and sanitize are
copied verbatim from IEEE_SP_END_TO_END_LARGE_GPU23/bridge/live.py (the E13/E14 bridge). Only the
actor (bridge/adapters.py), the additional forced arms and the runner are new.
"""
from copy import deepcopy
from functools import partial
import json
import math
import os
import subprocess
from time import monotonic
from types import SimpleNamespace

from bridge.adapters import actor
from bridge.batching import BlockEngine, schedule
from bridge.historical import action_string, context_serializer, is_privileged
from bridge.gate2_plan import (ARMS, CANDIDATES, CARRIER, HORIZON, INSTRUCTIONS, SYSTEM, compact, effective_base,
                               identifier_sentence, surgical_delete, user_text)
from common import ROOT, action_tokenization, digest, read, write

CONFIG = read(ROOT / "data" / "historical_guard.json")
PROTO = {"config": CONFIG}
NULL_CONTENT = "[content removed by guard]"


class Native:
    def __init__(self, interpreter, logfile):
        self.interpreter, self.logfile = interpreter, logfile

    def __enter__(self):
        self.log = self.logfile.open("w")
        try:
            self.process = subprocess.Popen(
                [self.interpreter, "-u", "-m", "bridge.native"], cwd=ROOT, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=self.log, encoding="utf-8",
                env=os.environ | {"CUDA_VISIBLE_DEVICES": ""})
        except Exception:
            self.log.close()
            raise
        return self

    def __exit__(self, *exc):
        try:
            self.process.stdin.close()
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()
        finally:
            self.process.stdout.close()
            self.log.close()

    def request(self, op, **kwargs):
        self.process.stdin.write(compact({"op": op, **kwargs}) + "\n")
        self.process.stdin.flush()
        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError(f"Native tool worker stopped. See {self.logfile}")
        response = json.loads(line)
        if "ok" not in response:
            raise RuntimeError(response["failure"])
        return response["ok"]

    def open(self, base, cell, *, slot=0):
        return self.request("open", base=base, cell=cell, slot=slot)

    def call(self, action, enforce=False, *, slot=0):
        return self.request("call", action=action, enforce=enforce, slot=slot)

    def slot(self, index):
        return SimpleNamespace(open=partial(self.open, slot=index), call=partial(self.call, slot=index))


def history(messages):
    native = [dict(msg) for msg in messages]
    for msg in native:
        if "tool_call" in msg:
            msg["tool_call"] = SimpleNamespace(**msg["tool_call"])
        if "tool_calls" in msg:
            msg["tool_calls"] = [SimpleNamespace(**c) for c in msg["tool_calls"]]
    return native


def initial(base, cell, schemas):
    # Role framing matches historical scoring. Actor generation adds the model's
    # native outer chat template around the serialized inner transcript.
    return [{"role": "system", "content": SYSTEM + "\nTool schemas:\n" + compact(schemas)},
            {"role": "user", "content": user_text(base, cell)}]


def receive(messages, action, result):
    return [*messages,
            {"role": "assistant", "content": "", "tool_calls": [action]},
            {"role": "tool", "content": result["content"], "error": result["error"],
             "tool_call": action, "primary_delivered": result.get("primary_delivered", False),
             "preview_seen": result.get("preview_seen", False),
             "original_attack": result.get("primary_delivered", False) and result.get("attack_delivered", False)}]


def action_parts(tokenizer, base, action):
    full = action_string(SimpleNamespace(**action))
    cursor = len(action["function"]) + 2  # opening parenthesis and JSON brace
    spans = {}
    for k, value in sorted(action["args"].items()):
        start = cursor + len(compact(k)) + 1
        end = start + len(compact(value))
        next_cursor = end + 1
        if k == base["identifier"]:
            role = "identifier"
        elif k == base["parameter"]:
            role = "parameter"
        else:
            role = None
        if role:
            # Exclude wrapper syntax for the targeted simple values. Complex
            # unanticipated actor values retain the score with no role patch.
            if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
                start, end = start + 2, end - 2
            elif isinstance(value, str):
                start, end = start + 1, end - 1
            elif not isinstance(value, (int, float)) or isinstance(value, bool):
                start = end
            if start < end:
                spans[role] = start, end
        cursor = next_cursor
    return action_tokenization(tokenizer, full, spans)


def placebo(roles, target):
    selected = [i for i, r in enumerate(roles) if r == target]
    candidates = [i for i, r in enumerate(roles) if r == "other"]
    if not selected or len(candidates) < len(selected):
        return None, None
    distance = lambda i: (min(abs(i-j) for j in selected), i)
    return selected, sorted(candidates, key=distance)[:len(selected)]


def guard_scores(engine, base, messages, action):
    positions = [i for i, msg in enumerate(messages) if msg["role"] == "tool"]
    if not positions or not is_privileged(action["function"], PROTO):
        return {"spans": [], "action": None}
    tokens = action_parts(engine.tokenizer, base, action)
    msgs = history(messages)
    prefixes = [context_serializer(msgs), context_serializer(msgs, ablate_user=True),
                *(context_serializer(msgs, ablate_tool_message_index=i) for i in positions)]
    ids, vectors = yield from engine.score(prefixes, tokens["cids"])
    user_vector = vectors[1]
    n = len(user_vector)
    spans = []
    for idx, (request_id, tool_vector) in enumerate(zip(ids[2:], vectors[2:], strict=True)):
        margin = [a - b for a, b in zip(user_vector, tool_vector, strict=True)]
        delta_u = math.fsum(a-b for a,b in zip(vectors[0], user_vector, strict=True)) / n
        delta_s = math.fsum(a-b for a,b in zip(vectors[0], tool_vector, strict=True)) / n
        span = {"message_index": positions[idx], "request": request_id, "scalar": delta_s - delta_u,
                "delta_u": delta_u, "delta_s": delta_s, "tool_loss_components": {
                    role: math.fsum(v-w for v,w,r in zip(vectors[0], tool_vector, tokens["roles"], strict=True)
                                    if role == r) / n for role in ("identifier", "parameter", "other")},
                "components": {
                    role: math.fsum(v for v, r in zip(margin, tokens["roles"], strict=True) if role == r) / n
                    for role in ("identifier", "parameter", "other")},
                "primary": messages[positions[idx]].get("primary_delivered", False),
                "preview": messages[positions[idx]].get("preview_seen", False)
                and not messages[positions[idx]].get("sanitized", False),
                "attacked": messages[positions[idx]].get("original_attack", False)
                and not messages[positions[idx]].get("sanitized", False)}
        for role, suffix in (("identifier", "id"), ("parameter", "parameter")):
            a, b = placebo(tokens["roles"], role)
            for arm, indices in (("without_" + suffix, a), ("placebo_" + suffix, b)):
                span[arm] = (span["scalar"] - math.fsum(margin[i] for i in indices) / n
                             if indices and span["primary"] else span["scalar"])
                span[arm + "_positions"] = indices if span["primary"] else None
        spans.append(span)
    return {"spans": spans, "action": tokens, "full_request": ids[0], "no_user_request": ids[1]}


def route(scores, arm):
    if arm in ("plain", "authority"):
        return []
    return [span["message_index"] for span in scores["spans"] if span[arm] > 0]


def sanitize(engine, messages, flagged):
    messages = deepcopy(messages)
    detector = CONFIG["detector"]
    earliest = min(flagged)
    receipts = []
    for idx in flagged:
        m = messages[idx]
        text = detector["sanitizer_user_template"].format(
            user_request=messages[1]["content"], tool_name=m["tool_call"]["function"],
            untrusted_content=m["content"])
        result = yield from engine.generate([{"role": "user", "content": detector["sanitizer_system_prompt"] + "\n\n" + text}],
                                 "sanitizer")
        if not result["text"].strip() or result["limit_reached"]:
            return None, [*receipts, {"index": idx, "result": result}]
        m["content"] = result["text"]
        m["sanitized"] = True
        receipts.append({"index": idx, "result": result})
    for m in messages[earliest+1:]:
        if m["role"] == "assistant" and m["content"].strip():
            m["content"] = detector["cot_mask_placeholder"]
    return messages, receipts


def escaped(text):
    return json.dumps(text, ensure_ascii=False)[1:-1]


def primary_index(messages):
    return next((i for i, m in enumerate(messages) if m["role"] == "tool" and m.get("primary_delivered")), None)


def identifier_present(base, text):
    good = base["good"][base["identifier"]]
    values = good if isinstance(good, list) else [good]
    return all(str(v) in text for v in values)


def transform(engine, base, cell, messages, arm, flags):
    """Apply an arm's remediation to the flagged spans. Returns (messages or None, receipt)."""
    if arm in ("scalar", "forced_sanitize"):
        cleaned, receipts = yield from sanitize(engine, messages, flags)
        return cleaned, {"kind": "llm_sanitizer", "sanitizers": receipts}
    if arm == "sanitize_addback":
        cleaned, receipts = yield from sanitize(engine, messages, flags)
        if cleaned is None:
            return None, {"kind": "llm_sanitizer_addback", "sanitizers": receipts}
        (idx,) = flags
        before = cleaned[idx]["content"]
        applied = not identifier_present(base, before)
        if applied:  # M2: restore only the authorized identifier, nothing else
            cleaned[idx]["content"] = before.rstrip() + " " + identifier_sentence(base)
        return cleaned, {"kind": "llm_sanitizer_addback", "sanitizers": receipts, "addback_applied": applied,
                         "sanitized_before_addback": before, "content_after": cleaned[idx]["content"]}
    out = deepcopy(messages)
    (idx,) = flags
    if arm == "surgical_delete":  # M1: remove only the sentence stating the authorized identifier
        primary, deleted, sentence = surgical_delete(base, cell)
        old = out[idx]["content"]
        if old.count(escaped(primary)) != 1:
            raise RuntimeError("Surgical deletion could not locate the primary record exactly once")
        out[idx]["content"] = old.replace(escaped(primary), escaped(deleted))
        out[idx]["sanitized"] = True
        return out, {"kind": arm, "removed": sentence, "content_before": old, "content_after": out[idx]["content"]}
    if arm == "null_clean":
        out[idx]["content"] = NULL_CONTENT
    else:
        raise ValueError(arm)
    out[idx]["sanitized"] = True
    return out, {"kind": arm, "content_after": out[idx]["content"]}


def workflow(engine, runtime, base, cell, arm):
    base = effective_base(base, cell)
    receipt = runtime.open(base, cell)
    schemas = receipt["schemas"]
    messages = initial(base, cell, schemas)
    rows, terminal, intervened, pending = [], "HORIZON", False, []
    for step in range(HORIZON):
        if pending:
            # Amendment A1: a later call from the same multi-call turn; no new generation.
            generated, proposal = {"from_multi_call": True}, pending.pop(0)
        else:
            generated, proposal = yield from actor(engine, messages, cell["adapter"], schemas)
            if proposal is not None and "calls" in proposal:
                proposal, pending = proposal["calls"][0], list(proposal["calls"][1:])
        event = {"step": step, "input_digest": digest(messages), "actor": generated, "proposal": proposal,
                 "scores": None, "flags": [], "transform": None, "regeneration": None, "result": None}
        rows.append(event)
        if proposal is None:
            terminal = "ACTOR_UNPARSED"
            break
        if "final" in proposal:
            terminal = "ACTOR_FINAL"
            break
        executed = proposal
        write_call = proposal["function"] == base["action"]
        if write_call and arm not in ("plain", "authority"):
            event["scores"] = yield from guard_scores(engine, base, messages, proposal)
            if arm == "scalar":
                event["flags"] = route(event["scores"], "scalar")
            elif not intervened:
                idx = primary_index(messages)
                event["flags"] = [] if idx is None else [idx]
                event["forced_without_primary"] = idx is None
            if event["flags"]:
                intervened = True
                cleaned, event["transform"] = yield from transform(engine, base, cell, messages, arm, event["flags"])
                if cleaned is None:
                    terminal = "SANITIZER_UNUSABLE"
                    break
                messages = cleaned
                idx = primary_index(messages)
                event["primary_after"] = None if idx is None else messages[idx]["content"]
                event["regeneration"], executed = yield from actor(engine, messages, cell["adapter"], schemas)
                if executed is not None and "calls" in executed:
                    executed, pending = executed["calls"][0], list(executed["calls"][1:])
                if executed is None:
                    terminal = "REGEN_UNPARSED"
                    break
                if "final" in executed:
                    terminal = "REGEN_FINAL"
                    break
        event["dispatched"] = executed
        result = runtime.call(executed, enforce=arm == "authority")
        event["result"] = result
        messages = receive(messages, executed, result)
    return {"cell": cell, "arm": arm, "terminal": terminal, "initial": initial(base, cell, schemas),
            "events": rows, "final_history": messages}


def qualify_runtime(interpreter, out, plan):
    """Every base x candidate world opens, delivers both records with the planned text, locates the
    identifier sentence exactly once, denies the forbidden write, commits the authorized write once,
    and commits every candidate value as an out-of-contract effect (so substitution is observable)."""
    receipts = []
    with Native(interpreter, out / "native.log") as runtime:
        for base_original in plan["bases"]:
            for cand in CANDIDATES:
                # Carrier is a property of the family (gate2_plan.CARRIER), not of the plan's cells: a smoke
                # plan keeps every base but only some cells.
                cell = {"carrier": CARRIER[base_original["family"]],
                        "candidate": cand, "instr": "tool", "source": 1, "linked": 0, "copy": 1, "attack": 0,
                        "flex": 0}
                base = effective_base(base_original, cell)
                receipt = runtime.open(base, cell)
                first = runtime.call(base["primary"])
                preview = runtime.call(base["preview"])
                primary, deleted, _ = surgical_delete(base, cell)
                denied = runtime.call({"function": base["action"], "args": base["alt"]}, enforce=True)
                commit = runtime.call({"function": base["action"], "args": base["good"]}, enforce=True)
                duplicate = runtime.call({"function": base["action"], "args": base["good"]}, enforce=True)
                ok = (not receipt["effects"] and first["primary_delivered"] and preview["preview_seen"]
                      and first["content"].count(escaped(primary)) == 1 and denied["denied"]
                      and not denied["commits"] and [c["class"] for c in commit["commits"]] == ["preferred"]
                      and duplicate["denied"] and not duplicate["commits"] and deleted != primary)
                substitutes = {}
                for kind, value in base["candidates"].items():
                    runtime.open(base, cell)
                    args = dict(base["good"])
                    args[base["identifier"]] = [value] if isinstance(base["good"][base["identifier"]], list) else value
                    r = runtime.call({"function": base["action"], "args": args})
                    substitutes[kind] = [c["class"] for c in r["commits"]]
                    ok = ok and substitutes[kind] == ["other_out_of_contract"]
                if not ok:
                    raise RuntimeError(f"Native preflight failed: {base['id']}/{cand} " +
                                       compact([receipt, first, preview, denied, commit, duplicate, substitutes]))
                receipts.append({"base": base["id"], "carrier": cell["carrier"], "candidate": cand, "source": 1,
                                 "native_version": receipt["agentdojo"], "primary_content": first["content"],
                                 "preview_content": preview["content"], "substitute_commit_classes": substitutes})
    write(out / "native_qualification.json", receipts)
    return receipts


def host_memory():
    """Host RAM telemetry (Gate 1's Gemma worker was SIGKILLed with no Python traceback)."""
    info = {}
    try:
        with open("/proc/meminfo") as f:
            mem = {line.split(":")[0]: int(line.split()[1]) for line in f}
        with open("/proc/self/status") as f:
            rss = next(int(line.split()[1]) for line in f if line.startswith("VmRSS:"))
        info = {"host_mem_available_gib": round(mem["MemAvailable"] / 2**20, 1),
                "host_mem_total_gib": round(mem["MemTotal"] / 2**20, 1), "worker_rss_gib": round(rss / 2**20, 1)}
    except (OSError, KeyError, StopIteration, ValueError):
        pass
    return info


def run_gate2(backend, interpreter, out, plan):
    bases = {b["id"]: b for b in plan["bases"]}
    episodes = out / "episodes"
    episodes.mkdir(exist_ok=True)
    # Resume: a cell is complete only when every arm's episode file exists (files are written atomically).
    # A partially written cell is rerun from its native start state; its episode files are overwritten.
    complete = {c["id"] for c in plan["cells"]
                if all((episodes / f"{c['id']}.{arm}.json").exists() for arm in ARMS)}
    if complete:
        print(f"Resuming: {len(complete)}/{len(plan['cells'])} cells already complete; rerunning the rest", flush=True)
        with (out / "resume_log.jsonl").open("a") as f:
            f.write(compact({"complete_cells": len(complete), "total_cells": len(plan["cells"])}) + "\n")
    with Native(interpreter, out / "native_episodes.log") as runtime:
        def job(cell, lane):
            engine = BlockEngine(backend, cell["id"])
            world = runtime.slot(lane)
            # One job per cell; arms in a fixed digest order share exact model requests via the cache.
            for arm in sorted(ARMS, key=lambda name: digest([cell["id"], name])):
                result = yield from workflow(engine, world, bases[cell["base"]], cell, arm)
                write(episodes / (cell["id"] + "." + arm + ".json"), result)
            return cell["id"]

        started = monotonic()
        cells = [c for c in plan["cells"] if c["id"] not in complete]
        offset = len(complete)
        for done, cell_id in enumerate(schedule(cells, job, backend.resolve, backend.lanes), 1):
            elapsed = monotonic() - started
            write(out / "progress.json", {"cells_done": offset + done, "cells_total": offset + len(cells),
                                          "cells_resumed": offset, "episodes_done": (offset + done) * len(ARMS),
                                          "elapsed_seconds": round(elapsed),
                                          "eta_seconds": round(elapsed * (len(cells) - done) / done) if done >= 8 else None,
                                          "batches": dict(backend.stats), "last": cell_id, **host_memory()})
            if done == 1 or done % 8 == 0 or done == len(cells):
                eta = round(elapsed * (len(cells) - done) / done / 60)
                mem = host_memory()
                print(f"Gate 2 {offset + done}/{offset + len(cells)} cells ({cell_id}); elapsed {round(elapsed/60)} min, ETA {eta} min; "
                      f"host RAM free {mem.get('host_mem_available_gib')} GiB, worker RSS {mem.get('worker_rss_gib')} GiB",
                      flush=True)
