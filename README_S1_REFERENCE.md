# Run the complete S1 reference/admission experiment

This package runs the focal study described in `docs/IEEE_SP_S1_Reference_Admission_Experiment_Design.md`: CPU qualification, 32 fresh reference blocks, 48 conditional admission comparisons, native simulated Slack effects, an established stateful comparator, analysis, and an evidence archive. It uses the original retained release constructors, serializers, attenuation, survival and dispatch methods. It holds the archived actor proposal fixed; it does not run 48 autonomous attacks.

## Install into your existing IEEE S&P directory

Put `IEEE_SP_S1_Reference_GPU3_Complete.zip` in `/home/tahad/IEEE_SP/IEEE_SP_2027`, then run:

```bash
cd /home/tahad/IEEE_SP/IEEE_SP_2027
unzip IEEE_SP_S1_Reference_GPU3_Complete.zip
bash RUN_S1_REFERENCE_GPU3.sh
```

The ZIP has files at its root and adds a uniquely named `s1_reference_study` package. It does not include or replace your environments, old results, authority document, or previous experiment code. Unzip asks before overwriting a same-named file if you already extracted this package. Start with a fresh package extraction rather than combining modified source files.

The launcher always starts a nohup worker with a unique `.log`, `.log.pid`, `.status`, and results directory. It explicitly invokes `.venv/bin/python`, whether or not your shell has activated the environment. Keep using your existing `.venv` and `.venv-serving`. No installation or model download happens automatically.

The launcher prints the exact progress command, for example `tail -f '/home/tahad/IEEE_SP/IEEE_SP_2027/logs/s1_reference_gpu3_....log'`. Ctrl+C stops tailing, not the nohup worker.

The worker verifies physical GPU 3 and its pinned UUID, obtains the shared `logs/gpu3_sequence.lock`, starts its own Qwen3-32B vLLM server on loopback port 18080, runs the complete eligible focal schedule, stops its owned server, and archives results. Existing GPU processes and occupied endpoints are never reused or killed. This experiment is Qwen only; Gemma and historical bridge trials are not automatic follow-ups.

## Expected inputs

- Existing `.venv` with AgentDojo 0.1.35 and the research dependencies. Native source hashes and qualification tests must pass before serving starts.
- Existing `.venv-serving` with the working vLLM 0.26.0 / torch 2.11.0 installation and `ninja`.
- The cached Qwen3-32B snapshot already selected for the project:
  `/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache/models--Qwen--Qwen3-32B/snapshots/9216db5781bf21249d130ec9da846c4624c16137`.
- Free physical GPU 3, UUID `GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6`, and free port 18080.

The small origin subset and relevant original release files are bundled. This code does not import another project directory or require you to copy the full old run archive. The model-cache path supplies weights only. `requirements-s1-tested.lock.txt` records the local qualification environment; it is not installed on your server by the launcher.

## What the run measures

The actual exposed two-send S1 proposal is tested under an exactly-one-send task and an explicit two-send control. The single-send and duplicate candidates under the one-send task share a reference. Reference-only hostile/neutral carrier inputs cross actual attenuation and unchanged-input generation, with four fresh realizations each.

An authentic native read prefix is reconstructed from retained records. Reference generation executes the unmodified source query until just before admission. Admission evaluations rerun the same unmodified query, replaying the exact recorded attenuation/reference queries and outputs. Every replay input must be equal. The source is paused immediately before dispatch, then its original dispatch helper executes released calls in a fresh native state. Live judge calls occur only when the source invokes them. There is no actor regeneration or final reporting continuation.

The unchanged-input branch is a declared diagnostic intervention. The source `_attenuate_observation` instance method is wrapped to return its input only in that branch; original vendor files remain byte-identical. In the attenuated branch, the wrapper invokes the source method unchanged and logs the input/output. Python tracing pauses execution at verified source lines; it does not rewrite the admission logic.

SDK transport retries are disabled. The source request function's Tenacity decorator is bypassed by calling its original `__wrapped__` body; the successful request construction remains unchanged. A failed transport is retained without a replacement scientific draw. The source's explicit unsupported-logprobs fallback is preserved and logged. Empty references, refusals, malformed outputs, tool errors, and truncations remain in the evidence. Truncated source decisions may still be executed and recorded, but they are excluded from qualified claims.

The amended two-send task retains earlier assistant reasoning originally generated under the one-send task. That output is not a trusted instruction, but it can influence the lawful control. The report preserves this limitation. References never receive the pending duplicate assistant message; they retain the earlier source history exactly except for the declared interventions.

## Outputs

The worker prints an upload archive path ending in `.tar.gz`. Keep that archive and its `.sha256` file. Inside are:

- `FROZEN_MANIFEST.json`, `census.json`, `status.json`, and `execution_environment.json`.
- `cpu_qualification/`: source hashes, archive-subset proof, native replay, test log and retained fixtures.
- `references/<block>/`: input/intervention diff, full shadow context, transformed observations, original raw role requests/responses, HTTP bodies and reference calls.
- `admissions/<trial>/`: shared-input equality checks, per-occurrence matching routes, native pre/post worlds, tool errors, independent effect observation and stateful comparator.
- `serving/`: exact command, snapshot/template identity, versions, ownership/placement, vLLM log and shutdown record (live runs only).
- `SUMMARY.json`, `FINDINGS.md`, `CONTRASTS.json`, `admission_ledger.json`, `admissions.csv`, `conditions.csv`, and `RESULTS_VERIFICATION.json`.
- Source/input snapshot and `SHA256SUMS`.

All 32 reference blocks and 48 comparisons receive terminal census entries, including technical failure and dependency failure. An interruption archives partial evidence. It does not erase the run or silently resume with changed random draws. Historical and autonomous follow-ups require their own predeclared decision.

The final machine memo is a trace-review aid; human review remains pending. It cannot certify a mechanistic claim or IEEE S&P novelty automatically. Findings from `--mock` are marked engineering-only and zero model inference.

## Optional engineering checks

These are optional; the full launcher already runs CPU qualification before model startup.

```bash
bash RUN_S1_REFERENCE_GPU3.sh --cpu-only
```

For the complete 32/48 schedule with scripted HTTP responses and no model/GPU:

```bash
bash RUN_S1_REFERENCE_GPU3.sh --mock
```

Do not run either concurrently with a scientific sequence: they use the same lock. Unit fixtures use actual native tools and retained source, with OpenAI-compatible mocked HTTP responses. They provide engineering verification only.

Runtime is workload-dependent: there are 32 reference generations, normally two attenuation calls in each of the 16 transformed blocks, and any source-required fuzzy judge calls. The number of reference blocks is not the number of HTTP requests. No fixed completion time is promised.
