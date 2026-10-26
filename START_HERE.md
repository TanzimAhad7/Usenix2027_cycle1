# Start here

Use this directory as the single working repository for the new IEEE S&P paper. All selected inherited research dependencies are local. The complete standalone authority is `docs/RESEARCH_PLAN.md`.

```bash
cd IEEE_SP_2027
bash INIT_LOCAL_GIT.sh
code IEEE_SP_2027.code-workspace
bash LAUNCH.sh setup setup_01
tail -f logs/setup_01.log
```

Continue only after `logs/setup_01.status` contains `exit_code=0`. Then:

```bash
bash LAUNCH.sh historical historical_01
bash LAUNCH.sh components components_01
bash LAUNCH.sh protocols protocols_01
```

Each job runs through nohup with a unique log, PID and final status, and uses the root `.venv`. Those three jobs are CPU-only and may run concurrently. New run IDs prevent overwriting. `tail -f logs/components_01.log` follows the component job; Ctrl+C exits the log viewer, not the job.

Read `WORK_NEXT.md` for the next scientific work and how to continue without repeating completed work. Read `docs/FOUNDATION.md`, `docs/PLAN_COVERAGE.csv`, `docs/program/RESEARCH_WORK_PROGRAM.md` and the reviewer/gap records for the whole program. The root README contains qualified model-client commands restricted to physical GPU 2 or 3. Do not execute historical launchers under `research_basis/` as current jobs.

Optional `bash LAUNCH.sh figures figures_01` regenerates frozen displays with recorded render differences; it is not new inference. The new paper still requires novel claim selection, reviewed grants, actual model reachability/effects, causal interventions, independent human adjudication and fresh confirmation. File presence and schedule arithmetic do not satisfy those obligations.
