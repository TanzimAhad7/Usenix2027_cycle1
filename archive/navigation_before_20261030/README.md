# IEEE S&P standalone research project

This is the **complete cleaned code and light-artifact repository** for the new IEEE Symposium on Security and Privacy project. It contains the current campaign, selected original research foundation, historical implementations and available bounded result summaries. The rejected USENIX manuscript is the author's own unpublished research; this is a new submission, not a rebuttal. The hosting name `Usenix2027_cycle1` does not define the venue.

## Publish this clean tree to the existing GitHub repository

Extract this complete ZIP into a **separate folder** while the current experiment continues. From the extracted `IEEE_SP_2027_GITHUB_CLEAN` directory:

```bash
bash PUSH_LIGHT_TO_GITHUB.sh
```

This runs under nohup, prints its log/PID/status paths, and uses an existing project `.venv`. It clones `https://github.com/TanzimAhad7/Usenix2027_cycle1.git` into a separate temporary checkout, stages this complete clean code/light tree, commits and performs a normal push. Previous Git history is retained. Existing eligible remote result/foundation files and remote-only evidence are preserved; the cleanup cannot overwrite them with this older snapshot. If required runtime source has changed remotely since the supplied ZIP, publication stops rather than rolling it back. The original running directory, environments, GPU servers and raw results are never changed; publication does not require the experiment lock or an experiment restart. Existing Git/GitHub authentication and commit identity are needed. No force push occurs.

For a staged checkout without committing/pushing, use `bash PUSH_LIGHT_TO_GITHUB.sh --stage-only`. The log prints the prepared checkout path for inspection. If the project interpreter is elsewhere, set `IEEE_SP_RESEARCH_PYTHON=/absolute/project/.venv/bin/python`. The original configured interpreter at `/home/tahad/IEEE_SP/IEEE_SP_2027/.venv/bin/python` is the fallback. Publication uses no model inference.

Only root README, required legal notices and dependency/environment metadata are published as documentation exceptions. Research authorities/reports/papers remain excluded. The latest supplied authority is included **locally** as `IEEE_SP_Standalone_Research_Authority_Current.md` and is ignored by Git. The root `AGENTS.md` is likewise a local operating guide. A source clone may need those local documents supplied separately. Model weights, venvs, caches, full raw traces and archives are excluded. Code/artifact file cap: 10 MiB; result-file cap: 2 MiB; total selected cap: 512 MiB.

## Current scientific question and campaign

When does generated reference support preserve the authorization of an actual effect sequence—and when does a protected workflow avoid reaching an otherwise susceptible admission path?

The sole active implementation is `reference_discovery_parallel/` with entry point `RUN_PARALLEL_REFERENCE_GPU23.sh`.

| Allocation | Qwen | Gemma | Total |
|---|---:|---:|---:|
| CORE autonomous workflows | 176 | 176 | 352 |
| Ordinary execution/recovery | 72 | 72 | 144 |
| Recipient/parameter boundary | 96 | 96 | 192 |
| **Autonomous workflows** | **344** | **344** | **688** |
| Authentic matched continuations | Up to 30 | Up to 30 | **Up to 60** |

Policies per profile: OFF144, RELEASE144, EXACT_CAPACITY28 and RELEASE_G28. Comparators concentrate on UPFRONT neutral/count conditions. Other structures cover naturally consumed permission, distinct continuations, staged information, ordinary precommit failure and lost acknowledgement. Native DM/channel/email/banking effects span three simulated suites. The study is authored development evidence, not production prevalence, independent confirmation or an acceptance guarantee. The completed S1 held-candidate panel is not repeated.

## Models, GPU policy and environments

- **All model inference uses physical GPU 3**, UUID `GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6`.
- Qwen3-32B then Gemma-3-27B-IT run sequentially through one owned vLLM server on `127.0.0.1:18080`.
- Two isolated research workers overlap independent workflows on the same endpoint. This offers batching/overlap, not a measured twofold speedup.
- Shared GPU2 runs only a small optional accounting helper: no vLLM or model weights. The 40GB authorization is not implemented model-inference usage.
- Use `.venv` for research and `.venv-serving` for vLLM. Existing working environments are reused. All research collection uses nohup, unique logs/status/results, a shared GPU lock and owned-process cleanup.

| Model | Exact snapshot revision | Interface |
|---|---|---|
| Qwen/Qwen3-32B | `9216db5781bf21249d130ec9da846c4624c16137` | Cached native template / Hermes |
| google/gemma-3-27b-it | `005ad3404e59d6023443cb575daa05336842228a` | Explicit Gemma tagged-JSON adapter / strict parser |

Configured weight cache: `/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache`. That path supplies weights only; there is no dependency on the other project's code. New machines need the exact snapshots, CUDA/driver support and pinned environments. Tested versions include Python3.12.15, AgentDojo0.1.35, vLLM0.26.0, Torch2.11.0+cu130 and Transformers5.20.2. Current research pins are `requirements-reference-discovery.lock.txt`; existing environments should not be rebuilt for repository cleanup.

## Verify or inspect saved progress

```bash
bash VERIFY_PROJECT.sh
bash PROJECT_STATUS.sh
```

Verification checks required runtime hashes and the executable/frozen schedule with zero inference. Optional missing documentation and the full historical S1 archive are explicitly reported; they are not runtime dependencies. The embedded authenticated origin subset and every required source file remain checked. Missing an original full archive prevents full historical reanalysis even when current source verification passes.

The read-only status reader uses each profile's census and saved result files in this checkout. To inspect the original working run, pass `--run /home/tahad/IEEE_SP/IEEE_SP_2027/results/user_runs/YOUR_RUN_ID`. Parent-level census can remain SCHEDULED during child collection; a running Git snapshot is not atomic. No status reader starts or stops a model or corrects copied result files.

For an intended **new research campaign only after the existing run closes**, with both working venvs available:

```bash
source .venv/bin/activate
bash RUN_PARALLEL_REFERENCE_GPU23.sh
```

Do not restart current collection to publish or clean GitHub. Each case retains 15 iterations, a20-minute limit,96 HTTP attempts and8,192 output tokens per request. There is no default global cutoff or measured completion-time guarantee. Missing authentic fork origins remain `NO_ELIGIBLE_CHECKPOINT`, not safe completion.

## Evidence status in the supplied snapshot

Completed native pilot:36 autonomous workflows and two conditional continuations; ten conditional slots ineligible. Preserve raw labels22/12/2 and the explicit protocol overlay27/7/2. Guarded S1 was protected; the guarded email violation began before hostile exposure.

Completed S1 diagnostic:32 generated references,48 held admissions and80 native effects. Sixteen excess conditions violate,13 with a one-operation reference. These conditional comparisons are not48 autonomous guarded attacks. Lawful one-/two-operation controls and the capacity utility cost remain important.

The supplied older Git index is dated **2026-10-26T15:01:14Z /09:01MDT** and is preserved at `provenance/github_snapshots/20261026T150114_INDEX.json`. That non-atomic run export has100 saved Qwen result files,95 producer-qualified:79 secure,18 safe incomplete,two violation and one unknown-incomplete labels. The child census separately records100 COMPLETE,one iteration-censored,one RUNNING and242 SCHEDULED;30 forks scheduled. The two violation summaries concern email subject mismatch without accepted actor-carrier exposure. No Gemma child results or terminal campaign archive were supplied. These are partial producer labels, not current live progress, independently audited campaign findings or injected duplicate witnesses.

`GITHUB_LIGHT_ARTIFACTS.json` describes this clean exported tree or a subsequent publication snapshot, not later experiment progress. Light summaries never replace the complete local raw `.tar.gz` archive needed for scientific analysis.

## Repository organization

| Path | Role |
|---|---|
| `reference_discovery_parallel/` | Current collection, source/runtime adapters, observer, recovery, analysis and operational tests |
| `RUN_PARALLEL_REFERENCE_GPU23.sh`, `VERIFY_PROJECT.sh`, `PROJECT_STATUS.sh` | Current top-level operational entry points |
| `PARALLEL_REFERENCE_*MANIFEST.json`, `SOURCE_PROVENANCE_PARALLEL_REFERENCE.json` | Current scientific allocation and required runtime provenance |
| `research_basis/` | Selected original study code/data and third-party integrations; original valid contributions remain available |
| Earlier named study modules | Retained completed-study implementations at their original import paths |
| `results/user_runs/` | Available light summaries, including failed, partial, negative and unknown records; full raw traces are excluded |
| `archive/root_entrypoints/`, `archive/package_receipts/` | Old root launcher source and original build receipts, separated from current instructions |
| `provenance/`, `protocols/`, `validation/` | Source/evidence lineage, prior declarations and scoped assurance records |
| `ARCHIVE_MAP.json`, `REPOSITORY_CONTENTS.json` | Exact relocations, preserved hashes and inclusion/exclusion scope |

Archived launchers retain their original bytes and original-root assumptions; they are source records, not runnable current entry points from the archive folder. Historical package manifests certify their original assemblies, not every merged lightweight checkout. Keep original lossless archives for faithful historical reproduction. No scientific module, frozen allocation or saved result label was modified for this cleanup.

Select the final paper from the evidence, including protection and counterexamples. Source integrity, software qualification, autonomous reachability, effect truth, causal identification, human semantic review and confirmation are distinct obligations.
