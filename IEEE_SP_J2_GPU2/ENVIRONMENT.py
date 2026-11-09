"""Read-only environment compatibility checks. Never installs or mutates."""
import argparse
import importlib.metadata
import json
import sys
from pathlib import Path


def check(kind):
    if sys.prefix == sys.base_prefix:
        raise RuntimeError('An isolated virtual environment is required')
    if kind == 'release':
        if sys.version_info[:3] != (3, 10, 21):
            raise RuntimeError('RELEASE requires Python 3.10.21')
        pins = (Path(__file__).parent / 'lineage/release.lock.txt').read_text().splitlines()
        for line in pins:
            if not line or line.startswith('#'):
                continue
            name, version = line.split('==')
            if importlib.metadata.version(name) != version:
                raise RuntimeError('RELEASE dependency mismatch: ' + name + '==' + version)
    else:
        if sys.version_info[:2] != (3, 12):
            raise RuntimeError('Serving requires isolated Python 3.12')
        for name, expected in [('vllm', '0.26.0'), ('torch', '2.11.0')]:
            actual = importlib.metadata.version(name)
            if actual.split('+')[0] != expected:
                raise RuntimeError('Serving dependency mismatch: ' + name + '==' + expected)
    return dict(status='PASS', kind=kind, executable=sys.executable,
                python=list(sys.version_info[:3]), prefix=sys.prefix)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('kind', choices=('release', 'serving'))
    p.add_argument('--quiet', action='store_true')
    a = p.parse_args()
    try:
        result = check(a.kind)
    except Exception as exc:
        if not a.quiet:
            print(str(exc), file=sys.stderr)
        raise SystemExit(1)
    if not a.quiet:
        print(json.dumps(result))
