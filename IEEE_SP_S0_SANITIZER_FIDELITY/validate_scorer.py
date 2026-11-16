"""CPU validation of the S0 scorer before any inference.

A. Synthetic fixtures on every natural S0 item (known answers):
   identity (sanitized == original)          -> E1..E4 all retained          (specificity)
   oracle deletion of every value form       -> E2 lost                       (sensitivity)
   same-type substitution                    -> E1, E2 lost
   anchored-record removal (structured)      -> E3 lost
   YAML -> JSON re-serialization (lossless)  -> E3 retained (structure-agnostic)
B. Positive control on REAL recorded Gate 2 sanitizer outputs (no new inference): for every Gate 2 base x candidate
   C0..C3x under the scalar arm, score the authorized identifier in the sanitizer output; expected Qwen = the 4 known
   bases, Gemma = 0 (IEEE_SP_GATE2_GLOBAL_FORENSIC_RECONCILIATION_AND_NEXT_SCIENTIFIC_DECISION_2026-11-11.md III.2).

  python validate_scorer.py S0_INPUTS_JSON GATE2_RUNS_DIR OUT_JSON
"""
import copy
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import retention as score  # noqa: E402

INPUTS, RUNS, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
data = json.loads(INPUTS.read_text())
report = {"fixtures": {}, "fixture_failures": [], "positive_control": {}}


def all_forms(cv):
    return sorted({cv["forms"]["exact"][0], *cv["forms"]["equivalent"]}, key=len, reverse=True)


def delete_value(text, cv):
    for f in all_forms(cv):
        text = re.sub(r"(?<![\w@.\-])" + re.escape(f) + r"(?![\w@\-]|\.\d)", "", text, flags=re.IGNORECASE)
    return text


def substitute(text, cv):
    v = str(cv["value"])
    new = ("zz.unrelated@example.org" if "@" in v else "XX00ZZZZ0000000000000000" if re.fullmatch(r"[A-Z]{2}\d{2}\w+", v)
           else "99887766" if v.replace(".", "").isdigit() else "zz_unrelated_value")
    for f in all_forms(cv):
        text = re.sub(r"(?<![\w@.\-])" + re.escape(f) + r"(?![\w@\-]|\.\d)", new, text, flags=re.IGNORECASE)
    return text


def drop_records(text, cv):
    obj = yaml.safe_load(text)
    target = {(h["field"], json.dumps(h["siblings"], sort_keys=True, default=str)) for h in cv["anchor"]["records"]}

    def anchored(x):
        # same sibling rule as build_inputs.anchor (bools are ints there, so they are included)
        return isinstance(x, dict) and any(json.dumps({k: v for k, v in x.items() if k != f and isinstance(v, (str, int, float))
                                                       and len(str(v)) <= 120},
                                                      sort_keys=True, default=str) == sig for f, sig in target)

    def walk(o):
        if isinstance(o, list):
            return [walk(x) for x in o if not anchored(x)]
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items()}
        return o
    return yaml.safe_dump(walk(obj))


checks = {"identity": lambda t, cv: t, "oracle_delete": delete_value, "substitute": substitute,
          "json_reserialize": lambda t, cv: json.dumps(score.parse(t), default=str)
          if isinstance(score.parse(t), (list, dict)) else t}
expect = {"identity": {"E1": True, "E2": True, "E3": True, "E4": True}, "oracle_delete": {"E2": False},
          "substitute": {"E1": False, "E2": False}, "json_reserialize": {"E3": True}}
for name, fn in checks.items():
    n = ok = 0
    for it in data["items"]:
        for cv in it["carried_values"]:
            res = score.score_value(it["untrusted_content"], fn(it["untrusted_content"], cv), cv)
            n += 1
            exp = dict(expect[name])
            if name == "identity":  # E1 can only hold if the exact form was in the original
                exp["E1"] = score.present(it["untrusted_content"], cv["forms"]) == "exact"
            good = all(res[k] == v for k, v in exp.items())
            ok += good
            if not good:
                report["fixture_failures"].append({"fixture": name, "item": it["item_id"], "key": cv["key"],
                                                   "value": cv["value"], "result": res})
    report["fixtures"][name] = {"values": n, "as_expected": ok}
n = ok = 0
for it in data["items"]:
    for cv in it["carried_values"]:
        if cv["anchor"]["kind"] == "structured" and cv["anchor"].get("match") == "field_equal":
            try:
                res = score.score_value(it["untrusted_content"], drop_records(it["untrusted_content"], cv), cv)
            except Exception as exc:  # recorded, not hidden
                res = {"error": repr(exc), "E3": None}
            n += 1
            ok += res.get("E3") is False
            if res.get("E3") is not False:
                report["fixture_failures"].append({"fixture": "drop_record", "item": it["item_id"], "key": cv["key"],
                                                   "value": cv["value"], "result": res})
report["fixtures"]["drop_record"] = {"values": n, "as_expected": ok}

# B. positive control on recorded Gate 2 outputs
for profile in ("qwen", "gemma"):
    run = RUNS / f"20261111T185944Z_gate2_all_both_{profile}"
    plan = json.loads((run / "gate2_plan.json").read_text())
    lost = {}
    for b in plan["bases"]:
        good = b["good"][b["identifier"]]
        vals = good if isinstance(good, list) else [good]
        for cand in ("C0", "C1", "C2", "C3", "C3x"):
            y = json.loads((run / f"model_{profile}" / "episodes" / f"{b['id']}.{cand}.tool.l0.scalar.json").read_text())
            ev = next((e for e in y["events"] if e.get("transform")), None)
            if ev is None:
                continue  # scalar did not flag (Gemma: some cells)
            original = next(e["result"]["content"] for e in y["events"] if (e.get("result") or {}).get("kind") == "primary")
            sanitized = ev["transform"]["sanitizers"][0]["result"]["text"]
            for v in vals:
                fm = {"exact": [str(v)], "equivalent": []}
                lab = re.findall(r"[A-Za-z]+", original[:original.find(str(v))])[-2:] if str(v) in original else []
                cv = {"key": b["identifier"], "value": v, "forms": fm, "anchor": {"kind": "text", "label": [x.lower() for x in lab]}}
                res = score.score_value(original, sanitized, cv)
                if not res["E4"]:
                    lost.setdefault("E4|" + cand, set()).add(b["id"])
                if not res["E3"]:
                    lost.setdefault("E3|" + cand, set()).add(b["id"])
    report["positive_control"][profile] = {c: sorted(s) for c, s in sorted(lost.items())}
OUT.write_text(json.dumps(report, indent=1, default=str) + "\n")
print(json.dumps({"fixtures": report["fixtures"], "n_failures": len(report["fixture_failures"]),
                  "positive_control": report["positive_control"]}, indent=1))
