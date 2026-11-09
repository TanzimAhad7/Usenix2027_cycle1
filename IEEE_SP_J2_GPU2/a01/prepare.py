"""Construct real source requests through each SDK without model inference."""
import argparse
import importlib.metadata
import sys
import tempfile
from pathlib import Path
from reference_study.common import activate, digest, read, sha, write, ROOT
from .design import manifest
from .worker import run_job

def prepare(stage, family, out):
    activate(family)
    # Register suites before importing individual workspace modules; the
    # pinned upstream package otherwise has a circular import in this order.
    import agentdojo.task_suite.load_suites
    from reference_discovery_parallel.base.source import verify_source
    source_identity = verify_source()
    m = manifest(stage, family)
    bodies = {}
    with tempfile.TemporaryDirectory(prefix='a01_prepare_') as tmp:
        for item in m['jobs']:
            if item['input_key'] in bodies:
                continue
            directory = Path(tmp) / item['id']
            result = run_job(item, directory, family, True)
            if not result['technical_complete']:
                raise RuntimeError('Source/simulator preparation failed: ' + str(result.get('error')))
            records = read(directory / 'model_io/driver_records.json')
            if len(records) != 1 or records[0]['role'] != 'judge':
                raise RuntimeError('Unexpected preparation request count/role')
            held = read(directory / 'held_input.json')
            bodies[item['input_key']] = dict(body=records[0]['request'], state_hash=held['initial_state_hash'])
    write(out, dict(version='A01_PREPARED_V1', stage=stage, family=family, bodies=bodies,
        model_inference=0, source_manifest_sha256=sha(ROOT / 'PACKAGE_MANIFEST.json'), source_identity=source_identity,
        environment=dict(python=sys.version, executable=sys.executable,
            dependencies={name: importlib.metadata.version(name) for name in ('agentdojo', 'openai', 'pydantic', 'httpx', 'tenacity')})))
    return bodies

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--stage', choices=('A0', 'A1'), required=True)
    p.add_argument('--family', choices=('qwen', 'gemma'), required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    prepare(a.stage, a.family, a.out)
