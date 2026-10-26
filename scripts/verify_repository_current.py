#!/usr/bin/env python3
"""Verify the current checkout; historical manifests are original build receipts."""
import hashlib
import json
import sys
from pathlib import Path


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    from reference_discovery_parallel.integrity import verify_package
    from reference_discovery_parallel.campaign import plan
    from reference_discovery_parallel.protocol import manifest

    receipt = verify_package(root)
    one = manifest()
    full = plan()
    if one['counts']['autonomous_workflows'] != 344 or full['autonomous_workflows'] != 688:
        raise RuntimeError('Current declared allocation differs from 344 per profile /688 combined')
    optional_missing = []
    for group in ('documentation_files', 'archival_evidence_files'):
        for name, expected in receipt.get(group, {}).items():
            path = root / name
            if not path.is_file():
                optional_missing.append(name)
            elif sha(path) != expected:
                raise RuntimeError('Present optional record differs from receipt: ' + name)
    original = receipt.get('original_full_package_manifest')
    if original and sha(root / original['path']) != original['sha256']:
        raise RuntimeError('Preserved original package receipt differs')
    readme = (root / 'README.md').read_text()
    for phrase in ('688', 'Up to 60', 'GPU 3', 'reference_discovery_parallel/', 'PROJECT_STATUS.sh'):
        if phrase not in readme:
            raise RuntimeError('Current README navigation is incomplete: ' + phrase)
    forbidden = ('# IEEE S&P v6.2 research foundation', 'already running Qwen server on port 18080 for GPU 2')
    if any(text in readme for text in forbidden):
        raise RuntimeError('Stale README launch guidance')
    authority = root / 'IEEE_SP_Standalone_Research_Authority_Current.md'
    if authority.exists():
        if '688' not in authority.read_text():
            raise RuntimeError('Local authority predates current campaign')
    print('CURRENT REPOSITORY VERIFY: PASS')
    print(f'Required runtime/source hashes: {len(receipt["files"])}; executable/frozen allocation: 688 autonomous + up to60 continuations.')
    print(f'Optional documentation/archive files absent: {len(optional_missing)}. Full archival reanalysis is not certified.')
    for name in optional_missing:
        print('OPTIONAL_NOT_SUPPLIED:', name)
    if not authority.exists():
        print('LOCAL_AUTHORITY_NOT_SUPPLIED: obtain the current authority separately for scientific planning.')
    print('Historical package manifests remain original assembly receipts, not integrity claims for this merged light checkout.')
    print('Zero model inference. Source consistency is not experiment completion, independent semantic review or scientific confirmation.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('CURRENT REPOSITORY VERIFY: FAIL:', str(exc), file=sys.stderr)
        raise SystemExit(1)
