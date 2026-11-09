"""Recovery integrity and unchanged per-profile scientific schedule."""
from .common import read,file_hash
from .protocol import manifest

def verify_package(root):
    recorded=read(root/'PARALLEL_REFERENCE_PACKAGE_MANIFEST.json')
    for name,expected in recorded['files'].items():
        if not (root/name).is_file() or file_hash(root/name)!=expected:raise RuntimeError('Package drift: '+name)
    if manifest()!=read(root/'PARALLEL_REFERENCE_MODEL_MANIFEST.json'):raise RuntimeError('Per-profile schedule changed')
    r=read(root/'GEMMA_RECOVERY_MANIFEST.json')
    if (r['model_family'],r['autonomous_workflows'],r['conditional_slots_max'])!=('gemma',344,30):raise RuntimeError('Recovery scope changed')
    if file_hash(root/'PARALLEL_REFERENCE_MODEL_MANIFEST.json')!=r['original_per_profile_manifest_sha256']:raise RuntimeError('Original scientific schedule changed')
    return recorded
