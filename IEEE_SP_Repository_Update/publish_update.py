"""Publish the bundled project transition through a separate, normal Git clone."""
from pathlib import Path, PurePosixPath
import argparse, datetime, fcntl, hashlib, json, os, re, shutil, stat, subprocess, sys, time

DEFAULT_REMOTE='https://github.com/TanzimAhad7/Usenix2027_cycle1.git'
RAW_DIRS={'source','retained','vendor','fixtures','checkpoints','origins','http','requests','model_io','raw','token_diagnostics','episode_workers','workers','job_inputs','native','snapshots','serving','initial_world','final_world','__pycache__'}
RAW_NAMES={'FROZEN_MANIFEST.json','messages.json','events.json','driver_records.json','initial_world.json','final_world.json','before.json','after.json','parent_checkpoint.json'}
SECRET=[re.compile(rb'gh[pousr]_[A-Za-z0-9]{36,}'),re.compile(rb'github_pat_[A-Za-z0-9_]{30,}'),re.compile(rb'sk-(?:proj-|ant-)?[A-Za-z0-9_-]{24,}'),re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]

def digest(data):return hashlib.sha256(data).hexdigest()

def run(args,cwd=None,check=True):
    p=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if check and p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace')[-2500:] or 'Command failed: '+args[0])
    return p

def safe_path(name):
    p=PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or not p.parts:raise ValueError('Unsafe publication path')
    return p

def stable_bytes(path):
    if path.is_symlink():return None
    for _ in range(3):
        try:
            with path.open('rb') as f:
                before=os.fstat(f.fileno())
                if not stat.S_ISREG(before.st_mode) or before.st_size>2*1024**2:return None
                data=f.read(2*1024**2+1);after=os.fstat(f.fileno())
            now=path.stat()
            identity=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)
            if identity(before)==identity(after)==identity(now) and len(data)<=2*1024**2:
                if path.suffix=='.json':json.loads(data)
                return data
        except (OSError,ValueError):pass
        time.sleep(.05)
    return None

def live_files(project):
    base=project/'results/user_runs'
    if base.is_symlink():raise ValueError('Result base may not be a symlink')
    for directory in sorted(base.glob('reference_study_gpu2_*')):
        if not directory.is_dir() or directory.is_symlink():continue
        for current,dirs,files in os.walk(directory,followlinks=False):
            here=Path(current)
            dirs[:]=sorted(d for d in dirs if d not in RAW_DIRS and not d.startswith('.') and not (here/d).is_symlink())
            for name in sorted(files):
                p=here/name
                if p.suffix.lower() not in {'.json','.csv','.tsv','.status','.sha256'} or name in RAW_NAMES or name.startswith(('.','batch_')):continue
                if any(x in name.lower() for x in ['checkpoint','world_before','world_after','.request.','.response.','.transport.','.tokens.']):continue
                rel=p.relative_to(directory)
                if name not in {'result.json','item.json','final_reporting.json','status.json','census.json','fatal_error.json','execution_environment.json','serving_versions.json','PREDICTIONS_BEFORE_P3.json'} and rel.parts[0] not in {'analysis','template_qualification','live_qualification','cpu_qualification'}:continue
                data=stable_bytes(p)
                if data is not None:yield p.relative_to(project).as_posix(),data

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-root',type=Path,default=Path.cwd())
    ap.add_argument('--remote');ap.add_argument('--branch')
    ap.add_argument('--stage-only',action='store_true')
    ap.add_argument('--skip-live-results',action='store_true')
    a=ap.parse_args(argv)
    bundle=Path(__file__).resolve().parent
    payload=bundle/'payload';project=a.project_root.resolve()
    # Validate all bundled inputs before any clone or staging.
    sys.path.insert(0,str(payload/'scripts'))
    from verify_current_update import verify
    verify(payload)
    manifest=json.loads((payload/'provenance/PROJECT_UPDATE_MANIFEST.json').read_text())
    baseline=json.loads((bundle/'BASELINE_HASHES.json').read_text())
    connected=run(['git','-C',str(project),'rev-parse','--git-dir'],check=False).returncode==0
    remote=a.remote
    if not remote and connected:remote=run(['git','-C',str(project),'remote','get-url','--push','origin'],check=False).stdout.decode().strip()
    remote=remote or DEFAULT_REMOTE
    if re.search(r'https?://[^/]*@',remote):raise ValueError('Use a credential-free remote URL')
    branch=a.branch
    if not branch and connected:
        up=run(['git','-C',str(project),'rev-parse','--abbrev-ref','--symbolic-full-name','@{upstream}'],check=False).stdout.decode().strip()
        if up.startswith('origin/'):branch=up[len('origin/'):]
    if branch:run(['git','check-ref-format','--branch',branch])
    logs=project/'logs'
    if logs.is_symlink():raise ValueError('Logs directory may not be a symlink')
    logs.mkdir(exist_ok=True)
    lock=(logs/'ieee_sp_repository_update.lock').open('a')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    ident='repository_update_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+str(os.getpid())
    work=logs/ident;work.mkdir()
    checkout=work/'checkout'
    transport=['git']
    if remote.startswith('https://github.com/') and shutil.which('gh'):
        transport+=['-c','credential.helper=','-c','credential.https://github.com.helper=!gh auth git-credential']
    run(transport+['clone','--single-branch','--no-tags']+(['--branch',branch] if branch else [])+[remote,str(checkout)])
    def git(*args,check=True):return run(['git','-C',str(checkout),*args],check=check)
    branch=git('symbolic-ref','--short','HEAD').stdout.decode().strip()
    base=git('rev-parse','HEAD').stdout.decode().strip()
    selected={n:((payload/n).read_bytes(),rec['mode'],'bundled') for n,rec in manifest['files'].items()}
    selected['provenance/PROJECT_UPDATE_MANIFEST.json']=((payload/'provenance/PROJECT_UPDATE_MANIFEST.json').read_bytes(),0o644,'bundled')
    live_count=0
    if not a.skip_live_results:
        for name,data in live_files(project):
            if name in selected:raise ValueError('Live result conflicts with immutable historical bundle')
            selected[name]=(data,0o644,'live_per_file_snapshot');live_count+=1
    total=0;changed=[];receipt=[]
    for name,(data,mode,kind) in selected.items():
        safe_path(name)
        if any(p.search(data) for p in SECRET):raise ValueError('Possible credential in '+name+'; no value displayed')
        total+=len(data)
        if total>256*1024**2:raise ValueError('Publication exceeds 256 MiB')
        dst=checkout/name
        if any(p.is_symlink() for p in [dst,*dst.parents]):raise ValueError('Symlink destination: '+name)
        if dst.is_file():
            old=dst.read_bytes()
            if old==data:continue
            # Never overwrite remote changes to source, imported evidence or navigation.
            if kind=='bundled' and digest(old)!=baseline.get(name):
                raise ValueError('Remote content differs from both baseline and bundle: '+name+'; update stopped without a commit')
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data);dst.chmod(mode)
        changed.append(name);receipt.append(dict(path=name,sha256=digest(data),bytes=len(data),kind=kind))
    # Verify the actual exported checkout, with original statuses and manifests.
    verify(checkout)
    for p in checkout.glob('*.sh'):
        if p.name in {'RUN_CURRENT_EXPERIMENT.sh','SHOW_CURRENT_EXPERIMENT.sh','PROJECT_STATUS.sh','VERIFY_PROJECT.sh'}:run(['bash','-n',str(p)])
    print('CHECKOUT:',checkout,flush=True)
    print('SELECTED:',len(selected),'files;',total,'bytes; CHANGED:',len(changed),'; CURRENT LIVE FILES:',live_count,flush=True)
    if not changed:print('ALREADY UP TO DATE; no commit or push.');return
    receipt_name='provenance/github_updates/'+ident+'.json'
    rec=checkout/receipt_name
    if any(p.is_symlink() for p in [rec,*rec.parents]):raise ValueError('Symlink in publication receipt path')
    rec.parent.mkdir(parents=True,exist_ok=True)
    rec.write_text(json.dumps(dict(base_commit=base,branch=branch,files=receipt,live_result_files=live_count,live_snapshot='Stable individual files; not an atomic campaign snapshot or completion certificate',policy='Normal push, no deletions, no raw archives or research reports'),indent=2)+'\n')
    paths=work/'selected.paths';paths.write_bytes(b'\0'.join(os.fsencode(n) for n in [*changed,receipt_name])+b'\0')
    git('--literal-pathspecs','add','-f','--pathspec-from-file='+str(paths),'--pathspec-file-nul')
    staged=set(x.decode() for x in git('diff','--cached','--name-only','-z').stdout.split(b'\0') if x)
    if staged!=set(changed+[receipt_name]):raise ValueError('Staged file list differs from selection')
    if git('diff','--cached','--diff-filter=D','--name-only').stdout:raise ValueError('Deletion detected')
    if a.stage_only:print('STAGE_ONLY: ready for inspection; no commit or push.');return
    for field in ['user.name','user.email']:
        value=run(['git','-C',str(project),'config',field],check=False).stdout.decode().strip() if connected else ''
        if value:git('config','--local',field,value)
        if not git('config',field,check=False).stdout.strip():
            if not shutil.which('gh'):raise ValueError('Configure Git '+field+' or authenticate gh; no push made')
            user=json.loads(run(['gh','api','user']).stdout)
            value=user['login'] if field=='user.name' else str(user['id'])+'+'+user['login']+'@users.noreply.github.com'
            git('config','--local',field,value)
    git('commit','-m','Add permission panels, Gemma completion and current P0-P3 experiment')
    p=run(transport+['-C',str(checkout),'push','origin','HEAD:refs/heads/'+branch])
    print(p.stdout.decode()+p.stderr.decode(),flush=True)
    print('PUSH COMPLETE:',git('rev-parse','HEAD').stdout.decode().strip(),flush=True)
    print('Live project source, Git checkout, GPU processes and running collection were not changed.')

if __name__=='__main__':
    try:main()
    except Exception as e:print('UPDATE STOPPED:',e,file=sys.stderr,flush=True);sys.exit(1)
