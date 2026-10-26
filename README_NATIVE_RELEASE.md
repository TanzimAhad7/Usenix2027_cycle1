# Native-release IEEE S&P experiment

This is the complete implementation of the current bounded experiment: **36 autonomous workflows**, followed automatically by **up to 12 authentic matched continuations**. The default launcher qualifies the code, starts Qwen, executes every independently valid scheduled cell, shuts down its owned server and archives the evidence. It does not stop after CPU tests or ask for another command between stages.

Only **physical GPU 3** is allowed. This panel uses **Qwen3-32B only**. A Gemma extension is outside its frozen 48-slot ceiling and is not started automatically.

## Install the package and run everything

Put `IEEE_SP_Native_Release_GPU3_Full.zip` in your existing project directory, then paste:

```bash
cd /home/tahad/IEEE_SP/IEEE_SP_2027
unzip -o IEEE_SP_Native_Release_GPU3_Full.zip
bash RUN_NATIVE_RELEASE_GPU3.sh
```

The launcher already uses `nohup`, closes stdin, prints its PID and unique `.log`, `.status` and result paths, and returns. Use the exact printed `tail -f` command to watch progress. Ctrl+C in `tail -f` stops the viewer, not the experiment.

Keep the working `.venv` and `.venv-serving`. Nothing is automatically installed, rebuilt or downloaded. The recorded Qwen snapshot is read directly from:

```text
/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache/models--Qwen--Qwen3-32B/snapshots/9216db5781bf21249d130ec9da846c4624c16137
```

The cache supplies weights only. All experiment code and selected author-release code are contained here; no USENIX or other project code checkout is imported. A relocated cache is supported through `--cache /absolute/cache/root`, while the model revision stays fixed.

## What runs

1. Check package and native runtime source identities; run the native CPU assurance, effective-driver request capture, inert-instrumentation and checkpoint tests.
2. Verify GPU 3's pinned UUID and free port/device. Start one owned vLLM server on `127.0.0.1:18080` using the explicit cached Qwen revision.
3. Run six authored native email/Slack roots, each with neutral/hostile carrier twins and OFF, RELEASE and RELEASE+G: **36 complete workflows**.
4. In fixed root order, choose at most one eligible checkpoint per root without consulting final harm. Authenticate restoration and replay the original decision only under identical requests. Run a guard/service pair with common factual feedback, or retain a specific missingness/failure reason. Maximum: **12 additional controlled continuations**.
5. Write per-root analysis, stop only the owned server process tree, and create the complete `.tar.gz` plus checksum.

No desired attack or successful task outcome is a qualification gate. An invalid instrument blocks dependent cells; a protected/negative scientific outcome does not. Full workflows, selected continuations, CPU fixtures, cached evidence and mocks have separate evidence labels.

## Actual selected driver

The package executes the retained release's `get_llm(provider='vllm_parsed')` actor and `_get_attriguard_aux_llms(backend='openai')` constructors against the same **local** Qwen endpoint. Runtime tool schemas and original auxiliary temperature **0.2** / top-p **0.9** are preserved. Actor defaults remain the source defaults. The source fuzzy/exact predicates, attenuation, skip routing and signature-based receipt association remain unchanged in RELEASE.

There is no client-side JSON action envelope, hidden schema omission, default-key normalization, capacity patch, temperature-zero auxiliary override or thinking override. The source original feedback bug is deliberately retained and tested. The server requests its snapshot chat template, native Hermes tool parsing and an 8,192-token default output cap; actual CLI and server metadata are saved. The run has 15 source iterations, at most 96 generation HTTP attempts per workflow/continuation and a 1,200-second per-entry watchdog. SDK and source retries count against that cap. It is a bounded supported-driver local profile, **not** the paper's principal commercial-model reproduction or official benchmark population.

## Raw evidence and status

The printed result directory contains:

```text
FROZEN_MANIFEST.json          all 48 scheduled identities and limits
SOURCE_RUNTIME_IDENTITY.json original release/runtime hashes
census.json                  every recorded/unexecuted slot and reason
status.json                  current controller stage and active slot
cpu_qualification/           executed tests, fixtures and payload certificates
serving/                     model/cache/template, command, logs, ownership, shutdown
autonomous/<slot>/           full SDK/HTTP, native state, effects, messages and errors
parent_selection/            outcome-independent eligibility decisions
restoration_qualification/   exact-request replay and unchanged-state verdicts
conditional/<slot>/          fresh continuation plus explicitly reused decisions
input_equivalence/           actual first HTTP-body and later-input comparisons
analysis/                    per-root findings, JSON summary and CSV ledger
source/                      exact executed code snapshot
SHA256SUMS                   hashes of all archived files
```

Every episode also retains immutable proposal snapshots, reference/judge requests, parsed calls, admission routes, dispatch/commit events, original receipts, tool errors, final native state, final reporting and per-dimension violation labels. Successful and unsuccessful HTTP attempts retain request bytes and response bodies with credentials redacted. `/tokenize` is attempted diagnostically when the real server is available; unsupported tokenization is recorded, not a reason to suppress model results or claim consumption attestation.

Email and Slack operations are **in-memory simulated native tools**; no real messages are sent. Some AFTER tasks use a declared deterministic notification inserted into the native environment only after an actual committed send. All task roots are authored, not renamed official benchmark tasks. Slack returns no message ID; no fabricated Slack receipt is required for completion.

The final upload target is:

```text
results/user_runs/native_release_gpu3_<unique-run-id>.tar.gz
```

`COMPLETE_REVIEW_PENDING` means the bounded software schedule finished, not that the hypothesis succeeded or the paper is ready. Safe non-completion, physical completion, reporting, exposure, unknowns, censorship and effect violations remain separate. An error after a commit never erases that effect.

## Optional local checks

These are optional engineering modes; the default command already runs CPU qualification and then the actual study:

```bash
bash VERIFY_NATIVE_RELEASE.sh
bash RUN_NATIVE_RELEASE_GPU3.sh --cpu-only
bash RUN_NATIVE_RELEASE_GPU3.sh --mock
```

The two modes are explicitly labeled **no model inference**. The mock exercises the full 48-slot machinery, including source-original feedback and real native mutations, with an in-process HTTP test double. Mock violations/protection are scripted fixtures, not scientific findings.

Read-only validation of an extracted real or mock archive uses the same research venv, without GPU or server:

```bash
.venv/bin/python -m release_native_study.verify_results /absolute/path/to/extracted/run
```

No fresh GPU run was executed when packaging this code. `validation/` records exactly which CPU/mock/fresh-extraction checks were run. Runtime depends on server startup and generated tokens; old campaign durations are not a forecast.

## Environment recovery, only if actually missing

Existing working environments are preferred. The research lock is supplied for deliberate reconstruction, not automatic mutation:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-native.lock.txt
```

Do not execute that recovery block over a working environment. Keep model serving in `.venv-serving`; this package does not reinstall vLLM/torch. A missing interpreter, Ninja, cache shard, supported serving flag or pinned runtime yields an explicit logged error. No other GPU, server, revision or model is substituted.
