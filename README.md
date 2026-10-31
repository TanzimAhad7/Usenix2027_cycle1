# IEEE S&P research project

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
