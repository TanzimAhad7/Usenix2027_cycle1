"""All source/SDK requests and simulator calibrations before GPU allocation."""
import argparse
import importlib.metadata
import sys
import tempfile
from pathlib import Path
from reference_study.common import ROOT, activate, digest, sha, write
from .design import manifest, inputs


def prepare(family, out):
    activate(family)
    import agentdojo.task_suite.load_suites
    from reference_discovery_parallel.base.source import verify_source, load_source
    from .worker import run_job
    from .cases import world_for
    from .simulation import dispatch
    source_identity = verify_source()
    core, _ = load_source()
    bodies = {}
    m = manifest(family)
    with tempfile.TemporaryDirectory(prefix='j2_prepare_') as tmp:
        for item in m['jobs']:
            key = item['input_key']
            if key in bodies:
                continue
            directory = Path(tmp) / item['id']
            result = run_job(item, directory, family, True)
            if not result['technical_complete']:
                raise RuntimeError('SDK/source/effect preparation failed: ' + str(result.get('error')))
            from reference_study.common import read
            records = read(directory / 'model_io/driver_records.json')
            if len(records) != 1 or records[0]['request'] != item['request_body']:
                raise RuntimeError('Frozen body not reproduced by actual SDK')
            task, candidate, references, allowed = inputs(item)
            world = world_for(item)
            # Every listed alternative must actually execute, not only the
            # candidate/reference. These are software calibrations, not trials.
            for index, operation in enumerate(allowed):
                effect = dispatch(core, world, operation, allowed, True,
                    directory / 'allowed_operation_calibrations' / str(index))
                if effect['assessment']['committed_count'] != 1 or effect['assessment']['violation']:
                    raise RuntimeError('Permitted alternative is not an executable lawful operation')
            held = read(directory / 'held_input.json')
            bodies[key] = dict(body=records[0]['request'], state_hash=held['initial_state_hash'])
    write(out, dict(version='J2_PREPARED_V1', family=family, bodies=bodies,
        model_inference=0, unique_requests=len(bodies),
        source_manifest_sha256=sha(ROOT / 'PACKAGE_MANIFEST.json'), source_identity=source_identity,
        simulator_all_alternatives_calibrated=True,
        environment=dict(python=sys.version, executable=sys.executable,
            dependencies={n: importlib.metadata.version(n) for n in
                ('agentdojo', 'openai', 'pydantic', 'httpx', 'tenacity')})))
    print('PREPARATION PASS', family, len(bodies), 'actual SDK requests; zero inference', flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--family', choices=('qwen', 'gemma'), required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    prepare(a.family, a.out)
