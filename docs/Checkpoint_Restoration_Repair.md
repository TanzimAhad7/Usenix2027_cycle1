# Live checkpoint restoration repair

## Observed failure

The supplied run stopped during CPU qualification: three failures in 54 tests,
zero model inference. All 19 retained-source tests passed. The build host
reproduced the same three failing test methods before changing the code:

- Authentic email checkpoint deemed ineligible after restoration.
- Native checkpoint snapshot changed after a save/load round trip.
- Spawned recovery arms rejected with `ReplayMismatch`.

This is a checkpoint implementation defect, not a research outcome or model
failure. Preserve the failed run and its original source snapshot as a record.

## Cause and repair

The pinned AgentDojo Inbox has an after-validator that initializes `emails`
from `initial_emails`. Normal environment `model_validate` therefore replaces
the captured live mailbox with its initial contents, losing later sent emails
and injected notices. A safe committed prefix can disappear. Exact restoration
checks correctly refused that changed state.

The adapter now validates all persisted Inbox fields individually, then restores
that container without invoking its initialization validators. It preserves
initial emails, live messages, contacts and trash as distinct saved fields.
Native field types and email identifiers are checked. All other environment
components use normal native validation. The entire serialized environment must
match the saved state exactly, followed by the existing complete-world and
sealed-checkpoint checks. Missing fields, inconsistent IDs or other changed
state are rejected. No hash check or eligibility condition was relaxed.

Recovery accounting previously performed a second normal environment load to
count inherited effects. It now reads the already authenticated restored world
before continuation. This avoids losing or misclassifying the committed email
prefix a second time.

Qualification failures now print their names and tracebacks in the main run log.
Retained vendor source and native runtime code were not modified.

## Verification and limits

The original 54-test suite passes after the repair, with one host-only ownership
test skipped because this container's Python and `/proc` PID namespaces differ.
That same skip was present in the pre-fix reproduction; the user's original
report had no skips. The check remains unchanged and enabled on the user host.

Three additional CPU test methods check:

1. Live email round trips preserve reads, trash, contacts and subsequent native
   effects, without aliasing or mutating the input snapshot.
2. Missing Inbox fields and inconsistent email IDs are rejected.
3. All five declared recovery arms preserve inherited effects and count only
   fresh effects, across DM, email and banking: 15 scripted continuations.

The expanded suite has 57 tests: 56 passed and the single namespace-dependent
ownership test was skipped on the build host. Real spawned worker tests execute
as part of the suite. Scripted responses make zero model inference requests.
The 22 separate operational tests, package hashes, ZIP CRC and frozen schedule
are also checked. Machine-readable before/after reports and test logs are in
`validation/`. Cached tokenizer/parser qualification and actual CUDA/vLLM model
inference still require the user's machine and run before scientific collection.

## Fresh run

Use the replacement ZIP with the existing `.venv` and `.venv-serving`.
No reinstall, cache deletion or result deletion is required. The regular launcher
creates a unique detached `nohup` job, reruns CPU qualification and automatically
continues to Qwen and then Gemma if qualification passes.

The scientific schedule is unchanged: 688 autonomous workflows, up to 60
eligible conditional continuations, the same frozen contracts and controls,
two isolated workflow workers per model, and the same model serving profiles.
This repair adds no inference experiments or quantized model profiles.
