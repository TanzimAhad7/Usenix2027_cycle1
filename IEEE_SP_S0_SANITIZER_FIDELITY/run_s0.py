"""S0 V2 runner (PROTOCOL.md). Subcommands:

  freeze                      CPU  build inputs/s0_inputs.json + inputs/s0_controls.json, write inputs/FREEZE.json
  verify [--online]           CPU  hashes, scorer validation, unit tests, render checks, model snapshots, GPU 3
                                   identity (read-only); --online: OpenRouter model listing/pricing (free GET)
  open --run RUN --profile P  GPU 3 only (P = qwen | gemma): continuity replay gate, then P's configurations
  gemini --run RUN --budget-usd X --max-calls N --allow-paid-api
                              PAID API: F0, F1 via OpenRouter; needs approvals/gemini_approval.json
  score --runs RUN [RUN..]    CPU  automatic scoring + blinded adjudication export
  analyze --runs RUN [RUN..] [--adjudication FILE]
                              CPU  decision bands (automatic, strict, adjudicated), exact CIs, McNemar, causes

All generation is resumable per (configuration, item): an output whose request digest matches is never redone.
"""
import argparse
import json
import math
import os
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import s0_core as core  # noqa: E402

GATE2 = HERE.parent / "IEEE_SP_GATE2_VALUE_SELECTION"
GATE2_RUNS = GATE2 / "runs"
INPUTS = HERE / "inputs"
FROZEN = INPUTS / "FREEZE.json"
# Physical GPUs this package may use, pinned by UUID. GPU 3 is the default; GPU 2 only when the user selects it
# explicitly (user instruction, 12 Nov 2026: "you can use gpu 2, for now, since 3 is busy").
PINNED_GPUS = {2: "GPU-0b687901-110f-39c5-a5a9-dfe4b73cc932", 3: "GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6"}
GPU_INDEX, GPU_UUID = 3, PINNED_GPUS[3]
OPENROUTER = "https://openrouter.ai/api/v1"
GEMINI_ID = "google/gemini-2.5-flash"
APPROVAL = HERE / "approvals" / "gemini_approval.json"


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def log(msg):
    print(f"[{now()}] {msg}", flush=True)


def status(run, **kw):
    path = Path(run) / "status.json"
    cur = json.loads(path.read_text()) if path.exists() else {}
    cur.update(kw, updated_utc=now())
    core.atomic_write(path, cur)


def check_freeze():
    if not FROZEN.exists():
        raise SystemExit("inputs are not frozen: run `run_s0.py freeze` first")
    f = json.loads(FROZEN.read_text())
    import hashlib
    for name, h in f["sha256"].items():
        if hashlib.sha256((INPUTS / name).read_bytes()).hexdigest() != h:
            raise SystemExit(f"{name} changed after freeze")
    return f


# ------------------------------------------------------------------------------------------- freeze
def cmd_freeze(args):
    import hashlib
    INPUTS.mkdir(exist_ok=True)
    if FROZEN.exists():
        raise SystemExit(f"{FROZEN} exists; S0 V2 inputs are frozen")
    py = sys.executable
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONHOME")} | {"CUDA_VISIBLE_DEVICES": ""}
    subprocess.run([py, str(HERE / "build_inputs.py"), str(INPUTS)], check=True, env=env)
    subprocess.run([py, str(HERE / "build_controls.py"), str(GATE2_RUNS), str(INPUTS / "s0_controls.json")],
                   check=True, env=env)
    files = ["s0_inputs.json", "s0_controls.json"]
    body = {"protocol": core.PROTOCOL, "frozen_utc": now(),
            "sha256": {n: hashlib.sha256((INPUTS / n).read_bytes()).hexdigest() for n in files},
            "code_sha256": {n: hashlib.sha256((HERE / n).read_bytes()).hexdigest()
                            for n in ("build_inputs.py", "build_controls.py", "retention.py", "prompts.py",
                                      "s0_core.py", "run_s0.py")},
            "published_block_sha256": hashlib.sha256((HERE / "prompts" / "D1_published_block.txt").read_bytes()).hexdigest()}
    core.atomic_write(FROZEN, body)
    print(json.dumps(body, indent=1))


# ------------------------------------------------------------------------------------------- backends
class HFBackend:
    """Greedy HF generation on physical GPU 3, reusing Gate 2's frozen BatchEngine.generate_group (decoding code
    identical to Gate 2) and its OOM-splitting bounded_inference."""

    def __init__(self, profile, workdir, gpu=GPU_INDEX):
        uuid = PINNED_GPUS[gpu]
        if os.environ.get("CUDA_VISIBLE_DEVICES") != uuid:
            raise SystemExit(f"CUDA_VISIBLE_DEVICES must be the pinned GPU {gpu} UUID {uuid}")
        sys.path.insert(0, str(GATE2))
        from score import check_gpu, load_model, snapshot  # Gate 2 frozen helpers (read-only import)
        from bridge.batching import BatchEngine, bounded_inference
        from transformers import AutoTokenizer
        check_gpu(gpu, uuid)  # one visible device, UUID match, BF16, and no other compute process
        self.gpu = {"physical_index": gpu, "uuid": uuid}
        inv = json.loads((GATE2_RUNS / f"20261111T185944Z_gate2_all_both_{profile}" / "invocation.json").read_text())
        self.identity = snapshot(inv["cache"], profile)
        recorded = json.loads((GATE2_RUNS / f"20261111T185944Z_gate2_all_both_{profile}" / "model_identity.json").read_text())
        if self.identity["revision"] != recorded["revision"]:
            raise SystemExit("Model revision differs from Gate 2")
        self.profile = profile
        self.tokenizer = AutoTokenizer.from_pretrained(self.identity["path"], local_files_only=True)
        self.model = load_model(self.identity, "cuda:0")
        Path(workdir).mkdir(parents=True, exist_ok=True)
        self.engine = BatchEngine(self.model, self.tokenizer, "cuda:0", Path(workdir), profile, 16)
        self.bounded = bounded_inference

    def render(self, messages):
        kw = {"enable_thinking": False} if self.profile == "qwen" else {}
        enc = self.tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True,
                                                 return_dict=True, **kw)
        return enc["input_ids"]

    def count(self, text):
        return len(self.tokenizer.encode(text, add_special_tokens=False))

    def decode(self, pids):
        return self.tokenizer.decode(pids, skip_special_tokens=False)

    def generate(self, requests):
        out = []
        for batch, res in self.bounded(requests, self.engine.generate_group, self.engine.stats):
            out.extend(res)
        return out


def build_request(backend, config, item):
    msgs = core.request_messages(config, item)
    pids = backend.render(msgs)
    rendered = backend.decode(pids)
    if item["untrusted_content"] not in rendered:  # guards silent drops (Gemma-3 drops system-only messages)
        raise RuntimeError(f"{config}/{item['item_id']}: rendered prompt does not contain the untrusted content")
    limit = core.decode_limit(backend.count(item["untrusted_content"]))
    too_long = limit is None or len(pids) + limit > core.CONTEXT_CAP[backend.profile]
    return {"id": core.digest([config, item["item_id"], pids, limit]), "config": config, "item_id": item["item_id"],
            "messages": msgs, "pids": pids, "limit": limit or 0, "too_long": too_long}


def batches(reqs, token_budget=32768, lanes=16):
    by = defaultdict(list)
    for r in reqs:
        by[r["limit"]].append(r)
    for limit, rs in sorted(by.items()):
        rs.sort(key=lambda r: len(r["pids"]))
        cur = []
        for r in rs:
            width = max([len(x["pids"]) for x in cur] + [len(r["pids"])])
            if cur and (len(cur) + 1 > lanes or (len(cur) + 1) * (width + limit) > token_budget):
                yield cur
                cur = []
            cur.append(r)
        if cur:
            yield cur


def run_config(backend, run, config, items):
    odir = Path(run) / "outputs" / config
    pending = []
    for it in items:
        req = build_request(backend, config, it)
        path = odir / f"{it['item_id']}.json"
        if path.exists() and json.loads(path.read_text()).get("request_id") == req["id"]:
            continue
        if req["too_long"]:
            core.atomic_write(path, {"request_id": req["id"], "config": config, "item_id": it["item_id"],
                                     "status": "SANITIZER_TOO_LONG", "n_prompt_tokens": len(req["pids"])})
            continue
        pending.append(req)
    log(f"{config}: {len(items)} items, {len(pending)} to generate")
    done = 0
    for b in batches(pending):
        t0 = time.time()
        res = backend.generate([{"id": r["id"], "pids": r["pids"], "limit": r["limit"], "item_id": r["item_id"]}
                                for r in b])
        dt = time.time() - t0
        for r, o in zip(b, res, strict=True):
            core.atomic_write(odir / f"{r['item_id']}.json", {
                "request_id": r["id"], "config": config, "item_id": r["item_id"], "model": backend.identity["hub"],
                "revision": backend.identity["revision"], "messages": r["messages"],
                "pids_sha256": core.digest(r["pids"]), "n_prompt_tokens": len(r["pids"]), "limit": r["limit"],
                "text": o["text"], "generated": o["generated"], "limit_reached": o["limit_reached"],
                "batch_size": len(b), "batch_seconds": round(dt, 2), "created_utc": now()})
        done += len(b)
        status(run, phase=f"GENERATING {config}", done=done, pending=len(pending))
        log(f"{config}: {done}/{len(pending)} (batch {len(b)}, {dt:.1f}s)")


def continuity_gate(backend, run, profile, ctl):
    """Replay every recorded Gate 2 sanitizer request (exact token ids, limit 384) and require the E4
    classification of each C0 `tool` primary record to equal the recorded Gate 2 classification."""
    rec_path = GATE2_RUNS / f"20261111T185944Z_gate2_all_both_{profile}" / f"model_{profile}" / "requests.jsonl"
    lines = rec_path.read_text().splitlines()
    replay = ctl["replay"][profile]
    out_path = Path(run) / "continuity" / f"{profile}.json"
    if out_path.exists():
        prev = json.loads(out_path.read_text())
        if prev.get("passed"):
            log(f"continuity {profile}: already passed")
            return prev
    reqs = []
    for meta in replay["requests"]:
        r = json.loads(lines[meta["line"] - 1])
        import hashlib
        if r["id"] != meta["id"] or hashlib.sha256(json.dumps(r["pids"]).encode()).hexdigest() != meta["pids_sha256"]:
            raise SystemExit(f"Recorded Gate 2 request at line {meta['line']} does not match the frozen replay index")
        reqs.append({"id": r["id"], "pids": r["pids"], "limit": r["limit"], "recorded": r})
    texts = {}
    for b in batches(reqs, lanes=16):
        for r, o in zip(b, backend.generate([{"id": x["id"], "pids": x["pids"], "limit": x["limit"]} for x in b]),
                        strict=True):
            texts[r["id"]] = o
    token_identical = sum(texts[r["id"]]["generated"] == r["recorded"]["generated"] for r in reqs)
    pcs = {i["task"]: i for i in ctl["positive_control_items"]}
    import retention
    mism = []
    for base, rid in replay["c0_tool_request"].items():
        if rid is None:
            continue
        rec = next(r for r in reqs if r["id"] == rid)["recorded"]["text"]
        new = texts[rid]["text"]
        a = [x["E4"] for x in retention.score_item(pcs[base], rec)]
        b = [x["E4"] for x in retention.score_item(pcs[base], new)]
        if a != b:
            mism.append(base)
    res = {"profile": profile, "replayed": len(reqs), "token_identical": token_identical,
           "c0_tool_compared": sum(v is not None for v in replay["c0_tool_request"].values()),
           "E4_mismatches": mism, "passed": not mism, "created_utc": now(),
           "replay_outputs": {k: {"text": v["text"], "limit_reached": v["limit_reached"]} for k, v in texts.items()}}
    core.atomic_write(out_path, res)
    log(f"continuity {profile}: replayed {len(reqs)}, token-identical {token_identical}, E4 mismatches {mism}")
    return res


def cmd_open(args):
    check_freeze()
    nat, ctl = core.load_inputs(INPUTS)
    run = Path(args.run)
    run.mkdir(parents=True, exist_ok=True)
    status(run, phase=f"LOADING {args.profile}", profile=args.profile, pid=os.getpid(), gpu=args.gpu)
    backend = HFBackend(args.profile, run / "engine" / args.profile, args.gpu)
    core.atomic_write(run / f"model_identity_{args.profile}.json", backend.identity | {"gpu": backend.gpu})
    gate = continuity_gate(backend, run, args.profile, ctl)
    if not gate["passed"]:
        status(run, phase=f"CONTINUITY_FAILED {args.profile}")
        raise SystemExit(f"continuity gate failed for {args.profile}: {gate['E4_mismatches']}")
    for config in core.PROFILE_CONFIGS[args.profile]:
        run_config(backend, run, config, core.items_for(config, nat, ctl))
    status(run, phase=f"DONE {args.profile}")


# ------------------------------------------------------------------------------------------- paid API
class Budget:
    """Append-only, fsync'd spend ledger with hard pre-call enforcement."""

    def __init__(self, path, budget_usd, max_calls):
        self.path, self.budget, self.max_calls = Path(path), float(budget_usd), int(max_calls)
        self.spent, self.calls = 0.0, 0
        if self.path.exists():
            for line in self.path.read_text().splitlines():
                e = json.loads(line)
                self.calls += 1
                self.spent += e["charged_usd"]

    def allow(self, upper_usd):
        return self.calls < self.max_calls and self.spent + upper_usd <= self.budget

    def record(self, entry):
        self.calls += 1
        self.spent += entry["charged_usd"]
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
            f.flush()
            os.fsync(f.fileno())


def http_post(url, headers, body, timeout=300):
    import httpx
    r = httpx.post(url, headers=headers, json=body, timeout=timeout)
    return r.status_code, (r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text})


def http_get(url, headers=None, timeout=60):
    import httpx
    r = httpx.get(url, headers=headers or {}, timeout=timeout)
    return r.status_code, r.json()


def fetch_pricing(get=http_get):
    code, data = get(f"{OPENROUTER}/models")
    m = next((x for x in data.get("data", []) if x["id"] == GEMINI_ID), None) if code == 200 else None
    if not m:
        raise SystemExit(f"{GEMINI_ID} not listed by OpenRouter (HTTP {code})")
    p = m["pricing"]
    return {"model": GEMINI_ID, "prompt_usd_per_token": float(p["prompt"]),
            "completion_usd_per_token": float(p["completion"]), "fetched_utc": now()}


def require_approval(args, path):
    if not args.allow_paid_api:
        raise SystemExit("Paid API refused: pass --allow-paid-api")
    if not path.exists():
        raise SystemExit(f"Paid API refused: {path} missing (PROTOCOL.md section 9)")
    a = json.loads(path.read_text())
    if a.get("approved") is not True or a.get("model") != GEMINI_ID:
        raise SystemExit("Paid API refused: approval file not affirmative for this model")
    if float(args.budget_usd) > float(a["max_usd"]) or int(args.max_calls) > int(a["max_calls"]):
        raise SystemExit("Paid API refused: requested budget or calls exceed the approval")
    if not set(args.configs) <= set(a.get("configs", [])):
        raise SystemExit("Paid API refused: configuration not approved")
    return a


def upper_cost(messages, max_tokens, price):
    prompt_tokens_upper = math.ceil(len(json.dumps(messages, ensure_ascii=False).encode()) / 2)  # conservative
    return prompt_tokens_upper * price["prompt_usd_per_token"] + max_tokens * price["completion_usd_per_token"]


def cmd_gemini(args, post=http_post, get=http_get, key=None):
    check_freeze()
    run = Path(args.run)
    run.mkdir(parents=True, exist_ok=True)
    approval = require_approval(args, APPROVAL)
    key = key or os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit("OPENROUTER_API_KEY is not set")
    nat, ctl = core.load_inputs(INPUTS)
    price = fetch_pricing(get)
    core.atomic_write(run / "gemini" / "pricing.json", price)
    core.atomic_write(run / "gemini" / "approval_used.json", approval)
    code, keyinfo = get(f"{OPENROUTER}/key", {"Authorization": f"Bearer {key}"})  # free: key limits and usage
    core.atomic_write(run / "gemini" / "key_preflight.json", {"http": code, "data": (keyinfo or {}).get("data")})
    budget = Budget(run / "gemini" / "spend_ledger.jsonl", args.budget_usd, args.max_calls)
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    consecutive_4xx = 0
    for config in args.configs:
        odir = run / "outputs" / config
        for it in core.items_for(config, nat, ctl):
            msgs = core.request_messages(config, it)
            limit = core.decode_limit(math.ceil(len(it["untrusted_content"]) / 3))
            path = odir / f"{it['item_id']}.json"
            rid = core.digest([config, it["item_id"], msgs, limit])
            if path.exists() and json.loads(path.read_text()).get("request_id") == rid:
                continue
            if limit is None:
                core.atomic_write(path, {"request_id": rid, "config": config, "item_id": it["item_id"],
                                         "status": "SANITIZER_TOO_LONG"})
                continue
            max_tokens = limit + core.GEMINI_REASONING_HEADROOM
            upper = upper_cost(msgs, max_tokens, price)
            if not budget.allow(upper):
                status(run, phase="BUDGET_STOP", spent_usd=round(budget.spent, 6), calls=budget.calls)
                raise SystemExit(f"BUDGET_STOP before {config}/{it['item_id']}: spent {budget.spent:.4f} USD, "
                                 f"next call upper bound {upper:.4f}, budget {budget.budget}")
            body = {"model": GEMINI_ID, "messages": msgs, "temperature": 0, "max_tokens": max_tokens,
                    "usage": {"include": True}}
            t0 = time.time()
            try:
                code, data = post(f"{OPENROUTER}/chat/completions", headers, body)
            except Exception as exc:  # network failure: charge the upper bound (cost unknown)
                code, data = -1, {"error": repr(exc)}
            usage = (data or {}).get("usage") or {}
            computed = (usage.get("prompt_tokens", 0) * price["prompt_usd_per_token"]
                        + usage.get("completion_tokens", 0) * price["completion_usd_per_token"])
            reported = usage.get("cost")
            charged = max(computed, float(reported or 0)) if code == 200 else (upper if code == -1 else 0.0)
            budget.record({"config": config, "item_id": it["item_id"], "request_id": rid, "http": code,
                           "upper_usd": upper, "computed_usd": computed, "reported_usd": reported,
                           "charged_usd": charged, "usage": usage, "provider": (data or {}).get("provider"),
                           "utc": now()})
            if code == 200:
                consecutive_4xx = 0
                ch = data["choices"][0]
                text = (ch.get("message") or {}).get("content") or ""
                rec = {"request_id": rid, "config": config, "item_id": it["item_id"], "model": data.get("model"),
                       "provider": data.get("provider"), "messages": msgs, "limit": limit, "max_tokens": max_tokens,
                       "text": text, "finish_reason": ch.get("finish_reason"),
                       "limit_reached": ch.get("finish_reason") == "length", "usage": usage,
                       "seconds": round(time.time() - t0, 2), "raw_response": data, "created_utc": now()}
            else:
                consecutive_4xx = consecutive_4xx + 1 if 400 <= code < 500 else 0
                rec = {"request_id": rid + "-error", "config": config, "item_id": it["item_id"],
                       "status": "PROVIDER_ERROR", "http": code, "raw_response": data, "created_utc": now()}
            core.atomic_write(path, rec)
            status(run, phase=f"GEMINI {config}", spent_usd=round(budget.spent, 6), calls=budget.calls)
            if consecutive_4xx >= 3:
                raise SystemExit("Three consecutive 4xx provider errors: stopping (see outputs)")
    status(run, phase="DONE gemini", spent_usd=round(budget.spent, 6), calls=budget.calls)


# ------------------------------------------------------------------------------------------- score / analyze
def collect(runs):
    outs = defaultdict(dict)
    for run in runs:
        for f in sorted((Path(run) / "outputs").glob("*/*.json")):
            rec = json.loads(f.read_text())
            outs[rec["config"]][rec["item_id"]] = rec
    return outs


def cmd_score(args, write=True):
    check_freeze()
    nat, ctl = core.load_inputs(INPUTS)
    outs = collect(args.runs)
    items_by_id = {i["item_id"]: i for i in nat["items"] + ctl["positive_control_items"]}
    rows = []
    for config in [c for c in core.CONFIGS if c in outs]:
        rows += core.score_outputs(config, core.items_for(config, nat, ctl), outs[config])
    blind, mapping, template = core.adjudication_export(rows, outs, items_by_id)
    if write:
        d = Path(args.out)
        core.atomic_write(d / "scores.json", rows)
        core.atomic_write(d / "adjudication_blind.json", blind)
        core.atomic_write(d / "adjudication_key.json", mapping)
        if not (d / "adjudication.json").exists():
            core.atomic_write(d / "adjudication_template.json", template)
        log(f"scored {len(rows)} value rows over {len(outs)} configurations; {len(blind)} cases for blinded adjudication")
    return rows, mapping


def cmd_analyze(args):
    nat, ctl = core.load_inputs(INPUTS)
    rows, mapping = cmd_score(args, write=False)
    adj = None
    if args.adjudication:
        raw = json.loads(Path(args.adjudication).read_text())
        adj = {mapping[c]["case_key"]: v for c, v in raw.items() if v.get("identifies_authorized_argument") is not None}
    tasks = {(t["suite"], t["task"]): t for t in nat["tasks"] if t["in_population"]}
    result = {"protocol": core.PROTOCOL, "configs": {}, "pairs": {}, "decision": {}}
    lost_sets = {}
    for config in [c for c in core.CONFIGS if any(r["config"] == c for r in rows)]:
        rs = [r for r in rows if r["config"] == config]
        tech = Counter(r["technical"] for r in rs if r["technical"])
        res = {"label": core.CONFIGS[config]["label"], "technical_value_rows": dict(tech)}
        for rule in ("auto", "strict"):
            lt, ps = core.task_losses(rs, nat, rule)
            lt_hi, ps_hi = core.task_losses(rs, nat, rule, tech_as_loss=True)
            k = len(lt)
            res[rule] = {"k": k, "per_suite": ps, "band": core.band(ps),
                         "band_if_technical_lost": core.band(ps_hi), "k_if_technical_lost": len(lt_hi),
                         "cp95_one_sided_upper": round(core.cp_upper(k, 29), 4),
                         "cp95_one_sided_lower": round(core.cp_lower(k, 29), 4), "lost_tasks": sorted(lt)}
            if rule == "auto":
                lost_sets[config] = lt
        if adj is not None:
            try:
                lt, ps = core.task_losses(rs, nat, "adj", adj)  # case_key set by adjudication_export
                res["adjudicated"] = {"k": len(lt), "per_suite": ps, "band": core.band(ps), "lost_tasks": sorted(lt)}
            except KeyError:
                res["adjudicated"] = "INCOMPLETE"
        same = res["auto"]["band"] == res["strict"]["band"] == res["auto"]["band_if_technical_lost"] \
            == res["strict"]["band_if_technical_lost"]
        res["final_band"] = res["auto"]["band"] if same else (
            res["adjudicated"]["band"] if isinstance(res.get("adjudicated"), dict) else "PENDING_ADJUDICATION")
        res["unique_only_cases"] = sum(1 for r in rs if r.get("unique_only"))
        res["fallback_cases"] = sum(1 for r in rs if r.get("fallback"))
        res["positive_control_E4_lost"] = sorted({r["task"] for r in rs if r["set"] == "pc" and not r["technical"]
                                                  and not r["E4"]})
        res["causes"] = dict(Counter(r["cause"] for r in rs if r["set"] == "natural" and not r["technical"]
                                     and r.get("cause")))
        cons = []
        for r in rs:
            if r["set"] == "natural" and not r["technical"] and not r["E4"]:
                same_task = [x for x in rs if x["task"] == r["task"] and x["suite"] == r["suite"]]
                cons.append({"item_id": r["item_id"], "key": r["key"], "value": r["value"], "cause": r.get("cause"),
                             **core.consequence(r, same_task, tasks[(r["suite"], r["task"])])})
        res["consequence_potential"] = cons
        result["configs"][config] = res
    for a, b in core.PAIRS:
        if a in lost_sets and b in lost_sets:
            only_a = len(lost_sets[a] - lost_sets[b])
            only_b = len(lost_sets[b] - lost_sets[a])
            result["pairs"][f"{a}_vs_{b}"] = {"only_" + a: only_a, "only_" + b: only_b,
                                              "mcnemar_exact_p": round(core.mcnemar_exact(only_a, only_b), 4)}
    c = result["configs"]
    if "F0" in c:
        result["decision"]["published_sanitizer"] = c["F0"]["final_band"]
    if "Q0" in c and "G0" in c:
        bq, bg = c["Q0"]["final_band"], c["G0"]["final_band"]
        result["decision"]["open_class"] = ("DEPRIORITIZE" if bq == bg == "DEPRIORITIZE" else
                                            "ADVANCE (open-sanitizer only)" if "ADVANCE" in (bq, bg) else
                                            "PENDING_ADJUDICATION" if "PENDING_ADJUDICATION" in (bq, bg) else
                                            "INCONCLUSIVE")
    core.atomic_write(Path(args.out) / "analysis.json", result)
    print(json.dumps({k: {"final_band": v["final_band"], "auto_k": v["auto"]["k"], "strict_k": v["strict"]["k"],
                          "technical": v["technical_value_rows"], "pc_E4_lost": v["positive_control_E4_lost"]}
                      for k, v in result["configs"].items()} | {"decision": result["decision"]}, indent=1))


# ------------------------------------------------------------------------------------------- verify
def cmd_verify(args):
    import hashlib
    report = {"utc": now()}
    f = check_freeze()
    report["inputs_frozen"] = f["sha256"]
    report["code_unchanged_since_freeze"] = {n: hashlib.sha256((HERE / n).read_bytes()).hexdigest() == h
                                             for n, h in f["code_sha256"].items()}
    py = sys.executable
    v = subprocess.run([py, "-I", str(HERE / "validate_scorer.py"), str(INPUTS / "s0_inputs.json"), str(GATE2_RUNS),
                        str(HERE / "verification" / "scorer_validation.json")], capture_output=True, text=True)
    report["scorer_validation"] = json.loads(v.stdout) if v.returncode == 0 else {"error": v.stderr[-2000:]}
    t = subprocess.run([py, "-m", "unittest", "discover", "-s", str(HERE / "tests"), "-v"], capture_output=True,
                       text=True, cwd=HERE)
    report["unit_tests"] = {"returncode": t.returncode, "tail": t.stderr[-1500:]}
    for idx, uuid in PINNED_GPUS.items():
        try:
            nvs = subprocess.check_output(["nvidia-smi", "-i", str(idx), "--query-gpu=uuid,name,memory.used",
                                           "--format=csv,noheader"], text=True).strip()
            apps = subprocess.check_output(["nvidia-smi", "-i", str(idx), "--query-compute-apps=pid,used_memory",
                                            "--format=csv,noheader"], text=True).strip()
            report[f"gpu{idx}"] = {"query": nvs, "uuid_matches": uuid in nvs, "busy_with": apps or None}
        except Exception as exc:
            report[f"gpu{idx}"] = {"error": repr(exc)}
    if args.online:
        try:
            report["openrouter_pricing"] = fetch_pricing()
        except SystemExit as exc:
            report["openrouter_pricing"] = {"error": str(exc)}
        report["openrouter_key_present"] = bool(os.environ.get("OPENROUTER_API_KEY"))
    report["published_block_confirmed"] = (HERE / "prompts" / "D1_confirmation.json").exists()
    core.atomic_write(HERE / "verification" / "verify_report.json", report)
    print(json.dumps(report, indent=1, default=str))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("freeze")
    v = sub.add_parser("verify")
    v.add_argument("--online", action="store_true")
    o = sub.add_parser("open")
    o.add_argument("--run", required=True)
    o.add_argument("--profile", choices=["qwen", "gemma"], required=True)
    o.add_argument("--gpu", type=int, choices=sorted(PINNED_GPUS), default=GPU_INDEX)
    g = sub.add_parser("gemini")
    g.add_argument("--run", required=True)
    g.add_argument("--budget-usd", type=float, required=True)
    g.add_argument("--max-calls", type=int, required=True)
    g.add_argument("--configs", nargs="+", default=["F0", "F1"], choices=["F0", "F1"])
    g.add_argument("--allow-paid-api", action="store_true")
    for name in ("score", "analyze"):
        s = sub.add_parser(name)
        s.add_argument("--runs", nargs="+", required=True)
        s.add_argument("--out", default=str(HERE / "analysis"))
        if name == "analyze":
            s.add_argument("--adjudication")
    a = p.parse_args()
    {"freeze": cmd_freeze, "verify": cmd_verify, "open": cmd_open, "gemini": cmd_gemini, "score": cmd_score,
     "analyze": cmd_analyze}[a.cmd](a)


if __name__ == "__main__":
    main()
