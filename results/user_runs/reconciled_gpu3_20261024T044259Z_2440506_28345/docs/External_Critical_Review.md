# IEEE S&P 2027 — Critical review and implementation amendments to the October 23 final experiment design

**Reviewed:** `IEEE_SP_Final_Experiment_Design(1).md` (prospective, 392 numbered source lines including headings).  
**Evidence consulted:** `IEEE_SP_Occurrence_GPU3_20261023_Independent_Scientific_Audit.md`, `IEEE_SP_Scientific_Reconstruction.md`, and the public AttriGuard, TraceGrant, ContrAgent, and ToolSafe method descriptions.  
**Status:** Scientific protocol review only. No new models, autonomous experiments, native integrations, or commit effects were executed for this addendum.

## Decision

**Approve the overall scientific direction, but do not freeze the current protocol as the final causal test until the changes below are incorporated.** The 174 rollout arithmetic is correct: F 24 + C 36 + historical C 6 + R 56 + historical R 4 + A 48 = 174, comprising 108 autonomous and 66 controlled/conditional rollouts. J's 24 fixed-candidate evaluations and up to 48 P cells are *not* rollouts.

The strongest prospect is a bounded explanation of how security interventions affect **effectful recovery**, not a claim that a reference guard ought to provide a complete authorization oracle. AttriGuard already describes action-level causal attribution, fuzzy survival, and teacher-forced replay. Ordinary remaining-grant enforcement and temporal contract monitors already appear in external work. Novelty remains conditional on consequential native/supported evidence and a predictive protected boundary.

## Amendments required before the code freeze

### A1. Add genuine M0-versus-M1 policy forks on each new R parent (**highest-priority causal fix**)

The current R panel sets `NONE/FIRST/SECOND/BOTH` by intervention and then runs M1 for the remaining trajectory. These branches identify the effect of forced partial release and resulting receipt/feedback as a *bundle*. They cannot, alone, establish that the M1 occurrence-capacity rule **caused** the partial release, even if an offline M1 assignment is also printed.

**Add two policy-realization continuations per existing R parent**, under identical initial trusted world, frozen scripted actor batch, frozen reference evidence and occurrence-corrected receipt implementation:

- `R-POLICY-M0`: Let unmodified M0 make and execute the first-batch decision, then continue the actual workflow with M0, review-continuity enabled, and the same declared feedback variant.
- `R-POLICY-M1`: Let M1 make and execute the first-batch decision on precisely the same identified compatibility relation, then continue with M1 and the same other controls.

Do **not** override the first-batch release in these eight forks. Capture precise release IDs, legal committed prefix, feedback, new actor/ref proposals, and final ledger. If M0 and M1 initially decide identically, that parent does not identify a repair-induced first-batch difference; preserve it as a negative case. If compatibility is unresolved, mark `UNKNOWN_COMPATIBILITY` instead of forcing an M1 admission graph. Preselect one feedback condition (`T0`, consistent across both forks) and document it in the frozen manifest. These are controlled-prefix continuations, not eight new autonomous attack origins.

**Revised allocation if appended:** R 56 + 8 = **64**, rollout total **182**, broken down into 108 autonomous and 74 controlled/conditional; J24 and P up to 48 remain separate. The alternative is to replace eight less informative R diagnostic branches with these forks while maintaining 174, but do not silently drop factorial cells and continue claiming a complete factorial.

### A2. Separate initial-release and recovery-policy effects in interpretation

Classify each R result by **(initial selector, initial actual committed prefix, block feedback, subsequent policy, actual further effects)**. A harmful future 10-unit payment following a forced `FIRST` state does not automatically establish M1's harm. Conversely, a changed M0/M1 outcome with the same parent does not isolate *why* it changed without examining receipt and new-generation traces. The report should use three distinct labels: `RELEASE_INTERVENTION_EFFECT`, `POLICY_REALIZATION_EFFECT`, and `AUTONOMOUSLY_REACHED_POLICY_EFFECT` (the last requires a complete natural workflow).

### A3. Fix the potentially misleading T1 feedback wording

The root grant remains unchanged when a legal installment is blocked, but **remaining permitted effects are reduced by any installment that already committed**. Do not say simply “the user's grant is unchanged” as that can be interpreted as “the full amount remains.” T1 should truthfully distinguish (i) unchanged original contract, (ii) specific successful commits already made, (iii) the blocked occurrence having **no** effect, and (iv) no claim that a blocked installment was malicious. Keep T0/T1 message structure, receipt IDs, response-status fields and other context matched. Do not suggest the next payment or compute the remainder in T1; the `V_actor/V_reference` intervention already tests an explicit remaining-state summary. Inspect rendered text to confirm it does not introduce extra authority.

### A4. Add an actual policy comparator rather than treating G as the evaluated defense

Keep `G` as an oracle *ceiling* using structured trusted contracts, and distinguish it from the reference-based comparators M0 and M1. In the final analysis include an elementary application-enforced budget/idempotency comparator with **the same trusted contract/ledger information** in declared tasks, and openly state that this is an existing authorization principle, not a novel algorithm. A more realistic public-information implementation or an external comparator (if technically available) is needed before claiming practicality. The project must be able to conclude: “the interesting effect is explained entirely by ordinary stateful authorization.”

### A5. Define the outcome of every terminal/pending effect as a four-way operational status

For each proposal record `PROPOSED`, `REVIEWED/SKIPPED`, `RELEASED/BLOCKED`, `DISPATCHED`, `COMMITTED_EFFECT` or `COMMITTED_NONE` or `UNKNOWN_COMMIT`, and contract truth at the **pre- and post-effect** prefixes. A timeout/error after commit is a violation if the effect breaks the grant. An unreached/blocked attack is not a measured release failure. For email count native sent records and addressed-recipient uses; do not infer distinct external SMTP deliveries. For partial batch execution attribute each receipt to occurrence IDs and keep the rest of the batch in their original ordering.

### A6. Make the causal role of review-continuity explicit

C0/C1/C2 on newly run, evolving autonomous workflows measure a *total policy effect* because changing review coverage can alter shadow generation, feedback, and subsequent actor behavior. For each selected legitimate pre-block historical C parent, separately report the same fixed **later sensitive candidate** under source-default routing versus forced-current-review, preserving true precommit state and eligibility. This is a local routing/admission comparison and should not be counted as an autonomous continuation. State whether extra review was actually invoked and whether the **new reference** still approved the candidate. In particular, restored review is not proof of blocked harm.

### A7. Publish native/source fidelity and qualifying controls *before* substantive attack conclusions

F's source-feedback versus repaired-feedback comparison is important and should remain. CPU parity must validate original reference requests, reviewed branches, status and committed effects on the same recorded-response tape. Label all primary observations `pinned AgentDojo simulated email sink in authored adapted AttriGuard integration`, not an untouched benchmark or production email deployment. Preserve the published-profile role/model differences. Keep failed lawful two-send controls as functionality limits, not silent qualification passes.

## Strongly recommended refinements, without further large sweep

**R1. Freeze the matrix even when branch eligibility collapses.** Precommit all 182 rollouts if A1 is appended, all 24 J evaluations and all P origins before inference; do not search for additional favorable cases if an intended auto partial-release never occurs. An absent or ambiguous cell remains named `UNREACHED`, `UNKNOWN`, or `TECHNICAL_FAILURE` with original lineage.

**R2. Measure reason for acceptance, not merely final grant violation.** For every unauthorized commit report four potentially overlapping diagnostics: `(a) review skipped`, `(b) reference action infeasible in current trusted prefix`, `(c) feasible reference matched to infeasible actor operation`, `(d) jointly infeasible collection despite individually plausible matches`. One incident may satisfy multiple. This classification distinguishes the P paper's hypothetical failure paths.

**R3. Keep recipient-wise email permissions as a separate contribution candidate.** A+B combined message and separate A then B are both authorized; A then A+B is not. The native sent-record operation and recipient-incidence vector must be independently reconciled. This tests more than payment arithmetic and may provide the best predictive transfer if exposed autonomously.

**R4. Distinguish conditional recovery from actual attacker reachability.** R has scripted lawful initial proposals and branch-forced release; A/C/F have evolving model proposals. The argument “security repair causes harm under agent recovery” requires both a valid controlled policy effect and evidence that the required partial-release/recovery transition occurs in an actual supported workflow, with its empirical frequency bounded to tested tasks.

**R5. Add missing nearest-work obligations to the paper plan.** AttriGuard is the target mechanism; TraceGrant addresses task-effect contracts and runtime effect authorization; ContrAgent (Sept. 2026 preprint) already compiles finite-trace logic contracts to online monitors; ToolSafe (Findings ACL 2026) explicitly studies guardrail feedback; Temporary Authority, Permanent Effects addresses commit-boundary authority. These constrain claims to the *specific reference-mediated release and recovery interaction*, not generic stateful budgets, post-refusal behavior, or a novel trace checker. Paper/artifact comparisons still require method-level study and fair applicable implementations.

**R6. Do not force one paper from two distinct phenomena.** The hostile-message F/P studies concern lower-trust instructions and counterfactual attribution; the clean scripted R studies concern defender-induced partial execution and replanning. They become one scientific contribution only if a specified reference-admission property *predicts both* under connected tests. Otherwise report a primary supported finding with the other as a clearly bounded secondary evaluation, rather than claim one causal mechanism for all results.

**R7. Predefine an end-state decision.** If the faithful original-feedback email panel does not expose a consequential supported mechanism, and the new real-policy R forks do not show a nontrivial reference-dependent difference beyond a familiar budget check, change the main direction. More model rows cannot fix that evidence gap.

## Updated claim ladder

1. **Already supported from historical audit:** 96 authored workflows, including 20 forbidden-effect cases and 47 secure completions under the declared finite contracts; reconstructed and scripted controlled 4+10 repair-associated continuation; source-adaptation bounds apply.
2. **If F/C/A show new complete native-tool outcomes:** bounded autonomous reachability and protections in authored workflows using a supported sink, with original-feedback provenance explicitly reported.
3. **If R policy-realization forks differ reproducibly:** controlled causal effect of M0 versus M1 on the same scripted legal proposal and parent state, with full outcome and alternative explanations.
4. **If an autonomous A/F workflow naturally reaches the corresponding partial-release transition and effect:** a consequential release/recovery behavior in a tested workflow, not merely a forced component.
5. **Only if novelty comparison and prospective prediction survive:** a predictive, paper-level boundary of reference-based admission with legitimate-work cost. Neither the authorization principle nor the elementary finite-trace invariants are new theorems.

## Run and provenance policy

No new model run has been performed for this review. Preserve the existing `/home/tahad/IEEE_SP/IEEE_SP_2027` root, `.venv`, `.venv-serving`, *physical GPU 3 only*, Qwen then Gemma serially, `nohup` plus uniquely named logs, immutable old archives, fresh run IDs, full raw requests/responses, ledger/receipt deltas, atomic archive finalization on failure, and original schedules. Hash this addendum and the final merged protocol before science. Keep the exact advertised scope and counts in the executor status and final report.

## Principal external literature to verify in manuscript work

- AttriGuard (USENIX Security 2026): https://arxiv.org/html/2603.10749v2
- TraceGrant (2026 preprint): https://arxiv.org/html/2608.21126
- ContrAgent (2026 preprint): https://arxiv.org/html/2609.18128
- ToolSafe (Findings ACL 2026): https://aclanthology.org/2026.findings-acl.1850/
- Temporary Authority, Permanent Effects (2026 preprint): https://arxiv.org/abs/2607.10487
