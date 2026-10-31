"""Authenticate imported source and light evidence without research dependencies."""
from pathlib import Path, PurePosixPath
import hashlib, json, sys

def verify(root):
    root=Path(root).resolve()
    manifest=json.loads((root/'provenance/PROJECT_UPDATE_MANIFEST.json').read_text())
    checked=0
    for name,record in manifest['files'].items():
        p=PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts:raise ValueError('Unsafe manifest path')
        target=root/name
        if any(x.is_symlink() for x in [target,*list(target.parents)[:len(p.parts)-1]]):
            raise ValueError('Symlink in '+name)
        data=target.read_bytes()
        if hashlib.sha256(data).hexdigest()!=record['sha256']:raise ValueError('Hash mismatch: '+name)
        checked+=1
    for package in manifest['packages']:
        directory=root/package['directory']
        source=json.loads((directory/'PACKAGE_MANIFEST.json').read_text())
        for name,expected in source['files'].items():
            data=(directory/name).read_bytes()
            if hashlib.sha256(data).hexdigest()!=expected:raise ValueError('Runtime hash mismatch: '+str(directory/name))
    # Verify the actual panel records, not merely aggregate totals in a README.
    qwen=root/'results/user_runs/permission_admission_20261027T205610Z_3429255_17219/qwen'
    completion=root/'results/user_runs/gemma_completion_gpu2_20261029T211739Z_1117045_8864'
    for label,directory in [('original_qwen',qwen),('new_gemma',completion/'gemma'),('retained_qwen',completion/'qwen')]:
        count=sum(1 for p in directory.glob('E*/**/result.json'))
        if count!=544:raise ValueError(label+' record count differs: '+str(count))
    for path in qwen.glob('E*/**/result.json'):
        raw=path.read_bytes();original=json.loads(raw)
        retained=json.loads((completion/'qwen'/path.relative_to(qwen)).read_text())
        provenance=retained.pop('_retained_from_parent')
        if provenance['original_sha256']!=hashlib.sha256(raw).hexdigest():
            raise ValueError('Retained Qwen original hash differs: '+str(path))
        # The delivered completion compacted environments but retained decisions,
        # flags, effects and scientific fields. Preserve both actual file versions.
        for record in [original,retained]:
            for arm in record.get('native_clone_arms',{}).values():
                arm.pop('environment',None)
        if original!=retained:raise ValueError('Retained Qwen scientific fields differ: '+str(path))
    print('PASS:',checked,'imported files; all three source manifests; 544 original Qwen + 544 new Gemma + 544 retained Qwen records.')
    print('This verifies light evidence and source bytes; raw traces and live model behavior are outside this check.')
    return checked

if __name__=='__main__':
    try:verify(Path(__file__).resolve().parents[1])
    except Exception as e:print('VERIFY FAILED:',e,file=sys.stderr);sys.exit(1)
