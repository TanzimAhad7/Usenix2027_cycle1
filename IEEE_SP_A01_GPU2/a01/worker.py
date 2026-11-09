import argparse
import contextlib
import json
import signal
import sys
import time
import traceback
from pathlib import Path
from reference_study.common import activate, read, write

def run_job(item, out, family, mock=False, frozen=None):
    from .cases import run
    out = Path(out)
    if out.exists():
        raise RuntimeError('Refusing to overwrite or redraw attempted acquisition')
    start = time.monotonic()
    log = out.parent / '_diagnostic_logs' / (item['id'] + '.log')
    log.parent.mkdir(parents=True, exist_ok=True)
    old = signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('660-second cell watchdog')))
    signal.alarm(660)
    try:
        with log.open('w') as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
            result = run(item, out, family, mock, frozen)
    except BaseException as exc:
        out.mkdir(parents=True, exist_ok=True)
        result = dict(status='INTERRUPTED' if isinstance(exc, KeyboardInterrupt) else 'TECHNICAL_ERROR',
                      technical_complete=False, error=dict(type=type(exc).__name__, message=str(exc), traceback=traceback.format_exc()))
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
    result.update(item=item, id=item['id'], profile=family, mock=mock, elapsed_seconds=time.monotonic() - start)
    write(out / 'item.json', item)
    write(out / 'result.json', result)
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--family', choices=('qwen', 'gemma'), required=True)
    p.add_argument('--mock', action='store_true')
    p.add_argument('--prepared', type=Path)
    a = p.parse_args()
    activate(a.family)
    plan = read(a.prepared)['bodies'] if a.prepared else None
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt('Owned stop')))
    for line in sys.stdin:
        q = json.loads(line)
        key = q['item']['input_key']
        r = run_job(q['item'], q['out'], a.family, a.mock, plan[key] if plan else None)
        print(json.dumps(dict(id=r['id'], status=r['status'], qualified=r['technical_complete'])), flush=True)

if __name__ == '__main__':
    main()
