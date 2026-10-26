# Complete authorization and recovery experiment

Extract this ZIP into `/home/tahad/IEEE_SP/IEEE_SP_2027`, beside the existing `.venv` and `.venv-serving`. The new `authorization_study` module and launcher have their own names; previous result archives remain separate.

Run the entire campaign:

```bash
cd /home/tahad/IEEE_SP/IEEE_SP_2027
bash START_AUTHORIZATION_GPU3.sh
```

It starts in nohup, prints a unique PID/log/results path, and needs no scientific approval between panels. Follow the printed `tail -f` command; Ctrl+C exits tail without stopping the detached campaign. Do not start another copy while it runs.

Qwen3-32B runs first, its owned server stops, then Gemma3-27B runs on the same physical GPU 3. The exact GPU UUID, cached model revisions, localhost port 18080 and supplied chat templates are checked. Another GPU or someone else's server is never substituted. All roles use the active model; Qwen uses native tools and Gemma the explicit JSON interface. Those configurations do not isolate model architecture effects.

The package runs **182 scheduled rollouts: 108 autonomous and 74 controlled/conditional**. It separately schedules **24 fixed-candidate admission evaluations, four fixed-candidate route evaluations, and up to 48 reference component cells** from six frozen origins. Four R initial-evidence preparations are shared, not extra autonomous episodes. All independent slots are attempted despite negative scientific findings or failed lawful controls. Invalid infrastructure or unauthenticatable parent data produces explicit named unavailable/unknown slots.

The launcher requires 4 GiB free before a live campaign and checks a 256 MiB reserve before each slot, recording low-storage failures. Existing environments are used without installation during science. For a fresh machine with Python 3.12 available, `bash SETUP_AUTHORIZATION.sh` installs the pinned research environment and the declared serving stack in project-local venvs under nohup, with a log. Model weights are explicit cached machine assets, not included in this ZIP. Default cache:

```
/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache
```

An alternative cache root can be supplied once with `bash START_AUTHORIZATION_GPU3.sh --cache /absolute/cache/path`; revisions remain pinned. No other source repository is required. Minimal historical parent records and their hashes are included locally.

Every slot retains native messages, HTTP requests/responses, generated text, parsing/errors, token usage/tokenization where supported, source diffs, proposals, routing, reference/judge decisions, releases, receipt identities, dispatches and primitive effect ledgers. Analysis exports a complete rollout census, overlapping failure diagnostics, paired R matrix, autonomous bridge exposure, recipient counts, a fixed-tape application comparator and inspection flags. Informative cards are request-local to the treated role; raw card text and tokenizer responses are saved. The original admission exact-match fast path is preserved in J.

On completion, failure or catchable interruption, the controller stops only its owned server and writes `results/user_runs/<run-id>.tar.gz` plus its SHA-256. Archive publication uses an atomic rename. `SIGKILL`, host failure and exhausted storage cannot guarantee finalization; the raw run directory remains the recovery source. Final status, shutdown records, source and file checksums are included. No automatic science retries or result-based task replacement occur.

The research claim is not a new budget monitor. G is a structured-contract enforcement ceiling; the separate reference-free application comparator replays frozen candidate tapes. A practical external defense comparison, independent confirmation and human semantic review remain outside this development campaign.

Read `IEEE_SP_Final_Experiment_Design.md` for the full merged scientific design, `IEEE_SP_Standalone_Research_Authority_Current.md` for the integrated project authority, and `INTEGRATION_DECISIONS.md` for how the critique was handled. The authority preserves the historical science and negative evidence; this package does not silently rerun or relabel it.

CPU verification:

```bash
.venv/bin/python -m unittest authorization_study.tests.test_campaign
.venv/bin/python -m authorization_study.qualification results/cpu_check_new_id
```

These are engineering checks using scripted/recorded responses and real pinned tool dispatch. They are not new model experiments. No GPU campaign was executed while producing this delivery. See `authorization_study/validation/BUILD_VALIDATION.md` for actual validation coverage and remaining limitations.
