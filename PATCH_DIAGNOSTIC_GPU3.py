#!/usr/bin/env python3
"""Create an isolated GPU3 diagnostic copy; never stop jobs or edit old results.

Usage from the IEEE_SP_2027 project directory:
    python3 PATCH_DIAGNOSTIC_GPU3.py
    bash IEEE_SP_Discriminating_Diagnostic_GPU3/RUN_DIAGNOSTIC.sh
"""
from __future__ import annotations

import argparse
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

PATCH_ID = 'diagnostic_gpu3_port18081_v1'
PORT = 18081
OLD_UUID = 'GPU-0b687901-110f-39c5-a5a9-dfe4b73cc932'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def verify(root):
    data = read_json(root / 'PACKAGE_MANIFEST.json')
    if not isinstance(data.get('files'), dict):
        raise RuntimeError('Unrecognized package manifest')
    for name, expected in data['files'].items():
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts:
            raise RuntimeError('Unsafe manifest member')
        path = root / rel
        if path.is_symlink() or not path.is_file() or sha(path) != expected:
            raise RuntimeError('Package hash differs: ' + name)
    return data


def gpu3_uuid():
    command = ['nvidia-smi', '-i', '3', '--query-gpu=index,uuid', '--format=csv,noheader,nounits']
    result = subprocess.run(command, capture_output=True, text=True, timeout=30, check=True)
    rows = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if len(rows) != 1:
        raise RuntimeError('GPU 3 did not resolve to exactly one device')
    values = [value.strip() for value in rows[0].split(',')]
    if len(values) != 2 or values[0] != '3' or not re.fullmatch(r'GPU-[0-9a-fA-F-]{36}', values[1]):
        raise RuntimeError('Could not authenticate physical GPU 3 index/UUID: ' + result.stdout)
    if values[1] == OLD_UUID:
        raise RuntimeError('GPU 3 UUID equals the recorded GPU 2 UUID; refusing ambiguous placement')
    return values[1]


def replace_once(text, old, new, label):
    if text.count(old) != 1:
        raise RuntimeError('Unexpected source version at ' + label)
    return text.replace(old, new, 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    project = args.project_root.expanduser().resolve()
    original = project / 'IEEE_SP_Discriminating_Diagnostic_GPU2'
    target = project / 'IEEE_SP_Discriminating_Diagnostic_GPU3'
    uuid = gpu3_uuid()
    if not original.is_dir():
        raise RuntimeError('Original diagnostic package missing: ' + str(original))
    source_manifest = verify(original)
    source_identity = sha(original / 'PACKAGE_MANIFEST.json')
    if target.exists():
        if target.is_symlink():
            raise RuntimeError('Target is a symlink; no files changed')
        receipt = target / 'GPU3_PATCH.json'
        if not receipt.is_file():
            raise RuntimeError('GPU3 directory already exists without this patch receipt; no overwrite')
        data = read_json(receipt)
        if (data.get('patch_id'), data.get('gpu_uuid'), data.get('source_manifest_sha256')) != (PATCH_ID, uuid, source_identity):
            raise RuntimeError('Existing GPU3 copy has different provenance; no overwrite')
        verify(target)
        print('GPU3 patch already applied and verified.')
        print('Run: bash IEEE_SP_Discriminating_Diagnostic_GPU3/RUN_DIAGNOSTIC.sh')
        return
    temporary = Path(tempfile.mkdtemp(prefix='.diagnostic_gpu3_patch_', dir=project))
    modified = []
    try:
        # Copy only authenticated distribution members, never logs, results,
        # environments, untracked files or neighboring project code.
        for rel in source_manifest['files']:
            dst = temporary / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original / rel, dst)

        paths = [Path('reference_study/common.py'), Path('diagnostic/controller.py'),
                 Path('reference_study/profile.py'), Path('retained/reference_discovery_parallel/common.py')]
        for rel in paths:
            path = temporary / rel
            text = path.read_text()
            if str(rel) == 'reference_study/common.py':
                text = replace_once(text, 'GPU_INDEX=2', 'GPU_INDEX=3', str(rel))
                text = replace_once(text, "GPU_UUID='" + OLD_UUID + "'", "GPU_UUID='" + uuid + "'", str(rel))
                text = replace_once(text, "LOCK_NAME='gpu2_sequence.lock'", "LOCK_NAME='gpu3_sequence.lock'", str(rel))
            elif str(rel) == 'retained/reference_discovery_parallel/common.py':
                text, count = re.subn(r"^GPU_UUID\s*=\s*'GPU-[0-9a-fA-F-]+'", "GPU_UUID = '" + uuid + "'", text, flags=re.M)
                if count != 1:
                    raise RuntimeError('Retained GPU UUID anchor changed')
            elif str(rel) == 'diagnostic/controller.py':
                text = replace_once(text, 'physical_gpu=2,gpu_uuid=GPU_UUID', 'physical_gpu=GPU_INDEX,gpu_uuid=GPU_UUID', str(rel))
            text = text.replace('GPU2', 'GPU3').replace('physical GPU 2', 'physical GPU 3')
            path.write_text(text)

        # Endpoint changes are restricted to runnable adapter/runtime code.
        # Vendored public guard, task/checkpoint data and historical provenance
        # are not changed. The source factory receives the new port via its
        # existing LOCAL_LLM_PORT setting in these adapters.
        for folder in ['diagnostic', 'reference_study', 'permission_admission', 'retained/reference_discovery_parallel']:
            for path in (temporary / folder).rglob('*.py'):
                if 'vendor' in path.parts:
                    continue
                text = path.read_text().replace('18080', str(PORT))
                if path.name == 'execution_config.py':
                    text = text.replace(OLD_UUID, uuid)
                path.write_text(text)

        for name in ['RUN_DIAGNOSTIC.sh', '_inner.sh', 'STOP_DIAGNOSTIC.sh', 'SHOW_PROGRESS.sh', 'README.md', 'AGENTS.md']:
            path = temporary / name
            text = path.read_text().replace('GPU2', 'GPU3').replace('GPU 2', 'GPU 3')
            text = text.replace('gpu2_sequence.lock', 'gpu3_sequence.lock')
            text = text.replace('discriminating_diagnostic_gpu2_', 'discriminating_diagnostic_gpu3_')
            text = text.replace('IEEE_SP_Discriminating_Diagnostic_GPU2', 'IEEE_SP_Discriminating_Diagnostic_GPU3')
            text = text.replace('DIAGNOSTIC_LATEST', 'DIAGNOSTIC_GPU3_LATEST')
            path.write_text(text)
        readme = temporary / 'README.md'
        readme.write_text('GPU3 execution amendment: physical GPU 3 / UUID ' + uuid +
                          ', local port 18081, gpu3_sequence.lock, separate GPU3 latest-run pointer.\n'
                          'Scientific conditions, model revisions and public guard are unchanged.\n'
                          'Earlier validation records describe the GPU2 software build; this patch has no live GPU3 result yet.\n\n' + readme.read_text())

        for rel, old_hash in source_manifest['files'].items():
            path = temporary / rel
            new_hash = sha(path)
            if new_hash != old_hash:
                modified.append(dict(path=rel, before_sha256=old_hash, after_sha256=new_hash))
            # Evidence and public implementation must be bit-for-bit preserved.
            if rel.startswith(('diagnostic_inputs/', 'review_packets/')) or '/vendor/' in rel:
                if new_hash != old_hash:
                    raise RuntimeError('Protected evidence/source changed: ' + rel)
        for path in temporary.rglob('*.py'):
            ast.parse(path.read_text(), filename=str(path))
        for path in temporary.glob('*.sh'):
            subprocess.run(['bash', '-n', str(path)], check=True)
        common = (temporary / 'reference_study/common.py').read_text()
        assert 'GPU_INDEX=3' in common and uuid in common and 'gpu3_sequence.lock' in common
        assert 'PORT=18081' in (temporary / 'retained/reference_discovery_parallel/base/serving.py').read_text()
        assert 'DIAGNOSTIC_GPU3_LATEST' in (temporary / 'RUN_DIAGNOSTIC.sh').read_text()
        for folder in ['diagnostic', 'reference_study', 'permission_admission', 'retained/reference_discovery_parallel']:
            for path in (temporary / folder).rglob('*.py'):
                if 'vendor' not in path.parts and '18080' in path.read_text():
                    raise RuntimeError('Unpatched endpoint: ' + str(path))
        receipt = dict(patch_id=PATCH_ID, created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                       physical_gpu=3, gpu_uuid=uuid, local_port=PORT, lock='gpu3_sequence.lock',
                       source_package=str(original), source_manifest_sha256=source_identity,
                       changed_files=modified, scientific_conditions_changed=False,
                       public_vendor_and_evidence_unchanged=True, old_package_unchanged=True,
                       live_gpu_inference_executed=False)
        (temporary / 'GPU3_PATCH.json').write_text(json.dumps(receipt, indent=2) + '\n')
        files = {str(p.relative_to(temporary)): sha(p) for p in sorted(temporary.rglob('*')) if p.is_file()}
        manifest = dict(source_manifest)
        manifest.update(kind='DISCRIMINATING_DIAGNOSTIC_GPU3_PATCH_V1', files=files)
        (temporary / 'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
        verify(temporary)
        if sha(original / 'PACKAGE_MANIFEST.json') != source_identity:
            raise RuntimeError('Original package changed while patching')
        temporary.rename(target)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    print('GPU3 patch applied: ' + str(target))
    print('Physical GPU: 3 | UUID: ' + uuid + ' | Port: 18081')
    print('Original package and results preserved. No processes stopped.')
    print('Run: bash IEEE_SP_Discriminating_Diagnostic_GPU3/RUN_DIAGNOSTIC.sh')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        raise SystemExit('PATCH FAILED: ' + str(exc))
