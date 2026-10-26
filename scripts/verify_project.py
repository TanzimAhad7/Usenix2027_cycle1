#!/usr/bin/env python3
"""Compare a packaged workspace to its precomputed original-file SHA-256 inventory.

No network calls and no model calls. This checks bytes, not scientific truth.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    mf = ROOT / 'PACKAGE_MANIFEST.json'
    payload = json.loads(mf.read_text(encoding='utf-8'))
    entries = payload['files']
    fail = []
    for rel, expected in entries.items():
        p = ROOT / rel
        if not p.is_file():
            fail.append('MISSING: ' + rel)
        elif sha256(p) != expected:
            fail.append('CHANGED: ' + rel)
    if fail:
        for item in fail:
            print('ERROR:', item, file=sys.stderr)
        raise SystemExit(1)
    print('PROJECT VERIFY PASS:', len(entries), 'packaged files match their SHA-256 manifest')
    print('Scientific scope: file integrity only; not a native, autonomous or publication result.')

if __name__ == '__main__':
    main()
