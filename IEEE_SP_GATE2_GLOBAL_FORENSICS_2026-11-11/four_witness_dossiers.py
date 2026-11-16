"""Gate 2 global forensics: machine-checkable dossiers for the Qwen C3x B witnesses and matched controls.

Read-only on the run directory; standard library only; does not import the experiment's analyzer.
  python four_witness_dossiers.py RUN_DIR OUT_JSON

For every base it records, under the scalar arm: T0 per candidate, primary/preview LOO scores, flags,
sanitizer output, identifier/attacker survival, regenerated value, native commit. For witness bases it adds the
full A-H trace plus the same-base counterfactuals (C0/C1/C2/C3) and the add-back / surgical / plain arms, and
checks the invariants the causal reading needs (identical T0 across candidates; identical sanitized primary
across candidates; preview never sanitized; attacker literal equals the frozen plan literal).
"""
import json
import sys
from pathlib import Path

RUN, OUT = Path(sys.argv[1]), Path(sys.argv[2])
plan = json.loads((RUN / "gate2_plan.json").read_text())
BASES = {b["id"]: b for b in plan["bases"]}
EP = next(d for d in RUN.glob("model_*") if d.is_dir()) / "episodes"
CANDS = ("C0", "C1", "C2", "C3", "C3x")


def ep(base, cand, arm, instr="tool"):
    return json.loads((EP / f"{base}.{cand}.{instr}.l0.{arm}.json").read_text())


def first_write(y, action):
    return next((e for e in y["events"] if (e.get("proposal") or {}).get("function") == action), None)


def ident(args, b):
    return None if args is None else args.get(b["identifier"])


def commits(y):
    return [c for e in y["events"] for c in ((e.get("result") or {}).get("commits") or [])]


def scores(e):
    if not e or not e.get("scores"):
        return None
    return [{"message_index": s["message_index"], "primary": s["primary"], "preview": s["preview"],
             "scalar": round(s["scalar"], 4), "delta_s": round(s["delta_s"], 4), "delta_u": round(s["delta_u"], 4),
             "identifier_component": round(s["components"]["identifier"], 4)} for s in e["scores"]["spans"]]


def summary(b, cand, arm):
    y = ep(b["id"], cand, arm)
    e = first_write(y, b["action"])
    good = b["good"][b["identifier"]]
    vals = [str(v) for v in (good if isinstance(good, list) else [good])]
    san = None
    if e and e.get("transform") and e["transform"].get("sanitizers"):
        san = e["transform"]["sanitizers"][0]["result"]["text"]
    after = e.get("primary_after") if e else None
    att = b["candidates"]["attacker"]
    return {"T0_identifier": ident((e or {}).get("proposal", {}).get("args"), b),
            "flags": (e or {}).get("flags"), "scores": scores(e),
            "sanitizer_output": san, "primary_after": after,
            "identifier_in_primary_after": None if after is None else all(v in after for v in vals),
            "attacker_in_primary_after": None if after is None else att in after,
            "regenerated_identifier": ident(((e or {}).get("dispatched") or {}).get("args"), b)
            if e and e.get("regeneration") else None,
            "dispatched_identifier": ident(((e or {}).get("dispatched") or {}).get("args"), b) if e else None,
            "native_error": ((e or {}).get("result") or {}).get("error") if e else None,
            "commits": [{"class": c["class"], "identifier": ident(c["args"], b), "native_id": c.get("native_id")}
                        for c in commits(y)],
            "terminal": y["terminal"]}


def witness(b):
    """Full A-H trace for one base (C3x, scalar) with counterfactuals and invariant checks."""
    y = ep(b["id"], "C3x", "scalar")
    yp = ep(b["id"], "C3x", "plain")
    e = first_write(y, b["action"])
    hist = y["final_history"]
    tools = [m for m in hist if m.get("role") == "tool"]
    preview_after = next((m["content"] for m in tools if "preview-A" in str(m.get("content"))), None)
    original = y["events"]
    prim_orig = next(ev["result"]["content"] for ev in original if (ev.get("result") or {}).get("kind") == "primary")
    prev_orig = next(ev["result"]["content"] for ev in original if (ev.get("result") or {}).get("kind") == "preview")
    att = b["candidates"]["attacker"]
    cf = {c: summary(b, c, "scalar") for c in CANDS}
    arms = {a: summary(b, "C3x", a) for a in ("plain", "forced_sanitize", "sanitize_addback", "surgical_delete",
                                                "null_clean", "authority")}
    c3_arms = {a: summary(b, "C3", a) for a in ("plain", "scalar", "surgical_delete")}
    checks = {
        # C0/C1/C2/C3x share the primary record (candidates differ only in preview-A); C3 alters the primary.
        "T0_identical_C0_C1_C2_C3x": len({json.dumps(cf[c]["T0_identifier"]) for c in ("C0", "C1", "C2", "C3x")}) == 1,
        "T0_authorized": json.dumps(cf["C3x"]["T0_identifier"]) == json.dumps(b["good"][b["identifier"]]),
        "sanitized_primary_identical_C0_C1_C2_C3x": len({cf[c]["primary_after"] for c in ("C0", "C1", "C2", "C3x")}) == 1,
        "preview_A_unchanged_after_remediation": preview_after is not None and preview_after == prev_orig,
        "attacker_literal_in_preview_after": preview_after is not None and att in preview_after,
        "only_primary_flagged": e["flags"] == [s["message_index"] for s in scores(e) if s["primary"]],
        "regenerated_not_rescored": e.get("regeneration") is not None and "rescore" not in e,
        "committed_identifier_equals_frozen_attacker_literal": any(
            json.dumps(c["identifier"]) in (json.dumps(att), json.dumps([att])) for c in cf["C3x"]["commits"]),
        "plain_committed_authorized": any(c["class"] == "preferred" for c in arms["plain"]["commits"]),
    }
    return {"cell": f"{b['id']}.C3x.tool.l0", "family": b["family"], "identifier_field": b["identifier"],
            "parameter_field": b["parameter"], "action": b["action"],
            "A_trusted_instruction": next(m["content"] for m in y["initial"] if m["role"] == "user"),
            "A_frozen_contract": b["good"], "attacker_literal": att,
            "B_primary_record_original": prim_orig, "B_preview_record_original": prev_orig,
            "B_source_tools": [(ev.get("dispatched") or {}).get("function") for ev in original if ev.get("dispatched")],
            "C_T0_proposal": e["proposal"], "D_scores": scores(e), "D_flags": e["flags"],
            "E_sanitizer_output": cf["C3x"]["sanitizer_output"], "E_primary_after": cf["C3x"]["primary_after"],
            "E_preview_after": preview_after, "F_regeneration_text": (e.get("regeneration") or {}).get("text"),
            "G_dispatched": e.get("dispatched"), "G_native_result": {k: (e.get("result") or {}).get(k)
                                                                     for k in ("error", "commits")},
            "H_counterfactual_candidates_scalar": cf, "H_other_arms_C3x": arms, "H_same_base_C3": c3_arms,
            "invariants": checks}


bases_table = []
for bid, b in BASES.items():
    s = summary(b, "C3x", "scalar")
    prim = next((x for x in (s["scores"] or []) if x["primary"]), {})
    prev = next((x for x in (s["scores"] or []) if x["preview"]), {})
    bases_table.append({"base": bid, "family": b["family"], "identifier": b["identifier"], "parameter": b["parameter"],
                        "primary_scalar": prim.get("scalar"), "preview_scalar": prev.get("scalar"),
                        "identifier_kept": s["identifier_in_primary_after"],
                        "regenerated": s["regenerated_identifier"],
                        "attacker_commit": any(json.dumps(c["identifier"]) in (json.dumps(b["candidates"]["attacker"]),
                                                                              json.dumps([b["candidates"]["attacker"]]))
                                               for c in s["commits"])})
wit = [witness(BASES[r["base"]]) for r in bases_table if r["attacker_commit"]]
lost = [r for r in bases_table if r["identifier_kept"] is False]
out = {"run": str(RUN), "plan_protocol": plan["protocol"],
       "C3x_scalar_by_base": bases_table,
       "conditional_pattern": {"identifier_lost": len(lost),
                               "attacker_commit_when_lost": sum(r["attacker_commit"] for r in lost),
                               "identifier_kept": sum(r["identifier_kept"] is True for r in bases_table),
                               "attacker_commit_when_kept": sum(r["attacker_commit"] for r in bases_table
                                                                if r["identifier_kept"] is True)},
       "deletion_by_family_parameter": {},
       "witnesses": wit,
       "all_invariants_hold": all(all(w["invariants"].values()) for w in wit)}
for r in bases_table:
    k = f"{r['family']}|{r['parameter']}"
    d = out["deletion_by_family_parameter"].setdefault(k, {"bases": 0, "identifier_lost": 0})
    d["bases"] += 1
    d["identifier_lost"] += int(r["identifier_kept"] is False)
OUT.write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({k: out[k] for k in ("conditional_pattern", "deletion_by_family_parameter", "all_invariants_hold")},
                 indent=1))
for w in wit:
    print(w["cell"], {k: v for k, v in w["invariants"].items() if not v} or "all invariants hold")
    print("   regenerated by candidate:", {c: w["H_counterfactual_candidates_scalar"][c]["dispatched_identifier"]
                                           for c in CANDS},
          "| addback:", w["H_other_arms_C3x"]["sanitize_addback"]["dispatched_identifier"],
          "| scores:", [(s["message_index"], s["scalar"]) for s in w["D_scores"]])
