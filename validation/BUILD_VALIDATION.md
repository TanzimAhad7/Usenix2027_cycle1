# Implementation validation

The final shipped Python files match those tested after a fresh ZIP extraction.

- 18 CPU qualification tests passed; zero failures. One additional process-cleanup test was skipped because this local runtime remaps Python process IDs relative to /proc. The live launcher explicitly refuses this mismatch before starting a server.
- The documented nohup launcher completed all 32 reference blocks and 48 admission comparisons using scripted HTTP responses, original release source and actual native Slack state.
- Shared reference input, output and initial-state checks passed for all 16 ONE/EXCESS pairs.
- An injected first-request failure produced exactly one HTTP attempt, left only its two dependent admissions unexecuted, and finalized all 48 census entries. Other blocks continued.
- A held shared lock blocked another launcher without starting a server.
- Every one of 1,773 full-run evidence-file hashes and 1,742 failure-run evidence-file hashes matched its generated archive.
- Terminal launcher status was verified to appear after the archive existed.
- Shell and Python syntax checks passed.

These are engineering checks with zero model inference. Live GPU placement, vLLM startup and scientific outcomes must still be established on the user's server. The run repeats qualification in the actual research environment before starting Qwen.
