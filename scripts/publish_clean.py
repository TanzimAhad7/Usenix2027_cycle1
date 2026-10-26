#!/usr/bin/env python3
"""Publish a clean code/light snapshot in an isolated clone; never edit a live run."""
import argparse
import ast
import collections
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys

SOURCE_LIMIT=10*1024*1024
OUTPUT_LIMIT=2*1024*1024
TOTAL_LIMIT=512*1024*1024
SKIP_DIRS={'.git','.git-publish','.tools','.cache','.hf_cache','__pycache__','.rsync-tmp','.pytest_cache','.mypy_cache','.ruff_cache','node_modules','wandb','local_research'}
DOC_DIRS={'docs','doc','documentation','references'}
DOC_SUFFIXES={'.md','.markdown','.rst','.txt','.pdf','.doc','.docx','.ppt','.pptx','.odt','.rtf','.tex','.bib'}
RAW_DIRS={'source','sources','fixtures','checkpoints','eligible','matched_origins','http','requests','model_io','raw','token_diagnostics','episode_workers'}
ARCHIVES=('.zip','.gz','.bz2','.xz','.zst','.7z','.tar','.tgz','.pt','.pth','.safetensors','.ckpt','.onnx','.gguf','.bin','.npy','.npz','.pkl','.pickle','.pyc','.pyo','.so','.dll','.dylib')
RAW_NAMES={'messages.json','events.jsonl','driver_records.json','initial_world.json','final_world.json','parent_checkpoint.json','executed_guard.py','native.log','diagnostic.log','server.log','controller.log'}
LIGHT_SUFFIXES={'.json','.csv','.tsv','.md','.txt','.sha256','.svg','.png','.pdf','.log','.status','.jinja'}
KEYS=[re.compile(rb'gh[pousr]_[A-Za-z0-9]{36,}'),re.compile(rb'github_pat_[A-Za-z0-9_]{30,}'),re.compile(rb'sk-(?:proj-|ant-)?[A-Za-z0-9_-]{24,}'),re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\r\n]+(?:[A-Za-z0-9+/=]{40,}[\r\n]+)')]

def sha(data):return hashlib.sha256(data).hexdigest()
def excluded_dir(name):return name in SKIP_DIRS or name.startswith(('.venv','venv.backup'))
def documentation(path):
    if path.as_posix()=='README.md':return False
    low=path.name.lower()
    legal=low.startswith(('license','copying','notice','third_party_notices','third-party-notices'))
    metadata=low.startswith(('requirements','constraints')) or 'sha256sums' in low or (path.parts[0]=='validation' and low.endswith('_packages.txt')) or low in {'uv.lock','poetry.lock','pipfile.lock','requirements.lock'}
    if legal or metadata:return False
    return any(x.lower() in DOC_DIRS for x in path.parts[:-1]) or path.suffix.lower() in DOC_SUFFIXES or low.startswith(('readme','changelog','authors','contributing'))

def policy(path,size):
    low=path.name.lower();parts=path.parts
    if parts[0]=='logs':return 'live_root_logs'
    if any(excluded_dir(x) for x in parts[:-1]):return 'environment_cache_or_local_only'
    if documentation(path):return 'research_documentation'
    if low.endswith(ARCHIVES) or low.endswith(('.tmp','.partial')) or (low.endswith('.lock') and low not in {'uv.lock','poetry.lock','pipfile.lock','requirements.lock'}):return 'archive_binary_or_temporary'
    if low=='.env' or (low.startswith('.env.') and low not in {'.env.example','.env.sample','.env.template'}) or low.endswith(('.pem','.key','.p12','.pfx')) or low in {'id_rsa','id_ed25519','.netrc','.git-credentials'} or re.match(r'^(credentials|secrets|service.account).*\.json$',low):return 'credential_file'
    if parts[0]=='results':
        if any(x in RAW_DIRS for x in parts[1:-1]):return 'raw_or_duplicate_output'
        if low in RAW_NAMES or any(x in low for x in ('.request.','.response.','.tokens.','.transport.','.reused.','policy_records','checkpoint','before_world','after_world')) or low.startswith('batch_') or low.endswith('.jsonl'):return 'raw_trace_or_state'
        if low!='sha256sums' and path.suffix.lower() not in LIGHT_SUFFIXES:return 'not_light_output'
        if size>OUTPUT_LIMIT:return 'result_over_2MiB'
    elif size>SOURCE_LIMIT:return 'file_over_10MiB'
    return None

def selected(root):
    paths=[];omitted=collections.Counter();total=0
    for current,dirs,files in os.walk(root,followlinks=False):
        here=Path(current)
        dirs[:]=sorted(x for x in dirs if not excluded_dir(x) and not (here==root and x=='logs') and not (here/x).is_symlink())
        for name in sorted(files):
            path=here/name;rel=path.relative_to(root)
            try:info=path.lstat()
            except FileNotFoundError:omitted['vanished_during_snapshot']+=1;continue
            if not stat.S_ISREG(info.st_mode):omitted['symlink_or_special']+=1;continue
            if rel.as_posix()=='GITHUB_LIGHT_ARTIFACTS.json':continue
            reason=policy(rel,info.st_size)
            if reason:omitted[reason]+=1
            else:paths.append(rel);total+=info.st_size
    if total>TOTAL_LIMIT:raise RuntimeError('Code/light snapshot exceeds512MiB; nothing published')
    return sorted(paths),omitted

def run(argv,cwd=None,check=True):
    value=subprocess.run(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if check and value.returncode:raise RuntimeError('Command failed: '+str(argv[0])+'\n'+value.stderr.decode(errors='replace'))
    return value

def publish(root,remote,stage_only=False):
    if re.search(r'https?://[^/]*@',remote):raise RuntimeError('Use a credential-free remote URL')
    # Package verification imports no model-serving or research dependencies.
    sys.path.insert(0,str(root))
    from reference_discovery_parallel.integrity import verify_package
    recorded=verify_package(root)
    paths,omitted=selected(root)
    if not set(recorded['files']).issubset({p.as_posix() for p in paths}):raise RuntimeError('Publication would omit required runtime inputs')
    git=['git']
    if remote.startswith('https://github.com/') and shutil.which('gh'):
        git+=['-c','credential.helper=','-c','credential.https://github.com.helper=!gh auth git-credential']
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    if (root/'.git-publish').is_symlink():raise RuntimeError('Publication directory must not be a symlink')
    checkout=root/'.git-publish'/stamp/'checkout';checkout.parent.mkdir(parents=True)
    run(git+['clone','--no-tags','--single-branch',remote,str(checkout)])
    def local(*args,check=True):return run(['git',*args],cwd=checkout,check=check)
    tracked=[os.fsdecode(x) for x in local('ls-files','-z').stdout.split(b'\0') if x]
    # A repository cleanup must not roll back science updated after the supplied ZIP.
    for name,expected in recorded['files'].items():
        target=checkout/name
        if target.is_file() and not target.is_symlink() and sha(target.read_bytes())!=expected:
            raise RuntimeError('Remote required runtime/input differs from the supplied scientific snapshot: '+name+'; refusing a scientific rollback')
    preserved=set()
    for name in tracked:
        path=Path(name);target=checkout/path
        if path.parts[0] in {'results','research_basis'} and target.is_file() and not target.is_symlink() and policy(path,target.stat().st_size) is None:
            preserved.add(name)
    wanted={p.as_posix() for p in paths}|preserved|{'GITHUB_LIGHT_ARTIFACTS.json'}
    removed=[x for x in tracked if x not in wanted]
    if removed:
        pathfile=checkout.parent/'removed.paths';pathfile.write_bytes(b'\0'.join(os.fsencode(x) for x in removed)+b'\0')
        local('--literal-pathspecs','rm','-f','--ignore-unmatch','--pathspec-from-file='+str(pathfile),'--pathspec-file-nul')
    records=[]
    for rel in paths:
        src=root/rel;data=src.read_bytes()
        if rel.as_posix() in preserved:data=(checkout/rel).read_bytes()
        if policy(rel,len(data)):raise RuntimeError('File changed outside publication policy: '+rel.as_posix())
        if any(pattern.search(data) for pattern in KEYS):raise RuntimeError('Possible credential in '+rel.as_posix()+'; value not printed')
        expected=recorded['files'].get(rel.as_posix())
        if expected and sha(data)!=expected:raise RuntimeError('Required source changed while snapshotting: '+rel.as_posix())
        dst=checkout/rel
        parent=checkout
        for part in rel.parts[:-1]:
            parent=parent/part
            if parent.is_symlink():raise RuntimeError('Refusing cloned symlink parent: '+rel.as_posix())
        if dst.is_symlink():dst.unlink()
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
        dst.chmod(0o755 if src.stat().st_mode&0o111 else 0o644)
        records.append(dict(path=rel.as_posix(),bytes=len(data),sha256=sha(data)))
    for name in sorted(preserved-{p.as_posix() for p in paths}):
        data=(checkout/name).read_bytes()
        if any(pattern.search(data) for pattern in KEYS):raise RuntimeError('Possible credential in existing evidence '+name+'; value not printed')
        records.append(dict(path=name,bytes=len(data),sha256=sha(data)))
    if sum(x['bytes'] for x in records)>TOTAL_LIMIT:raise RuntimeError('Actual snapshot exceeds512MiB')
    index=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Complete cleaned source, retained research foundation and light artifacts; root README only plus legal/dependency metadata.',files=records,selected_files=len(records),selected_bytes=sum(x['bytes'] for x in records),excluded_entry_counts=dict(omitted),removed_previous_remote_paths=removed,preserved_existing_remote_evidence=len(preserved),limits=dict(source_file_bytes=SOURCE_LIMIT,output_file_bytes=OUTPUT_LIMIT,total_bytes=TOTAL_LIMIT),active_run_note='Supplied clean source plus existing eligible remote evidence. Existing remote result/foundation files win conflicts and remote-only evidence is retained, preventing cleanup from rolling back later records. Not live attestation; no original running directory was modified.',raw_evidence_note='Full raw traces/archives, weights and environments are excluded. Keep original lossless archives separately.')
    index_path=checkout/'GITHUB_LIGHT_ARTIFACTS.json'
    if index_path.is_symlink():index_path.unlink()
    index_path.write_text(json.dumps(index,indent=2)+'\n')
    pathfile=checkout.parent/'selected.paths';pathfile.write_bytes(b'\0'.join(os.fsencode(x) for x in sorted(wanted))+b'\0')
    local('--literal-pathspecs','add','-f','--pathspec-from-file='+str(pathfile),'--pathspec-file-nul')
    if local('diff','--cached','--quiet',check=False).returncode not in (0,1):raise RuntimeError('Cannot inspect staged snapshot')
    print('Prepared clean checkout:',checkout,flush=True)
    print(f'Files: {len(records)}; {sum(x["bytes"] for x in records)/2**20:.1f}MiB; obsolete remote paths removed from this checkout: {len(removed)}',flush=True)
    if stage_only:
        print('STAGE_ONLY: no commit or push. Inspect the prepared checkout.',flush=True);return checkout
    for field in ['user.name','user.email']:
        if not local('config',field,check=False).stdout.strip():
            if not shutil.which('gh'):raise RuntimeError('Configure Git '+field+' before publishing; prepared checkout preserved')
            user=json.loads(run(['gh','api','user']).stdout)
            value=user['login'] if field=='user.name' else str(user['id'])+'+'+user['login']+'@users.noreply.github.com'
            local('config','--local',field,value)
    if local('rev-parse','--verify','HEAD',check=False).returncode:local('symbolic-ref','HEAD','refs/heads/main')
    local('commit','-m','Reconcile IEEE S&P repository and archive historical entrypoints')
    branch=local('symbolic-ref','--short','HEAD').stdout.decode().strip()
    value=run(git+['-C',str(checkout),'push','--set-upstream','origin',branch])
    print(value.stdout.decode(errors='replace')+value.stderr.decode(errors='replace'),flush=True)
    print('PUSH COMPLETE:',local('rev-parse','HEAD').stdout.decode().strip(),flush=True)
    print('Existing remote history preserved. Original experiment directory, environments, GPU processes and raw results untouched.',flush=True)
    return checkout

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--remote',default='https://github.com/TanzimAhad7/Usenix2027_cycle1.git')
    parser.add_argument('--stage-only',action='store_true')
    args=parser.parse_args()
    publish(Path(__file__).resolve().parents[1],args.remote,args.stage_only)

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('PUBLISH STOPPED:',str(exc),file=sys.stderr,flush=True)
        print('Prepared files are retained. No force push or original-run mutation was performed.',file=sys.stderr,flush=True)
        raise SystemExit(1)
