"""Apply only the R3 CPU tokenization-container fix; retain previous runs."""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PATCH_DIR = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.r3fix-' + str(os.getpid()))
    temp.write_bytes(data)
    os.replace(temp, path)

def main(root):
    root = root.resolve()
    if root.name == 'source' or 'user_runs' in root.parts:
        raise RuntimeError('Choose the installed R3 project, not a frozen results/source directory')
    if not (root / 'RUN_STUDY.sh').is_file():
        raise RuntimeError('R3 project not found: ' + str(root))
    patch = json.loads((PATCH_DIR / 'PATCH.json').read_text())
    manifest_path = root / 'PACKAGE_MANIFEST.json'
    (root / 'logs').mkdir(exist_ok=True)
    with (root / 'logs/.r3_gpu2.lock').open('a') as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError('An R3 controller/setup is active; no files were changed') from exc
        manifest = json.loads(manifest_path.read_text())
        for name, expected in manifest['files'].items():
            rel = Path(name)
            if rel.is_absolute() or '..' in rel.parts or not (root / rel).is_file() or sha(root / rel) != expected:
                raise RuntimeError('Existing package verification failed: ' + name)
        for name, expected in patch['new_files'].items():
            if sha(PATCH_DIR / 'payload' / name) != expected:
                raise RuntimeError('Fix payload verification failed: ' + name)
        already = all((root / name).is_file() and sha(root / name) == expected
                      for name, expected in patch['new_files'].items())
        if already:
            print('ALREADY APPLIED: R3 tokenizer-container fix; existing files verified.')
            return 0
        if sha(manifest_path) != patch['original_manifest_sha256']:
            raise RuntimeError('This fix targets the delivered R3 package; its manifest differs. No files were changed.')
        for name, expected in patch['expected_original_files'].items():
            path = root / name
            if expected is None:
                if path.exists():
                    raise RuntimeError('Refusing to overwrite an unrelated file: ' + name)
            elif not path.is_file() or sha(path) != expected:
                raise RuntimeError('Original target differs: ' + name)
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        backup = root / 'patch_backups' / ('tokenization_' + stamp + '_' + str(os.getpid()))
        backup.mkdir(parents=True, exist_ok=False)
        changed = list(patch['new_files']) + ['PACKAGE_MANIFEST.json', 'DELIVERY_SHA256SUMS']
        before = {}
        for name in changed:
            path = root / name
            before[name] = path.read_bytes() if path.is_file() else None
            if before[name] is not None:
                target = backup / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(before[name])
        shutil.copy2(PATCH_DIR / 'PATCH.json', backup / 'PATCH.json')
        try:
            for name, expected in patch['new_files'].items():
                atomic(root / name, (PATCH_DIR / 'payload' / name).read_bytes())
                manifest['files'][name] = expected
            atomic(manifest_path, (json.dumps(manifest, indent=2) + '\n').encode())
            sums = ''.join(expected + '  ' + name + '\n' for name, expected in manifest['files'].items())
            sums += sha(manifest_path) + '  PACKAGE_MANIFEST.json\n'
            atomic(root / 'DELIVERY_SHA256SUMS', sums.encode())
            env = dict(os.environ, PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1', CUDA_VISIBLE_DEVICES='')
            env.pop('PYTHONPATH', None)
            env.pop('PYTHONHOME', None)
            with (backup / 'regression_tests.log').open('w') as output:
                result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_render.py', '-v'],
                                        cwd=root, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=180)
            if result.returncode:
                raise RuntimeError('Regression test failed; see ' + str(backup / 'regression_tests.log'))
            for name, expected in manifest['files'].items():
                if sha(root / name) != expected:
                    raise RuntimeError('Post-install verification failed: ' + name)
        except BaseException:
            for name, data in before.items():
                if data is None:
                    (root / name).unlink(missing_ok=True)
                else:
                    atomic(root / name, data)
            print('Installation rolled back; original package restored. Backup:', backup, file=sys.stderr)
            raise
        print('APPLIED: preserve native tokenizer output and validate its input_ids.')
        print('BACKUP:', backup)
        print('Previous results, environments, GPU2 settings, model requests and schedule preserved.')
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-root', type=Path, default=PATCH_DIR.parent / 'IEEE_SP_R3_GPU2')
    args = parser.parse_args()
    try:
        raise SystemExit(main(args.project_root))
    except Exception as exc:
        print('FIX NOT APPLIED:', exc, file=sys.stderr)
        raise SystemExit(1)
