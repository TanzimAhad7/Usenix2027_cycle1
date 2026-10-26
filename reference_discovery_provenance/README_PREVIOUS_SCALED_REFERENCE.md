# Larger reference-authorization experiment

This is the complete prospective follow-up to the completed S1 run. It preserves the original run and audit under `evidence_basis/`. It adds new code under `scaled_reference_study/`; it does not replace earlier experiment modules, launchers or results.

The schedule is **128 fresh references / 192 conditional admissions**, followed by **960 fresh autonomous workflows**. The complete schedule runs from one launch regardless of favorable, negative or mixed scientific outcomes. No manual continuation after a pilot is required.

## Unzip and launch

Download the ZIP into your existing project directory, then run:

```bash
cd /home/tahad/IEEE_SP/IEEE_SP_2027
unzip -o IEEE_SP_Reference_Authorization_Scaled_GPU3.zip
bash RUN_SCALED_REFERENCE_GPU3.sh
```

The launcher itself uses **nohup**, closed stdin, unique logs and PID/status files. It calls `.venv/bin/python` explicitly, so shell activation is optional. It uses the existing `.venv-serving/bin/python` to start Qwen on **physical GPU 3 only**, validates ownership/placement, completes the full schedule, stops its owned server, and makes a checksummed upload archive.

The cache revision is pinned to `9216db5781bf21249d130ec9da846c4624c16137` under `/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache/models--Qwen--Qwen3-32B/snapshots/`. It needs no `refs/main`, does not select another revision, and does not download weights or install packages. The existing AgentDojo 0.1.35 and serving environment are required. No imports from another research repository are used. This is a project overlay, not a replacement Python environment.

Do not launch a second copy while a run owns `logs/gpu3_sequence.lock`. A busy GPU/port fails safely rather than reusing or stopping another user's server.

## Watch and finish

The launcher prints the exact progress command:

```bash
tail -f /home/tahad/IEEE_SP/IEEE_SP_2027/logs/scaled_reference_gpu3_RUN_ID.log
```

Replace `RUN_ID` with the printed run identifier. `Ctrl+C` in `tail` stops watching; it does not stop the nohup job. Heartbeats show references, admissions, autonomous workflows and elapsed time every 20 seconds. Stage counts have different scientific units and are not added into one sample-size claim.

At completion, `logs/RUN_ID.status` records exit code and archive location. The controller prints `UPLOAD ARCHIVE: ...tar.gz`. Upload that complete archive for analysis. Raw results remain under `results/user_runs/RUN_ID/`, including on partial failure. Status is finalized only after archive creation.

Optional archive integrity verification:

```bash
.venv/bin/python -m scaled_reference_study.verify results/user_runs/RUN_ID.tar.gz
```

## What it runs

| Module | Allocation | Purpose |
|---|---:|---|
| Conditional reproduction | 128 fresh reference blocks, 192 admissions | Sixteen fresh references per original contract/carrier/attenuation cell; paired candidate comparisons share exact reference evidence |
| Autonomous study | 960 full workflows | Four effect families × three workflow shapes × two grants × two carriers × four policies × five fresh fact variants |
| Local dispatch counterfactuals | Every reviewed sensitive proposal | Replay actual release, exact-capacity-after-actual, and trusted-gate-after-actual from identical native state, without fresh generation |

The policies are OFF, original RELEASE, declared per-proposal EXACT_CAPACITY, and RELEASE_G with a privileged stateful contract gate. Shapes are upfront authorization, a notice after the full grant is spent, and continuation with a consumed first operation plus newly permitted operations.

Bank results concern native simulated transaction records and amounts; the native API does not decrement balance. These are not real transfers. Slack and email also run in AgentDojo's local simulation, with no real messages sent.

## Runtime and evidence

This is a long follow-up. The completed fixed-checkpoint study took about 14 minutes, but that is not a valid estimate for 960 full trajectories with repeated actor/reference calls. Allow a day or several days; actual timing depends on generation lengths and recovery loops. Each autonomous slot has a 20-minute deadline, 15 loop iterations and 96 HTTP-attempt cap. Those are failure bounds, not expected durations. The run does not stop after a positive result.

Every workflow saves its trusted contract, initial/final native state, source and instrumentation diff, model-visible messages, driver requests, HTTP requests/responses, available tokenization diagnostics, proposal checkpoints, reference decisions, tool errors, committed effects and local counterfactuals. All source hashes, model/cache identity, server logs, GPU telemetry, negative/censored/missing results, and automated descriptive analysis are archived. Secret authorization headers are redacted. Raw generation text is retained.

`analysis/summary.json`, `cells.csv`, both complete ledgers and `FINDINGS.md` are descriptive outputs, not automatic acceptance of a scientific hypothesis. `COMPLETE_REVIEW_PENDING` means collection completed, not that the paper claim succeeded. See `docs/IEEE_SP_Scaled_Reference_Authorization_Design.md` for hypotheses and decision rules.

## Engineering modes

```bash
bash RUN_SCALED_REFERENCE_GPU3.sh --cpu-only
bash RUN_SCALED_REFERENCE_GPU3.sh --mock
```

Both use the same launcher and archive policy. Mock mode exercises the whole schedule with scripted responses and **zero model inference**; never mix it with scientific results. Live launch first runs CPU qualification. A local container PID-namespace mismatch skips only the process-signaling test; the live preflight refuses ambiguous process ownership before starting a server.
