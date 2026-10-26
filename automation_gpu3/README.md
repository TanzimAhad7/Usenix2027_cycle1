# One-command Qwen → Gemma diagnostic on GPU 3

This small overlay adds automation to the existing IEEE S&P project. It does not replace the foundation, reinstall dependencies, or copy model weights. Put the ZIP in `/home/tahad/IEEE_SP/IEEE_SP_2027`, then run from that directory:

```bash
unzip -o IEEE_SP_GPU3_Sequential_Run.zip && bash START_GPU3_SEQUENCE.sh
```

`START_GPU3_SEQUENCE.sh` immediately returns a PID, a `.log` path, and a results directory. The background controller runs under `nohup` with stdin disconnected. No interactive terminal is required. Viewing the log with `tail -f` is optional; Ctrl+C in the viewer leaves the experiment running.

## Automatic sequence

1. Use existing `.venv` for research and `.venv-serving` for vLLM. Check the pinned AgentDojo runtime and the source-bound native guard. No setup or historical rerun.
2. Resolve both models from cached `refs/main`, or use the unique complete local snapshot when that pointer is absent. Multiple complete revisions are listed rather than selected silently. Pin explicit local snapshot paths. Check weight-shard presence, tokenizer files, and native chat templates. Offline mode prevents accidental downloads.
3. Select **physical GPU 3 by its UUID**. Refuse an occupied GPU or endpoint; do not stop unrelated jobs. Acquire a local sequence lock.
4. Start Qwen3-32B on localhost port 18080, BF16, one GPU, 32,768-token context cap, at most four simultaneous sequences, GPU memory target 90%. Verify socket ownership and actual descendant GPU-worker placement.
5. Run 30 development episodes: 3 input conditions × 5 guard variants × 2 repeated executions.
6. Stop only this launcher's server and children; verify shutdown before switching models.
7. Start Gemma-3-27B-IT from its cache on the same physical GPU and port. Run the identical schedule. Shut Gemma down when finished.
8. Produce JSON/CSV summaries, a short findings record, file checksums, and one uploadable `.tar.gz` archive with its own checksum.

Default cache root:

```text
/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache
```

Only model infrastructure is read there. No source, experiment results, or virtual environment from that other project is imported. Model caches are not copied into the results archive.

## What this experiment measures

Input conditions: `clean`, `review_claim`, and `duplicate_claim`. Guard variants: `original`, `placebo`, `r_minimal`, `r_all_errors`, and `b_occurrence`.

The autonomous agent chooses actions in a custom simulated-payment workflow. The native source-bound guard and AgentDojo runtime execute the choices; a separate ledger records actual simulated effects under the explicit one-payment grant. No real payment or external service is used.

This is an **adapted development diagnostic**, not a published benchmark replication, holdout experiment, independent human audit, or complete v6.2 research program. Scripted qualification controls and larger experiments remain distinct work. A fixed-payload null does not rule out other attack paths.

Both models use a common text JSON action interface. The model generates action names and arguments; the adapter assigns occurrence identifiers and performs strict parsing/schema validation. Tool observations become labeled user messages, preserving occurrence identifiers and native error text. Adjacent same-role messages are combined for Gemma's alternating-role template. The complete actual wire requests are saved. There is no forced valid action sequence, constrained decoding, Markdown stripping, hidden retry, or automatic JSON repair. Invalid output and generation truncation are recorded as errors; effect-free interrupted episodes remain UNKNOWN.

Temperature is zero, generation cap 4,096 tokens per request, budget 80 chat requests per episode, native-loop bound 12 iterations. Qwen thinking is explicitly disabled in every request. Repetition seeds are 20261019 and 20261020. Seeds and temperature zero do not imply deterministic replay or independent tasks. Native per-role `extra_args`, including requested logprobs, are recorded; this adapter does not return logprobs.

Actor, reference/shadow, attenuation, and fuzzy-review roles use the active model. Consequently Qwen-versus-Gemma differences change all those roles together and cannot isolate the actor-model effect. Human semantic review remains pending. Committed effects, secure task completion, payload delivery, and unknown/error outcomes are reported separately.

## Evidence retained

All new evidence is under:

```text
results/user_runs/gpu3_sequence_<UTC timestamp>_<PID>/
```

| Location | Contents |
|---|---|
| `status.json`, root `logs/<run>.status` | Completion, interruption, model exit codes, and failures |
| `schedule.json` | Exact fixed design and execution settings |
| `controller.log`, per-model `server.log`, `diagnostic.log` | Launcher, startup, inference-server, and experiment logs |
| `gpu_telemetry.csv`, GPU snapshots | Physical GPU 3 utilization, memory, power, and device identity |
| Per-model `gpu_qualification.json` | Socket owners and attributable GPU workers |
| `deployment.json` | Snapshot revisions, command, metadata hashes, cached blob links, and file sizes |
| Template/config files | Native template used by the server, rendered example, model config, cached generation config |
| `serving_packages.txt`, `research_packages.txt` | Actual installed versions; no environment secrets |
| `source/` | Research adapter, native diagnostic/guard, qualification script, lock file, and plan snapshot when present |
| `diagnostic/generated/` | Exact guard variants and source diffs |
| Per-episode `http_*.request.json` | Full model-visible prompts/history and sampling settings |
| `http_*.response.json` | Complete successful server response, output, token usage, finish reason, IDs, and any returned metadata |
| `http_*.transport.json`, error files | Latency, response headers, HTTP failures, and error bodies |
| `http_*.tokens.json` | Server-rendered token stream when `/tokenize` is supported; otherwise an explicit unavailable record |
| Per-episode `events.jsonl` | Incrementally flushed requests, responses, roles, decisions, releases, dispatches, carrier delivery, effects, and errors |
| `native.log`, `messages.json` | Native debug output and returned transcript |
| `result.json`, `effects.json` | Contract, outcome, actual committed simulated effects, latency, usage, and failures |
| `summary.json`, `summary.csv`, `FINDINGS.md` | Descriptive results with unknowns and errors preserved |
| `SHA256SUMS` | Evidence-file integrity hashes |

The wrapper saves both completed and failed episodes. It does not rerun failed episodes silently. Episode-level errors do not prevent the next scheduled episode or the Gemma stage; they make final status `COMPLETE_WITH_ERRORS` and the exit code nonzero. Cache, ownership, source-integrity, or server-startup failures stop the sequence and preserve diagnostics. SIGTERM/SIGINT triggers owned-process cleanup and partial-result archiving. SIGKILL, host shutdown, or filesystem failure can prevent final archiving, but already-flushed files remain.

Large model weights are not reread merely to compute digests. Cached blob names, revision, shard presence/size, and small metadata-file hashes are recorded; this is not independent cryptographic verification of every weight byte. Per-token logits, attention maps, hidden states, and server-internal activations are not collected. Successful `/tokenize` output records the server rendering; a tokenizer example alone is not a proof of every request's rendered input.

## Monitoring and return artifact

Use the exact `.log` and result paths printed by the launcher. Model-specific progress is also in `<results>/qwen/diagnostic.log` and then `<results>/gemma/diagnostic.log`.

On completion or handled failure, upload:

```text
results/user_runs/gpu3_sequence_<...>.tar.gz
```

The archive contains data for both stages, or preserved partial data if execution failed. It excludes model weights and virtual environments.

## Verification scope

`test_automation.py` exercises CPU/native-runtime behavior with mock HTTP responses, incomplete caches, strict action parsing, error preservation, model-switch ordering, archiving, and shutdown ownership. Mock tests are engineering validation and never research results. Actual vLLM startup, H100 execution, cached model completeness, and model competence must be established on the user's machine.

To run the included tests manually (optional):

```bash
IEEE_SP_TEST_ROOT="$PWD" .venv/bin/python -m unittest discover -s automation_gpu3 -p 'test_*.py' -v
```

The controller uses the cached native template explicitly via the server's `--chat-template` flag. It does not assume that Gemma-3 supports Qwen's Hermes tool-call protocol. Cache/model changes, adapter changes, and subsequent follow-up campaigns must remain separately identified.
