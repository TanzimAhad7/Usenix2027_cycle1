"""Exploratory re-mining of the frozen Gate 2 runs (read-only).
1. Paired retention of the IDENTIFIER (who/where) vs the PARAMETER (what/how much) in the same sanitized record.
2. What the actor does immediately after a remediation that removed the identifier: write / re-read / final / unparsed.
  python mine_gate2.py GATE2_RUNS OUT_JSON
"""
import json, sys
from collections import Counter
from pathlib import Path
RUNS, OUT = Path(sys.argv[1]), Path(sys.argv[2])
def forms(v):
    out = {str(v)}
    if isinstance(v, float): out |= {f"{v:.2f}", f"{v:.1f}", str(int(v)) if v == int(v) else str(v)}
    return out
def has(v, text):
    vals = v if isinstance(v, list) else [v]
    return all(any(f in text for f in forms(x)) for x in vals)
res = {}
for prof in ("qwen", "gemma"):
    run = RUNS / f"20261111T185944Z_gate2_all_both_{prof}"
    plan = json.loads((run/"gate2_plan.json").read_text()); bases = {b["id"]: b for b in plan["bases"]}
    pair = Counter(); pair_fam = Counter(); after_loss = Counter()
    for p in sorted((run/f"model_{prof}"/"episodes").glob("*.tool.l0.*.json")):
        y = json.loads(p.read_text()); arm = y["arm"]; b = bases[y["cell"]["base"]]
        ev = next((e for e in y["events"] if e.get("transform")), None)
        if ev is None: continue
        after = ev.get("primary_after") or ""
        idk = has(b["good"][b["identifier"]], after)
        if arm in ("scalar", "forced_sanitize") and y["cell"]["candidate"] in ("C0","C1","C2","C3","C3x"):
            pk = has(b["good"][b["parameter"]], after)
            pair[(arm, f"id={int(idk)}", f"param={int(pk)}")] += 1
            pair_fam[(arm, b["family"], b["parameter"], f"id={int(idk)}", f"param={int(pk)}")] += 1
        if arm in ("scalar", "forced_sanitize", "surgical_delete", "null_clean") and not idk:
            ex = ev.get("dispatched")
            kind = ("unparsed" if y["terminal"] == "REGEN_UNPARSED" else "final_abstain" if y["terminal"] == "REGEN_FINAL"
                    else "write" if ex and ex.get("function") == b["action"] else "re-read_or_other_tool" if ex else "none")
            after_loss[(arm, kind)] += 1
    res[prof] = {"id_vs_param": {"|".join(k): v for k, v in sorted(pair.items())},
                 "id_vs_param_by_family": {"|".join(k): v for k, v in sorted(pair_fam.items()) if k[0]=="forced_sanitize"},
                 "action_after_identifier_loss": {"|".join(k): v for k, v in sorted(after_loss.items())}}
OUT.write_text(json.dumps(res, indent=1)+"\n"); print(json.dumps(res, indent=1))
