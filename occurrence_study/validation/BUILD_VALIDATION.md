# Delivery validation

- 28 engineering tests passed. The full controller test uses real study orchestration with scripted model responses and mocked serving/GPU operations: all 96 workflows execute even when Gemma's two-use tasks fail, both model servers stop, all 16 lawful-prefix continuations are recorded and reconstructed diagnostic cells complete. Additional regression tests cover paraphrased carriers across all four structures, immutable fields and non-carrier messages, first/last serial-duplicate checkpoints, diagnostic failure isolation, transport, clone integrity, request replay, no retries, GPU-placement rejection and owned shutdown.
- 37 scripted CPU integration assertions passed using the real pinned AgentDojo runtime and stock simulated email functions under the declared fixed simulator clock.
- Fresh model calls: **0**. GPU inference: **0**. No Qwen or Gemma server was launched for this build.
- The controller's 96 slots and 16 continuations are engineering fixtures, **not autonomous model episodes or scientific results**.
- Native email effects in CPU tests are in-memory sent records; no external email was transmitted.
- Original-signature receipt aliasing is explicitly observed. The pre-inference auto profile selects the named receipt-binding correction while preserving M0 admission; original-feedback sensitivity remains separate.
- The complete raw CPU records are preserved in `cpu_raw_evidence.tar.gz`; `cpu_summary.json` contains the assertion ledger. Engineering output is in `engineering_tests.log`.
- Real vLLM startup, cached weight completeness and actual GPU-worker placement remain remote execution checks on the user's server. The launcher enforces them before using a model.
