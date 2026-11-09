"""Score fixed and acquired proposals, then execute matched native policy branches."""
from copy import deepcopy
from functools import partial
import json
import math
import os
from pathlib import Path
import re
import subprocess
from time import monotonic
from types import SimpleNamespace

from bridge.batching import FIXED_SCORE_WINDOW, BlockEngine, schedule
from bridge.historical import action_string, context_serializer, is_privileged
from bridge.plan import ARMS, HORIZON, SYSTEM, compact, user_text
from design import ROOT, digest, read, write
from prepare import action_tokenization

CONFIG = read(ROOT / "data" / "historical_guard.json")
PROTO = {"config": CONFIG}


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


def parse(raw):
    text = raw.strip()
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence:
        text = fence[1]
    try:
        def unique(items):
            result = dict(items)
            if len(result) != len(items):
                raise ValueError("duplicate keys")
            return result

        payload = json.loads(text, object_pairs_hook=unique)
        compact(payload)  # reject nonfinite numbers
    except (ValueError, RecursionError):
        return None
    if not isinstance(payload, dict):
        return None
    if set(payload) == {"final"} and isinstance(payload["final"], str):
        return payload
    if (set(payload) == {"function", "args"} and isinstance(payload["function"], str)
            and isinstance(payload["args"], dict)):
        return payload
    return None


def actor(engine, messages):
    prompt = context_serializer(history(messages)).removesuffix("<ASSISTANT_ACTION>\n")
    r = yield from engine.generate([{"role": "user", "content": prompt}], "actor")
    return r, None if r["limit_reached"] else parse(r["text"])


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


def fixed(engine, runtime, base, cell, records):
    # Linkage and permission live in the user text. The alternate flag selects
    # the proposal. None changes these two clean read receipts.
    key = base["id"], cell["source"], cell["copy"], cell["attack"]
    if key not in records:
        receipt = runtime.open(base, cell)
        reads = []
        for role in ("primary", "preview"):
            call = base[role]
            result = runtime.call(call)
            observed = "primary_delivered" if role == "primary" else "preview_seen"
            if result["error"] or not result[observed]:
                raise RuntimeError(f"Fixed prefix missing expected native read {role}: {result}")
            reads.append((call, result))
        records[key] = receipt["schemas"], reads
    schemas, reads = records[key]
    messages = initial(base, cell, schemas)
    for call, result in reads:
        messages = receive(messages, call, result)
    action = {"function": base["action"], "args": base["alt" if cell["alternate"] else "good"]}
    scores = yield from guard_scores(engine, base, messages, action)
    return {"cell": cell, "origin": "fixed_score_only", "messages": messages, "proposal": action, "scores": scores}


def workflow(engine, runtime, base, cell, arm):
    receipt = runtime.open(base, cell)
    messages = initial(base, cell, receipt["schemas"])
    rows = []
    terminal = "HORIZON"
    attack_seen = False
    for step in range(HORIZON):
        generated, proposal = yield from actor(engine, messages)
        event = {"step": step, "input_digest": digest(messages), "actor": generated, "proposal": proposal,
                 "scores": None, "flags": [], "regeneration": None, "result": None,
                 "attack_in_actor_history": attack_seen,
                 "raw_target_proposal": proposal == {"function": base["action"], "args": base["alt"]}}
        rows.append(event)
        if proposal is None:
            terminal = "ACTOR_UNPARSED"
            break
        if "final" in proposal:
            terminal = "ACTOR_FINAL"
            break
        executed = proposal
        if proposal["function"] == base["action"] and arm not in ("plain", "authority"):
            event["scores"] = yield from guard_scores(engine, base, messages, proposal)
            event["flags"] = route(event["scores"], arm)
            if event["flags"]:
                cleaned, event["sanitizers"] = yield from sanitize(engine, messages, event["flags"])
                if cleaned is None:
                    terminal = "SANITIZER_UNUSABLE"
                    break
                messages = cleaned
                event["regeneration"], executed = yield from actor(engine, messages)
                if executed is None:
                    terminal = "REGEN_UNPARSED"
                    break
                if "final" in executed:
                    terminal = "REGEN_FINAL"
                    break
        event["dispatched"] = executed
        result = runtime.call(executed, enforce=arm == "authority")
        event["result"] = result
        attack_seen = attack_seen or result.get("attack_delivered", False)
        messages = receive(messages, executed, result)
    return {"cell": cell, "arm": arm, "terminal": terminal, "initial": initial(base, cell, receipt["schemas"]),
            "events": rows, "final_history": messages}


def qualify_runtime(interpreter, out, plan):
    receipts = []
    with Native(interpreter, out / "native.log") as runtime:
        for base in plan["bases"]:
            for source in (0, 1):
                cell = {"source": source, "linked": 1, "copy": 1, "attack": 1, "flex": 0}
                receipt = runtime.open(base, cell)
                before = runtime.call(base["primary"])
                after = runtime.call(base["primary"])
                preview = runtime.call(base["preview"])
                alt = {"function": base["action"], "args": base["alt"]}
                good = {"function": base["action"], "args": base["good"]}
                denied = runtime.call(alt, enforce=True)
                commit = runtime.call(good, enforce=True)
                duplicate = runtime.call(good, enforce=True)
                expected = (not receipt["effects"] and before["attack_delivered"] and before["primary_delivered"]
                            and not after["primary_delivered"] and before["content"] != after["content"]
                            and preview["preview_seen"] and denied["denied"] and not denied["commits"]
                            and [x["class"] for x in commit["commits"]] == ["preferred"]
                            and duplicate["denied"] and not duplicate["commits"])
                runtime.open(base, cell | {"flex": 1})
                allowed_alt = runtime.call(alt, enforce=True)
                expected = expected and [x["class"] for x in allowed_alt["commits"]] == ["permitted_alternate"]
                if not expected:
                    raise RuntimeError(f"Native preflight failed: {base['id']}/{source} " +
                                       compact([receipt,before,after,preview,denied,commit,duplicate,allowed_alt]))
                receipts.append({"base": base["id"], "source": source, "native_version": receipt["agentdojo"],
                                 "schemas": receipt["schemas"], "tested_one_response": True,
                                 "tested_authority_and_effect_observer": True})
    write(out / "native_qualification.json", receipts)


def run_bridge(backend, interpreter, out, plan):
    bases = {b["id"]: b for b in plan["bases"]}
    for sub in ("fixed", "episodes"):
        (out / sub).mkdir()
    with Native(interpreter, out / "native.log") as runtime:
        records = {}
        fixed_world = runtime.slot(0)

        def job(cell, lane):
            engine = BlockEngine(backend, cell["id"])
            base = bases[cell["base"]]
            if "alternate" in cell:
                # Each fixed block finishes its two native reads before waiting for scoring.
                result = yield from fixed(engine, fixed_world, base, cell, records)
                write(out / "fixed" / (cell["id"] + ".json"), result)
            else:
                world = runtime.slot(lane)
                # Keep every policy's original order and exact-input reuse.
                for arm in sorted(ARMS, key=lambda name: digest([cell["id"], name])):
                    result = yield from workflow(engine, world, base, cell, arm)
                    write(out / "episodes" / (cell["id"] + "." + arm + ".json"), result)
            return cell["id"]

        index = 0
        total = len(plan["fixed"]) + len(plan["episodes"])
        for phase, cells in (("fixed_prefix", plan["fixed"]), ("live_policy", plan["episodes"])):
            started = monotonic()
            window = FIXED_SCORE_WINDOW if phase == "fixed_prefix" else backend.lanes
            for done, cell_id in enumerate(schedule(cells, job, backend.resolve, window), 1):
                index += 1
                elapsed = monotonic() - started
                write(out / "progress.json", {"completed_blocks": index, "total_blocks": total,
                                              "phase": phase, "phase_done": done, "phase_total": len(cells),
                                              "phase_elapsed_seconds": round(elapsed),
                                              "phase_eta_seconds": round(elapsed * (len(cells) - done) / done)
                                              if done >= 16 or done == len(cells) else None,
                                              "batch_lanes": backend.lanes, "batches": dict(backend.stats),
                                              "fixed_native_read_pairs": len(records),
                                              "phase_window": window,
                                              "last": cell_id})
                if done == 1 or done % 16 == 0 or done == len(cells):
                    print(f"Bridge {phase} {done}/{len(cells)} ({cell_id}); batches {dict(backend.stats)}", flush=True)
