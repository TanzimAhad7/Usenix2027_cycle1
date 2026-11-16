"""D0 pilot gate: parse census per stage, arm and family for one run/profile.

PASS requires, for every stage present:
  - unparsed regenerations <= 1% in every guarded arm, and
  - in E2L, at least one parsed first write in every family, and first_unparsed <= 1% overall.
This is an operational interface check, not a scientific endpoint.

Usage: python3 pilot_check.py runs/RUN_ID qwen
"""
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys

UNPARSED = {"regeneration_unparsed", "first_unparsed"}


def census(path):
    arms, families, rows = defaultdict(Counter), defaultdict(Counter), 0
    with path.open() as f:
        for line in f:
            r = json.loads(line)
            rows += 1
            families[r["family"]]["rows"] += 1
            families[r["family"]]["first_parsed"] += r.get("first") is not None
            families[r["family"]]["first_unparsed"] += r.get("status") == "first_unparsed"
            for arm, a in r.get("arms", {}).items():
                arms[arm][a.get("status")] += 1
    return rows, arms, families


def main(run, profile):
    out, ok = {}, True
    for stage in ("E1R", "E2L"):
        path = Path(run) / profile / f"{stage}.jsonl"
        if not path.exists():
            continue
        rows, arms, families = census(path)
        report = {"rows": rows, "arms": {}, "families": {k: dict(v) for k, v in families.items()}}
        for arm, c in sorted(arms.items()):
            attempted = sum(v for k, v in c.items() if k not in ("ineligible_placebo", "no_primary"))
            bad = sum(c[k] for k in UNPARSED)
            rate = bad / attempted if attempted else 0.0
            report["arms"][arm] = {"statuses": dict(c), "unparsed_rate": round(rate, 4)}
            if arm != "bypass" and rate > 0.01:
                ok = False
        if stage == "E2L":
            first_unparsed = sum(v["first_unparsed"] for v in families.values())
            if first_unparsed > 0.01 * rows or any(v["first_parsed"] == 0 for v in families.values()):
                ok = False
        out[stage] = report
    if not out:
        raise SystemExit("No E1R/E2L rows found for " + str(Path(run) / profile))
    out["verdict"] = "PASS" if ok else "FAIL"
    print(json.dumps(out, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    sys.exit(main(*sys.argv[1:]))
