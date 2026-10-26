# IEEE S&P v6.2 research foundation

**Single starting sequence:** `START_HERE.md`. **Continue scientific work:** `WORK_NEXT.md`. Additional evidence gates, manuscript requirements, module status and proposed schedules are consolidated under `docs/program/` and `protocols/proposed/`. Check schedules through `bash LAUNCH.sh protocols protocols_01`; they remain unimplemented conditional studies.

This is the starting repository for the **whole v6.2 research program** and a new IEEE S&P paper. It includes the selected USENIX design/code/data/results the plan builds on, their corrections and provenance, the current R/B implementation, and explicit obligations for the rest of the research. It is not a rebuttal or a claim that proposed experiments have already been completed.

The full plan is `docs/RESEARCH_PLAN.md`, preserved unchanged. `docs/PLAN_COVERAGE.csv` maps **every main section and appendix** to local artifacts, readiness and remaining work. Start by reading `docs/FOUNDATION.md`.

## What was selected from the prior project

The new project incorporates **all nine historical study trees**, including their task/design definitions, prompts, raw outputs, configurations/freezes, analysis code and scientific failure/correction records. It also includes the tested guard/runtime integrations and adapters, original oracle/replay logic, implementation evidence, final figures/producers, relevant verification/reproduction source and provenance.

`provenance/USENIX_SELECTION.csv` accounts for every original file. It includes 5,682 files and excludes 106 files (general project logs, superseded early pilot/cosmetic histories and model-generated literature-audit responses). Scientific per-study logs and failed/frozen records remain. A primary-source catalog and qualified reading/audit records are included separately. The bulk original ZIP and a duplicate complete extracted checkout are not required.

Everything retained is part of this directory. No command requires another USENIX project, archive or venv.

## Open and set up

Open `IEEE_SP_2027.code-workspace` in VS Code, locally or over Remote SSH. Python 3.12 on Linux is tested. Bootstrap needs a system Python and package-index access; research packages are installed only into this project's `.venv`.

```bash
bash LAUNCH.sh setup setup_01
tail -f logs/setup_01.log
```

Wait for `logs/setup_01.status` to report `exit_code=0`. Closing the terminal or stopping log viewing does not stop the nohup job on an ordinary host. For an explicit bootstrap interpreter use `RB_BASE_PYTHON=/absolute/path/to/python3.12 bash LAUNCH.sh setup setup_02`.

## Supported research modes

All setup/research jobs use **nohup**, a new log/PID/final status file, and the project venv. Use a unique run ID each time. These commands do different work and must not be confused:

```bash
# Recompute inherited frozen results and corrected primitive contrasts:
bash LAUNCH.sh historical historical_01

# Execute current source-bound R/B components and software tests:
bash LAUNCH.sh components components_01

# Regenerate historical displays from frozen evidence:
bash LAUNCH.sh figures figures_01
```

Follow a job with `tail -f logs/RUN_ID.log`, inspect `logs/RUN_ID.status`, and retain `results/user_runs/RUN_ID/`. Historical mode runs 48 inherited scientific checks and a separate primitive correction/oracle report. Components run 8 project tests plus 15 native tests, then 98 controlled executions / 61 diagnostic assertions. Figures 2–6 are regenerated; figure 1 is copied because its producer was not supplied. None is fresh model inference.

`bash VERIFY_PROJECT.sh` checks the delivered baseline bytes; intentional edits correctly appear as changes. `bash INIT_LOCAL_GIT.sh` creates a local repository without staging, committing or configuring a remote.

## GPU model jobs

Only **physical GPU 2 or 3** is authorized. The included adapted model client uses an already running Qwen server on port 18080 for GPU 2 or Gemma on 18081 for GPU 3. Socket-owner/descendant NVIDIA worker preflight refuses missing or mismatched placement; client CUDA visibility is not proof. `ss`, `ps` and `nvidia-smi` process visibility are required.

Create `config/qwen-attestation.json` or `config/gemma-attestation.json` from `experiments/review_binding/attestation.example.json`, recording the actual deployment and physical `gpu_index`.

```bash
export QWEN_MODEL_ID='YOUR_EXACT_SERVED_MODEL_ID'
export QWEN_ATTESTATION="$PWD/config/qwen-attestation.json"
bash LAUNCH.sh models qwen_development_01 2
tail -f logs/qwen_development_01.log
```

For GPU 3, set `GEMMA_MODEL_ID` and `GEMMA_ATTESTATION` and use `bash LAUNCH.sh models gemma_development_01 3`. Separate jobs can use GPUs 2 and 3 concurrently. CPU modes use no GPU. Model weights, drivers and serving software are deployment resources, not an old-project dependency. Actual server/parser/role qualification is still required.

## Scientific navigation

| Path | What it supplies |
|---|---|
| `docs/RESEARCH_PLAN.md` | Complete standalone v6.2 authority |
| `docs/PLAN_COVERAGE.csv` | All 16 sections and 14 appendices mapped to source, readiness and gaps |
| `docs/REVIEWER_OBLIGATIONS.csv` | Prior criticisms → new scientific obligations → evidence/status |
| `docs/WORK_PRODUCTS.csv`, `docs/DEFENSIBILITY_GAPS.md` | Eight plan deliverables and unresolved proof obligations |
| `research_basis/studies/01_*` through `09_*` | Historical natural, source, unauthorized, threshold, three guard/integration, live and replay studies |
| `research_basis/third_party/`, `implementation_evidence/`, `scripts/`, `figures/` | Exact inherited source, oracle, frozen checks, reproduction logic and displays |
| `experiments/review_binding/` | Current native-runtime R/B engine, model client, tests, protocol and raw development evidence |
| `provenance/` | Included/excluded file ledger, plan references, source availability and independent audit |
| `references/` | Manuscript, reviews, incident and primary-literature source catalog and reading records |
| `protocols/`, `research_records/` | Draft claim/confirmation templates and an initially empty real decision register |
| `validation/` | Software/isolation validation; not completed new research |
| `logs/`, `results/user_runs/` | Your fresh jobs and outputs |

## Readiness boundary

This is a **paper research foundation**, not completed evidence for a paper. R/B native components are implemented; their autonomous development client is adapted and no authoring model episode was completed. H24/P fixed-objective tasks, the missing pilot's D24/forks, conditional S128/A64/H64, independent human adjudication, claim-specific confirmation and the new manuscript still require actual work. See the coverage/gap tables rather than interpreting a test pass as completion.

Historical live wrappers are preserved as source, with the URL/context/fresh-parent defects identified by the plan. They are not approved launch commands and may contain old GPU defaults. Use only the current root launcher. Original labels/results remain immutable; new corrections carry their own primitive calculations. Frozen reanalysis, regenerated plots, component execution and fresh model evidence remain distinct.
