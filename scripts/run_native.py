#!/usr/bin/env python3
"""Run the native diagnostic with its tests and a provenance receipt."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('run_id')
    args = p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.run_id):
        p.error('run_id must contain only letters, digits, underscores or hyphens')
    out = ROOT / 'results/user_runs' / args.run_id
    out.mkdir(parents=True, exist_ok=False)
    native = ROOT / 'experiments/review_binding'
    receipt = dict(run_id=args.run_id, status='STARTED',
        started_utc=datetime.now(timezone.utc).isoformat(),
        python=sys.version, executable=sys.executable, platform=platform.platform(),
        scope='Scripted native-runtime diagnostics with a custom simulated ledger',
        autonomous_episodes=0, stages=[], source_sha256={})
    for base in (native, ROOT/'scripts', ROOT/'tests'):
        for path in sorted(base.rglob('*')):
            if (path.is_file() and path.suffix in ('.py', '.sh', '.txt')
                and not any(x in path.relative_to(base).parts for x in ('evidence','runs','__pycache__','.venv'))):
                receipt['source_sha256'][str(path.relative_to(ROOT))] = sha(path)
    for path in [Path(__file__), *ROOT.glob('*.sh'), ROOT/'PACKAGE_MANIFEST.json',
                 ROOT/'docs/RESEARCH_PLAN.md']:
        receipt['source_sha256'][str(path.relative_to(ROOT))] = sha(path)
    def save():
        (out / 'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    save()
    stages = [
        ('project_tests', ROOT, ['-m','unittest','discover','-s','tests','-v']),
        ('native_tests', native, ['-m','unittest','discover','-s','tests','-v']),
        ('native_components', native, ['diagnostic.py','--out',str(out/'native')]),
    ]
    try:
        for name, cwd, argv in stages:
            print('Running '+name, flush=True)
            with (out/(name+'.log')).open('w') as log:
                result = subprocess.run([sys.executable,*argv],cwd=cwd,stdout=log,stderr=subprocess.STDOUT)
            receipt['stages'].append(dict(name=name,returncode=result.returncode))
            save()
            if result.returncode:
                raise RuntimeError(name+' failed; see '+str(out/(name+'.log')))
        receipt['status']='PASSED'
    except Exception as exc:
        receipt['status']='FAILED'
        receipt['error']=str(exc)
    receipt['ended_utc']=datetime.now(timezone.utc).isoformat()
    receipt['output_sha256']={str(f.relative_to(out)):sha(f) for f in sorted(out.rglob('*'))
        if f.is_file() and f.name!='receipt.json'}
    save()
    print(receipt['status']+': '+str(out))
    if receipt['status']!='PASSED':
        print(receipt.get('error'), file=sys.stderr)
        return 1
    print('Scripted component evidence only. Zero autonomous model episodes in this run.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
