# Fresh reading and source-inspection ledger

## Scope statement

The goal was to test the supplied work's scientific inference and identify a stronger research direction. Coverage below distinguishes full text, targeted inspection, mechanical inventory, reported history, and unavailable evidence. No claim is made that every line of 254 accepted S&P papers or every vendored dependency was manually read.

## Supplied material

| Source | Fresh coverage | Limitation |
|---|---|---|
| `sec27cycle1-paper2797.pdf` | Complete 19-page text including appendices/references; selected figure/layout check | No original LaTeX or private review discussion |
| `USENIX Security 27 Cycle.txt` | Both reviews end to end | No separate decision/meta-review letter supplied |
| `IEEE_SP_Standalone_Research_Plan_v6_2026-10-07.md` | Complete 1,585 lines | Its newer-code and prior-reading claims are documentary history |
| `hugging-face-incident-report-aug-2026 (1).pdf` | Complete 91-page text/footnotes; selected page rendering | No private canonical transcript corpus; report claims are not our incident replication |
| A674 ZIP | Every member inventoried/hashed; all Python parsed; all nine study paths mapped; critical code inspected as below | Not every line of every duplicated/vendored module manually read; no fresh inference |

## Accepted S&P 2026 research

Official membership checked against https://sp2026.ieee-security.org/accepted-papers.html (254 roster entries). The corpus below is selected for conceptual/methodological relevance, not a representative acceptance-probability sample.

| Paper | Retrieved source | Pages | Fresh reading |
|---|---|---:|---|
| Towards Automating Data Access Permissions in AI Agents | `https://www.umariqbal.com/papers/permissions-sp2026.pdf` | 19 | Complete scientific text, appendices, available meta-review |
| When AI Meets the Web | arXiv:2511.05797v1 | 20 | Complete scientific text, appendices, available meta-review |
| PromptLocate | arXiv:2510.12252v2 | 19 | Complete scientific text, appendices, available meta-review |
| Parasites in the Toolchain | arXiv:2509.06572v5 | 18 | Complete scientific text, appendices, available meta-review |
| Site Isolation is Dead | `https://wsp-lab.github.io/papers/lee-sp26.pdf` | 18 | Complete final IEEE scientific text, appendices, meta-review |
| MAYA | arXiv:2504.16651 PDF | 20 | Targeted methods and conclusions; not complete |
| AttnTrace | arXiv:2508.03793 PDF | 20 | Targeted threat model, baseline/design/theory, meta-review; not full results/appendices |
| Your Compiler is Backdooring Your Model | arXiv:2509.11173 PDF | 19 | Targeted threat, four objectives, challenge/solution design, meta-review; not complete |

Complete-read sample: five papers, 94 pages. Additional targeted sample: three papers, 59 pages of source documents, not 59 pages claimed fully read. A complete text reading is not a claim of visual inspection of every PDF page or replication of the artifact. Available author/arXiv versions may differ from the archival proceedings.

## Closest-work coverage

| Work | Fresh coverage | Not done |
|---|---|---|
| Endogenous Authorization Laundering, arXiv:2609.01836v1 | Main scientific text through conclusions/limitations (~first nine pages); selected artifact availability information | Full appendix and raw-execution artifact audit |
| When Memory Becomes Authority, arXiv:2608.01679v2 | Main scientific text (~first nine pages), methods/results and tradeoffs | Full appendix and independent benchmark replication |
| DRIFT, arXiv:2506.12104v3 | Trusted planning, dynamic validation, isolation, selected evaluation/limitations | Full artifact replication |
| CausalArmor, arXiv:2602.07918v1 | Contextual sanitization and later-reasoning treatment | Native system execution |
| AgentSys, arXiv:2602.07398v1 | Worker isolation, structured-output boundary, validation scope | Native system execution |
| ACE, official NDSS page and linked paper | Abstract/architecture overview | Complete line-by-line reading and implementation audit |

## Code inspection

All paths below are relative to the original A674 archive. “Full” refers to the named core file, not the entire surrounding dependency tree. Large files were examined through relevant functions and callers; that is deliberately labeled targeted.

| Path or module | Coverage | Evidence role |
|---|---|---|
| `README.md`, `CLAIM_TO_ARTIFACT.md`, study READMEs, reproduction guidance | Claim/provenance mapping and execution boundaries | Links paper claims to frozen artifacts |
| `third_party/integrations/attriguard_zenodo_v1/usenix-artifacts/main/pipeline/AttriGuard.py` | Full policy/control-flow inspection, including prompts; three source-executed fixtures | Allowlist, synchronization, exact/fuzzy matching, skip/execute, receipt binding |
| `implementation_evidence/paef_oracle.py` | Full; deterministic probes | Historical outcome and state reconstruction limits |
| `studies/02_controlled_source_relocation/support/A14M_04_analyze.py` | Full | Source/descendant contrasts and binary edges |
| `studies/02_controlled_source_relocation/support/a14m_common.py` | Targeted task construction, schemas, source/descendant edits, score ablations | Four-family/identifier structure and instrument |
| `studies/03_matched_unauthorized_comparison/support/N3_DISCRIMINANT_PREFREEZE_v1_2/N3_04_analyze.py` | Full | Endpoint versus joint action/context contrasts |
| Same N3 directory, `n3_common.py` | Targeted runtime/configuration checks | Serving preflight and source-bound reproduction |
| `studies/01_natural_relevance/support/A13.py` | Targeted taxonomy and label construction | Lexical coverage and workload selection |
| `studies/06_attriguard/support/N6_ATTRIGUARD_N3_TECH_AMENDMENT_v1_2/N6_03_paired_adapter.py` | Full | Forced candidate batching, synthetic tool behavior, scheduling |
| `studies/08_live_end_to_end/code_and_protocol/code/E2E_PRE_03_science_runner.py` | Full | Live runs, retries, observer, outcomes, recovery |
| Same directory, `e2e_attacks.py` | Full | Carrier serialization and injection bytes |
| `studies/07_causalarmor/support/P0B3_CAUSALARMOR_LIVE_v1/p0b3_live_common.py` | Targeted proxy scoring, boundary, sanitization/masking | Reconstruction fidelity |
| `third_party/integrations/AgentWatcher_armc_runtime_v1/agents/agentdojo/src/agentdojo/agent_pipeline/piarena_defense_adapter.py` | Targeted pipeline/assessed object, detection handling and retained history | Monitor contract and integration |
| Corresponding monitor `messages.py` | Targeted benign/injection prompt contract | Context detection versus action authorization |
| `studies/09_evaluation_replay/support/P2B_XM_CI_v1_2_ORACLE_PATCH_NO_SERVER_RERUN/action_local.py` and identical/related snapshots | Full core immediate-state comparison | Fidelity versus permission |
| Replay `p2b_common.py` snapshots | Targeted frozen continuation and role adaptation | Replay is not autonomous recovery |
| `scripts/reproduction/lib.sh`, relevant stages 05 and 09 | Full wrapper/stage inspection | Fresh/frozen paths, server context, copied products |
| `scripts/verification/verify_current_claims.py` | Targeted claim map and checks; supplied verifier invoked | Frozen arithmetic consistency, not semantic validity |

The CSV inventory gives exact member hashes and definition locations for deeper follow-up. Identical hash groups help distinguish copied code from genuinely different revisions.

## Unresolved evidence

- No `IEEE_SP_V5_CODE_2026-10-07.zip` supplied; v6's 95 tests, D24 fixtures, and fork implementation descriptions were not independently executed.
- No university-server/backend qualification, model diagnostic, adaptive attack, or fresh structural confirmation.
- No independent contract adjudication by two human reviewers in this audit; proposed review packets are not completed reviews.
- No causal claim from incident quotations, no incident defeat of a supposedly deployed causal grader, no general deployment prevalence.
- Native occurrence-binding behavior, autonomous reachability, natural reference contamination, and semantic validity of candidate forks remain research questions.
