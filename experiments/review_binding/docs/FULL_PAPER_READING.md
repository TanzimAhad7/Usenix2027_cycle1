# Complete readings and claim-specific reasoning

This records what was actually read in this task. A complete text reading is distinguished from targeted artifact inspection or a metadata check. PDF-derived lines are a reading audit trail, not quotations reproduced in this document.

## Coverage

| Paper/version | Complete text read | Visual inspection | Artifact scope |
| --- | --- | --- | --- |
| [AttriGuard, arXiv 2603.10749v1](https://arxiv.org/pdf/2603.10749v1) | All 24 pages: Sections 1–7, references, Appendices A–E, prompts, omitted results, adaptive-attack specification and limitations | PDF pages 6, 7, 9–12, 21–22; Algorithm 1, all three numbered figures and all eight tables | Supplied guard's key execution, routing, matching, attenuation and receipt paths; bundled-source equality; real runtime interfaces and byte comparison. Not all published experiments reproduced. |
| [DRIFT, arXiv 2506.12104v3](https://arxiv.org/pdf/2506.12104v3) | All 20 pages: Sections 1–5, limitations, references and Appendices A–C, including every prompt and detailed result table | PDF pages 4, 6–11, 15–20; all numbered figures and tables, including prompt figures | No DRIFT code execution or reproduction in this task. |
| [ACE, arXiv 2504.20984v3](https://arxiv.org/pdf/2504.20984v3) | All 24 pages: Sections I–VII, references and Appendices A–F, including grammar restrictions, information-flow rules, prompts, failures and attack traces | PDF pages 3–5, 7–8, 11–13, 15–17, 22–24; all numbered figures and tables | No ACE code execution or reproduction in this task. |

`reading_coverage.json` records PDF/text hashes and consecutive newline-based reading windows. Minor line-number discrepancies from PDF form-feed characters are handled by using newline counts. Visual checks used rendered pages alongside the full text, not OCR snippets alone.

The [official AttriGuard proceedings page](https://www.usenix.org/conference/usenixsecurity26/presentation/he-yu) and its linked 21-page PDF, which includes a proceedings cover, were checked through web retrieval. Direct local download returned HTTP 403. That proceedings PDF received targeted inspection only and is not represented as a second full reading. The complete AttriGuard analysis here is pinned to the explicitly identified arXiv version. The 18-page NDSS proceedings ACE PDF was located; the full reading used the 24-page arXiv version with supplementary appendices.

The rejected manuscript and reviews were used as supplied project context. This task does not claim a fresh complete rereading of every prior project document, incident report, or paper named in the authority plan.

## AttriGuard: what bears directly on our claim

**Method and scope.** Sections 2.3 and 4 separate an observation-level attacker from root instructions and exclude explicit delegation to attacker-modifiable content. Algorithm 1 gates each candidate; blocked calls return empty content with an error warning. The operational design compares individual calls with a teacher-forced shadow, with exact matches accepted before fuzzy adjudication. Section 4.4 separately discusses scheduling variance. The paper acknowledges imperfect attenuation and no proof of robustness. The cost table's footnote excludes auxiliary-model tokens from its target-agent token accounting. Appendix C explains ASB's residual rates through benchmark scope, and Appendix D specifies adaptive attempts.

**Our inference and test choice.** The strongest review-continuity question is a refinement mismatch between the supplied execution path and the conceptual mediation obligation. We should not recast it as a failure of influence measurement. Conversely, a membership check is insensitive to extra identical occurrences; its effect depends on tool semantics and actual grant use. The same-batch scheduling instruction motivates examining multiplicity but is not evidence that an attacker induces duplicates. A real fuzzy model, auxiliary configuration, native provider transport, and reachable histories remain necessary for deployment-level interpretation.

**Design consequence.** Keep the root task fixed and supply useful factual data. Do not base a security claim on the excluded unrestricted-delegation setting. Keep component exact/fuzzy checks distinct from semantic judgment performance. Count auxiliary generation, failed calls and recovery in future full-workflow cost.

## DRIFT: what is already established conceptually

**Method and evidence.** Section 3 begins with trusted-query planning, constrains trajectories and parameters, then allows a privilege-aware dynamic validator to handle deviations. Its isolator masks conflicting tool instructions before reuse. Sections 4 and Appendix A report component ablations, a limited open-ended-task study and adaptive tests targeting the isolator; Appendix C gives the actual prompts. Read-only operations receive different treatment from writes or external actions. The paper explicitly discusses untrusted memory reaching policy-updating components, so that broad motivation is already prior work.

**Our inference and test choice.** We cannot claim novelty merely because intermediate state can influence a later safety decision, or because an agent needs dynamic fact-dependent actions. Our controlled review transition is narrower: an empty result controls whether a later occurrence is reviewed. A future history result would need the actual reference's delivered inputs and operative release/effect dependence. Our payment contract should express permitted effects explicitly rather than inheriting a universal Read/Write/Execute ordering.

**Design consequence.** If DRIFT is selected as a comparator, implement its relevant protections faithfully and report the interface adaptation. The isolator is a distinct possible protection mechanism, not a name to add to a table. Its paper-only results do not establish how it handles this package's custom duplicate-payment or error-transition workload. Observational trajectory-length comparisons and targeted isolator attacks are not a universal causal or adaptive guarantee for every module.

## ACE: what a stronger execution boundary changes

**Method and qualifications.** Sections IV–V separate trusted abstract planning, concrete matching and isolated execution. Appendix A tracks explicit and implicit information flow, including loop fixpoints. Appendix C expressly limits formal soundness claims for its Python runtime and notes the orchestrator's lack of explicit worker-state visibility. Appendix F separates simulated tool invocation from richer effect correctness. Its threat model includes malicious app metadata, unlike an observation-only attacker.

**Our inference and test choice.** A source comparison against ACE must respect its supported interface and trust boundary. Feeding attacker-written roots or inventing a missing error representation would not test the stated guarantee. Its loop and branching analyses also mean we should not present generic persistent dependencies as a new principle. The observer should check actual committed effects even where a benchmark calls a tool invocation the security endpoint. A claim about cumulative payment permission is different from a claim about information-flow labels.

**Design consequence.** Our independent contract gate is a positive containment control, not an ACE implementation or a new architectural contribution. A meaningful cross-system comparison needs the same contract and effect semantics with faithful implementations. A protected type error may preserve one boundary while losing a useful result; security and availability should remain separate outcomes.

## What the readings change about novelty

The following are our judgments, not additional experimental findings about these systems:

| Proposed claim | Current assessment | What would make it substantive |
| --- | --- | --- |
| External influence is not authorization | Insufficient as the main novelty | A new mechanism with consequential effects, tested boundaries and a precise distinction from existing enforcement |
| A previous block changes later review coverage | Concrete implementation evidence; scientific scope unresolved | Autonomous reachability, a forbidden commit, adequate controls, and importance or recurrence beyond a local conditional |
| A matching reference can release excess occurrences | Concrete structural/implementation lead; uses familiar counting principles | Natural excessive proposals, true non-idempotent harm, grant-aware controls and meaningful transfer |
| Intermediate artifacts can retain hostile authority cues | Broad principle already overlaps prior memory/isolation work | Actual operative reference dependence and causal release/effect evidence beyond existing results |
| A defense protects through later enforcement or recovery | Worth investigating, not yet a selected contribution | A new condition that predicts protection and limits on fresh cases, with usefulness and total cost |

The component matrix strengthens implementation fidelity and observation. It does not close the novelty, reachability, or transfer obligations. The proper next experiment is the smallest autonomous diagnostic that distinguishes a reachable security mechanism from a protected or unattainable component path.

## Remaining comparison work

No exhaustive literature claim is made. Before a main history, policy, or measurement contribution is selected, read its additional nearest papers and artifacts in full under the same coverage discipline. CausalArmor, CaMeL, Progent, AgentSys, AuthMem-Bench and EAL are not represented here as newly completed full readings or reproduced systems. The source availability of those methods and the final chosen mechanism determine which comparisons are necessary.
