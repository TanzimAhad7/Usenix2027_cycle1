"""Snapshot, qualify, serve Qwen then Gemma, analyze and archive every outcome."""
from __future__ import annotations
import argparse,fcntl,importlib.metadata,json,os,shutil,signal,subprocess,sys,tarfile,threading,time,traceback
from pathlib import Path
from .common import ROOT,GPU_INDEX,GPU_UUID,LOCK_NAME,read,write,sha,verify_package,activate
from .design import manifest
from .report import analyze

class StopRequested(BaseException):pass

def package(out):
    files=sorted(p for p in out.rglob('*')if p.is_file()and p!=out/'SHA256SUMS')
    (out/'SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(out))+'\n'for p in files))
    raw=Path(str(out)+'.tar.gz');partial=Path(str(raw)+'.partial')
    with tarfile.open(partial,'w:gz',compresslevel=1)as f:f.add(out,arcname=out.name)
    partial.replace(raw);Path(str(raw)+'.sha256').write_text(sha(raw)+'  '+raw.name+'\n')
    review=Path(str(out)+'.review.tar.gz')
    with tarfile.open(review,'w:gz',compresslevel=1)as f:
        for rel in('status.json','FROZEN_MANIFEST.json','analysis','cpu_qualification','execution_environment.json','preflight'):
            p=out/rel
            if p.exists():f.add(p,arcname=out.name+'/'+rel)
        for family in('qwen','gemma'):
            for rel in('status.json','census.json','schedule_events.jsonl','PREDICTIONS_BEFORE_P3.json','fatal_error.json','serving/command.json','serving/shutdown.json','serving/placement.json','serving/live_qualification/qualification.json'):
                p=out/family/rel
                if p.exists():f.add(p,arcname=out.name+'/'+family+'/'+rel)
    return raw,review

def main(a):
    if sys.prefix==sys.base_prefix:raise RuntimeError('Use the project .venv; RUN_STUDY.sh selects it explicitly')
    if sys.version_info<(3,11):raise RuntimeError('Python3.11+ required;3.12 tested')
    project=a.project_root.resolve();logs=project/'logs';logs.mkdir(parents=True,exist_ok=True)
    out=project/'results/user_runs'/a.run_id
    previous=None
    if a.frozen_snapshot is not None:
        if ROOT.resolve()!=a.frozen_snapshot.resolve()or ROOT.resolve()!=(out/'source').resolve():raise RuntimeError('Frozen controller identity mismatch')
        previous=read(out/'status.json')
        if previous['run_id']!=a.run_id or previous['status']!='STARTING':raise RuntimeError('Refusing a second execution of a recorded campaign')
    else:out.mkdir(parents=True,exist_ok=False)
    if a.lock_fd is not None:
        if os.fstat(a.lock_fd).st_ino!=(logs/LOCK_NAME).stat().st_ino:raise RuntimeError('Bootstrap lock identity mismatch')
        lock=os.fdopen(os.dup(a.lock_fd),'a')
    else:lock=(logs/LOCK_NAME).open('a')
    acquired=False;active=None;rc=0;raw=None;review=None
    m=manifest();write(out/'FROZEN_MANIFEST.json',m)
    catalog=[dict(root=b[0]['spec']['id'],purpose=b[0]['spec']['purpose'],semantic_job=b[0]['spec']['semantic_job'],
        family=b[0]['spec']['family'],structure=b[0]['spec']['structure'],shape=b[0]['spec']['shape'],
        contract=b[0]['spec']['choice_contract'],trusted_task=b[0]['spec']['root'],
        attack_targets=b[0]['spec']['attack_targets'])for b in m['P3_blocks']]
    write(out/'TASK_CATALOG.json',catalog)
    write(out/'SEMANTIC_REVIEW_TEMPLATE.json',dict(status='PENDING_NOT_HUMAN_REVIEWED',
        tasks=[dict(root=r['root'],reviewer_A=None,reviewer_B=None,policy_unambiguous=None,
            lawful_variations_valid=None,attacks_meaning_changing=None,notes=None)for r in catalog],
        scope='Unsigned template. Automated tests are not substituted for independent human adjudication.'))
    status=dict(status='STARTING',run_id=a.run_id,started_epoch=previous['started_epoch']if previous else time.time(),physical_gpu=GPU_INDEX,gpu_uuid=GPU_UUID,
        mode='CPU_ONLY'if a.cpu_only else'MOCK_ENGINEERING_ZERO_INFERENCE'if a.mock else'LIVE_EXPLORATORY_STUDY',
        profiles={},semantic_review='PENDING_INDEPENDENT_HUMAN_ADJUDICATION',principal_published_profile_reproduction=False)
    stopbeat=threading.Event()
    def update(**values):status.update(values);write(out/'status.json',status)
    def beat():
        while not stopbeat.wait(20):print(f'CONTROLLER status={status["status"]} profile={status.get("active_profile")} elapsed={int(time.time()-status["started_epoch"])}s results={out}',flush=True)
    thread=threading.Thread(target=beat,daemon=True);thread.start()
    def terminate_active():
        if active and active.poll()is None:
            active.terminate();end=time.monotonic()+150
            while active.poll()is None and time.monotonic()<end:time.sleep(.5)
            if active.poll()is None:
                # Only authenticated, previously recorded server identities may be signaled.
                activate('qwen');from reference_discovery_parallel.base import serving
                f=out/status.get('active_profile','')/'serving/owned_identities.json'
                identities=read(f)if f.is_file()else{}
                for pid,start in identities.items():
                    if start is not None and serving.proc_start(int(pid))==start:
                        try:os.kill(int(pid),signal.SIGTERM)
                        except ProcessLookupError:pass
                active.kill();active.wait();raise RuntimeError('Profile cleanup watchdog; inspect owned identities before another launch')
    signal.signal(signal.SIGTERM,lambda *_:(_ for _ in()).throw(StopRequested('SIGTERM')))
    try:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);acquired=True
        except BlockingIOError:update(status='BLOCKED_CONCURRENT_SEQUENCE');raise RuntimeError('Another campaign owns the GPU2 project lock; no process stopped')
        identity=verify_package()
        if a.frozen_snapshot is None:
            source=out/'source';source.mkdir()
            for rel in identity['files']:
                dst=source/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,dst)
            shutil.copyfile(ROOT/'PACKAGE_MANIFEST.json',source/'PACKAGE_MANIFEST.json')
            # Controller, later imports and workers all execute frozen code.
            os.set_inheritable(lock.fileno(),True)
            cmd=[sys.executable,'-u','-m','reference_study.controller','--project-root',str(project),'--run-id',a.run_id,
                '--serving-python',str(a.serving_python),'--cache',str(a.cache),'--workers',str(a.workers),
                '--lock-fd',str(lock.fileno()),'--frozen-snapshot',str(source)]
            if a.mock:cmd.append('--mock')
            if a.cpu_only:cmd.append('--cpu-only')
            update(status='STARTING')
            os.chdir(source);frozen_env=os.environ.copy();frozen_env.pop('PYTHONPATH',None);frozen_env.pop('PYTHONHOME',None)
            os.execve(sys.executable,cmd,frozen_env)
        source=ROOT
        env={**os.environ,'CUDA_VISIBLE_DEVICES':'','PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1'}
        env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
        write(out/'execution_environment.json',dict(python=sys.version,executable=sys.executable,prefix=sys.prefix,
            package_manifest_sha256=sha(ROOT/'PACKAGE_MANIFEST.json'),physical_gpu=GPU_INDEX,gpu_uuid=GPU_UUID,workers=a.workers,
            dependencies={n:importlib.metadata.version(n)for n in('agentdojo','openai','pydantic','httpx','tenacity')},
            scientific_redraws=0,profile_scope='Declared local-role profiles; not a principal published-model replication',
            model_cache=str(a.cache),serving_python=str(a.serving_python)))
        freeze=subprocess.run([sys.executable,'-m','pip','freeze'],capture_output=True,text=True,timeout=30);(out/'research_packages.txt').write_text(freeze.stdout+freeze.stderr)
        update(status='CPU_QUALIFICATION')
        with (out/'cpu_qualification_process.log').open('w')as stream:
            p=subprocess.run([sys.executable,'-m','reference_study.qualification','--out',str(out/'cpu_qualification')],cwd=source,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
        q=read(out/'cpu_qualification/qualification.json')if(out/'cpu_qualification/qualification.json').is_file()else{'status':'FAIL','tests_run':0}
        print(f'CPU QUALIFICATION: {q["status"]}; {q["tests_run"]} tests with real source/native subcases; zero model inference',flush=True)
        if p.returncode or q['status']!='PASS':raise RuntimeError('CPU qualification failed; no GPU model started')
        if a.cpu_only:update(status='CPU_QUALIFICATION_COMPLETE_ZERO_INFERENCE')
        else:
            eligible={family:True for family in('qwen','gemma')}
            if not a.mock:
                update(status='PREFLIGHT_BOTH_MODELS')
                if not a.serving_python.is_file():raise RuntimeError('Missing .venv-serving/bin/python; run SETUP.sh serving')
                check=subprocess.run([str(a.serving_python),'-c',
                    'import sys,torch,vllm,json;print(json.dumps(dict(python=sys.version,venv=sys.prefix!=sys.base_prefix,torch=torch.__version__,vllm=vllm.__version__)))'],
                    env=env,capture_output=True,text=True,timeout=120)
                (out/'serving_versions.log').write_text(check.stdout+check.stderr);check.check_returncode()
                versions=json.loads(check.stdout.strip().splitlines()[-1]);write(out/'serving_versions.json',versions)
                if not versions['venv']or versions['vllm']!='0.26.0'or not versions['torch'].startswith('2.11.0'):raise RuntimeError('Qualified serving profile is vLLM0.26.0/torch2.11.0 in .venv-serving; no silent upgrade')
                activate('qwen');from reference_discovery_parallel.base import serving
                from .models import profiles
                for family,p in profiles().items():
                    folder=out/'preflight'/family;folder.mkdir(parents=True)
                    try:
                        snap,cache_identity=serving.inspect_snapshot(a.cache/('models--'+p['hub'].replace('/','--')),p['hub'],p['revision'])
                        write(folder/'snapshot_identity.json',cache_identity)
                        child_env={**env,'PATH':str(a.serving_python.parent)+os.pathsep+env.get('PATH',''),'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'}
                        with (folder/'process.log').open('w')as stream:
                            proc=subprocess.run([str(a.serving_python),'-m','reference_study.models','--snapshot',str(snap),'--family',family,'--out',str(folder/'rendering')],
                                cwd=source,env=child_env,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
                        if proc.returncode or read(folder/'rendering/qualification.json')['status']!='PASS':raise RuntimeError('Cached rendering/parser qualification failed')
                    except BaseException as e:
                        if isinstance(e,(StopRequested,KeyboardInterrupt)):raise
                        eligible[family]=False;write(folder/'error.json',dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc()))
                        print('PREFLIGHT FAILED',family,'; preserved evidence; other qualified profile may still run.',flush=True)
            for family in('qwen','gemma'):
                if not eligible[family]:status['profiles'][family]='NOT_EXECUTED_PREFLIGHT_FAILURE';rc=1;continue
                update(status='RUNNING_PROFILE',active_profile=family)
                cmd=[sys.executable,'-u','-m','reference_study.profile','--family',family,'--out',str(out/family),
                    '--manifest',str(out/'FROZEN_MANIFEST.json'),'--project-root',str(project),'--serving-python',str(a.serving_python),
                    '--cache',str(a.cache),'--lock-fd',str(lock.fileno()),'--workers',str(a.workers)]+(['--mock']if a.mock else[])
                active=subprocess.Popen(cmd,cwd=source,env=env,pass_fds=(lock.fileno(),))
                write(out/f'{family}_profile_process.json',dict(pid=active.pid,argv=cmd))
                while active.poll()is None:time.sleep(.2 if a.mock else 1)
                status['profiles'][family]=active.returncode;update()
                if active.returncode:rc=1
                profile_status=read(out/family/'status.json')if(out/family/'status.json').is_file()else{}
                if profile_status.get('status')=='OWNED_CLEANUP_FAILED':raise RuntimeError('Owned cleanup failed; next model will not start')
            update(status='COMPLETE_WITH_TECHNICAL_ISSUES'if rc else'MOCK_COMPLETE_ZERO_INFERENCE'if a.mock else'COMPLETE_EXPLORATORY_REVIEW_PENDING',active_profile=None)
    except BaseException as e:
        rc=2 if status['status']=='BLOCKED_CONCURRENT_SEQUENCE'else 1
        if status['status']!='BLOCKED_CONCURRENT_SEQUENCE':update(status='INTERRUPTED'if isinstance(e,(StopRequested,KeyboardInterrupt))else'FAILED')
        write(out/'fatal_error.json',dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc()));print('STOP:',str(e),flush=True)
    finally:
        try:terminate_active()
        except BaseException as e:rc=1;update(status='OWNED_CLEANUP_FAILED',cleanup_error=str(e))
        try:
            report=analyze(out,m)
            from .verification import verify
            native_check=verify(out)
            print('INDEPENDENT NATIVE EFFECT CHECK:',native_check['status'],'worlds:',native_check['native_world_checks'],flush=True)
            if native_check['status']!='PASS':rc=1;update(status='MEASUREMENT_INCONSISTENCY_RAW_PRESERVED')
            if status['status']in('COMPLETE_EXPLORATORY_REVIEW_PENDING','MOCK_COMPLETE_ZERO_INFERENCE')and any(x['recorded']!=x['planned']or x['qualified']!=x['planned']for f in report['counts'].values()for x in f.values()):
                rc=1;update(status='COMPLETE_WITH_TECHNICAL_ISSUES')
        except Exception as e:rc=1;write(out/'analysis_error.json',dict(message=str(e),traceback=traceback.format_exc()))
        update(finished_epoch=time.time(),exit_code=rc)
        logfile=logs/(a.run_id+'.log')
        if logfile.is_file():shutil.copyfile(logfile,out/'controller.log')
        try:
            print('PACKAGING complete lossless raw evidence; GPU collection has ended.',flush=True)
            raw,review=package(out);print('COMPLETE RAW ARCHIVE:',raw,flush=True);print('COMPACT REVIEW:',review,flush=True)
        except BaseException as e:rc=1;update(status='ARCHIVE_FAILED_RAW_DIRECTORY_PRESERVED',archive_error=str(e))
        (logs/(a.run_id+'.status')).write_text(f'exit_code={rc}\nstatus={status["status"]}\nresults={out}\narchive={raw}\nreview={review}\n')
        stopbeat.set();thread.join(timeout=1)
        if acquired:fcntl.flock(lock,fcntl.LOCK_UN)
        lock.close()
    return rc

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--project-root',type=Path,required=True);p.add_argument('--run-id',required=True)
    p.add_argument('--serving-python',type=Path,required=True);p.add_argument('--cache',type=Path,default=Path('/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache'))
    p.add_argument('--workers',type=int,choices=(1,2,3,4),default=4)
    p.add_argument('--lock-fd',type=int,help='Inherited authenticated bootstrap GPU2 lock; normally supplied by RUN_STUDY.sh')
    p.add_argument('--frozen-snapshot',type=Path,help=argparse.SUPPRESS)
    modes=p.add_mutually_exclusive_group();modes.add_argument('--cpu-only',action='store_true');modes.add_argument('--mock',action='store_true')
    a=p.parse_args()
    import re
    if not re.fullmatch('[A-Za-z0-9_-]+',a.run_id):p.error('Unsafe run ID')
    a.serving_python=Path(os.path.abspath(a.serving_python));a.cache=a.cache.expanduser().absolute()
    raise SystemExit(main(a))
