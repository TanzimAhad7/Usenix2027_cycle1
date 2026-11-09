"""Stage controller. GPU models run in separate children with disjoint runtime ownership."""
import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import time
import traceback

from analysis import adjudication, blind_case, blind_packet, export_or_analyze, jsonl, threshold_calibration
from bridge.batching import BatchEngine, DEFAULT_LANES, MAX_LANES, schedule
from design import DESIGN_SEED, MODELS, NUMERIC_TOLERANCE, PROTOCOL, ROOT, compact, digest, make_plan, read, write
from experiment import Runtime, decide, job, qualify
from model import Adapter, AdapterBlock, LocalBlock
from score import check_gpu, file_hash, gpu_uuid, load_model, require_idle_gpu, snapshot


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def status(out, phase, **details):
    row = {"at": timestamp(), "phase": phase, **details}
    write(out / "status.json", row)
    print(compact(row), flush=True)


class FixtureBlock:
    """Synthetic model for wiring tests. Its results are never scientific data."""
    def __init__(self, base, cell):
        self.base, self.cell = base, cell

    def actor(self, messages, seed):
        yield from ()
        primary = next((m for m in messages if m.get("primary")), None)
        if primary is None:
            proposal = self.base["primary"]
        elif "SANITIZED TEST" in primary["content"] and "Verified record field" not in primary["content"]:
            proposal = self.base["alternate"]
        else:
            proposal = self.base["good"]
        return {"raw": {"id": digest([messages, seed]), "text": compact(proposal)}, "proposal": proposal}

    def scoring(self, base, messages, proposal):
        yield from ()
        spans = []
        for i,m in enumerate(messages):
            if m["role"] != "tool" or m.get("error"):
                continue
            primary = bool(m.get("primary"))
            scalar = (0.3 if self.cell["edit"] == "hostile" else -0.2) if primary else -0.4
            spans.append({"index": i, "primary": primary, "scalar": scalar,
                          "parts": {"identifier": 0.4 if primary else 0, "parameter": 0,
                                    "other": scalar - 0.4 if primary else scalar},
                          "patched": {"remove_id": scalar - 0.4 if primary else scalar,
                                      "equal_placebo": scalar, "margin_placebo": None if primary else scalar}})
        return {"spans": spans, "flags": [s["index"] for s in spans if s["scalar"] > 0]}

    def clean(self, messages, flags, seed):
        yield from ()
        output = [dict(m) for m in messages]
        for i in flags:
            output[i]["content"] = "SANITIZED TEST"
        return {"messages": output, "receipts": [{"fixture": True}]}


def phase_attempts(plan, phase, engine):
    seeds = plan["seeds"][:1] if phase == "cal" or plan["smoke"] else plan["seeds"]
    cells = [cell for cell in plan["cells"] if cell["stage"] == phase]
    rng = random.Random(DESIGN_SEED)
    if phase == "replay" and engine == "local":
        # Put all stochastic draws of one fixed prefix in the same scheduler window.
        rng.shuffle(cells)
        return [(cell, seed) for cell in cells for seed in seeds]
    attempts = [(cell, seed) for cell in cells for seed in seeds]
    rng.shuffle(attempts)
    return attempts


def capture_phase(rt, plan, backend, out, phase, threshold, lanes, engine):
    path = out / ({"cal": "calibration", "replay": "E1R", "live": "E2L"}[phase] + ".jsonl")
    receipt = path.with_suffix(".seal.json")
    bases = {b["id"]: b for b in plan["bases"]}
    cells = phase_attempts(plan, phase, engine)
    if receipt.exists():
        saved = read(receipt)
        if saved["sha256"] != file_hash(path) or saved["planned"] != len(cells):
            raise RuntimeError(f"Stage seal disagrees with {path}")
        return saved
    if path.exists():
        raise RuntimeError(f"An unsealed phase already exists at {path}. Preserve it and use a new run directory.")
    backend_resolve = backend.resolve if backend else lambda requests: {} if not requests else None
    def make_job(pair, _lane):
        cell, seed = pair
        b = bases[cell["base"]]
        if engine == "local":
            make_block = lambda condition: LocalBlock(backend, condition)
        elif engine == "external":
            make_block = AdapterBlock
        else:
            make_block = lambda _condition: FixtureBlock(b, cell)
        return job(make_block, rt, b, cell, seed, threshold)

    status(out, phase, done=0, total=len(cells))
    counts, started = Counter(), time.monotonic()
    qualified = getattr(backend, "qualified_calibration", None) if phase == "cal" else None
    if qualified:
        acquired = {(row["cell"]["id"], row["seed"]) for row in qualified["rows"]}
        if len(qualified["rows"]) != len(cells) or acquired != {(cell["id"], seed) for cell, seed in cells}:
            raise RuntimeError("Qualification rows do not match the calibration plan")
    rows = iter(qualified["rows"]) if qualified else schedule(cells, make_job, backend_resolve, lanes)
    i = 0
    with path.open("x", encoding="utf-8", buffering=1) as f:
        for i, row in enumerate(rows, 1):
            f.write(compact(row) + "\n")
            counts[row["status"]] += 1
            counts["exposed"] += row["exposed"]
            counts["first_proposal"] += row.get("first") is not None
            counts["scalar_trigger"] += bool(row.get("scores", {}).get("flags"))
            if i % 32 == 0 or i == len(cells):
                elapsed = time.monotonic() - started
                status(out, phase, done=i, total=len(cells), seconds_per_cell=round(elapsed/i, 3),
                       eta_seconds=round((len(cells)-i)*elapsed/i), backend=dict(backend.stats) if backend else {})
    if i != len(cells):
        raise RuntimeError("Scheduler failed to record every planned attempt")
    data = {"planned": len(cells), "sha256": file_hash(path), "counts": counts,
            "elapsed_seconds": time.monotonic() - started}
    if qualified:
        data["score_qualification_source"] = qualified["source"]
    write(receipt, data)
    return data


def execute_stages(args, plan, backend, out):
    with Runtime(args.native_python, out / ("native_" + args.stage + ".log")) as rt:
        if args.stage in ("replay", "all"):
            capture_phase(rt, plan, backend, out, "cal", 0, args.lanes, args.engine)
            calibration = threshold_calibration(jsonl(out / "calibration.jsonl"))
            write(out / "rate_calibration.json", calibration)
            capture_phase(rt, plan, backend, out, "replay", calibration["threshold"], args.lanes, args.engine)
        if args.stage in ("live", "all"):
            seal = read(out / "E1R.seal.json")
            if file_hash(out / "E1R.jsonl") != seal["sha256"]:
                raise RuntimeError("E1R rows do not match the frozen seal")
            # Opportunity gate only. Do not look at E1R material outcome labels.
            n = seal["planned"]
            if not seal["counts"].get("scalar_trigger") or seal["counts"].get("technical_error", 0) > 0.02 * n:
                status(out, "E2L_BLOCKED_BY_E1R_OPPORTUNITY_OR_TECHNICAL_GATE", seal=seal)
                return
            capture_phase(rt, plan, backend, out, "live", 0, args.lanes, args.engine)
    status(out, "STAGES_COMPLETE")


def score_qualification(serial, candidate):
    """Check the score observables, guard decisions, and paired rank readouts."""
    max_gap, disagreements = 0.0, Counter()
    names = ("scalar", "remove_id", "equal_placebo", "margin_placebo")
    reference_threshold = threshold_calibration(serial)["threshold"]
    candidate_threshold = threshold_calibration(candidate)["threshold"]

    def compare_numbers(left, right):
        nonlocal max_gap
        if (left is None) != (right is None):
            disagreements["eligibility"] += 1
        elif left is not None:
            max_gap = max(max_gap, abs(left - right))

    compare_numbers(reference_threshold, candidate_threshold)
    for reference, trial in zip(serial, candidate, strict=True):
        if reference["cell"]["id"] != trial["cell"]["id"] or trial["status"] != "calibration_only":
            disagreements["missing_or_failed_case"] += 1
            continue
        pair_values = []
        for key in ("scores", "alternate_scores"):
            a, b = reference[key], trial[key]
            if [(s["index"], s["primary"]) for s in a["spans"]] != [
                    (s["index"], s["primary"]) for s in b["spans"]]:
                disagreements["span_identity"] += 1
                continue
            for arm in (*names, "rate_threshold"):
                if decide(a, arm, reference_threshold) != decide(b, arm, candidate_threshold):
                    disagreements["route"] += 1
            maxima = []
            for arm in names:
                arm_values = [[s["scalar"] if arm == "scalar" else s["patched"][arm]
                               for s in result["spans"]] for result in (a, b)]
                maxima.append([max(values) if values and None not in values else None for values in arm_values])
            pair_values.append(maxima)
            for left, right in zip(a["spans"], b["spans"], strict=True):
                for metric in ("scalar", "delta_tool", "delta_user"):
                    compare_numbers(left[metric], right[metric])
                for metric in ("parts", "patched"):
                    for field in left[metric]:
                        compare_numbers(left[metric][field], right[metric][field])
                left_mask, right_mask = left["patch_tokens"], right["patch_tokens"]
                if left_mask and right_mask:
                    for arm in names[1:]:
                        if left_mask[arm] != right_mask[arm]:
                            disagreements["placebo_tokens"] += 1
        if len(pair_values) == 2:
            for (good_serial, good_batch), (bad_serial, bad_batch) in zip(*pair_values, strict=True):
                if None not in (good_serial, good_batch, bad_serial, bad_batch):
                    if (good_serial >= bad_serial) != (good_batch >= bad_batch):
                        disagreements["paired_rank"] += 1
    if not serial or not any(row["scores"]["spans"] for row in serial):
        disagreements["empty_probe"] += 1
    return {"cases": len(serial), "max_abs_derived_score_difference": max_gap,
            "tolerance": NUMERIC_TOLERANCE, "disagreements": dict(disagreements),
            "pass": max_gap <= NUMERIC_TOLERANCE and not disagreements}


def qualify_local_scores(args, plan, engine, out):
    # These calibration inputs are disjoint from both evaluation stages.
    cases = phase_attempts(plan, "cal", args.engine)
    bases = {base["id"]: base for base in plan["bases"]}
    probe_root = out / ("score_qualification_" + args.stage)
    probe_root.mkdir(exist_ok=True)
    rows, timings, stats = {}, {}, {}
    with Runtime(args.native_python, probe_root / "native.log") as rt:
        for mode in ("single", "batch"):
            directory = probe_root / mode
            directory.mkdir(exist_ok=True)
            probe = BatchEngine(engine.model, engine.tokenizer, engine.device, directory,
                                engine.label, engine.lanes, score_mode=mode)
            started = time.monotonic()
            try:
                def make_job(pair, _lane):
                    cell, seed = pair
                    return job(lambda condition: LocalBlock(probe, condition), rt, bases[cell["base"]], cell, seed)

                rows[mode] = list(schedule(cases, make_job, probe.resolve, engine.lanes))
                timings[mode] = time.monotonic() - started
                stats[mode] = dict(probe.stats)
                write(directory / "rows.json", rows[mode])
            finally:
                probe.close()
    if any(row["status"] != "calibration_only" for row in rows["single"]):
        raise RuntimeError("Reference scoring qualification failed. See " + str(probe_root))
    report = score_qualification(rows["single"], rows["batch"])
    raw = {mode: {row["id"]: row["logprobs"] for row in jsonl(probe_root / mode / "requests.jsonl")}
           for mode in rows}
    if raw["single"].keys() != raw["batch"].keys():
        report["disagreements"]["raw_request_identity"] = 1
        report["pass"] = False
    report["max_abs_raw_token_difference"] = max(
        (abs(a - b) for key in raw["single"].keys() & raw["batch"].keys()
         for a, b in zip(raw["single"][key], raw["batch"][key], strict=True)), default=None)
    report["timings_seconds"] = timings
    report["stats"] = stats
    report["max_batch_tested"] = stats["batch"].get("score_max_batch", 0)
    # Verify the same execution path is genuinely batched and saves work.
    report["selected"] = "batch" if (report["pass"] and report["max_batch_tested"] > 1
                                     and timings["batch"] < timings["single"]) else "single"
    return report, rows, probe_root


@contextmanager
def local_backend(args, plan, out):
    import torch
    import transformers

    if (sys.version_info[:2] != (3,12) or torch.__version__.split("+")[0] != "2.11.0"
            or transformers.__version__ != "5.20.2"):
        raise RuntimeError("Expected the prior pinned Python 3.12, Torch 2.11.0, Transformers 5.20.2 stack")
    uuid = os.environ["CUDA_VISIBLE_DEVICES"]
    check_gpu(3, uuid)
    identity = snapshot(args.cache, args.profile, args.gemma_revision)
    previous = out / "runtime_identity.json"
    record = {"model": identity, "physical_gpu": 3, "uuid": uuid, "torch": torch.__version__,
              "transformers": transformers.__version__, "decoder": {"top_k": 32, "temperature": 0.35},
              "lanes": args.lanes}
    saved = read(previous) if previous.exists() else None
    if saved and any(saved.get(key) != value for key, value in record.items()):
        raise RuntimeError("Local profile runtime identity changed between stages")
    status(out, "LOADING", model=identity["hub"], gpu=3)
    torch.manual_seed(DESIGN_SEED)
    torch.backends.cuda.matmul.allow_tf32 = False
    tok = transformers.AutoTokenizer.from_pretrained(identity["path"], local_files_only=True,
                                                      trust_remote_code=False, use_fast=True)
    if not tok.is_fast:
        raise RuntimeError("The frozen scorer needs tokenizer offset mappings")
    device = torch.device("cuda:0")
    model = load_model(identity, device)
    engine = BatchEngine(model, tok, device, out, args.profile, args.lanes)
    try:
        qualification = engine.qualify_generation()
        write(out / ("generation_probe_" + args.stage + ".json"), qualification)
        if not qualification["exact_match"]:
            raise RuntimeError("Local batch/single generation qualification differs")
        score_probe, probe_rows, probe_root = qualify_local_scores(args, plan, engine, out)
        write(out / ("score_probe_" + args.stage + ".json"), score_probe)
        engine.score_mode = saved["score_mode"] if saved else score_probe["selected"]
        if engine.score_mode == "batch" and not score_probe["pass"]:
            raise RuntimeError("Previously qualified score batching failed stage requalification")
        if args.stage in ("replay", "all"):
            selected = probe_root / engine.score_mode
            engine.qualified_calibration = {
                "rows": probe_rows[engine.score_mode],
                "source": {str(path.relative_to(out)): file_hash(path) for path in
                           (selected / "rows.json", selected / "requests.jsonl")},
            }
        write(previous, record | {"score_mode": engine.score_mode})
        status(out, "SCORE_QUALIFIED", score_mode=engine.score_mode,
               score_batch=score_probe["max_batch_tested"], checks=score_probe["disagreements"],
               max_abs_derived_score_difference=score_probe["max_abs_derived_score_difference"],
               timings_seconds=score_probe["timings_seconds"])
        yield engine
    finally:
        engine.close()


def worker(args, plan):
    out = args.out / args.profile
    out.mkdir(exist_ok=True)
    try:
        if args.engine == "local":
            with local_backend(args, plan, out) as backend:
                execute_stages(args, plan, backend, out)
        elif args.engine == "external":
            backend = Adapter(args.adapter, out)
            try:
                identity = {"adapter": backend.identity, "spec_sha256": file_hash(args.adapter)}
                f = out / "runtime_identity.json"
                if f.exists() and read(f) != identity:
                    raise RuntimeError("External comparator changed across stages")
                write(f, identity)
                execute_stages(args, plan, backend, out)
            finally:
                backend.close()
        else:
            execute_stages(args, plan, None, out)
    except BaseException:
        status(out, "FAILED")
        (out / "failure.txt").write_text(traceback.format_exc())
        raise


def qualify_stage(args, plan):
    p = args.out / "E0V.json"
    if not p.exists():
        with Runtime(args.native_python, args.out / "native_E0V.log") as rt:
            cases = qualify(rt, plan)
        write(p, {"status": "PASS_NATIVE_CAPABILITY_PROBES", "cases": cases})
    result = read(p)
    rows = []
    for case in result["cases"]:
        item = blind_case(case["contract"], case["receipt"], case.get("prior_count", 0))
        if item is not None:
            rows.append(item | {"expected": case["expected"]})
    packet = blind_packet(({k:v for k,v in row.items() if k != "expected"} for row in rows), PROTOCOL + "/E0V")
    write(args.out / "blind_E0V.json", packet)
    reviews, info = adjudication(packet, args.qualification_review)
    if reviews:
        disagreements = [r["id"] for r in rows if reviews[r["id"]] != r["expected"]]
        info |= {"disagrees_with_fixture": len(disagreements), "unmatched_cases": sorted(set(disagreements))}
    write(args.out / "E0V_review_receipt.json", info)
    return bool(reviews) and not info["disagrees_with_fixture"]


def freeze(args):
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    p = out / "plan.json"
    plan = make_plan(args.smoke)
    binding = {"protocol": PROTOCOL, "plan_sha256": digest(plan), "engine": args.engine,
               "profiles": args.profiles, "lanes": args.lanes, "source_sha256": file_hash(ROOT / "SHA256SUMS") if
               (ROOT / "SHA256SUMS").exists() else None, "adapter_sha256": file_hash(args.adapter) if args.adapter else None}
    if p.exists():
        if read(p) != plan and digest(read(p)) != digest(plan):
            raise RuntimeError("Plan changed on resume")
        frozen = read(out / "run_binding.json")
        if args.stage != "qualify" and frozen != binding:
            raise RuntimeError("Run binding changed on resume. Start a fresh run.")
    else:
        write(p, plan)
        write(out / "run_binding.json", binding)
        if (ROOT / "SHA256SUMS").exists():
            shutil.copyfile(ROOT / "SHA256SUMS", out / "source_SHA256SUMS")
    return plan


def run_controller(args):
    if args.stage == "analyze":
        plan = read(args.out / "plan.json")
        export_or_analyze(args.out, plan, args.outcome_review)
        if args.archive:
            archive(args.out, ".analyzed")
        return
    plan = freeze(args)
    try:
        status(args.out, "E0V_START", engine=args.engine)
        agreed = qualify_stage(args, plan)
        if args.stage == "qualify":
            status(args.out, "E0V_COMPLETE", independent_review=agreed)
            return
        if args.engine == "external" and not agreed:
            status(args.out, "BLOCKED_PENDING_E0V_BLIND_ADJUDICATION")
            return
        profiles = args.profiles if args.engine == "local" else [args.engine]
        for profile in profiles:
            env = os.environ.copy()
            env["CUDA_VISIBLE_DEVICES"] = ""
            if args.engine == "local":
                uuid = gpu_uuid(3)
                require_idle_gpu(3, uuid)
                env["CUDA_VISIBLE_DEVICES"] = uuid
            status(args.out, "PROFILE_START", profile=profile)
            cmd = [sys.executable, str(ROOT / "run.py"), *sys.argv[1:], "--profile", profile]
            subprocess.run(cmd, cwd=ROOT, env=env, check=True)
            profile_status = read(args.out / profile / "status.json")
            status(args.out, "PROFILE_EXIT", profile=profile, result=profile_status["phase"])
            if args.archive:
                archive(args.out, "." + profile)
        export_or_analyze(args.out, plan, args.outcome_review)
        live_completed = {p: (args.out / p / "E2L.seal.json").exists() for p in profiles}
        status(args.out, "RUN_COMPLETE", live_completed=live_completed,
               evidence_scope={"local": "local_reconstruction", "fixture": "synthetic_test",
                               "external": "externally_attested_comparator_pending_scientific_review"}[args.engine])
    except BaseException:
        status(args.out, "FAILED")
        (args.out / "failure.txt").write_text(traceback.format_exc())
        raise
    finally:
        if args.archive:
            archive(args.out)


def archive(out, suffix=""):
    target = out.parent / (out.name + suffix)
    temp = target.with_name(target.name + ".tmp")
    shutil.make_archive(str(temp), "zip", root_dir=out.parent, base_dir=out.name)
    temp.with_suffix(temp.suffix + ".zip").replace(target.with_name(target.name + ".zip"))
    print(f"ARCHIVE {target}.zip", flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", required=True, type=lambda s: Path(s).resolve())
    p.add_argument("--stage", choices=("qualify", "replay", "live", "all", "analyze"), default="qualify")
    p.add_argument("--engine", choices=("local", "external", "fixture"), default="local")
    p.add_argument("--profiles", nargs="+", choices=tuple(MODELS), default=list(MODELS))
    p.add_argument("--native-python")
    p.add_argument("--cache", default="/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache")
    p.add_argument("--gemma-revision")
    p.add_argument("--adapter", type=lambda s: Path(s).resolve())
    p.add_argument("--qualification-review", type=Path, action="append", default=[])
    p.add_argument("--outcome-review", type=Path, action="append", default=[])
    p.add_argument("--lanes", type=int, default=DEFAULT_LANES)
    p.add_argument("--archive", action="store_true")
    p.add_argument("--smoke", action="store_true")
    p.add_argument("--profile", help=argparse.SUPPRESS)
    args = p.parse_args()
    if not 1 <= args.lanes <= MAX_LANES or len(set(args.profiles)) != len(args.profiles):
        p.error("Invalid batch lane count or duplicate profile")
    if args.profiles != [x for x in MODELS if x in args.profiles]:
        p.error("Profile order is Qwen then Gemma")
    if args.engine == "fixture" and not args.smoke:
        p.error("The fixture engine is restricted to --smoke")
    if args.engine == "external" and not args.adapter and args.stage != "analyze":
        p.error("--engine external requires --adapter")
    if args.stage != "analyze":
        if not args.native_python:
            p.error("--native-python is required")
        args.native_python = os.path.abspath(args.native_python)
    if args.profile:
        worker(args, read(args.out / "plan.json"))
    else:
        run_controller(args)


if __name__ == "__main__":
    main()
