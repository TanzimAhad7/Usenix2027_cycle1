from __future__ import annotations
import argparse,fcntl,hashlib,importlib.metadata,json,os,re,shutil,signal,subprocess,sys,tarfile,threading,time,traceback
from pathlib import Path
from reference_study.common import ROOT,GPU_INDEX,GPU_UUID,LOCK_NAME,read,write,sha,verify_package,activate
from diagnostic.design import manifest
from diagnostic.report import analyze

class StopRequested(BaseException):pass

def archive(out):
    files=sorted(p for p in out.rglob('*')if p.is_file()and p.name!='SHA256SUMS')
    (out/'SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(out))+'\n'for p in files))
    target=Path(str(out)+'.tar.gz');temp=Path(str(target)+'.partial')
    with tarfile.open(temp,'w:gz',compresslevel=1)as f:f.add(out,arcname=out.name)
    temp.replace(target);Path(str(target)+'.sha256').write_text(sha(target)+'  '+target.name+'\n')
    review=Path(str(out)+'.review.tar.gz')
    with tarfile.open(review,'w:gz',compresslevel=1)as f:
        for rel in('status.json','FROZEN_MANIFEST.json','analysis','cpu_qualification/qualification.json','cpu_qualification/skip/result.json','preflight','environment.json','SEMANTIC_REVIEW_STATUS.json'):
            p=out/rel
            if p.exists():f.add(p,arcname=out.name+'/'+rel)
    return target,review

def cached_revision(cache,hub):
    folder=cache/('models--'+hub.replace('/','--'));ref=folder/'refs/main'
    if ref.is_file():
        value=ref.read_text().strip()
        if re.fullmatch('[0-9a-f]{40}',value)and(folder/'snapshots'/value/'config.json').is_file():return value
    hits=[p.name for p in(folder/'snapshots').glob('*')if(p/'config.json').is_file()and re.fullmatch('[0-9a-f]{40}',p.name)]
    return hits[0]if len(hits)==1 else None

def main(a):
    if sys.prefix==sys.base_prefix:raise RuntimeError('Run through isolated project .venv')
    project=a.project_root.resolve();out=project/'results/user_runs'/a.run_id;logs=project/'logs';logs.mkdir(parents=True,exist_ok=True)
    if a.lock_fd is None or os.fstat(a.lock_fd).st_ino!=(logs/LOCK_NAME).stat().st_ino:raise RuntimeError('Authenticated inherited GPU3 project lock missing')
    fcntl.flock(a.lock_fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if a.frozen_snapshot:
        if ROOT.resolve()!=a.frozen_snapshot.resolve()or ROOT.resolve()!=(out/'source').resolve():raise RuntimeError('Frozen source identity mismatch')
    else:
        out.mkdir(parents=True,exist_ok=False);identity=verify_package();source=out/'source';source.mkdir()
        for rel in identity['files']:
            dst=source/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,dst)
        shutil.copyfile(ROOT/'PACKAGE_MANIFEST.json',source/'PACKAGE_MANIFEST.json')
        os.set_inheritable(a.lock_fd,True)
        cmd=[sys.executable,'-u','-m','diagnostic.controller',*sys.argv[1:],'--frozen-snapshot',str(source)]
        os.chdir(source);os.execve(sys.executable,cmd,dict(os.environ))
    verify_package();status=dict(status='STARTING',run_id=a.run_id,started_epoch=time.time(),physical_gpu=GPU_INDEX,gpu_uuid=GPU_UUID,
        mode='CPU_ONLY'if a.cpu_only else'MOCK_ZERO_INFERENCE'if a.mock else'LIVE_CONDITIONAL_DIAGNOSTIC',profiles={},semantic_review='PENDING',autonomous_episodes=0)
    active=None;rc=0;archives=[];beat_stop=threading.Event()
    def update(**kw):status.update(kw);write(out/'status.json',status)
    def beat():
        while not beat_stop.wait(20):print('CONTROLLER',status['status'],status.get('active_profile'),'elapsed',int(time.time()-status['started_epoch']),'s',flush=True)
    thread=threading.Thread(target=beat,daemon=True);thread.start()
    signal.signal(signal.SIGTERM,lambda *_:(_ for _ in()).throw(StopRequested('Stop requested')))
    m=manifest(a.draws);write(out/'FROZEN_MANIFEST.json',m)
    env={**os.environ,'CUDA_VISIBLE_DEVICES':'','PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1'}
    env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    write(out/'SEMANTIC_REVIEW_STATUS.json',dict(status='PENDING_NOT_HUMAN_REVIEWED',packets='source/review_packets',automated_qualification_is_not_adjudication=True))
    try:
        write(out/'environment.json',dict(python=sys.version,executable=sys.executable,serving_python=str(a.serving_python),cache=str(a.cache),
            dependency_versions={n:importlib.metadata.version(n)for n in('agentdojo','openai','pydantic','httpx','tenacity')},source_manifest_hash=sha(ROOT/'PACKAGE_MANIFEST.json'),draws=a.draws,workers=a.workers))
        update(status='CPU_QUALIFICATION')
        with(out/'cpu_qualification_process.log').open('w')as f:
            q=subprocess.run([sys.executable,'-m','diagnostic.qualification','--out',str(out/'cpu_qualification')],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=600)
        if q.returncode:raise RuntimeError('CPU qualification failed; inspect cpu_qualification_process.log. No GPU was started.')
        print('CPU SOURCE/NATIVE CHECKS PASS',flush=True)
        if not a.cpu_only:
            if not a.mock:
                check=subprocess.run([str(a.serving_python),'-c','import sys,torch,vllm,json;print(json.dumps(dict(venv=sys.prefix!=sys.base_prefix,torch=torch.__version__,vllm=vllm.__version__)))'],env=env,capture_output=True,text=True,timeout=120)
                (out/'serving_versions.log').write_text(check.stdout+check.stderr);check.check_returncode();version=json.loads(check.stdout.strip().splitlines()[-1]);write(out/'serving_versions.json',version)
                if not version['venv']or version['vllm']!='0.26.0'or not version['torch'].startswith('2.11.0'):raise RuntimeError('Expected isolated vLLM0.26.0 / torch2.11.0')
            variants=[('qwen_native','qwen',None),('gemma27_recorded','gemma',None)]
            revision=cached_revision(a.cache,'google/gemma-3-12b-it')if not a.mock else'0'*40
            if a.no_gemma12:status['profiles']['gemma12_sensitivity']='NOT_REQUESTED'
            elif revision:variants.append(('gemma12_sensitivity','gemma',revision))
            else:status['profiles']['gemma12_sensitivity']='NOT_EXECUTED_CACHE_ABSENT_OR_AMBIGUOUS'
            for variant,family,revision in variants:
                child={**env,'DIAG_VARIANT':variant}
                if revision:child['DIAG_MODEL_REVISION']=revision
                update(status='PREFLIGHT',active_profile=variant)
                if not a.mock:
                    activate('qwen');from reference_discovery_parallel.base import serving
                    # Select configuration in a fresh process to avoid family imports.
                    from reference_discovery_parallel.models import PROFILES
                    from permission_admission.completion_models import PROFILE
                    p=PROFILES['qwen']if family=='qwen'else dict(PROFILE)
                    if revision:p.update(hub='google/gemma-3-12b-it',revision=revision)
                    try:
                        snapshot,identity=serving.inspect_snapshot(a.cache/('models--'+p['hub'].replace('/','--')),p['hub'],p['revision']);folder=out/'preflight'/variant;folder.mkdir(parents=True);write(folder/'snapshot_identity.json',identity)
                        with(folder/'rendering.log').open('w')as f:
                            result=subprocess.run([str(a.serving_python),'-m','diagnostic.models','--snapshot',str(snapshot),'--family',family,'--out',str(folder/'rendering')],cwd=ROOT,env=child,stdout=f,stderr=subprocess.STDOUT,timeout=600)
                        if result.returncode:raise RuntimeError('Rendering qualification failed')
                    except Exception as e:
                        status['profiles'][variant]='PREFLIGHT_FAILED';write(out/'preflight'/variant/'error.json',dict(error=str(e),traceback=traceback.format_exc()));rc=1;continue
                update(status='RUNNING',active_profile=variant)
                cmd=[sys.executable,'-u','-m','reference_study.profile','--family',family,'--out',str(out/variant),'--manifest',str(out/'FROZEN_MANIFEST.json'),
                    '--project-root',str(project),'--serving-python',str(a.serving_python),'--cache',str(a.cache),'--lock-fd',str(a.lock_fd),'--workers',str(a.workers)]
                if a.mock:cmd.append('--mock')
                active=subprocess.Popen(cmd,cwd=ROOT,env=child,pass_fds=(a.lock_fd,));write(out/(variant+'_process.json'),dict(pid=active.pid,argv=cmd))
                while active.poll()is None:time.sleep(.1 if a.mock else 1)
                status['profiles'][variant]=active.returncode
                if active.returncode:rc=1
                profile=read(out/variant/'status.json')
                if profile.get('status')=='OWNED_CLEANUP_FAILED':raise RuntimeError('Owned cleanup failed; next model is not started')
                print('STAGE FINISHED',variant,'; preserving complete partial/full archive',flush=True)
                # Archive complete diagnostics after each profile, while nothing writes to its cells.
                update(status='PROFILE_COMPLETE',active_profile=None);analyze(out,m);archive(out)
        update(status='CPU_COMPLETE_ZERO_INFERENCE'if a.cpu_only else'MOCK_COMPLETE_ZERO_INFERENCE'if a.mock else'COMPLETE_CONDITIONAL_DIAGNOSTIC_REVIEW_PENDING',active_profile=None)
    except BaseException as e:
        rc=1;update(status='INTERRUPTED'if isinstance(e,(StopRequested,KeyboardInterrupt))else'FAILED',error=str(e));write(out/'fatal_error.json',dict(type=type(e).__name__,error=str(e),traceback=traceback.format_exc()));print('STOP',str(e),flush=True)
    finally:
        if active and active.poll()is None:
            active.terminate()
            try:active.wait(timeout=180)
            except subprocess.TimeoutExpired:
                # Do not kill the profile controller and abandon its GPU children.
                update(status='CLEANUP_PENDING',cleanup='Profile still owns its recorded workers; inspect process/ownership records. No next profile launched.');rc=1
        try:
            counts=analyze(out,m)
            for profile,state in status['profiles'].items():
                if isinstance(state,int)and counts[profile]['qualified']<counts[profile]['scheduled']:rc=1
            if rc and status['status']in('COMPLETE_CONDITIONAL_DIAGNOSTIC_REVIEW_PENDING','MOCK_COMPLETE_ZERO_INFERENCE'):update(status='COMPLETE_WITH_TECHNICAL_ISSUES')
        except Exception as e:rc=1;write(out/'analysis_error.json',dict(error=str(e),traceback=traceback.format_exc()))
        update(finished_epoch=time.time(),exit_code=rc)
        logfile=logs/(a.run_id+'.log')
        if logfile.exists():shutil.copyfile(logfile,out/'controller.log')
        try:
            raw,review=archive(out);print('RAW ARCHIVE:',raw,flush=True);print('REVIEW ARCHIVE:',review,flush=True)
        except Exception as e:rc=1;write(out/'archive_error.json',dict(error=str(e)))
        (logs/(a.run_id+'.status')).write_text('exit_code='+str(rc)+'\nstatus='+status['status']+'\nresults='+str(out)+'\n')
        beat_stop.set();thread.join(timeout=1)
    return rc

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--project-root',required=True,type=Path);p.add_argument('--run-id',required=True);p.add_argument('--serving-python',required=True,type=Path);p.add_argument('--cache',required=True,type=Path);p.add_argument('--lock-fd',required=True,type=int);p.add_argument('--frozen-snapshot',type=Path);p.add_argument('--draws',type=int,default=1);p.add_argument('--workers',type=int,choices=(1,2,3,4),default=4);g=p.add_mutually_exclusive_group();g.add_argument('--cpu-only',action='store_true');g.add_argument('--mock',action='store_true');p.add_argument('--no-gemma12',action='store_true');a=p.parse_args()
    if not re.fullmatch('[A-Za-z0-9_-]+',a.run_id):p.error('Unsafe run ID')
    if not 1<=a.draws<=10:p.error('draws must be 1..10; repetition is exploratory, not confirmation')
    a.project_root=a.project_root.absolute();a.cache=a.cache.expanduser().absolute();a.serving_python=a.serving_python.absolute();raise SystemExit(main(a))
