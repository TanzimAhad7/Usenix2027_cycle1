"""S0 V2 control builder (CPU, standard library; read-only on the Gate 2 runs).

1. Positive-control items: the 24 Gate 2 primary records (candidate C0, `tool`), with the Gate 2 user request,
   source tool, untrusted content and the authorized identifier as the carried value; plus the classification of
   the RECORDED Gate 2 sanitizer output for each profile (expected: Qwen loses E4 in exactly
   slack.2.1, workspace.0.0, workspace.1.2, workspace.3.0; Gemma in none).
2. Replay index: every recorded Gate 2 sanitizer request (requests.jsonl, kind == "sanitizer") per profile, with
   its line number, request id, token ids digest and recorded output, and the request used by each C0 `tool` cell.

  python build_controls.py GATE2_RUNS_DIR OUT_JSON      (refuses to overwrite)
"""
import json
import re
import sys
from hashlib import sha256
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import retention  # noqa: E402

RUNS, OUT = Path(sys.argv[1]), Path(sys.argv[2])
PIPE = "20261111T185944Z_gate2_all_both"


def label(original, value):
    i = original.find(str(value))
    return [w.lower() for w in re.findall(r"[A-Za-z]+", original[:i])[-2:]] if i >= 0 else []


def forms(value):
    v = str(value)
    return {"exact": [v], "equivalent": sorted({v.lower(), v.upper()} - {v})}


items, expected, replay = [], {}, {}
for profile in ("qwen", "gemma"):
    run = RUNS / f"{PIPE}_{profile}"
    plan = json.loads((run / "gate2_plan.json").read_text())
    ep = run / f"model_{profile}" / "episodes"
    reqs = {}
    for n, line in enumerate((run / f"model_{profile}" / "requests.jsonl").read_text().splitlines(), 1):
        r = json.loads(line)
        if r["kind"] == "sanitizer":
            reqs[r["id"]] = {"line": n, "id": r["id"], "limit": r["limit"], "n_pids": len(r["pids"]),
                             "pids_sha256": sha256(json.dumps(r["pids"]).encode()).hexdigest(),
                             "recorded_text": r["text"], "recorded_generated_len": len(r["generated"]),
                             "limit_reached": r["limit_reached"], "conditions": r["conditions"]}
    c0 = {}
    lost = []
    for b in plan["bases"]:
        y = json.loads((ep / f"{b['id']}.C0.tool.l0.scalar.json").read_text())
        ev = next((e for e in y["events"] if e.get("transform")), None)
        prim = next(e for e in y["events"] if (e.get("result") or {}).get("kind") == "primary")
        original = prim["result"]["content"]
        good = b["good"][b["identifier"]]
        vals = good if isinstance(good, list) else [good]
        item = {"item_id": f"pc.{b['id']}", "suite": b["family"], "task": b["id"], "control": "gate2_primary_C0",
                "user_request": next(m["content"] for m in y["initial"] if m["role"] == "user"),
                "source_tool": prim["dispatched"]["function"], "untrusted_content": original,
                "proposed_actions": [ev["proposal"]] if ev else [],
                "carried_values": [{"key": b["identifier"], "value": v, "forms": forms(v),
                                    "anchor": {"kind": "text", "label": label(original, v)}} for v in vals]}
        if profile == "qwen":
            items.append(item)
        else:  # the Gemma run must have produced the same primary records
            q = next(i for i in items if i["item_id"] == item["item_id"])
            assert q["untrusted_content"] == item["untrusted_content"] and q["user_request"] == item["user_request"]
        if ev is not None:
            out = ev["transform"]["sanitizers"][0]["result"]["text"]
            if not all(r["E4"] for r in retention.score_item(item, out)):
                lost.append(b["id"])
            rid = ev["transform"]["sanitizers"][0]["result"]["id"]  # the exact request id Gate 2 executed
            if rid not in reqs:
                raise SystemExit(f"Recorded request {rid} for {b['id']} missing from requests.jsonl")
            if reqs[rid]["recorded_text"] != out:
                raise SystemExit(f"Recorded request text differs from episode receipt for {b['id']}")
            c0[b["id"]] = rid
        else:
            c0[b["id"]] = None  # scalar did not flag this cell (Gemma)
    expected[profile] = {"recorded_E4_lost_C0_tool": sorted(lost), "flagged_C0_tool": sum(v is not None for v in c0.values())}
    replay[profile] = {"requests": sorted(reqs.values(), key=lambda r: r["line"]), "c0_tool_request": c0}

OUT.parent.mkdir(parents=True, exist_ok=True)
if OUT.exists():
    raise SystemExit(f"{OUT} exists (frozen)")
body = {"protocol": "S0_SANITIZER_FIDELITY_V2_CONTROLS", "gate2_pipeline": PIPE,
        "builder_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "positive_control_items": items, "expected_recorded": expected, "replay": replay}
OUT.write_text(json.dumps(body, indent=1, default=str) + "\n")
print(json.dumps({"positive_control_items": len(items), "expected_recorded": expected,
                  "replay_requests": {p: len(v["requests"]) for p, v in replay.items()}}, indent=1))
