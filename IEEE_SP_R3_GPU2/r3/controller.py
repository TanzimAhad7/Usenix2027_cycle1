import argparse,concurrent.futures,fcntl,importlib.metadata,json,os,shutil,signal,subprocess,sys,threading,time,traceback
from pathlib import Path
from .common import ROOT,CACHE,REVISION,read,write,verify_package,sha
from .design import manifest
from .report import analyze
from .archive import archive
from .server import OwnedServer
from .serving_base import proc_start

def main(a):
    project=a.project_root.resolve();out=project/'results/user_runs'/a.run_id
    if sys.prefix==sys.base_prefix:raise RuntimeError('Use the R3 isolated client environment')
    if os.fstat(a.lock_fd).st_ino!=(project/'logs/.r3_gpu2.lock').stat().st_ino:raise RuntimeError('GPU2 project lock is not authenticated')
    fcntl.flock(a.lock_fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if not a.frozen:
        out.mkdir(parents=True,exist_ok=False);identity=verify_package();source=out/'source'
        for rel in identity['files']:
            target=source/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,target)
        shutil.copy2(ROOT/'PACKAGE_MANIFEST.json',source/'PACKAGE_MANIFEST.json');os.set_inheritable(a.lock_fd,True);os.chdir(source)
        env=dict(os.environ,CUDA_VISIBLE_DEVICES='',PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1')
        for k in ('PYTHONPATH','PYTHONHOME'):env.pop(k,None)
        os.execve(sys.executable,[sys.executable,'-u','-m','r3.controller',*sys.argv[1:],'--frozen'],env)
    if ROOT.absolute()!=out/'source':raise RuntimeError('Frozen controller source path mismatch')
    verify_package();m=manifest();write(out/'MANIFEST.json',m);write(out/'LIMITS_PREDECLARED.json',m['limits'])
    stop=threading.Event();signal.signal(signal.SIGTERM,lambda *_:stop.set());signal.signal(signal.SIGINT,lambda *_:stop.set())
    state=dict(status='QUALIFYING',run_id=a.run_id,physical_gpu=2,model='Qwen/Qwen3-32B',started_epoch=time.time(),full_planned=32,conditional_slots=32,completed=0,active=[])
    census={j['id']:'SCHEDULED' for j in m['jobs']};census.update({j['id']:'PENDING_ELIGIBILITY' for j in m['branches']});running={};lock=threading.Lock();lastbeat=0;server=None;exit_code=0
    env=dict(os.environ,CUDA_VISIBLE_DEVICES='',PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1')
    for k in ('PYTHONPATH','PYTHONHOME','HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','http_proxy','https_proxy','all_proxy'):env.pop(k,None)
    def update(**kw):
        with lock:
            state.update(kw);state['active']=list(running);state['elapsed_seconds']=time.time()-state['started_epoch'];write(out/'status.json',state);write(out/'census.json',census)
    def heartbeat(force=False):
        nonlocal lastbeat
        if stop.is_set():raise InterruptedError('Owned stop requested')
        if force or time.monotonic()-lastbeat>20:
            lastbeat=time.monotonic();update();print('HEARTBEAT',state['status'],'recorded='+str(state['completed'])+'/64','active='+str(state['active']),'elapsed='+str(int(state['elapsed_seconds']))+'s',flush=True)
            if server:server.refresh()
    def run_process(cmd,log,timeout,key):
        log.parent.mkdir(parents=True,exist_ok=True)
        with log.open('w') as f:
            if stop.is_set():raise InterruptedError('Stop requested before launch')
            process=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True);identity=proc_start(process.pid)
            with lock:running[key]=dict(pid=process.pid,start=identity)
            started=time.monotonic()
            try:
                while process.poll() is None:
                    if stop.is_set() or time.monotonic()-started>timeout:
                        if identity is not None and proc_start(process.pid)==identity:os.killpg(process.pid,signal.SIGTERM)
                        try:process.wait(timeout=10)
                        except subprocess.TimeoutExpired:
                            if identity is not None and proc_start(process.pid)==identity:os.killpg(process.pid,signal.SIGKILL)
                            process.wait(timeout=10)
                        raise InterruptedError('Owned stop') if stop.is_set() else TimeoutError('Technical process watchdog')
                    time.sleep(.2)
                return process.returncode
            finally:
                with lock:running.pop(key,None)
    def command(cmd,log,timeout=600):
        # Keep the controller's heartbeat responsive during setup/qualification subprocesses.
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future=pool.submit(run_process,cmd,log,timeout,'qualification')
            while not future.done():heartbeat();time.sleep(.5)
            if future.result()!=0:raise RuntimeError('Qualification command failed: '+str(log))
    def terminal(j,folder,status,**kw):
        path=out/folder/j['id'];path.mkdir(parents=True,exist_ok=True)
        if not (path/'result.json').is_file():
            result=dict(id=j['id'],kind=j['kind'],status=status,attempted=bool(kw.get('attempted_process',False)),qualified=False,scientific_negative=False,anytime_violation=None,**kw)
            receipt=path/'live_state_receipt.json'
            if receipt.is_file():
                observed=read(receipt);prefix=0
                if j['kind']=='BRANCH':
                    cp=out/'full'/j['parent']/'checkpoint.json'
                    if cp.is_file():prefix=read(cp)['prefix_effect_count']
                bad=observed['violation_indices'];fresh=[i for i in bad if i>=prefix]
                result.update(partial_effects=observed['effects'],violation_indices=bad,prefix_effect_count=prefix,anytime_violation=True if bad else None,new_unauthorized_effects=len(fresh) if fresh else None,partial_observation_scope='Last persisted native state, not a complete/qualified workflow; later events may exist')
            write(path/'result.json',result)
    def acquire(j,folder,parent=None):
        path=out/folder/j['id'];jobfile=out/'jobs'/(j['id']+'.json');write(jobfile,j)
        if stop.is_set():terminal(j,folder,'NOT_EXECUTED_USER_STOP');return
        cmd=[sys.executable,'-u','-m','r3.episode','--job',str(jobfile),'--out',str(path)]+(['--parent',str(parent)] if parent else[])
        try:
            code=run_process(cmd,out/'worker_logs'/(j['id']+'.log'),m['limits']['case_timeout_seconds'],j['id'])
            if not (path/'result.json').is_file():terminal(j,folder,'WORKER_EXIT_WITHOUT_RESULT',attempted_process=True,exit_code=code)
        except BaseException as exc:
            terminal(j,folder,'INTERRUPTED' if isinstance(exc,InterruptedError) else 'TECHNICAL_WATCHDOG',error=str(exc),attempted_process=True)
    def stage(jobs,folder):
        update(status='RUNNING_'+folder.upper())
        with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
            futures={pool.submit(acquire,j,folder,out/'full'/j['parent'] if folder=='branches' else None):j for j in jobs}
            while futures:
                done,_=concurrent.futures.wait(futures,timeout=1,return_when=concurrent.futures.FIRST_COMPLETED)
                for f in done:
                    j=futures.pop(f);f.result();r=read(out/folder/j['id']/'result.json');census[j['id']]=r['status'];state['completed']+=1
                    print(j['id'],r['status'],'qualified='+str(r.get('qualified')),flush=True)
                heartbeat();update()
        analyze(out,m)
    try:
        update();command([sys.executable,str(ROOT/'ENVIRONMENT.py'),'client'],out/'qualification/client_environment.log')
        write(out/'environment.json',dict(python=sys.version,client=sys.executable,serving_python=str(a.serving_python),model_cache=str(a.cache),model_revision=REVISION,packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()},scope='Official generic local Qwen target and auxiliaries on GPU2, authored development tasks; not principal remote-model replication'))
        command([sys.executable,'-m','unittest','discover','-s','tests','-v'],out/'qualification/cpu_tests.log')
        command([sys.executable,'-m','r3.qualification','prepare','--out',str(out/'qualification/prepared')],out/'qualification/preparation.log')
        command([str(a.serving_python),str(ROOT/'ENVIRONMENT.py'),'serving'],out/'qualification/serving_environment.log')
        server=OwnedServer(a.serving_python,a.cache,out/'serving',heartbeat);snapshot=server.prepare()
        command([str(a.serving_python),'-m','r3.render','--snapshot',str(snapshot),'--prepared',str(out/'qualification/prepared/prepared_requests.json'),'--out',str(out/'qualification/rendered')],out/'qualification/rendering.log')
        update(status='STARTING_OWNED_GPU2_SERVER');server.start(m['limits']);update(status='LIVE_INTERFACE_QUALIFICATION')
        command([sys.executable,'-m','r3.qualification','live','--out',str(out/'qualification/live')],out/'qualification/live.log',1200)
        write(out/'DESIGN_FREEZE_BEFORE_ACQUISITION.json',dict(manifest_sha256=sha(out/'MANIFEST.json'),limits=m['limits'],render_qualification=read(out/'qualification/rendered/qualification.json'),live_qualification=read(out/'qualification/live/qualification.json'),no_outcome_based_threshold_tuning=True))
        stage(m['jobs'],'full');archive(out,'after_full')
        eligible=[]
        for j in m['branches']:
            cp=out/'full'/j['parent']/'checkpoint.json'
            if cp.is_file():eligible.append(j)
            else:
                parent_result=read(out/'full'/j['parent']/'result.json')
                reason='NOT_ELIGIBLE_NO_TARGET_DENIAL' if parent_result.get('qualified') else 'NOT_ELIGIBLE_PARENT_INCOMPLETE'
                terminal(j,'branches',reason,parent_status=parent_result['status'],reason='No qualified predeclared target-denial checkpoint was recorded; not a safety result')
                census[j['id']]=reason;state['completed']+=1
        stage(eligible,'branches');update(status='COMPLETE_R3_REVIEW_PENDING')
        if any(read(out/'full'/j['id']/'result.json').get('qualified') is not True for j in m['jobs']) or any(read(out/'branches'/j['id']/'result.json').get('qualified') is not True for j in eligible):exit_code=1;update(status='COMPLETE_WITH_TECHNICAL_ISSUES_REVIEW_PENDING')
    except BaseException as exc:
        exit_code=1;stop.set();update(status='INTERRUPTED' if isinstance(exc,InterruptedError) else 'QUALIFICATION_OR_CONTROLLER_FAILED',error=str(exc))
        write(out/'fatal_error.json',dict(error=str(exc),type=type(exc).__name__,traceback=traceback.format_exc()))
    finally:
        for folder,items in [('full',m['jobs']),('branches',m['branches'])]:
            for j in items:
                if not (out/folder/j['id']/'result.json').is_file():terminal(j,folder,'NOT_EXECUTED_'+state['status']);census[j['id']]='NOT_EXECUTED_'+state['status']
        if server:
            completion_status=state['status'];update(status='STOPPING_OWNED_GPU2_SERVER')
            try:server.close();state['owned_cleanup_verified']=True;state['status']=completion_status
            except Exception as exc:exit_code=1;state.update(status='OWNED_CLEANUP_FAILED',cleanup_error=str(exc),owned_cleanup_verified=False)
        analyze(out,m);update(exit_code=exit_code,finished_epoch=time.time())
        log=project/'logs'/(a.run_id+'.log')
        if log.is_file():shutil.copyfile(log,out/'controller.log')
        try:
            paths=archive(out);print('RAW ARCHIVE:',paths[0],'\nREVIEW ARCHIVE:',paths[1],flush=True)
        except Exception as exc:
            exit_code=1;write(out/'archive_error.json',dict(error=str(exc)));update(status='ARCHIVE_FAILED',exit_code=exit_code);print('ARCHIVE FAILED:',str(exc),flush=True)
        (project/'logs'/(a.run_id+'.status')).write_text('exit_code='+str(exit_code)+'\nstatus='+state['status']+'\nresults='+str(out)+'\n')
    return exit_code
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--project-root',type=Path,required=True);p.add_argument('--run-id',required=True);p.add_argument('--serving-python',type=Path,required=True);p.add_argument('--cache',type=Path,default=Path(CACHE));p.add_argument('--lock-fd',type=int,required=True);p.add_argument('--workers',type=int,choices=[1,2,4],default=4);p.add_argument('--frozen',action='store_true');a=p.parse_args()
    import re
    if not re.fullmatch('[A-Za-z0-9_-]+',a.run_id):p.error('Unsafe run ID')
    for key in ('project_root','serving_python','cache'):setattr(a,key,getattr(a,key).expanduser().absolute())
    raise SystemExit(main(a))
