# Parallel workflows on GPU3, lightweight accounting on shared GPU2

One detached job runs **Qwen3-32B, then Gemma-3-27B-IT** through one owned vLLM
server on physical **GPU3**. For each model, **two isolated workflow processes**
can send requests concurrently. Each workflow's actor/reference/tool steps stay
ordered. Shared **GPU2** performs a small read-only integer accounting audit;
it loads **no model weights and no vLLM**.

## Unzip and start a fresh run

```bash
cd /home/tahad/IEEE_SP/IEEE_SP_2027
unzip -o IEEE_SP_Parallel_Reference_GPU23_Preflight_Fixed.zip
source .venv/bin/activate
bash RUN_PARALLEL_REFERENCE_GPU23.sh
```

The launcher backgrounds the complete job with `nohup`, closed stdin, unique
PID/log/status/result paths and explicit `.venv/bin/python`. It uses the shared
`logs/gpu3_sequence.lock`. No manual step is needed between models. Watching
with `tail -f` and pressing Ctrl+C stops that viewer, not the detached job.
The new `reference_discovery_parallel/` module and launchers leave earlier
experiment modules and result directories intact.

This package fixes live email checkpoint restoration. Normal native Inbox
validation initializes a task from `initial_emails`; it must not be used to
reconstruct later sends and notices. Restored live inbox fields are individually
typed and the complete environment and checkpoint hashes must still match.
Inherited-effect accounting uses that authenticated restored world directly.
See `docs/Checkpoint_Restoration_Repair.md` for the reproduced failures,
regression coverage and build-host limitation. The qualification suite now has
57 tests. Failures print their test names and tracebacks in the main log.

The template preflight also supports Transformers 5.20.2's `BatchEncoding`
return type. JSON artifacts preserve token IDs, masks, the original wire fixture
and the conversation prepared by installed vLLM text-message preprocessing.
This follows vLLM's content-format detection instead of sending OpenAI content
blocks directly into a string-only tokenizer template. Native templates and
scientific generation requests remain unchanged. Preflight errors print in the
main log. See `docs/Template_Preflight_Repair.md` for tested scope and limits.

## Scientific allocation

| Panel | Each model | Both models |
|---|---:|---:|
| Core autonomous workflows |176|352|
| Ordinary execution/recovery workflows |72|144|
| Recipient/parameter boundary workflows |96|192|
| **Autonomous total** |**344**|**688**|
| Authentic matched recovery continuations |**Up to30**|**Up to60**|

Each profile has144 OFF,144 original source-guard,28 exact-capacity and28
source-plus-trusted-gate workflows. The original344 task specifications,
contracts, carriers, controls, fact realizations, frozen submission order and
30 declared recovery slots are retained exactly per model. There is no repeated
S1 inference panel and no outcome-dependent pruning or favorable redraw.

Phase order is CORE → authentic recovery → ordinary recovery → boundary.
The entire phase drains before the next starts. Within a phase, the next
scheduled job starts as soon as either worker becomes available. Completion
order can differ from submission order; both are recorded.

Recovery origins are chosen **after CORE drains, in the original frozen
workflow/proposal order**, independently for each model. The faster completion
or final success/failure of a parent cannot select the origin. Absent origins
remain `NO_ELIGIBLE_CHECKPOINT`, not manufactured calls or safe completions.
Available recovery arms run as separate isolated continuations; their internal
steps remain ordered and actual role-input equivalence is still certified.

## GPU3: the principal wall-clock improvement

Two persistent research worker processes, created with Python's `spawn`
method, share the one qualified vLLM endpoint. They do not share runtime state,
patches, signal timers, tool histories or output directories. No concurrent
threads run two source guard sessions inside one process.

The configured two-workflow maximum applies to all policies and both models.
Each workflow issues its dependent model requests sequentially. There is no
reduction in context/output limits, change in sampling parameters, quantization
or reuse of responses across independent cases. Model generations from different
workflows can now overlap and batch. Server settings remain BF16, TP1,32K
context,8K output cap and max-num-seqs4.

This is a declared **two-worker execution profile**. Batching, request order
and server random-number consumption can change outputs relative to serial
runs, even with unchanged sampling parameters. Bit-identical generations or a
twofold speedup are not promised. Queue-inclusive request times, worker PIDs,
actual scheduling and raw model I/O remain available for audit. Censoring and
technical failures stay explicit; overlapping cases are not independent samples
from a population.

An outage pauses new dispatch, drains both in-flight cases, then permits an
authenticated owned-server restart. Failed cases remain failed; only untouched
slots continue. A restart never deliberately interrupts another active case.
An interrupted worker gets a chance to preserve evidence; any forced cleanup
is limited to authenticated owned research PIDs and leaves partial cases unknown.

## GPU2: small, independent evidence cross-checks

GPU2 gets one low-priority helper in `.venv-serving`, with only GPU2's pinned
UUID visible. It reconstructs effects independently from native JSON, maps
operation signatures to integer IDs, and uses CUDA integer counts to check:

- Committed effects against permitted operation multiplicities.
- Missing authorized effects and exhausted permission.
- Native-state versus event-ledger agreement.
- Exact reference and released-call multiplicities at actual admissions.

Every CUDA result is cross-checked against a separate CPU counter. This helper
is read-only: it never approves/blocks calls, chooses origins, modifies primary
results or adds new experiment cases. Exact-support multiplicity alone is not
a causal explanation or proof of unauthorized effect.

The working tensors are small. The PyTorch caching allocator is capped at
approximately **256 MiB**, with a **1 GiB measured process soft budget** and
a requirement for at least **2 GiB free** on the shared device. CUDA driver/
context memory is outside the allocator cap, so this is **not a hard guarantee
of total memory usage**. Actual process memory is measured and saved. On memory
pressure, measurement failure, unsupported CUDA or an overage, the CUDA helper exits completely, releasing its CUDA context. At the next
model boundary or final drain, the controller starts a separate pure CPU helper
that checks all preserved cases. The reason is preserved;
GPU2 use is not falsely claimed if it fell back. Foreign processes are untouched.

This audit is a useful additional accounting check, not the main inference
speedup. Two concurrent workflows on GPU3 provide the principal throughput
opportunity. GPU2 loads no second copy of Qwen/Gemma.

## Other optimizations and interfaces

The native CPU suite runs once, with its package/runtime/Python receipt checked
by each model controller. Model-specific interfaces qualify separately. Token
diagnostics use one background worker per active workflow and fully drain before
that workflow closes. Raw model I/O is saved synchronously. One source snapshot
is shared. Gemma starts after Qwen's authenticated shutdown without waiting for
per-model analysis or compression.

Qwen retains its unmodified cached chat template and Hermes parser. Gemma uses
the packaged explicit Gemma-turn tagged-JSON template and strict non-streaming
parser. Both cached rendering paths qualify on CPU before serving. Each owned
server then gets two fixed live tool-generation/result-history probes: four
infrastructure requests total, separate from the scientific allocation.
No adaptive prompt repair is attempted.

All roles use the selected model family within a controller. Within-profile
treatment contrasts are primary. A difference between Qwen and Gemma does not
isolate model weights from their different interfaces. This is not a byte-faithful
replication of earlier Gemma JSON-interface experiments or serial execution.

## Environments, caches and runtime

Use the existing research `.venv` with AgentDojo0.1.35 and the pinned research
dependencies, and `.venv-serving` with vLLM0.26.0,torch2.11.0 and ninja. No
dependency installation, downloads, model substitutions or foreign-server
adoption occurs. Cached snapshots are pinned explicitly:

- Qwen: `9216db5781bf21249d130ec9da846c4624c16137`
- Gemma: `005ad3404e59d6023443cb575daa05336842228a`

Both are under `/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache`.
GPU3 UUID: `GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6`.
GPU2 UUID: `GPU-0b687901-110f-39c5-a5a9-dfe4b73cc932`.
The only model API is localhost:18080 on GPU3.

**No default global cutoff and no measured duration/speedup claim.** The old
single-model10–16-hour estimate is not a benchmark for this configuration.
Each case retains the20-minute,15-iteration and96-HTTP-attempt watchdogs.
Optional collection limits apply to the complete two-model job:

```bash
bash RUN_PARALLEL_REFERENCE_GPU23.sh --max-collection-hours 24
```

An optional stop preserves censored and unexecuted cases. It does not turn
them into safe results. Shutdown, audit draining and packaging follow collection.

## Artifacts

The main log shows both active cases, completion counts and the audit backend.
All requests/responses, diagnostic tokens, model reasoning returned by the API,
native states, effects, errors, source diffs/hashes, checkpoints, reference
certificates and missing/censored cases remain in their own directories.
Worker construction logs and authenticated process records are retained too.
Gemma additionally logs generated text before tagged-call parsing.

`analysis/` contains per-profile results, matched authored conditions, and
observed overlap/timing statistics. The overlap ratio is not a measured serial
counterfactual speedup. `gpu2_audit/` contains independent accounting records,
health measurements and any CPU-fallback transition. Autonomous roots and
conditional continuations retain separate ledgers; no prevalence estimate or
paper-ready verdict is generated.

After both servers and the helper stop, one complete lossless raw `.tar.gz`
and an all-case compact review bundle are written using gzip level1. All raw
files remain uncompressed too. Optional duplicate upload shards:

```bash
bash RUN_PARALLEL_REFERENCE_GPU23.sh --raw-parts
```

Or generate them later with no inference:

```bash
.venv/bin/python -m reference_discovery_parallel.uploads --create /ABSOLUTE/RAW_RUN_DIRECTORY
```

## Validation limits

Build checks run host-independent operational tests (including real spawned
CPU processes), syntax, frozen allocation equality, vendor hashes and ZIP
integrity. No model inference, GPU2 CUDA execution or GPU3 vLLM batching was
run here. On your machine, the native CPU suite additionally checks serial/
parallel mocked native effects, authenticated fork replay, and the independent
JSON accountant before scientific inference. The actual cached model/parser
and live server probes then qualify their installed integration.

The complete scientific design is in
`docs/IEEE_SP_Parallel_Reference_Experiment_Design.md`.
