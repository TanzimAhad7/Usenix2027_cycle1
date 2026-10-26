"""Read-only package and both frozen schedule checks; no research dependencies."""
from .common import read,file_hash
from .protocol import manifest

def verify_package(root):
    recorded=read(root/'PARALLEL_REFERENCE_PACKAGE_MANIFEST.json')
    for name,expected in recorded['files'].items():
        path=root/name
        if not path.is_file() or file_hash(path)!=expected:raise RuntimeError('Package drift: '+name)
    if manifest()!=read(root/'PARALLEL_REFERENCE_MODEL_MANIFEST.json'):raise RuntimeError('Per-profile manifest differs from executable schedule')
    from .campaign import plan
    if plan()!=read(root/'PARALLEL_REFERENCE_FROZEN_MANIFEST.json'):raise RuntimeError('Dual manifest differs from executable schedule')
    return recorded
