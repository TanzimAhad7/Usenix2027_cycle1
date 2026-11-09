#!/usr/bin/env bash
set -euo pipefail
P="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN="$(cat "$P/logs/LATEST_N1")"
"$P/.venv/bin/python" - "$P/results/user_runs/$RUN" <<'PY'
import json,sys
from pathlib import Path
r=Path(sys.argv[1]);s=json.loads((r/'status.json').read_text())
if s['status'] in ('STARTING','RUNNING','PREFLIGHT','CPU_QUALIFICATION','PROFILE_COMPLETE','CLEANUP_PENDING'):raise SystemExit('Run is still active; use SHOW_PROGRESS.sh.')
sys.path.insert(0,str(r/'source'))
from n1.report import analyze
analyze(r,json.loads((r/'FROZEN_MANIFEST.json').read_text()))
print((r/'analysis/totals.json').read_text())
print('Existing archive is an earlier snapshot; analysis on raw directory has been refreshed.')
PY
