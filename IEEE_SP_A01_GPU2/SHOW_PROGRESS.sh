#!/usr/bin/env bash
set -euo pipefail
P="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN="$(cat "$P/logs/LATEST_A01")"
python3 - "$P" "$RUN" <<'PY'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);run=sys.argv[2];out=p/'results/user_runs'/run
print('Run:',run)
for f in [out/'status.json',out/'qwen/status.json',out/'gemma/status.json']:
 if f.is_file():
  x=json.loads(f.read_text());print(f.parent.name, {k:x[k] for k in ('status','stage','completed','planned','active','elapsed_seconds','error') if k in x})
terminal=p/'logs'/(run+'.status')
if terminal.exists():print(terminal.read_text())
log=p/'logs'/(run+'.log');print('Log:',log)
if log.exists():print('\n'.join(log.read_text(errors='replace').splitlines()[-35:]))
print('Results:',out)
for a in sorted((p/'results/user_runs').glob(run+'*.tar.gz')):print('Archive:',a)
PY
