# Build validation

Validation performed with Python 3.12 and the pinned AgentDojo runtime. No GPU inference or new scientific model experiment was performed.

- **13 engineering tests passed**, including the full frozen 182-slot offline campaign, J/P/fixed-route scheduling, genuine M0/M1 first-selector divergence under controlled fixtures, all R factorial branches, historical first-batch replay under the actual model aliases, role-card isolation, strict replay drift rejection, unidentified compatibility, recipient-wise gates, keyed retries, monotonic snapshots, primitive-observer reconciliation, and archive generation. A separate low-disk preflight test passed and verifies that inadequate storage prevents inference while preserving a diagnostic record.
- **23 CPU qualification checks passed**, including the retained real-runtime CPU suite, request/message/routing/status/effect parity against an uninstrumented source on recorded fixture tapes, lawful separate/combined email, forbidden recipient reuse, whole-email rejection, commit-before-error labeling, historical file hashes and exact reconstruction of both overwritten retry states.
- The actual controller's **CPU-only path exited 0**, archived its source and complete named census, and correctly reported zero new model work. Its unexecuted GPU slots remain explicitly unexecuted.
- Both shell entrypoints passed `bash -n`. All 182 roots/carriers and separately counted J/P/route schedules are exported in FROZEN_PROTOCOL.json.

The full offline schedule intentionally preserves the source's receipt-identity errors in original-feedback duplicate batches. It also exercises visible strict request drift when a deliberately wrong CPU model alias is supplied to historical replay; the ten historical rollout settings are separately tested with the correct recorded aliases. These are checks of error retention, not scientific results.

Raw CPU qualification evidence, the qualification summary, controller CPU status/scope, and test logs accompany this report. They contain scripted responses and reused historical tapes. The independent observer matched primitive effects throughout the complete offline campaign.

Not validated here: remote vLLM startup on the user's H100, cache completeness, the installed serving environment on that host, live model compliance, live causal hypotheses, external baselines or publication novelty. SETUP_AUTHORIZATION.sh passed syntax validation but its network installation was not executed here. The launcher checks runtime/source/GPU/model identity on the target host and archives startup failures. A complete campaign still requires the user's GPU run and subsequent semantic inspection.
