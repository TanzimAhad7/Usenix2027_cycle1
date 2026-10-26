# IEEE_SP Project Tree

Generated: 2026-10-26T14:08:14Z
Root: `/home/tahad/IEEE_SP/IEEE_SP_2027`

## Contents

1. [Summary](#summary)
2. [Full tree (source, configs, docs, results metadata)](#full-tree)
3. [results/user_runs (run outputs, depth-limited)](#resultsuser_runs)

## Summary

```
Total entries (incl. venvs): 204678

   ENTRIES  PATH
     77275  results/
     10175  research_basis/
      2023  experiments/
      1098  validation/
       319  authorization_study/
       297  reconciled_study/
       182  expanded_gpu3/
       117  reference_discovery_parallel/
        77  s1_reference_study/
        76  logs/
        50  occurrence_study/
        47  targeted_gpu3/
        46  release_native_study/
        28  docs/
        18  reference_discovery_provenance/
        18  provenance/
        14  scripts/
        11  protocols/
         9  automation_gpu3/
         7  references/
         6  tests/
         4  reference_discovery_evidence/
         3  research_records/
         2  config/
     84213  .venv-serving/
     22851  .venv/
      5601  .tools/
        28  .git/
         3  .vscode/
```

Excluded from the full tree below (build/tooling artifacts): `.venv/`, `.venv-serving/`, `.tools/`, `.git/`.

## Full tree

Everything except `results/user_runs/` (listed separately in section 3).

```
.
|-- AGENTS.md
|-- ANALYZE_TARGETED_GPU3.sh*
|-- authorization_study/
|   |-- AGENTS.md
|   |-- analyze.py
|   |-- common.py
|   |-- contracts.py
|   |-- cpu.py
|   |-- engine.py
|   |-- historical/
|   |   |-- gemma/
|   |   |   |-- lawful_recovery/
|   |   |   |   |-- L3_M0/
|   |   |   |   |   |-- batch_000_before.json
|   |   |   |   |   |-- batch_000_result.json
|   |   |   |   |   |-- batch_001_before.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- http_001_reference.request.json
|   |   |   |   |   |-- http_001_reference.response.json
|   |   |   |   |   |-- http_001_reference.tokens.json
|   |   |   |   |   |-- http_001_reference.transport.json
|   |   |   |   |   |-- http_002_judge.request.json
|   |   |   |   |   |-- http_002_judge.response.json
|   |   |   |   |   |-- http_002_judge.tokens.json
|   |   |   |   |   |-- http_002_judge.transport.json
|   |   |   |   |   |-- http_003_judge.request.json
|   |   |   |   |   |-- http_003_judge.response.json
|   |   |   |   |   |-- http_003_judge.tokens.json
|   |   |   |   |   |-- http_003_judge.transport.json
|   |   |   |   |   |-- http_004_actor.request.json
|   |   |   |   |   |-- http_004_actor.response.json
|   |   |   |   |   |-- http_004_actor.tokens.json
|   |   |   |   |   |-- http_004_actor.transport.json
|   |   |   |   |   |-- lineage.json
|   |   |   |   |   |-- messages.json
|   |   |   |   |   |-- result.json
|   |   |   |   |   |-- selected_batch.json
|   |   |   |   |   `-- selected_checkpoint.json
|   |   |   |   |-- L3_M1/
|   |   |   |   |   |-- batch_000_before.json
|   |   |   |   |   |-- batch_000_result.json
|   |   |   |   |   |-- batch_001_before.json
|   |   |   |   |   |-- batch_001_result.json
|   |   |   |   |   |-- batch_002_before.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- http_001_reference.request.json
|   |   |   |   |   |-- http_001_reference.response.json
|   |   |   |   |   |-- http_001_reference.reused.json
|   |   |   |   |   |-- http_002_judge.request.json
|   |   |   |   |   |-- http_002_judge.response.json
|   |   |   |   |   |-- http_002_judge.reused.json
|   |   |   |   |   |-- http_003_judge.request.json
|   |   |   |   |   |-- http_003_judge.response.json
|   |   |   |   |   |-- http_003_judge.reused.json
|   |   |   |   |   |-- http_004_actor.request.json
|   |   |   |   |   |-- http_004_actor.response.json
|   |   |   |   |   |-- http_004_actor.tokens.json
|   |   |   |   |   |-- http_004_actor.transport.json
|   |   |   |   |   |-- http_005_reference.request.json
|   |   |   |   |   |-- http_005_reference.response.json
|   |   |   |   |   |-- http_005_reference.tokens.json
|   |   |   |   |   |-- http_005_reference.transport.json
|   |   |   |   |   |-- http_006_judge.request.json
|   |   |   |   |   |-- http_006_judge.response.json
|   |   |   |   |   |-- http_006_judge.tokens.json
|   |   |   |   |   |-- http_006_judge.transport.json
|   |   |   |   |   |-- http_007_actor.request.json
|   |   |   |   |   |-- http_007_actor.response.json
|   |   |   |   |   |-- http_007_actor.tokens.json
|   |   |   |   |   |-- http_007_actor.transport.json
|   |   |   |   |   |-- lineage.json
|   |   |   |   |   |-- messages.json
|   |   |   |   |   |-- result.json
|   |   |   |   |   |-- selected_batch.json
|   |   |   |   |   `-- selected_checkpoint.json
|   |   |   |   `-- L3_prefix/
|   |   |   |       |-- batch_000_before.json
|   |   |   |       |-- events.jsonl
|   |   |   |       |-- http_001_attenuator.request.json
|   |   |   |       |-- http_001_attenuator.response.json
|   |   |   |       |-- http_001_attenuator.tokens.json
|   |   |   |       |-- http_001_attenuator.transport.json
|   |   |   |       |-- http_002_attenuator.request.json
|   |   |   |       |-- http_002_attenuator.response.json
|   |   |   |       |-- http_002_attenuator.tokens.json
|   |   |   |       |-- http_002_attenuator.transport.json
|   |   |   |       |-- messages.json
|   |   |   |       |-- result.json
|   |   |   |       `-- selected_checkpoint.json
|   |   |   `-- workflows/
|   |   |       |-- gemma_p-before_i1_hostile_on/
|   |   |       |   |-- batch_000_before.json
|   |   |       |   |-- batch_000_result.json
|   |   |       |   |-- batch_001_before.json
|   |   |       |   |-- batch_001_result.json
|   |   |       |   |-- batch_002_before.json
|   |   |       |   |-- events.jsonl
|   |   |       |   |-- http_001_actor.request.json
|   |   |       |   |-- http_001_actor.response.json
|   |   |       |   |-- http_001_actor.tokens.json
|   |   |       |   |-- http_001_actor.transport.json
|   |   |       |   |-- http_002_attenuator.request.json
|   |   |       |   |-- http_002_attenuator.response.json
|   |   |       |   |-- http_002_attenuator.tokens.json
|   |   |       |   |-- http_002_attenuator.transport.json
|   |   |       |   |-- http_003_attenuator.request.json
|   |   |       |   |-- http_003_attenuator.response.json
|   |   |       |   |-- http_003_attenuator.tokens.json
|   |   |       |   |-- http_003_attenuator.transport.json
|   |   |       |   |-- http_004_actor.request.json
|   |   |       |   |-- http_004_actor.response.json
|   |   |       |   |-- http_004_actor.tokens.json
|   |   |       |   |-- http_004_actor.transport.json
|   |   |       |   |-- http_005_reference.request.json
|   |   |       |   |-- http_005_reference.response.json
|   |   |       |   |-- http_005_reference.tokens.json
|   |   |       |   |-- http_005_reference.transport.json
|   |   |       |   |-- http_006_actor.request.json
|   |   |       |   |-- http_006_actor.response.json
|   |   |       |   |-- http_006_actor.tokens.json
|   |   |       |   |-- http_006_actor.transport.json
|   |   |       |   |-- http_007_reference.request.json
|   |   |       |   |-- http_007_reference.response.json
|   |   |       |   |-- http_007_reference.tokens.json
|   |   |       |   |-- http_007_reference.transport.json
|   |   |       |   |-- http_008_actor.request.json
|   |   |       |   |-- http_008_actor.response.json
|   |   |       |   |-- http_008_actor.tokens.json
|   |   |       |   |-- http_008_actor.transport.json
|   |   |       |   |-- http_009_actor.request.json
|   |   |       |   |-- http_009_actor.response.json
|   |   |       |   |-- http_009_actor.tokens.json
|   |   |       |   |-- http_009_actor.transport.json
|   |   |       |   |-- messages.json
|   |   |       |   |-- result.json
|   |   |       |   |-- selected_batch.json
|   |   |       |   `-- selected_checkpoint.json
|   |   |       `-- gemma_p-before_i2_hostile_on/
|   |   |           |-- batch_000_before.json
|   |   |           |-- batch_000_result.json
|   |   |           |-- batch_001_before.json
|   |   |           |-- batch_001_result.json
|   |   |           |-- batch_002_before.json
|   |   |           |-- events.jsonl
|   |   |           |-- http_001_actor.request.json
|   |   |           |-- http_001_actor.response.json
|   |   |           |-- http_001_actor.tokens.json
|   |   |           |-- http_001_actor.transport.json
|   |   |           |-- http_002_attenuator.request.json
|   |   |           |-- http_002_attenuator.response.json
|   |   |           |-- http_002_attenuator.tokens.json
|   |   |           |-- http_002_attenuator.transport.json
|   |   |           |-- http_003_attenuator.request.json
|   |   |           |-- http_003_attenuator.response.json
|   |   |           |-- http_003_attenuator.tokens.json
|   |   |           |-- http_003_attenuator.transport.json
|   |   |           |-- http_004_actor.request.json
|   |   |           |-- http_004_actor.response.json
|   |   |           |-- http_004_actor.tokens.json
|   |   |           |-- http_004_actor.transport.json
|   |   |           |-- http_005_reference.request.json
|   |   |           |-- http_005_reference.response.json
|   |   |           |-- http_005_reference.tokens.json
|   |   |           |-- http_005_reference.transport.json
|   |   |           |-- http_006_actor.request.json
|   |   |           |-- http_006_actor.response.json
|   |   |           |-- http_006_actor.tokens.json
|   |   |           |-- http_006_actor.transport.json
|   |   |           |-- http_007_reference.request.json
|   |   |           |-- http_007_reference.response.json
|   |   |           |-- http_007_reference.tokens.json
|   |   |           |-- http_007_reference.transport.json
|   |   |           |-- http_008_actor.request.json
|   |   |           |-- http_008_actor.response.json
|   |   |           |-- http_008_actor.tokens.json
|   |   |           |-- http_008_actor.transport.json
|   |   |           |-- http_009_actor.request.json
|   |   |           |-- http_009_actor.response.json
|   |   |           |-- http_009_actor.tokens.json
|   |   |           |-- http_009_actor.transport.json
|   |   |           |-- messages.json
|   |   |           |-- result.json
|   |   |           |-- selected_batch.json
|   |   |           `-- selected_checkpoint.json
|   |   |-- PROVENANCE.json
|   |   `-- qwen/
|   |       `-- lawful_recovery/
|   |           |-- L3_M0/
|   |           |   |-- batch_000_before.json
|   |           |   |-- batch_000_result.json
|   |           |   |-- batch_001_before.json
|   |           |   |-- events.jsonl
|   |           |   |-- http_001_reference.request.json
|   |           |   |-- http_001_reference.response.json
|   |           |   |-- http_001_reference.tokens.json
|   |           |   |-- http_001_reference.transport.json
|   |           |   |-- http_002_judge.request.json
|   |           |   |-- http_002_judge.response.json
|   |           |   |-- http_002_judge.tokens.json
|   |           |   |-- http_002_judge.transport.json
|   |           |   |-- http_003_judge.request.json
|   |           |   |-- http_003_judge.response.json
|   |           |   |-- http_003_judge.tokens.json
|   |           |   |-- http_003_judge.transport.json
|   |           |   |-- http_004_actor.request.json
|   |           |   |-- http_004_actor.response.json
|   |           |   |-- http_004_actor.tokens.json
|   |           |   |-- http_004_actor.transport.json
|   |           |   |-- lineage.json
|   |           |   |-- messages.json
|   |           |   |-- result.json
|   |           |   |-- selected_batch.json
|   |           |   `-- selected_checkpoint.json
|   |           |-- L3_M1/
|   |           |   |-- batch_000_before.json
|   |           |   |-- batch_000_result.json
|   |           |   |-- batch_001_before.json
|   |           |   |-- batch_001_result.json
|   |           |   |-- batch_002_before.json
|   |           |   |-- events.jsonl
|   |           |   |-- http_001_reference.request.json
|   |           |   |-- http_001_reference.response.json
|   |           |   |-- http_001_reference.reused.json
|   |           |   |-- http_002_judge.request.json
|   |           |   |-- http_002_judge.response.json
|   |           |   |-- http_002_judge.reused.json
|   |           |   |-- http_003_judge.request.json
|   |           |   |-- http_003_judge.response.json
|   |           |   |-- http_003_judge.reused.json
|   |           |   |-- http_004_actor.request.json
|   |           |   |-- http_004_actor.response.json
|   |           |   |-- http_004_actor.tokens.json
|   |           |   |-- http_004_actor.transport.json
|   |           |   |-- http_005_reference.request.json
|   |           |   |-- http_005_reference.response.json
|   |           |   |-- http_005_reference.tokens.json
|   |           |   |-- http_005_reference.transport.json
|   |           |   |-- http_006_actor.request.json
|   |           |   |-- http_006_actor.response.json
|   |           |   |-- http_006_actor.tokens.json
|   |           |   |-- http_006_actor.transport.json
|   |           |   |-- lineage.json
|   |           |   |-- messages.json
|   |           |   |-- result.json
|   |           |   |-- selected_batch.json
|   |           |   `-- selected_checkpoint.json
|   |           `-- L3_prefix/
|   |               |-- batch_000_before.json
|   |               |-- events.jsonl
|   |               |-- http_001_attenuator.request.json
|   |               |-- http_001_attenuator.response.json
|   |               |-- http_001_attenuator.tokens.json
|   |               |-- http_001_attenuator.transport.json
|   |               |-- http_002_attenuator.request.json
|   |               |-- http_002_attenuator.response.json
|   |               |-- http_002_attenuator.tokens.json
|   |               |-- http_002_attenuator.transport.json
|   |               |-- messages.json
|   |               |-- result.json
|   |               `-- selected_checkpoint.json
|   |-- __init__.py
|   |-- interventions.py
|   |-- legacy_protocol.py
|   |-- observer.py
|   |-- protocol.py
|   |-- PROVENANCE.md
|   |-- __pycache__/
|   |   |-- analyze.cpython-312.pyc
|   |   |-- common.cpython-312.pyc
|   |   |-- contracts.cpython-312.pyc
|   |   |-- cpu.cpython-312.pyc
|   |   |-- engine.cpython-312.pyc
|   |   |-- __init__.cpython-312.pyc
|   |   |-- interventions.cpython-312.pyc
|   |   |-- legacy_protocol.cpython-312.pyc
|   |   |-- observer.cpython-312.pyc
|   |   |-- protocol.cpython-312.pyc
|   |   |-- qualification.cpython-312.pyc
|   |   |-- replay.cpython-312.pyc
|   |   |-- runner.cpython-312.pyc
|   |   |-- sequence.cpython-312.pyc
|   |   |-- session.cpython-312.pyc
|   |   |-- study.cpython-312.pyc
|   |   |-- transport.cpython-312.pyc
|   |   `-- world.cpython-312.pyc
|   |-- qualification.py
|   |-- replay.py
|   |-- requirements.lock.txt
|   |-- runner.py
|   |-- sequence.py
|   |-- session.py
|   |-- study.py
|   |-- tests/
|   |   |-- fixtures.py
|   |   |-- __init__.py
|   |   `-- test_campaign.py
|   |-- transport.py
|   |-- validation/
|   |   |-- BUILD_VALIDATION.md
|   |   |-- campaign_tests.log
|   |   |-- controller_cpu_only_scope.json
|   |   |-- controller_cpu_only_status.json
|   |   |-- cpu_qualification_raw.tar.gz
|   |   |-- qualification.log
|   |   |-- qualification_summary.json
|   |   `-- resource_preflight_test.log
|   |-- vendor/
|   |   |-- AttriGuard.py
|   |   |-- __init__.py
|   |   |-- protocol.py
|   |   |-- PROVENANCE.md
|   |   |-- __pycache__/
|   |   |   |-- __init__.cpython-312.pyc
|   |   |   |-- protocol.cpython-312.pyc
|   |   |   |-- qualify_gpu.cpython-312.pyc
|   |   |   `-- serving_helpers.cpython-312.pyc
|   |   |-- qualify_gpu.py
|   |   |-- scheduling.json
|   |   |-- SELECTION_PROVENANCE.json
|   |   `-- serving_helpers.py
|   `-- world.py
|-- automation_gpu3/
|   |-- diagnostic_runner.py
|   |-- PACKAGE_SHA256.json
|   |-- README.md
|   |-- sequence.py
|   |-- test_automation.py
|   `-- validation/
|       |-- CPU_MOCK_TESTS.log
|       `-- VALIDATION.json
|-- config/
|   `-- README.md
|-- docs/
|   |-- AUTHORITY_RECONCILIATION.json
|   |-- Checkpoint_Restoration_Repair.md
|   |-- DEFENSIBILITY_GAPS.md
|   |-- DEPENDENCY_AUDIT.md
|   |-- External_Critical_Review.md
|   |-- FOUNDATION.md
|   |-- IEEE_SP_Next_Experiment_Reconciled_Design.md
|   |-- IEEE_SP_Parallel_Reference_Experiment_Design.md
|   |-- IEEE_SP_S1_Reference_Admission_Experiment_Design.md
|   |-- INDEPENDENT_CRITIQUE.md
|   |-- INHERITED_CLAIMS.csv
|   |-- PLAN_COVERAGE.csv
|   |-- program/
|   |   |-- EVIDENCE_GATES.md
|   |   |-- MODULE_REGISTRY.json
|   |   |-- PAPER_EVIDENCE_MAP.md
|   |   |-- PROTOCOLS_README.md
|   |   |-- RESEARCH_WORK_PROGRAM.md
|   |   `-- REVIEWER_TO_EXPERIMENT_MATRIX.csv
|   |-- PUBLISHED_ATTRIGUARD_PROVENANCE.json
|   |-- REPRODUCTION_STATUS.md
|   |-- RESEARCH_BACKGROUND.md
|   |-- RESEARCH_PLAN.md
|   |-- REVIEWER_OBLIGATIONS.csv
|   |-- SCIENTIFIC_REDESIGN.md
|   |-- Template_Preflight_Repair.md
|   `-- WORK_PRODUCTS.csv
|-- expanded_gpu3/
|   |-- components.py
|   |-- guards.py
|   |-- protocol.py
|   |-- __pycache__/
|   |   |-- guards.cpython-312.pyc
|   |   |-- protocol.cpython-312.pyc
|   |   |-- transport.cpython-312.pyc
|   |   `-- world.cpython-312.pyc
|   |-- README.md
|   |-- REVIEWABLE_PROTOCOL.json
|   |-- runner.py
|   |-- sequence.py
|   |-- test_expanded.py
|   |-- transport.py
|   |-- validation/
|   |   |-- ENGINEERING_TESTS.log
|   |   |-- native_components/
|   |   |   |-- aggregate_clean__capacity_and_grant/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- aggregate_clean__grant_gate/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- aggregate_clean__reference_capacity/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- atomic_split__baseline/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- atomic_split__capacity_and_grant/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- atomic_split__grant_gate/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- atomic_split__reference_capacity/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- blocked_predecessor__baseline/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- blocked_predecessor__grant_gate/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- blocked_predecessor__r_continuity/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- generated/
|   |   |   |   |-- baseline.diff
|   |   |   |   |-- capacity_and_grant.diff
|   |   |   |   |-- exact_counter.diff
|   |   |   |   |-- grant_gate.diff
|   |   |   |   |-- guard_baseline.py
|   |   |   |   |-- guard_capacity_and_grant.py
|   |   |   |   |-- guard_exact_counter.py
|   |   |   |   |-- guard_grant_gate.py
|   |   |   |   |-- guard_judge_strict.py
|   |   |   |   |-- guard_r_continuity.py
|   |   |   |   |-- guard_reference_capacity.py
|   |   |   |   |-- judge_strict.diff
|   |   |   |   |-- r_continuity.diff
|   |   |   |   `-- reference_capacity.diff
|   |   |   |-- identical_signature_duplicate__baseline/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- identical_signature_duplicate__exact_counter/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- identical_signature_duplicate__reference_capacity/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- optional_default_duplicate__baseline/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- optional_default_duplicate__capacity_and_grant/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- optional_default_duplicate__exact_counter/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- optional_default_duplicate__grant_gate/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- optional_default_duplicate__judge_strict/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- optional_default_duplicate__r_continuity/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- optional_default_duplicate__reference_capacity/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- results.json
|   |   |   |-- safe_retry__capacity_and_grant/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- safe_retry__grant_gate/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- safe_retry__reference_capacity/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- spent_duplicate__capacity_and_grant/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- spent_duplicate__grant_gate/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- spent_duplicate__reference_capacity/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- status.json
|   |   |   |-- two_clean__capacity_and_grant/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   |-- two_clean__grant_gate/
|   |   |   |   |-- effects.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- messages.json
|   |   |   |   `-- result.json
|   |   |   `-- two_clean__reference_capacity/
|   |   |       |-- effects.json
|   |   |       |-- events.jsonl
|   |   |       |-- messages.json
|   |   |       `-- result.json
|   |   `-- VALIDATION.json
|   `-- world.py
|-- experiments/
|   `-- review_binding/
|       |-- attestation.example.json
|       |-- autonomous.py
|       |-- diagnostic.py
|       |-- docs/
|       |   |-- FULL_PAPER_READING.md
|       |   |-- PROTOCOL.md
|       |   `-- reading_coverage.json
|       |-- evidence/
|       |   |-- bundled_source_comparison.json
|       |   |-- component_run/
|       |   |   |-- B_duplicate_one_reference__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- checks.json
|       |   |   |-- environment.json
|       |   |   |-- generated/
|       |   |   |   |-- b_occurrence.diff
|       |   |   |   |-- guard_b_occurrence.py
|       |   |   |   |-- guard_original.py
|       |   |   |   |-- guard_placebo.py
|       |   |   |   |-- guard_r_all_errors.py
|       |   |   |   |-- guard_r_minimal.py
|       |   |   |   |-- original.diff
|       |   |   |   |-- placebo.diff
|       |   |   |   |-- r_all_errors.diff
|       |   |   |   `-- r_minimal.diff
|       |   |   |-- R_blocked_skip_disabled__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- results.csv
|       |   |   |-- results.json
|       |   |   |-- R_prior_allowed_empty__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   `-- runtime_sources.json
|       |   |-- component_run_with_controls/
|       |   |   |-- B_duplicate_one_reference__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- checks.json
|       |   |   |-- environment.json
|       |   |   |-- generated/
|       |   |   |   |-- b_occurrence.diff
|       |   |   |   |-- guard_b_occurrence.py
|       |   |   |   |-- guard_original.py
|       |   |   |   |-- guard_placebo.py
|       |   |   |   |-- guard_r_all_errors.py
|       |   |   |   |-- guard_r_minimal.py
|       |   |   |   |-- original.diff
|       |   |   |   |-- placebo.diff
|       |   |   |   |-- r_all_errors.diff
|       |   |   |   `-- r_minimal.diff
|       |   |   |-- R_blocked_skip_disabled__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- results.csv
|       |   |   |-- results.json
|       |   |   |-- R_prior_allowed_empty__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   `-- runtime_sources.json
|       |   |-- development_record.md
|       |   |-- final_component_run/
|       |   |   |-- B_duplicate_one_reference__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- checks.json
|       |   |   |-- environment.json
|       |   |   |-- generated/
|       |   |   |   |-- b_occurrence.diff
|       |   |   |   |-- guard_b_occurrence.py
|       |   |   |   |-- guard_original.py
|       |   |   |   |-- guard_placebo.py
|       |   |   |   |-- guard_r_all_errors.py
|       |   |   |   |-- guard_r_minimal.py
|       |   |   |   |-- original.diff
|       |   |   |   |-- placebo.diff
|       |   |   |   |-- r_all_errors.diff
|       |   |   |   `-- r_minimal.diff
|       |   |   |-- R_blocked_skip_disabled__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- results.csv
|       |   |   |-- results.json
|       |   |   |-- R_prior_allowed_empty__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   `-- runtime_sources.json
|       |   |-- final_unit_tests.log
|       |   |-- gemma_backend/
|       |   |   `-- backend.json
|       |   |-- human_review_template.csv
|       |   |-- qualified_component_run/
|       |   |   |-- B_duplicate_one_reference__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_one_reference__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_two_references_one_grant__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_duplicate_with_independent_gate__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_idempotent_retry__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_one_legal__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_two_legal_two_references__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__b_occurrence__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__b_occurrence__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- B_wrong_recipient__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- checks.json
|       |   |   |-- environment.json
|       |   |   |-- generated/
|       |   |   |   |-- b_occurrence.diff
|       |   |   |   |-- guard_b_occurrence.py
|       |   |   |   |-- guard_original.py
|       |   |   |   |-- guard_placebo.py
|       |   |   |   |-- guard_r_all_errors.py
|       |   |   |   |-- guard_r_minimal.py
|       |   |   |   |-- original.diff
|       |   |   |   |-- placebo.diff
|       |   |   |   |-- r_all_errors.diff
|       |   |   |   `-- r_minimal.diff
|       |   |   |-- R_blocked_skip_disabled__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_blocked_skip_disabled__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- results.csv
|       |   |   |-- results.json
|       |   |   |-- R_prior_allowed_empty__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_empty__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed_error__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_allowed__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_prior_blocked_with_independent_gate__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__original__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__original__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__placebo__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__placebo__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__r_all_errors__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__r_all_errors__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__r_minimal__exact/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   |-- R_skip_branch_error_chain__r_minimal__fuzzy/
|       |   |   |   |-- case.json
|       |   |   |   |-- events.jsonl
|       |   |   |   |-- messages.json
|       |   |   |   `-- result.json
|       |   |   `-- runtime_sources.json
|       |   |-- qwen_backend/
|       |   |   `-- backend.json
|       |   |-- runtime_snapshot_comparison.json
|       |   `-- unit_tests.log
|       |-- FINDINGS.md
|       |-- __pycache__/
|       |   |-- autonomous.cpython-312.pyc
|       |   `-- diagnostic.cpython-312.pyc
|       |-- README.md
|       |-- requirements.lock.txt
|       |-- tests/
|       |   |-- __pycache__/
|       |   |   |-- test_diagnostic.cpython-312.pyc
|       |   |   `-- test_transport.cpython-312.pyc
|       |   |-- test_diagnostic.py
|       |   `-- test_transport.py
|       `-- vendor/
|           |-- AttriGuard.py
|           `-- PROVENANCE.md
|-- FROZEN_PROTOCOL.json
|-- .gitignore
|-- IEEE_SP_2027.code-workspace
|-- IEEE_SP_Authorization_Recovery_GPU3_Full.zip
|-- IEEE_SP_Final_Experiment_Design.md
|-- IEEE_SP_Native_Release_GPU3_Full.zip
|-- IEEE_SP_Occurrence_Study_GPU3_Fresh.zip
|-- IEEE_SP_Occurrence_Study_GPU3.zip
|-- IEEE_SP_Parallel_Reference_GPU23_Fixed.zip
|-- IEEE_SP_Parallel_Reference_GPU23_Preflight_Fixed.zip
|-- IEEE_SP_Parallel_Reference_GPU23.zip
|-- IEEE_SP_Reconciled_Experiment_GPU3_Full.zip
|-- IEEE_SP_S1_Reference_GPU3_Complete.zip
|-- IEEE_SP_Standalone_Research_Authority_Current.md
|-- IEEE_SP_V6_4_Experiment.zip
|-- IMPLEMENTATION_NOTES.md
|-- INIT_LOCAL_GIT.sh*
|-- INTEGRATION_DECISIONS.md
|-- LAUNCH.sh*
|-- logs/
|   |-- authorization_gpu3_20261023T221414Z_2619402_23755.log
|   |-- authorization_gpu3_20261023T221414Z_2619402_23755.pid
|   |-- authorization_gpu3_20261023T221414Z_2619402_23755.status
|   |-- components_01.log
|   |-- components_01.pid
|   |-- components_01.status
|   |-- expanded_gpu3_20261020T224703Z_517128.log
|   |-- expanded_gpu3_20261020T224703Z_517128.pid
|   |-- expanded_gpu3_20261020T224703Z_517128.status
|   |-- fix_ninja_20261020T042901Z.log
|   |-- fix_ninja_20261020T043347Z.log
|   |-- gpu3_check_20261020T002135Z_517617.log
|   |-- gpu3_check_20261020T002135Z_517617.pid
|   |-- gpu3_sequence_20261020T040635Z_1989750.log
|   |-- gpu3_sequence_20261020T040635Z_1989750.pid
|   |-- gpu3_sequence_20261020T040635Z_1989750.status
|   |-- gpu3_sequence_20261020T041603Z_2051143.log
|   |-- gpu3_sequence_20261020T041603Z_2051143.pid
|   |-- gpu3_sequence_20261020T041603Z_2051143.status
|   |-- gpu3_sequence_20261020T042902Z_2146327.log
|   |-- gpu3_sequence_20261020T042902Z_2146327.pid
|   |-- gpu3_sequence_20261020T042902Z_2146327.status
|   |-- gpu3_sequence_20261020T043349Z_2177718.log
|   |-- gpu3_sequence_20261020T043349Z_2177718.pid
|   |-- gpu3_sequence.lock
|   |-- historical_01.log
|   |-- historical_01.pid
|   |-- historical_01.status
|   |-- native_release_gpu3_20261025T005833Z_2622163_28698.log
|   |-- native_release_gpu3_20261025T005833Z_2622163_28698.log.pid
|   |-- native_release_gpu3_20261025T005833Z_2622163_28698.status
|   |-- occurrence_fresh_gpu3_20261023T030845Z_3250532.log
|   |-- occurrence_fresh_gpu3_20261023T030845Z_3250532.pid
|   |-- occurrence_fresh_gpu3_20261023T030845Z_3250532.status
|   |-- occurrence_gpu3_20261023T004740Z_2853755.log
|   |-- occurrence_gpu3_20261023T004740Z_2853755.pid
|   |-- occurrence_gpu3_20261023T004740Z_2853755.status
|   |-- parallel_reference_gpu23_20261026T045504Z_3579822_22634.log
|   |-- parallel_reference_gpu23_20261026T045504Z_3579822_22634.log.pid
|   |-- parallel_reference_gpu23_20261026T045504Z_3579822_22634.status
|   |-- parallel_reference_gpu23_20261026T130619Z_946797_7302.log
|   |-- parallel_reference_gpu23_20261026T130619Z_946797_7302.log.pid
|   |-- parallel_reference_gpu23_20261026T130619Z_946797_7302.status
|   |-- parallel_reference_gpu23_20261026T131613Z_976131_28637.log
|   |-- parallel_reference_gpu23_20261026T131613Z_976131_28637.log.pid
|   |-- parallel_reference_gpu23_20261026T131613Z_976131_28637.status
|   |-- parallel_reference_gpu23_20261026T133503Z_1032615_10605.log
|   |-- parallel_reference_gpu23_20261026T133503Z_1032615_10605.log.pid
|   |-- parallel_reference_gpu23_20261026T133503Z_1032615_10605_qwen.log
|   |-- protocols_01.log
|   |-- protocols_01.pid
|   |-- protocols_01.status
|   |-- reconciled_gpu3_20261024T044259Z_2440506_28345.log
|   |-- reconciled_gpu3_20261024T044259Z_2440506_28345.log.pid
|   |-- reconciled_gpu3_20261024T044259Z_2440506_28345.status
|   |-- s1_reference_gpu3_20261025T173651Z_1528393_1266.log
|   |-- s1_reference_gpu3_20261025T173651Z_1528393_1266.log.pid
|   |-- s1_reference_gpu3_20261025T173651Z_1528393_1266.status
|   |-- serving_setup_20261019T234011Z_250253.log
|   |-- serving_setup_20261019T234011Z_250253.packages.txt
|   |-- serving_setup_20261019T234011Z_250253.pid
|   |-- serving_setup_20261019T234011Z_250253.status
|   |-- setup_01.log
|   |-- setup_01.pid
|   |-- setup_01.status
|   |-- targeted_gpu3_20261021T055714Z_3261043.log
|   |-- targeted_gpu3_20261021T055714Z_3261043.pid
|   |-- targeted_gpu3_20261021T055714Z_3261043.status
|   |-- targeted_gpu3_20261022T213519Z_2309383.log
|   |-- targeted_gpu3_20261022T213519Z_2309383.pid
|   |-- targeted_gpu3_20261022T213519Z_2309383.status
|   |-- venv_bootstrap_20261019T232859Z_176395.log
|   |-- venv_bootstrap_20261019T232859Z_176395.log.pid
|   |-- venv_complete_20261019T232859Z_176398.packages.txt
|   `-- venv_complete_20261019T232859Z_176398.status
|-- NATIVE_PACKAGE_MANIFEST.json
|-- NEAREST_WORK_CHECK.md
|-- OCCURRENCE_PACKAGE_MANIFEST.json
|-- occurrence_study/
|   |-- analyze.py
|   |-- common.py
|   |-- cpu.py
|   |-- engine.py
|   |-- __init__.py
|   |-- interventions.py
|   |-- observer.py
|   |-- protocol.py
|   |-- __pycache__/
|   |   |-- analyze.cpython-312.pyc
|   |   |-- common.cpython-312.pyc
|   |   |-- cpu.cpython-312.pyc
|   |   |-- engine.cpython-312.pyc
|   |   |-- __init__.cpython-312.pyc
|   |   |-- interventions.cpython-312.pyc
|   |   |-- observer.cpython-312.pyc
|   |   |-- protocol.cpython-312.pyc
|   |   |-- sequence.cpython-312.pyc
|   |   |-- study.cpython-312.pyc
|   |   |-- transport.cpython-312.pyc
|   |   `-- world.cpython-312.pyc
|   |-- requirements.lock.txt
|   |-- sequence.py
|   |-- study.py
|   |-- tests/
|   |   |-- __init__.py
|   |   `-- test_study.py
|   |-- transport.py
|   |-- validation/
|   |   |-- BUILD_VALIDATION.md
|   |   |-- cpu.log
|   |   |-- cpu_raw_evidence.tar.gz
|   |   |-- cpu_summary.json
|   |   `-- engineering_tests.log
|   |-- vendor/
|   |   |-- AttriGuard.py
|   |   |-- __init__.py
|   |   |-- protocol.py
|   |   |-- PROVENANCE.md
|   |   |-- __pycache__/
|   |   |   |-- __init__.cpython-312.pyc
|   |   |   |-- protocol.cpython-312.pyc
|   |   |   |-- qualify_gpu.cpython-312.pyc
|   |   |   `-- serving_helpers.cpython-312.pyc
|   |   |-- qualify_gpu.py
|   |   |-- scheduling.json
|   |   |-- SELECTION_PROVENANCE.json
|   |   `-- serving_helpers.py
|   `-- world.py
|-- PACKAGE_MANIFEST.json
|-- PACKAGE_SHA256SUMS.txt
|-- PARALLEL_REFERENCE_FROZEN_MANIFEST.json
|-- PARALLEL_REFERENCE_MODEL_MANIFEST.json
|-- PARALLEL_REFERENCE_PACKAGE_MANIFEST.json
|-- PROJECT_TREE.md
|-- PROTOCOL_OCCURRENCE.md
|-- protocols/
|   |-- claim_memo.md
|   |-- confirmation.template.json
|   |-- NATIVE_RELEASE_MANIFEST.json
|   |-- NATIVE_TASKS.json
|   `-- proposed/
|       |-- A64.json
|       |-- D24.json
|       |-- H24.json
|       |-- H64.json
|       `-- S128.json
|-- provenance/
|   |-- CONSOLIDATION.json
|   |-- independent_audit/
|   |   |-- artifact_inventory.csv
|   |   |-- audit_results.json
|   |   |-- code_content_groups.json
|   |   |-- frozen_verification.log
|   |   |-- independent_audit.py
|   |   |-- raw_zip_integrity.json
|   |   |-- reading_and_code_coverage.md
|   |   |-- README.md
|   |   `-- source_manifest.json
|   |-- LITERATURE_FILES.csv
|   |-- PLAN_AUDIT_COVERAGE.json
|   |-- PLAN_PATH_REFERENCES.csv
|   |-- SELECTION_SUMMARY.json
|   |-- SOURCE_AVAILABILITY.json
|   `-- USENIX_SELECTION.csv
|-- README_AUTHORIZATION.md
|-- README.md
|-- README_NATIVE_RELEASE.md
|-- README_OCCURRENCE.md
|-- README_PARALLEL_REFERENCE.md
|-- README_RECONCILED.md
|-- README_S1_REFERENCE.md
|-- RECONCILED_PACKAGE_MANIFEST.json
|-- reconciled_study/
|   |-- AGENTS.md
|   |-- analysis.py
|   |-- assets/
|   |   |-- E0_EQUIVALENCE_REQUIREMENTS.json
|   |   |-- E3_INPUT_EQUIVALENCE_SPEC.json
|   |   |-- historical_decisive_traces/
|   |   |   |-- qwen_A-P10_arm0/
|   |   |   |   |-- batch_000_result.json
|   |   |   |   |-- batch_001_result.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- generated_guard.py
|   |   |   |   |-- http_001_actor.request.json
|   |   |   |   |-- http_001_actor.response.json
|   |   |   |   |-- http_001_actor.tokens.json
|   |   |   |   |-- http_001_actor.transport.json
|   |   |   |   |-- http_002_attenuator.request.json
|   |   |   |   |-- http_002_attenuator.response.json
|   |   |   |   |-- http_002_attenuator.tokens.json
|   |   |   |   |-- http_002_attenuator.transport.json
|   |   |   |   |-- http_003_attenuator.request.json
|   |   |   |   |-- http_003_attenuator.response.json
|   |   |   |   |-- http_003_attenuator.tokens.json
|   |   |   |   |-- http_003_attenuator.transport.json
|   |   |   |   |-- http_004_actor.request.json
|   |   |   |   |-- http_004_actor.response.json
|   |   |   |   |-- http_004_actor.tokens.json
|   |   |   |   |-- http_004_actor.transport.json
|   |   |   |   |-- http_005_reference.request.json
|   |   |   |   |-- http_005_reference.response.json
|   |   |   |   |-- http_005_reference.tokens.json
|   |   |   |   |-- http_005_reference.transport.json
|   |   |   |   |-- http_006_judge.request.json
|   |   |   |   |-- http_006_judge.response.json
|   |   |   |   |-- http_006_judge.tokens.json
|   |   |   |   |-- http_006_judge.transport.json
|   |   |   |   |-- http_007_judge.request.json
|   |   |   |   |-- http_007_judge.response.json
|   |   |   |   |-- http_007_judge.tokens.json
|   |   |   |   |-- http_007_judge.transport.json
|   |   |   |   |-- http_008_actor.request.json
|   |   |   |   |-- http_008_actor.response.json
|   |   |   |   |-- http_008_actor.tokens.json
|   |   |   |   |-- http_008_actor.transport.json
|   |   |   |   |-- http_009_reference.request.json
|   |   |   |   |-- http_009_reference.response.json
|   |   |   |   |-- http_009_reference.tokens.json
|   |   |   |   |-- http_009_reference.transport.json
|   |   |   |   |-- http_010_actor.request.json
|   |   |   |   |-- http_010_actor.response.json
|   |   |   |   |-- http_010_actor.tokens.json
|   |   |   |   |-- http_010_actor.transport.json
|   |   |   |   |-- messages.json
|   |   |   |   |-- native.log
|   |   |   |   |-- proposal_000_before.json
|   |   |   |   |-- proposal_001_before.json
|   |   |   |   |-- proposal_002_before.json
|   |   |   |   |-- proposal_003_before.json
|   |   |   |   |-- result.json
|   |   |   |   |-- selected_batch.json
|   |   |   |   |-- selected_checkpoint.json
|   |   |   |   |-- slot_status.json
|   |   |   |   `-- source_changes.diff
|   |   |   `-- qwen_A-P17_arm0/
|   |   |       |-- batch_000_result.json
|   |   |       |-- events.jsonl
|   |   |       |-- generated_guard.py
|   |   |       |-- http_001_actor.request.json
|   |   |       |-- http_001_actor.response.json
|   |   |       |-- http_001_actor.tokens.json
|   |   |       |-- http_001_actor.transport.json
|   |   |       |-- http_002_attenuator.request.json
|   |   |       |-- http_002_attenuator.response.json
|   |   |       |-- http_002_attenuator.tokens.json
|   |   |       |-- http_002_attenuator.transport.json
|   |   |       |-- http_003_attenuator.request.json
|   |   |       |-- http_003_attenuator.response.json
|   |   |       |-- http_003_attenuator.tokens.json
|   |   |       |-- http_003_attenuator.transport.json
|   |   |       |-- http_004_actor.request.json
|   |   |       |-- http_004_actor.response.json
|   |   |       |-- http_004_actor.tokens.json
|   |   |       |-- http_004_actor.transport.json
|   |   |       |-- http_005_reference.request.json
|   |   |       |-- http_005_reference.response.json
|   |   |       |-- http_005_reference.tokens.json
|   |   |       |-- http_005_reference.transport.json
|   |   |       |-- http_006_judge.request.json
|   |   |       |-- http_006_judge.response.json
|   |   |       |-- http_006_judge.tokens.json
|   |   |       |-- http_006_judge.transport.json
|   |   |       |-- http_007_judge.request.json
|   |   |       |-- http_007_judge.response.json
|   |   |       |-- http_007_judge.tokens.json
|   |   |       |-- http_007_judge.transport.json
|   |   |       |-- http_008_actor.request.json
|   |   |       |-- http_008_actor.response.json
|   |   |       |-- http_008_actor.tokens.json
|   |   |       |-- http_008_actor.transport.json
|   |   |       |-- messages.json
|   |   |       |-- native.log
|   |   |       |-- proposal_000_before.json
|   |   |       |-- proposal_001_before.json
|   |   |       |-- proposal_002_before.json
|   |   |       |-- result.json
|   |   |       |-- selected_batch.json
|   |   |       |-- selected_checkpoint.json
|   |   |       |-- slot_status.json
|   |   |       `-- source_changes.diff
|   |   |-- historical_L3/
|   |   |   |-- gemma/
|   |   |   |   |-- batch_000_result.json
|   |   |   |   |-- http_001_reference.request.json
|   |   |   |   |-- http_001_reference.response.json
|   |   |   |   |-- http_001_reference.reused.json
|   |   |   |   |-- http_002_judge.request.json
|   |   |   |   |-- http_002_judge.response.json
|   |   |   |   |-- http_002_judge.reused.json
|   |   |   |   |-- http_003_judge.request.json
|   |   |   |   |-- http_003_judge.response.json
|   |   |   |   |-- http_003_judge.reused.json
|   |   |   |   `-- lineage.json
|   |   |   `-- qwen/
|   |   |       |-- batch_000_result.json
|   |   |       |-- http_001_reference.request.json
|   |   |       |-- http_001_reference.response.json
|   |   |       |-- http_001_reference.reused.json
|   |   |       |-- http_002_judge.request.json
|   |   |       |-- http_002_judge.response.json
|   |   |       |-- http_002_judge.reused.json
|   |   |       |-- http_003_judge.request.json
|   |   |       |-- http_003_judge.response.json
|   |   |       |-- http_003_judge.reused.json
|   |   |       `-- lineage.json
|   |   |-- initial_tapes/
|   |   |   |-- gemma_O96_L3/
|   |   |   |   |-- http_001_reference.request.json
|   |   |   |   |-- http_001_reference.response.json
|   |   |   |   |-- http_001_reference.tokens.json
|   |   |   |   |-- http_001_reference.transport.json
|   |   |   |   |-- http_002_judge.request.json
|   |   |   |   |-- http_002_judge.response.json
|   |   |   |   |-- http_002_judge.tokens.json
|   |   |   |   |-- http_002_judge.transport.json
|   |   |   |   |-- http_003_judge.request.json
|   |   |   |   |-- http_003_judge.response.json
|   |   |   |   |-- http_003_judge.tokens.json
|   |   |   |   `-- http_003_judge.transport.json
|   |   |   |-- gemma_R10_POLICY_M0_T0_Va0_Vr0_G0/
|   |   |   |   |-- http_001_reference.request.json
|   |   |   |   |-- http_001_reference.response.json
|   |   |   |   |-- http_001_reference.reused.json
|   |   |   |   |-- http_002_judge.request.json
|   |   |   |   |-- http_002_judge.response.json
|   |   |   |   |-- http_002_judge.reused.json
|   |   |   |   |-- http_003_judge.request.json
|   |   |   |   |-- http_003_judge.response.json
|   |   |   |   `-- http_003_judge.reused.json
|   |   |   |-- gemma_R17_POLICY_M0_T0_Va0_Vr0_G0/
|   |   |   |   |-- http_001_reference.request.json
|   |   |   |   |-- http_001_reference.response.json
|   |   |   |   |-- http_001_reference.reused.json
|   |   |   |   |-- http_002_judge.request.json
|   |   |   |   |-- http_002_judge.response.json
|   |   |   |   |-- http_002_judge.reused.json
|   |   |   |   |-- http_003_judge.request.json
|   |   |   |   |-- http_003_judge.response.json
|   |   |   |   `-- http_003_judge.reused.json
|   |   |   |-- qwen_A-P10_arm0/
|   |   |   |   |-- http_005_reference.request.json
|   |   |   |   |-- http_005_reference.response.json
|   |   |   |   |-- http_005_reference.tokens.json
|   |   |   |   |-- http_005_reference.transport.json
|   |   |   |   |-- http_006_judge.request.json
|   |   |   |   |-- http_006_judge.response.json
|   |   |   |   |-- http_006_judge.tokens.json
|   |   |   |   |-- http_006_judge.transport.json
|   |   |   |   |-- http_007_judge.request.json
|   |   |   |   |-- http_007_judge.response.json
|   |   |   |   |-- http_007_judge.tokens.json
|   |   |   |   `-- http_007_judge.transport.json
|   |   |   |-- qwen_A-P17_arm0/
|   |   |   |   |-- http_005_reference.request.json
|   |   |   |   |-- http_005_reference.response.json
|   |   |   |   |-- http_005_reference.tokens.json
|   |   |   |   |-- http_005_reference.transport.json
|   |   |   |   |-- http_006_judge.request.json
|   |   |   |   |-- http_006_judge.response.json
|   |   |   |   |-- http_006_judge.tokens.json
|   |   |   |   |-- http_006_judge.transport.json
|   |   |   |   |-- http_007_judge.request.json
|   |   |   |   |-- http_007_judge.response.json
|   |   |   |   |-- http_007_judge.tokens.json
|   |   |   |   `-- http_007_judge.transport.json
|   |   |   |-- qwen_O96_L3/
|   |   |   |   |-- http_001_reference.request.json
|   |   |   |   |-- http_001_reference.response.json
|   |   |   |   |-- http_001_reference.tokens.json
|   |   |   |   |-- http_001_reference.transport.json
|   |   |   |   |-- http_002_judge.request.json
|   |   |   |   |-- http_002_judge.response.json
|   |   |   |   |-- http_002_judge.tokens.json
|   |   |   |   |-- http_002_judge.transport.json
|   |   |   |   |-- http_003_judge.request.json
|   |   |   |   |-- http_003_judge.response.json
|   |   |   |   |-- http_003_judge.tokens.json
|   |   |   |   `-- http_003_judge.transport.json
|   |   |   |-- qwen_R10_POLICY_M0_T0_Va0_Vr0_G0/
|   |   |   |   |-- http_001_reference.request.json
|   |   |   |   |-- http_001_reference.response.json
|   |   |   |   |-- http_001_reference.reused.json
|   |   |   |   |-- http_002_judge.request.json
|   |   |   |   |-- http_002_judge.response.json
|   |   |   |   |-- http_002_judge.reused.json
|   |   |   |   |-- http_003_judge.request.json
|   |   |   |   |-- http_003_judge.response.json
|   |   |   |   `-- http_003_judge.reused.json
|   |   |   `-- qwen_R17_POLICY_M0_T0_Va0_Vr0_G0/
|   |   |       |-- http_001_reference.request.json
|   |   |       |-- http_001_reference.response.json
|   |   |       |-- http_001_reference.reused.json
|   |   |       |-- http_002_judge.request.json
|   |   |       |-- http_002_judge.response.json
|   |   |       |-- http_002_judge.reused.json
|   |   |       |-- http_003_judge.request.json
|   |   |       |-- http_003_judge.response.json
|   |   |       `-- http_003_judge.reused.json
|   |   |-- NEXT_EXPERIMENT_ALLOCATION.json
|   |   |-- parents.json
|   |   |-- PROFILE_QUALIFICATION_SPEC.json
|   |   |-- REPEAT_SELECTION_RULE.json
|   |   |-- roots.json
|   |   `-- TRUSTED_LEDGER_SPEC.json
|   |-- cpu.py
|   |-- execution.py
|   |-- graphs.py
|   |-- __init__.py
|   |-- legacy_a/
|   |   |-- common.py
|   |   |-- contracts.py
|   |   |-- engine.py
|   |   |-- __init__.py
|   |   |-- interventions.py
|   |   |-- observer.py
|   |   |-- __pycache__/
|   |   |   |-- common.cpython-312.pyc
|   |   |   |-- contracts.cpython-312.pyc
|   |   |   |-- engine.cpython-312.pyc
|   |   |   |-- __init__.cpython-312.pyc
|   |   |   |-- interventions.cpython-312.pyc
|   |   |   |-- observer.cpython-312.pyc
|   |   |   |-- transport.cpython-312.pyc
|   |   |   `-- world.cpython-312.pyc
|   |   |-- transport.py
|   |   |-- vendor/
|   |   |   |-- AttriGuard.py
|   |   |   `-- scheduling.json
|   |   `-- world.py
|   |-- legacy_o/
|   |   |-- common.py
|   |   |-- engine.py
|   |   |-- __init__.py
|   |   |-- interventions.py
|   |   |-- observer.py
|   |   |-- __pycache__/
|   |   |   |-- common.cpython-312.pyc
|   |   |   |-- engine.cpython-312.pyc
|   |   |   |-- __init__.cpython-312.pyc
|   |   |   |-- interventions.cpython-312.pyc
|   |   |   |-- observer.cpython-312.pyc
|   |   |   |-- transport.cpython-312.pyc
|   |   |   `-- world.cpython-312.pyc
|   |   |-- transport.py
|   |   |-- vendor/
|   |   |   |-- AttriGuard.py
|   |   |   `-- scheduling.json
|   |   `-- world.py
|   |-- placement.py
|   |-- protocol.py
|   |-- __pycache__/
|   |   |-- analysis.cpython-312.pyc
|   |   |-- cpu.cpython-312.pyc
|   |   |-- execution.cpython-312.pyc
|   |   |-- graphs.cpython-312.pyc
|   |   |-- __init__.cpython-312.pyc
|   |   |-- placement.cpython-312.pyc
|   |   |-- protocol.cpython-312.pyc
|   |   |-- qualification.cpython-312.pyc
|   |   |-- runner.cpython-312.pyc
|   |   |-- sequence.cpython-312.pyc
|   |   |-- serving.cpython-312.pyc
|   |   `-- util.cpython-312.pyc
|   |-- qualification.py
|   |-- runner.py
|   |-- sequence.py
|   |-- serving.py
|   `-- util.py
|-- reference_discovery_evidence/
|   |-- IDENTITY.json
|   |-- IEEE_SP_S1_Run_Deep_Audit_and_Scientific_Decision.md
|   `-- s1_reference_gpu3_20261025T173651Z_1528393_1266.tar.gz
|-- reference_discovery_parallel/
|   |-- ADDITIONAL_RUNTIME_HASHES.json
|   |-- AGENTS.md
|   |-- audit_core.py
|   |-- base/
|   |   |-- AGENTS.md
|   |   |-- bootstrap.py
|   |   |-- common.py
|   |   |-- experiment.py
|   |   |-- __init__.py
|   |   |-- native.py
|   |   |-- origin_data/
|   |   |   |-- ARCHIVE_SHA256SUMS
|   |   |   |-- S1_C1_OFF/
|   |   |   |   |-- diagnostic.log
|   |   |   |   |-- driver_records.json
|   |   |   |   |-- effective_driver_profile.json
|   |   |   |   |-- events.jsonl
|   |   |   |   |-- executed_guard.py
|   |   |   |   |-- final_reporting.json
|   |   |   |   |-- final_world.json
|   |   |   |   |-- http/
|   |   |   |   |   |-- 0001.request.json
|   |   |   |   |   |-- 0001.response.json
|   |   |   |   |   |-- 0002.request.json
|   |   |   |   |   |-- 0002.response.json
|   |   |   |   |   |-- 0003.request.json
|   |   |   |   |   `-- 0003.response.json
|   |   |   |   |-- initial_world.json
|   |   |   |   |-- instrumentation.diff
|   |   |   |   |-- item.json
|   |   |   |   |-- messages.json
|   |   |   |   |-- native.log
|   |   |   |   |-- requests/
|   |   |   |   |   |-- 0000_actor.driver_request.json
|   |   |   |   |   |-- 0000_actor.response.json
|   |   |   |   |   |-- 0001_actor.driver_request.json
|   |   |   |   |   |-- 0001_actor.response.json
|   |   |   |   |   |-- 0002_actor.driver_request.json
|   |   |   |   |   `-- 0002_actor.response.json
|   |   |   |   |-- result.json
|   |   |   |   `-- tokenization/
|   |   |   |       |-- 0001.json
|   |   |   |       |-- 0002.json
|   |   |   |       `-- 0003.json
|   |   |   `-- SOURCE_ARCHIVE.json
|   |   |-- origin.py
|   |   |-- protocol.py
|   |   |-- __pycache__/
|   |   |   |-- common.cpython-312.pyc
|   |   |   |-- __init__.cpython-312.pyc
|   |   |   `-- protocol.cpython-312.pyc
|   |   |-- qualification.py
|   |   |-- report.py
|   |   |-- RUNTIME_HASHES.json
|   |   |-- sequence.py
|   |   |-- serving.py
|   |   |-- source.py
|   |   |-- transport.py
|   |   `-- vendor/
|   |       |-- AttriGuard.py
|   |       |-- AUTHOR_RELEASE_README.md
|   |       |-- local_llm_compat.py
|   |       |-- my_agent_pipeline.py
|   |       |-- openai_llm_compat.py
|   |       `-- SOURCE_IDENTITY.json
|   |-- bootstrap.py
|   |-- budget.py
|   |-- campaign.py
|   |-- checkpoint_state.py
|   |-- combined.py
|   |-- common.py
|   |-- counterfactual.py
|   |-- diagnostics.py
|   |-- driver.py
|   |-- effects.py
|   |-- engine.py
|   |-- episode_worker.py
|   |-- execution_config.py
|   |-- experiment.py
|   |-- gate.py
|   |-- gemma_parser_plugin.py
|   |-- gpu2_audit.py
|   |-- infrastructure.py
|   |-- __init__.py
|   |-- integrity.py
|   |-- live_profile.py
|   |-- matched_recovery.py
|   |-- mock_model.py
|   |-- models.py
|   |-- observer.py
|   |-- operational_tests.py
|   |-- packaging.py
|   |-- protocol.py
|   |-- __pycache__/
|   |   |-- campaign.cpython-312.pyc
|   |   |-- common.cpython-312.pyc
|   |   |-- execution_config.cpython-312.pyc
|   |   |-- __init__.cpython-312.pyc
|   |   |-- integrity.cpython-312.pyc
|   |   |-- models.cpython-312.pyc
|   |   |-- protocol.cpython-312.pyc
|   |   |-- scaled_protocol.cpython-312.pyc
|   |   `-- verify.cpython-312.pyc
|   |-- qualification.py
|   |-- report.py
|   |-- rolling.py
|   |-- runtime_receipt.py
|   |-- scaled_protocol.py
|   |-- sequence.py
|   |-- strict_tags.py
|   |-- templates/
|   |   `-- gemma3_tools_adapted.jinja
|   |-- token_diagnostics.py
|   |-- uploads.py
|   |-- verify.py
|   `-- world.py
|-- reference_discovery_provenance/
|   |-- IEEE_SP_Previous_Scaled_Design.md
|   |-- ORIGINAL_344_ALLOCATION.json
|   |-- previous_scaled_validation/
|   |   |-- ARCHIVE_VALIDATION.json
|   |   |-- BUILD_VALIDATION.json
|   |   |-- BUILD_VALIDATION.md
|   |   |-- CPU_QUALIFICATION.json
|   |   |-- CPU_QUALIFICATION.log
|   |   |-- FRESH_LAUNCHER_VALIDATION.json
|   |   |-- INTERRUPTION_VALIDATION.json
|   |   |-- LOCK_VALIDATION.json
|   |   `-- ORDERING_RECOMPUTATION.json
|   |-- README_PREVIOUS_SCALED_REFERENCE.md
|   |-- retained_s1/
|   |   |-- SOURCE_PROVENANCE_S1.json
|   |   `-- THIRD_PARTY_NOTICES_S1.md
|   `-- SOURCE_PROVENANCE_PREVIOUS_SCALED.json
|-- references/
|   |-- incident_report.pdf
|   |-- literature/
|   |   `-- README.md
|   |-- prior_reviews.txt
|   |-- prior_study.pdf
|   `-- transition_lead.json
|-- release_native_study/
|   |-- AGENTS.md
|   |-- bootstrap.py
|   |-- common.py
|   |-- driver.py
|   |-- effects.py
|   |-- engine.py
|   |-- gate.py
|   |-- __init__.py
|   |-- mock_model.py
|   |-- observer.py
|   |-- protocol.py
|   |-- __pycache__/
|   |   |-- bootstrap.cpython-312.pyc
|   |   |-- common.cpython-312.pyc
|   |   |-- driver.cpython-312.pyc
|   |   |-- effects.cpython-312.pyc
|   |   |-- engine.cpython-312.pyc
|   |   |-- gate.cpython-312.pyc
|   |   |-- __init__.cpython-312.pyc
|   |   |-- mock_model.cpython-312.pyc
|   |   |-- observer.cpython-312.pyc
|   |   |-- protocol.cpython-312.pyc
|   |   |-- qualify.cpython-312.pyc
|   |   |-- runner.cpython-312.pyc
|   |   |-- sequence.cpython-312.pyc
|   |   |-- serving.cpython-312.pyc
|   |   `-- world.cpython-312.pyc
|   |-- qualify.py
|   |-- runner.py
|   |-- sequence.py
|   |-- serving.py
|   |-- vendor/
|   |   |-- AttriGuard.py
|   |   |-- AUTHOR_RELEASE_README.md
|   |   |-- local_llm_compat.py
|   |   |-- my_agent_pipeline.py
|   |   |-- openai_llm_compat.py
|   |   |-- __pycache__/
|   |   |   |-- AttriGuard.cpython-312.pyc
|   |   |   |-- local_llm_compat.cpython-312.pyc
|   |   |   |-- my_agent_pipeline.cpython-312.pyc
|   |   |   `-- openai_llm_compat.cpython-312.pyc
|   |   `-- SOURCE_IDENTITY.json
|   |-- verify_results.py
|   `-- world.py
|-- requirements-authorization-research.lock.txt
|-- requirements-native.lock.txt
|-- requirements-reconciled.lock.txt
|-- requirements-reference-discovery.lock.txt
|-- requirements-research.lock.txt
|-- requirements-s1-tested.lock.txt
|-- research_basis/
|   |-- CHECK_ANONYMITY.sh
|   |-- CHECK_E2E.sh
|   |-- CHECK_ENV.sh
|   |-- CLAIM_TO_ARTIFACT.md
|   |-- docs/
|   |   |-- ARTIFACT_STRUCTURE_AND_POLICIES.md
|   |   `-- REPRODUCTION.md
|   |-- figures/
|   |   |-- figure1.pdf
|   |   |-- figure2.pdf
|   |   |-- Figure2.py
|   |   |-- figure3.pdf
|   |   |-- Figure3.py
|   |   |-- figure4.pdf
|   |   |-- Figure4.py
|   |   |-- figure5.pdf
|   |   |-- Figure5.py
|   |   |-- figure6.pdf
|   |   `-- Figure6.py
|   |-- implementation_evidence/
|   |   |-- ATTRIGUARD_SOURCE_SHA256.txt
|   |   |-- paef_oracle.py
|   |   `-- source_bound_isolation/
|   |       `-- ATTRIGUARD_AUDIT_TRANSITION_RESULT.json
|   |-- LEGACY_PATH_MAP.tsv
|   |-- README.md
|   |-- READ_THIS_FIRST.md
|   |-- requirements-e2e-core.txt
|   |-- requirements.txt
|   |-- RUN_END_TO_END.sh
|   |-- RUN_FIGURES.sh
|   |-- RUN_FULL_RERUN.sh
|   |-- scripts/
|   |   |-- reproduction/
|   |   |   |-- analyze_agentwatcher_on.py
|   |   |   |-- lib.sh
|   |   |   |-- materialize_legacy_worktree.py
|   |   |   |-- patch_a13c0_runner_for_anonymous_archives.py
|   |   |   |-- resolve_legacy_path.py
|   |   |   `-- stages/
|   |   |       |-- 01_a13_natural.sh
|   |   |       |-- 02_a13_c0_extension.sh
|   |   |       |-- 03_b1_generator_breadth.sh
|   |   |       |-- 04_a14_controlled_source.sh
|   |   |       |-- 05_n3_unauthorized_control.sh
|   |   |       |-- 06_r2b_threshold_frontier.sh
|   |   |       |-- 07_agentwatcher.sh
|   |   |       |-- 08_n6_attriguard_architecture.sh
|   |   |       |-- 09_causalarmor_calibration.sh
|   |   |       |-- 10_live_e2e_attriguard.sh
|   |   |       |-- 11_replay.sh
|   |   |       `-- 12_figures.sh
|   |   `-- verification/
|   |       |-- build_hash_manifest.py
|   |       |-- check_anonymity.py
|   |       |-- render_figure6.py
|   |       |-- verify_current_claims.py
|   |       |-- verify_hashes.py
|   |       `-- verify_source_coverage.py
|   |-- SELF_TEST.sh
|   |-- SETUP_E2E.sh
|   |-- SHA256SUMS.txt
|   |-- studies/
|   |   |-- 01_natural_relevance/
|   |   |   |-- corrected_natural_cohort/
|   |   |   |   |-- A13_C0_COMBINED_73_DECISIONS_DERIVED_v1.jsonl
|   |   |   |   |-- A13_C0_EXTENSION_DECISIONS_SUMMARY_v1.csv
|   |   |   |   |-- A13_C0_EXTENSION_DECISIONS_v1.jsonl
|   |   |   |   |-- A13_C0_EXTENSION_PROVENANCE_v1.json
|   |   |   |   |-- A13_C0_EXTENSION_RESULT_v1.json
|   |   |   |   |-- agentdojo_runs/
|   |   |   |   |   `-- vllm_parsed/
|   |   |   |   |       `-- workspace/
|   |   |   |   |           |-- user_task_29/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_34/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           `-- user_task_7/
|   |   |   |   |               `-- none/
|   |   |   |   |                   `-- none.json
|   |   |   |   |-- FINAL_SHA256.txt
|   |   |   |   `-- README.txt
|   |   |   |-- generator_breadth/
|   |   |   |   |-- claude45/
|   |   |   |   |   |-- agentdojo_runs/
|   |   |   |   |   |   `-- b1_openrouter_anthropic_claude-sonnet-4.5/
|   |   |   |   |   |       |-- banking/
|   |   |   |   |   |       |   |-- user_task_0/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_11/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_12/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_13/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_14/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_15/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_2/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_3/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_4/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_5/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_6/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   `-- user_task_9/
|   |   |   |   |   |       |       `-- none/
|   |   |   |   |   |       |           `-- none.json
|   |   |   |   |   |       |-- slack/
|   |   |   |   |   |       |   |-- user_task_1/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_10/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_11/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_12/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_13/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_14/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_15/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_16/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_17/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_18/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_19/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_2/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_3/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_4/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_5/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_7/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_8/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   `-- user_task_9/
|   |   |   |   |   |       |       `-- none/
|   |   |   |   |   |       |           `-- none.json
|   |   |   |   |   |       |-- travel/
|   |   |   |   |   |       |   |-- user_task_0/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_1/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_3/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_4/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_7/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   `-- user_task_8/
|   |   |   |   |   |       |       `-- none/
|   |   |   |   |   |       |           `-- none.json
|   |   |   |   |   |       `-- workspace/
|   |   |   |   |   |           |-- user_task_12/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_13/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_15/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_18/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_20/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_21/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_25/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_29/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_31/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_32/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_33/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_34/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_36/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_37/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_4/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_6/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_7/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_8/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           `-- user_task_9/
|   |   |   |   |   |               `-- none/
|   |   |   |   |   |                   `-- none.json
|   |   |   |   |   |-- decisions.jsonl
|   |   |   |   |   |-- manifest.json
|   |   |   |   |   |-- protocol_pointer.json
|   |   |   |   |   |-- REPORT.md
|   |   |   |   |   |-- results.json
|   |   |   |   |   `-- taxonomy.json
|   |   |   |   |-- COMBINED_REPORT.md
|   |   |   |   |-- combined_results.json
|   |   |   |   |-- FREEZE_COMPLETE.json
|   |   |   |   |-- gpt4o/
|   |   |   |   |   |-- agentdojo_runs/
|   |   |   |   |   |   `-- b1_openrouter_openai_gpt-4o/
|   |   |   |   |   |       |-- banking/
|   |   |   |   |   |       |   |-- user_task_0/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_11/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_12/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_13/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_14/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_15/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_2/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_3/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_4/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_5/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_6/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   `-- user_task_9/
|   |   |   |   |   |       |       `-- none/
|   |   |   |   |   |       |           `-- none.json
|   |   |   |   |   |       |-- slack/
|   |   |   |   |   |       |   |-- user_task_1/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_10/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_11/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_12/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_13/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_14/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_15/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_16/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_17/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_18/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_19/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_2/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_3/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_4/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_5/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_7/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_8/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   `-- user_task_9/
|   |   |   |   |   |       |       `-- none/
|   |   |   |   |   |       |           `-- none.json
|   |   |   |   |   |       |-- travel/
|   |   |   |   |   |       |   |-- user_task_0/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_1/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_3/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_4/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   |-- user_task_7/
|   |   |   |   |   |       |   |   `-- none/
|   |   |   |   |   |       |   |       `-- none.json
|   |   |   |   |   |       |   `-- user_task_8/
|   |   |   |   |   |       |       `-- none/
|   |   |   |   |   |       |           `-- none.json
|   |   |   |   |   |       `-- workspace/
|   |   |   |   |   |           |-- user_task_12/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_13/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_15/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_18/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_20/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_21/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_25/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_29/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_31/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_32/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_33/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_34/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_36/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_37/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_4/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_6/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_7/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           |-- user_task_8/
|   |   |   |   |   |           |   `-- none/
|   |   |   |   |   |           |       `-- none.json
|   |   |   |   |   |           `-- user_task_9/
|   |   |   |   |   |               `-- none/
|   |   |   |   |   |                   `-- none.json
|   |   |   |   |   |-- decisions.jsonl
|   |   |   |   |   |-- manifest.json
|   |   |   |   |   |-- protocol_pointer.json
|   |   |   |   |   |-- REPORT.md
|   |   |   |   |   |-- results.json
|   |   |   |   |   `-- taxonomy.json
|   |   |   |   |-- model_lineage.json
|   |   |   |   |-- protocol.json
|   |   |   |   |-- source_hashes.json
|   |   |   |   |-- task_manifest.json
|   |   |   |   `-- taxonomy.json
|   |   |   |-- original_natural_runs/
|   |   |   |   |-- agentdojo_runs/
|   |   |   |   |   `-- vllm_parsed/
|   |   |   |   |       |-- banking/
|   |   |   |   |       |   |-- user_task_0/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_11/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_12/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_13/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_14/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_15/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_2/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_3/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_4/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_5/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_6/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   `-- user_task_9/
|   |   |   |   |       |       `-- none/
|   |   |   |   |       |           `-- none.json
|   |   |   |   |       |-- slack/
|   |   |   |   |       |   |-- user_task_1/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_10/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_11/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_12/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_13/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_14/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_15/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_16/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_17/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_18/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_19/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_2/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_3/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_4/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_5/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_7/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_8/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   `-- user_task_9/
|   |   |   |   |       |       `-- none/
|   |   |   |   |       |           `-- none.json
|   |   |   |   |       |-- travel/
|   |   |   |   |       |   |-- user_task_0/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_1/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_3/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_4/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   |-- user_task_7/
|   |   |   |   |       |   |   `-- none/
|   |   |   |   |       |   |       `-- none.json
|   |   |   |   |       |   `-- user_task_8/
|   |   |   |   |       |       `-- none/
|   |   |   |   |       |           `-- none.json
|   |   |   |   |       `-- workspace/
|   |   |   |   |           |-- user_task_12/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_13/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_15/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_18/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_20/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_21/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_25/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_31/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_32/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_33/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_36/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_37/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_4/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_6/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           |-- user_task_8/
|   |   |   |   |           |   `-- none/
|   |   |   |   |           |       `-- none.json
|   |   |   |   |           `-- user_task_9/
|   |   |   |   |               `-- none/
|   |   |   |   |                   `-- none.json
|   |   |   |   |-- decisions.jsonl
|   |   |   |   |-- manifest.json
|   |   |   |   |-- protocol.json
|   |   |   |   |-- REPORT.md
|   |   |   |   |-- results.json
|   |   |   |   `-- taxonomy.json
|   |   |   |-- README.md
|   |   |   `-- support/
|   |   |       |-- A13_C0_EXTENSION_PREFREEZE_v1/
|   |   |       |   |-- A13_C0_EXTENSION_DECISIONS_v1.csv
|   |   |       |   |-- A13_C0_EXTENSION_FREEZE_v1.json
|   |   |       |   |-- A13_C0_FUNCTION_ADJUDICATION_v1.csv
|   |   |       |   |-- FINAL_SHA256.txt
|   |   |       |   `-- README.txt
|   |   |       |-- A13_C0_EXTENSION_PREFREEZE_v1_AUTHOR_COMPLETE.tar.gz
|   |   |       |-- A13_C0_EXTENSION_PREFREEZE_v1_AUTHOR_RUN.log
|   |   |       |-- A13_C0_EXTENSION_PREFREEZE_v1.py
|   |   |       |-- A13_C0_EXTENSION_RUNNER_FREEZE_v1/
|   |   |       |   |-- A13_C0_EXTENSION_RUNNER_FREEZE_v1.json
|   |   |       |   |-- A13_C0_EXTENSION_RUNNER_TARGETS_v1.csv
|   |   |       |   |-- FINAL_SHA256.txt
|   |   |       |   `-- README.txt
|   |   |       |-- A13_C0_EXTENSION_RUNNER_PREFLIGHT_v1_AUTHOR_RUN.log
|   |   |       |-- A13_C0_EXTENSION_RUNNER_v1.py
|   |   |       |-- A13_C0_EXTENSION_SCIENCE_v1_AUTHOR_RUN.log
|   |   |       |-- A13_C0_HISTORICAL_A13_COMPLETE_v1.zip
|   |   |       |-- A13_C0_HISTORICAL_A13_COMPLETE_v1.zip.sha256
|   |   |       |-- A13_C0_INPUT_BUNDLE_v1.zip
|   |   |       |-- A13_C0_INPUT_BUNDLE_v1.zip.sha256
|   |   |       |-- A13_C0_V2_1_AUTHOR_AUDIT/
|   |   |       |   |-- A13_C0_V2_1_BROAD_SCREEN_DECISION_CENSUS.csv
|   |   |       |   |-- A13_C0_V2_1_DEEP_AUDIT.json
|   |   |       |   |-- A13_C0_V2_1_FUNCTION_COVERAGE.csv
|   |   |       |   |-- A13_C0_V2_1_LABEL_REASON_MATRIX.csv
|   |   |       |   |-- A13_C0_V2_1_MISSED_CANDIDATES.csv
|   |   |       |   |-- A13_C0_V2_1_ORIGINAL_DECISION_CENSUS.csv
|   |   |       |   |-- A13_C0_V2_1_TASK_CENSUS.csv
|   |   |       |   `-- FINAL_SHA256.txt
|   |   |       |-- A13_C0_V2_1_AUTHOR_RUN_COMPLETE.tar.gz
|   |   |       |-- A13_C0_V2_1_AUTHOR_RUN.log
|   |   |       |-- A13_C0_V2_1_DEEP_ZERO_CALL_AUDIT.py
|   |   |       |-- A13.py
|   |   |       |-- a13_r1b_llama_boundarysafe/
|   |   |       |   |-- checkpoint_decisions.jsonl
|   |   |       |   |-- decisions.jsonl
|   |   |       |   |-- manifest.json
|   |   |       |   |-- protocol.json
|   |   |       |   |-- REPORT.md
|   |   |       |   `-- results.json
|   |   |       |-- A13_R1B_Llama_BoundarySafe.py
|   |   |       |-- a13_r1_llama/
|   |   |       |   |-- checkpoint_decisions.jsonl
|   |   |       |   |-- decisions.jsonl
|   |   |       |   |-- manifest.json
|   |   |       |   |-- protocol.json
|   |   |       |   |-- REPORT.md
|   |   |       |   `-- results.json
|   |   |       |-- A13_R1_Llama.py
|   |   |       |-- a13_r2_llama/
|   |   |       |   |-- agentdojo_runs/
|   |   |       |   |   `-- vllm_parsed/
|   |   |       |   |       |-- banking/
|   |   |       |   |       |   |-- user_task_0/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_11/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_12/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_13/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_14/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_15/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_2/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_3/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_4/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_5/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_6/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   `-- user_task_9/
|   |   |       |   |       |       `-- none/
|   |   |       |   |       |           `-- none.json
|   |   |       |   |       |-- slack/
|   |   |       |   |       |   |-- user_task_1/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_10/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_11/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_12/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_13/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_14/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_15/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_16/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_17/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_18/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_19/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_2/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_3/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_4/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_5/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_7/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_8/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   `-- user_task_9/
|   |   |       |   |       |       `-- none/
|   |   |       |   |       |           `-- none.json
|   |   |       |   |       |-- travel/
|   |   |       |   |       |   |-- user_task_0/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_1/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_3/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_4/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_7/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   `-- user_task_8/
|   |   |       |   |       |       `-- none/
|   |   |       |   |       |           `-- none.json
|   |   |       |   |       `-- workspace/
|   |   |       |   |           |-- user_task_12/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_13/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_15/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_18/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_20/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_21/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_25/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_31/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_32/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_33/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_36/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_37/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_4/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_6/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_8/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           `-- user_task_9/
|   |   |       |   |               `-- none/
|   |   |       |   |                   `-- none.json
|   |   |       |   |-- decisions.jsonl
|   |   |       |   |-- manifest.json
|   |   |       |   |-- protocol.json
|   |   |       |   |-- REPORT.md
|   |   |       |   |-- results.json
|   |   |       |   `-- taxonomy.json
|   |   |       |-- A13_R2_Llama.py
|   |   |       |-- A13_R2_Llama_Server_Smoke.py
|   |   |       |-- a13_r3_gemini/
|   |   |       |   |-- agentdojo_runs/
|   |   |       |   |   `-- openrouter_google_gemini-2.5-flash/
|   |   |       |   |       |-- banking/
|   |   |       |   |       |   |-- user_task_0/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_11/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_12/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_13/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_14/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_15/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_2/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_3/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_4/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_5/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_6/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   `-- user_task_9/
|   |   |       |   |       |       `-- none/
|   |   |       |   |       |           `-- none.json
|   |   |       |   |       |-- slack/
|   |   |       |   |       |   |-- user_task_1/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_10/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_11/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_12/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_13/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_14/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_15/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_16/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_17/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_18/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_19/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_2/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_3/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_4/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_5/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_7/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_8/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   `-- user_task_9/
|   |   |       |   |       |       `-- none/
|   |   |       |   |       |           `-- none.json
|   |   |       |   |       |-- travel/
|   |   |       |   |       |   |-- user_task_0/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_1/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_3/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_4/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   |-- user_task_7/
|   |   |       |   |       |   |   `-- none/
|   |   |       |   |       |   |       `-- none.json
|   |   |       |   |       |   `-- user_task_8/
|   |   |       |   |       |       `-- none/
|   |   |       |   |       |           `-- none.json
|   |   |       |   |       `-- workspace/
|   |   |       |   |           |-- user_task_12/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_13/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_15/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_18/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_20/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_21/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_25/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_31/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_32/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_33/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_36/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_37/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_4/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_6/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           |-- user_task_8/
|   |   |       |   |           |   `-- none/
|   |   |       |   |           |       `-- none.json
|   |   |       |   |           `-- user_task_9/
|   |   |       |   |               `-- none/
|   |   |       |   |                   `-- none.json
|   |   |       |   |-- decisions.jsonl
|   |   |       |   |-- manifest.json
|   |   |       |   |-- protocol.json
|   |   |       |   |-- REPORT.md
|   |   |       |   |-- results.json
|   |   |       |   |-- smoke_agentdojo/
|   |   |       |   |   `-- openrouter_google_gemini-2.5-flash/
|   |   |       |   |       `-- workspace/
|   |   |       |   |           `-- user_task_19/
|   |   |       |   |               `-- none/
|   |   |       |   |                   `-- none.json
|   |   |       |   `-- taxonomy.json
|   |   |       |-- A13_R3_Gemini.py
|   |   |       |-- b1_a12_backbone_replication/
|   |   |       |   |-- FREEZE_COMPLETE.json
|   |   |       |   |-- model_lineage.json
|   |   |       |   |-- protocol.json
|   |   |       |   |-- source_hashes.json
|   |   |       |   |-- task_manifest.json
|   |   |       |   `-- taxonomy.json
|   |   |       |-- B1_C0_amend_freeze.log
|   |   |       |-- B1_C0_claude45_preflight.log
|   |   |       |-- B1_C0_claude45_science.log
|   |   |       |-- B1_C0_gpt4o_preflight.log
|   |   |       |-- B1_C0_gpt4o_science.log
|   |   |       |-- B1_C0_joint_analysis.log
|   |   |       |-- B1_C0_POPULATION_AMENDMENT_v2/
|   |   |       |   |-- B1_C0_00_amend_freeze.py
|   |   |       |   |-- B1_C0_01_run.py
|   |   |       |   |-- B1_C0_02_analyze.py
|   |   |       |   |-- B1_C0_PROTOCOL_SPEC.md
|   |   |       |   |-- B1_C0_RUNBOOK.md
|   |   |       |   `-- PACKAGE_SHA256.txt
|   |   |       |-- run_a13_c0_end_to_end.sh
|   |   |       |-- start_A13_R1_Llama_vLLM.sh
|   |   |       `-- start_A13_R2_Llama_vLLM.sh
|   |   |-- 02_controlled_source_relocation/
|   |   |   |-- frozen_results/
|   |   |   |   |-- analysis/
|   |   |   |   |   |-- REPORT.md
|   |   |   |   |   `-- results.json
|   |   |   |   |-- authorization_equivalence_graph.jsonl
|   |   |   |   |-- base_instances.json
|   |   |   |   |-- completion_token_semantics.jsonl
|   |   |   |   |-- component_registry.jsonl
|   |   |   |   |-- contexts/
|   |   |   |   |   |-- structured_contexts.jsonl
|   |   |   |   |   `-- token_maps.jsonl
|   |   |   |   |-- FROZEN_ARTIFACT_SHA256.txt
|   |   |   |   |-- human_base_quartet_audit.jsonl
|   |   |   |   |-- human_base_quartet_audit_TEMPLATE.jsonl
|   |   |   |   |-- human_equivalence_audit.jsonl
|   |   |   |   |-- human_equivalence_audit_TEMPLATE.jsonl
|   |   |   |   |-- lineage_graph.jsonl
|   |   |   |   |-- mechanical_checks.jsonl
|   |   |   |   |-- neutral_replacements.jsonl
|   |   |   |   |-- prediction_ledger.json
|   |   |   |   |-- PREFREEZE_SUMMARY.json
|   |   |   |   |-- protocol.json
|   |   |   |   |-- scorer_gemma/
|   |   |   |   |   |-- condition_scores.jsonl
|   |   |   |   |   |-- raw_requests.jsonl
|   |   |   |   |   |-- raw_responses.jsonl
|   |   |   |   |   |-- RUN_COMPLETE.json
|   |   |   |   |   |-- score_cache.jsonl
|   |   |   |   |   `-- server_preflight.json
|   |   |   |   |-- scorer_llama/
|   |   |   |   |   |-- condition_scores.jsonl
|   |   |   |   |   |-- raw_requests.jsonl
|   |   |   |   |   |-- raw_responses.jsonl
|   |   |   |   |   |-- RUN_COMPLETE.json
|   |   |   |   |   |-- score_cache.jsonl
|   |   |   |   |   `-- server_preflight.json
|   |   |   |   |-- scoring_plan_gemma.jsonl
|   |   |   |   |-- scoring_plan_llama.jsonl
|   |   |   |   |-- source_hashes.json
|   |   |   |   `-- threshold_aivr_v1/
|   |   |   |       |-- A14M_THRESHOLD_AIVR_FREEZE.json
|   |   |   |       |-- family_aivr_gemma.csv
|   |   |   |       |-- family_aivr_llama.csv
|   |   |   |       |-- loso_aivr_gemma.csv
|   |   |   |       |-- loso_aivr_llama.csv
|   |   |   |       |-- MANIFEST.json
|   |   |   |       |-- REPORT.md
|   |   |   |       |-- results.json
|   |   |   |       |-- threshold_sweep_gemma.csv
|   |   |   |       `-- threshold_sweep_llama.csv
|   |   |   |-- README.md
|   |   |   `-- support/
|   |   |       |-- a14_authorization_invariance_PREFREEZE_AUDIT0_20260809_075011/
|   |   |       |   `-- authorization_nonequivalent_controls.jsonl
|   |   |       |-- A14M_00_prepare_draft.py
|   |   |       |-- A14M_01b_base_quartet_audit_cli.py
|   |   |       |-- A14M_01_human_audit_cli.py
|   |   |       |-- A14M_02_freeze_protocol.py
|   |   |       |-- A14M_03_score.py
|   |   |       |-- A14M_04_analyze.py
|   |   |       |-- A14M_05_threshold_aivr.py
|   |   |       |-- a14m_common.py
|   |   |       |-- A14M_PROTOCOL_SPEC.md
|   |   |       |-- A14M_RUN_PREFREEZE.sh
|   |   |       |-- A14M_THRESHOLD_AIVR_PREFREEZE_SPEC_v1.md
|   |   |       |-- PREFREEZE_AMENDMENT_01_BASE_QUARTET_AUDIT.md
|   |   |       |-- start_A14M_Gemma_vLLM_8111.sh
|   |   |       `-- start_A14M_Llama_vLLM.sh
|   |   |-- 03_matched_unauthorized_comparison/
|   |   |   |-- frozen_results/
|   |   |   |   |-- N3_ANALYSIS.json
|   |   |   |   |-- N3_BASELINE_A14_UNITS.jsonl
|   |   |   |   |-- N3_BASE_PROJECTION.json
|   |   |   |   |-- N3_FREEZE.json
|   |   |   |   |-- N3_FREEZE_SHA256.txt
|   |   |   |   |-- N3_HUMAN_AUDIT.jsonl
|   |   |   |   |-- N3_HUMAN_AUDIT_TEMPLATE.jsonl
|   |   |   |   |-- N3_MECHANICAL_CHECKS.json
|   |   |   |   |-- N3_POSITIVE_CONTEXTS.jsonl
|   |   |   |   |-- N3_POSITIVE_SCORING_UNITS.jsonl
|   |   |   |   |-- N3_PREFREEZE_DRAFT_MANIFEST.json
|   |   |   |   |-- N3_PROTOCOL_DRAFT.json
|   |   |   |   |-- science_gemma/
|   |   |   |   |   |-- RAW_REQUESTS.jsonl
|   |   |   |   |   |-- RAW_RESPONSES.jsonl
|   |   |   |   |   |-- RUN_COMPLETE.json
|   |   |   |   |   |-- SCIENCE_SCORES.jsonl
|   |   |   |   |   |-- SCORE_CACHE.jsonl
|   |   |   |   |   `-- SERVER_PREFLIGHT.json
|   |   |   |   `-- science_llama/
|   |   |   |       |-- RAW_REQUESTS.jsonl
|   |   |   |       |-- RAW_RESPONSES.jsonl
|   |   |   |       |-- RUN_COMPLETE.json
|   |   |   |       |-- SCIENCE_SCORES.jsonl
|   |   |   |       |-- SCORE_CACHE.jsonl
|   |   |   |       `-- SERVER_PREFLIGHT.json
|   |   |   |-- README.md
|   |   |   `-- support/
|   |   |       |-- N3_analysis.log
|   |   |       |-- N3_COMPLETE_AUTHOR_v1_2.tar.gz
|   |   |       |-- N3_COMPLETE_AUTHOR_v1_2.tar.gz.sha256
|   |   |       |-- N3_DISCRIMINANT_PREFREEZE_v1_2/
|   |   |       |   |-- N3_00_prepare_prefreeze.py
|   |   |       |   |-- N3_01_human_audit_cli.py
|   |   |       |   |-- N3_02_freeze_protocol.py
|   |   |       |   |-- N3_03_score_science.py
|   |   |       |   |-- N3_04_analyze.py
|   |   |       |   |-- n3_common.py
|   |   |       |   |-- PACKAGE_SHA256.txt
|   |   |       |   |-- README.md
|   |   |       |   |-- start_N3_Gemma_vLLM.sh
|   |   |       |   `-- start_N3_Llama_vLLM.sh
|   |   |       |-- N3_gemma_science.log
|   |   |       `-- N3_llama_science.log
|   |   |-- 04_threshold_frontier/
|   |   |   |-- frozen_results/
|   |   |   |   |-- R2B_JTF_FREEZE.json
|   |   |   |   |-- R2B_JTF_FRONTIER_gemma.csv
|   |   |   |   |-- R2B_JTF_FRONTIER_llama.csv
|   |   |   |   |-- R2B_JTF_MANIFEST.json
|   |   |   |   |-- R2B_JTF_REPORT.md
|   |   |   |   |-- R2B_JTF_RESULTS.json
|   |   |   |   |-- RUN_COMPLETE.json
|   |   |   |   `-- VERIFY_REPORT.json
|   |   |   |-- README.md
|   |   |   `-- support/
|   |   |       `-- R2B_JTF_PREFREEZE_v1/
|   |   |           |-- analyze_R2B_JTF_v1.sh
|   |   |           |-- freeze_R2B_JTF_v1.sh
|   |   |           |-- PACKAGE_SHA256.txt
|   |   |           |-- PROTOCOL_SPEC.md
|   |   |           |-- R2B_00_freeze.py
|   |   |           |-- R2B_01_analyze.py
|   |   |           |-- R2B_02_verify.py
|   |   |           `-- README.md
|   |   |-- 05_agentwatcher/
|   |   |   |-- on_off_comparison/
|   |   |   |   |-- FINAL_ARTIFACT_SHA256.txt
|   |   |   |   |-- P2_ANALYSIS.json
|   |   |   |   |-- P2_ANALYSIS.md
|   |   |   |   |-- P2_PAIRED_ROWS.csv
|   |   |   |   |-- P2_PREFREEZE_PACKAGE_MANIFEST.tsv
|   |   |   |   |-- P2_RAW_RESULT_MANIFEST.tsv
|   |   |   |   |-- P2_RUN_COMPLETE.json
|   |   |   |   |-- P2_SCIENCE_FREEZE.json
|   |   |   |   |-- P2_SCIENCE_FREEZE.md
|   |   |   |   |-- P2_SUITE_SUMMARY.csv
|   |   |   |   `-- raw_results/
|   |   |   |       `-- gpt-4o-mini/
|   |   |   |           |-- banking/
|   |   |   |           |   |-- injection_task_0/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_1/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_2/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_3/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_4/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_5/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_6/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_7/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_8/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- user_task_0/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_1.json
|   |   |   |           |   |       `-- injection_task_4.json
|   |   |   |           |   |-- user_task_1/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   |-- user_task_10/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_1.json
|   |   |   |           |   |       `-- injection_task_4.json
|   |   |   |           |   |-- user_task_11/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   |-- user_task_13/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_7.json
|   |   |   |           |   |       `-- injection_task_8.json
|   |   |   |           |   |-- user_task_14/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_0.json
|   |   |   |           |   |       |-- injection_task_2.json
|   |   |   |           |   |       |-- injection_task_5.json
|   |   |   |           |   |       `-- injection_task_8.json
|   |   |   |           |   |-- user_task_2/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_0.json
|   |   |   |           |   |       `-- injection_task_3.json
|   |   |   |           |   |-- user_task_3/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_6.json
|   |   |   |           |   |       `-- injection_task_8.json
|   |   |   |           |   |-- user_task_4/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_0.json
|   |   |   |           |   |       |-- injection_task_2.json
|   |   |   |           |   |       `-- injection_task_3.json
|   |   |   |           |   |-- user_task_5/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_1.json
|   |   |   |           |   |       `-- injection_task_2.json
|   |   |   |           |   |-- user_task_6/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_0.json
|   |   |   |           |   |       |-- injection_task_4.json
|   |   |   |           |   |       |-- injection_task_5.json
|   |   |   |           |   |       `-- injection_task_8.json
|   |   |   |           |   |-- user_task_7/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_1.json
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   |-- user_task_8/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_1.json
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   `-- user_task_9/
|   |   |   |           |       `-- tool_knowledge/
|   |   |   |           |           |-- injection_task_0.json
|   |   |   |           |           |-- injection_task_3.json
|   |   |   |           |           `-- injection_task_5.json
|   |   |   |           |-- slack/
|   |   |   |           |   |-- injection_task_1/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_2/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_3/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_4/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_5/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- user_task_1/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_1.json
|   |   |   |           |   |       `-- injection_task_4.json
|   |   |   |           |   |-- user_task_10/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_3.json
|   |   |   |           |   |-- user_task_11/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   |-- user_task_12/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_1.json
|   |   |   |           |   |       |-- injection_task_2.json
|   |   |   |           |   |       `-- injection_task_4.json
|   |   |   |           |   |-- user_task_13/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   |-- user_task_15/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_1.json
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   |-- user_task_16/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_4.json
|   |   |   |           |   |-- user_task_17/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_3.json
|   |   |   |           |   |       `-- injection_task_4.json
|   |   |   |           |   |-- user_task_18/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_2.json
|   |   |   |           |   |       `-- injection_task_3.json
|   |   |   |           |   |-- user_task_19/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_1.json
|   |   |   |           |   |       |-- injection_task_2.json
|   |   |   |           |   |       |-- injection_task_3.json
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   |-- user_task_2/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_1.json
|   |   |   |           |   |-- user_task_20/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_4.json
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   |-- user_task_3/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_2.json
|   |   |   |           |   |       `-- injection_task_3.json
|   |   |   |           |   |-- user_task_4/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_4.json
|   |   |   |           |   |-- user_task_6/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_3.json
|   |   |   |           |   |-- user_task_7/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_2.json
|   |   |   |           |   |-- user_task_8/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_2.json
|   |   |   |           |   `-- user_task_9/
|   |   |   |           |       `-- tool_knowledge/
|   |   |   |           |           `-- injection_task_2.json
|   |   |   |           |-- travel/
|   |   |   |           |   |-- injection_task_0/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_1/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_2/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_3/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_4/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_5/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- injection_task_6/
|   |   |   |           |   |   `-- none/
|   |   |   |           |   |       `-- none.json
|   |   |   |           |   |-- user_task_0/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_4.json
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   |-- user_task_1/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_2.json
|   |   |   |           |   |-- user_task_10/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_2.json
|   |   |   |           |   |-- user_task_11/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_2.json
|   |   |   |           |   |       |-- injection_task_4.json
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   |-- user_task_12/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   |-- user_task_13/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_2.json
|   |   |   |           |   |       |-- injection_task_3.json
|   |   |   |           |   |       `-- injection_task_4.json
|   |   |   |           |   |-- user_task_14/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_4.json
|   |   |   |           |   |       `-- injection_task_6.json
|   |   |   |           |   |-- user_task_15/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_5.json
|   |   |   |           |   |       `-- injection_task_6.json
|   |   |   |           |   |-- user_task_16/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_4.json
|   |   |   |           |   |-- user_task_18/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_5.json
|   |   |   |           |   |       `-- injection_task_6.json
|   |   |   |           |   |-- user_task_19/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_2.json
|   |   |   |           |   |       |-- injection_task_4.json
|   |   |   |           |   |       `-- injection_task_5.json
|   |   |   |           |   |-- user_task_2/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_5.json
|   |   |   |           |   |       `-- injection_task_6.json
|   |   |   |           |   |-- user_task_4/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_2.json
|   |   |   |           |   |-- user_task_5/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_1.json
|   |   |   |           |   |       `-- injection_task_2.json
|   |   |   |           |   |-- user_task_6/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_0.json
|   |   |   |           |   |       `-- injection_task_1.json
|   |   |   |           |   |-- user_task_7/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       `-- injection_task_0.json
|   |   |   |           |   |-- user_task_8/
|   |   |   |           |   |   `-- tool_knowledge/
|   |   |   |           |   |       |-- injection_task_1.json
|   |   |   |           |   |       `-- injection_task_6.json
|   |   |   |           |   `-- user_task_9/
|   |   |   |           |       `-- tool_knowledge/
|   |   |   |           |           `-- injection_task_6.json
|   |   |   |           `-- workspace/
|   |   |   |               |-- injection_task_0/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_1/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_10/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_11/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_12/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_13/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_2/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_3/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_4/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_5/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_6/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_7/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_8/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- injection_task_9/
|   |   |   |               |   `-- none/
|   |   |   |               |       `-- none.json
|   |   |   |               |-- user_task_0/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_11.json
|   |   |   |               |       |-- injection_task_3.json
|   |   |   |               |       `-- injection_task_6.json
|   |   |   |               |-- user_task_1/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_11.json
|   |   |   |               |       `-- injection_task_13.json
|   |   |   |               |-- user_task_10/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       `-- injection_task_1.json
|   |   |   |               |-- user_task_11/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_1.json
|   |   |   |               |       |-- injection_task_2.json
|   |   |   |               |       `-- injection_task_6.json
|   |   |   |               |-- user_task_12/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_12.json
|   |   |   |               |       |-- injection_task_13.json
|   |   |   |               |       |-- injection_task_2.json
|   |   |   |               |       |-- injection_task_5.json
|   |   |   |               |       |-- injection_task_7.json
|   |   |   |               |       `-- injection_task_9.json
|   |   |   |               |-- user_task_13/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       `-- injection_task_11.json
|   |   |   |               |-- user_task_14/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       `-- injection_task_0.json
|   |   |   |               |-- user_task_15/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_3.json
|   |   |   |               |       |-- injection_task_6.json
|   |   |   |               |       `-- injection_task_9.json
|   |   |   |               |-- user_task_16/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_0.json
|   |   |   |               |       `-- injection_task_7.json
|   |   |   |               |-- user_task_17/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_10.json
|   |   |   |               |       |-- injection_task_13.json
|   |   |   |               |       |-- injection_task_4.json
|   |   |   |               |       |-- injection_task_6.json
|   |   |   |               |       `-- injection_task_7.json
|   |   |   |               |-- user_task_18/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_10.json
|   |   |   |               |       |-- injection_task_11.json
|   |   |   |               |       |-- injection_task_12.json
|   |   |   |               |       |-- injection_task_1.json
|   |   |   |               |       `-- injection_task_9.json
|   |   |   |               |-- user_task_2/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_2.json
|   |   |   |               |       |-- injection_task_4.json
|   |   |   |               |       `-- injection_task_6.json
|   |   |   |               |-- user_task_20/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_2.json
|   |   |   |               |       `-- injection_task_4.json
|   |   |   |               |-- user_task_21/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       `-- injection_task_7.json
|   |   |   |               |-- user_task_22/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_0.json
|   |   |   |               |       |-- injection_task_10.json
|   |   |   |               |       |-- injection_task_1.json
|   |   |   |               |       |-- injection_task_4.json
|   |   |   |               |       `-- injection_task_9.json
|   |   |   |               |-- user_task_23/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_11.json
|   |   |   |               |       |-- injection_task_2.json
|   |   |   |               |       |-- injection_task_7.json
|   |   |   |               |       `-- injection_task_8.json
|   |   |   |               |-- user_task_24/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_0.json
|   |   |   |               |       `-- injection_task_12.json
|   |   |   |               |-- user_task_25/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_11.json
|   |   |   |               |       `-- injection_task_4.json
|   |   |   |               |-- user_task_26/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_0.json
|   |   |   |               |       `-- injection_task_5.json
|   |   |   |               |-- user_task_27/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_10.json
|   |   |   |               |       |-- injection_task_3.json
|   |   |   |               |       |-- injection_task_4.json
|   |   |   |               |       |-- injection_task_5.json
|   |   |   |               |       |-- injection_task_7.json
|   |   |   |               |       `-- injection_task_8.json
|   |   |   |               |-- user_task_28/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_1.json
|   |   |   |               |       `-- injection_task_4.json
|   |   |   |               |-- user_task_3/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_2.json
|   |   |   |               |       `-- injection_task_4.json
|   |   |   |               |-- user_task_30/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_0.json
|   |   |   |               |       |-- injection_task_10.json
|   |   |   |               |       `-- injection_task_1.json
|   |   |   |               |-- user_task_31/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_12.json
|   |   |   |               |       `-- injection_task_8.json
|   |   |   |               |-- user_task_32/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_13.json
|   |   |   |               |       `-- injection_task_2.json
|   |   |   |               |-- user_task_33/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_12.json
|   |   |   |               |       `-- injection_task_9.json
|   |   |   |               |-- user_task_34/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_13.json
|   |   |   |               |       `-- injection_task_2.json
|   |   |   |               |-- user_task_35/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_11.json
|   |   |   |               |       |-- injection_task_2.json
|   |   |   |               |       `-- injection_task_6.json
|   |   |   |               |-- user_task_36/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_13.json
|   |   |   |               |       |-- injection_task_1.json
|   |   |   |               |       |-- injection_task_7.json
|   |   |   |               |       `-- injection_task_8.json
|   |   |   |               |-- user_task_37/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_1.json
|   |   |   |               |       `-- injection_task_3.json
|   |   |   |               |-- user_task_38/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       `-- injection_task_9.json
|   |   |   |               |-- user_task_39/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_0.json
|   |   |   |               |       |-- injection_task_12.json
|   |   |   |               |       |-- injection_task_3.json
|   |   |   |               |       `-- injection_task_5.json
|   |   |   |               |-- user_task_4/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       `-- injection_task_3.json
|   |   |   |               |-- user_task_5/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_11.json
|   |   |   |               |       |-- injection_task_1.json
|   |   |   |               |       `-- injection_task_9.json
|   |   |   |               |-- user_task_6/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_10.json
|   |   |   |               |       |-- injection_task_11.json
|   |   |   |               |       |-- injection_task_1.json
|   |   |   |               |       `-- injection_task_3.json
|   |   |   |               |-- user_task_7/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_10.json
|   |   |   |               |       |-- injection_task_11.json
|   |   |   |               |       |-- injection_task_5.json
|   |   |   |               |       `-- injection_task_9.json
|   |   |   |               |-- user_task_8/
|   |   |   |               |   `-- tool_knowledge/
|   |   |   |               |       |-- injection_task_10.json
|   |   |   |               |       |-- injection_task_1.json
|   |   |   |               |       |-- injection_task_5.json
|   |   |   |               |       `-- injection_task_6.json
|   |   |   |               `-- user_task_9/
|   |   |   |                   `-- tool_knowledge/
|   |   |   |                       |-- injection_task_0.json
|   |   |   |                       |-- injection_task_2.json
|   |   |   |                       `-- injection_task_5.json
|   |   |   |-- paired_gate_study/
|   |   |   |   |-- AWN3_ALL_192_INPUTS.jsonl
|   |   |   |   |-- AWN3_ANALYSIS_COMPLETE.json
|   |   |   |   |-- AWN3_BASE_EFFECTS.csv
|   |   |   |   |-- AWN3_EXECUTION_INPUTS.jsonl
|   |   |   |   |-- AWN3_FREEZE_COMPLETE.json
|   |   |   |   |-- AWN3_FREEZE.json
|   |   |   |   |-- AWN3_MANIFEST.json
|   |   |   |   |-- AWN3_MAPPED_OUTPUTS.jsonl
|   |   |   |   |-- AWN3_PREFLIGHT.json
|   |   |   |   |-- AWN3_PREFREEZE_BUILD_SUMMARY.json
|   |   |   |   |-- AWN3_REPORT.md
|   |   |   |   |-- AWN3_RESULTS.json
|   |   |   |   |-- AWN3_SCIENCE_RUN_COMPLETE.json
|   |   |   |   |-- AWN3_SCIENCE_UNIQUE_OUTPUTS.jsonl
|   |   |   |   |-- AWN3_SHAM_ECHO_STATIC_IDENTITY_AUDIT.jsonl
|   |   |   |   `-- AWN3_VERIFY_REPORT.json
|   |   |   |-- README.md
|   |   |   `-- support/
|   |   |       |-- A15B0_00_source_lock.py
|   |   |       |-- A15B0_01_prepare_inputs.py
|   |   |       |-- A15B0_02_freeze_protocol.py
|   |   |       |-- A15B0_03_preflight.py
|   |   |       |-- A15B0_04b_run_no_attribution.py
|   |   |       |-- A15B0_04_run_agentwatcher.py
|   |   |       |-- A15B0_05_rescore_natural_gemma.py
|   |   |       |-- A15B0_06_analyze.py
|   |   |       |-- a15b0_agentwatcher_recon_v2/
|   |   |       |   |-- apply_reconstruction.py
|   |   |       |   |-- core.py
|   |   |       |   |-- defenses_init.py
|   |   |       |   |-- PACKAGE_SHA256.json
|   |   |       |   |-- README.md
|   |   |       |   |-- smoke_monitor.py
|   |   |       |   |-- start_monitor_vllm.sh
|   |   |       |   `-- verify_reconstruction.py
|   |   |       |-- a15b0_agentwatcher_recon_v3/
|   |   |       |   |-- core.py
|   |   |       |   |-- PACKAGE_SHA256.json
|   |   |       |   |-- patch_v2_to_v3.py
|   |   |       |   |-- README.md
|   |   |       |   `-- verify_v3.py
|   |   |       |-- a15b0_architecture_boundary/
|   |   |       |   |-- agentwatcher_controlled_outputs.jsonl
|   |   |       |   |-- agentwatcher_natural_outputs.jsonl
|   |   |       |   |-- agentwatcher_no_localization_controlled_outputs.jsonl
|   |   |       |   |-- agentwatcher_no_localization_natural_outputs.jsonl
|   |   |       |   |-- analysis_results.json
|   |   |       |   |-- attack_anchor/
|   |   |       |   |   |-- A15B0_ARMC_ATTACK_ANCHOR_FREEZE.json
|   |   |       |   |   |-- A15B0_ARMC_ATTACK_ANCHOR_FREEZE.sha256
|   |   |       |   |   |-- A15B0_IMPORTANT_INSTRUCTIONS_200_FILE_SHA256.txt
|   |   |       |   |   `-- A15B0_IMPORTANT_INSTRUCTIONS_200_LOG_SHA256.txt
|   |   |       |   |-- causalarmor_natural_gemma.jsonl
|   |   |       |   |-- controlled_96_inputs.jsonl
|   |   |       |   |-- controlled_execution_inputs.jsonl
|   |   |       |   |-- FREEZE_COMPLETE.json
|   |   |       |   |-- gemma_source_fidelity_lock.json
|   |   |       |   |-- natural_26_inputs.jsonl
|   |   |       |   |-- natural_static_input_hash_audit.jsonl
|   |   |       |   |-- PREFLIGHT.json
|   |   |       |   |-- PREFREEZE_INPUT_SUMMARY.json
|   |   |       |   |-- protocol.json
|   |   |       |   `-- source_lock.json
|   |   |       |-- a15b0_common.py
|   |   |       |-- A15B0_PROTOCOL_SPEC.md
|   |   |       |-- A15B0_RUNBOOK.md
|   |   |       |-- AW_N3_PREFREEZE_v1/
|   |   |       |   |-- AWN3_00_build_inputs.py
|   |   |       |   |-- AWN3_01_freeze_protocol.py
|   |   |       |   |-- AWN3_02_preflight.py
|   |   |       |   |-- AWN3_03_run_science.py
|   |   |       |   |-- AWN3_04_analyze.py
|   |   |       |   |-- AWN3_05_verify.py
|   |   |       |   |-- awn3_common.py
|   |   |       |   |-- AWN3_PROTOCOL_SPEC.md
|   |   |       |   |-- build_AWN3_v1.sh
|   |   |       |   |-- freeze_AWN3_v1.sh
|   |   |       |   |-- PACKAGE_SHA256.txt
|   |   |       |   |-- preflight_AWN3_v1.sh
|   |   |       |   |-- README.md
|   |   |       |   |-- run_AWN3_v1.sh
|   |   |       |   `-- start_AWN3_monitor_vllm.sh
|   |   |       |-- P2_AGENTWATCHER_NODEFENSE_AUTHOR_RUN.log
|   |   |       `-- P2_AGENTWATCHER_NODEFENSE_PREFREEZE_v1/
|   |   |           |-- P2_00_preflight_freeze.py
|   |   |           |-- P2_01_run_nodefense.py
|   |   |           |-- P2_02_analyze.py
|   |   |           |-- P2_03_verify.py
|   |   |           |-- p2_common.py
|   |   |           |-- P2_CONFIG.json
|   |   |           |-- P2_DEFENSE_ON_REFERENCE.csv
|   |   |           |-- P2_HISTORICAL_DEFENSE_ON_MANIFEST.tsv
|   |   |           |-- P2_PROTOCOL_FREEZE.md
|   |   |           |-- P2_RUNTIME_MANIFEST.tsv
|   |   |           |-- P2_SELECTED_PAIRS.json
|   |   |           |-- PACKAGE_SHA256.txt
|   |   |           |-- README.md
|   |   |           `-- RUN_P2.sh
|   |   |-- 06_attriguard/
|   |   |   |-- README.md
|   |   |   |-- route_and_block_study/
|   |   |   |   `-- scientific_v1/
|   |   |   |       |-- N6_ANALYSIS.json
|   |   |   |       |-- N6_ANALYSIS.md
|   |   |   |       |-- N6_ATTEMPTS.jsonl
|   |   |   |       |-- N6_PROVIDER_CALLS.jsonl
|   |   |   |       `-- N6_RESULTS.jsonl
|   |   |   `-- support/
|   |   |       |-- attriguard_a14_v2/
|   |   |       |   |-- ATTRIGUARD_A14_V2_FINAL_ADAPTER_PREFREEZE.json
|   |   |       |   |-- ATTRIGUARD_A14_V2_INTERFACE_DISCOVERY.json
|   |   |       |   |-- ATTRIGUARD_A14_V2_NO_MODEL_PREFLIGHT.json
|   |   |       |   |-- ATTRIGUARD_A14_V2_SOURCE_CORPUS_PREFREEZE.json
|   |   |       |   |-- scientific_v1/
|   |   |       |   |   |-- ATTRIGUARD_A14_V2_SCIENTIFIC_FREEZE.json
|   |   |       |   |   |-- PROVIDER_CALLS.jsonl
|   |   |       |   |   |-- RUN_SUMMARY.json
|   |   |       |   |   |-- SCIENTIFIC_ANALYSIS.json
|   |   |       |   |   |-- SCIENTIFIC_ATTEMPTS.jsonl
|   |   |       |   |   `-- SCIENTIFIC_RESULTS.jsonl
|   |   |       |   `-- synthetic_smoke_v1/
|   |   |       |       |-- SYNTHETIC_SMOKE_PROTOCOL.json
|   |   |       |       `-- SYNTHETIC_SMOKE_RESULTS.json
|   |   |       |-- ATTRIGUARD_A14_V2_00_verify_source_and_discover.py
|   |   |       |-- ATTRIGUARD_A14_V2_01_adapter.py
|   |   |       |-- ATTRIGUARD_A14_V2_02_freeze_and_no_model_preflight.py
|   |   |       |-- ATTRIGUARD_A14_V2_03_synthetic_api_smoke.py
|   |   |       |-- ATTRIGUARD_A14_V2_04_freeze_science.py
|   |   |       |-- ATTRIGUARD_A14_V2_05_run_science.py
|   |   |       |-- ATTRIGUARD_A14_V2_06_analyze_science.py
|   |   |       |-- ATTRIGUARD_A14_V2_FINAL_ADAPTER_SPEC.md
|   |   |       |-- ATTRIGUARD_A14_V2_PREFREEZE_PLAN.md
|   |   |       |-- ATTRIGUARD_A14_V2_SCIENTIFIC_PROTOCOL_SPEC.md
|   |   |       |-- ATTRIGUARD_A14_V2_SYNTHETIC_API_SMOKE_SPEC.md
|   |   |       |-- N6_00_build.log
|   |   |       |-- N6_01_scope_audit.log
|   |   |       |-- N6_02_freeze.log
|   |   |       |-- N6_04_technical_preflight.log
|   |   |       |-- N6_04_technical_preflight_v1_2_FAILED_STALE_FILENAME.log
|   |   |       |-- N6_04_technical_preflight_v1_2_PATCHED.log
|   |   |       |-- N6_05_science.log
|   |   |       |-- N6_06_analysis.log
|   |   |       |-- N6_ATTRIGUARD_N3_PREFREEZE_v1/
|   |   |       |   |-- N6_00_build_design.py
|   |   |       |   |-- N6_01_scope_audit_cli.py
|   |   |       |   |-- N6_02_freeze_protocol.py
|   |   |       |   |-- n6_common.py
|   |   |       |   |-- N6_PROTOCOL_SPEC.md
|   |   |       |   |-- PACKAGE_SHA256.txt
|   |   |       |   `-- README.md
|   |   |       |-- N6_ATTRIGUARD_N3_PREFREEZE_v1_out/
|   |   |       |   |-- N6_ATTRIGUARD_SCOPE_AUDIT.jsonl
|   |   |       |   |-- N6_DESIGN_DRAFT.json
|   |   |       |   |-- N6_SCIENTIFIC_PREFREEZE.json
|   |   |       |   |-- N6_SCIENTIFIC_PREFREEZE.md
|   |   |       |   `-- N6_TECHNICAL_AMENDMENT_v1_2.json
|   |   |       `-- N6_ATTRIGUARD_N3_TECH_AMENDMENT_v1_2/
|   |   |           |-- N6_03_paired_adapter.py
|   |   |           |-- N6_04_no_model_preflight_and_amend.py
|   |   |           |-- N6_05_run_science.py
|   |   |           |-- N6_06_analyze.py
|   |   |           |-- n6_tech_common.py
|   |   |           |-- N6_TECHNICAL_AMENDMENT_SPEC_v1_2.md
|   |   |           |-- PACKAGE_SHA256.txt
|   |   |           |-- PREOUTCOME_PATCH_RECORD.txt
|   |   |           `-- README.md
|   |   |-- 07_causalarmor/
|   |   |   |-- activation_audit/
|   |   |   |   |-- decision_inventory.jsonl
|   |   |   |   |-- PREP_REPORT.md
|   |   |   |   |-- protocol.json
|   |   |   |   |-- REPORT.md
|   |   |   |   |-- results.json
|   |   |   |   |-- sanitizer_checkpoint.jsonl
|   |   |   |   |-- sanitizer_jobs.jsonl
|   |   |   |   `-- sanitizer_results.jsonl
|   |   |   |-- README.md
|   |   |   |-- reconstruction_results/
|   |   |   |   |-- FINAL_ARTIFACT_SHA256.txt
|   |   |   |   |-- P0B3_ANALYSIS.json
|   |   |   |   |-- P0B3_CLEAN_FULL_RERUN_COMPLETE.json
|   |   |   |   |-- P0B3_CLEAN_RERUN_CAPACITY_FINALIZATION.json
|   |   |   |   |-- P0B3_CLEAN_RERUN_CAPACITY_FINALIZATION.md
|   |   |   |   |-- P0B3_CLEAN_RERUN_FINAL_SHA256.txt
|   |   |   |   |-- P0B3_DEFENSE_EVENTS.jsonl
|   |   |   |   |-- P0B3_LIVE_IMPLEMENTATION_FREEZE.json
|   |   |   |   |-- P0B3_LIVE_PREFLIGHT.md
|   |   |   |   |-- P0B3_PROVIDER_CALLS.jsonl
|   |   |   |   |-- P0B3_REPORT.md
|   |   |   |   |-- P0B3_SCIENCE_ROWS.jsonl
|   |   |   |   |-- P0B3_SUITE_RESULTS.csv
|   |   |   |   `-- P0B3_TECHNICAL_CALLS.jsonl
|   |   |   `-- support/
|   |   |       |-- A15a_00_prepare_freeze.py
|   |   |       |-- A15a_01_sanitize.py
|   |   |       |-- A15a_02_analyze.py
|   |   |       |-- a15a_common.py
|   |   |       |-- A15a_PROTOCOL_NOTE.md
|   |   |       |-- A15A_SELECTIVITY_CONSEQUENCE_PACKAGE/
|   |   |       |   |-- A15a_00_prepare_freeze.py
|   |   |       |   |-- A15a_01_sanitize.py
|   |   |       |   |-- A15a_02_analyze.py
|   |   |       |   |-- a15a_common.py
|   |   |       |   |-- A15a_PROTOCOL_NOTE.md
|   |   |       |   |-- README.md
|   |   |       |   `-- SHA256SUMS.txt
|   |   |       |-- P0B3_ACT_freeze.log
|   |   |       |-- P0B3_ACT_result.log
|   |   |       |-- P0B3_ACT_RUN_v1/
|   |   |       |   |-- FINAL_ARTIFACT_SHA256.txt
|   |   |       |   |-- P0B3_ACT_FREEZE.json
|   |   |       |   |-- P0B3_ACT_FREEZE.md
|   |   |       |   |-- P0B3_ACT_REPORT.md
|   |   |       |   |-- P0B3_ACT_RESULT.json
|   |   |       |   `-- P0B3_ACT_SPLIT.csv
|   |   |       |-- P0B3_ACT_SHADOW_freeze.log
|   |   |       |-- P0B3_ACT_SHADOW_result.log
|   |   |       |-- P0B3_ACT_SHADOW_RUN_v1/
|   |   |       |   |-- FINAL_ARTIFACT_SHA256.txt
|   |   |       |   |-- P0B3_ACT_SHADOW_FREEZE.json
|   |   |       |   |-- P0B3_ACT_SHADOW_FREEZE.md
|   |   |       |   |-- P0B3_ACT_SHADOW_REPORT.md
|   |   |       |   |-- P0B3_ACT_SHADOW_RESULT.json
|   |   |       |   `-- P0B3_ACT_SHADOW_SPLIT.csv
|   |   |       |-- P0B3_ACT_SHADOW_SUPPLEMENT_v1/
|   |   |       |   |-- P0B3_ACT_SHADOW_00_freeze.py
|   |   |       |   |-- P0B3_ACT_SHADOW_01_run.py
|   |   |       |   |-- p0b3_act_shadow_common.py
|   |   |       |   |-- PACKAGE_SHA256.txt
|   |   |       |   `-- README.md
|   |   |       |-- P0B3_ACT_ZERO_CALL_v1/
|   |   |       |   |-- P0B3_ACT_00_freeze.py
|   |   |       |   |-- P0B3_ACT_01_run.py
|   |   |       |   |-- p0b3_act_common.py
|   |   |       |   |-- PACKAGE_SHA256.txt
|   |   |       |   `-- README.md
|   |   |       |-- P0B3_AUTHOR_RUN_HISTORY/
|   |   |       |   |-- P0B3_ATTEMPT0_16K_TECHNICAL_ABORT_992_OF_1046/
|   |   |       |   |   |-- P0B3_DEFENSE_EVENTS.jsonl
|   |   |       |   |   |-- P0B3_ERRORS.jsonl
|   |   |       |   |   |-- P0B3_LIVE_IMPLEMENTATION_FREEZE.json
|   |   |       |   |   |-- P0B3_LIVE_PREFLIGHT.md
|   |   |       |   |   |-- P0B3_PROVIDER_CALLS.jsonl
|   |   |       |   |   |-- P0B3_SCIENCE_CONSOLE.log
|   |   |       |   |   |-- P0B3_SCIENCE_ROWS.jsonl
|   |   |       |   |   `-- P0B3_TECHNICAL_CALLS.jsonl
|   |   |       |   |-- P0B3_ATTEMPT0_16K_TECHNICAL_ABORT_992_OF_1046_FILES_SHA256.txt
|   |   |       |   `-- P0B3_ATTEMPT0_STATUS.md
|   |   |       |-- P0B3_CAUSALARMOR_CALIBRATION_FREEZE_COMPLETE_v1.zip
|   |   |       |-- P0B3_CAUSALARMOR_CALIBRATION_FREEZE_RUN_v1/
|   |   |       |   |-- FINAL_ARTIFACT_SHA256.txt
|   |   |       |   |-- P0B3_BENIGN_97_TASKS.csv
|   |   |       |   |-- P0B3_ENV_POP_PREFLIGHT.json
|   |   |       |   |-- P0B3_ENV_POP_PREFLIGHT.md
|   |   |       |   |-- P0B3_LEGACY_629_PAIRS.csv
|   |   |       |   |-- P0B3_PRIMARY_949_PAIRS.csv
|   |   |       |   |-- P0B3_PROTOCOL_FREEZE.json
|   |   |       |   |-- P0B3_PROTOCOL_FREEZE.md
|   |   |       |   `-- P0B3_SUITE_COUNTS.csv
|   |   |       |-- P0B3_CAUSALARMOR_CALIBRATION_FREEZE_v1/
|   |   |       |   |-- P0B3_00_environment_population_preflight.py
|   |   |       |   |-- P0B3_01_freeze_protocol.py
|   |   |       |   |-- P0B3_02_hash_outputs.py
|   |   |       |   |-- P0B3_CAUSALARMOR_CALIBRATION_FREEZE_v1_RUN_COMMANDS.txt
|   |   |       |   |-- p0b3_common.py
|   |   |       |   |-- P0B3_CONFIG.json
|   |   |       |   |-- P0B3_POPULATION_ADJUDICATION_v1.md
|   |   |       |   |-- PACKAGE_SHA256.txt
|   |   |       |   `-- README.md
|   |   |       |-- P0B3_CAUSALARMOR_CLEAN_FULL_RERUN_v1/
|   |   |       |   |-- P0B3_00_ARCHIVE_ATTEMPT0.sh
|   |   |       |   |-- P0B3_10_verify_clean_start.py
|   |   |       |   |-- P0B3_20_finalize_32k_before_science.py
|   |   |       |   |-- P0B3_90_validate_complete_clean_rerun.py
|   |   |       |   |-- P0B3_CLEAN_FULL_RERUN_RUN_COMMANDS.txt
|   |   |       |   |-- P0B3_RUN_CLEAN_FULL_RERUN.sh
|   |   |       |   |-- PACKAGE_SHA256.txt
|   |   |       |   `-- README.md
|   |   |       |-- P0B3_CAUSALARMOR_LIVE_v1/
|   |   |       |   |-- FREEZE_BINDING.json
|   |   |       |   |-- FROZEN_INPUTS/
|   |   |       |   |   |-- FINAL_ARTIFACT_SHA256.txt
|   |   |       |   |   |-- P0B3_BENIGN_97_TASKS.csv
|   |   |       |   |   |-- P0B3_ENV_POP_PREFLIGHT.json
|   |   |       |   |   |-- P0B3_LEGACY_629_PAIRS.csv
|   |   |       |   |   |-- P0B3_PRIMARY_949_PAIRS.csv
|   |   |       |   |   |-- P0B3_PROTOCOL_FREEZE.json
|   |   |       |   |   `-- P0B3_SUITE_COUNTS.csv
|   |   |       |   |-- P0B3_10_live_preflight.py
|   |   |       |   |-- P0B3_20_run_science.py
|   |   |       |   |-- P0B3_30_analyze.py
|   |   |       |   |-- P0B3_40_hash_outputs.py
|   |   |       |   |-- P0B3_CAUSALARMOR_LIVE_v1_RUN_COMMANDS.txt
|   |   |       |   |-- p0b3_live_common.py
|   |   |       |   |-- P0B3_RUN_SCIENCE_THEN_ANALYZE.sh
|   |   |       |   |-- PACKAGE_SHA256.txt
|   |   |       |   `-- README.md
|   |   |       |-- P0B3_CAUSALARMOR_LIVE_v1.zip
|   |   |       |-- P0BV_AGENTDOJO_VERSION_AUDIT_v1/
|   |   |       |   |-- P0BV_00_freeze_analysis.py
|   |   |       |   |-- P0BV_01_run_compatibility.py
|   |   |       |   |-- P0BV_02_hash_outputs.py
|   |   |       |   |-- p0bv_common.py
|   |   |       |   |-- P0BV_CONFIG.json
|   |   |       |   |-- PACKAGE_SHA256.txt
|   |   |       |   `-- README.md
|   |   |       `-- P0BV_AGENTDOJO_VERSION_RUN_v1/
|   |   |           |-- FINAL_ARTIFACT_SHA256.txt
|   |   |           |-- P0BV_AGENTWATCHER_ATTACK_PAIR_VERSION_MAP.csv
|   |   |           |-- P0BV_ANALYSIS_FREEZE.json
|   |   |           |-- P0BV_ANALYSIS_FREEZE.md
|   |   |           |-- P0BV_INJECTION_TASK_DIFFS.csv
|   |   |           |-- P0BV_INJECTION_TASK_SIGNATURES.jsonl
|   |   |           |-- P0BV_INPUT_MANIFEST.tsv
|   |   |           |-- P0BV_PAPER_POPULATION_IMPACT.csv
|   |   |           |-- P0BV_POPULATION_FREEZE.json
|   |   |           |-- P0BV_RESULT.json
|   |   |           |-- P0BV_SUITE_SUMMARY.csv
|   |   |           |-- P0BV_SUMMARY.md
|   |   |           |-- P0BV_TOOL_DIFFS.csv
|   |   |           |-- P0BV_USER_TASK_DIFFS.csv
|   |   |           `-- P0BV_USER_TASK_SIGNATURES.jsonl
|   |   |-- 08_live_end_to_end/
|   |   |   |-- code_and_protocol/
|   |   |   |   |-- code/
|   |   |   |   |   |-- E2E_A4_00_build_and_test_paef.py
|   |   |   |   |   |-- e2e_attacks.py
|   |   |   |   |   |-- E2E_PRE_01_build_contexts_schedule.py
|   |   |   |   |   |-- E2E_PRE_02_analysis.py
|   |   |   |   |   |-- E2E_PRE_03_science_runner.py
|   |   |   |   |   |-- E2E_PRE_04_build_freeze.py
|   |   |   |   |   |-- E2E_PRE_05_live_dev_preflight.py
|   |   |   |   |   |-- E2E_PRE_06_seal.py
|   |   |   |   |   |-- E2E_PRE_07_auditpath_dev_preflight.py
|   |   |   |   |   |-- E2E_PRE_08_reseal.py
|   |   |   |   |   |-- E2E_PRE_09_verify_seal.py
|   |   |   |   |   |-- E2E_PRE_10_yaml_roundtrip_audit.py
|   |   |   |   |   `-- paef_oracle.py
|   |   |   |   |-- package_PRESCIENCE_OUTPUTS.sh
|   |   |   |   |-- PACKAGE_SHA256.txt
|   |   |   |   |-- README_START_HERE.md
|   |   |   |   |-- run_FINAL_PRESCIENCE_BUILD.sh
|   |   |   |   |-- run_LIVE_DEV_PREFLIGHT_AND_SEAL.sh
|   |   |   |   |-- run_SCIENCE_NOHUP.sh
|   |   |   |   `-- USENIX27_FINAL_EXPERIMENT_FREEZE_E2E_ATTRIGUARD_v4_FINAL_CODING_FREEZE_RECONCILED.md
|   |   |   |-- frozen_results/
|   |   |   |   |-- A2_A3_PREP_CONSOLE.log
|   |   |   |   |-- A3_UNBLIND_CONSOLE.log
|   |   |   |   |-- code/
|   |   |   |   |   |-- E2E_A1_00_build_census.py
|   |   |   |   |   |-- E2E_A1_01_multicall_source_audit.py
|   |   |   |   |   |-- E2E_A2_00_fix_a1_provenance.py
|   |   |   |   |   |-- E2E_A2_01_build_auth_alt_and_blinded_packet.py
|   |   |   |   |   |-- E2E_A3_00_finalize_blinded_gate.py
|   |   |   |   |   |-- run_E2E_A1_phase0_2.sh
|   |   |   |   |   `-- run_E2E_A2_A3_prepare.sh
|   |   |   |   |-- E2E_SCIENCE_AUTHOR_RUN.log
|   |   |   |   |-- E2E_SCIENCE_AUTHOR_RUN.pid
|   |   |   |   |-- FINAL_PRESCIENCE_BUILD.log
|   |   |   |   |-- input_lock/
|   |   |   |   |   `-- A13_C0_INPUT_BUNDLE_v1/
|   |   |   |   |       |-- AGENTDOJO_PIP_SHOW.txt
|   |   |   |   |       |-- agentdojo_source/
|   |   |   |   |       |   |-- agent_pipeline/
|   |   |   |   |       |   |   |-- agent_pipeline.py
|   |   |   |   |       |   |   |-- base_pipeline_element.py
|   |   |   |   |       |   |   |-- basic_elements.py
|   |   |   |   |       |   |   |-- errors.py
|   |   |   |   |       |   |   |-- ground_truth_pipeline.py
|   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |       |   |   |-- llms/
|   |   |   |   |       |   |   |   |-- anthropic_llm.py
|   |   |   |   |       |   |   |   |-- cohere_llm.py
|   |   |   |   |       |   |   |   |-- google_llm.py
|   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |-- local_llm.py
|   |   |   |   |       |   |   |   |-- openai_llm.py
|   |   |   |   |       |   |   |   `-- prompting_llm.py
|   |   |   |   |       |   |   |-- pi_detector.py
|   |   |   |   |       |   |   |-- planner.py
|   |   |   |   |       |   |   `-- tool_execution.py
|   |   |   |   |       |   |-- ast_utils.py
|   |   |   |   |       |   |-- attacks/
|   |   |   |   |       |   |   |-- attack_registry.py
|   |   |   |   |       |   |   |-- base_attacks.py
|   |   |   |   |       |   |   |-- baseline_attacks.py
|   |   |   |   |       |   |   |-- dos_attacks.py
|   |   |   |   |       |   |   |-- important_instructions_attacks.py
|   |   |   |   |       |   |   `-- __init__.py
|   |   |   |   |       |   |-- base_tasks.py
|   |   |   |   |       |   |-- benchmark.py
|   |   |   |   |       |   |-- data/
|   |   |   |   |       |   |   |-- suites/
|   |   |   |   |       |   |   |   |-- banking/
|   |   |   |   |       |   |   |   |   |-- environment.yaml
|   |   |   |   |       |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |       |   |   |   |-- slack/
|   |   |   |   |       |   |   |   |   |-- environment.yaml
|   |   |   |   |       |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |       |   |   |   |-- travel/
|   |   |   |   |       |   |   |   |   |-- environment.yaml
|   |   |   |   |       |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |       |   |   |   `-- workspace/
|   |   |   |   |       |   |   |       |-- environment.yaml
|   |   |   |   |       |   |   |       |-- gpt_prompts.txt
|   |   |   |   |       |   |   |       |-- include/
|   |   |   |   |       |   |   |       |   |-- calendar.yaml
|   |   |   |   |       |   |   |       |   |-- cloud_drive.yaml
|   |   |   |   |       |   |   |       |   `-- inbox.yaml
|   |   |   |   |       |   |   |       `-- injection_vectors.yaml
|   |   |   |   |       |   |   `-- system_messages.yaml
|   |   |   |   |       |   |-- default_suites/
|   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |       |   |   |-- v1/
|   |   |   |   |       |   |   |   |-- banking/
|   |   |   |   |       |   |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |   |-- injection_tasks.py
|   |   |   |   |       |   |   |   |   |-- task_suite.py
|   |   |   |   |       |   |   |   |   `-- user_tasks.py
|   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |-- slack/
|   |   |   |   |       |   |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |   |-- injection_tasks.py
|   |   |   |   |       |   |   |   |   |-- task_suite.py
|   |   |   |   |       |   |   |   |   `-- user_tasks.py
|   |   |   |   |       |   |   |   |-- tools/
|   |   |   |   |       |   |   |   |   |-- banking_client.py
|   |   |   |   |       |   |   |   |   |-- calendar_client.py
|   |   |   |   |       |   |   |   |   |-- cloud_drive_client.py
|   |   |   |   |       |   |   |   |   |-- email_client.py
|   |   |   |   |       |   |   |   |   |-- file_reader.py
|   |   |   |   |       |   |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |   |-- slack.py
|   |   |   |   |       |   |   |   |   |-- travel_booking_client.py
|   |   |   |   |       |   |   |   |   |-- types.py
|   |   |   |   |       |   |   |   |   |-- user_account.py
|   |   |   |   |       |   |   |   |   `-- web.py
|   |   |   |   |       |   |   |   |-- travel/
|   |   |   |   |       |   |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |   |-- injection_tasks.py
|   |   |   |   |       |   |   |   |   |-- task_suite.py
|   |   |   |   |       |   |   |   |   `-- user_tasks.py
|   |   |   |   |       |   |   |   `-- workspace/
|   |   |   |   |       |   |   |       |-- __init__.py
|   |   |   |   |       |   |   |       |-- injection_tasks.py
|   |   |   |   |       |   |   |       |-- task_suite.py
|   |   |   |   |       |   |   |       `-- user_tasks.py
|   |   |   |   |       |   |   |-- v1_1/
|   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   `-- travel/
|   |   |   |   |       |   |   |       `-- user_tasks.py
|   |   |   |   |       |   |   |-- v1_1_1/
|   |   |   |   |       |   |   |   |-- banking/
|   |   |   |   |       |   |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |   `-- user_tasks.py
|   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |-- slack/
|   |   |   |   |       |   |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |   `-- user_tasks.py
|   |   |   |   |       |   |   |   |-- travel/
|   |   |   |   |       |   |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |   |-- injection_tasks.py
|   |   |   |   |       |   |   |   |   `-- user_tasks.py
|   |   |   |   |       |   |   |   `-- workspace/
|   |   |   |   |       |   |   |       `-- user_tasks.py
|   |   |   |   |       |   |   |-- v1_1_2/
|   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |-- travel/
|   |   |   |   |       |   |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |   `-- injection_tasks.py
|   |   |   |   |       |   |   |   `-- workspace/
|   |   |   |   |       |   |   |       |-- __init__.py
|   |   |   |   |       |   |   |       |-- injection_tasks.py
|   |   |   |   |       |   |   |       `-- user_tasks.py
|   |   |   |   |       |   |   |-- v1_2/
|   |   |   |   |       |   |   |   |-- banking/
|   |   |   |   |       |   |   |   |   `-- injection_tasks.py
|   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   |-- slack/
|   |   |   |   |       |   |   |   |   `-- user_tasks.py
|   |   |   |   |       |   |   |   |-- travel/
|   |   |   |   |       |   |   |   |   |-- injection_tasks.py
|   |   |   |   |       |   |   |   |   `-- user_tasks.py
|   |   |   |   |       |   |   |   `-- workspace/
|   |   |   |   |       |   |   |       |-- injection_tasks.py
|   |   |   |   |       |   |   |       `-- user_tasks.py
|   |   |   |   |       |   |   |-- v1_2_1/
|   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |       |   |   |   `-- workspace/
|   |   |   |   |       |   |   |       `-- injection_tasks.py
|   |   |   |   |       |   |   `-- v1_2_2/
|   |   |   |   |       |   |       |-- banking/
|   |   |   |   |       |   |       |   |-- __init__.py
|   |   |   |   |       |   |       |   `-- user_tasks.py
|   |   |   |   |       |   |       |-- __init__.py
|   |   |   |   |       |   |       `-- workspace/
|   |   |   |   |       |   |           |-- __init__.py
|   |   |   |   |       |   |           `-- user_tasks.py
|   |   |   |   |       |   |-- functions_runtime.py
|   |   |   |   |       |   |-- __init__.py
|   |   |   |   |       |   |-- logging.py
|   |   |   |   |       |   |-- models.py
|   |   |   |   |       |   |-- scripts/
|   |   |   |   |       |   |   |-- benchmark.py
|   |   |   |   |       |   |   |-- check_suites.py
|   |   |   |   |       |   |   `-- __init__.py
|   |   |   |   |       |   |-- strenum.py
|   |   |   |   |       |   |-- task_suite/
|   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |       |   |   |-- load_suites.py
|   |   |   |   |       |   |   |-- task_combinators.py
|   |   |   |   |       |   |   `-- task_suite.py
|   |   |   |   |       |   |-- types.py
|   |   |   |   |       |   `-- yaml_loader.py
|   |   |   |   |       |-- AGENTDOJO_SOURCE_PATH.txt
|   |   |   |   |       |-- FILE_LIST.txt
|   |   |   |   |       |-- FILE_SHA256.txt
|   |   |   |   |       |-- PIP_FREEZE.txt
|   |   |   |   |       `-- project_files/
|   |   |   |   |           |-- A13.py
|   |   |   |   |           |-- A13_R1B_Llama_BoundarySafe.py
|   |   |   |   |           |-- A13_R1_Llama.py
|   |   |   |   |           |-- A13_R2_Llama.py
|   |   |   |   |           |-- A13_R2_Llama_Server_Smoke.py
|   |   |   |   |           |-- A13_R3_Gemini.py
|   |   |   |   |           |-- A13_R3_Gemini.scaffold.bak
|   |   |   |   |           |-- A14_MINIMAL_P1xP3_FACTORIAL_PACKAGE.zip
|   |   |   |   |           |-- A15a_00_prepare_freeze.py
|   |   |   |   |           |-- A15a_01_sanitize.py
|   |   |   |   |           |-- A15a_02_analyze.py
|   |   |   |   |           |-- a15a_common.py
|   |   |   |   |           |-- A15a_PROTOCOL_NOTE.md
|   |   |   |   |           |-- a15a_sanitizer_run.log
|   |   |   |   |           |-- A15A_SELECTIVITY_CONSEQUENCE_PACKAGE/
|   |   |   |   |           |   |-- A15a_00_prepare_freeze.py
|   |   |   |   |           |   |-- A15a_01_sanitize.py
|   |   |   |   |           |   |-- A15a_02_analyze.py
|   |   |   |   |           |   |-- a15a_common.py
|   |   |   |   |           |   `-- A15a_PROTOCOL_NOTE.md
|   |   |   |   |           |-- A15A_SELECTIVITY_CONSEQUENCE_PACKAGE.zip
|   |   |   |   |           |-- archive/
|   |   |   |   |           |   `-- a12_run2_6cells/
|   |   |   |   |           |       `-- preregistration_A13.json
|   |   |   |   |           |-- falsify/
|   |   |   |   |           |   `-- preregistration_A13.json
|   |   |   |   |           |-- logs/
|   |   |   |   |           |   |-- a13.log
|   |   |   |   |           |   |-- a13_r1b_llama.log
|   |   |   |   |           |   |-- a13_r1b_llama.pid
|   |   |   |   |           |   |-- a13_r1_llama.log
|   |   |   |   |           |   |-- a13_r1_llama.pid
|   |   |   |   |           |   |-- a13_r2_llama.log
|   |   |   |   |           |   |-- a13_r2_llama.pid
|   |   |   |   |           |   |-- vllm_a13.log
|   |   |   |   |           |   |-- vllm_a13_r1_llama.log
|   |   |   |   |           |   |-- vllm_a13_r1_llama.pid
|   |   |   |   |           |   |-- vllm_a13_r2_llama.log
|   |   |   |   |           |   `-- vllm_a13_r2_llama.pid
|   |   |   |   |           |-- P3_HARDENING_COMPLETE_v1.zip
|   |   |   |   |           |-- P3_HARDENING_COMPLETE_v1.zip.sha256
|   |   |   |   |           |-- P3_HARDENING_RUN_v1/
|   |   |   |   |           |   |-- P3_A13_LEAVE_ONE_SUITE_OUT.csv
|   |   |   |   |           |   |-- P3_A13_LEAVE_ONE_TASK_OUT.csv
|   |   |   |   |           |   |-- P3_A13_TASK_SPAN_DIAGNOSTICS.csv
|   |   |   |   |           |   |-- P3_A15A_LEAVE_ONE_SUITE_OUT.csv
|   |   |   |   |           |   |-- P3_A15A_SUITE_SUMMARY.csv
|   |   |   |   |           |   |-- P3_ANALYSIS_FREEZE.json
|   |   |   |   |           |   |-- P3_ANALYSIS_FREEZE.md
|   |   |   |   |           |   |-- P3_HARDENING.json
|   |   |   |   |           |   |-- P3_HARDENING_SUMMARY.md
|   |   |   |   |           |   |-- P3_P2B_CROSS_MODEL_DECISIONS.csv
|   |   |   |   |           |   |-- P3_P2B_LEAVE_ONE_DECISION_OUT.csv
|   |   |   |   |           |   |-- P3_P2B_LEAVE_ONE_FUNCTION_OUT.csv
|   |   |   |   |           |   |-- P3_P2B_LEAVE_ONE_SUITE_OUT.csv
|   |   |   |   |           |   |-- P3_P2B_MASKED_ROWS.csv
|   |   |   |   |           |   |-- P3_P2B_MODEL_DECISION_CELLS.csv
|   |   |   |   |           |   |-- P3_P2B_ORIGINAL_QWEN_WEAK_RECURRENCE.csv
|   |   |   |   |           |   |-- P3_P2B_SUBGROUP_SUMMARY.csv
|   |   |   |   |           |   `-- P3_P2B_WITHIN_STRATUM.csv
|   |   |   |   |           |-- P3_ZERO_CALL_HARDENING_v1/
|   |   |   |   |           |   |-- P3_00_freeze_analysis.py
|   |   |   |   |           |   |-- P3_01_run_hardening.py
|   |   |   |   |           |   |-- P3_02_hash_outputs.py
|   |   |   |   |           |   `-- P3_CONFIG.json
|   |   |   |   |           |-- P3_ZERO_CALL_HARDENING_v1.zip
|   |   |   |   |           |-- start_A13_R1_Llama_vLLM.sh
|   |   |   |   |           `-- start_A13_R2_Llama_vLLM.sh
|   |   |   |   |-- LIVE_DEV_PREFLIGHT_AND_SEAL.log
|   |   |   |   |-- PATCH1_RESEAL.log
|   |   |   |   |-- PATCH2B_RESEAL.log
|   |   |   |   |-- PATCH2C_RESEAL.log
|   |   |   |   |-- PATCH2_RESEAL.log
|   |   |   |   |-- PHASE0_2_CONSOLE.log
|   |   |   |   |-- PHASE_A1_START_HERE.md
|   |   |   |   |-- prefreeze/
|   |   |   |   |   |-- final_prescience_build/
|   |   |   |   |   |   |-- AGENTDOJO_V1_RETAINED_SOURCE_SHA256.tsv
|   |   |   |   |   |   |-- ANALYSIS_SELFTEST.json
|   |   |   |   |   |   |-- ANALYSIS_SELFTEST_PATCH1.json
|   |   |   |   |   |   |-- ATTRIGUARD_EXTERNAL_OUTPUT_TOOLS.json
|   |   |   |   |   |   |-- CONTEXT_PAIR_DIFF_REPORT.json
|   |   |   |   |   |   |-- CONTEXT_RENDERED.jsonl
|   |   |   |   |   |   |-- DEV_AUDITPATH_PREFLIGHT/
|   |   |   |   |   |   |   `-- None-None-attriguard/
|   |   |   |   |   |   |       `-- workspace/
|   |   |   |   |   |   |           `-- user_task_8/
|   |   |   |   |   |   |               `-- none/
|   |   |   |   |   |   |                   `-- none.json
|   |   |   |   |   |   |-- DEV_AUDITPATH_PREFLIGHT.json
|   |   |   |   |   |   |-- DEV_LIVE_PREFLIGHT/
|   |   |   |   |   |   |   |-- OFF/
|   |   |   |   |   |   |   |   `-- None-None-nodefense/
|   |   |   |   |   |   |   |       `-- workspace/
|   |   |   |   |   |   |   |           `-- user_task_0/
|   |   |   |   |   |   |   |               `-- none/
|   |   |   |   |   |   |   |                   `-- none.json
|   |   |   |   |   |   |   `-- ON/
|   |   |   |   |   |   |       `-- None-None-attriguard/
|   |   |   |   |   |   |           `-- workspace/
|   |   |   |   |   |   |               `-- user_task_0/
|   |   |   |   |   |   |                   `-- none/
|   |   |   |   |   |   |                       `-- none.json
|   |   |   |   |   |   |-- DEV_LIVE_PREFLIGHT.json
|   |   |   |   |   |   |-- ENVIRONMENT_LOCK.json
|   |   |   |   |   |   |-- FREEZE.json
|   |   |   |   |   |   |-- INJECTION_CARRIER_TOOL_AUDIT.csv
|   |   |   |   |   |   |-- INJECTION_LOCATION_LEDGER.csv
|   |   |   |   |   |   |-- PAEF_ORACLE_FREEZE/
|   |   |   |   |   |   |   |-- A3_HASH_RECONCILIATION.json
|   |   |   |   |   |   |   |-- A3_OUTPUT_SHA256_RECONCILED.tsv
|   |   |   |   |   |   |   |-- CASE_012_FREE_TIME_RESOLUTION.json
|   |   |   |   |   |   |   |-- FINAL_OUTPUT_SHA256.tsv
|   |   |   |   |   |   |   |-- PAEF_MUTATION_TEST_REPORT.json
|   |   |   |   |   |   |   |-- PAEF_ORACLE_GATE_SUMMARY.json
|   |   |   |   |   |   |   |-- PAEF_RESOLUTION_LOG.md
|   |   |   |   |   |   |   |-- PAEF_SPECS/
|   |   |   |   |   |   |   |   |-- CASE_001.json
|   |   |   |   |   |   |   |   |-- CASE_002.json
|   |   |   |   |   |   |   |   |-- CASE_003.json
|   |   |   |   |   |   |   |   |-- CASE_004.json
|   |   |   |   |   |   |   |   |-- CASE_005.json
|   |   |   |   |   |   |   |   |-- CASE_006.json
|   |   |   |   |   |   |   |   |-- CASE_007.json
|   |   |   |   |   |   |   |   |-- CASE_008.json
|   |   |   |   |   |   |   |   |-- CASE_009.json
|   |   |   |   |   |   |   |   |-- CASE_010.json
|   |   |   |   |   |   |   |   |-- CASE_011.json
|   |   |   |   |   |   |   |   |-- CASE_012.json
|   |   |   |   |   |   |   |   |-- CASE_013.json
|   |   |   |   |   |   |   |   `-- CASE_014.json
|   |   |   |   |   |   |   `-- SOURCE_LOCKS.tsv
|   |   |   |   |   |   |-- PATCH1_PREIMAGE/
|   |   |   |   |   |   |   |-- E2E_PRE_02_analysis.py
|   |   |   |   |   |   |   `-- E2E_PRE_03_science_runner.py
|   |   |   |   |   |   |-- PATCH2B_PREIMAGE/
|   |   |   |   |   |   |   |-- E2E_PRE_03_science_runner.py
|   |   |   |   |   |   |   `-- E2E_PRE_10_yaml_roundtrip_audit.py
|   |   |   |   |   |   |-- PATCH2C_PREIMAGE/
|   |   |   |   |   |   |   `-- E2E_PRE_10_yaml_roundtrip_audit.py
|   |   |   |   |   |   |-- PATCH2_PREIMAGE/
|   |   |   |   |   |   |   |-- e2e_attacks.py
|   |   |   |   |   |   |   |-- E2E_PRE_02_analysis.py
|   |   |   |   |   |   |   |-- E2E_PRE_03_science_runner.py
|   |   |   |   |   |   |   |-- E2E_PRE_08_reseal.py
|   |   |   |   |   |   |   `-- E2E_PRE_09_verify_seal.py
|   |   |   |   |   |   |-- PRE_ENVIRONMENT_LOCKS.json
|   |   |   |   |   |   |-- PREFREEZE_COMPLETE.md
|   |   |   |   |   |   |-- PREFREEZE_SHA256.tsv
|   |   |   |   |   |   |-- PRESCIENCE_PATCH_RECONCILIATION.json
|   |   |   |   |   |   |-- PRE_SCIENCE_SHA256.tsv
|   |   |   |   |   |   |-- RANDOMIZATION_METADATA.json
|   |   |   |   |   |   |-- SCIENTIFIC_SCHEDULE.csv
|   |   |   |   |   |   |-- SOURCE_LOCKS.tsv
|   |   |   |   |   |   `-- YAML_DIRECTIVE_ROUNDTRIP_AUDIT.json
|   |   |   |   |   |-- phase0_2_author_run/
|   |   |   |   |   |   |-- 00_PROJECT_SNAPSHOT.json
|   |   |   |   |   |   |-- 01_A13_CENSUS_REPORT.json
|   |   |   |   |   |   |-- 01_A13_PRIMARY_DECISIONS.jsonl
|   |   |   |   |   |   |-- 02_ALT_CANDIDATES.jsonl
|   |   |   |   |   |   |-- 02_COHORT_AFTER_SOURCE_AUDIT.csv
|   |   |   |   |   |   |-- 02_MULTI_CALL_SOURCE_AUDIT.csv
|   |   |   |   |   |   |-- 02_SOURCE_AUDIT_SUMMARY.json
|   |   |   |   |   |   |-- COHORT_CENSUS.csv
|   |   |   |   |   |   |-- COHORT_SUMMARY.json
|   |   |   |   |   |   |-- EXCLUSIONS.csv
|   |   |   |   |   |   |-- FINAL_OUTPUT_SHA256.tsv
|   |   |   |   |   |   |-- OUTPUT_SHA256.tsv
|   |   |   |   |   |   |-- PHASE0_2_AUTHOR_RUN.log
|   |   |   |   |   |   `-- STRICT_SUBSET.csv
|   |   |   |   |   `-- phase3_author_run/
|   |   |   |   |       |-- A1_PROVENANCE_AMENDMENT/
|   |   |   |   |       |   |-- A1_PROVENANCE_AMENDMENT.json
|   |   |   |   |       |   `-- A1_SOURCE_AUDIT_PROVENANCE_AMENDMENT.csv
|   |   |   |   |       |-- A2_A3_PREP/
|   |   |   |   |       |   |-- A2_A3_PREP_SUMMARY.json
|   |   |   |   |       |   |-- AUTH_ALT_LEDGER_DRAFT.jsonl
|   |   |   |   |       |   |-- BLINDED_RATER_DECISIONS_TEMPLATE.csv
|   |   |   |   |       |   |-- BLINDED_RATER_PACKET/
|   |   |   |   |       |   |   |-- CASE_001.md
|   |   |   |   |       |   |   |-- CASE_002.md
|   |   |   |   |       |   |   |-- CASE_003.md
|   |   |   |   |       |   |   |-- CASE_004.md
|   |   |   |   |       |   |   |-- CASE_005.md
|   |   |   |   |       |   |   |-- CASE_006.md
|   |   |   |   |       |   |   |-- CASE_007.md
|   |   |   |   |       |   |   |-- CASE_008.md
|   |   |   |   |       |   |   |-- CASE_009.md
|   |   |   |   |       |   |   |-- CASE_010.md
|   |   |   |   |       |   |   |-- CASE_011.md
|   |   |   |   |       |   |   |-- CASE_012.md
|   |   |   |   |       |   |   |-- CASE_013.md
|   |   |   |   |       |   |   `-- CASE_014.md
|   |   |   |   |       |   |-- BLINDED_RATER_PACKET_FOR_REVIEW.zip
|   |   |   |   |       |   |-- CASE_MAP.csv
|   |   |   |   |       |   `-- RATER_INSTRUCTIONS.md
|   |   |   |   |       |-- A2_A3_PREP_AUTHOR_RUN.log
|   |   |   |   |       |-- A2_A3_PREP_OUTPUT_SHA256.tsv
|   |   |   |   |       `-- A3_UNBLIND_SCOPE_FREEZE/
|   |   |   |   |           |-- A3_UNBLIND_SCOPE_FREEZE.log
|   |   |   |   |           |-- ATTRIGUARD_SCOPE_AUDIT.csv
|   |   |   |   |           |-- BLINDED_RATER_DECISIONS_LOCKED.csv
|   |   |   |   |           |-- FINAL_AUTH_ALT_LEDGER.jsonl
|   |   |   |   |           |-- FINAL_COHORT.csv
|   |   |   |   |           |-- FINAL_COHORT_SUMMARY.json
|   |   |   |   |           |-- FINAL_EXCLUSIONS.csv
|   |   |   |   |           |-- FINAL_OUTPUT_SHA256.tsv
|   |   |   |   |           `-- UNBLINDED_RATER_RESULTS.csv
|   |   |   |   |-- PROMOTED_E2E_SHA256.tsv
|   |   |   |   `-- scientific_v1/
|   |   |   |       |-- ATTEMPTS.jsonl
|   |   |   |       |-- raw/
|   |   |   |       |   |-- 0001_CASE_001_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0002_CASE_001_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0003_CASE_001_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0004_CASE_001_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0005_CASE_001_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0006_CASE_001_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0007_CASE_001_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0008_CASE_001_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0009_CASE_001_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0010_CASE_001_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0011_CASE_001_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0012_CASE_001_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0013_CASE_001_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0014_CASE_001_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0015_CASE_001_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0016_CASE_001_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0017_CASE_001_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0018_CASE_001_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0019_CASE_001_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0020_CASE_001_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0021_CASE_001_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0022_CASE_001_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0023_CASE_001_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0024_CASE_001_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0025_CASE_001_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0026_CASE_001_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0027_CASE_001_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0028_CASE_001_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0029_CASE_001_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_0.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0030_CASE_001_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_0/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0031_CASE_002_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0032_CASE_002_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0033_CASE_002_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0034_CASE_002_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0035_CASE_002_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0036_CASE_002_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0037_CASE_002_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0038_CASE_002_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0039_CASE_002_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0040_CASE_002_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0041_CASE_002_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0042_CASE_002_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0043_CASE_002_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0044_CASE_002_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0045_CASE_002_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0046_CASE_002_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0047_CASE_002_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0048_CASE_002_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0049_CASE_002_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0050_CASE_002_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0051_CASE_002_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0052_CASE_002_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0053_CASE_002_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0054_CASE_002_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0055_CASE_002_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0056_CASE_002_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0057_CASE_002_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0058_CASE_002_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0059_CASE_002_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0060_CASE_002_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- banking/
|   |   |   |       |   |   |       `-- user_task_14/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_7.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0061_CASE_003_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0062_CASE_003_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0063_CASE_003_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0064_CASE_003_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0065_CASE_003_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0066_CASE_003_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0067_CASE_003_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0068_CASE_003_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0069_CASE_003_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0070_CASE_003_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0071_CASE_003_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0072_CASE_003_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0073_CASE_003_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0074_CASE_003_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0075_CASE_003_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0076_CASE_003_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0077_CASE_003_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0078_CASE_003_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0079_CASE_003_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0080_CASE_003_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0081_CASE_003_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0082_CASE_003_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0083_CASE_003_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0084_CASE_003_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0085_CASE_003_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0086_CASE_003_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0087_CASE_003_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0088_CASE_003_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0089_CASE_003_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0090_CASE_003_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_1/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0091_CASE_004_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0092_CASE_004_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0093_CASE_004_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0094_CASE_004_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0095_CASE_004_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0096_CASE_004_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0097_CASE_004_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0098_CASE_004_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0099_CASE_004_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0100_CASE_004_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0101_CASE_004_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0102_CASE_004_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0103_CASE_004_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0104_CASE_004_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0105_CASE_004_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0106_CASE_004_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0107_CASE_004_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0108_CASE_004_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0109_CASE_004_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0110_CASE_004_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0111_CASE_004_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0112_CASE_004_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0113_CASE_004_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0114_CASE_004_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0115_CASE_004_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0116_CASE_004_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0117_CASE_004_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0118_CASE_004_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0119_CASE_004_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0120_CASE_004_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_13/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0121_CASE_005_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0122_CASE_005_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0123_CASE_005_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0124_CASE_005_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0125_CASE_005_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0126_CASE_005_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0127_CASE_005_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0128_CASE_005_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0129_CASE_005_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0130_CASE_005_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0131_CASE_005_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0132_CASE_005_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0133_CASE_005_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0134_CASE_005_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0135_CASE_005_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0136_CASE_005_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0137_CASE_005_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0138_CASE_005_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0139_CASE_005_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0140_CASE_005_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0141_CASE_005_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0142_CASE_005_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0143_CASE_005_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0144_CASE_005_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0145_CASE_005_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0146_CASE_005_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0147_CASE_005_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0148_CASE_005_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0149_CASE_005_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0150_CASE_005_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_17/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0151_CASE_006_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0152_CASE_006_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0153_CASE_006_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0154_CASE_006_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0155_CASE_006_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0156_CASE_006_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0157_CASE_006_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0158_CASE_006_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0159_CASE_006_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0160_CASE_006_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0161_CASE_006_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0162_CASE_006_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0163_CASE_006_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0164_CASE_006_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0165_CASE_006_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0166_CASE_006_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0167_CASE_006_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0168_CASE_006_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0169_CASE_006_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0170_CASE_006_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0171_CASE_006_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0172_CASE_006_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0173_CASE_006_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0174_CASE_006_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0175_CASE_006_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0176_CASE_006_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0177_CASE_006_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0178_CASE_006_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0179_CASE_006_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0180_CASE_006_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_2/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_5.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0181_CASE_007_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0182_CASE_007_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0183_CASE_007_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0184_CASE_007_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0185_CASE_007_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0186_CASE_007_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0187_CASE_007_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0188_CASE_007_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0189_CASE_007_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0190_CASE_007_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0191_CASE_007_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0192_CASE_007_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0193_CASE_007_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0194_CASE_007_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0195_CASE_007_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0196_CASE_007_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0197_CASE_007_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0198_CASE_007_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0199_CASE_007_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0200_CASE_007_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0201_CASE_007_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0202_CASE_007_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0203_CASE_007_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0204_CASE_007_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0205_CASE_007_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0206_CASE_007_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0207_CASE_007_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0208_CASE_007_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0209_CASE_007_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0210_CASE_007_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- slack/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0211_CASE_008_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0212_CASE_008_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0213_CASE_008_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0214_CASE_008_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0215_CASE_008_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0216_CASE_008_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0217_CASE_008_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0218_CASE_008_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0219_CASE_008_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0220_CASE_008_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0221_CASE_008_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0222_CASE_008_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0223_CASE_008_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0224_CASE_008_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0225_CASE_008_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0226_CASE_008_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0227_CASE_008_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0228_CASE_008_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0229_CASE_008_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0230_CASE_008_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0231_CASE_008_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0232_CASE_008_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0233_CASE_008_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0234_CASE_008_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0235_CASE_008_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0236_CASE_008_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0237_CASE_008_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0238_CASE_008_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0239_CASE_008_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0240_CASE_008_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- travel/
|   |   |   |       |   |   |       `-- user_task_3/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_1.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0241_CASE_009_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0242_CASE_009_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0243_CASE_009_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0244_CASE_009_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0245_CASE_009_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0246_CASE_009_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0247_CASE_009_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0248_CASE_009_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0249_CASE_009_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0250_CASE_009_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0251_CASE_009_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0252_CASE_009_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0253_CASE_009_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0254_CASE_009_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0255_CASE_009_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0256_CASE_009_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0257_CASE_009_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0258_CASE_009_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0259_CASE_009_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0260_CASE_009_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0261_CASE_009_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0262_CASE_009_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0263_CASE_009_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0264_CASE_009_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0265_CASE_009_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0266_CASE_009_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0267_CASE_009_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0268_CASE_009_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0269_CASE_009_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0270_CASE_009_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_12/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0271_CASE_010_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0272_CASE_010_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0273_CASE_010_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0274_CASE_010_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0275_CASE_010_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0276_CASE_010_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0277_CASE_010_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0278_CASE_010_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0279_CASE_010_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0280_CASE_010_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0281_CASE_010_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0282_CASE_010_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0283_CASE_010_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0284_CASE_010_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0285_CASE_010_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0286_CASE_010_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0287_CASE_010_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0288_CASE_010_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0289_CASE_010_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0290_CASE_010_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0291_CASE_010_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0292_CASE_010_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0293_CASE_010_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0294_CASE_010_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0295_CASE_010_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0296_CASE_010_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0297_CASE_010_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0298_CASE_010_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0299_CASE_010_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0300_CASE_010_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_15/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0301_CASE_011_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0302_CASE_011_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0303_CASE_011_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0304_CASE_011_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0305_CASE_011_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0306_CASE_011_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0307_CASE_011_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0308_CASE_011_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0309_CASE_011_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0310_CASE_011_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0311_CASE_011_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0312_CASE_011_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0313_CASE_011_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0314_CASE_011_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0315_CASE_011_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0316_CASE_011_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0317_CASE_011_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0318_CASE_011_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0319_CASE_011_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0320_CASE_011_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0321_CASE_011_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0322_CASE_011_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0323_CASE_011_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0324_CASE_011_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0325_CASE_011_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0326_CASE_011_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0327_CASE_011_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0328_CASE_011_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0329_CASE_011_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0330_CASE_011_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_21/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0331_CASE_012_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0332_CASE_012_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0333_CASE_012_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0334_CASE_012_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0335_CASE_012_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0336_CASE_012_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0337_CASE_012_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0338_CASE_012_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0339_CASE_012_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0340_CASE_012_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0341_CASE_012_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0342_CASE_012_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0343_CASE_012_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0344_CASE_012_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0345_CASE_012_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0346_CASE_012_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0347_CASE_012_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0348_CASE_012_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0349_CASE_012_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0350_CASE_012_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0351_CASE_012_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0352_CASE_012_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0353_CASE_012_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0354_CASE_012_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0355_CASE_012_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0356_CASE_012_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0357_CASE_012_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0358_CASE_012_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0359_CASE_012_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0360_CASE_012_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_4/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0361_CASE_013_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0362_CASE_013_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0363_CASE_013_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0364_CASE_013_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0365_CASE_013_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0366_CASE_013_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0367_CASE_013_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0368_CASE_013_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0369_CASE_013_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0370_CASE_013_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0371_CASE_013_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0372_CASE_013_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0373_CASE_013_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0374_CASE_013_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0375_CASE_013_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0376_CASE_013_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0377_CASE_013_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0378_CASE_013_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0379_CASE_013_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0380_CASE_013_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0381_CASE_013_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0382_CASE_013_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0383_CASE_013_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0384_CASE_013_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0385_CASE_013_CONFLICT_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0386_CASE_013_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0387_CASE_013_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0388_CASE_013_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0389_CASE_013_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0390_CASE_013_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_6/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0391_CASE_014_CONFLICT_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0392_CASE_014_CONFLICT_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0393_CASE_014_ALIGNED_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0394_CASE_014_CLEAN_OFF_r1_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0395_CASE_014_CLEAN_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0396_CASE_014_ALIGNED_ON_r1_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0397_CASE_014_ALIGNED_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0398_CASE_014_CONFLICT_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0399_CASE_014_CLEAN_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0400_CASE_014_ALIGNED_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0401_CASE_014_CLEAN_OFF_r2_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0402_CASE_014_CONFLICT_ON_r2_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0403_CASE_014_CLEAN_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0404_CASE_014_ALIGNED_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0405_CASE_014_CONFLICT_OFF_r3_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0406_CASE_014_CONFLICT_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0407_CASE_014_CLEAN_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0408_CASE_014_ALIGNED_ON_r3_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0409_CASE_014_ALIGNED_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0410_CASE_014_CLEAN_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0411_CASE_014_ALIGNED_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0412_CASE_014_CONFLICT_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0413_CASE_014_CLEAN_ON_r4_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0414_CASE_014_CONFLICT_OFF_r4_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0415_CASE_014_CLEAN_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0416_CASE_014_CLEAN_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- none/
|   |   |   |       |   |   |               `-- none.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0417_CASE_014_ALIGNED_OFF_r5_a1/
|   |   |   |       |   |   |-- None-None-nodefense/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0418_CASE_014_ALIGNED_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_aligned_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   |-- 0419_CASE_014_CONFLICT_ON_r5_a1/
|   |   |   |       |   |   |-- None-None-attriguard/
|   |   |   |       |   |   |   `-- workspace/
|   |   |   |       |   |   |       `-- user_task_9/
|   |   |   |       |   |   |           `-- e2e_conflict_v1/
|   |   |   |       |   |   |               `-- injection_task_2.json
|   |   |   |       |   |   |-- POST_ENVIRONMENT.json
|   |   |   |       |   |   `-- PRE_ENVIRONMENT.json
|   |   |   |       |   `-- 0420_CASE_014_CONFLICT_OFF_r5_a1/
|   |   |   |       |       |-- None-None-nodefense/
|   |   |   |       |       |   `-- workspace/
|   |   |   |       |       |       `-- user_task_9/
|   |   |   |       |       |           `-- e2e_conflict_v1/
|   |   |   |       |       |               `-- injection_task_2.json
|   |   |   |       |       |-- POST_ENVIRONMENT.json
|   |   |   |       |       `-- PRE_ENVIRONMENT.json
|   |   |   |       `-- RUN_ROWS.jsonl
|   |   |   `-- README.md
|   |   |-- 09_evaluation_replay/
|   |   |   |-- gemma/
|   |   |   |   |-- baseline_terminal.log
|   |   |   |   |-- FINAL_ARTIFACT_SHA256.txt
|   |   |   |   |-- P2B_CI_ACTION_LOCAL_ORACLE_SELFTEST.json
|   |   |   |   |-- P2B_CI_ACTION_STRUCTURE_ROWS.csv
|   |   |   |   |-- P2B_CI_ARGUMENT_SLOT_ROWS.csv
|   |   |   |   |-- P2B_CI_ARGUMENT_VOLATILITY.json
|   |   |   |   |-- P2B_CI_ARGUMENT_VOLATILITY.md
|   |   |   |   |-- P2B_CI_ARM_ANALYSIS.json
|   |   |   |   |-- P2B_CI_ARM_ANALYSIS.md
|   |   |   |   |-- P2B_CI_ARM_FREEZE.json
|   |   |   |   |-- P2B_CI_BASELINE_RAW.jsonl
|   |   |   |   |-- P2B_CI_DOWNSTREAM_ORACLE_SELFTEST.json
|   |   |   |   |-- P2B_CI_RENDER_PREFLIGHT.json
|   |   |   |   `-- vllm_server.log
|   |   |   |-- joint/
|   |   |   |   |-- P2B_XM_CI_JOINT.json
|   |   |   |   `-- P2B_XM_CI_JOINT.md
|   |   |   |-- llama/
|   |   |   |   |-- baseline_terminal.log
|   |   |   |   |-- FINAL_ARTIFACT_SHA256.txt
|   |   |   |   |-- P2B_CI_ACTION_LOCAL_ORACLE_SELFTEST_FAILURE.json
|   |   |   |   |-- P2B_CI_ACTION_LOCAL_ORACLE_SELFTEST_FAILURE_SUPERSEDED_TIMESTAMP_BUG.json
|   |   |   |   |-- P2B_CI_ACTION_LOCAL_ORACLE_SELFTEST.json
|   |   |   |   |-- P2B_CI_ACTION_STRUCTURE_ROWS.csv
|   |   |   |   |-- P2B_CI_ARGUMENT_SLOT_ROWS.csv
|   |   |   |   |-- P2B_CI_ARGUMENT_VOLATILITY.json
|   |   |   |   |-- P2B_CI_ARGUMENT_VOLATILITY.md
|   |   |   |   |-- P2B_CI_ARM_ANALYSIS.json
|   |   |   |   |-- P2B_CI_ARM_ANALYSIS.md
|   |   |   |   |-- P2B_CI_ARM_FREEZE.json
|   |   |   |   |-- P2B_CI_BASELINE_RAW.jsonl
|   |   |   |   |-- P2B_CI_DOWNSTREAM_ORACLE_SELFTEST.json
|   |   |   |   |-- P2B_CI_RENDER_PREFLIGHT.json
|   |   |   |   |-- P2B_CI_RENDER_PREFLIGHT_SUPERSEDED_BEFORE_ORACLE_PATCH.json
|   |   |   |   `-- vllm_server.log
|   |   |   |-- qwen/
|   |   |   |   |-- baseline_terminal.log
|   |   |   |   |-- FINAL_ARTIFACT_SHA256.txt
|   |   |   |   |-- P2B_CI_ACTION_LOCAL_ORACLE_SELFTEST.json
|   |   |   |   |-- P2B_CI_ACTION_STRUCTURE_ROWS.csv
|   |   |   |   |-- P2B_CI_ARGUMENT_SLOT_ROWS.csv
|   |   |   |   |-- P2B_CI_ARGUMENT_VOLATILITY.json
|   |   |   |   |-- P2B_CI_ARGUMENT_VOLATILITY.md
|   |   |   |   |-- P2B_CI_ARM_ANALYSIS.json
|   |   |   |   |-- P2B_CI_ARM_ANALYSIS.md
|   |   |   |   |-- P2B_CI_ARM_FREEZE.json
|   |   |   |   |-- P2B_CI_BASELINE_RAW.jsonl
|   |   |   |   |-- P2B_CI_DOWNSTREAM_ORACLE_SELFTEST.json
|   |   |   |   |-- P2B_CI_RENDER_PREFLIGHT.json
|   |   |   |   `-- vllm_server.log
|   |   |   |-- README.md
|   |   |   `-- support/
|   |   |       |-- P2B_CROSS_MODEL_REPLICATION_v1_3_ARGUMENT_ROLE_ENDPOINT/
|   |   |       |   |-- canonical_json_adapter.py
|   |   |       |   |-- CROSS_MODEL_PROTOCOL.md
|   |   |       |   |-- inputs/
|   |   |       |   |   |-- P2B_PREFLIGHT_REPORT.md
|   |   |       |   |   |-- P2B_PREFLIGHT_SUMMARY.json
|   |   |       |   |   |-- P2B_REPLAY_CONTEXTS.jsonl
|   |   |       |   |   `-- P2B_REPLAY_INVENTORY.jsonl
|   |   |       |   |-- MODEL_REGISTRY.json
|   |   |       |   |-- P2B_ARGUMENT_ROLE_STATIC_AUDIT.json
|   |   |       |   |-- P2B_ARGUMENT_ROLE_TAXONOMY.json
|   |   |       |   |-- p2b_common.py
|   |   |       |   |-- P2B_STATIC_ADAPTER_AUDIT.json
|   |   |       |   |-- P2b_XM_00_adapter_smoke.py
|   |   |       |   |-- P2b_XM_00a_render_preflight.py
|   |   |       |   |-- P2b_XM_00_resolve_revision_lock.py
|   |   |       |   |-- P2b_XM_01_freeze_model.py
|   |   |       |   |-- P2b_XM_02_run_baseline.py
|   |   |       |   |-- P2b_XM_03a_argument_volatility.py
|   |   |       |   |-- P2b_XM_03_check_gate.py
|   |   |       |   |-- P2b_XM_04_joint_compare.py
|   |   |       |   |-- P2B_XMODEL_SCIENTIFIC_AMENDMENT_3.md
|   |   |       |   |-- P2B_XMODEL_TECHNICAL_AMENDMENT_1.md
|   |   |       |   |-- P2B_XMODEL_TECHNICAL_AMENDMENT_2.md
|   |   |       |   |-- README.md
|   |   |       |   |-- serve_gemma.sh
|   |   |       |   |-- serve_llama.sh
|   |   |       |   |-- serve_qwen_canonical.sh
|   |   |       |   `-- SHA256SUMS.txt
|   |   |       |-- P2B_SCIENCE_RUN_v1/
|   |   |       |   |-- P2B_BASELINE_RAW.jsonl
|   |   |       |   |-- P2B_BASELINE_TERMINAL.log
|   |   |       |   |-- P2B_ORACLE_SELFTEST.json
|   |   |       |   `-- P2B_SCIENCE_FREEZE.json
|   |   |       |-- P2B_XM_CI_v1_2_COMPLETE_RESULTS.sha256
|   |   |       |-- P2B_XM_CI_v1_2_ORACLE_PATCH_NO_SERVER_RERUN/
|   |   |       |   |-- action_local.py
|   |   |       |   |-- apply_patch.sh
|   |   |       |   |-- P2b_CI_00_static_audit.py
|   |   |       |   |-- P2b_CI_02_freeze_global.py
|   |   |       |   |-- PATCH_FILE_SHA256.txt
|   |   |       |   `-- V1_2_1R_ACTION_LOCAL_ORACLE_AMENDMENT.md
|   |   |       |-- P2B_XM_CI_v1_2_PREOUTCOME_TECH_GATE_CORRECTED/
|   |   |       |   |-- ACTION_ENVELOPE_SCHEMA.json
|   |   |       |   |-- action_local.py
|   |   |       |   |-- ci_integrity.py
|   |   |       |   |-- common_action_interface.py
|   |   |       |   |-- inputs/
|   |   |       |   |   |-- EXCLUDED_STRESS_CONTEXTS.json
|   |   |       |   |   |-- P2B_PREFLIGHT_REPORT.md
|   |   |       |   |   |-- P2B_PREFLIGHT_SUMMARY.json
|   |   |       |   |   |-- P2B_REPLAY_CONTEXTS.jsonl
|   |   |       |   |   `-- P2B_REPLAY_INVENTORY.jsonl
|   |   |       |   |-- MODEL_REGISTRY_CI.json
|   |   |       |   |-- P2B_ARGUMENT_ROLE_TAXONOMY.json
|   |   |       |   |-- P2b_CI_00_static_audit.py
|   |   |       |   |-- P2b_CI_01_stress_preflight.py
|   |   |       |   |-- P2b_CI_02_freeze_global.py
|   |   |       |   |-- P2b_CI_03_render_preflight.py
|   |   |       |   |-- P2b_CI_04_freeze_arm.py
|   |   |       |   |-- P2b_CI_05_run_baseline.py
|   |   |       |   |-- P2b_CI_06_analyze_arm.py
|   |   |       |   |-- P2b_CI_07_argument_role.py
|   |   |       |   |-- P2b_CI_08_joint_compare.py
|   |   |       |   |-- P2b_CI_RUNBOOK.md
|   |   |       |   |-- P2B_CI_STATIC_AUDIT.json
|   |   |       |   |-- p2b_common.py
|   |   |       |   |-- P2B_XM_CI_GLOBAL_FREEZE.json
|   |   |       |   |-- P2B_XM_CI_GLOBAL_FREEZE_SUPERSEDED_ORIGINAL_v1_2.json
|   |   |       |   |-- P2B_XM_CI_REVISION_LOCK.json
|   |   |       |   |-- PACKAGE_FILE_SHA256.txt
|   |   |       |   |-- PREOUTCOME_BUILD_VALIDATION.json
|   |   |       |   |-- PREOUTCOME_VERIFICATION_REPORT.md
|   |   |       |   |-- PROTOCOL_P2B_XM_CI_v1_2.md
|   |   |       |   |-- README.md
|   |   |       |   |-- requirements_ci.txt
|   |   |       |   |-- serve_model.sh
|   |   |       |   |-- stop_server.sh
|   |   |       |   |-- stress_runtime.py
|   |   |       |   |-- technical_preflight/
|   |   |       |   |   |-- gemma/
|   |   |       |   |   |   |-- .gitkeep
|   |   |       |   |   |   `-- P2B_CI_STRESS_PREFLIGHT.json
|   |   |       |   |   |-- llama/
|   |   |       |   |   |   |-- .gitkeep
|   |   |       |   |   |   `-- P2B_CI_STRESS_PREFLIGHT.json
|   |   |       |   |   `-- qwen_canonical/
|   |   |       |   |       |-- .gitkeep
|   |   |       |   |       `-- P2B_CI_STRESS_PREFLIGHT.json
|   |   |       |   |-- technical_server/
|   |   |       |   |   |-- gemma/
|   |   |       |   |   |   `-- vllm_server.log
|   |   |       |   |   |-- llama/
|   |   |       |   |   |   `-- vllm_server.log
|   |   |       |   |   `-- qwen_canonical/
|   |   |       |   |       `-- vllm_server.log
|   |   |       |   |-- V1_2_1R_ACTION_LOCAL_ORACLE_AMENDMENT.md
|   |   |       |   |-- V1_2_TECHNICAL_GATE_AMENDMENT.md
|   |   |       |   `-- V13_ADJUDICATION_LINEAGE.md
|   |   |       |-- P2B_XMODEL_GEMMA_RUN_v1/
|   |   |       |   |-- baseline_terminal.log
|   |   |       |   |-- P2B_ADAPTER_SMOKE.json
|   |   |       |   |-- P2B_ORACLE_SELFTEST.json
|   |   |       |   |-- P2B_XMODEL_FREEZE.json
|   |   |       |   `-- vllm_server.log
|   |   |       |-- P2B_XMODEL_LLAMA_RUN_v1/
|   |   |       |   |-- baseline_terminal.log
|   |   |       |   |-- P2B_ADAPTER_SMOKE.json
|   |   |       |   |-- P2B_ORACLE_SELFTEST.json
|   |   |       |   |-- P2B_XMODEL_BASELINE_GATE.json
|   |   |       |   |-- P2B_XMODEL_BASELINE_RAW.jsonl
|   |   |       |   |-- P2B_XMODEL_FREEZE.json
|   |   |       |   `-- vllm_server.log
|   |   |       |-- P2B_XMODEL_REVISION_LOCK_v1_3.json
|   |   |       `-- P2B_XMODEL_v1_3_COMPLETE_RESULTS.sha256
|   |   `-- README.md
|   |-- supporting_material/
|   |   |-- legacy_scripts/
|   |   |   `-- make_figure1_ecology.py
|   |   |-- provenance/
|   |   |   |-- ARTIFACT_INCREMENTAL_PROMOTION_2026-08-19_R2B_AWN3_SHA256.tsv
|   |   |   |-- ARTIFACT_SOURCE_EXCLUDE_MANIFEST_v1.tsv
|   |   |   |-- ARTIFACT_SOURCE_INCLUDE_MANIFEST_v1.tsv
|   |   |   |-- ARTIFACT_WORKING_BASE_FILE_SHA256_v1.tsv
|   |   |   |-- ARTIFACT_WORKING_NOTES.md
|   |   |   |-- README_ORIGINAL_ARTIFACT_FREEZE.md
|   |   |   |-- SOURCE_ARTIFACT_COVERAGE.json
|   |   |   |-- SOURCE_ARTIFACT_COVERAGE.tsv
|   |   |   `-- source_artifact_metadata/
|   |   |       `-- SHA256SUMS.txt
|   |   `-- validation_and_hardening/
|   |       |-- A12_falsify.py
|   |       |-- BASE_FINISHING_ZERO_CALL_v1/
|   |       |   |-- A14_AR/
|   |       |   |   |-- A14_AR_AUDIT.json
|   |       |   |   |-- A14_AR_FINAL_SHA256.txt
|   |       |   |   `-- A14_AR_REPORT.md
|   |       |   `-- P3_C0/
|   |       |       |-- FINAL_SHA256.txt
|   |       |       |-- P3_C0_ANALYSIS_FREEZE.json
|   |       |       |-- P3_C0_FOREST.svg
|   |       |       |-- P3_C0_LEAVE_ONE_SUITE_OUT.csv
|   |       |       |-- P3_C0_LEAVE_ONE_TASK_OUT.csv
|   |       |       |-- P3_C0_REFRESH.json
|   |       |       |-- P3_C0_SUMMARY.md
|   |       |       `-- P3_C0_TASK_SPAN_DIAGNOSTICS.csv
|   |       |-- BASE_FINISHING_ZERO_CALL_v1_AUTHOR_RUN.log
|   |       |-- falsify/
|   |       |   |-- falsify.json
|   |       |   |-- observations.jsonl
|   |       |   |-- preregistration_A13.json
|   |       |   |-- run_config_copy.json
|   |       |   `-- run_metadata.json
|   |       |-- N4_N5_BOUNDED_SYNTHESIS_v1/
|   |       |   |-- N4_N5_00_collect_validate.py
|   |       |   |-- N4_N5_01_synthesize.py
|   |       |   |-- n4n5_common.py
|   |       |   |-- PACKAGE_SHA256.txt
|   |       |   `-- README.md
|   |       |-- N4_N5_collect.log
|   |       |-- N4_N5_RUN_v1/
|   |       |   |-- FINAL_ARTIFACT_SHA256.txt
|   |       |   |-- N2_NEC_INPUT.md
|   |       |   |-- N4_N5_EVIDENCE_MATRIX.json
|   |       |   |-- N4_N5_INPUT_MANIFEST.json
|   |       |   `-- N4_N5_SYNTHESIS.md
|   |       |-- N4_N5_synthesis.log
|   |       |-- P3_C0_A14_AR_ZERO_CALL_v1/
|   |       |   |-- A14_AR_00_verify_recovery.py
|   |       |   |-- P3_C0_00_freeze.py
|   |       |   |-- P3_C0_01_refresh.py
|   |       |   |-- P3_C0_02_hash_outputs.py
|   |       |   |-- P3_C0_CONFIG.json
|   |       |   |-- PACKAGE_SHA256.txt
|   |       |   |-- README.md
|   |       |   `-- run_zero_call_finishing.sh
|   |       |-- P3_HARDENING_RUN_v1/
|   |       |   |-- FINAL_ARTIFACT_SHA256.txt
|   |       |   |-- P3_A13_LEAVE_ONE_SUITE_OUT.csv
|   |       |   |-- P3_A13_LEAVE_ONE_TASK_OUT.csv
|   |       |   |-- P3_A13_TASK_SPAN_DIAGNOSTICS.csv
|   |       |   |-- P3_A15A_LEAVE_ONE_SUITE_OUT.csv
|   |       |   |-- P3_A15A_SUITE_SUMMARY.csv
|   |       |   |-- P3_ANALYSIS_FREEZE.json
|   |       |   |-- P3_ANALYSIS_FREEZE.md
|   |       |   |-- P3_HARDENING.json
|   |       |   |-- P3_HARDENING_SUMMARY.md
|   |       |   |-- P3_P2B_CROSS_MODEL_DECISIONS.csv
|   |       |   |-- P3_P2B_LEAVE_ONE_DECISION_OUT.csv
|   |       |   |-- P3_P2B_LEAVE_ONE_FUNCTION_OUT.csv
|   |       |   |-- P3_P2B_LEAVE_ONE_SUITE_OUT.csv
|   |       |   |-- P3_P2B_MASKED_ROWS.csv
|   |       |   |-- P3_P2B_MODEL_DECISION_CELLS.csv
|   |       |   |-- P3_P2B_ORIGINAL_QWEN_WEAK_RECURRENCE.csv
|   |       |   |-- P3_P2B_SUBGROUP_SUMMARY.csv
|   |       |   `-- P3_P2B_WITHIN_STRATUM.csv
|   |       |-- P3_ZERO_CALL_HARDENING_v1/
|   |       |   |-- P3_00_freeze_analysis.py
|   |       |   |-- P3_01_run_hardening.py
|   |       |   |-- P3_02_hash_outputs.py
|   |       |   |-- P3_CONFIG.json
|   |       |   `-- README.md
|   |       |-- P6_CLEAN_AUTHOR_RUN.log
|   |       |-- P6_CLEAN_PREFLIGHT.log
|   |       |-- P6_CLEAN_RUN_v1/
|   |       |   |-- FINAL_ARTIFACT_SHA256.txt
|   |       |   |-- P6_ARGUMENT_ROLE_HSLOT.csv
|   |       |   |-- P6_ATTACK_ANCHORS.csv
|   |       |   |-- P6_AUTHORIZATION_STRATIFIED_BENIGN.csv
|   |       |   |-- P6_CLAIM_LEDGER.csv
|   |       |   |-- P6_CONTROLLED_BENIGN_CONSISTENCY.csv
|   |       |   |-- P6_EQUIVALENCE_LADDER.csv
|   |       |   |-- P6_EVALUATION_FRAMEWORK.svg
|   |       |   |-- P6_INPUT_FREEZE.json
|   |       |   |-- P6_INPUT_FREEZE.md
|   |       |   |-- P6_INPUT_MANIFEST.tsv
|   |       |   |-- P6_MASTER_EVALUATION_VECTOR.csv
|   |       |   |-- P6_REPLAY_EQUIVALENCE_MATRIX.csv
|   |       |   |-- P6_SELECTED_POPULATION_BEHAVIOR.csv
|   |       |   |-- P6_SUMMARY.md
|   |       |   `-- P6_SYNTHESIS.json
|   |       |-- P6_CLEAN_SYNTHESIS.log
|   |       |-- P6_CLEAN_VERIFY.log
|   |       `-- P6_CLEAN_ZERO_CALL_v1/
|   |           |-- P6_00_preflight_and_freeze.py
|   |           |-- P6_01_synthesize.py
|   |           |-- P6_02_verify_and_hash.py
|   |           |-- p6_common.py
|   |           |-- P6_CONFIG.json
|   |           |-- PACKAGE_SHA256.txt
|   |           |-- README.md
|   |           `-- RUN_P6_CLEAN.sh
|   |-- third_party/
|   |   |-- integrations/
|   |   |   |-- AgentWatcher/
|   |   |   |   |-- agents/
|   |   |   |   |   |-- agentdojo/
|   |   |   |   |   |   |-- CITATION.bib
|   |   |   |   |   |   |-- CLAUDE.md
|   |   |   |   |   |   |-- CONTRIBUTING.md
|   |   |   |   |   |   |-- .devcontainer/
|   |   |   |   |   |   |   |-- devcontainer.json
|   |   |   |   |   |   |   |-- Dockerfile
|   |   |   |   |   |   |   `-- init-firewall.sh
|   |   |   |   |   |   |-- docs/
|   |   |   |   |   |   |   |-- api/
|   |   |   |   |   |   |   |   |-- agent_pipeline/
|   |   |   |   |   |   |   |   |   |-- basic_elements.md
|   |   |   |   |   |   |   |   |   |-- defenses.md
|   |   |   |   |   |   |   |   |   `-- llms.md
|   |   |   |   |   |   |   |   |-- attacks/
|   |   |   |   |   |   |   |   |   |-- base_attacks.md
|   |   |   |   |   |   |   |   |   |-- baseline_attacks.md
|   |   |   |   |   |   |   |   |   |-- dos_attacks.md
|   |   |   |   |   |   |   |   |   `-- registering_and_loading_attacks.md
|   |   |   |   |   |   |   |   |-- base_tasks.md
|   |   |   |   |   |   |   |   |-- benchmark.md
|   |   |   |   |   |   |   |   |-- functions_runtime.md
|   |   |   |   |   |   |   |   |-- task_suite.md
|   |   |   |   |   |   |   |   `-- types.md
|   |   |   |   |   |   |   |-- changelog.md
|   |   |   |   |   |   |   |-- CNAME
|   |   |   |   |   |   |   |-- concepts/
|   |   |   |   |   |   |   |   |-- agent_pipeline.md
|   |   |   |   |   |   |   |   |-- attacks.md
|   |   |   |   |   |   |   |   |-- functions_runtime.md
|   |   |   |   |   |   |   |   `-- task_suite_and_tasks.md
|   |   |   |   |   |   |   |-- development.md
|   |   |   |   |   |   |   |-- index.md
|   |   |   |   |   |   |   |-- results.md
|   |   |   |   |   |   |   `-- results-table.html
|   |   |   |   |   |   |-- examples/
|   |   |   |   |   |   |   |-- attack.py
|   |   |   |   |   |   |   |-- counter_benchmark/
|   |   |   |   |   |   |   |   |-- benchmark.py
|   |   |   |   |   |   |   |   |-- data/
|   |   |   |   |   |   |   |   |   `-- suites/
|   |   |   |   |   |   |   |   |       `-- counter/
|   |   |   |   |   |   |   |   |           |-- environment.yaml
|   |   |   |   |   |   |   |   |           `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   `-- suites/
|   |   |   |   |   |   |   |       |-- counter/
|   |   |   |   |   |   |   |       |   |-- __init__.py
|   |   |   |   |   |   |   |       |   |-- injection_tasks.py
|   |   |   |   |   |   |   |       |   |-- task_suite.py
|   |   |   |   |   |   |   |       |   `-- user_tasks.py
|   |   |   |   |   |   |   |       |-- __init__.py
|   |   |   |   |   |   |   |       `-- tools.py
|   |   |   |   |   |   |   |-- functions_runtime.py
|   |   |   |   |   |   |   |-- pipeline.py
|   |   |   |   |   |   |   `-- README.md
|   |   |   |   |   |   |-- .github/
|   |   |   |   |   |   |   `-- workflows/
|   |   |   |   |   |   |       |-- CODEOWNERS
|   |   |   |   |   |   |       |-- lint-docs.yaml
|   |   |   |   |   |   |       `-- publish.yaml
|   |   |   |   |   |   |-- .gitignore
|   |   |   |   |   |   |-- LICENSE
|   |   |   |   |   |   |-- mkdocs.yml
|   |   |   |   |   |   |-- notebooks/
|   |   |   |   |   |   |   |-- agent_pipeline_example.ipynb
|   |   |   |   |   |   |   `-- analysis.ipynb
|   |   |   |   |   |   |-- .pre-commit-config.yaml
|   |   |   |   |   |   |-- pyproject.toml
|   |   |   |   |   |   |-- .python-version
|   |   |   |   |   |   |-- README.md
|   |   |   |   |   |   |-- src/
|   |   |   |   |   |   |   `-- agentdojo/
|   |   |   |   |   |   |       |-- agent_pipeline/
|   |   |   |   |   |   |       |   |-- agent_pipeline.py
|   |   |   |   |   |   |       |   |-- base_pipeline_element.py
|   |   |   |   |   |   |       |   |-- basic_elements.py
|   |   |   |   |   |   |       |   |-- errors.py
|   |   |   |   |   |   |       |   |-- ground_truth_pipeline.py
|   |   |   |   |   |   |       |   |-- inference_utils.py
|   |   |   |   |   |   |       |   |-- __init__.py
|   |   |   |   |   |   |       |   |-- llms/
|   |   |   |   |   |   |       |   |   |-- anthropic_llm.py
|   |   |   |   |   |   |       |   |   |-- cohere_llm.py
|   |   |   |   |   |   |       |   |   |-- google_llm.py
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |-- local_llm.py
|   |   |   |   |   |   |       |   |   |-- openai_llm.py
|   |   |   |   |   |   |       |   |   |-- prompting_llm.py
|   |   |   |   |   |   |       |   |   `-- transformers_llm.py
|   |   |   |   |   |   |       |   |-- piarena_defense_adapter.py
|   |   |   |   |   |   |       |   |-- pi_detector.py
|   |   |   |   |   |   |       |   |-- planner.py
|   |   |   |   |   |   |       |   `-- tool_execution.py
|   |   |   |   |   |   |       |-- ast_utils.py
|   |   |   |   |   |   |       |-- attacks/
|   |   |   |   |   |   |       |   |-- attack_registry.py
|   |   |   |   |   |   |       |   |-- base_attacks.py
|   |   |   |   |   |   |       |   |-- baseline_attacks.py
|   |   |   |   |   |   |       |   |-- dos_attacks.py
|   |   |   |   |   |   |       |   |-- important_instructions_attacks.py
|   |   |   |   |   |   |       |   `-- __init__.py
|   |   |   |   |   |   |       |-- base_tasks.py
|   |   |   |   |   |   |       |-- benchmark.py
|   |   |   |   |   |   |       |-- data/
|   |   |   |   |   |   |       |   |-- suites/
|   |   |   |   |   |   |       |   |   |-- banking/
|   |   |   |   |   |   |       |   |   |   |-- environment.yaml
|   |   |   |   |   |   |       |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |       |   |   |-- slack/
|   |   |   |   |   |   |       |   |   |   |-- environment.yaml
|   |   |   |   |   |   |       |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |       |   |   |-- travel/
|   |   |   |   |   |   |       |   |   |   |-- environment.yaml
|   |   |   |   |   |   |       |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |       |   |   `-- workspace/
|   |   |   |   |   |   |       |   |       |-- environment.yaml
|   |   |   |   |   |   |       |   |       |-- gpt_prompts.txt
|   |   |   |   |   |   |       |   |       |-- include/
|   |   |   |   |   |   |       |   |       |   |-- calendar.yaml
|   |   |   |   |   |   |       |   |       |   |-- cloud_drive.yaml
|   |   |   |   |   |   |       |   |       |   `-- inbox.yaml
|   |   |   |   |   |   |       |   |       `-- injection_vectors.yaml
|   |   |   |   |   |   |       |   `-- system_messages.yaml
|   |   |   |   |   |   |       |-- default_suites/
|   |   |   |   |   |   |       |   |-- __init__.py
|   |   |   |   |   |   |       |   |-- v1/
|   |   |   |   |   |   |       |   |   |-- banking/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |       |   |   |   |-- task_suite.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |-- slack/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |       |   |   |   |-- task_suite.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   |-- tools/
|   |   |   |   |   |   |       |   |   |   |-- banking_client.py
|   |   |   |   |   |   |       |   |   |   |-- calendar_client.py
|   |   |   |   |   |   |       |   |   |   |-- cloud_drive_client.py
|   |   |   |   |   |   |       |   |   |   |-- email_client.py
|   |   |   |   |   |   |       |   |   |   |-- file_reader.py
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   |-- slack.py
|   |   |   |   |   |   |       |   |   |   |-- travel_booking_client.py
|   |   |   |   |   |   |       |   |   |   |-- types.py
|   |   |   |   |   |   |       |   |   |   |-- user_account.py
|   |   |   |   |   |   |       |   |   |   `-- web.py
|   |   |   |   |   |   |       |   |   |-- travel/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |       |   |   |   |-- task_suite.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   `-- workspace/
|   |   |   |   |   |   |       |   |       |-- __init__.py
|   |   |   |   |   |   |       |   |       |-- injection_tasks.py
|   |   |   |   |   |   |       |   |       |-- task_suite.py
|   |   |   |   |   |   |       |   |       `-- user_tasks.py
|   |   |   |   |   |   |       |   |-- v1_1/
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   `-- travel/
|   |   |   |   |   |   |       |   |       `-- user_tasks.py
|   |   |   |   |   |   |       |   |-- v1_1_1/
|   |   |   |   |   |   |       |   |   |-- banking/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |-- slack/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   |-- travel/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   `-- workspace/
|   |   |   |   |   |   |       |   |       `-- user_tasks.py
|   |   |   |   |   |   |       |   |-- v1_1_2/
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |-- travel/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   `-- injection_tasks.py
|   |   |   |   |   |   |       |   |   `-- workspace/
|   |   |   |   |   |   |       |   |       |-- __init__.py
|   |   |   |   |   |   |       |   |       |-- injection_tasks.py
|   |   |   |   |   |   |       |   |       `-- user_tasks.py
|   |   |   |   |   |   |       |   |-- v1_2/
|   |   |   |   |   |   |       |   |   |-- banking/
|   |   |   |   |   |   |       |   |   |   `-- injection_tasks.py
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |-- slack/
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   |-- travel/
|   |   |   |   |   |   |       |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   `-- workspace/
|   |   |   |   |   |   |       |   |       |-- injection_tasks.py
|   |   |   |   |   |   |       |   |       `-- user_tasks.py
|   |   |   |   |   |   |       |   |-- v1_2_1/
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   `-- workspace/
|   |   |   |   |   |   |       |   |       `-- injection_tasks.py
|   |   |   |   |   |   |       |   `-- v1_2_2/
|   |   |   |   |   |   |       |       |-- banking/
|   |   |   |   |   |   |       |       |   |-- __init__.py
|   |   |   |   |   |   |       |       |   `-- user_tasks.py
|   |   |   |   |   |   |       |       |-- __init__.py
|   |   |   |   |   |   |       |       `-- workspace/
|   |   |   |   |   |   |       |           |-- __init__.py
|   |   |   |   |   |   |       |           `-- user_tasks.py
|   |   |   |   |   |   |       |-- functions_runtime.py
|   |   |   |   |   |   |       |-- __init__.py
|   |   |   |   |   |   |       |-- models.py
|   |   |   |   |   |   |       |-- scripts/
|   |   |   |   |   |   |       |   |-- benchmark.py
|   |   |   |   |   |   |       |   |-- check_suites.py
|   |   |   |   |   |   |       |   `-- __init__.py
|   |   |   |   |   |   |       |-- strenum.py
|   |   |   |   |   |   |       |-- task_suite/
|   |   |   |   |   |   |       |   |-- __init__.py
|   |   |   |   |   |   |       |   |-- load_suites.py
|   |   |   |   |   |   |       |   |-- task_combinators.py
|   |   |   |   |   |   |       |   `-- task_suite.py
|   |   |   |   |   |   |       |-- types.py
|   |   |   |   |   |   |       `-- yaml_loader.py
|   |   |   |   |   |   |-- tests/
|   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |-- test_agent_pipeline/
|   |   |   |   |   |   |   |   |-- test_anthropic_llm.py
|   |   |   |   |   |   |   |   |-- test_cohere_llm.py
|   |   |   |   |   |   |   |   |-- test_google_llm.py
|   |   |   |   |   |   |   |   |-- test_pi_detector.py
|   |   |   |   |   |   |   |   `-- test_prompting_llm.py
|   |   |   |   |   |   |   |-- test_ast_utils.py
|   |   |   |   |   |   |   |-- test_benchmark.py
|   |   |   |   |   |   |   |-- test_functions_runtime/
|   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   `-- test_functions_runtime.py
|   |   |   |   |   |   |   `-- test_workspace_user_tasks.py
|   |   |   |   |   |   |-- util_scripts/
|   |   |   |   |   |   |   |-- create_results_table.py
|   |   |   |   |   |   |   |-- run_vllm_parallel.sh
|   |   |   |   |   |   |   `-- run_vllm.sh
|   |   |   |   |   |   `-- uv.lock
|   |   |   |   |   |-- agentdyn/
|   |   |   |   |   |   |-- agentdojo_README.md
|   |   |   |   |   |   |-- CITATION.bib
|   |   |   |   |   |   |-- CLAUDE.md
|   |   |   |   |   |   |-- CONTRIBUTING.md
|   |   |   |   |   |   |-- docs/
|   |   |   |   |   |   |   |-- api/
|   |   |   |   |   |   |   |   |-- agent_pipeline/
|   |   |   |   |   |   |   |   |   |-- basic_elements.md
|   |   |   |   |   |   |   |   |   |-- defenses.md
|   |   |   |   |   |   |   |   |   `-- llms.md
|   |   |   |   |   |   |   |   |-- attacks/
|   |   |   |   |   |   |   |   |   |-- base_attacks.md
|   |   |   |   |   |   |   |   |   |-- baseline_attacks.md
|   |   |   |   |   |   |   |   |   |-- dos_attacks.md
|   |   |   |   |   |   |   |   |   `-- registering_and_loading_attacks.md
|   |   |   |   |   |   |   |   |-- base_tasks.md
|   |   |   |   |   |   |   |   |-- benchmark.md
|   |   |   |   |   |   |   |   |-- functions_runtime.md
|   |   |   |   |   |   |   |   |-- task_suite.md
|   |   |   |   |   |   |   |   `-- types.md
|   |   |   |   |   |   |   |-- changelog.md
|   |   |   |   |   |   |   |-- CNAME
|   |   |   |   |   |   |   |-- concepts/
|   |   |   |   |   |   |   |   |-- agent_pipeline.md
|   |   |   |   |   |   |   |   |-- attacks.md
|   |   |   |   |   |   |   |   |-- functions_runtime.md
|   |   |   |   |   |   |   |   `-- task_suite_and_tasks.md
|   |   |   |   |   |   |   |-- development.md
|   |   |   |   |   |   |   |-- index.md
|   |   |   |   |   |   |   |-- results.md
|   |   |   |   |   |   |   `-- results-table.html
|   |   |   |   |   |   |-- examples/
|   |   |   |   |   |   |   |-- attack.py
|   |   |   |   |   |   |   |-- counter_benchmark/
|   |   |   |   |   |   |   |   |-- benchmark.py
|   |   |   |   |   |   |   |   |-- data/
|   |   |   |   |   |   |   |   |   `-- suites/
|   |   |   |   |   |   |   |   |       `-- counter/
|   |   |   |   |   |   |   |   |           |-- environment.yaml
|   |   |   |   |   |   |   |   |           `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   `-- suites/
|   |   |   |   |   |   |   |       |-- counter/
|   |   |   |   |   |   |   |       |   |-- __init__.py
|   |   |   |   |   |   |   |       |   |-- injection_tasks.py
|   |   |   |   |   |   |   |       |   |-- task_suite.py
|   |   |   |   |   |   |   |       |   `-- user_tasks.py
|   |   |   |   |   |   |   |       |-- __init__.py
|   |   |   |   |   |   |   |       `-- tools.py
|   |   |   |   |   |   |   |-- functions_runtime.py
|   |   |   |   |   |   |   |-- pipeline.py
|   |   |   |   |   |   |   `-- README.md
|   |   |   |   |   |   |-- LICENSE
|   |   |   |   |   |   |-- mkdocs.yml
|   |   |   |   |   |   |-- notebooks/
|   |   |   |   |   |   |   |-- agent_pipeline_example.ipynb
|   |   |   |   |   |   |   `-- analysis.ipynb
|   |   |   |   |   |   |-- pyproject.toml
|   |   |   |   |   |   |-- README.md
|   |   |   |   |   |   |-- src/
|   |   |   |   |   |   |   |-- agentdojo/
|   |   |   |   |   |   |   |   |-- agent_pipeline/
|   |   |   |   |   |   |   |   |   |-- agent_pipeline.py
|   |   |   |   |   |   |   |   |   |-- base_pipeline_element.py
|   |   |   |   |   |   |   |   |   |-- basic_elements.py
|   |   |   |   |   |   |   |   |   |-- errors.py
|   |   |   |   |   |   |   |   |   |-- ground_truth_pipeline.py
|   |   |   |   |   |   |   |   |   |-- inference_utils.py
|   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |-- llms/
|   |   |   |   |   |   |   |   |   |   |-- anthropic_llm.py
|   |   |   |   |   |   |   |   |   |   |-- cohere_llm.py
|   |   |   |   |   |   |   |   |   |   |-- google_llm.py
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |-- local_llm.py
|   |   |   |   |   |   |   |   |   |   |-- openai_llm.py
|   |   |   |   |   |   |   |   |   |   `-- prompting_llm.py
|   |   |   |   |   |   |   |   |   |-- piarena_defense_adapter.py
|   |   |   |   |   |   |   |   |   |-- pi_detector.py
|   |   |   |   |   |   |   |   |   |-- planner.py
|   |   |   |   |   |   |   |   |   `-- tool_execution.py
|   |   |   |   |   |   |   |   |-- ast_utils.py
|   |   |   |   |   |   |   |   |-- attacks/
|   |   |   |   |   |   |   |   |   |-- attack_registry.py
|   |   |   |   |   |   |   |   |   |-- base_attacks.py
|   |   |   |   |   |   |   |   |   |-- baseline_attacks.py
|   |   |   |   |   |   |   |   |   |-- dos_attacks.py
|   |   |   |   |   |   |   |   |   |-- important_instructions_attacks.py
|   |   |   |   |   |   |   |   |   `-- __init__.py
|   |   |   |   |   |   |   |   |-- base_tasks.py
|   |   |   |   |   |   |   |   |-- benchmark.py
|   |   |   |   |   |   |   |   |-- data/
|   |   |   |   |   |   |   |   |   |-- suites/
|   |   |   |   |   |   |   |   |   |   |-- banking/
|   |   |   |   |   |   |   |   |   |   |   |-- environment.yaml
|   |   |   |   |   |   |   |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   |   |-- dailylife/
|   |   |   |   |   |   |   |   |   |   |   |-- environment.yaml
|   |   |   |   |   |   |   |   |   |   |   |-- include/
|   |   |   |   |   |   |   |   |   |   |   |   |-- bank_database.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- calendar.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- email_database.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- filesystem.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- github_platform.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- shopping_platform.yaml
|   |   |   |   |   |   |   |   |   |   |   |   `-- web_database.yaml
|   |   |   |   |   |   |   |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   |   |-- github/
|   |   |   |   |   |   |   |   |   |   |   |-- environment.yaml
|   |   |   |   |   |   |   |   |   |   |   |-- include/
|   |   |   |   |   |   |   |   |   |   |   |   |-- bank_database.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- calendar.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- email_database.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- filesystem.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- github_platform.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- shopping_platform.yaml
|   |   |   |   |   |   |   |   |   |   |   |   `-- web_database.yaml
|   |   |   |   |   |   |   |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   |   |-- shopping/
|   |   |   |   |   |   |   |   |   |   |   |-- environment.yaml
|   |   |   |   |   |   |   |   |   |   |   |-- environment——.yaml
|   |   |   |   |   |   |   |   |   |   |   |-- include/
|   |   |   |   |   |   |   |   |   |   |   |   |-- bank_database.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- calendar.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- email_database.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- filesystem.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- github_platform.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- shopping_platform.yaml
|   |   |   |   |   |   |   |   |   |   |   |   `-- web_database.yaml
|   |   |   |   |   |   |   |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   |   |-- slack/
|   |   |   |   |   |   |   |   |   |   |   |-- environment.yaml
|   |   |   |   |   |   |   |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   |   |-- travel/
|   |   |   |   |   |   |   |   |   |   |   |-- environment.yaml
|   |   |   |   |   |   |   |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   |   `-- workspace/
|   |   |   |   |   |   |   |   |   |       |-- environment.yaml
|   |   |   |   |   |   |   |   |   |       |-- gpt_prompts.txt
|   |   |   |   |   |   |   |   |   |       |-- include/
|   |   |   |   |   |   |   |   |   |       |   |-- calendar.yaml
|   |   |   |   |   |   |   |   |   |       |   |-- cloud_drive.yaml
|   |   |   |   |   |   |   |   |   |       |   `-- inbox.yaml
|   |   |   |   |   |   |   |   |   |       `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   `-- system_messages.yaml
|   |   |   |   |   |   |   |   |-- default_suites/
|   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |-- v1/
|   |   |   |   |   |   |   |   |   |   |-- banking/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   |-- task_suite.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- dailylife/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   |-- task_suite.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- github/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   |-- task_suite.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |-- shopping/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   |-- task_suite.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- slack/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   |-- task_suite.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- tools/
|   |   |   |   |   |   |   |   |   |   |   |-- banking_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- calendar_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- cloud_drive_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- dynamic_banking_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- dynamic_calendar_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- dynamic_email_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- dynamic_web_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- email_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- file_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- file_reader.py
|   |   |   |   |   |   |   |   |   |   |   |-- github_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- shopping_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- slack.py
|   |   |   |   |   |   |   |   |   |   |   |-- tool_registry.py
|   |   |   |   |   |   |   |   |   |   |   |-- travel_booking_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- types.py
|   |   |   |   |   |   |   |   |   |   |   |-- user_account.py
|   |   |   |   |   |   |   |   |   |   |   |-- utils.py
|   |   |   |   |   |   |   |   |   |   |   `-- web.py
|   |   |   |   |   |   |   |   |   |   |-- travel/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   |-- task_suite.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   `-- workspace/
|   |   |   |   |   |   |   |   |   |       |-- __init__.py
|   |   |   |   |   |   |   |   |   |       |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |       |-- task_suite.py
|   |   |   |   |   |   |   |   |   |       `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |-- v1_1/
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   `-- travel/
|   |   |   |   |   |   |   |   |   |       `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |-- v1_1_1/
|   |   |   |   |   |   |   |   |   |   |-- banking/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |-- slack/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- travel/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   `-- workspace/
|   |   |   |   |   |   |   |   |   |       `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |-- v1_1_2/
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |-- travel/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   `-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   `-- workspace/
|   |   |   |   |   |   |   |   |   |       |-- __init__.py
|   |   |   |   |   |   |   |   |   |       |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |       `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |-- v1_2/
|   |   |   |   |   |   |   |   |   |   |-- banking/
|   |   |   |   |   |   |   |   |   |   |   `-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |-- slack/
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- travel/
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   `-- workspace/
|   |   |   |   |   |   |   |   |   |       |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |       `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |-- v1_2_1/
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   `-- workspace/
|   |   |   |   |   |   |   |   |   |       `-- injection_tasks.py
|   |   |   |   |   |   |   |   |   `-- v1_2_2/
|   |   |   |   |   |   |   |   |       |-- banking/
|   |   |   |   |   |   |   |   |       |   |-- __init__.py
|   |   |   |   |   |   |   |   |       |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |       |-- __init__.py
|   |   |   |   |   |   |   |   |       `-- workspace/
|   |   |   |   |   |   |   |   |           |-- __init__.py
|   |   |   |   |   |   |   |   |           `-- user_tasks.py
|   |   |   |   |   |   |   |   |-- functions_runtime.py
|   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |-- models.py
|   |   |   |   |   |   |   |   |-- scripts/
|   |   |   |   |   |   |   |   |   |-- benchmark.py
|   |   |   |   |   |   |   |   |   |-- check_suites.py
|   |   |   |   |   |   |   |   |   `-- __init__.py
|   |   |   |   |   |   |   |   |-- strenum.py
|   |   |   |   |   |   |   |   |-- task_suite/
|   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |-- load_suites.py
|   |   |   |   |   |   |   |   |   |-- task_combinators.py
|   |   |   |   |   |   |   |   |   `-- task_suite.py
|   |   |   |   |   |   |   |   |-- types.py
|   |   |   |   |   |   |   |   `-- yaml_loader.py
|   |   |   |   |   |   |   `-- runs/
|   |   |   |   |   |   |       `-- gpt-4o-2024-08-06-piarena-agentwatcher/
|   |   |   |   |   |   |           |-- dailylife/
|   |   |   |   |   |   |           |   |-- injection_task_0/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_1/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_2/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_3/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_4/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_5/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_6/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_7/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_8/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_9/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_0/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_1/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_10/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_11/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_12/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_13/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_14/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_15/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_16/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_17/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_18/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_19/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_2/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_3/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_4/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_5/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_6/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_7/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_8/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   `-- user_task_9/
|   |   |   |   |   |   |           |       |-- important_instructions/
|   |   |   |   |   |   |           |       |   |-- injection_task_2.json
|   |   |   |   |   |   |           |       |   |-- injection_task_3.json
|   |   |   |   |   |   |           |       |   |-- injection_task_4.json
|   |   |   |   |   |   |           |       |   |-- injection_task_5.json
|   |   |   |   |   |   |           |       |   |-- injection_task_6.json
|   |   |   |   |   |   |           |       |   |-- injection_task_7.json
|   |   |   |   |   |   |           |       |   |-- injection_task_8.json
|   |   |   |   |   |   |           |       |   `-- injection_task_9.json
|   |   |   |   |   |   |           |       `-- none/
|   |   |   |   |   |   |           |           `-- none.json
|   |   |   |   |   |   |           |-- github/
|   |   |   |   |   |   |           |   |-- injection_task_0/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_1/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_2/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_3/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_4/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_5/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_6/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_7/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_8/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_0/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_1/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_10/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_11/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_12/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_13/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_14/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_15/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_16/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_17/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_18/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_19/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_2/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_3/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_4/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_5/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_6/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_7.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_7/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_8/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   `-- user_task_9/
|   |   |   |   |   |   |           |       |-- important_instructions/
|   |   |   |   |   |   |           |       |   |-- injection_task_0.json
|   |   |   |   |   |   |           |       |   |-- injection_task_1.json
|   |   |   |   |   |   |           |       |   |-- injection_task_2.json
|   |   |   |   |   |   |           |       |   |-- injection_task_3.json
|   |   |   |   |   |   |           |       |   |-- injection_task_6.json
|   |   |   |   |   |   |           |       |   |-- injection_task_7.json
|   |   |   |   |   |   |           |       |   `-- injection_task_8.json
|   |   |   |   |   |   |           |       `-- none/
|   |   |   |   |   |   |           |           `-- none.json
|   |   |   |   |   |   |           `-- shopping/
|   |   |   |   |   |   |               |-- injection_task_0/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_1/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_2/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_3/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_4/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_5/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_6/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_7/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_8/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_0/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_1/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_10/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_11/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_12/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_13/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_14/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_15/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_16/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_17/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_18/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_19/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_2/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_3/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_4/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_5/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_6/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_7/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_8/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               `-- user_task_9/
|   |   |   |   |   |   |                   |-- important_instructions/
|   |   |   |   |   |   |                   |   |-- injection_task_0.json
|   |   |   |   |   |   |                   |   |-- injection_task_1.json
|   |   |   |   |   |   |                   |   |-- injection_task_2.json
|   |   |   |   |   |   |                   |   |-- injection_task_3.json
|   |   |   |   |   |   |                   |   |-- injection_task_4.json
|   |   |   |   |   |   |                   |   |-- injection_task_6.json
|   |   |   |   |   |   |                   |   `-- injection_task_8.json
|   |   |   |   |   |   |                   `-- none/
|   |   |   |   |   |   |                       `-- none.json
|   |   |   |   |   |   |-- tests/
|   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |-- test_agent_pipeline/
|   |   |   |   |   |   |   |   |-- test_anthropic_llm.py
|   |   |   |   |   |   |   |   |-- test_cohere_llm.py
|   |   |   |   |   |   |   |   |-- test_google_llm.py
|   |   |   |   |   |   |   |   |-- test_pi_detector.py
|   |   |   |   |   |   |   |   `-- test_prompting_llm.py
|   |   |   |   |   |   |   |-- test_ast_utils.py
|   |   |   |   |   |   |   |-- test_benchmark.py
|   |   |   |   |   |   |   |-- test_functions_runtime/
|   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   `-- test_functions_runtime.py
|   |   |   |   |   |   |   `-- test_workspace_user_tasks.py
|   |   |   |   |   |   |-- util_scripts/
|   |   |   |   |   |   |   |-- create_results_table.py
|   |   |   |   |   |   |   |-- run_vllm_parallel.sh
|   |   |   |   |   |   |   `-- run_vllm.sh
|   |   |   |   |   |   `-- uv.lock
|   |   |   |   |   `-- InjecAgent/
|   |   |   |   |       |-- asset/
|   |   |   |   |       |   |-- overview.pdf
|   |   |   |   |       |   `-- overview.png
|   |   |   |   |       |-- data/
|   |   |   |   |       |   |-- attacker_cases_dh.jsonl
|   |   |   |   |       |   |-- attacker_cases_ds.jsonl
|   |   |   |   |       |   |-- attacker_simulated_responses.json
|   |   |   |   |       |   |-- test_cases_dh_base.json
|   |   |   |   |       |   |-- test_cases_dh_enhanced.json
|   |   |   |   |       |   |-- test_cases_ds_base.json
|   |   |   |   |       |   |-- test_cases_ds_enhanced.json
|   |   |   |   |       |   |-- tools.json
|   |   |   |   |       |   `-- user_cases.jsonl
|   |   |   |   |       |-- .gitignore
|   |   |   |   |       |-- LICENCE
|   |   |   |   |       |-- README.md
|   |   |   |   |       |-- requirements.txt
|   |   |   |   |       `-- src/
|   |   |   |   |           |-- evaluate_finetuned_agent.py
|   |   |   |   |           |-- evaluate_prompted_agent.py
|   |   |   |   |           |-- models.py
|   |   |   |   |           |-- output_parsing.py
|   |   |   |   |           |-- params.py
|   |   |   |   |           |-- prompts/
|   |   |   |   |           |   |-- agent_prompts.py
|   |   |   |   |           |   |-- generation_prompts.py
|   |   |   |   |           |   `-- prompt_template.py
|   |   |   |   |           `-- utils.py
|   |   |   |   |-- assets/
|   |   |   |   |   |-- fig_illustration.jpg
|   |   |   |   |   |-- figure1_agentdyn_benign_utility_asr.png
|   |   |   |   |   `-- .gitkeep
|   |   |   |   |-- datasets/
|   |   |   |   |   `-- wasp.json
|   |   |   |   |-- .gitignore
|   |   |   |   |-- main_agentdojo.py
|   |   |   |   |-- main_injecagent.py
|   |   |   |   |-- main.py
|   |   |   |   |-- README.md
|   |   |   |   |-- requirements.txt
|   |   |   |   |-- scripts/
|   |   |   |   |   |-- main_agentdojo.sh
|   |   |   |   |   |-- main_agentdyn.sh
|   |   |   |   |   |-- main_injecagent.sh
|   |   |   |   |   |-- main.sh
|   |   |   |   |   |-- run_agentdojo.py
|   |   |   |   |   |-- run_agentdyn.sh
|   |   |   |   |   |-- run_injecagent.py
|   |   |   |   |   `-- run_long_context.py
|   |   |   |   `-- src/
|   |   |   |       |-- attacks/
|   |   |   |       |   |-- attack_heuristic.py
|   |   |   |       |   |-- attack_none.py
|   |   |   |       |   `-- __init__.py
|   |   |   |       |-- defenses/
|   |   |   |       |   |-- agentwatcher/
|   |   |   |       |   |   |-- attention_utils.py
|   |   |   |       |   |   |-- defense_agentwatcher.py
|   |   |   |       |   |   |-- __init__.py
|   |   |   |       |   |   `-- utils.py
|   |   |   |       |   |-- datasentinel/
|   |   |   |       |   |   |-- defense_datasentinel.py
|   |   |   |       |   |   |-- __init__.py
|   |   |   |       |   |   `-- OpenPromptInjection/
|   |   |   |       |   |       |-- apps/
|   |   |   |       |   |       |   |-- Application.py
|   |   |   |       |   |       |   |-- bpe.py
|   |   |   |       |   |       |   |-- DataSentinelDetector.py
|   |   |   |       |   |       |   |-- __init__.py
|   |   |   |       |   |       |   |-- PromptLocate.py
|   |   |   |       |   |       |   `-- utils.py
|   |   |   |       |   |       |-- attackers/
|   |   |   |       |   |       |   |-- Attacker.py
|   |   |   |       |   |       |   |-- CombineAttacker.py
|   |   |   |       |   |       |   |-- EscapeCharAttacker.py
|   |   |   |       |   |       |   |-- FakeCompAttacker.py
|   |   |   |       |   |       |   |-- IgnoreAttacker.py
|   |   |   |       |   |       |   |-- __init__.py
|   |   |   |       |   |       |   `-- NaiveAttacker.py
|   |   |   |       |   |       |-- evaluator/
|   |   |   |       |   |       |   |-- Evaluator.py
|   |   |   |       |   |       |   |-- gleu_utils.py
|   |   |   |       |   |       |   |-- __init__.py
|   |   |   |       |   |       |   `-- utils.py
|   |   |   |       |   |       |-- __init__.py
|   |   |   |       |   |       |-- models/
|   |   |   |       |   |       |   |-- DeepSeek.py
|   |   |   |       |   |       |   |-- Flan.py
|   |   |   |       |   |       |   |-- GPT.py
|   |   |   |       |   |       |   |-- __init__.py
|   |   |   |       |   |       |   |-- Internlm.py
|   |   |   |       |   |       |   |-- Llama3.py
|   |   |   |       |   |       |   |-- Llama.py
|   |   |   |       |   |       |   |-- Model.py
|   |   |   |       |   |       |   |-- PaLM2.py
|   |   |   |       |   |       |   |-- QLoraModel.py
|   |   |   |       |   |       |   `-- Vicuna.py
|   |   |   |       |   |       |-- tasks/
|   |   |   |       |   |       |   |-- CompromiseTask.py
|   |   |   |       |   |       |   |-- gigaword.py
|   |   |   |       |   |       |   |-- gleu.py
|   |   |   |       |   |       |   |-- hsol.py
|   |   |   |       |   |       |   |-- __init__.py
|   |   |   |       |   |       |   |-- InjectedTask.py
|   |   |   |       |   |       |   |-- jfleg.py
|   |   |   |       |   |       |   |-- Math500.py
|   |   |   |       |   |       |   |-- ReasoningTask.py
|   |   |   |       |   |       |   |-- sms_spam.py
|   |   |   |       |   |       |   |-- sst2.py
|   |   |   |       |   |       |   |-- TargetTask.py
|   |   |   |       |   |       |   |-- Task.py
|   |   |   |       |   |       |   `-- utils.py
|   |   |   |       |   |       `-- utils/
|   |   |   |       |   |           |-- __init__.py
|   |   |   |       |   |           |-- process_config.py
|   |   |   |       |   |           `-- process_txt.py
|   |   |   |       |   |-- defense_none.py
|   |   |   |       |   |-- gptsafeguard/
|   |   |   |       |   |   |-- defense_gptsafeguard.py
|   |   |   |       |   |   `-- __init__.py
|   |   |   |       |   |-- __init__.py
|   |   |   |       |   |-- monitor_llm_module/
|   |   |   |       |   |   |-- __init__.py
|   |   |   |       |   |   `-- messages.py
|   |   |   |       |   |-- piguard/
|   |   |   |       |   |   |-- defense_piguard.py
|   |   |   |       |   |   `-- __init__.py
|   |   |   |       |   |-- promptarmor/
|   |   |   |       |   |   |-- defense_promptarmor.py
|   |   |   |       |   |   `-- __init__.py
|   |   |   |       |   `-- promptguard/
|   |   |   |       |       |-- defense_promptguard.py
|   |   |   |       |       `-- __init__.py
|   |   |   |       |-- evaluations/
|   |   |   |       |   |-- __init__.py
|   |   |   |       |   |-- llm_judge.py
|   |   |   |       |   |-- longbench_metrics.py
|   |   |   |       |   `-- open_prompt_injection_metrics.py
|   |   |   |       |-- __init__.py
|   |   |   |       |-- llm.py
|   |   |   |       |-- llm_vllm.py
|   |   |   |       `-- utils.py
|   |   |   |-- AgentWatcher_armc_runtime_v1/
|   |   |   |   |-- A15B0_AGENTWATCHER_RECONSTRUCTION_v2_VLLM.json
|   |   |   |   |-- A15B0_AGENTWATCHER_RECONSTRUCTION_v3_COMPLETION_SAFE.json
|   |   |   |   |-- agents/
|   |   |   |   |   |-- agentdojo/
|   |   |   |   |   |   |-- CITATION.bib
|   |   |   |   |   |   |-- CLAUDE.md
|   |   |   |   |   |   |-- CONTRIBUTING.md
|   |   |   |   |   |   |-- .devcontainer/
|   |   |   |   |   |   |   |-- devcontainer.json
|   |   |   |   |   |   |   |-- Dockerfile
|   |   |   |   |   |   |   `-- init-firewall.sh
|   |   |   |   |   |   |-- docs/
|   |   |   |   |   |   |   |-- api/
|   |   |   |   |   |   |   |   |-- agent_pipeline/
|   |   |   |   |   |   |   |   |   |-- basic_elements.md
|   |   |   |   |   |   |   |   |   |-- defenses.md
|   |   |   |   |   |   |   |   |   `-- llms.md
|   |   |   |   |   |   |   |   |-- attacks/
|   |   |   |   |   |   |   |   |   |-- base_attacks.md
|   |   |   |   |   |   |   |   |   |-- baseline_attacks.md
|   |   |   |   |   |   |   |   |   |-- dos_attacks.md
|   |   |   |   |   |   |   |   |   `-- registering_and_loading_attacks.md
|   |   |   |   |   |   |   |   |-- base_tasks.md
|   |   |   |   |   |   |   |   |-- benchmark.md
|   |   |   |   |   |   |   |   |-- functions_runtime.md
|   |   |   |   |   |   |   |   |-- task_suite.md
|   |   |   |   |   |   |   |   `-- types.md
|   |   |   |   |   |   |   |-- changelog.md
|   |   |   |   |   |   |   |-- CNAME
|   |   |   |   |   |   |   |-- concepts/
|   |   |   |   |   |   |   |   |-- agent_pipeline.md
|   |   |   |   |   |   |   |   |-- attacks.md
|   |   |   |   |   |   |   |   |-- functions_runtime.md
|   |   |   |   |   |   |   |   `-- task_suite_and_tasks.md
|   |   |   |   |   |   |   |-- development.md
|   |   |   |   |   |   |   |-- index.md
|   |   |   |   |   |   |   |-- results.md
|   |   |   |   |   |   |   `-- results-table.html
|   |   |   |   |   |   |-- examples/
|   |   |   |   |   |   |   |-- attack.py
|   |   |   |   |   |   |   |-- counter_benchmark/
|   |   |   |   |   |   |   |   |-- benchmark.py
|   |   |   |   |   |   |   |   |-- data/
|   |   |   |   |   |   |   |   |   `-- suites/
|   |   |   |   |   |   |   |   |       `-- counter/
|   |   |   |   |   |   |   |   |           |-- environment.yaml
|   |   |   |   |   |   |   |   |           `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   `-- suites/
|   |   |   |   |   |   |   |       |-- counter/
|   |   |   |   |   |   |   |       |   |-- __init__.py
|   |   |   |   |   |   |   |       |   |-- injection_tasks.py
|   |   |   |   |   |   |   |       |   |-- task_suite.py
|   |   |   |   |   |   |   |       |   `-- user_tasks.py
|   |   |   |   |   |   |   |       |-- __init__.py
|   |   |   |   |   |   |   |       `-- tools.py
|   |   |   |   |   |   |   |-- functions_runtime.py
|   |   |   |   |   |   |   |-- pipeline.py
|   |   |   |   |   |   |   `-- README.md
|   |   |   |   |   |   |-- .github/
|   |   |   |   |   |   |   `-- workflows/
|   |   |   |   |   |   |       |-- CODEOWNERS
|   |   |   |   |   |   |       |-- lint-docs.yaml
|   |   |   |   |   |   |       `-- publish.yaml
|   |   |   |   |   |   |-- .gitignore
|   |   |   |   |   |   |-- LICENSE
|   |   |   |   |   |   |-- mkdocs.yml
|   |   |   |   |   |   |-- notebooks/
|   |   |   |   |   |   |   |-- agent_pipeline_example.ipynb
|   |   |   |   |   |   |   `-- analysis.ipynb
|   |   |   |   |   |   |-- .pre-commit-config.yaml
|   |   |   |   |   |   |-- pyproject.toml
|   |   |   |   |   |   |-- .python-version
|   |   |   |   |   |   |-- README.md
|   |   |   |   |   |   |-- src/
|   |   |   |   |   |   |   `-- agentdojo/
|   |   |   |   |   |   |       |-- agent_pipeline/
|   |   |   |   |   |   |       |   |-- agent_pipeline.py
|   |   |   |   |   |   |       |   |-- base_pipeline_element.py
|   |   |   |   |   |   |       |   |-- basic_elements.py
|   |   |   |   |   |   |       |   |-- errors.py
|   |   |   |   |   |   |       |   |-- ground_truth_pipeline.py
|   |   |   |   |   |   |       |   |-- inference_utils.py
|   |   |   |   |   |   |       |   |-- __init__.py
|   |   |   |   |   |   |       |   |-- llms/
|   |   |   |   |   |   |       |   |   |-- anthropic_llm.py
|   |   |   |   |   |   |       |   |   |-- cohere_llm.py
|   |   |   |   |   |   |       |   |   |-- google_llm.py
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |-- local_llm.py
|   |   |   |   |   |   |       |   |   |-- openai_llm.py
|   |   |   |   |   |   |       |   |   |-- prompting_llm.py
|   |   |   |   |   |   |       |   |   `-- transformers_llm.py
|   |   |   |   |   |   |       |   |-- piarena_defense_adapter.py
|   |   |   |   |   |   |       |   |-- pi_detector.py
|   |   |   |   |   |   |       |   |-- planner.py
|   |   |   |   |   |   |       |   `-- tool_execution.py
|   |   |   |   |   |   |       |-- ast_utils.py
|   |   |   |   |   |   |       |-- attacks/
|   |   |   |   |   |   |       |   |-- attack_registry.py
|   |   |   |   |   |   |       |   |-- base_attacks.py
|   |   |   |   |   |   |       |   |-- baseline_attacks.py
|   |   |   |   |   |   |       |   |-- dos_attacks.py
|   |   |   |   |   |   |       |   |-- important_instructions_attacks.py
|   |   |   |   |   |   |       |   `-- __init__.py
|   |   |   |   |   |   |       |-- base_tasks.py
|   |   |   |   |   |   |       |-- benchmark.py
|   |   |   |   |   |   |       |-- data/
|   |   |   |   |   |   |       |   |-- suites/
|   |   |   |   |   |   |       |   |   |-- banking/
|   |   |   |   |   |   |       |   |   |   |-- environment.yaml
|   |   |   |   |   |   |       |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |       |   |   |-- slack/
|   |   |   |   |   |   |       |   |   |   |-- environment.yaml
|   |   |   |   |   |   |       |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |       |   |   |-- travel/
|   |   |   |   |   |   |       |   |   |   |-- environment.yaml
|   |   |   |   |   |   |       |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |       |   |   `-- workspace/
|   |   |   |   |   |   |       |   |       |-- environment.yaml
|   |   |   |   |   |   |       |   |       |-- gpt_prompts.txt
|   |   |   |   |   |   |       |   |       |-- include/
|   |   |   |   |   |   |       |   |       |   |-- calendar.yaml
|   |   |   |   |   |   |       |   |       |   |-- cloud_drive.yaml
|   |   |   |   |   |   |       |   |       |   `-- inbox.yaml
|   |   |   |   |   |   |       |   |       `-- injection_vectors.yaml
|   |   |   |   |   |   |       |   `-- system_messages.yaml
|   |   |   |   |   |   |       |-- default_suites/
|   |   |   |   |   |   |       |   |-- __init__.py
|   |   |   |   |   |   |       |   |-- v1/
|   |   |   |   |   |   |       |   |   |-- banking/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |       |   |   |   |-- task_suite.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |-- slack/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |       |   |   |   |-- task_suite.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   |-- tools/
|   |   |   |   |   |   |       |   |   |   |-- banking_client.py
|   |   |   |   |   |   |       |   |   |   |-- calendar_client.py
|   |   |   |   |   |   |       |   |   |   |-- cloud_drive_client.py
|   |   |   |   |   |   |       |   |   |   |-- email_client.py
|   |   |   |   |   |   |       |   |   |   |-- file_reader.py
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   |-- slack.py
|   |   |   |   |   |   |       |   |   |   |-- travel_booking_client.py
|   |   |   |   |   |   |       |   |   |   |-- types.py
|   |   |   |   |   |   |       |   |   |   |-- user_account.py
|   |   |   |   |   |   |       |   |   |   `-- web.py
|   |   |   |   |   |   |       |   |   |-- travel/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |       |   |   |   |-- task_suite.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   `-- workspace/
|   |   |   |   |   |   |       |   |       |-- __init__.py
|   |   |   |   |   |   |       |   |       |-- injection_tasks.py
|   |   |   |   |   |   |       |   |       |-- task_suite.py
|   |   |   |   |   |   |       |   |       `-- user_tasks.py
|   |   |   |   |   |   |       |   |-- v1_1/
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   `-- travel/
|   |   |   |   |   |   |       |   |       `-- user_tasks.py
|   |   |   |   |   |   |       |   |-- v1_1_1/
|   |   |   |   |   |   |       |   |   |-- banking/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |-- slack/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   |-- travel/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   `-- workspace/
|   |   |   |   |   |   |       |   |       `-- user_tasks.py
|   |   |   |   |   |   |       |   |-- v1_1_2/
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |-- travel/
|   |   |   |   |   |   |       |   |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |   `-- injection_tasks.py
|   |   |   |   |   |   |       |   |   `-- workspace/
|   |   |   |   |   |   |       |   |       |-- __init__.py
|   |   |   |   |   |   |       |   |       |-- injection_tasks.py
|   |   |   |   |   |   |       |   |       `-- user_tasks.py
|   |   |   |   |   |   |       |   |-- v1_2/
|   |   |   |   |   |   |       |   |   |-- banking/
|   |   |   |   |   |   |       |   |   |   `-- injection_tasks.py
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   |-- slack/
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   |-- travel/
|   |   |   |   |   |   |       |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |       |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |       |   |   `-- workspace/
|   |   |   |   |   |   |       |   |       |-- injection_tasks.py
|   |   |   |   |   |   |       |   |       `-- user_tasks.py
|   |   |   |   |   |   |       |   |-- v1_2_1/
|   |   |   |   |   |   |       |   |   |-- __init__.py
|   |   |   |   |   |   |       |   |   `-- workspace/
|   |   |   |   |   |   |       |   |       `-- injection_tasks.py
|   |   |   |   |   |   |       |   `-- v1_2_2/
|   |   |   |   |   |   |       |       |-- banking/
|   |   |   |   |   |   |       |       |   |-- __init__.py
|   |   |   |   |   |   |       |       |   `-- user_tasks.py
|   |   |   |   |   |   |       |       |-- __init__.py
|   |   |   |   |   |   |       |       `-- workspace/
|   |   |   |   |   |   |       |           |-- __init__.py
|   |   |   |   |   |   |       |           `-- user_tasks.py
|   |   |   |   |   |   |       |-- functions_runtime.py
|   |   |   |   |   |   |       |-- __init__.py
|   |   |   |   |   |   |       |-- logging.py
|   |   |   |   |   |   |       |-- models.py
|   |   |   |   |   |   |       |-- scripts/
|   |   |   |   |   |   |       |   |-- benchmark.py
|   |   |   |   |   |   |       |   |-- check_suites.py
|   |   |   |   |   |   |       |   `-- __init__.py
|   |   |   |   |   |   |       |-- strenum.py
|   |   |   |   |   |   |       |-- task_suite/
|   |   |   |   |   |   |       |   |-- __init__.py
|   |   |   |   |   |   |       |   |-- load_suites.py
|   |   |   |   |   |   |       |   |-- task_combinators.py
|   |   |   |   |   |   |       |   `-- task_suite.py
|   |   |   |   |   |   |       |-- types.py
|   |   |   |   |   |   |       `-- yaml_loader.py
|   |   |   |   |   |   |-- tests/
|   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |-- test_agent_pipeline/
|   |   |   |   |   |   |   |   |-- test_anthropic_llm.py
|   |   |   |   |   |   |   |   |-- test_cohere_llm.py
|   |   |   |   |   |   |   |   |-- test_google_llm.py
|   |   |   |   |   |   |   |   |-- test_pi_detector.py
|   |   |   |   |   |   |   |   `-- test_prompting_llm.py
|   |   |   |   |   |   |   |-- test_ast_utils.py
|   |   |   |   |   |   |   |-- test_benchmark.py
|   |   |   |   |   |   |   |-- test_functions_runtime/
|   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   `-- test_functions_runtime.py
|   |   |   |   |   |   |   `-- test_workspace_user_tasks.py
|   |   |   |   |   |   |-- util_scripts/
|   |   |   |   |   |   |   |-- create_results_table.py
|   |   |   |   |   |   |   |-- run_vllm_parallel.sh
|   |   |   |   |   |   |   `-- run_vllm.sh
|   |   |   |   |   |   `-- uv.lock
|   |   |   |   |   |-- agentdyn/
|   |   |   |   |   |   |-- agentdojo_README.md
|   |   |   |   |   |   |-- CITATION.bib
|   |   |   |   |   |   |-- CLAUDE.md
|   |   |   |   |   |   |-- CONTRIBUTING.md
|   |   |   |   |   |   |-- docs/
|   |   |   |   |   |   |   |-- api/
|   |   |   |   |   |   |   |   |-- agent_pipeline/
|   |   |   |   |   |   |   |   |   |-- basic_elements.md
|   |   |   |   |   |   |   |   |   |-- defenses.md
|   |   |   |   |   |   |   |   |   `-- llms.md
|   |   |   |   |   |   |   |   |-- attacks/
|   |   |   |   |   |   |   |   |   |-- base_attacks.md
|   |   |   |   |   |   |   |   |   |-- baseline_attacks.md
|   |   |   |   |   |   |   |   |   |-- dos_attacks.md
|   |   |   |   |   |   |   |   |   `-- registering_and_loading_attacks.md
|   |   |   |   |   |   |   |   |-- base_tasks.md
|   |   |   |   |   |   |   |   |-- benchmark.md
|   |   |   |   |   |   |   |   |-- functions_runtime.md
|   |   |   |   |   |   |   |   |-- task_suite.md
|   |   |   |   |   |   |   |   `-- types.md
|   |   |   |   |   |   |   |-- changelog.md
|   |   |   |   |   |   |   |-- CNAME
|   |   |   |   |   |   |   |-- concepts/
|   |   |   |   |   |   |   |   |-- agent_pipeline.md
|   |   |   |   |   |   |   |   |-- attacks.md
|   |   |   |   |   |   |   |   |-- functions_runtime.md
|   |   |   |   |   |   |   |   `-- task_suite_and_tasks.md
|   |   |   |   |   |   |   |-- development.md
|   |   |   |   |   |   |   |-- index.md
|   |   |   |   |   |   |   |-- results.md
|   |   |   |   |   |   |   `-- results-table.html
|   |   |   |   |   |   |-- examples/
|   |   |   |   |   |   |   |-- attack.py
|   |   |   |   |   |   |   |-- counter_benchmark/
|   |   |   |   |   |   |   |   |-- benchmark.py
|   |   |   |   |   |   |   |   |-- data/
|   |   |   |   |   |   |   |   |   `-- suites/
|   |   |   |   |   |   |   |   |       `-- counter/
|   |   |   |   |   |   |   |   |           |-- environment.yaml
|   |   |   |   |   |   |   |   |           `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   `-- suites/
|   |   |   |   |   |   |   |       |-- counter/
|   |   |   |   |   |   |   |       |   |-- __init__.py
|   |   |   |   |   |   |   |       |   |-- injection_tasks.py
|   |   |   |   |   |   |   |       |   |-- task_suite.py
|   |   |   |   |   |   |   |       |   `-- user_tasks.py
|   |   |   |   |   |   |   |       |-- __init__.py
|   |   |   |   |   |   |   |       `-- tools.py
|   |   |   |   |   |   |   |-- functions_runtime.py
|   |   |   |   |   |   |   |-- pipeline.py
|   |   |   |   |   |   |   `-- README.md
|   |   |   |   |   |   |-- LICENSE
|   |   |   |   |   |   |-- mkdocs.yml
|   |   |   |   |   |   |-- notebooks/
|   |   |   |   |   |   |   |-- agent_pipeline_example.ipynb
|   |   |   |   |   |   |   `-- analysis.ipynb
|   |   |   |   |   |   |-- pyproject.toml
|   |   |   |   |   |   |-- README.md
|   |   |   |   |   |   |-- src/
|   |   |   |   |   |   |   |-- agentdojo/
|   |   |   |   |   |   |   |   |-- agent_pipeline/
|   |   |   |   |   |   |   |   |   |-- agent_pipeline.py
|   |   |   |   |   |   |   |   |   |-- base_pipeline_element.py
|   |   |   |   |   |   |   |   |   |-- basic_elements.py
|   |   |   |   |   |   |   |   |   |-- errors.py
|   |   |   |   |   |   |   |   |   |-- ground_truth_pipeline.py
|   |   |   |   |   |   |   |   |   |-- inference_utils.py
|   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |-- llms/
|   |   |   |   |   |   |   |   |   |   |-- anthropic_llm.py
|   |   |   |   |   |   |   |   |   |   |-- cohere_llm.py
|   |   |   |   |   |   |   |   |   |   |-- google_llm.py
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |-- local_llm.py
|   |   |   |   |   |   |   |   |   |   |-- openai_llm.py
|   |   |   |   |   |   |   |   |   |   `-- prompting_llm.py
|   |   |   |   |   |   |   |   |   |-- piarena_defense_adapter.py
|   |   |   |   |   |   |   |   |   |-- pi_detector.py
|   |   |   |   |   |   |   |   |   |-- planner.py
|   |   |   |   |   |   |   |   |   `-- tool_execution.py
|   |   |   |   |   |   |   |   |-- ast_utils.py
|   |   |   |   |   |   |   |   |-- attacks/
|   |   |   |   |   |   |   |   |   |-- attack_registry.py
|   |   |   |   |   |   |   |   |   |-- base_attacks.py
|   |   |   |   |   |   |   |   |   |-- baseline_attacks.py
|   |   |   |   |   |   |   |   |   |-- dos_attacks.py
|   |   |   |   |   |   |   |   |   |-- important_instructions_attacks.py
|   |   |   |   |   |   |   |   |   `-- __init__.py
|   |   |   |   |   |   |   |   |-- base_tasks.py
|   |   |   |   |   |   |   |   |-- benchmark.py
|   |   |   |   |   |   |   |   |-- data/
|   |   |   |   |   |   |   |   |   |-- suites/
|   |   |   |   |   |   |   |   |   |   |-- banking/
|   |   |   |   |   |   |   |   |   |   |   |-- environment.yaml
|   |   |   |   |   |   |   |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   |   |-- dailylife/
|   |   |   |   |   |   |   |   |   |   |   |-- environment.yaml
|   |   |   |   |   |   |   |   |   |   |   |-- include/
|   |   |   |   |   |   |   |   |   |   |   |   |-- bank_database.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- calendar.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- email_database.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- filesystem.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- github_platform.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- shopping_platform.yaml
|   |   |   |   |   |   |   |   |   |   |   |   `-- web_database.yaml
|   |   |   |   |   |   |   |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   |   |-- github/
|   |   |   |   |   |   |   |   |   |   |   |-- environment.yaml
|   |   |   |   |   |   |   |   |   |   |   |-- include/
|   |   |   |   |   |   |   |   |   |   |   |   |-- bank_database.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- calendar.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- email_database.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- filesystem.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- github_platform.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- shopping_platform.yaml
|   |   |   |   |   |   |   |   |   |   |   |   `-- web_database.yaml
|   |   |   |   |   |   |   |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   |   |-- shopping/
|   |   |   |   |   |   |   |   |   |   |   |-- environment.yaml
|   |   |   |   |   |   |   |   |   |   |   |-- environment——.yaml
|   |   |   |   |   |   |   |   |   |   |   |-- include/
|   |   |   |   |   |   |   |   |   |   |   |   |-- bank_database.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- calendar.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- email_database.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- filesystem.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- github_platform.yaml
|   |   |   |   |   |   |   |   |   |   |   |   |-- shopping_platform.yaml
|   |   |   |   |   |   |   |   |   |   |   |   `-- web_database.yaml
|   |   |   |   |   |   |   |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   |   |-- slack/
|   |   |   |   |   |   |   |   |   |   |   |-- environment.yaml
|   |   |   |   |   |   |   |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   |   |-- travel/
|   |   |   |   |   |   |   |   |   |   |   |-- environment.yaml
|   |   |   |   |   |   |   |   |   |   |   `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   |   `-- workspace/
|   |   |   |   |   |   |   |   |   |       |-- environment.yaml
|   |   |   |   |   |   |   |   |   |       |-- gpt_prompts.txt
|   |   |   |   |   |   |   |   |   |       |-- include/
|   |   |   |   |   |   |   |   |   |       |   |-- calendar.yaml
|   |   |   |   |   |   |   |   |   |       |   |-- cloud_drive.yaml
|   |   |   |   |   |   |   |   |   |       |   `-- inbox.yaml
|   |   |   |   |   |   |   |   |   |       `-- injection_vectors.yaml
|   |   |   |   |   |   |   |   |   `-- system_messages.yaml
|   |   |   |   |   |   |   |   |-- default_suites/
|   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |-- v1/
|   |   |   |   |   |   |   |   |   |   |-- banking/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   |-- task_suite.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- dailylife/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   |-- task_suite.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- github/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   |-- task_suite.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |-- shopping/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   |-- task_suite.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- slack/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   |-- task_suite.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- tools/
|   |   |   |   |   |   |   |   |   |   |   |-- banking_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- calendar_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- cloud_drive_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- dynamic_banking_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- dynamic_calendar_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- dynamic_email_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- dynamic_web_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- email_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- file_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- file_reader.py
|   |   |   |   |   |   |   |   |   |   |   |-- github_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- shopping_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- slack.py
|   |   |   |   |   |   |   |   |   |   |   |-- tool_registry.py
|   |   |   |   |   |   |   |   |   |   |   |-- travel_booking_client.py
|   |   |   |   |   |   |   |   |   |   |   |-- types.py
|   |   |   |   |   |   |   |   |   |   |   |-- user_account.py
|   |   |   |   |   |   |   |   |   |   |   |-- utils.py
|   |   |   |   |   |   |   |   |   |   |   `-- web.py
|   |   |   |   |   |   |   |   |   |   |-- travel/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   |-- task_suite.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   `-- workspace/
|   |   |   |   |   |   |   |   |   |       |-- __init__.py
|   |   |   |   |   |   |   |   |   |       |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |       |-- task_suite.py
|   |   |   |   |   |   |   |   |   |       `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |-- v1_1/
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   `-- travel/
|   |   |   |   |   |   |   |   |   |       `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |-- v1_1_1/
|   |   |   |   |   |   |   |   |   |   |-- banking/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |-- slack/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- travel/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   `-- workspace/
|   |   |   |   |   |   |   |   |   |       `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |-- v1_1_2/
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |-- travel/
|   |   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |   `-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   `-- workspace/
|   |   |   |   |   |   |   |   |   |       |-- __init__.py
|   |   |   |   |   |   |   |   |   |       |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |       `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |-- v1_2/
|   |   |   |   |   |   |   |   |   |   |-- banking/
|   |   |   |   |   |   |   |   |   |   |   `-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   |-- slack/
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   |-- travel/
|   |   |   |   |   |   |   |   |   |   |   |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |   |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |   `-- workspace/
|   |   |   |   |   |   |   |   |   |       |-- injection_tasks.py
|   |   |   |   |   |   |   |   |   |       `-- user_tasks.py
|   |   |   |   |   |   |   |   |   |-- v1_2_1/
|   |   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |   `-- workspace/
|   |   |   |   |   |   |   |   |   |       `-- injection_tasks.py
|   |   |   |   |   |   |   |   |   `-- v1_2_2/
|   |   |   |   |   |   |   |   |       |-- banking/
|   |   |   |   |   |   |   |   |       |   |-- __init__.py
|   |   |   |   |   |   |   |   |       |   `-- user_tasks.py
|   |   |   |   |   |   |   |   |       |-- __init__.py
|   |   |   |   |   |   |   |   |       `-- workspace/
|   |   |   |   |   |   |   |   |           |-- __init__.py
|   |   |   |   |   |   |   |   |           `-- user_tasks.py
|   |   |   |   |   |   |   |   |-- functions_runtime.py
|   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |-- models.py
|   |   |   |   |   |   |   |   |-- scripts/
|   |   |   |   |   |   |   |   |   |-- benchmark.py
|   |   |   |   |   |   |   |   |   |-- check_suites.py
|   |   |   |   |   |   |   |   |   `-- __init__.py
|   |   |   |   |   |   |   |   |-- strenum.py
|   |   |   |   |   |   |   |   |-- task_suite/
|   |   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   |   |-- load_suites.py
|   |   |   |   |   |   |   |   |   |-- task_combinators.py
|   |   |   |   |   |   |   |   |   `-- task_suite.py
|   |   |   |   |   |   |   |   |-- types.py
|   |   |   |   |   |   |   |   `-- yaml_loader.py
|   |   |   |   |   |   |   `-- runs/
|   |   |   |   |   |   |       `-- gpt-4o-2024-08-06-piarena-agentwatcher/
|   |   |   |   |   |   |           |-- dailylife/
|   |   |   |   |   |   |           |   |-- injection_task_0/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_1/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_2/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_3/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_4/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_5/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_6/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_7/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_8/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_9/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_0/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_1/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_10/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_11/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_12/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_13/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_14/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_15/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_16/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_17/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_18/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_19/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_2/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_3/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_4/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_5/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_8.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_6/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_9.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_7/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_8/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   `-- user_task_9/
|   |   |   |   |   |   |           |       |-- important_instructions/
|   |   |   |   |   |   |           |       |   |-- injection_task_2.json
|   |   |   |   |   |   |           |       |   |-- injection_task_3.json
|   |   |   |   |   |   |           |       |   |-- injection_task_4.json
|   |   |   |   |   |   |           |       |   |-- injection_task_5.json
|   |   |   |   |   |   |           |       |   |-- injection_task_6.json
|   |   |   |   |   |   |           |       |   |-- injection_task_7.json
|   |   |   |   |   |   |           |       |   |-- injection_task_8.json
|   |   |   |   |   |   |           |       |   `-- injection_task_9.json
|   |   |   |   |   |   |           |       `-- none/
|   |   |   |   |   |   |           |           `-- none.json
|   |   |   |   |   |   |           |-- github/
|   |   |   |   |   |   |           |   |-- injection_task_0/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_1/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_2/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_3/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_4/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_5/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_6/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_7/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- injection_task_8/
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_0/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_1/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_10/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_11/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_12/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_13/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_14/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_15/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_16/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_17/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_18/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_19/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_2/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_3/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_4/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_5/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_6/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_7.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_7/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_1.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_6.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   |-- user_task_8/
|   |   |   |   |   |   |           |   |   |-- important_instructions/
|   |   |   |   |   |   |           |   |   |   |-- injection_task_0.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_2.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_3.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_4.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_5.json
|   |   |   |   |   |   |           |   |   |   |-- injection_task_7.json
|   |   |   |   |   |   |           |   |   |   `-- injection_task_8.json
|   |   |   |   |   |   |           |   |   `-- none/
|   |   |   |   |   |   |           |   |       `-- none.json
|   |   |   |   |   |   |           |   `-- user_task_9/
|   |   |   |   |   |   |           |       |-- important_instructions/
|   |   |   |   |   |   |           |       |   |-- injection_task_0.json
|   |   |   |   |   |   |           |       |   |-- injection_task_1.json
|   |   |   |   |   |   |           |       |   |-- injection_task_2.json
|   |   |   |   |   |   |           |       |   |-- injection_task_3.json
|   |   |   |   |   |   |           |       |   |-- injection_task_6.json
|   |   |   |   |   |   |           |       |   |-- injection_task_7.json
|   |   |   |   |   |   |           |       |   `-- injection_task_8.json
|   |   |   |   |   |   |           |       `-- none/
|   |   |   |   |   |   |           |           `-- none.json
|   |   |   |   |   |   |           `-- shopping/
|   |   |   |   |   |   |               |-- injection_task_0/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_1/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_2/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_3/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_4/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_5/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_6/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_7/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- injection_task_8/
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_0/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_1/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_10/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_11/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_12/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_13/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_14/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_15/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_16/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_17/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_18/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_19/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_2/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_3/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_4/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_5/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_6/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_7/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               |-- user_task_8/
|   |   |   |   |   |   |               |   |-- important_instructions/
|   |   |   |   |   |   |               |   |   |-- injection_task_0.json
|   |   |   |   |   |   |               |   |   |-- injection_task_1.json
|   |   |   |   |   |   |               |   |   |-- injection_task_2.json
|   |   |   |   |   |   |               |   |   |-- injection_task_3.json
|   |   |   |   |   |   |               |   |   |-- injection_task_4.json
|   |   |   |   |   |   |               |   |   |-- injection_task_5.json
|   |   |   |   |   |   |               |   |   |-- injection_task_6.json
|   |   |   |   |   |   |               |   |   |-- injection_task_7.json
|   |   |   |   |   |   |               |   |   `-- injection_task_8.json
|   |   |   |   |   |   |               |   `-- none/
|   |   |   |   |   |   |               |       `-- none.json
|   |   |   |   |   |   |               `-- user_task_9/
|   |   |   |   |   |   |                   |-- important_instructions/
|   |   |   |   |   |   |                   |   |-- injection_task_0.json
|   |   |   |   |   |   |                   |   |-- injection_task_1.json
|   |   |   |   |   |   |                   |   |-- injection_task_2.json
|   |   |   |   |   |   |                   |   |-- injection_task_3.json
|   |   |   |   |   |   |                   |   |-- injection_task_4.json
|   |   |   |   |   |   |                   |   |-- injection_task_6.json
|   |   |   |   |   |   |                   |   `-- injection_task_8.json
|   |   |   |   |   |   |                   `-- none/
|   |   |   |   |   |   |                       `-- none.json
|   |   |   |   |   |   |-- tests/
|   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |-- test_agent_pipeline/
|   |   |   |   |   |   |   |   |-- test_anthropic_llm.py
|   |   |   |   |   |   |   |   |-- test_cohere_llm.py
|   |   |   |   |   |   |   |   |-- test_google_llm.py
|   |   |   |   |   |   |   |   |-- test_pi_detector.py
|   |   |   |   |   |   |   |   `-- test_prompting_llm.py
|   |   |   |   |   |   |   |-- test_ast_utils.py
|   |   |   |   |   |   |   |-- test_benchmark.py
|   |   |   |   |   |   |   |-- test_functions_runtime/
|   |   |   |   |   |   |   |   |-- __init__.py
|   |   |   |   |   |   |   |   `-- test_functions_runtime.py
|   |   |   |   |   |   |   `-- test_workspace_user_tasks.py
|   |   |   |   |   |   |-- util_scripts/
|   |   |   |   |   |   |   |-- create_results_table.py
|   |   |   |   |   |   |   |-- run_vllm_parallel.sh
|   |   |   |   |   |   |   `-- run_vllm.sh
|   |   |   |   |   |   `-- uv.lock
|   |   |   |   |   `-- InjecAgent/
|   |   |   |   |       |-- asset/
|   |   |   |   |       |   |-- overview.pdf
|   |   |   |   |       |   `-- overview.png
|   |   |   |   |       |-- data/
|   |   |   |   |       |   |-- attacker_cases_dh.jsonl
|   |   |   |   |       |   |-- attacker_cases_ds.jsonl
|   |   |   |   |       |   |-- attacker_simulated_responses.json
|   |   |   |   |       |   |-- test_cases_dh_base.json
|   |   |   |   |       |   |-- test_cases_dh_enhanced.json
|   |   |   |   |       |   |-- test_cases_ds_base.json
|   |   |   |   |       |   |-- test_cases_ds_enhanced.json
|   |   |   |   |       |   |-- tools.json
|   |   |   |   |       |   `-- user_cases.jsonl
|   |   |   |   |       |-- .gitignore
|   |   |   |   |       |-- LICENCE
|   |   |   |   |       |-- README.md
|   |   |   |   |       |-- requirements.txt
|   |   |   |   |       `-- src/
|   |   |   |   |           |-- evaluate_finetuned_agent.py
|   |   |   |   |           |-- evaluate_prompted_agent.py
|   |   |   |   |           |-- models.py
|   |   |   |   |           |-- output_parsing.py
|   |   |   |   |           |-- params.py
|   |   |   |   |           |-- prompts/
|   |   |   |   |           |   |-- agent_prompts.py
|   |   |   |   |           |   |-- generation_prompts.py
|   |   |   |   |           |   `-- prompt_template.py
|   |   |   |   |           `-- utils.py
|   |   |   |   |-- assets/
|   |   |   |   |   |-- fig_illustration.jpg
|   |   |   |   |   |-- figure1_agentdyn_benign_utility_asr.png
|   |   |   |   |   `-- .gitkeep
|   |   |   |   |-- configs/
|   |   |   |   |   `-- openai_configs/
|   |   |   |   |       `-- gpt-4o-mini.yaml
|   |   |   |   |-- datasets/
|   |   |   |   |   `-- wasp.json
|   |   |   |   |-- .gitignore
|   |   |   |   |-- main_agentdojo.py
|   |   |   |   |-- main_injecagent.py
|   |   |   |   |-- main.py
|   |   |   |   |-- README.md
|   |   |   |   |-- requirements.txt
|   |   |   |   |-- results/
|   |   |   |   |   `-- agent_evaluations/
|   |   |   |   |       `-- agentdojo/
|   |   |   |   |           |-- A15B0_ARMC_DEV_SMOKE_REPAIRED/
|   |   |   |   |           |   `-- gpt-4o-mini-piarena-agentwatcher/
|   |   |   |   |           |       `-- workspace/
|   |   |   |   |           |           |-- injection_task_0/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_1/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_10/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_11/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_12/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_13/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_2/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_3/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_4/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_5/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_6/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_7/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_8/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_9/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           `-- user_task_9/
|   |   |   |   |           |               `-- tool_knowledge/
|   |   |   |   |           |                   `-- injection_task_2.json
|   |   |   |   |           |-- A15B0_ARMC_SCI_IMPORTANT_INSTRUCTIONS_200/
|   |   |   |   |           |   `-- gpt-4o-mini-piarena-agentwatcher/
|   |   |   |   |           |       |-- banking/
|   |   |   |   |           |       |   |-- injection_task_0/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_1/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_2/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_3/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_4/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_5/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_6/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_7/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_8/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- user_task_0/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_1.json
|   |   |   |   |           |       |   |       `-- injection_task_4.json
|   |   |   |   |           |       |   |-- user_task_1/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   |-- user_task_10/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_1.json
|   |   |   |   |           |       |   |       `-- injection_task_4.json
|   |   |   |   |           |       |   |-- user_task_11/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   |-- user_task_13/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_7.json
|   |   |   |   |           |       |   |       `-- injection_task_8.json
|   |   |   |   |           |       |   |-- user_task_14/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_0.json
|   |   |   |   |           |       |   |       |-- injection_task_2.json
|   |   |   |   |           |       |   |       |-- injection_task_5.json
|   |   |   |   |           |       |   |       `-- injection_task_8.json
|   |   |   |   |           |       |   |-- user_task_2/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_0.json
|   |   |   |   |           |       |   |       `-- injection_task_3.json
|   |   |   |   |           |       |   |-- user_task_3/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_6.json
|   |   |   |   |           |       |   |       `-- injection_task_8.json
|   |   |   |   |           |       |   |-- user_task_4/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_0.json
|   |   |   |   |           |       |   |       |-- injection_task_2.json
|   |   |   |   |           |       |   |       `-- injection_task_3.json
|   |   |   |   |           |       |   |-- user_task_5/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_1.json
|   |   |   |   |           |       |   |       `-- injection_task_2.json
|   |   |   |   |           |       |   |-- user_task_6/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_0.json
|   |   |   |   |           |       |   |       |-- injection_task_4.json
|   |   |   |   |           |       |   |       |-- injection_task_5.json
|   |   |   |   |           |       |   |       `-- injection_task_8.json
|   |   |   |   |           |       |   |-- user_task_7/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_1.json
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   |-- user_task_8/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_1.json
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   `-- user_task_9/
|   |   |   |   |           |       |       `-- important_instructions/
|   |   |   |   |           |       |           |-- injection_task_0.json
|   |   |   |   |           |       |           |-- injection_task_3.json
|   |   |   |   |           |       |           `-- injection_task_5.json
|   |   |   |   |           |       |-- slack/
|   |   |   |   |           |       |   |-- injection_task_1/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_2/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_3/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_4/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_5/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- user_task_1/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_1.json
|   |   |   |   |           |       |   |       `-- injection_task_4.json
|   |   |   |   |           |       |   |-- user_task_10/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_3.json
|   |   |   |   |           |       |   |-- user_task_11/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   |-- user_task_12/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_1.json
|   |   |   |   |           |       |   |       |-- injection_task_2.json
|   |   |   |   |           |       |   |       `-- injection_task_4.json
|   |   |   |   |           |       |   |-- user_task_13/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   |-- user_task_15/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_1.json
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   |-- user_task_16/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_4.json
|   |   |   |   |           |       |   |-- user_task_17/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_3.json
|   |   |   |   |           |       |   |       `-- injection_task_4.json
|   |   |   |   |           |       |   |-- user_task_18/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_2.json
|   |   |   |   |           |       |   |       `-- injection_task_3.json
|   |   |   |   |           |       |   |-- user_task_19/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_1.json
|   |   |   |   |           |       |   |       |-- injection_task_2.json
|   |   |   |   |           |       |   |       |-- injection_task_3.json
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   |-- user_task_2/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_1.json
|   |   |   |   |           |       |   |-- user_task_20/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_4.json
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   |-- user_task_3/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_2.json
|   |   |   |   |           |       |   |       `-- injection_task_3.json
|   |   |   |   |           |       |   |-- user_task_4/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_4.json
|   |   |   |   |           |       |   |-- user_task_6/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_3.json
|   |   |   |   |           |       |   |-- user_task_7/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_2.json
|   |   |   |   |           |       |   |-- user_task_8/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_2.json
|   |   |   |   |           |       |   `-- user_task_9/
|   |   |   |   |           |       |       `-- important_instructions/
|   |   |   |   |           |       |           `-- injection_task_2.json
|   |   |   |   |           |       |-- travel/
|   |   |   |   |           |       |   |-- injection_task_0/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_1/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_2/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_3/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_4/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_5/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- injection_task_6/
|   |   |   |   |           |       |   |   `-- none/
|   |   |   |   |           |       |   |       `-- none.json
|   |   |   |   |           |       |   |-- user_task_0/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_4.json
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   |-- user_task_1/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_2.json
|   |   |   |   |           |       |   |-- user_task_10/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_2.json
|   |   |   |   |           |       |   |-- user_task_11/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_2.json
|   |   |   |   |           |       |   |       |-- injection_task_4.json
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   |-- user_task_12/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   |-- user_task_13/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_2.json
|   |   |   |   |           |       |   |       |-- injection_task_3.json
|   |   |   |   |           |       |   |       `-- injection_task_4.json
|   |   |   |   |           |       |   |-- user_task_14/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_4.json
|   |   |   |   |           |       |   |       `-- injection_task_6.json
|   |   |   |   |           |       |   |-- user_task_15/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_5.json
|   |   |   |   |           |       |   |       `-- injection_task_6.json
|   |   |   |   |           |       |   |-- user_task_16/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_4.json
|   |   |   |   |           |       |   |-- user_task_18/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_5.json
|   |   |   |   |           |       |   |       `-- injection_task_6.json
|   |   |   |   |           |       |   |-- user_task_19/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_2.json
|   |   |   |   |           |       |   |       |-- injection_task_4.json
|   |   |   |   |           |       |   |       `-- injection_task_5.json
|   |   |   |   |           |       |   |-- user_task_2/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_5.json
|   |   |   |   |           |       |   |       `-- injection_task_6.json
|   |   |   |   |           |       |   |-- user_task_4/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_2.json
|   |   |   |   |           |       |   |-- user_task_5/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_1.json
|   |   |   |   |           |       |   |       `-- injection_task_2.json
|   |   |   |   |           |       |   |-- user_task_6/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_0.json
|   |   |   |   |           |       |   |       `-- injection_task_1.json
|   |   |   |   |           |       |   |-- user_task_7/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       `-- injection_task_0.json
|   |   |   |   |           |       |   |-- user_task_8/
|   |   |   |   |           |       |   |   `-- important_instructions/
|   |   |   |   |           |       |   |       |-- injection_task_1.json
|   |   |   |   |           |       |   |       `-- injection_task_6.json
|   |   |   |   |           |       |   `-- user_task_9/
|   |   |   |   |           |       |       `-- important_instructions/
|   |   |   |   |           |       |           `-- injection_task_6.json
|   |   |   |   |           |       `-- workspace/
|   |   |   |   |           |           |-- injection_task_0/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_1/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_10/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_11/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_12/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_13/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_2/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_3/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_4/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_5/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_6/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_7/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_8/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- injection_task_9/
|   |   |   |   |           |           |   `-- none/
|   |   |   |   |           |           |       `-- none.json
|   |   |   |   |           |           |-- user_task_0/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_11.json
|   |   |   |   |           |           |       |-- injection_task_3.json
|   |   |   |   |           |           |       `-- injection_task_6.json
|   |   |   |   |           |           |-- user_task_1/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_11.json
|   |   |   |   |           |           |       `-- injection_task_13.json
|   |   |   |   |           |           |-- user_task_10/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       `-- injection_task_1.json
|   |   |   |   |           |           |-- user_task_11/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_1.json
|   |   |   |   |           |           |       |-- injection_task_2.json
|   |   |   |   |           |           |       `-- injection_task_6.json
|   |   |   |   |           |           |-- user_task_12/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_12.json
|   |   |   |   |           |           |       |-- injection_task_13.json
|   |   |   |   |           |           |       |-- injection_task_2.json
|   |   |   |   |           |           |       |-- injection_task_5.json
|   |   |   |   |           |           |       |-- injection_task_7.json
|   |   |   |   |           |           |       `-- injection_task_9.json
|   |   |   |   |           |           |-- user_task_13/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       `-- injection_task_11.json
|   |   |   |   |           |           |-- user_task_14/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       `-- injection_task_0.json
|   |   |   |   |           |           |-- user_task_15/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_3.json
|   |   |   |   |           |           |       |-- injection_task_6.json
|   |   |   |   |           |           |       `-- injection_task_9.json
|   |   |   |   |           |           |-- user_task_16/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_0.json
|   |   |   |   |           |           |       `-- injection_task_7.json
|   |   |   |   |           |           |-- user_task_17/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_10.json
|   |   |   |   |           |           |       |-- injection_task_13.json
|   |   |   |   |           |           |       |-- injection_task_4.json
|   |   |   |   |           |           |       |-- injection_task_6.json
|   |   |   |   |           |           |       `-- injection_task_7.json
|   |   |   |   |           |           |-- user_task_18/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_10.json
|   |   |   |   |           |           |       |-- injection_task_11.json
|   |   |   |   |           |           |       |-- injection_task_12.json
|   |   |   |   |           |           |       |-- injection_task_1.json
|   |   |   |   |           |           |       `-- injection_task_9.json
|   |   |   |   |           |           |-- user_task_2/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_2.json
|   |   |   |   |           |           |       |-- injection_task_4.json
|   |   |   |   |           |           |       `-- injection_task_6.json
|   |   |   |   |           |           |-- user_task_20/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_2.json
|   |   |   |   |           |           |       `-- injection_task_4.json
|   |   |   |   |           |           |-- user_task_21/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       `-- injection_task_7.json
|   |   |   |   |           |           |-- user_task_22/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_0.json
|   |   |   |   |           |           |       |-- injection_task_10.json
|   |   |   |   |           |           |       |-- injection_task_1.json
|   |   |   |   |           |           |       |-- injection_task_4.json
|   |   |   |   |           |           |       `-- injection_task_9.json
|   |   |   |   |           |           |-- user_task_23/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_11.json
|   |   |   |   |           |           |       |-- injection_task_2.json
|   |   |   |   |           |           |       |-- injection_task_7.json
|   |   |   |   |           |           |       `-- injection_task_8.json
|   |   |   |   |           |           |-- user_task_24/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_0.json
|   |   |   |   |           |           |       `-- injection_task_12.json
|   |   |   |   |           |           |-- user_task_25/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_11.json
|   |   |   |   |           |           |       `-- injection_task_4.json
|   |   |   |   |           |           |-- user_task_26/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_0.json
|   |   |   |   |           |           |       `-- injection_task_5.json
|   |   |   |   |           |           |-- user_task_27/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_10.json
|   |   |   |   |           |           |       |-- injection_task_3.json
|   |   |   |   |           |           |       |-- injection_task_4.json
|   |   |   |   |           |           |       |-- injection_task_5.json
|   |   |   |   |           |           |       |-- injection_task_7.json
|   |   |   |   |           |           |       `-- injection_task_8.json
|   |   |   |   |           |           |-- user_task_28/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_1.json
|   |   |   |   |           |           |       `-- injection_task_4.json
|   |   |   |   |           |           |-- user_task_3/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_2.json
|   |   |   |   |           |           |       `-- injection_task_4.json
|   |   |   |   |           |           |-- user_task_30/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_0.json
|   |   |   |   |           |           |       |-- injection_task_10.json
|   |   |   |   |           |           |       `-- injection_task_1.json
|   |   |   |   |           |           |-- user_task_31/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_12.json
|   |   |   |   |           |           |       `-- injection_task_8.json
|   |   |   |   |           |           |-- user_task_32/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_13.json
|   |   |   |   |           |           |       `-- injection_task_2.json
|   |   |   |   |           |           |-- user_task_33/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_12.json
|   |   |   |   |           |           |       `-- injection_task_9.json
|   |   |   |   |           |           |-- user_task_34/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_13.json
|   |   |   |   |           |           |       `-- injection_task_2.json
|   |   |   |   |           |           |-- user_task_35/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_11.json
|   |   |   |   |           |           |       |-- injection_task_2.json
|   |   |   |   |           |           |       `-- injection_task_6.json
|   |   |   |   |           |           |-- user_task_36/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_13.json
|   |   |   |   |           |           |       |-- injection_task_1.json
|   |   |   |   |           |           |       |-- injection_task_7.json
|   |   |   |   |           |           |       `-- injection_task_8.json
|   |   |   |   |           |           |-- user_task_37/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_1.json
|   |   |   |   |           |           |       `-- injection_task_3.json
|   |   |   |   |           |           |-- user_task_38/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       `-- injection_task_9.json
|   |   |   |   |           |           |-- user_task_39/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_0.json
|   |   |   |   |           |           |       |-- injection_task_12.json
|   |   |   |   |           |           |       |-- injection_task_3.json
|   |   |   |   |           |           |       `-- injection_task_5.json
|   |   |   |   |           |           |-- user_task_4/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       `-- injection_task_3.json
|   |   |   |   |           |           |-- user_task_5/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_11.json
|   |   |   |   |           |           |       |-- injection_task_1.json
|   |   |   |   |           |           |       `-- injection_task_9.json
|   |   |   |   |           |           |-- user_task_6/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_10.json
|   |   |   |   |           |           |       |-- injection_task_11.json
|   |   |   |   |           |           |       |-- injection_task_1.json
|   |   |   |   |           |           |       `-- injection_task_3.json
|   |   |   |   |           |           |-- user_task_7/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_10.json
|   |   |   |   |           |           |       |-- injection_task_11.json
|   |   |   |   |           |           |       |-- injection_task_5.json
|   |   |   |   |           |           |       `-- injection_task_9.json
|   |   |   |   |           |           |-- user_task_8/
|   |   |   |   |           |           |   `-- important_instructions/
|   |   |   |   |           |           |       |-- injection_task_10.json
|   |   |   |   |           |           |       |-- injection_task_1.json
|   |   |   |   |           |           |       |-- injection_task_5.json
|   |   |   |   |           |           |       `-- injection_task_6.json
|   |   |   |   |           |           `-- user_task_9/
|   |   |   |   |           |               `-- important_instructions/
|   |   |   |   |           |                   |-- injection_task_0.json
|   |   |   |   |           |                   |-- injection_task_2.json
|   |   |   |   |           |                   `-- injection_task_5.json
|   |   |   |   |           `-- A15B0_ARMC_SCI_TOOL_KNOWLEDGE_200/
|   |   |   |   |               `-- gpt-4o-mini-piarena-agentwatcher/
|   |   |   |   |                   |-- banking/
|   |   |   |   |                   |   |-- injection_task_0/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_1/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_2/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_3/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_4/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_5/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_6/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_7/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_8/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- user_task_0/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_1.json
|   |   |   |   |                   |   |       `-- injection_task_4.json
|   |   |   |   |                   |   |-- user_task_1/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   |-- user_task_10/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_1.json
|   |   |   |   |                   |   |       `-- injection_task_4.json
|   |   |   |   |                   |   |-- user_task_11/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   |-- user_task_13/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_7.json
|   |   |   |   |                   |   |       `-- injection_task_8.json
|   |   |   |   |                   |   |-- user_task_14/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_0.json
|   |   |   |   |                   |   |       |-- injection_task_2.json
|   |   |   |   |                   |   |       |-- injection_task_5.json
|   |   |   |   |                   |   |       `-- injection_task_8.json
|   |   |   |   |                   |   |-- user_task_2/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_0.json
|   |   |   |   |                   |   |       `-- injection_task_3.json
|   |   |   |   |                   |   |-- user_task_3/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_6.json
|   |   |   |   |                   |   |       `-- injection_task_8.json
|   |   |   |   |                   |   |-- user_task_4/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_0.json
|   |   |   |   |                   |   |       |-- injection_task_2.json
|   |   |   |   |                   |   |       `-- injection_task_3.json
|   |   |   |   |                   |   |-- user_task_5/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_1.json
|   |   |   |   |                   |   |       `-- injection_task_2.json
|   |   |   |   |                   |   |-- user_task_6/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_0.json
|   |   |   |   |                   |   |       |-- injection_task_4.json
|   |   |   |   |                   |   |       |-- injection_task_5.json
|   |   |   |   |                   |   |       `-- injection_task_8.json
|   |   |   |   |                   |   |-- user_task_7/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_1.json
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   |-- user_task_8/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_1.json
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   `-- user_task_9/
|   |   |   |   |                   |       `-- tool_knowledge/
|   |   |   |   |                   |           |-- injection_task_0.json
|   |   |   |   |                   |           |-- injection_task_3.json
|   |   |   |   |                   |           `-- injection_task_5.json
|   |   |   |   |                   |-- slack/
|   |   |   |   |                   |   |-- injection_task_1/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_2/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_3/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_4/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_5/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- user_task_1/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_1.json
|   |   |   |   |                   |   |       `-- injection_task_4.json
|   |   |   |   |                   |   |-- user_task_10/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_3.json
|   |   |   |   |                   |   |-- user_task_11/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   |-- user_task_12/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_1.json
|   |   |   |   |                   |   |       |-- injection_task_2.json
|   |   |   |   |                   |   |       `-- injection_task_4.json
|   |   |   |   |                   |   |-- user_task_13/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   |-- user_task_15/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_1.json
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   |-- user_task_16/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_4.json
|   |   |   |   |                   |   |-- user_task_17/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_3.json
|   |   |   |   |                   |   |       `-- injection_task_4.json
|   |   |   |   |                   |   |-- user_task_18/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_2.json
|   |   |   |   |                   |   |       `-- injection_task_3.json
|   |   |   |   |                   |   |-- user_task_19/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_1.json
|   |   |   |   |                   |   |       |-- injection_task_2.json
|   |   |   |   |                   |   |       |-- injection_task_3.json
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   |-- user_task_2/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_1.json
|   |   |   |   |                   |   |-- user_task_20/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_4.json
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   |-- user_task_3/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_2.json
|   |   |   |   |                   |   |       `-- injection_task_3.json
|   |   |   |   |                   |   |-- user_task_4/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_4.json
|   |   |   |   |                   |   |-- user_task_6/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_3.json
|   |   |   |   |                   |   |-- user_task_7/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_2.json
|   |   |   |   |                   |   |-- user_task_8/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_2.json
|   |   |   |   |                   |   `-- user_task_9/
|   |   |   |   |                   |       `-- tool_knowledge/
|   |   |   |   |                   |           `-- injection_task_2.json
|   |   |   |   |                   |-- travel/
|   |   |   |   |                   |   |-- injection_task_0/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_1/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_2/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_3/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_4/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_5/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- injection_task_6/
|   |   |   |   |                   |   |   `-- none/
|   |   |   |   |                   |   |       `-- none.json
|   |   |   |   |                   |   |-- user_task_0/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_4.json
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   |-- user_task_1/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_2.json
|   |   |   |   |                   |   |-- user_task_10/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_2.json
|   |   |   |   |                   |   |-- user_task_11/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_2.json
|   |   |   |   |                   |   |       |-- injection_task_4.json
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   |-- user_task_12/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   |-- user_task_13/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_2.json
|   |   |   |   |                   |   |       |-- injection_task_3.json
|   |   |   |   |                   |   |       `-- injection_task_4.json
|   |   |   |   |                   |   |-- user_task_14/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_4.json
|   |   |   |   |                   |   |       `-- injection_task_6.json
|   |   |   |   |                   |   |-- user_task_15/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_5.json
|   |   |   |   |                   |   |       `-- injection_task_6.json
|   |   |   |   |                   |   |-- user_task_16/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_4.json
|   |   |   |   |                   |   |-- user_task_18/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_5.json
|   |   |   |   |                   |   |       `-- injection_task_6.json
|   |   |   |   |                   |   |-- user_task_19/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_2.json
|   |   |   |   |                   |   |       |-- injection_task_4.json
|   |   |   |   |                   |   |       `-- injection_task_5.json
|   |   |   |   |                   |   |-- user_task_2/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_5.json
|   |   |   |   |                   |   |       `-- injection_task_6.json
|   |   |   |   |                   |   |-- user_task_4/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_2.json
|   |   |   |   |                   |   |-- user_task_5/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_1.json
|   |   |   |   |                   |   |       `-- injection_task_2.json
|   |   |   |   |                   |   |-- user_task_6/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_0.json
|   |   |   |   |                   |   |       `-- injection_task_1.json
|   |   |   |   |                   |   |-- user_task_7/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       `-- injection_task_0.json
|   |   |   |   |                   |   |-- user_task_8/
|   |   |   |   |                   |   |   `-- tool_knowledge/
|   |   |   |   |                   |   |       |-- injection_task_1.json
|   |   |   |   |                   |   |       `-- injection_task_6.json
|   |   |   |   |                   |   `-- user_task_9/
|   |   |   |   |                   |       `-- tool_knowledge/
|   |   |   |   |                   |           `-- injection_task_6.json
|   |   |   |   |                   `-- workspace/
|   |   |   |   |                       |-- injection_task_0/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_1/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_10/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_11/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_12/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_13/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_2/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_3/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_4/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_5/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_6/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_7/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_8/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- injection_task_9/
|   |   |   |   |                       |   `-- none/
|   |   |   |   |                       |       `-- none.json
|   |   |   |   |                       |-- user_task_0/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_11.json
|   |   |   |   |                       |       |-- injection_task_3.json
|   |   |   |   |                       |       `-- injection_task_6.json
|   |   |   |   |                       |-- user_task_1/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_11.json
|   |   |   |   |                       |       `-- injection_task_13.json
|   |   |   |   |                       |-- user_task_10/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       `-- injection_task_1.json
|   |   |   |   |                       |-- user_task_11/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_1.json
|   |   |   |   |                       |       |-- injection_task_2.json
|   |   |   |   |                       |       `-- injection_task_6.json
|   |   |   |   |                       |-- user_task_12/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_12.json
|   |   |   |   |                       |       |-- injection_task_13.json
|   |   |   |   |                       |       |-- injection_task_2.json
|   |   |   |   |                       |       |-- injection_task_5.json
|   |   |   |   |                       |       |-- injection_task_7.json
|   |   |   |   |                       |       `-- injection_task_9.json
|   |   |   |   |                       |-- user_task_13/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       `-- injection_task_11.json
|   |   |   |   |                       |-- user_task_14/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       `-- injection_task_0.json
|   |   |   |   |                       |-- user_task_15/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_3.json
|   |   |   |   |                       |       |-- injection_task_6.json
|   |   |   |   |                       |       `-- injection_task_9.json
|   |   |   |   |                       |-- user_task_16/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_0.json
|   |   |   |   |                       |       `-- injection_task_7.json
|   |   |   |   |                       |-- user_task_17/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_10.json
|   |   |   |   |                       |       |-- injection_task_13.json
|   |   |   |   |                       |       |-- injection_task_4.json
|   |   |   |   |                       |       |-- injection_task_6.json
|   |   |   |   |                       |       `-- injection_task_7.json
|   |   |   |   |                       |-- user_task_18/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_10.json
|   |   |   |   |                       |       |-- injection_task_11.json
|   |   |   |   |                       |       |-- injection_task_12.json
|   |   |   |   |                       |       |-- injection_task_1.json
|   |   |   |   |                       |       `-- injection_task_9.json
|   |   |   |   |                       |-- user_task_2/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_2.json
|   |   |   |   |                       |       |-- injection_task_4.json
|   |   |   |   |                       |       `-- injection_task_6.json
|   |   |   |   |                       |-- user_task_20/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_2.json
|   |   |   |   |                       |       `-- injection_task_4.json
|   |   |   |   |                       |-- user_task_21/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       `-- injection_task_7.json
|   |   |   |   |                       |-- user_task_22/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_0.json
|   |   |   |   |                       |       |-- injection_task_10.json
|   |   |   |   |                       |       |-- injection_task_1.json
|   |   |   |   |                       |       |-- injection_task_4.json
|   |   |   |   |                       |       `-- injection_task_9.json
|   |   |   |   |                       |-- user_task_23/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_11.json
|   |   |   |   |                       |       |-- injection_task_2.json
|   |   |   |   |                       |       |-- injection_task_7.json
|   |   |   |   |                       |       `-- injection_task_8.json
|   |   |   |   |                       |-- user_task_24/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_0.json
|   |   |   |   |                       |       `-- injection_task_12.json
|   |   |   |   |                       |-- user_task_25/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_11.json
|   |   |   |   |                       |       `-- injection_task_4.json
|   |   |   |   |                       |-- user_task_26/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_0.json
|   |   |   |   |                       |       `-- injection_task_5.json
|   |   |   |   |                       |-- user_task_27/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_10.json
|   |   |   |   |                       |       |-- injection_task_3.json
|   |   |   |   |                       |       |-- injection_task_4.json
|   |   |   |   |                       |       |-- injection_task_5.json
|   |   |   |   |                       |       |-- injection_task_7.json
|   |   |   |   |                       |       `-- injection_task_8.json
|   |   |   |   |                       |-- user_task_28/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_1.json
|   |   |   |   |                       |       `-- injection_task_4.json
|   |   |   |   |                       |-- user_task_3/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_2.json
|   |   |   |   |                       |       `-- injection_task_4.json
|   |   |   |   |                       |-- user_task_30/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_0.json
|   |   |   |   |                       |       |-- injection_task_10.json
|   |   |   |   |                       |       `-- injection_task_1.json
|   |   |   |   |                       |-- user_task_31/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_12.json
|   |   |   |   |                       |       `-- injection_task_8.json
|   |   |   |   |                       |-- user_task_32/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_13.json
|   |   |   |   |                       |       `-- injection_task_2.json
|   |   |   |   |                       |-- user_task_33/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_12.json
|   |   |   |   |                       |       `-- injection_task_9.json
|   |   |   |   |                       |-- user_task_34/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_13.json
|   |   |   |   |                       |       `-- injection_task_2.json
|   |   |   |   |                       |-- user_task_35/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_11.json
|   |   |   |   |                       |       |-- injection_task_2.json
|   |   |   |   |                       |       `-- injection_task_6.json
|   |   |   |   |                       |-- user_task_36/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_13.json
|   |   |   |   |                       |       |-- injection_task_1.json
|   |   |   |   |                       |       |-- injection_task_7.json
|   |   |   |   |                       |       `-- injection_task_8.json
|   |   |   |   |                       |-- user_task_37/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_1.json
|   |   |   |   |                       |       `-- injection_task_3.json
|   |   |   |   |                       |-- user_task_38/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       `-- injection_task_9.json
|   |   |   |   |                       |-- user_task_39/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_0.json
|   |   |   |   |                       |       |-- injection_task_12.json
|   |   |   |   |                       |       |-- injection_task_3.json
|   |   |   |   |                       |       `-- injection_task_5.json
|   |   |   |   |                       |-- user_task_4/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       `-- injection_task_3.json
|   |   |   |   |                       |-- user_task_5/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_11.json
|   |   |   |   |                       |       |-- injection_task_1.json
|   |   |   |   |                       |       `-- injection_task_9.json
|   |   |   |   |                       |-- user_task_6/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_10.json
|   |   |   |   |                       |       |-- injection_task_11.json
|   |   |   |   |                       |       |-- injection_task_1.json
|   |   |   |   |                       |       `-- injection_task_3.json
|   |   |   |   |                       |-- user_task_7/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_10.json
|   |   |   |   |                       |       |-- injection_task_11.json
|   |   |   |   |                       |       |-- injection_task_5.json
|   |   |   |   |                       |       `-- injection_task_9.json
|   |   |   |   |                       |-- user_task_8/
|   |   |   |   |                       |   `-- tool_knowledge/
|   |   |   |   |                       |       |-- injection_task_10.json
|   |   |   |   |                       |       |-- injection_task_1.json
|   |   |   |   |                       |       |-- injection_task_5.json
|   |   |   |   |                       |       `-- injection_task_6.json
|   |   |   |   |                       `-- user_task_9/
|   |   |   |   |                           `-- tool_knowledge/
|   |   |   |   |                               |-- injection_task_0.json
|   |   |   |   |                               |-- injection_task_2.json
|   |   |   |   |                               `-- injection_task_5.json
|   |   |   |   |-- scripts/
|   |   |   |   |   |-- main_agentdojo.sh
|   |   |   |   |   |-- main_agentdyn.sh
|   |   |   |   |   |-- main_injecagent.sh
|   |   |   |   |   |-- main.sh
|   |   |   |   |   |-- run_agentdojo.py
|   |   |   |   |   |-- run_agentdyn.sh
|   |   |   |   |   |-- run_injecagent.py
|   |   |   |   |   `-- run_long_context.py
|   |   |   |   `-- src/
|   |   |   |       |-- attacks/
|   |   |   |       |   |-- attack_heuristic.py
|   |   |   |       |   |-- attack_none.py
|   |   |   |       |   `-- __init__.py
|   |   |   |       |-- defenses/
|   |   |   |       |   |-- agentwatcher/
|   |   |   |       |   |   |-- attention_utils.py
|   |   |   |       |   |   |-- defense_agentwatcher.py
|   |   |   |       |   |   |-- __init__.py
|   |   |   |       |   |   `-- utils.py
|   |   |   |       |   |-- datasentinel/
|   |   |   |       |   |   |-- defense_datasentinel.py
|   |   |   |       |   |   |-- __init__.py
|   |   |   |       |   |   `-- OpenPromptInjection/
|   |   |   |       |   |       |-- apps/
|   |   |   |       |   |       |   |-- Application.py
|   |   |   |       |   |       |   |-- bpe.py
|   |   |   |       |   |       |   |-- DataSentinelDetector.py
|   |   |   |       |   |       |   |-- __init__.py
|   |   |   |       |   |       |   |-- PromptLocate.py
|   |   |   |       |   |       |   `-- utils.py
|   |   |   |       |   |       |-- attackers/
|   |   |   |       |   |       |   |-- Attacker.py
|   |   |   |       |   |       |   |-- CombineAttacker.py
|   |   |   |       |   |       |   |-- EscapeCharAttacker.py
|   |   |   |       |   |       |   |-- FakeCompAttacker.py
|   |   |   |       |   |       |   |-- IgnoreAttacker.py
|   |   |   |       |   |       |   |-- __init__.py
|   |   |   |       |   |       |   `-- NaiveAttacker.py
|   |   |   |       |   |       |-- evaluator/
|   |   |   |       |   |       |   |-- Evaluator.py
|   |   |   |       |   |       |   |-- gleu_utils.py
|   |   |   |       |   |       |   |-- __init__.py
|   |   |   |       |   |       |   `-- utils.py
|   |   |   |       |   |       |-- __init__.py
|   |   |   |       |   |       |-- models/
|   |   |   |       |   |       |   |-- DeepSeek.py
|   |   |   |       |   |       |   |-- Flan.py
|   |   |   |       |   |       |   |-- GPT.py
|   |   |   |       |   |       |   |-- __init__.py
|   |   |   |       |   |       |   |-- Internlm.py
|   |   |   |       |   |       |   |-- Llama3.py
|   |   |   |       |   |       |   |-- Llama.py
|   |   |   |       |   |       |   |-- Model.py
|   |   |   |       |   |       |   |-- PaLM2.py
|   |   |   |       |   |       |   |-- QLoraModel.py
|   |   |   |       |   |       |   `-- Vicuna.py
|   |   |   |       |   |       |-- tasks/
|   |   |   |       |   |       |   |-- CompromiseTask.py
|   |   |   |       |   |       |   |-- gigaword.py
|   |   |   |       |   |       |   |-- gleu.py
|   |   |   |       |   |       |   |-- hsol.py
|   |   |   |       |   |       |   |-- __init__.py
|   |   |   |       |   |       |   |-- InjectedTask.py
|   |   |   |       |   |       |   |-- jfleg.py
|   |   |   |       |   |       |   |-- Math500.py
|   |   |   |       |   |       |   |-- ReasoningTask.py
|   |   |   |       |   |       |   |-- sms_spam.py
|   |   |   |       |   |       |   |-- sst2.py
|   |   |   |       |   |       |   |-- TargetTask.py
|   |   |   |       |   |       |   |-- Task.py
|   |   |   |       |   |       |   `-- utils.py
|   |   |   |       |   |       `-- utils/
|   |   |   |       |   |           |-- __init__.py
|   |   |   |       |   |           |-- process_config.py
|   |   |   |       |   |           `-- process_txt.py
|   |   |   |       |   |-- defense_none.py
|   |   |   |       |   |-- gptsafeguard/
|   |   |   |       |   |   |-- defense_gptsafeguard.py
|   |   |   |       |   |   `-- __init__.py
|   |   |   |       |   |-- __init__.py
|   |   |   |       |   |-- __init__.py.UPSTREAM_F6CE2C8
|   |   |   |       |   |-- monitor_llm_module/
|   |   |   |       |   |   |-- core.py
|   |   |   |       |   |   |-- __init__.py
|   |   |   |       |   |   `-- messages.py
|   |   |   |       |   |-- piguard/
|   |   |   |       |   |   |-- defense_piguard.py
|   |   |   |       |   |   `-- __init__.py
|   |   |   |       |   |-- promptarmor/
|   |   |   |       |   |   |-- defense_promptarmor.py
|   |   |   |       |   |   `-- __init__.py
|   |   |   |       |   `-- promptguard/
|   |   |   |       |       |-- defense_promptguard.py
|   |   |   |       |       `-- __init__.py
|   |   |   |       |-- evaluations/
|   |   |   |       |   |-- __init__.py
|   |   |   |       |   |-- llm_judge.py
|   |   |   |       |   |-- longbench_metrics.py
|   |   |   |       |   `-- open_prompt_injection_metrics.py
|   |   |   |       |-- __init__.py
|   |   |   |       |-- llm.py
|   |   |   |       |-- llm_vllm.py
|   |   |   |       `-- utils.py
|   |   |   `-- attriguard_zenodo_v1/
|   |   |       |-- usenix-artifacts/
|   |   |       |   |-- adaptive_attack/
|   |   |       |   |   |-- environment.yaml
|   |   |       |   |   |-- openevolve_for_agentdojo/
|   |   |       |   |   |   |-- agentdojo_evaluator.py
|   |   |       |   |   |   |-- attack.py
|   |   |       |   |   |   |-- attriguard_openevolve_patch.py
|   |   |       |   |   |   |-- AttriGuard.py
|   |   |       |   |   |   |-- combine_attack.py
|   |   |       |   |   |   |-- config_example.yaml
|   |   |       |   |   |   |-- config.yaml
|   |   |       |   |   |   |-- .env.example
|   |   |       |   |   |   |-- get_reaction_from_agentdojo_log.py
|   |   |       |   |   |   |-- kill.sh
|   |   |       |   |   |   |-- main_attack.py
|   |   |       |   |   |   |-- mutator_prompt/
|   |   |       |   |   |   |   |-- descriptionforattriguard.txt
|   |   |       |   |   |   |   |-- full_rewrite_user.txt
|   |   |       |   |   |   |   `-- unified_systemprompt.txt
|   |   |       |   |   |   |-- my_agent_pipeline.py
|   |   |       |   |   |   |-- my_benchmark.py
|   |   |       |   |   |   |-- openevolve_runner.py
|   |   |       |   |   |   |-- pydantic_fix.py
|   |   |       |   |   |   |-- run.sh
|   |   |       |   |   |   |-- runtime_patches.py
|   |   |       |   |   |   |-- scorer_llm.py
|   |   |       |   |   |   |-- scorer_prompt/
|   |   |       |   |   |   |   |-- attriguard.txt
|   |   |       |   |   |   |   `-- user_attriguard.txt
|   |   |       |   |   |   `-- seed_attriguard.txt
|   |   |       |   |   `-- README.md
|   |   |       |   `-- main/
|   |   |       |       |-- asb_attriguard/
|   |   |       |       |   |-- environment.yml
|   |   |       |       |   |-- overlay/
|   |   |       |       |   |   `-- pyopenagi/
|   |   |       |       |   |       |-- agents/
|   |   |       |       |   |       |   `-- react_agent_attack.py
|   |   |       |       |   |       |-- defenses/
|   |   |       |       |   |       |   |-- attriguard.py
|   |   |       |       |   |       |   `-- __init__.py
|   |   |       |       |   |       `-- tools/
|   |   |       |       |   |           `-- simulated_tool.py
|   |   |       |       |   |-- README.md
|   |   |       |       |   `-- setup_asb_attriguard.sh
|   |   |       |       |-- environment.yml
|   |   |       |       |-- pipeline/
|   |   |       |       |   |-- AttriGuard.py
|   |   |       |       |   |-- combine_attack.py
|   |   |       |       |   |-- .env.example
|   |   |       |       |   |-- local_llm_compat.py
|   |   |       |       |   |-- my_agent_pipeline.py
|   |   |       |       |   |-- my_benchmark.py
|   |   |       |       |   |-- openai_llm_compat.py
|   |   |       |       |   |-- pydantic_fix.py
|   |   |       |       |   |-- run.sh
|   |   |       |       |   `-- runtime_patches.py
|   |   |       |       `-- README.md
|   |   |       `-- usenix-artifacts.zip
|   |   `-- README.md
|   |-- VERIFY_HASHES.sh
|   |-- VERIFY_RESULTS_ONLY.sh
|   `-- VERIFY.sh
|-- research_records/
|   |-- decisions.jsonl
|   `-- README.md
|-- results/
|-- RUN_FIRST.sh*
|-- RUN_MODELS.sh*
|-- RUN_NATIVE_RELEASE_GPU3.sh*
|-- RUN_PARALLEL_REFERENCE_GPU23.sh
|-- RUN_RECONCILED_GPU3.sh*
|-- RUN_S1_REFERENCE_GPU3.sh
|-- S1_FROZEN_MANIFEST.json
|-- S1_PACKAGE_MANIFEST.json
|-- s1_reference_study/
|   |-- AGENTS.md
|   |-- bootstrap.py
|   |-- common.py
|   |-- experiment.py
|   |-- __init__.py
|   |-- native.py
|   |-- origin_data/
|   |   |-- ARCHIVE_SHA256SUMS
|   |   |-- S1_C1_OFF/
|   |   |   |-- diagnostic.log
|   |   |   |-- driver_records.json
|   |   |   |-- effective_driver_profile.json
|   |   |   |-- events.jsonl
|   |   |   |-- executed_guard.py
|   |   |   |-- final_reporting.json
|   |   |   |-- final_world.json
|   |   |   |-- http/
|   |   |   |   |-- 0001.request.json
|   |   |   |   |-- 0001.response.json
|   |   |   |   |-- 0002.request.json
|   |   |   |   |-- 0002.response.json
|   |   |   |   |-- 0003.request.json
|   |   |   |   `-- 0003.response.json
|   |   |   |-- initial_world.json
|   |   |   |-- instrumentation.diff
|   |   |   |-- item.json
|   |   |   |-- messages.json
|   |   |   |-- native.log
|   |   |   |-- requests/
|   |   |   |   |-- 0000_actor.driver_request.json
|   |   |   |   |-- 0000_actor.response.json
|   |   |   |   |-- 0001_actor.driver_request.json
|   |   |   |   |-- 0001_actor.response.json
|   |   |   |   |-- 0002_actor.driver_request.json
|   |   |   |   `-- 0002_actor.response.json
|   |   |   |-- result.json
|   |   |   `-- tokenization/
|   |   |       |-- 0001.json
|   |   |       |-- 0002.json
|   |   |       `-- 0003.json
|   |   `-- SOURCE_ARCHIVE.json
|   |-- origin.py
|   |-- protocol.py
|   |-- __pycache__/
|   |   |-- bootstrap.cpython-312.pyc
|   |   |-- common.cpython-312.pyc
|   |   |-- experiment.cpython-312.pyc
|   |   |-- __init__.cpython-312.pyc
|   |   |-- native.cpython-312.pyc
|   |   |-- origin.cpython-312.pyc
|   |   |-- protocol.cpython-312.pyc
|   |   |-- qualification.cpython-312.pyc
|   |   |-- report.cpython-312.pyc
|   |   |-- sequence.cpython-312.pyc
|   |   |-- serving.cpython-312.pyc
|   |   |-- source.cpython-312.pyc
|   |   `-- transport.cpython-312.pyc
|   |-- qualification.py
|   |-- report.py
|   |-- RUNTIME_HASHES.json
|   |-- sequence.py
|   |-- serving.py
|   |-- source.py
|   |-- transport.py
|   `-- vendor/
|       |-- AttriGuard.py
|       |-- AUTHOR_RELEASE_README.md
|       |-- local_llm_compat.py
|       |-- my_agent_pipeline.py
|       |-- openai_llm_compat.py
|       |-- __pycache__/
|       |   |-- AttriGuard.cpython-312.pyc
|       |   |-- local_llm_compat.cpython-312.pyc
|       |   |-- my_agent_pipeline.cpython-312.pyc
|       |   `-- openai_llm_compat.cpython-312.pyc
|       `-- SOURCE_IDENTITY.json
|-- SCIENTIFIC_PROTOCOL.md
|-- scripts/
|   |-- background_job.sh*
|   |-- figures_job.sh*
|   |-- historical_audit.py
|   |-- historical_job.sh*
|   |-- project_components.sh*
|   |-- protocols_job.sh
|   |-- __pycache__/
|   |   |-- historical_audit.cpython-312.pyc
|   |   `-- qualify_gpu.cpython-312.pyc
|   |-- qualify_gpu.py
|   |-- run_native.py
|   |-- validate_protocols.py
|   `-- verify_project.py
|-- SETUP_AUTHORIZATION.sh*
|-- SETUP_COMPLETE_VENV.sh
|-- SETUP_RECONCILED.sh*
|-- SETUP_SERVING.sh
|-- SETUP.sh*
|-- SOURCE_PROVENANCE.json
|-- SOURCE_PROVENANCE_PARALLEL_REFERENCE.json
|-- SOURCE_PROVENANCE_S1.json
|-- START_AUTHORIZATION_GPU3.sh*
|-- START_EXPANDED_GPU3.sh
|-- START_GPU3_SEQUENCE.sh
|-- START_HERE.md
|-- START_OCCURRENCE_GPU3_FRESH.sh
|-- START_OCCURRENCE_GPU3.sh*
|-- START_TARGETED_GPU3.sh*
|-- targeted_gpu3/
|   |-- analyze.py
|   |-- controls.py
|   |-- core.py
|   |-- experiment.py
|   |-- __init__.py
|   |-- __pycache__/
|   |   |-- controls.cpython-312.pyc
|   |   |-- core.cpython-312.pyc
|   |   |-- experiment.cpython-312.pyc
|   |   |-- __init__.cpython-312.pyc
|   |   `-- sequence.cpython-312.pyc
|   |-- RESEARCH_PLAN.md
|   |-- retained/
|   |   |-- expanded_gpu3/
|   |   |   |-- guards.py
|   |   |   |-- protocol.py
|   |   |   |-- __pycache__/
|   |   |   |   |-- guards.cpython-312.pyc
|   |   |   |   |-- protocol.cpython-312.pyc
|   |   |   |   |-- sequence.cpython-312.pyc
|   |   |   |   |-- transport.cpython-312.pyc
|   |   |   |   `-- world.cpython-312.pyc
|   |   |   |-- sequence.py
|   |   |   |-- transport.py
|   |   |   `-- world.py
|   |   |-- my_agent_pipeline.py
|   |   |-- __pycache__/
|   |   |   `-- qualify_gpu.cpython-312.pyc
|   |   |-- qualify_gpu.py
|   |   `-- review_binding/
|   |       |-- diagnostic.py
|   |       |-- __pycache__/
|   |       |   `-- diagnostic.cpython-312.pyc
|   |       `-- vendor/
|   |           `-- AttriGuard.py
|   |-- RETAINED_MANIFEST.json
|   |-- schedule.json
|   |-- sequence.py
|   |-- tests/
|   |   |-- __init__.py
|   |   `-- test_experiment.py
|   `-- validation/
|       |-- cpu_control_records.json
|       |-- engineering_tests.log
|       |-- README.md
|       `-- VALIDATION.json
|-- TARGETED_GPU3_README.md
|-- TARGETED_PACKAGE_SHA256SUMS
|-- tests/
|   |-- __pycache__/
|   |   |-- test_gpu_qualification.cpython-312.pyc
|   |   `-- test_historical_audit.cpython-312.pyc
|   |-- test_gpu_qualification.py
|   `-- test_historical_audit.py
|-- THIRD_PARTY_NOTICES.md
|-- THIRD_PARTY_NOTICES_S1.md
|-- validation/
|   |-- BUILD_VALIDATION.json
|   |-- BUILD_VALIDATION.md
|   |-- CHECKPOINT_BEFORE_QUALIFICATION.json
|   |-- consolidated/
|   |   |-- component_run/
|   |   |   |-- native/
|   |   |   |   |-- B_duplicate_one_reference__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_one_reference__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_one_reference__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_one_reference__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_one_reference__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_one_reference__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_two_references_one_grant__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_two_references_one_grant__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_two_references_one_grant__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_two_references_one_grant__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_two_references_one_grant__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_two_references_one_grant__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_with_independent_gate__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_with_independent_gate__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_with_independent_gate__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_with_independent_gate__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_with_independent_gate__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_with_independent_gate__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_idempotent_retry__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_idempotent_retry__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_idempotent_retry__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_idempotent_retry__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_idempotent_retry__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_idempotent_retry__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_one_legal__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_one_legal__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_one_legal__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_one_legal__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_one_legal__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_one_legal__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_two_legal_two_references__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_two_legal_two_references__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_two_legal_two_references__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_two_legal_two_references__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_two_legal_two_references__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_two_legal_two_references__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_wrong_recipient__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_wrong_recipient__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_wrong_recipient__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_wrong_recipient__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_wrong_recipient__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_wrong_recipient__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- checks.json
|   |   |   |   |-- environment.json
|   |   |   |   |-- generated/
|   |   |   |   |   |-- b_occurrence.diff
|   |   |   |   |   |-- guard_b_occurrence.py
|   |   |   |   |   |-- guard_original.py
|   |   |   |   |   |-- guard_placebo.py
|   |   |   |   |   |-- guard_r_all_errors.py
|   |   |   |   |   |-- guard_r_minimal.py
|   |   |   |   |   |-- original.diff
|   |   |   |   |   |-- placebo.diff
|   |   |   |   |   |-- r_all_errors.diff
|   |   |   |   |   `-- r_minimal.diff
|   |   |   |   |-- R_blocked_skip_disabled__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- results.csv
|   |   |   |   |-- results.json
|   |   |   |   |-- R_prior_allowed_empty__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   `-- runtime_sources.json
|   |   |   |-- native_components.log
|   |   |   |-- native_tests.log
|   |   |   |-- project_tests.log
|   |   |   `-- receipt.json
|   |   |-- consolidated_components_01.log
|   |   |-- consolidated_components_01.status
|   |   |-- consolidated_protocols_01.log
|   |   |-- consolidated_protocols_01.status
|   |   `-- README.md
|   |-- CPU_PROFILE_QUALIFICATION.json
|   |-- CPU_QUALIFICATION.json
|   |-- CPU_STATUS.json
|   |-- CPU_TESTS.log
|   |-- CPU_VALIDATION_PACKAGES.txt
|   |-- engineering_history/
|   |   `-- initial_matching_test_fixture_failure.log
|   |-- FRESH_EXTRACTION_VALIDATION.json
|   |-- full_foundation/
|   |   |-- CHECKS.json
|   |   |-- component_run/
|   |   |   |-- native/
|   |   |   |   |-- B_duplicate_one_reference__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_one_reference__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_one_reference__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_one_reference__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_one_reference__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_one_reference__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_two_references_one_grant__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_two_references_one_grant__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_two_references_one_grant__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_two_references_one_grant__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_two_references_one_grant__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_two_references_one_grant__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_with_independent_gate__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_with_independent_gate__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_with_independent_gate__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_with_independent_gate__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_with_independent_gate__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_duplicate_with_independent_gate__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_idempotent_retry__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_idempotent_retry__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_idempotent_retry__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_idempotent_retry__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_idempotent_retry__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_idempotent_retry__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_one_legal__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_one_legal__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_one_legal__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_one_legal__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_one_legal__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_one_legal__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_two_legal_two_references__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_two_legal_two_references__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_two_legal_two_references__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_two_legal_two_references__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_two_legal_two_references__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_two_legal_two_references__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_wrong_recipient__b_occurrence__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_wrong_recipient__b_occurrence__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_wrong_recipient__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_wrong_recipient__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_wrong_recipient__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- B_wrong_recipient__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- checks.json
|   |   |   |   |-- environment.json
|   |   |   |   |-- generated/
|   |   |   |   |   |-- b_occurrence.diff
|   |   |   |   |   |-- guard_b_occurrence.py
|   |   |   |   |   |-- guard_original.py
|   |   |   |   |   |-- guard_placebo.py
|   |   |   |   |   |-- guard_r_all_errors.py
|   |   |   |   |   |-- guard_r_minimal.py
|   |   |   |   |   |-- original.diff
|   |   |   |   |   |-- placebo.diff
|   |   |   |   |   |-- r_all_errors.diff
|   |   |   |   |   `-- r_minimal.diff
|   |   |   |   |-- R_blocked_skip_disabled__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_blocked_skip_disabled__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- results.csv
|   |   |   |   |-- results.json
|   |   |   |   |-- R_prior_allowed_empty__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_empty__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed_error__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_allowed__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_prior_blocked_with_independent_gate__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__original__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__original__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__placebo__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__placebo__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__r_all_errors__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__r_all_errors__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__r_minimal__exact/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   |-- R_skip_branch_error_chain__r_minimal__fuzzy/
|   |   |   |   |   |-- case.json
|   |   |   |   |   |-- events.jsonl
|   |   |   |   |   |-- messages.json
|   |   |   |   |   `-- result.json
|   |   |   |   `-- runtime_sources.json
|   |   |   |-- native_components.log
|   |   |   |-- native_tests.log
|   |   |   |-- project_tests.log
|   |   |   `-- receipt.json
|   |   |-- components.log
|   |   |-- components.status
|   |   |-- display_status.json
|   |   |-- figures.log
|   |   |-- figures.status
|   |   |-- frozen_figures/
|   |   |   |-- figure1.pdf
|   |   |   |-- figure2.pdf
|   |   |   |-- figure3.pdf
|   |   |   |-- figure4.pdf
|   |   |   |-- figure5.pdf
|   |   |   |-- figure6.pdf
|   |   |   `-- FIGURE_REGENERATION_REPORT.json
|   |   |-- historical.log
|   |   |-- historical_run/
|   |   |   |-- consumed_basis_files.json
|   |   |   |-- inherited_integrity.json
|   |   |   |-- legacy_frozen_checks/
|   |   |   |   |-- CLAIM_LEDGER.json
|   |   |   |   |-- CLAIM_TO_ARTIFACT.md
|   |   |   |   `-- SUMMARY.txt
|   |   |   |-- primitive_reanalysis.json
|   |   |   `-- status.json
|   |   |-- historical.status
|   |   |-- installed_packages.txt
|   |   |-- setup.log
|   |   `-- setup.status
|   |-- gemma_mock_E3_INPUT_EQUIVALENCE.json
|   |-- gemma_mock_profile_probes.json
|   |-- isolation_guard/
|   |   `-- sitecustomize.py
|   |-- LOCK_REFUSAL_TEST.json
|   |-- MISSINGNESS_TEST.json
|   |-- MOCK_PLANNED_VS_ACTUAL.csv
|   |-- MOCK_SUMMARY.json
|   |-- NATIVE_CPU_QUALIFICATION.json
|   |-- NATIVE_CPU_QUALIFICATION.log
|   |-- OPERATIONAL_TESTS.log
|   |-- qwen_mock_E3_INPUT_EQUIVALENCE.json
|   |-- qwen_mock_profile_probes.json
|   |-- qwen_template_fixtures/
|   |   |-- actor.json
|   |   |-- attenuator.json
|   |   |-- effective_template.jinja
|   |   |-- judge.json
|   |   |-- qualification.json
|   |   `-- reference_history.json
|   |-- README.md
|   |-- RETAINED_CPU_QUALIFICATION.json
|   |-- RETAINED_CPU_QUALIFICATION.log
|   |-- TRANSFORMERS_PREFLIGHT_VALIDATION.json
|   |-- TRANSFORMERS_PREFLIGHT_VALIDATION.log
|   |-- VALIDATION_REPORT.md
|   `-- VALIDATION_SCOPE.md
|-- VERIFY_NATIVE_RELEASE.sh*
|-- VERIFY_PARALLEL_REFERENCE.sh
|-- VERIFY_PROJECT.sh*
|-- VERIFY_RECONCILED_PACKAGE.py
|-- VERIFY_S1_REFERENCE.sh
|-- .vscode/
|   |-- settings.json
|   `-- tasks.json
`-- WORK_NEXT.md

5247 directories, 9463 files
```

## results/user_runs

Per-run output directories and archives. Shown two levels deep; each run directory holds hundreds to thousands of generated files.

```
results/user_runs
|-- authorization_gpu3_20261023T221414Z_2619402_23755/
|   |-- analysis/
|   |-- attempts.jsonl
|   |-- controller.log
|   |-- cpu_qualification/
|   |-- disk_initial.json
|   |-- FINDINGS.md
|   |-- frozen_protocol.json
|   |-- gemma/
|   |-- gpu_telemetry.csv
|   |-- IEEE_SP_Final_Experiment_Design.md
|   |-- IEEE_SP_Standalone_Research_Authority_Current.md
|   |-- qwen/
|   |-- README_AUTHORIZATION.md
|   |-- research_packages.txt
|   |-- serving_packages.txt
|   |-- SHA256SUMS
|   |-- source/
|   `-- status.json
|-- authorization_gpu3_20261023T221414Z_2619402_23755.tar.gz
|-- authorization_gpu3_20261023T221414Z_2619402_23755.tar.gz.sha256
|-- components_01/
|   |-- native/
|   |-- native_components.log
|   |-- native_tests.log
|   |-- project_tests.log
|   `-- receipt.json
|-- expanded_gpu3_20261020T224703Z_517128/
|   |-- assurance/
|   |-- assurance.log
|   |-- controller.log
|   |-- episodes.csv
|   |-- FINDINGS.md
|   |-- gemma/
|   |-- gpu_final.json
|   |-- gpu_initial.json
|   |-- gpu_telemetry.csv
|   |-- ninja_version.txt
|   |-- qwen/
|   |-- research_packages.txt
|   |-- schedule.json
|   |-- serving_packages.txt
|   |-- SHA256SUMS
|   |-- source/
|   |-- status.json
|   |-- summary.csv
|   `-- summary.json
|-- expanded_gpu3_20261020T224703Z_517128.tar.gz
|-- expanded_gpu3_20261020T224703Z_517128.tar.gz.sha256
|-- gpu3_sequence_20261020T040635Z_1989750/
|   |-- controller.log
|   |-- fatal_error.json
|   |-- FINDINGS.md
|   |-- gpu_final.json
|   |-- gpu_initial.json
|   |-- research_packages.txt
|   |-- serving_packages.txt
|   |-- SHA256SUMS
|   |-- source/
|   |-- status.json
|   |-- summary.csv
|   `-- summary.json
|-- gpu3_sequence_20261020T040635Z_1989750.tar.gz
|-- gpu3_sequence_20261020T040635Z_1989750.tar.gz.sha256
|-- gpu3_sequence_20261020T041603Z_2051143/
|   |-- controller.log
|   |-- emergency_shutdown.json
|   |-- fatal_error.json
|   |-- FINDINGS.md
|   |-- gpu_final.json
|   |-- gpu_initial.json
|   |-- gpu_telemetry.csv
|   |-- qwen/
|   |-- research_packages.txt
|   |-- schedule.json
|   |-- serving_packages.txt
|   |-- SHA256SUMS
|   |-- source/
|   |-- status.json
|   |-- summary.csv
|   `-- summary.json
|-- gpu3_sequence_20261020T041603Z_2051143.tar.gz
|-- gpu3_sequence_20261020T041603Z_2051143.tar.gz.sha256
|-- gpu3_sequence_20261020T042902Z_2146327/
|   |-- controller.log
|   |-- FINDINGS.md
|   |-- gemma/
|   |-- gpu_final.json
|   |-- gpu_initial.json
|   |-- gpu_telemetry.csv
|   |-- qwen/
|   |-- research_packages.txt
|   |-- schedule.json
|   |-- serving_packages.txt
|   |-- SHA256SUMS
|   |-- source/
|   |-- status.json
|   |-- summary.csv
|   `-- summary.json
|-- gpu3_sequence_20261020T042902Z_2146327.tar.gz
|-- gpu3_sequence_20261020T042902Z_2146327.tar.gz.sha256
|-- gpu3_sequence_20261020T043349Z_2177718/
|   `-- status.json
|-- historical_01/
|   |-- consumed_basis_files.json
|   |-- inherited_integrity.json
|   |-- legacy_frozen_checks/
|   |-- primitive_reanalysis.json
|   `-- status.json
|-- native_release_gpu3_20261025T005833Z_2622163_28698/
|   |-- analysis/
|   |-- autonomous/
|   |-- census.json
|   |-- conditional/
|   |-- controller.log
|   |-- cpu_qualification/
|   |-- execution_environment.json
|   |-- FROZEN_MANIFEST.json
|   |-- gpu_telemetry.csv
|   |-- input_equivalence/
|   |-- parent_selection/
|   |-- restoration_qualification/
|   |-- serving/
|   |-- SHA256SUMS
|   |-- snapshot_identity.json
|   |-- source/
|   |-- SOURCE_RUNTIME_IDENTITY.json
|   `-- status.json
|-- native_release_gpu3_20261025T005833Z_2622163_28698.tar.gz
|-- native_release_gpu3_20261025T005833Z_2622163_28698.tar.gz.sha256
|-- occurrence_fresh_gpu3_20261023T030845Z_3250532/
|   |-- analysis/
|   |-- attempts.jsonl
|   |-- controller.log
|   |-- cpu_qualification/
|   |-- episodes.csv
|   |-- episodes.json
|   |-- feedback_selection.json
|   |-- FINDINGS.md
|   |-- frozen_protocol.json
|   |-- gemma/
|   |-- gemma_breadth_decision.json
|   |-- gpu_final.json
|   |-- gpu_initial.json
|   |-- gpu_telemetry.csv
|   |-- ninja_version.txt
|   |-- qwen/
|   |-- qwen_breadth_decision.json
|   |-- research_packages.txt
|   |-- serving_packages.txt
|   |-- SHA256SUMS
|   |-- source/
|   |-- status.json
|   `-- unexecuted_schedule.json
|-- occurrence_fresh_gpu3_20261023T030845Z_3250532.tar.gz
|-- occurrence_fresh_gpu3_20261023T030845Z_3250532.tar.gz.sha256
|-- occurrence_gpu3_20261023T004740Z_2853755/
|   |-- analysis/
|   |-- attempts.jsonl
|   |-- controller.log
|   |-- cpu_qualification/
|   |-- episodes.csv
|   |-- episodes.json
|   |-- feedback_selection.json
|   |-- FINDINGS.md
|   |-- frozen_protocol.json
|   |-- gemma/
|   |-- gemma_breadth_decision.json
|   |-- gpu_final.json
|   |-- gpu_initial.json
|   |-- gpu_telemetry.csv
|   |-- ninja_version.txt
|   |-- qwen/
|   |-- qwen_breadth_decision.json
|   |-- research_packages.txt
|   |-- serving_packages.txt
|   |-- SHA256SUMS
|   |-- source/
|   |-- status.json
|   `-- unexecuted_schedule.json
|-- occurrence_gpu3_20261023T004740Z_2853755.tar.gz
|-- occurrence_gpu3_20261023T004740Z_2853755.tar.gz.sha256
|-- parallel_reference_gpu23_20261026T045504Z_3579822_22634/
|   |-- analysis/
|   |-- census.json
|   |-- controller.log
|   |-- cpu_qualification/
|   |-- fatal_error.json
|   |-- FROZEN_MANIFEST.json
|   |-- operational_tests.json
|   |-- operational_tests.log
|   |-- SHA256SUMS
|   |-- source/
|   |-- status_events.jsonl
|   `-- status.json
|-- parallel_reference_gpu23_20261026T045504Z_3579822_22634.packaging.json
|-- parallel_reference_gpu23_20261026T045504Z_3579822_22634.review.tar.gz
|-- parallel_reference_gpu23_20261026T045504Z_3579822_22634.tar.gz
|-- parallel_reference_gpu23_20261026T045504Z_3579822_22634.tar.gz.sha256
|-- parallel_reference_gpu23_20261026T130619Z_946797_7302/
|   |-- analysis/
|   |-- census.json
|   |-- controller.log
|   |-- cpu_qualification/
|   |-- fatal_error.json
|   |-- FROZEN_MANIFEST.json
|   |-- operational_tests.json
|   |-- operational_tests.log
|   |-- SHA256SUMS
|   |-- source/
|   |-- status_events.jsonl
|   `-- status.json
|-- parallel_reference_gpu23_20261026T130619Z_946797_7302.packaging.json
|-- parallel_reference_gpu23_20261026T130619Z_946797_7302.review.tar.gz
|-- parallel_reference_gpu23_20261026T130619Z_946797_7302.tar.gz
|-- parallel_reference_gpu23_20261026T130619Z_946797_7302.tar.gz.sha256
|-- parallel_reference_gpu23_20261026T131613Z_976131_28637/
|   |-- analysis/
|   |-- census.json
|   |-- controller.log
|   |-- cpu_qualification/
|   |-- fatal_error.json
|   |-- FROZEN_MANIFEST.json
|   |-- operational_tests.json
|   |-- operational_tests.log
|   |-- pid_namespace.json
|   |-- SHA256SUMS
|   |-- source/
|   |-- status_events.jsonl
|   |-- status.json
|   `-- template_qualification/
|-- parallel_reference_gpu23_20261026T131613Z_976131_28637.packaging.json
|-- parallel_reference_gpu23_20261026T131613Z_976131_28637.review.tar.gz
|-- parallel_reference_gpu23_20261026T131613Z_976131_28637.tar.gz
|-- parallel_reference_gpu23_20261026T131613Z_976131_28637.tar.gz.sha256
|-- parallel_reference_gpu23_20261026T133503Z_1032615_10605/
|   |-- census.json
|   |-- cpu_qualification/
|   |-- FROZEN_MANIFEST.json
|   |-- gpu2_audit/
|   |-- models/
|   |-- operational_tests.json
|   |-- operational_tests.log
|   |-- pid_namespace.json
|   |-- qwen_worker_command.json
|   |-- qwen_worker_process.json
|   |-- snapshot_preflight.json
|   |-- source/
|   |-- status_events.jsonl
|   |-- status.json
|   `-- template_qualification/
|-- reconciled_gpu3_20261024T044259Z_2440506_28345/
|   |-- analysis/
|   |-- controller.log
|   |-- cpu_qualification/
|   |-- docs/
|   |-- fresh_request_budget.json
|   |-- frozen_protocol.json
|   |-- gemma/
|   |-- gpu_telemetry.csv
|   |-- input_package_manifest.json
|   |-- ninja.json
|   |-- progress.jsonl
|   |-- qwen/
|   |-- research_environment.json
|   |-- serving_environment.json
|   |-- SHA256SUMS
|   |-- snapshot_preflight.json
|   |-- source/
|   `-- status.json
|-- reconciled_gpu3_20261024T044259Z_2440506_28345.tar.gz
|-- reconciled_gpu3_20261024T044259Z_2440506_28345.tar.gz.sha256
|-- s1_reference_gpu3_20261025T173651Z_1528393_1266/
|   |-- admission_ledger.json
|   |-- admissions/
|   |-- admissions.csv
|   |-- census.json
|   |-- conditions.csv
|   |-- CONTRASTS.json
|   |-- controller.log
|   |-- cpu_qualification/
|   |-- execution_environment.json
|   |-- FINDINGS.md
|   |-- FROZEN_MANIFEST.json
|   |-- gpu_telemetry.csv
|   |-- pid_namespace.json
|   |-- references/
|   |-- RESULTS_VERIFICATION.json
|   |-- serving/
|   |-- SHA256SUMS
|   |-- snapshot_identity.json
|   |-- source/
|   |-- status.json
|   `-- SUMMARY.json
|-- s1_reference_gpu3_20261025T173651Z_1528393_1266.tar.gz
|-- s1_reference_gpu3_20261025T173651Z_1528393_1266.tar.gz.sha256
|-- targeted_gpu3_20261021T055714Z_3261043/
|   |-- controller.log
|   |-- cpu_controls/
|   |-- episodes.csv
|   |-- episodes.json
|   |-- FINDINGS.md
|   |-- frozen_protocol.json
|   |-- gemma/
|   |-- gpu_final.json
|   |-- gpu_initial.json
|   |-- gpu_telemetry.csv
|   |-- ninja_version.txt
|   |-- qwen/
|   |-- reference_probes.csv
|   |-- reference_probes.json
|   |-- research_packages.txt
|   |-- serving_packages.txt
|   |-- SHA256SUMS
|   |-- source/
|   |-- status.json
|   |-- unrecorded_qualification_rows.json
|   `-- unrecorded_reference_rows.json
|-- targeted_gpu3_20261021T055714Z_3261043.tar.gz
|-- targeted_gpu3_20261021T055714Z_3261043.tar.gz.sha256
|-- targeted_gpu3_20261022T213519Z_2309383/
|   |-- controller.log
|   |-- cpu_controls/
|   |-- episodes.csv
|   |-- episodes.json
|   |-- FINDINGS.md
|   |-- frozen_protocol.json
|   |-- gemma/
|   |-- gpu_final.json
|   |-- gpu_initial.json
|   |-- gpu_telemetry.csv
|   |-- ninja_version.txt
|   |-- qwen/
|   |-- reference_probes.csv
|   |-- reference_probes.json
|   |-- research_packages.txt
|   |-- reused_qualification.json
|   |-- serving_packages.txt
|   |-- SHA256SUMS
|   |-- source/
|   |-- status.json
|   |-- unrecorded_qualification_rows.json
|   `-- unrecorded_reference_rows.json
|-- targeted_gpu3_20261022T213519Z_2309383.tar.gz
`-- targeted_gpu3_20261022T213519Z_2309383.tar.gz.sha256

89 directories, 256 files
```
