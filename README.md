# Prompt-injection guardrails for tool-using LLM agents: code and artifacts

This repository holds the code, frozen designs and lightweight outputs of a research project on guardrails that defend tool-using LLM agents against indirect prompt injection. It covers three phases:
1. the original study, which was rejected at USENIX Security;
2. the experiments run after the rejection;
3. the work in progress now.

The repository contains **code and artifacts only**. Papers, reviews, research notes and planning documents are not included. Third-party license notices are kept where third-party code is vendored.

---

## 1. The rejected paper

*Influence Is Not Authority: When Causal Guardrail Signals Make Legitimate Tool Use Look Like an Attack in Tool-Using LLM Agents* (arXiv:2608.29942). Submitted to USENIX Security 2027, cycle 1; not accepted.

### Question

A user can authorize an action without supplying every value it needs. "Pay the bill in this file" requires the agent to read the account number from a tool result. Guardrails such as CausalArmor, AttriGuard and AgentWatcher treat strong influence of tool content on a privileged action as a sign of attack. Can they tell legitimate dependence on a tool from injected control?

### Main results

| Study | Result |
|---|---|
| Matched source relocation (24 bases, 96 conditions) | Moving one required value from the user's request into a legitimate tool result, with authorization, action and effect unchanged, moved a reconstructed CausalArmor-style attribution signal toward "attack" in **24 of 24** bases under both scorers (Llama-3.3-70B, Gemma-3-12B). On average the move was larger than a matched change that removes authorization |
| Scalar threshold | At the operating point with no benign flags, only 25.0% (Llama) and 37.5% (Gemma) of matched unauthorized actions are caught |
| AgentWatcher | Under conflicting context it flagged all 24 authorized and all 24 unauthorized actions |
| AttriGuard routing | 57.5% of unauthorized calls passed by exact agreement with the shadow run, before the stricter judge, against 29.2% of authorized calls |
| AttriGuard, live (14 natural tasks, 420 runs) | It reduced the selected unauthorized outcome from 17/70 to 2/70. A block redirected rather than ended execution: 12/13 blocked unauthorized proposals were followed by the authorized effect; 9/9 blocked authorized proposals lost it. In the tested version, 18/168 privileged calls ran without the ordinary audit after a defense-generated empty result (disclosed to the authors) |
| Evaluation fidelity | Task success disagreed with preservation of the authorized effect: 18/420 live runs; 23/78 replay pairs |

### Reviewers' main concerns (paraphrased)

- The principle that influence is not authority overlaps with prior work.
- The core study used 24 constructed cases.
- The end-to-end link from signal to harm was weak, and AttriGuard in fact protected in the live study.
- The studies used different defenses, models and outcome measures.
- CausalArmor was reconstructed rather than run from released code.

### Where the artifacts are

`research_basis/studies/01_natural_relevance` … `09_evaluation_replay`, with the vendored defense code in `research_basis/third_party/`.

---

## 2. Experiments after the rejection (October–November 2026)

Each folder contains its code, frozen design and lightweight results. Negative and invalid results are kept.

| Folder | What it tested | Result |
|---|---|---|
| `results/user_runs/`, `reference_discovery_parallel/`, `authorization_study/`, `occurrence_study/`, `release_native_study/`, `reconciled_study/`, `s1_reference_study/` | Autonomous AttriGuard workflows (688 authored workflows), permission and reference studies | AttriGuard protected in the Qwen3-32B profile. Admissions of forbidden actions concentrated in an adapted Gemma-3-27B profile |
| `IEEE_SP_Reference_Study_GPU2`, `IEEE_SP_N1_GPU3`, `IEEE_SP_E1_GPU3`, `IEEE_SP_E2b_GPU2`, `IEEE_SP_A01_GPU2`, `IEEE_SP_J2_GPU2`, `IEEE_SP_Discriminating_Diagnostic_GPU*` | AttriGuard's judge on fixed ("held") candidate calls | Against lawful references, the Qwen judge admitted 0 of 175 forbidden candidates; the adapted Gemma judge admitted 87 of 153 (repeats over 7 candidates). Changed amounts were admitted, changed recipients were not. A permission-led judge prompt lowered Gemma's forbidden admissions from 16/36 to 7/36 on the same inputs |
| `IEEE_SP_R3_GPU2`, `IEEE_SP_R3_Tokenization_Fix` | Released AttriGuard profile end to end, with and without fixes | Every observed violation was contained by a conventional authorization gate |
| `IEEE_SP_END_TO_END_LARGE_GPU23`, `IEEE_SP_QWEN_FORMAT_REPAIR` | Source relocation at scale (96 held-out bases), plus agent runs with a CausalArmor-style guard | Relocation replicated: 0 of 96 bases moved the other way, for both models. An apparent rise in wrong actions under the guard was later traced to the authored records (decoy typed fields), not to the guard |
| `IEEE_SP_FINAL_EXPERIMENT_*`, `IEEE_SP_GATE1_KILL_TEST` | Removal-based remediation on authored records | Gate 1 (preregistered) was rated invalid for the Qwen interface. Results retained |
| `IEEE_SP_GATE2_VALUE_SELECTION`, `IEEE_SP_GATE2_RECONCILIATION_2026-11-11` | Preregistered: what an agent does when the needed identifier is removed | The agent still attempted the write: 94/94 (Qwen) and 76/76 (Gemma) with a substitute in view; 16/16 and 15/15 without one. Hijacking by an attacker-supplied value did not occur (0/22, 0/18). The Gemma interface was rated invalid |
| `IEEE_SP_S0_SANITIZER_FIDELITY` | Whether open-model sanitizers keep required values on natural AgentDojo tasks | Some required values are lost. No downstream harm measured |
| `IEEE_SP_AUGUST_AUDIT_2026-11-14`, `IEEE_SP_POST_S0_DEEP_AUDIT_2026-11-13`, `IEEE_SP_GLOBAL_*`, `IEEE_SP_DEEP_PASS_2026-11-15`, `v3_reanalysis_scripts/` | Model-free reanalyses of the stored data | A model-free "copied from tool output" rule reproduces the attribution detector's decisions (AUC 0.958 / 0.949). In AgentDojo reference solutions, 44 of 60 state-changing tasks need an argument value that only a tool result supplies |
| `IEEE_SP_N2_MISSING_VALUE` | Natural-task version of Gate 2 (silent, marked and signalled removal) | Built and tested on CPU; not run |

### Overall reading

The attribution signal reliably follows where a value came from, and the decision path, not the signal, decides the outcome. The hypotheses that the guards cause harm, or that removal lets an attacker hijack the action, were not supported: the guards mostly failed safe.

---

## 3. Current work (November 2026)

The current question is what released prompt-injection defenses actually enforce on the *arguments* of a tool call, and what utility their kind of policy can reach. Analysis code is in `EUROSP_2027_PLAN/analysis/`:

- **`census_grounding_ceiling.py`** — an upper bound on AgentDojo utility for policies that admit only values stated in the user's request, and for extensions of them. First estimate: 52 of 97 tasks (15 of the 60 that change state). String matching, not yet hand-checked.
- **`census_scope_placement.py`** — where the benchmark's attacker-controllable text sits relative to the values legitimate tasks take from tools.
- **`mine_judge_records.py`** — collects the 2,708 stored judge decisions, with their written reasons, from the runs above. In the stored data, the two judge models agree on changed recipients and split on changed values.

These are preliminary and are not claims of the project yet.

---

## 4. What is not in this repository

- Papers, reviews and research notes.
- Archives, model weights and environments.
- Per-step raw records: model requests, policy transcripts, world snapshots, per-episode copies of generated code, and the per-request model records of the large runs.
- Any single file over 5 MB (2 MB inside run folders).

Each run folder keeps its frozen design, status and summaries, per-episode results where they exist, and analyses, so every reported count can be recomputed. The raw records are retained by the authors.

## 5. Environment

- AgentDojo 0.1.35 (suite v1, plus v1.2.2 where noted).
- Open models served with vLLM: Qwen3-32B and Gemma-3-27B-IT.
- Exact package versions are in the `requirements-*.lock.txt` files.
- Each package's run scripts check model and source hashes before running.
