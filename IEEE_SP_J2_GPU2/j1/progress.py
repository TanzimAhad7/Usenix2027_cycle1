"""Read-only progress, including setup failures before a controller exists."""
import json
import sys
from pathlib import Path

project = Path(sys.argv[1])
latest = project / 'logs/LATEST_J1'
run = sys.argv[2] or (latest.read_text().strip() if latest.is_file() else '')
if not run or Path(run).name != run:
    raise SystemExit('No valid J1 run yet. Start RUN_STUDY.sh.')
print('Run:', run)
folder = project / 'results/user_runs' / run
for name in ('status.json', 'qwen/status.json', 'gemma/status.json'):
    path = folder / name
    if path.is_file():
        data = json.loads(path.read_text())
        print(name, {k: data[k] for k in ('status', 'stage', 'completed', 'planned', 'active',
            'active_profile', 'elapsed_seconds', 'exit_code', 'error') if k in data})
state = project / 'logs' / (run + '.status')
if state.is_file():
    print(state.read_text().strip())
log = project / 'logs' / (run + '.log')
print('\nLog:', log)
if log.is_file():
    # Bounded tail, not a full potentially large log read.
    with log.open('rb') as f:
        f.seek(0, 2); length = f.tell(); f.seek(max(0, length-24000))
        lines = f.read().decode(errors='replace').splitlines()
    print('\n'.join(lines[-30:]))
for archive in sorted(folder.parent.glob(run + '*.zip')):
    print('Archive:', archive)
