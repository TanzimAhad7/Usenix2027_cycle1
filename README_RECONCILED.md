# Reconciled IEEE S&P experiment — complete automated campaign

This package implements the current reconciled design. It includes the exact archived checkpoints, original initial reference/judge records, task roots, schemas, two frozen runtime versions, the published guard source, new intervention code, independent effect analysis, and a CPU test suite. It does not need the rejected-paper repository or another project's Python code. The specified model-weight cache is reused as requested.

## Install into your IEEE S&P directory

Put the ZIP in `/home/tahad/IEEE_SP/IEEE_SP_2027`, then run:

```bash
cd /home/tahad/IEEE_SP/IEEE_SP_2027
unzip -o IEEE_SP_Reconciled_Experiment_GPU3_Full.zip
bash RUN_RECONCILED_GPU3.sh
```

That last command starts the entire detached run. It prints the PID, `.log`, final `.status`, results directory and exact `tail -f` command. It does not require manually restarting between stages or models. Every invocation creates a new run from the frozen inputs; existing result directories are preserved.

The launcher uses `.venv` for research and `.venv-serving` for vLLM. It creates a missing research environment using Python 3.12 and the included research lock. It can bootstrap a missing serving environment. Existing working venvs are used; serving must be the previously qualified `vllm==0.26.0` with Ninja. To explicitly create/repair both environments under nohup before inference:

```bash
mkdir -p logs
setup_log="logs/reconciled_setup_$(date -u +%Y%m%dT%H%M%SZ)_$$.log"
nohup bash SETUP_RECONCILED.sh --all > "$setup_log" 2>&1 < /dev/null &
echo "PID: $!  Log: $setup_log"
```

## What runs automatically

| Stage | Allocation | Evidence type |
|---|---:|---|
| E0 | 22 CPU tests; eight profile fixture pairs | Engineering/source-path qualification |
| Published transport probes | At most 64 fresh requests campaign-wide | Fixed candidates, not autonomous episodes |
| E1 | 24 conditions | Fixed serialization/admission decisions |
| E2 | 20 continuations | Original initial evidence held fixed; fresh subsequent decisions |
| E2-G | 4 continuations | Trusted precommit ledger comparator |
| E2-R | Up to 12 reserved continuations | Admission-triggered repeats; no final-outcome selection |
| E3 | 12 continuations | Real guard/service interruptions; full input certificates |
| E4a | 16 workflows | Persistent policies from natural task roots |
| E4a-OFF | 4 workflows | Natural guard-OFF baselines |
| E4b | 40 workflows | Original O96 email roots and declared profile variations |
| E5 | 24 workflows | New neutral-carrier task structures |

There are **120 mandatory workflows/continuations + 24 fixed conditions**, plus **up to 12 triggered repeats**. Qualification is separate. All 156 reserved IDs are frozen before inference. Valid negative results do not cancel later mandatory slots. Invalid dependencies, errors, missing exposures and censored slots remain visible. There is no outcome-based retry or replacement search.

The sequence runs Qwen3-32B on physical **GPU 3**, stops only its owned server/workers, then runs Gemma-3-27B-it on the same GPU and port **18080**, stops it, analyzes the evidence and makes a single final upload archive. It never selects GPU 0, 1 or 2, and never reuses or kills another user's server. A concurrent run lock or an occupied GPU/port is recorded as blocked infrastructure.

Model snapshots are exact:

- Qwen: `9216db5781bf21249d130ec9da846c4624c16137`
- Gemma: `005ad3404e59d6023443cb575daa05336842228a`
- Cache: `/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache`
- GPU UUID: `GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6`

Both snapshots are checked before either model loads. No `refs/main` is required and no alternate revision is selected. Actor, reference and auxiliary roles use the active model pipeline; cross-model role isolation is not claimed.

## Progress and deliverables

Use the printed `tail -f` command. Ctrl+C stops following the log; the detached experiment continues. The log prints a heartbeat every 15 seconds during work, model startup notices, active slot, role/request attempts and completed-slot counts.

Within the printed result directory:

- `status.json`, `progress.jsonl`, `frozen_protocol.json`, `fresh_request_budget.json`.
- `qwen/serving/` and `gemma/serving/`: server logs, commands, pinned snapshot metadata, placement/ownership and shutdown records.
- `<model>/slots/<id>/`: raw role HTTP requests/responses, transport errors, tokenization, native events, proposed calls, guard decisions, allocations, world states, messages, generated guard source/diff, outcomes and lifecycle status.
- `<model>/shared_initial/`: original-versus-new evidence lineage; reused initial responses are never counted as fresh generations.
- `<model>/repeat_selection/`: the predeclared trigger and selected contrast or explicit nonactivation.
- `<model>/E3_INPUT_EQUIVALENCE.json`: native feedback differences, all captured model-role inputs/routes and the first divergence.
- `cpu_qualification/` and `<model>/published_transport_probes/`: separate source/path and interface evidence; no claim of a full published benchmark reproduction.
- `analysis/`: independent workflow predicates, reviewed batches, primitive events, admission events, all fresh request metadata/token counts, planned-versus-actual census, JSON/CSV exports and a human-review queue.
- `source/`, `docs/`, environment records and `SHA256SUMS`.

At completion or a handled failure, the controller prints:

```text
UPLOAD ARCHIVE: .../results/user_runs/reconciled_gpu3_<unique-id>.tar.gz
```

Upload that `.tar.gz` for the next audit. A sibling `.sha256` records its checksum. Raw directories remain even after archive creation. No scientific conclusion is fabricated from a successful run: semantic review remains pending.

## CPU-only and mock validation

These optional modes also launch detached and produce logs/status/archive:

```bash
bash RUN_RECONCILED_GPU3.sh --cpu-only
bash RUN_RECONCILED_GPU3.sh --mock
```

CPU mode exercises real AgentDojo runtime effects and controlled tapes without inference. Mock mode exercises the entire campaign's scheduling, task execution, conditional repeats, certificates, exports and archive with scripted model responses. It labels every workflow non-scientific and uses no GPU. Its task-success labels must not be reported as model findings.

`validation/VALIDATION_REPORT.md` records what was actually tested during package creation. Real vLLM startup, H100 placement and live model behavior still require your machine. No fixed runtime-duration promise is made; the declared request ceiling is 8,720, with actual tokens and timing preserved.

## Fidelity and interpretation

`legacy_a/` and `legacy_o/` are immutable inputs from the authorization and O96 campaigns. E4b keeps O96's source routing and archived first-request schemas instead of silently imposing the newer continuity policy. Profile differences are labeled. Published-profile probes request/propagate judge log probabilities separately; this does not change archival O96 judge behavior.

Default-key normalization applies only to the certified omitted-versus-empty case. Registered nonempty keys and null are not normalized into independent operations. The ledger checks actual committed state immediately before dispatch in a synchronous simulator; it is an ordinary privileged comparator, not a new crash-durable authorization system. Native emails and independently charged payments here are benchmark/simulated effects, not external mail or money.

See `IMPLEMENTATION_NOTES.md` for the exact mapping of design to code, limits and qualification scope.
