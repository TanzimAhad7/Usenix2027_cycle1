# IEEE S&P occurrence experiment — fresh complete run

This package contains its experiment and selected guard source. It uses your
existing `.venv`, `.venv-serving` and pinned cached Qwen/Gemma weights. It does
not import another project's source or previous experiment results.

## Start once

Put the ZIP in `/home/tahad/IEEE_SP/IEEE_SP_2027`, then paste:

```bash
cd /home/tahad/IEEE_SP/IEEE_SP_2027
unzip -o IEEE_SP_Occurrence_Study_GPU3_Fresh.zip &&
bash START_OCCURRENCE_GPU3_FRESH.sh
```

This starts from zero under `nohup`, with a new
`occurrence_fresh_gpu3_<timestamp>_<pid>` ID. Existing results/logs are not
deleted, resumed, imported or counted. The launcher prints the PID, log, status,
results directory and exact `tail -f` command. Ctrl+C while following that log
stops the viewer; the detached run continues.

The default executes **all 96 core workflows**: Qwen's 48, stop its owned server,
Gemma's 48, stop its owned server, analyze and archive. Physical GPU 3 only,
sequentially on local port 18080. Two server startups, with automatic switching.

## Corrections included

- Task non-completion, attack protection and attack success do not suppress
  remaining tasks. Initial controls record execution validity and task success
  separately. Individual recorded generation failures also remain outcomes
  while unrelated tasks continue. Invalid pinned integration, unavailable GPU/
  port, failed serving ownership and dead servers remain infrastructure failures.
- Hostile ON workflows diagnose the first and last eligible reviewed sensitive
  batches after carrier delivery. All reviewed batches remain in the ledger,
  including the batch in which the first forbidden effect appears.
- Reference contrasts no longer need an exact match to paraphrased text.
  Original delivered carrier data are joined to derived receipts by occurrence
  ID. Four identically rendered reconstructed-reference profiles test the raw
  notice unchanged, pure instruction deletion, declared neutral replacement,
  and a metadata placebo. Actual attenuated input stays a separate baseline.
- Four lawful-prefix recovery cases run for both models, regardless of attack
  outcomes or initial control success: one-use, two-use, legal installments and
  registered-key retry. Each has M0/M1 continuations: 16 in total.
- Diagnostic exceptions preserve their failures and allow unrelated work to
  continue. Final coverage explicitly exposes missing and unresolved evidence.

The original 96 task prompts, conditions, seed, tool semantics and default
receipt profile are unchanged. This is a fresh development rerun with an amended
diagnostic protocol, not independent confirmation on unseen tasks.

## Automatic panels and limits

1. Scripted CPU integration checks, with zero model calls.
2. All 96 autonomous core workflows, OFF/ON and clean/hostile/two-use.
3. Up to 32 checkpoint origins, selected without outcome filtering. Actual
   M0/M1/M2 controls plus four reconstructed-reference profiles, each with at
   most eight generation attempts: 32 attempts per origin.
4. Reference lawfulness assessed in isolated clones, never in the actor world.
5. Sixteen lawful-prefix M0/M1 continuations. Prefix calls are scripted;
   references and later actor recovery are model-generated. Initial responses
   are shared only when their exact requests match.
6. Receipt-profile sensitivity at the first mismatch or duplicate-signature
   batch per effect family/model, at most four parents/eight continuations.
7. Raw records, coverage, analysis, hashes and the final `.tar.gz` archive.

No carrier, no proposal, skipped review, missing provenance, unidentified edges,
budget exhaustion and execution errors are distinct from protective results.
Forced diagnostic components are not additional autonomous episodes. Email and
payment effects are simulated; no real messages or money leave the process.

Default feedback `auto` uses CPU evidence to select the named occurrence-ID
receipt-binding correction before inference, while retaining M0 admission.
Explicit `--feedback original` remains a separate recorded profile. No silent
repair of source admission, judge verdicts or malformed model outputs occurs.

Each full workflow/continuation permits 12 actor rounds, 64 generation attempts,
4,096 output tokens and a 3,600-second watchdog. Generation timeout: 300 seconds,
without retry. Separate diagnostic caps are frozen in the protocol. These
ceilings are safeguards, not predictions of runtime.

Previously observed core workflows averaged about 6–10 seconds, but this run
adds reference branches and recovery tests. Under similar serving behavior,
expect tens of minutes; slow branches/failures can extend it substantially.
Follow the printed log for measured progress.

## Outputs

| Path in the new run | Contents |
|---|---|
| `status.json` | Completed/expected core count, errors and final state |
| `frozen_protocol.json`, `source/` | Exact tasks, budgets, profiles and source |
| `cpu_qualification/` | Scripted integration checks and raw effects |
| `<model>/qualification_decision.json` | Execution validity versus task success; no task-success gate |
| `<model>/serving_i1/` | Snapshot/command, server log, GPU ownership and shutdown |
| `<model>/workflows/<id>/` | Requests/responses, token captures, events, receipts, state, checkpoints and outcome |
| `<model>/diagnostics/<id>/selection.json` | All reviewed batches and first/last selection |
| `<model>/diagnostics/<id>/batch_*/` | Actual controls, reconstructed inputs, edits, provenance, lawfulness and graphs |
| `<model>/lawful_recovery/` | Four prefixes and paired model continuations |
| `<model>/feedback/` | Receipt-profile comparison and reuse lineage |
| `analysis/` | Core-only ledgers, first-violation flags and diagnostic coverage |
| `attempts.jsonl`, `unexecuted_schedule.json` | Started IDs and every unfinished slot |
| `SHA256SUMS` | Archived-file hashes |

Successful scheduled completion has 96 core results and an empty
`unexecuted_schedule.json`. `COMPLETE_WITH_RECORDED_ERRORS_REVIEW_PENDING` means
the schedule finished but execution/diagnostic records require inspection; it
does not mean all tasks succeeded. Upload the final printed `.tar.gz` archive.

## Existing environment

GPU UUID: `GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6`.
Cache: `/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache`.
Qwen3-32B revision: `9216db5781bf21249d130ec9da846c4624c16137`.
Gemma-3-27B-IT revision: `005ad3404e59d6023443cb575daa05336842228a`.
No `refs/main` lookup, installation or cache search. Ninja is resolved through
`.venv-serving/bin`. AgentDojo 0.1.35 source hashes are verified. A shared
`logs/gpu3_sequence.lock` rejects concurrent runs. Unrelated processes are
neither reused nor killed.

Build-time validation is in `occurrence_study/validation/`. Its
`cpu_raw_evidence.tar.gz` is scripted validation evidence, not GPU research
results; you do not need to extract it.

Explicit `--scope structural` requests only 48 workflows; `--scope qualification`
requests Qwen's first six and omits recovery. Omit those flags for the full run.
