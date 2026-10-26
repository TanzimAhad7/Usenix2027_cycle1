# IEEE S&P targeted experiment

Put this ZIP in `/home/tahad/IEEE_SP/IEEE_SP_2027` and extract it there. This is the implemented v6.4 development experiment, with a complete local copy of the narrowly required runtime helpers. It does not overwrite your old `expanded_gpu3`, historical results, vendor tree, project setup or existing plan. The full scientific authority is included at `targeted_gpu3/RESEARCH_PLAN.md`.

## Start

```bash
cd /home/tahad/IEEE_SP/IEEE_SP_2027
unzip -o IEEE_SP_V6_4_Experiment.zip
bash START_TARGETED_GPU3.sh
```

The launcher itself uses **nohup** and prints the PID, `.log`, `.status`, and results directory immediately. `tail -f` the printed log. Ctrl+C while viewing that log stops the viewer, not the job. To intentionally stop the experiment, signal the printed controller PID with `kill -TERM PID`; partial artifacts are saved and owned servers are cleaned up. Do not start a duplicate run while another owns `logs/gpu3_sequence.lock`.

It uses the existing `.venv` for research and `.venv-serving` for vLLM. It installs nothing. Physical **GPU 3 only** is admitted, with UUID `GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6`. Another user's GPU process or an occupied port causes a recorded stop; it is never killed or reused. The controller loads Qwen, completes its eligible stages, stops its owned server/workers, then loads Gemma on the same device and port 18080. It stops Gemma and produces an upload archive. The Qwen/Gemma model family changes all four roles together.

The exact cached revisions are:

| Model | Revision |
|---|---|
| Qwen/Qwen3-32B | `9216db5781bf21249d130ec9da846c4624c16137` |
| google/gemma-3-27b-it | `005ad3404e59d6023443cb575daa05336842228a` |

Default weight cache: `/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache`. Only model/tokenizer/template files are read there; no research code, results or environment from that project is needed. Missing `refs/main` is harmless because revisions are explicit. Both snapshots are checked before loading either model. To relocate the same immutable weights, set `IEEE_SP_MODEL_CACHE` before launching. No automatic download, revision substitution, model change or dependency reinstall occurs.

## What the default run does

1. Verify retained source/runtime bytes and execute the new CPU effect controls, with actual AgentDojo 0.1.35 runtime objects and no model calls.
2. Run the frozen **12 configuration episodes**: Qwen native transport and Gemma JSON transport; clean one-payment, hostile duplicate and genuine two-payment tasks; S0 versus the exact upstream trusted scheduling suffix S1. Seed 29001, temperature zero, 32 attempted generations per episode.
3. Preserve every natural pre-reference checkpoint, including the actual world/effect/idempotency state, pending calls, actor/shadow histories, synchronization index, review/skip state, last attenuation fields, source settings and occurrence IDs.
4. Continue to reference probes only when the lawful controls and the relevant S1 failure/structure qualify. Verify passive instrumentation against unhooked source, and complete checkpoint restoration against the unpaused run, using exact captured requests/responses with **zero new inference**. If parity fails, record an engineering error and skip those probes.
5. Run only qualified reference rows: Qwen original versus neutral observation; Gemma observation × inherited-explanation ablation, sham, and two factual-state corners; five fixed seeds. The required person/account facts must already be present in the actual attenuated lookup view; otherwise neutralization would also restore missing facts, so that checkpoint is unqualified. The inherited-plan eligibility screen is predeclared and lexical; its exact assistant texts and selection rule are saved for human semantic review. It does not certify a history mechanism. Apply original admission, identified canonical capacity and remaining-grant control to the same reference outcomes. No extra judge calls are made to invent missing fuzzy edges; those capacity results remain UNKNOWN.
6. Stop the owned server before the next model, save descriptive CSV/JSON findings, checksums, status and `.tar.gz` evidence.

The immediate maximum is **384 qualification + 45 reference + at most 55 judge = 484 attempted generation requests**. Actual use can be much lower. Health/tokenization requests are logged separately. There are no hidden retries. Stopping, parse/transport failures, no reachability, failed lawful controls and unqualified checkpoints are recorded; rows are not replaced until a failure appears. This is development, not confirmation or an attack-prevalence estimate. Model startup is additional time; the request cap is not a duration promise.

The CPU controls exercise original tool execution, the explicit grant gate and the capacity comparator. A scripted compatible-edge fixture deliberately exposes capacity rejecting part of a legal 4+6 realization with only one reference occurrence. That expected boundary is preserved as a result, not treated as evidence that every repair preserves usefulness. Genuine two-use and actual same-key retry controls also execute. Whole-workflow recovery after a rejected installment is unmeasured by that forced batch fixture.

## Optional matched exhaustion diagnostic

The code for Section 7.5 is included, but is **not selected by the default command**. Select it only when the observed data leave the matched exhaustion/role question consequential:

```bash
bash START_TARGETED_GPU3.sh --exhaustion
```

Select that option before an initial campaign only when the additional question is already justified. Its ceiling is **244 additional attempts** (120 actor/reference probes + at most 60 judge + at most 64 clean-prefix requests), hence at most **728** across both complete selected modules. A failed configuration blocks the corresponding optional module. The decision is recorded before inference, never selected automatically from favorable probe outcomes.

If you have already completed the default campaign and subsequently select the exhaustion question, reuse its qualified configurations without repeating the 12 episodes or 45 reference rows:

```bash
bash START_TARGETED_GPU3.sh --exhaustion-from results/user_runs/targeted_gpu3_<completed_run_id>
```

This new run performs only the ≤244-request diagnostic, with a source/model/qualification check against the completed directory and explicit reused-evidence provenance. It still starts and stops both servers serially on GPU 3. A source mismatch or unqualified original configuration stops before inference. Reused episodes are never counted as new evidence. Do not launch either option concurrently with another controller.

The module uses one common root and hostile payload across available, initially consumed and naturally consumed states. U/I are real controlled runtime fixtures with seeded preparatory calls, not autonomous lookup demonstrations. N requires an actual clean one-commit actor prefix. Every context gets the same factual-state schema without gold permission labels. Actor responses are proposal-only probes; reference effects are forced batch components. Changed carrier views are oracle conditional interventions, not an unmodified attenuation result or a natural source-removed exploit. The initial-versus-natural history contrast remains a **history/initialization bundle**, not a pure transition or mental-memory effect. Unqualified N contexts remain unexecuted.

## Raw data and upload

The final printed archive is:

```text
results/user_runs/targeted_gpu3_<UTC timestamp>_<PID>.tar.gz
```

Upload that archive. It includes:

- Frozen schedule/contracts, settings, exact revisions, templates, code snapshot and generated source diffs.
- All actual request/response bodies, endpoint tokenization or explicit unavailability, HTTP headers/errors/timing, usage and model identities, across actor/reference/attenuator/judge roles.
- Native event logs, call/review/release/dispatch/effect/receipt joins, full message histories, actual errors, ledger and idempotency state.
- All checkpoints, hashes, exact-replay parity records, source/explanation edit maps and factual-state views.
- Same-reference source/capacity/grant comparisons, UNKNOWN compatibility, protected cases and explicit missing/unexecuted rows.
- CPU assurance records separately labeled from model episodes; server ownership, GPU qualification/telemetry, shutdown, controller logs, findings and manifests.

Neither a later successful completion nor an error receipt erases an earlier forbidden commit. A later occurrence is not intrinsically forbidden if its earlier sibling was blocked: `focal_released`, `Y_excess_release`, and `V_forbidden_component_commit` are separate records. V in reference probes is a qualified forced-batch consequence; it is not counted as another autonomous attack. Human semantic review remains pending.

## Offline analysis and local verification

No GPU or running server is needed to analyze a completed directory:

```bash
bash ANALYZE_TARGETED_GPU3.sh results/user_runs/targeted_gpu3_<your_run_id>
```

That command also uses nohup, writes a named log, and puts derived analysis under `results/analysis/`. It checks the file manifest, independently reconstructs actual qualification effects and violations, retains actor proposal profiles/invalid calls/error histories, and emits raw HTTP, response-class and trajectory-class ledgers. It never edits the raw run. Inspect these open response/trajectory classes alongside the mechanism tables; class counts are not independent samples or causal findings.

The package's engineering tests use a local mock HTTP service, the real pinned CPU runtime and mocked GPU/vLLM orchestration. They do **not** load Qwen/Gemma or establish H100 inference:

```bash
.venv/bin/python -m unittest targeted_gpu3.tests.test_experiment -v
```

Use them after a relevant code change; the default scientific launcher runs the scoped CPU controls, not repeated mock campaigns. The full-controller test skips rather than interfere if localhost port 18080 is already occupied. Included validation describes the checks actually executed while building this package. Native stock-email integration and fresh structural confirmation are subsequent experiments, not hidden parts of this launcher.

## Source and interpretation limits

Selected unchanged helpers are retained under `targeted_gpu3/retained/`: the project's world, transport, guard generation, source protocol and process/cache helpers; diagnostic/runtime verification; the supplied guard; GPU qualification; and the original scheduling loader as inspected source. `RETAINED_MANIFEST.json` records exact bytes and origin. These are project-local dependencies, not an unavailable archive or another research repository. Upstream material retains its original attribution and distribution terms; no new license is asserted for it.

Receipt identity repairs are common infrastructure; source admission/parsing semantics remain the recorded baseline for qualification. Checkpoint hooks and their diffs are explicit. Complete restore/parity is an engineering property with a captured-response tape, not a guarantee that a repeated seeded zero-temperature model request will return the same answer. Oracle state/neutralization and explicit contract gates are diagnostic controls, not new deployable defenses. All payments and fault injections are simulated in memory. Hashes establish byte integrity, not independent honesty of the simulator or a formal guarantee.
