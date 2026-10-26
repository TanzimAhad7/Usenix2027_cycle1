#!/usr/bin/env bash
# Run from the project directory. No Python packages are installed.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
mkdir -p logs
if [[ "${1:-}" != "--worker" ]]; then
  command -v git >/dev/null || { echo 'git is required.'; exit 1; }
  [[ -x "$ROOT/.venv/bin/python" ]] || { echo 'Missing .venv/bin/python'; exit 1; }
  stage_only=false
  for arg in "$@"; do [[ "$arg" != "--stage-only" ]] || stage_only=true; done
  if [[ "$stage_only" == false ]] && ! git remote get-url origin >/dev/null 2>&1; then
    command -v gh >/dev/null || { echo 'No origin configured. Install GitHub CLI (gh), run gh auth login, then rerun. Alternatively configure your existing GitHub origin first.'; exit 1; }
    gh auth status >/dev/null 2>&1 || { echo 'Run gh auth login once, then rerun this script.'; exit 1; }
  fi
  run_id="github_light_$(date -u +%Y%m%dT%H%M%SZ)_$$_${RANDOM}"
  log="$ROOT/logs/$run_id.log"
  nohup bash "$ROOT/PUSH_LIGHT_TO_GITHUB.sh" --worker "$run_id" "$@" > "$log" 2>&1 < /dev/null &
  pid=$!
  echo "$pid" > "$log.pid"
  echo "PID: $pid"
  echo "Log: $log"
  echo "Status: $ROOT/logs/$run_id.status"
  echo "Progress: tail -f '$log'"
  exit 0
fi
shift
run_id="$1"; shift
[[ "$run_id" =~ ^[A-Za-z0-9_-]+$ ]] || { echo 'Invalid run ID'; exit 1; }
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONUNBUFFERED=1 GIT_TERMINAL_PROMPT=0
unset PYTHONPATH PYTHONHOME
trap 'rc=$?; printf "exit_code=%s\nfinished_utc=%s\n" "$rc" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "logs/$run_id.status"' EXIT
"$ROOT/.venv/bin/python" -u - "$@" <<'PY'
import argparse,collections,datetime,fcntl,hashlib,json,os,re,stat,subprocess,sys,tempfile
from pathlib import Path

parser=argparse.ArgumentParser(description='Stage, commit and push code + lightweight evidence; no raw archives.')
parser.add_argument('--repo',help='OWNER/NAME for a new private repository; default: authenticated user/IEEE_SP_2027')
parser.add_argument('--stage-only',action='store_true',help='Prepare and stage only; do not commit, create a remote or push')
args=parser.parse_args();root=Path.cwd()
SOURCE_LIMIT=10*1024*1024
OUTPUT_LIMIT=2*1024*1024
TOTAL_LIMIT=512*1024*1024
MANIFEST='GITHUB_LIGHT_ARTIFACTS.json'
SKIP_DIRS={'.git','.tools','.cache','.hf_cache','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','node_modules','wandb'}
RAW_DIRS={'source','sources','fixtures','checkpoints','eligible','matched_origins','http','requests','model_io','raw','token_diagnostics','episode_workers'}
ARCHIVES=('.zip','.gz','.bz2','.xz','.zst','.7z','.tar','.tgz','.pt','.pth','.safetensors','.ckpt','.onnx','.gguf','.bin','.npy','.npz','.pkl','.pickle','.pyc','.pyo','.so','.dll','.dylib')
RAW_NAMES={'messages.json','events.jsonl','driver_records.json','initial_world.json','final_world.json','parent_checkpoint.json','executed_guard.py','native.log','diagnostic.log','server.log','controller.log'}
LIGHT_SUFFIXES={'.json','.csv','.tsv','.md','.txt','.sha256','.svg','.png','.pdf','.log','.status','.jinja'}
KEYS=[re.compile(rb'gh[pousr]_[A-Za-z0-9]{36,}'),re.compile(rb'github_pat_[A-Za-z0-9_]{30,}'),
      re.compile(rb'sk-(?:proj-|ant-)?[A-Za-z0-9_-]{24,}'),re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\r\n]+(?:[A-Za-z0-9+/=]{40,}[\r\n]+)')]

def run(*argv,check=True,input=None):
    p=subprocess.run(list(argv),input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if check and p.returncode:
        # Git/gh normally redact authentication; credential values are never supplied in argv here.
        raise RuntimeError('Command failed: '+argv[0]+' '+argv[1]+'\n'+p.stderr.decode(errors='replace'))
    return p
def git(*argv,**kwargs):return run('git',*argv,**kwargs)
def excluded_dir(name):return name in SKIP_DIRS or name.startswith(('.venv','venv.backup'))
def policy(path,size):
    parts=path.parts;name=path.name;low=name.lower()
    if any(excluded_dir(x) for x in parts[:-1]):return 'environment_or_cache'
    if low.endswith(ARCHIVES) or low.endswith(('.tmp','.partial')) or (low.endswith('.lock') and low not in {'uv.lock','poetry.lock','pipfile.lock','requirements.lock'}):return 'archive_binary_or_temporary'
    if (low=='.env' or (low.startswith('.env.') and low not in {'.env.example','.env.sample','.env.template'})
        or low.endswith(('.pem','.key','.p12','.pfx')) or low in {'id_rsa','id_ed25519','.netrc','.git-credentials'}
        or re.match(r'^(credentials|secrets|service.account).*\.json$',low)):
        return 'credential_file'
    if parts[0]=='logs':return 'live_logs'
    if parts[0]=='results':
        if any(x in RAW_DIRS for x in parts[1:-1]):return 'duplicate_source_or_raw_output'
        if (low in RAW_NAMES or any(t in low for t in ('.request.','.response.','.tokens.','.transport.','.reused.','policy_records','checkpoint','before_world','after_world'))
            or low.startswith('batch_') or low.endswith('.jsonl')):return 'raw_trace_or_state'
        if low!='sha256sums' and path.suffix.lower() not in LIGHT_SUFFIXES:return 'not_light_output_type'
        return 'output_over_2MiB' if size>OUTPUT_LIMIT else None
    if size>SOURCE_LIMIT:return 'source_or_artifact_over_10MiB'
    return None

def main():
    # No experiment lock, process signal, runtime import or scientific-file modification.
    if not (root/'.git').exists():git('init','-b','main')
    top=Path(git('rev-parse','--show-toplevel').stdout.decode().strip()).resolve()
    if top!=root:raise RuntimeError('This folder must be its own repository; refusing to stage a parent repository.')
    gitdir=Path(git('rev-parse','--absolute-git-dir').stdout.decode().strip())
    lock=(gitdir/'github-light-upload.lock').open('a')
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise RuntimeError('Another lightweight upload is active.')
    if git('diff','--cached','--quiet',check=False).returncode:
        raise RuntimeError('There are already staged changes. Inspect git status and commit or unstage them before running; existing staging was left untouched.')
    # Keep frozen .gitignore/package bytes unchanged. These local exclusions protect later git add .
    excludes=Path(git('rev-parse','--git-path','info/exclude').stdout.decode().strip())
    excludes.parent.mkdir(parents=True,exist_ok=True)
    block='\n# Lightweight IEEE S&P uploads; exact files staged by PUSH_LIGHT_TO_GITHUB.sh\n/.venv*/\n/.tools/\n/logs/\n/results/\n**/__pycache__/\n*.zip\n*.tar.gz\n*.safetensors\n*.pt\n*.pth\n.env\n.env.*\n'
    prior=excludes.read_text() if excludes.exists() else ''
    if '# Lightweight IEEE S&P uploads;' not in prior:excludes.write_text(prior+block)
    chosen=[];omitted=collections.Counter();examples=collections.defaultdict(list);total=0
    def omit(path,reason):
        omitted[reason]+=1
        if len(examples[reason])<20:examples[reason].append(str(path))
    for current,dirs,files in os.walk(root,followlinks=False):
        rel=Path(current).relative_to(root)
        keep=[]
        for name in sorted(dirs):
            path=rel/name
            if excluded_dir(name) or (Path(current)/name).is_symlink():omit(path,'pruned_environment_cache_or_symlink_directory')
            elif path.parts[0]=='logs':omit(path,'pruned_live_log_directory')
            elif path.parts[0]=='results' and name in RAW_DIRS:omit(path,'pruned_duplicate_source_or_raw_directory')
            else:keep.append(name)
        dirs[:]=keep
        for name in sorted(files):
            path=rel/name;p=root/path
            try:info=p.lstat()
            except FileNotFoundError:omit(path,'vanished_during_collection');continue
            if not stat.S_ISREG(info.st_mode):omit(path,'symlink_or_special_file');continue
            if str(path)==MANIFEST:continue
            reason=policy(path,info.st_size)
            if reason:omit(path,reason)
            else:chosen.append(str(path));total+=info.st_size
    chosen.sort()
    if total>TOTAL_LIMIT:raise RuntimeError(f'Selected files total {total/2**20:.1f} MiB, exceeding the 512 MiB lightweight limit. No files staged. Review sizes before publishing.')
    tracked=[os.fsdecode(x) for x in git('ls-files','-z').stdout.split(b'\0') if x]
    allowed=set(chosen)|{MANIFEST}
    unsafe=[p for p in tracked if (root/p).exists() and p not in allowed]
    if unsafe:raise RuntimeError('Already tracked files fall outside the lightweight policy; no automatic history rewriting or removal. Inspect these paths: '+', '.join(unsafe[:20]))
    missing=[p for p in tracked if not (root/p).exists()]
    if not chosen:raise RuntimeError('No eligible files found.')
    paths=gitdir/'github-light-upload.paths'
    paths.write_bytes(b'\0'.join(os.fsencode(p) for p in chosen+missing)+b'\0')
    git('--literal-pathspecs','add','-f','--pathspec-from-file='+str(paths),'--pathspec-file-nul')
    # Inspect actual Git-index objects, not changing live result files. Hashes describe the commit snapshot.
    staged=[];index=git('ls-files','--stage','-z').stdout
    process=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for entry in index.split(b'\0'):
            if not entry:continue
            meta,path=entry.split(b'\t',1);mode,oid,stage=meta.split();name=os.fsdecode(path)
            if name==MANIFEST:continue
            if stage!=b'0' or mode not in (b'100644',b'100755'):raise RuntimeError('Unsupported index entry: '+name)
            process.stdin.write(oid+b'\n');process.stdin.flush()
            header=process.stdout.readline().split();size=int(header[2]);data=process.stdout.read(size)
            if len(data)!=size or process.stdout.read(1)!=b'\n':raise RuntimeError('Incomplete staged Git object: '+name)
            if any(pattern.search(data) for pattern in KEYS):raise RuntimeError('Possible credential in staged file '+name+'; upload stopped. Value not printed.')
            if policy(Path(name),size):raise RuntimeError('Staged object no longer satisfies size/type policy: '+name)
            staged.append(dict(path=name,bytes=size,git_object=oid.decode(),sha256=hashlib.sha256(data).hexdigest()))
    finally:
        process.stdin.close();process.wait()
    if sum(x['bytes'] for x in staged)>TOTAL_LIMIT:raise RuntimeError('Actual staged snapshot exceeds 512 MiB; upload stopped.')
    report=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Code, documentation, retained small fixtures and lightweight outputs; all outcome classes eligible.',
        selected_files=len(staged),selected_bytes=sum(x['bytes'] for x in staged),files=staged,
        excluded_entry_counts=dict(omitted),excluded_path_examples=dict(examples),
        limits=dict(source_file_bytes=SOURCE_LIMIT,output_file_bytes=OUTPUT_LIMIT,total_bytes=TOTAL_LIMIT),
        active_run_note='Point-in-time Git index snapshot, not an atomic snapshot of the whole experiment. A running run may be partial. Rerun after completion.',
        raw_evidence_note='Original local raw evidence and archives are unchanged. This remote is not the complete raw evidence backup. Exclusion counts for pruned directories count directories, not unseen files.')
    (root/MANIFEST).write_text(json.dumps(report,indent=2)+'\n')
    git('add','-f','--',MANIFEST)
    print(f'STAGED: {len(staged)} files + manifest; {report["selected_bytes"]/2**20:.1f} MiB',flush=True)
    print('Omitted entry categories:',json.dumps(dict(omitted),sort_keys=True),flush=True)
    print('Manifest:',MANIFEST,flush=True)
    if args.stage_only:
        print('STAGE_ONLY: no commit, remote creation or push.');return
    origin=git('remote','get-url','origin',check=False)
    if origin.returncode:
        user=json.loads(run('gh','api','user').stdout)
        repo=args.repo or user['login']+'/IEEE_SP_2027'
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo):raise RuntimeError('Expected --repo OWNER/NAME')
        existing=run('gh','repo','view',repo,'--json','nameWithOwner,visibility,url',check=False)
        if existing.returncode:
            run('gh','repo','create',repo,'--private','--description','Standalone IEEE S&P research: code and lightweight evidence')
        else:
            details=json.loads(existing.stdout)
            if details['visibility']!='PRIVATE':raise RuntimeError('Auto-selected repository already exists and is public. Configure an explicit origin if that is your intended target.')
        git('remote','add','origin','https://github.com/'+repo+'.git')
        origin=git('remote','get-url','origin')
    elif args.repo:
        raise RuntimeError('origin already exists. Use it by omitting --repo; the script never replaces an existing remote.')
    remote=origin.stdout.decode().strip()
    if re.search(r'https?://[^/]*@',remote):raise RuntimeError('Use a credential-free origin URL; do not embed a token in Git config.')
    print('Remote:',remote,flush=True)
    if not git('config','user.name',check=False).stdout.strip() or not git('config','user.email',check=False).stdout.strip():
        user=json.loads(run('gh','api','user').stdout)
        if not git('config','user.name',check=False).stdout.strip():git('config','--local','user.name',user['login'])
        if not git('config','user.email',check=False).stdout.strip():git('config','--local','user.email',str(user['id'])+'+'+user['login']+'@users.noreply.github.com')
    if git('rev-parse','--verify','HEAD',check=False).returncode:git('symbolic-ref','HEAD','refs/heads/main')
    branch=git('symbolic-ref','--short','HEAD').stdout.decode().strip()
    commit=git('commit','-m','Track IEEE S&P code and lightweight research evidence')
    print(commit.stdout.decode(errors='replace'),flush=True)
    argv=['git']
    # Use authenticated gh for HTTPS GitHub pushes without changing global credential config.
    if remote.startswith('https://github.com/') and run('which','gh',check=False).returncode==0:
        argv+=['-c','credential.helper=','-c','credential.https://github.com.helper=!gh auth git-credential']
    result=run(*argv,'push','--set-upstream','origin',branch)
    print(result.stdout.decode(errors='replace')+result.stderr.decode(errors='replace'),flush=True)
    print('PUSH COMPLETE:',git('rev-parse','HEAD').stdout.decode().strip(),flush=True)
    print('Running experiment and raw local files were not stopped or removed. Rerun this script after new results arrive.',flush=True)

try:main()
except Exception as exc:
    print('UPLOAD STOPPED:',str(exc),file=sys.stderr,flush=True)
    print('Any staged changes/commit remain available for inspection. No force push or history rewrite was used.',file=sys.stderr,flush=True)
    raise SystemExit(1)
PY
