from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f'.{os.getpid()}.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temporary.replace(path)


def append(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a') as stream:
        stream.write(json.dumps(value, ensure_ascii=False) + '\n')
        stream.flush()


def activate(family='qwen'):
    """Import ONLY the byte-preserved bundled runtime, never a neighboring repo."""
    import sys
    if family not in ('qwen', 'gemma'):
        raise ValueError(family)
    retained = ROOT / 'retained'
    sys.path.insert(0, str(retained))
    os.environ['REFERENCE_DISCOVERY_MODEL_FAMILY'] = family
    import reference_discovery_parallel as package
    if Path(package.__file__).resolve().parent != retained / 'reference_discovery_parallel':
        raise RuntimeError('A different retained runtime was already imported')
    from reference_discovery_parallel import common
    if common.MODEL_FAMILY != family:
        raise RuntimeError('Profiles must run in separate fresh Python processes')
    # The older fixed-role transport has a Qwen constant. This explicit profile
    # binding changes only its backend identifier, not its serializers/prompts.
    from reference_discovery_parallel.base import common as base_common
    from reference_discovery_parallel.base import transport
    base_common.MODEL = common.MODEL
    transport.MODEL = common.MODEL
    return common


def verify_package():
    data = read(ROOT / 'PACKAGE_MANIFEST.json')
    for relative, expected in data['files'].items():
        path = ROOT / relative
        if not path.is_file() or file_hash(path) != expected:
            raise RuntimeError('Package drift: ' + relative)
    return data

