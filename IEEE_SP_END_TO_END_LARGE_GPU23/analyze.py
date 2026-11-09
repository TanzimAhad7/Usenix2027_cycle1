"""Outcome-blind contrasts, always grouped by independent task base."""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import asdict
import math
import random
from statistics import fmean, mean
from pathlib import Path

from design import Cell, read, write
from score import file_hash

EPS = 0.08
N_BOOT = 4000
INTERVALS = ("interval95", "template_interval95")


def summarize(values, families):
    if not values:
        return {"n_bases": 0}
    groups, templates = defaultdict(list), defaultdict(list)
    template_family = {}
    for base, val in sorted(values.items()):
        family, template = families[base], base.rsplit(".", 1)[0]
        groups[family].append(val)
        templates[template].append(val)
        template_family[template] = family

    def interval(strata, seed):
        rng = random.Random(seed)
        draws = sorted(fmean(rng.choice(items) for items in strata for _ in items) for _ in range(N_BOOT))
        return [draws[int(.025 * N_BOOT)], draws[int(.975 * N_BOOT)]]

    template_means = {key: mean(items) for key, items in templates.items()}
    cluster_strata = defaultdict(list)
    for key, value in template_means.items():
        cluster_strata[template_family[key]].append(value)
    return {"n_bases": len(values), "n_templates": len(templates), "mean": mean(values.values()),
            "interval95": interval(tuple(templates.values()), 20261107),
            "template_interval95": interval(tuple(cluster_strata.values()), 20261108),
            "positive": sum(v > 0 for v in values.values()), "negative": sum(v < 0 for v in values.values()),
            "family_mean": {k: mean(v) for k, v in groups.items()},
            "template_mean": template_means, "per_base": values}


def boot_values(values, families):
    return summarize({base: mean(v) for base, v in values.items() if v}, families)


def components(vector, roles):
    return {role: sum(x for x, label in zip(vector, roles) if label == role) / len(vector)
            for role in ("identifier", "parameter", "other")} | {"whole": mean(vector)}


def difference(a, b):
    return [x - y for x, y in zip(a, b, strict=True)]


def anchors(prepared, scores):
    rows = prepared["anchors"]
    data, historical, matched_drift = {}, {}, []
    for r in rows:
        key = (r["base"], r["source"], r["echo"], r["variant"])
        historical[key] = r["historical"]
        vals = scores.get(r["request"])
        if vals is None:
            continue
        data[key] = vals
        if r["completion_match"] and r["prompt_match"]:
            matched_drift.extend(abs(a - b) for a, b in zip(vals, r["historical"], strict=True))
    source_contrasts = []
    for base in sorted({r["base"] for r in rows}):
        for echo in ("ECHO", "SHAM"):
            def relocation(table):
                def margin(src):
                    return mean(difference(table[base, src, echo, "DELETE__S_REL"],
                                           table[base, src, echo, "DELETE__U"]))
                return margin("TOOL_ID") - margin("USER_ID")
            try:
                source_contrasts.append({"base": base, "echo": echo, "live": relocation(data),
                                         "historical": relocation(historical)})
            except KeyError:
                continue
    return {"scope": "historical Gemma-3-12B-IT development cases excluded from prospective contrasts. Differences at matching token IDs are comparisons across checkpoints and inference stacks.",
            "matched_prompt_ids": sum(r["prompt_match"] for r in rows),
            "matched_completion_ids": sum(r["completion_match"] for r in rows),
            "scored": len(data), "scheduled": len(rows), "source_contrasts": source_contrasts,
            "matched_token_abs_logp_delta_mean": mean(matched_drift) if matched_drift else None,
            "matched_token_abs_logp_delta_max": max(matched_drift, default=None)}


def analyze(prepared, scores, manifest):
    meta = {r["id"]: r for r in manifest["cells"]}
    families = {r["base"]: r["family"] for r in manifest["bases"]}
    cells, missing, table = {}, [], []
    for row in prepared["observations"]:
        c = meta[row["id"]]
        variants = {k: scores.get(key) for k, key in row["requests"].items()}
        absent = [v for v, score in variants.items() if score is None]
        if absent:
            missing.append({"cell": c["id"], "base": c["base"], "panel": c["panel"], "variants": absent})
            continue
        if c["panel"] == "deletion":
            delta = difference(variants["delete_s"], variants["delete_u"])
        else:
            delta = difference(variants["mask_s"], variants["mask_u"])
        roles = row["action"]["roles"]
        d = {"margin": components(delta, roles), "strict": components(delta, row["action"]["strict_roles"])}
        if "full" in variants:
            d["availability_gain"] = components(
                difference(variants["full"], variants["mask_" + c["source"]]), roles)
        if c["panel"] == "echo":
            d["echo_rescue"] = components(difference(variants["mask_u"], variants["mask_u_echo"]), roles)
        obj = Cell(**{k: v for k, v in c.items() if k != "id"})
        cells[obj] = d
        table.append(c | d)

    def slot_values(panel, focal, lexical, response="margin", role=None):
        vals, strata = defaultdict(list), defaultdict(lambda: defaultdict(list))
        role = role or focal
        for c, d in cells.items():
            if c.panel != panel or c.focal != focal or c.lexical != lexical or c.source != "u":
                continue
            pair = Cell(**(asdict(c) | {"source": "s"}))
            if pair not in cells:
                continue
            # Positive direction means greater apparent support at the supplying source.
            v = d[response][role] - cells[pair][response][role]
            vals[c.base].append(v)
            strata[f"{c.swap}/{c.reverse}/{c.layout}"][c.base].append(v)
        return vals, strata

    contrasts = {}
    for focal in ("identifier", "parameter"):
        other = "parameter" if focal == "identifier" else "identifier"
        for lexical in ("literal", "split"):
            name = f"{focal}/{lexical}"
            wanted, strata = slot_values("relocation", focal, lexical)
            rest, _ = slot_values("relocation", focal, lexical, role=other)
            strict, _ = slot_values("relocation", focal, lexical, response="strict")
            primary_adv = {b: mean(wanted[b]) - mean(rest[b]) for b in wanted if b in rest}
            gain = defaultdict(list)
            for c, d in cells.items():
                if (c.panel, c.focal, c.lexical) == ("relocation", focal, lexical):
                    gain[c.base].append(d["availability_gain"][focal])
            contrasts[name] = {
                "focal_relocation": boot_values(wanted, families),
                "nonfocal_relocation": boot_values(rest, families),
                "focal_minus_nonfocal": summarize(primary_adv, families),
                "strict_focal_relocation": boot_values(strict, families),
                "full_minus_mask_supplying_slot": boot_values(gain, families),
                "role_order_layout": {s: boot_values(x, families) for s, x in sorted(strata.items())},
            }
            for panel in ("redundancy", "serialization", "deletion"):
                x, _ = slot_values(panel, focal, lexical)
                # Match each sensitivity row to the canonical core stratum.
                y = strata.get("0/0/table", {})
                contrasts[name][panel] = {
                    "raw": boot_values(x, families),
                    "core_minus_sensitivity": summarize(
                        {b: mean(x0) - mean(x[b]) for b, x0 in y.items() if b in x}, families),
                }

    nuisance = {}
    for factor, lo, hi in (("swap", 0, 1), ("reverse", 0, 1), ("layout", "table", "json")):
        vals = defaultdict(list)
        for c, d in cells.items():
            if c.panel == "relocation" and getattr(c, factor) == lo:
                partner = Cell(**(asdict(c) | {factor: hi}))
                if partner in cells:
                    vals[c.base].append(abs(cells[partner]["margin"]["whole"] - d["margin"]["whole"]))
        nuisance[f"{factor}_fixed_value_location_abs_margin_change"] = boot_values(vals, families)

    def echo_values(measure, role, transform):
        out = defaultdict(list)
        for c in cells:
            if c.panel != "echo" or c.bound or c.copy:
                continue
            group = [Cell(**(asdict(c) | {"bound": b, "copy": e})) for b, e in ((0, 0), (0, 1), (1, 0), (1, 1))]
            if all(k in cells for k in group):
                out[c.base].append(transform(*(cells[k][measure][role] for k in group)))
        return boot_values(out, families)

    echo = {}
    for role in ("parameter", "identifier", "other", "whole"):
        echo[role] = {
            "margin_copy_when_current": echo_values("margin", role, lambda a, b, c, d: d - c),
            "margin_copy_when_archived": echo_values("margin", role, lambda a, b, c, d: b - a),
            "margin_linkage_interaction": echo_values("margin", role, lambda a, b, c, d: (d - c) - (b - a)),
            "rescue_linkage_interaction": echo_values("echo_rescue", role, lambda a, b, c, d: (d - c) - (b - a)),
        }

    def positive(r):
        return r.get("n_bases") == len(families) and all(r[k][0] > 0 for k in INTERVALS)

    def equivalent(r):
        return r.get("n_bases") == len(families) and all(-EPS < r[k][0] <= r[k][1] < EPS for k in INTERVALS)

    requirements = {}
    for focal in ("identifier", "parameter"):
        r = contrasts[f"{focal}/split"]
        requirements[focal] = {
            "split_usage_positive": positive(r["full_minus_mask_supplying_slot"]),
            "split_selectivity_positive": positive(r["focal_minus_nonfocal"]),
            "split_strict_focal_positive": positive(r["strict_focal_relocation"]),
            "split_redundant_backup_attenuates_effect": positive(r["redundancy"]["core_minus_sensitivity"]),
            "split_no_role_order_layout_reversal": len(r["role_order_layout"]) == 8 and all(
                s.get("n_bases") == len(families) and s["mean"] > 0 for s in r["role_order_layout"].values()),
            "split_all_family_means_positive": len(r["focal_relocation"].get("family_mean", {})) == 4
            and all(x > 0 for x in r["focal_relocation"].get("family_mean", {}).values()),
        }
    e = echo["parameter"]["rescue_linkage_interaction"]
    i = echo["identifier"]["margin_linkage_interaction"]
    em = echo["parameter"]["margin_linkage_interaction"]
    echo_gate = {"positive_linked_parameter_rescue": positive(e),
                 "negative_linked_parameter_margin_shift": em.get("n_bases") == len(families)
                 and all(em[k][1] < 0 for k in INTERVALS),
                 "identifier_margin_interaction_equivalent": equivalent(i)}
    ready = not missing and all(all(v.values()) for v in requirements.values()) and all(echo_gate.values())
    return {
        "label": prepared["label"], "protocol": manifest["protocol"], "scientific_unit": "task base",
        "n_scheduled_cells": len(prepared["observations"]), "n_complete_cells": len(table),
        "n_unique_requests": len(prepared["requests"]), "n_scored_unique_requests": len(scores),
        "missing": missing, "historical_anchors": anchors(prepared, scores), "relocation": contrasts,
        "echo": echo, "nuisance": nuisance, "relocation_requirements": requirements, "echo_requirements": echo_gate,
        "equivalence_band_nats_per_action_token": [-EPS, EPS],
        "decision": "REVIEW_SAME_WORKFLOW_BRIDGE" if ready else
                    "INCOMPLETE" if missing else "REASSESS_MECHANISM_BEFORE_BRIDGE",
        "scope": "Finite authored cohort, base-stratified and template-cluster intervals. No security effect measured.",
    }, table


def load_results(out):
    out = Path(out)
    prepared = read(out / "prepared.json")
    if file_hash(out / "prepared.json") != read(out / "freeze.json")["prepared_sha256"]:
        raise ValueError("Prepared requests no longer match pre-outcome freeze")
    scores = {}
    for batch in sorted((out / "batches").glob("*.json")):
        for key, vector in read(batch).items():
            if key in scores or key not in prepared["requests"]:
                raise ValueError(f"Duplicate or unknown scored request {key}")
            if len(vector) != len(prepared["requests"][key]["cids"]) or not all(math.isfinite(x) for x in vector):
                raise ValueError(f"Invalid archived score vector {key}")
            scores[key] = vector
    return prepared, scores


def main():
    p = argparse.ArgumentParser()
    p.add_argument("run", type=Path)
    args = p.parse_args()
    run = args.run
    manifest = read(run / "design.json")
    model_outcomes = {}
    for out in sorted(run.glob("model_*")):
        if not (out / "freeze.json").is_file():
            continue
        prepared, scores = load_results(out)
        result, table = analyze(prepared, scores, manifest)
        write(out / "analysis.json", result)
        write(out / "cell_results.json", table)
        model_outcomes[prepared["label"]] = result["decision"]
        print(f"{prepared['label']}: {result['decision']} ({result['n_complete_cells']}/{result['n_scheduled_cells']} cells)")

    write(run / "research_decision.json", {
        "model_decisions": model_outcomes,
        "both_profiles_pass": set(model_outcomes) == {"gemma", "qwen"} and all(
            v == "REVIEW_SAME_WORKFLOW_BRIDGE" for v in model_outcomes.values()),
        "review_before_new_experiment": [
            "Compare signed role contrasts with the A14 anchor and original source/echo decomposition.",
            "Inspect field, template and layout reversals before interpreting pooled estimates.",
            "Retain protective original live results and separate the R3 read, fuzzy and retry evidence.",
            "Compare these scorer predictions with the frozen native bridge outcomes separately.",
            "Null, contradictory or incomplete results narrow or postpone the claim.",
        ],
    })


if __name__ == "__main__":
    main()
