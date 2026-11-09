import argparse,importlib.metadata,json,sys
from pathlib import Path

def check(mode):
    if sys.prefix==sys.base_prefix:raise RuntimeError('An isolated virtual environment is required')
    if mode=='client':
        if sys.version_info[:3]!=(3,10,21):raise RuntimeError('Client requires pinned Python3.10.21')
        for line in (Path(__file__).parent/'release.lock.txt').read_text().splitlines():
            if not line or line.startswith('#'):continue
            name,version=line.split('==')
            if importlib.metadata.version(name)!=version:raise RuntimeError('Client dependency mismatch: '+name)
    else:
        if sys.version_info[:2]!=(3,12):raise RuntimeError('Serving requires Python3.12')
        for name,version in [('vllm','0.26.0'),('torch','2.11.0')]:
            if importlib.metadata.version(name).split('+')[0]!=version:raise RuntimeError('Serving dependency mismatch: '+name)
    return dict(status='PASS',mode=mode,python=sys.version,executable=sys.executable,packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['client','serving']);p.add_argument('--quiet',action='store_true');a=p.parse_args()
    try:r=check(a.mode)
    except Exception as e:
        if not a.quiet:print(str(e),file=sys.stderr)
        raise SystemExit(1)
    if not a.quiet:print(json.dumps(r))
