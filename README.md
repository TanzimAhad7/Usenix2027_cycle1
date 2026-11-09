# IEEE S&P research project

## Update of 9 November 2026: experiments added since 31 October

This update adds the code and light outputs of every experiment run from 1 to 9 November.
The "Current experiment" section further below describes the 31 October state and is now historical.

| Package | Experiment | Status |
|---|---|---|
| `results/user_runs/parallel_reference_gpu23_20261026T133503Z_*`, `gemma_recovery_20261027T015503Z_*` | 688-workflow parallel-reference campaign (Qwen, Gemma) | Complete; census/status updated from the mid-run snapshot |
| `IEEE_SP_Permission_Discrimination/`, `IEEE_SP_Gemma_Completion/`, `IEEE_SP_Gemma_Recovery/` | Permission-discrimination campaign and Gemma completions | Complete |
| `results/user_runs/discriminating_diagnostic_*`, `IEEE_SP_Discriminating_Diagnostic_GPU{2,3}/` | Facts x criterion diagnostic (X1/X3) | GPU 3 run complete; GPU 2 attempt failed early |
| `IEEE_SP_N1_GPU3/` | N1: why the generated reference becomes unsafe | Complete |
| `IEEE_SP_E1_GPU3/`, `IEEE_SP_E1_Preflight_Fix/` | E1: owner permission change under reference comparison | Complete (strict format 0/360; operative decisions reported) |
| `IEEE_SP_E2b_GPU2/` | E2b: controlled criterion study | Complete |
| `IEEE_SP_A01_GPU2/` | A1: semantic role, datatype and criterion | Complete |
| `IEEE_SP_J2_GPU2/` | J2: local fingerprint of the judge's joint-permission rule | Complete |
| `IEEE_SP_R3_GPU2/`, `IEEE_SP_R3_Tokenization_Fix/` | R3: enforcement after denial, released LocalLLM profile | Complete with technical issues |
| `IEEE_SP_END_TO_END_LARGE_GPU23/` | E0 prospective mechanism study and the score-to-effect bridge (7 policies, 108 bases) | Complete |
| `IEEE_SP_QWEN_FORMAT_REPAIR/`, `IEEE_SP_QWEN_FORMAT_REPAIR.py` | Qwen actor-format repair and full rerun of the bridge | Complete |
| `IEEE_SP_FINAL_EXPERIMENT_GPU3*/` | Final experiment `SP-GUARD-WRITE-20261108-V1` (serial, batched, shared-prefill attempts) | Qwen stages sealed, guarded outcomes censored by a parser regression; Gemma stopped at prefill qualification |
| `v3_reanalysis_scripts/` | Read-only reanalysis scripts behind the 9 November results | Current |
| `artifact_extracts/` | Compact evidence tables (see below) | Current |

**Evidence extracts.** The raw bridge episodes (about 490 MB) and final-experiment ledgers (`E1R.jsonl`, 673 MB) are too large for this mirror.
`artifact_extracts/` holds per-episode and per-record CSV tables with every field used by the 9 November analysis:

- `bridge_E13_gemma_episodes.csv`, `bridge_E14_qwen_episodes.csv` (12,096 episodes each; committed-effect classes, sanitizer value retention, proposed/dispatched/committed arguments) and the censored `bridge_E13_qwen_censored_episodes.csv`;
- `final_E1R_qwen_records.csv` (9,216 replay records with lawful and forbidden-variant scores) and `final_E2L_qwen_records.csv`;
- `witness_episodes/`: full raw episodes of the witness case `banking.3.0.live.1000` for every policy;
- `*.source_SHA256SUMS` and `EXTRACT_MANIFEST.json`: SHA-256 of every raw source file, so extracts can be checked against the local archives.

Rebuild them from the raw runs with `python3 v3_reanalysis_scripts/extract_artifacts.py`.

As before, only code and light outputs are published. Full raw archives, HTTP/model traces, world snapshots, weights, caches, environments,
research authorities, manuscripts and package documents stay local. Each run's `SHA256SUMS` or archive `.sha256` identifies its raw evidence.
`provenance/github_updates/` records every file added in this update with its SHA-256.

---

This repository follows the rejected USENIX submission's successor project.
The separate ICLR project is excluded. Older experiments and their original
outcome labels remain historical evidence; they are not current launch commands.

## Current experiment

`IEEE_SP_Reference_Study_GPU2/` implements the P0–P3 reference-admission study.
The physical device is **GPU 2 only**. Qwen3-32B and Gemma-3-27B-IT execute
sequentially, with four isolated experiment workers feeding one owned vLLM
server. Existing `.venv` and `.venv-serving` environments are reused.

```bash
bash RUN_CURRENT_EXPERIMENT.sh
bash SHOW_CURRENT_EXPERIMENT.sh
```

The first command starts a **new** nohup campaign. Publishing repository updates
does not restart collection. Do not launch a second campaign to update Git.
The launcher records logs, PIDs, status, raw model interactions, native effects,
interface diagnostics and complete archives below `results/user_runs/`.
It uses cached model weights and a GPU lock; it does not terminate unrelated jobs.

| Stage | Two-model allocation | Unit |
|---|---:|---|
| P0 | CPU qualification and live per-model probes | Engineering qualification |
| P1 | 304 | Held reference/admission sequences |
| P2 | 416, including 96 lawful-use controls | Held decision-component cells |
| P3 | 432 across 32 semantic roots | Autonomous workflows |

There are **1,152 planned scientific case records**, not independent attacks.
P1 and P2 cannot be pooled with P3 into an attack rate. Human semantic review is
pending and these auxiliary model configurations do not establish fidelity to
the principal published configuration. The evidence remains exploratory.

## Evidence history

| Stage | Location | Evidence status |
|---|---|---|
| Earlier parallel-reference and recovery work | Existing study directories and earlier `results/user_runs/` | Historical; original statuses retained |
| Permission-admission panel | `historical_experiments/IEEE_SP_Permission_Admission/` | 544 Qwen records; original Gemma qualification failed |
| Gemma completion | `historical_experiments/IEEE_SP_Gemma_Completion/` | 544 new Gemma records; 544 Qwen records retained, not rerun |
| Two intermediate Gemma failures | Dated `gemma_completion_gpu2_20261029T183327Z_565238_12588` and `...194618Z_823548_14030` result folders | Qualification failures; zero new Gemma science |
| Current reference-admission study | `IEEE_SP_Reference_Study_GPU2/` | Implemented and CPU/mock checked; live outcomes require current result files |

Gemma's completed panel contains 400 fixed-role records and 144 autonomous
attempts, of which 101 completed and 43 stopped on protocol errors. Qwen's
autonomous panel completed 137 of 144 attempts. Strict-format flags, parser
behavior, physical completion and final reporting remain separate.

The audits verified seven guarded workflows with forbidden simulated effects:
five exact-reference paths and two fuzzy-comparison paths. They establish
recorded admission paths, not a common causal explanation or general novelty.
Protective results, lawful controls and missingness constrain interpretation.
The current study tests reference construction, admission criteria and fresh
autonomous reachability rather than simply repeating those panels.

`EXPERIMENT_HISTORY.json` maps stages; `CURRENT_EXPERIMENT.json` identifies the
current launcher. `research_evidence/adversarial_reconstruction_20261030/`
contains bounded derived audit evidence and analysis code. Research manuscripts
and full reports are excluded from publication.

## Inspect and verify

```bash
bash PROJECT_STATUS.sh
bash VERIFY_PROJECT.sh
```

These commands use only Python's standard library and perform no inference.
Verification authenticates the added code and imported evidence, including the
current package manifest. Earlier verification/navigation files are preserved
under `archive/navigation_before_20261030/`; old launchers remain historical.
The old `GITHUB_LIGHT_ARTIFACTS.json` is a historical publication inventory,
not an inventory of this update. See `provenance/PROJECT_UPDATE_MANIFEST.json`.

Only light result files are published. Full raw archives, HTTP traces, model
weights, caches and environments remain local. Per-file SHA-256 hashes identify
the imported evidence and source archives. A running campaign's copied status
is a per-file snapshot, never an atomic or completed-run certificate.
