# Current native R/B diagnostic

This is one implemented part of the full research program. Read root `docs/PLAN_COVERAGE.csv` for the inherited basis and remaining modules. Use root `LAUNCH.sh` with its project venv/nohup logs and physical GPU 2/3 policy.

`diagnostic.py` uses the exact bundled guard, real AgentDojo runtime dispatch, explicit contracts and a separate simulated effect ledger. Fourteen constructed scenarios expand to 98 controlled executions with 61 assertions. Fifteen native tests cover observation/runtime/instrumentation and mock transport. Root tests additionally check GPU qualification and corruption detection in inherited primitive analysis.

Actors/reference proposals and fuzzy negative judgments in component mode are scripted; payments are simulated. Autonomous reachability is not established by component passes. `autonomous.py` is an adapted local-model development workflow. `FINDINGS.md`, `docs/PROTOCOL.md`, raw `evidence/` and reading ledgers preserve exact scope, controls, failed development and limitations. Your new runs are under root `results/user_runs/`.
