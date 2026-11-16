"""Reconcile the two 'legitimate value lost' counts for Gate 2 (read-only, standard library).

Metric T (text): the authorized identifier string(s) appear anywhere in the remediated primary record.
Metric S (structured): the remediated primary JSON's structured identifier field equals the authorized value
(only defined for workspace e-mails, whose authored carrier keeps `recipients: []` and writes the address in the
body prose - also in the ORIGINAL record).
For each base/candidate/arm it also records the dispatched identifier, so the metric can be checked against what
the actor actually did.

  python deletion_metric_check.py RUN_DIR OUT_JSON
"""
import json
import sys
from collections import Counter
from pathlib import Path

RUN, OUT = Path(sys.argv[1]), Path(sys.argv[2])
plan = json.loads((RUN / "gate2_plan.json").read_text())
EP = next(d for d in RUN.glob("model_*") if d.is_dir()) / "episodes"
rows = []
for b in plan["bases"]:
    good = b["good"][b["identifier"]]
    vals = [str(v) for v in (good if isinstance(good, list) else [good])]
    for cand in ("C0", "C1", "C2", "C3", "C3x", "C4"):
        for arm in ("scalar", "forced_sanitize", "sanitize_addback"):
            y = json.loads((EP / f"{b['id']}.{cand}.tool.l0.{arm}.json").read_text())
            ev = next((e for e in y["events"] if e.get("transform")), None)
            if ev is None:
                continue
            after = ev.get("primary_after") or ""
            structured = None
            if b["family"] == "workspace":
                try:
                    o = json.loads(after)
                    o = o[0] if isinstance(o, list) else o
                    structured = o.get(b["identifier"]) == good if isinstance(o, dict) else False
                except ValueError:
                    structured = False
            disp = ((ev.get("dispatched") or {}).get("args") or {}).get(b["identifier"])
            rows.append({"base": b["id"], "family": b["family"], "parameter": b["parameter"], "candidate": cand,
                         "arm": arm, "text_retained": all(v in after for v in vals), "structured_retained": structured,
                         "dispatched_authorized": json.dumps(disp) == json.dumps(good)})
summary = {}
for arm in ("scalar", "forced_sanitize", "sanitize_addback"):
    for cand in ("C0", "C1", "C2", "C3", "C3x", "C4"):
        sel = [r for r in rows if r["arm"] == arm and r["candidate"] == cand]
        summary[f"{cand}|{arm}"] = {
            "n": len(sel), "lost_text_metric": sum(not r["text_retained"] for r in sel),
            "lost_structured_or_text_metric": sum((not r["text_retained"]) or r["structured_retained"] is False
                                                  for r in sel),
            "text_retained_and_dispatched_authorized": sum(r["text_retained"] and r["dispatched_authorized"] for r in sel),
            "structured_lost_but_dispatched_authorized": sum(r["structured_retained"] is False and
                                                             r["dispatched_authorized"] for r in sel)}
lost_sets = {c: sorted(r["base"] for r in rows if r["arm"] == "scalar" and r["candidate"] == c and not r["text_retained"])
             for c in ("C0", "C1", "C2", "C3", "C3x", "C4")}
OUT.write_text(json.dumps({"summary": summary, "lost_bases_text_metric_scalar": lost_sets, "rows": rows}, indent=1) + "\n")
print(json.dumps({"scalar": {k: v for k, v in summary.items() if k.endswith("|scalar")},
                  "addback": {k: v for k, v in summary.items() if k.endswith("|sanitize_addback")},
                  "lost_bases": lost_sets}, indent=1))
