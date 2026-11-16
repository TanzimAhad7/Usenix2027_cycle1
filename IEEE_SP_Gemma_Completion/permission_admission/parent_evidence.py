"""Validate and retain the finished Qwen readouts without changing the parent.

Accepts the original result directory or its full raw tar.gz. No network, model
request, source import from the parent, or extraction of arbitrary archive files.
"""
import copy
import hashlib
import json
import tarfile
from pathlib import Path, PurePosixPath

from .util import ROOT, read, write, file_hash

PARENT_ID = 'permission_admission_20261027T205610Z_3429255_17219'
EXPECTED_ARCHIVE_SHA256 = 'cd0ee5489db2a8ca71563c75e28f52b85a3669e1069c1c4f2f85d117f35821d7'


def ids(manifest):
    return [(panel, item['id']) for panel in ('E1','E2') for item in manifest[panel]] + [
        ('E3', item['id']) for block in manifest['E3_blocks'] for item in block]


def default_parent(project):
    folder = Path(project) / 'results/user_runs' / PARENT_ID
    if folder.is_dir(): return folder
    archive = Path(str(folder) + '.tar.gz')
    return archive


def selected_names(manifest):
    return {'status.json','qwen/status.json','qwen/census.json','gemma/status.json',
            'FROZEN_MANIFEST.json','SHA256SUMS','source/PACKAGE_MANIFEST.json'} | {
            f'qwen/{panel}/{ident}/result.json' for panel,ident in ids(manifest)}


def load_selected(path, manifest):
    path = Path(path); names = selected_names(manifest); blobs = {}; original_archive_hash = None
    gemma_results_found = []
    if path.is_dir():
        for name in names:
            p = path / name
            if not p.is_file(): raise RuntimeError('Required parent evidence missing: '+str(p))
            blobs[name] = p.read_bytes()
        gemma_results_found = [str(p.relative_to(path)) for panel in ('E1','E2','E3')
                               for p in (path/'gemma'/panel).glob('*/result.json')]
    elif path.is_file():
        original_archive_hash = file_hash(path)
        if original_archive_hash != EXPECTED_ARCHIVE_SHA256:
            raise RuntimeError('Parent archive digest differs from the audited original; no inference started')
        with tarfile.open(path, 'r|gz') as archive:
            for member in archive:
                parts = PurePosixPath(member.name).parts
                if not parts or parts[0] != PARENT_ID or '..' in parts or member.name.startswith('/'):
                    raise RuntimeError('Unexpected parent archive path')
                if not (member.isfile() or member.isdir()):
                    raise RuntimeError('Unsupported parent archive entry')
                relative = '/'.join(parts[1:])
                if relative.startswith(('gemma/E1/','gemma/E2/','gemma/E3/')) and relative.endswith('/result.json'):
                    gemma_results_found.append(relative)
                if member.isfile() and relative in names:
                    blobs[relative] = archive.extractfile(member).read()
        if set(blobs) != names: raise RuntimeError('Parent archive is missing required evidence')
    else:
        raise RuntimeError('Parent run not found. Supply --parent /path/to/original/result-directory-or-full.tar.gz')
    if gemma_results_found:
        raise RuntimeError('Parent already contains Gemma scientific results; refusing a blind duplicate completion')
    sums = {}
    for line in blobs['SHA256SUMS'].decode().splitlines():
        sha, relative = line.split('  ', 1); sums[relative] = sha
    for relative, content in blobs.items():
        if relative == 'SHA256SUMS': continue
        if sums.get(relative) != hashlib.sha256(content).hexdigest():
            raise RuntimeError('Parent evidence checksum mismatch: '+relative)
    return blobs, original_archive_hash


def retain(path, out, manifest):
    blobs, archive_hash = load_selected(path, manifest)
    data = {name: json.loads(content) for name,content in blobs.items()
            if name != 'SHA256SUMS' and not name.endswith('/result.json')}
    status = data['status.json']
    if status.get('run_id') != PARENT_ID or status.get('mode') != 'MODEL_EXPERIMENT':
        raise RuntimeError('Parent identity/mode is not the audited scientific run')
    if data['FROZEN_MANIFEST.json'] != manifest:
        raise RuntimeError('Scientific allocation or task bytes differ from the parent; no inference started')
    if data['qwen/status.json'].get('completed') != 544 or data['gemma/status.json'].get('completed') != 0:
        raise RuntimeError('Parent does not have complete Qwen and zero scientific Gemma cases')
    expected_source = read(ROOT/'provenance/EXPECTED_PARENT_SOURCE_MANIFEST.json')
    if data['source/PACKAGE_MANIFEST.json'] != expected_source:
        raise RuntimeError('Parent source manifest differs from the audited original')
    index=[]
    for panel,ident in ids(manifest):
        relative=f'qwen/{panel}/{ident}/result.json';row=json.loads(blobs[relative])
        if row.get('id')!=ident or row.get('profile')!='qwen' or row.get('mock') is not False or not row.get('attempted'):
            raise RuntimeError('Invalid/mocked parent Qwen result: '+relative)
        # Keep every scalar decision, label and outcome. Drop only bulky native
        # clone environments from this carried readout; the original archive
        # retains full states, requests and all other raw evidence.
        compact=copy.deepcopy(row)
        for arm in compact.get('native_clone_arms',{}).values():
            arm.pop('environment',None)
        compact['_retained_from_parent']=dict(run_id=PARENT_ID,result_path=relative,
            original_sha256=hashlib.sha256(blobs[relative]).hexdigest(),inference_in_completion=0,
            omitted=['native_clone_arms.*.environment'],original_qualification_preserved=True)
        write(out/relative,compact)
        index.append(dict(id=ident,panel=panel,path=relative,sha256=hashlib.sha256(blobs[relative]).hexdigest(),
                          qualified=row['qualified'],status=row['status']))
    for relative in ('qwen/status.json','qwen/census.json'):
        target=out/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(blobs[relative])
    receipt=dict(status='RETAINED_VERIFIED',parent_run_id=PARENT_ID,parent_path=str(Path(path).absolute()),
        source_mode='directory' if Path(path).is_dir() else 'audited_full_archive',
        original_archive_sha256_expected=EXPECTED_ARCHIVE_SHA256,archive_sha256_recomputed=archive_hash,
        checked_selected_files=len(blobs)-1,retained_qwen_records=len(index),
        qwen_generations_in_completion=0,qualification_flags_rewritten=False,
        scope='Readouts only. Full parent raw requests/states remain in the original archive. '
              'Directory inputs are checked against their retained SHA256SUMS; archive inputs additionally match the audited full archive digest.')
    write(out/'qwen/RETAINED_EVIDENCE.json',receipt)
    write(out/'parent_link/PARENT_EVIDENCE.json',receipt)
    write(out/'parent_link/QWEN_RESULT_HASHES.json',index)
    for name in ['status.json','gemma/status.json','source/PACKAGE_MANIFEST.json']:
        write(out/'parent_link'/name,data[name])
    return receipt

