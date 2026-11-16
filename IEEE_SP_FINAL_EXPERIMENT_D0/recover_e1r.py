"""Recover E1R guarded outcomes censored by the <TOOL_CALL> parser regression (D0 amendment).

In run 20261108T232225Z_3654860_31695 every guarded regeneration was recorded as
`regeneration_unparsed` because model.parse() accepted only JSON. The generated text of every
regeneration is stored in the row (`arms[arm].regen.raw.text`), and in E1R the regeneration is a
single write whose generation does not depend on the parser. Re-parsing that stored text with the
amended parser and dispatching the action in a fresh native sandbox, forked from the same verified
pre-action state, therefore yields exactly the outcome the amended runner would have recorded for
that generation. No model is called.

Every recovered row keeps the original fields and adds `recovery` provenance. The original run is
read-only. Output goes to recovered/<RUN_ID>/<profile>/E1R.jsonl with a new seal, and the package's
own analysis is then run on it.

Usage (CPU only):
  python3 recover_e1r.py --run ../IEEE_SP_FINAL_EXPERIMENT_GPU3_SHARED_PREFILL/runs/20261108T232225Z_3654860_31695 \
      --profile qwen --native-python /path/to/agentdojo-0.1.35/python
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time

from analysis import export_or_analyze
from design import compact, read, write
from experiment import Runtime, label
from model import parse
from run import AMENDMENT
from score import file_hash

ORIGINAL_SEAL_FIELDS = ("planned", "sha256")


def recover_row(rt, base, row, stats):
    cell, seed = row["cell"], row["seed"]
    key = f"{cell['id']}/{seed}/recovery"
    opened = rt.ask("open", key, base=base, cell=cell)
    try:
        if opened["digest"] != row["start_state"]:
            raise RuntimeError(f"Start state differs for {cell['id']}/{seed}")
        reads = [rt.dispatch(key, proposal) for proposal in (base["primary"], base["preview"])]
        if any(r["error"] for r in reads) or reads[-1]["after"] != row["pre_action"]:
            raise RuntimeError(f"Pre-action state differs for {cell['id']}/{seed}")
        out = deepcopy(row)
        changed = []
        for arm, result in out["arms"].items():
            if result.get("status") != "regeneration_unparsed":
                stats[(arm, "unchanged_" + str(result.get("status")))] += 1
                continue
            text = ((result.get("regen") or {}).get("raw") or {}).get("text")
            proposal = parse(text) if isinstance(text, str) else None
            if proposal is None:
                stats[(arm, "still_unparsed")] += 1
                continue
            result["regen"]["proposal"] = proposal
            if "final" in proposal:
                result.update(status="regeneration_final", outcome="no_write")
                stats[(arm, "regeneration_final")] += 1
            else:
                with rt.branch(key, key + "/" + arm, row["pre_action"]) as fork:
                    write_row = rt.dispatch(fork, proposal, enforce=arm == "force_enforce")
                result.update(status="dispatch_rejected" if write_row["error"] else "executed",
                              outcome=label(write_row), write=write_row)
                stats[(arm, result["outcome"])] += 1
            result["recovered"] = True
            changed.append(arm)
        out["recovery"] = {"amendment": AMENDMENT["id"], "recovered_arms": sorted(changed),
                           "method": "re-parse stored regeneration text; dispatch in fresh native fork"}
        return out
    finally:
        rt.ask("close", key)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--run", required=True, type=lambda s: Path(s).resolve())
    p.add_argument("--profile", default="qwen", choices=("qwen", "gemma"))
    p.add_argument("--native-python", required=True)
    p.add_argument("--out", type=lambda s: Path(s).resolve(), default=None)
    p.add_argument("--limit", type=int, default=None,
                   help="Engineering smoke test only: recover the first N rows (requires --out; no analysis)")
    args = p.parse_args()
    if args.limit is not None and args.out is None:
        p.error("--limit requires an explicit --out so a partial file is never mistaken for the recovery")

    source = args.run / args.profile / "E1R.jsonl"
    seal = read(args.run / args.profile / "E1R.seal.json")
    if file_hash(source) != seal["sha256"]:
        raise SystemExit("Original E1R does not match its seal; refusing to recover")
    plan = read(args.run / "plan.json")
    bases = {b["id"]: b for b in plan["bases"]}
    out_root = args.out or Path(__file__).resolve().parent / "recovered" / args.run.name
    out_dir = out_root / args.profile
    if (out_dir / "E1R.jsonl").exists():
        raise SystemExit(f"{out_dir}/E1R.jsonl exists; use a fresh --out")
    out_dir.mkdir(parents=True)
    for name in ("plan.json", "run_binding.json", "source_SHA256SUMS"):
        if (args.run / name).exists():
            shutil.copyfile(args.run / name, out_root / name)

    stats, started, n = Counter(), time.monotonic(), 0
    target = out_dir / "E1R.jsonl"
    with Runtime(os.path.abspath(args.native_python), out_dir / "native_recovery.log") as rt, \
            source.open() as f, target.open("x") as g:
        for line in f:
            if args.limit is not None and n >= args.limit:
                break
            row = json.loads(line)
            if row["status"] != "complete":
                g.write(compact(row) + "\n")
                stats[("row", row["status"])] += 1
                continue
            g.write(compact(recover_row(rt, bases[row["base"]], row, stats)) + "\n")
            n += 1
            if n % 256 == 0:
                print(f"recovered {n} rows, {time.monotonic() - started:.0f}s", flush=True)
    write(out_dir / "E1R.seal.json", {
        "planned": seal["planned"], "sha256": file_hash(target), "recovered_from": {
            "path": str(source), "sha256": seal["sha256"]},
        "amendment": AMENDMENT, "recovery_counts": {f"{a}|{b}": v for (a, b), v in sorted(stats.items())},
        "recovery_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": time.monotonic() - started})
    if args.limit is not None:
        print(json.dumps({"smoke_rows": n, "counts": {f"{a}|{b}": v for (a, b), v in sorted(stats.items())}}, indent=1))
        return {"smoke": True}
    report = export_or_analyze(out_root, plan)
    print(json.dumps({"recovered_rows": n, "counts": {f"{a}|{b}": v for (a, b), v in sorted(stats.items())},
                      "analysis": str(out_root / "provisional_analysis.json")}, indent=1))
    return report


if __name__ == "__main__":
    sys.exit(0 if main() is not None else 1)
