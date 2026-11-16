"""One owned GPU-3 job, complete schedule and immutable evidence archive."""
from __future__ import annotations
import argparse,fcntl,importlib.metadata,json,os,re,shutil,signal,subprocess,sys,tarfile,threading,time,traceback
from pathlib import Path
from .common import MODULE,PACKAGE,GPU_UUID,MODEL,MODEL_FAMILY,REVISION,CACHE,read,write,file_hash,append
from .protocol import manifest
from .qualification import qualify
from .experiment import run_study
from .report import analyze,verify_results
from .base import serving
from .infrastructure import transport_outage,reserve_restart
from .budget import CampaignBudgetStop
from .execution_config import WORKERS,DrainBeforeRestart

from .integrity import verify_package

def server_command(python,snapshot):
    from .models import command
    return command(python,snapshot,MODEL_FAMILY)

def placement(server):
    descendants=serving.descendant_pids(server.pid)
    row=next((r for r in serving.gpu_table() if r[0].strip()=='3'),None)
    if not row or row[1].strip()!=GPU_UUID:raise RuntimeError('Physical GPU 3 UUID mismatch')
    sockets=serving.command(['ss','-ltnp','( sport = :18080 )'])
    listeners={int(p) for p in re.findall(r'pid=(\d+)',sockets)}
    if not listeners or not listeners<=descendants:raise RuntimeError('Endpoint does not belong exclusively to owned server')
    workers=[]
    for r in serving.gpu_applications():
        if len(r)<2 or not r[0].strip().isdigit():continue
        pid=int(r[0]);uuid=r[1].strip()
        if pid in descendants:workers.append(dict(pid=pid,gpu_uuid=uuid))
        elif uuid==GPU_UUID:raise RuntimeError('Foreign GPU-3 worker appeared; it was not stopped')
    if not workers or any(w['gpu_uuid']!=GPU_UUID for w in workers):raise RuntimeError('Owned workers not exclusively on GPU 3')
    return dict(qualified=True,listeners=sorted(listeners),workers=workers,physical_gpu=3,gpu_uuid=GPU_UUID)

def archive(out):
    print('ARCHIVING: hashing raw evidence and compressing; this may take time.',flush=True)
    paths=[p for p in sorted(out.rglob('*')) if p.is_file() and p!=out/'SHA256SUMS' and '__pycache__' not in p.relative_to(out).parts]
    (out/'SHA256SUMS').write_text(''.join(file_hash(p)+'  '+str(p.relative_to(out))+'\n' for p in paths))
    target=Path(str(out)+'.tar.gz');partial=Path(str(target)+'.partial')
    with tarfile.open(partial,'w:gz',compresslevel=3) as t:t.add(out,arcname=out.name,filter=lambda i:None if '__pycache__' in Path(i.name).parts else i)
    partial.replace(target);Path(str(target)+'.sha256').write_text(file_hash(target)+'  '+target.name+'\n')
    print('UPLOAD ARCHIVE:',target,flush=True);return target

def main(args):
    root=args.root.resolve();out=args.output.resolve() if args.output else root/'results/user_runs'/args.run_id;out.mkdir(parents=True,exist_ok=False)
    logs=root/'logs';logs.mkdir(exist_ok=True);frozen=manifest();write(out/'FROZEN_MANIFEST.json',frozen)
    census=dict(references={b['id']:'SCHEDULED' for b in frozen['blocks']},
        admissions={i:'SCHEDULED' for b in frozen['blocks'] for i in b['admissions']},workflows={w['id']:'SCHEDULED' for w in frozen['workflows']},forks={w['id']:'SCHEDULED' for w in frozen['forks']})
    write(out/'census.json',census)
    status=dict(status='STARTING',mode='MOCK' if args.mock else 'CPU_ONLY' if args.cpu_only else 'MODEL_STUDY',
        started_epoch=time.time(),run_id=args.run_id,active=None,physical_gpu=3,gpu_uuid=GPU_UUID)
    lock=None;server=None;server_log=None;owned={};rc=0;stop=threading.Event();threads=[];console=sys.stdout
    restart_count=0;restart_reason=None;active_slots=set()
    collection_done=threading.Event()
    collection_deadline=None if args.max_collection_hours is None else time.monotonic()+args.max_collection_hours*3600
    budget_expired=threading.Event()
    def require_budget():
        if budget_expired.is_set() or (collection_deadline is not None and time.monotonic()>=collection_deadline):
            raise CampaignBudgetStop('User-selected collection limit reached; preserving incomplete schedule')
    def deadline_signal(*_):
        if not collection_done.is_set():
            budget_expired.set()
            raise CampaignBudgetStop('User-selected collection limit reached')
    def watch_budget():
        if collection_deadline is None:return
        if not collection_done.wait(max(0,collection_deadline-time.monotonic())):
            budget_expired.set()
            if not collection_done.is_set():os.kill(os.getpid(),signal.SIGUSR1)
    def state(**values):status.update(values);write(out/'status.json',status)
    def beat():
        while not stop.wait(20):
            nr=sum(v not in ['SCHEDULED','RUNNING'] for v in census['references'].values())
            na=sum(v not in ['SCHEDULED','RUNNING'] for v in census['admissions'].values())
            nw=sum(v not in ['SCHEDULED','RUNNING'] for v in census['workflows'].values())
            nf=sum(v not in ['SCHEDULED','RUNNING'] for v in census['forks'].values())
            remaining='not clock-limited' if collection_deadline is None else str(max(0,int(collection_deadline-time.monotonic())))+'s'
            print(f'HEARTBEAT stage={status["status"]} active={status.get("active")} workflows={nw}/{frozen["counts"]["autonomous_workflows"]} conditional_slots={nf}/{len(frozen["forks"])} elapsed={int(time.time()-status["started_epoch"])}s collection_remaining={remaining} results={out}',flush=True,file=console)
    def progress(kind,ident,value):
        nonlocal server,server_log,owned,restart_count,restart_reason
        if value=='RUNNING':require_budget()
        if value=='RUNNING' and server is not None:
            if server.poll() is not None or restart_reason is not None:
                if active_slots:raise DrainBeforeRestart('Drain both in-flight workflows before restarting the owned server')
                restart_count=reserve_restart(restart_count,frozen['limits']['owned_server_restarts'])
                folder=out/'serving'/f'restart_{restart_count:02d}';folder.mkdir()
                state(status='RECOVERING_OWNED_SERVER',restart_count=restart_count)
                write(folder/'reason.json',dict(epoch=time.time(),reason=restart_reason or 'Owned process exited',next_slot=ident,failed_slots_are_not_redrawn=True))
                serving.stop_owned(server,owned,folder/'previous_shutdown.json')
                if server_log:server_log.close()
                serving.ensure_free(GPU_UUID);serving.ensure_port_free()
                write(folder/'command.json',dict(command=cmd,cuda_visible_devices=GPU_UUID))
                server_log=(folder/'server.log').open('w')
                server=subprocess.Popen(cmd,cwd=root,env=env,stdout=server_log,stderr=subprocess.STDOUT,start_new_session=True)
                owned={server.pid:serving.proc_start(server.pid)}
                write(folder/'owned_process.json',dict(pid=server.pid,start=owned[server.pid]))
                started=time.monotonic();last=-30
                while True:
                    require_budget()
                    if server.poll() is not None:raise RuntimeError('Replacement owned server failed; see '+str(folder/'server.log'))
                    for pid in serving.descendant_pids(server.pid):owned.setdefault(pid,serving.proc_start(pid))
                    try:
                        models=serving.read_json_url('http://127.0.0.1:18080/v1/models')
                        if models.get('data') and models['data'][0].get('id')==MODEL:break
                    except Exception:pass
                    elapsed=time.monotonic()-started
                    if elapsed>1800:raise RuntimeError('Replacement server startup watchdog expired')
                    if elapsed-last>=30:print(f'Waiting for replacement owned {MODEL_FAMILY}: {int(elapsed)}s; {folder}/server.log',flush=True);last=elapsed
                    time.sleep(2)
                write(folder/'placement.json',placement(server));write(folder/'models.json',models)
                restart_reason=None;print('RECOVERED owned server. Continuing untouched slots; failed slots retained.',flush=True)
            for pid in serving.descendant_pids(server.pid):owned.setdefault(pid,serving.proc_start(pid))
        if value=='RUNNING':active_slots.add((kind,ident))
        else:active_slots.discard((kind,ident))
        census[{'reference':'references','admission':'admissions','workflow':'workflows','fork':'forks'}[kind]][ident]=value
        append(out/'census_events.jsonl',dict(epoch=time.time(),kind=kind,id=ident,status=value,server_epoch=restart_count))
        if value!='RUNNING' and server is not None:
            directory=out/{'workflow':'workflows','reference':'references','admission':'admissions','fork':'forks'}[kind]/ident
            restart_reason=transport_outage(directory) or restart_reason
        if value!='RUNNING':write(out/'census.json',census)
        state(status='RUNNING_STUDY',active=ident,active_kind=kind,active_cases=[dict(kind=k,id=i) for k,i in sorted(active_slots)],workflow_workers=WORKERS)
    try:
        lock=os.fdopen(os.dup(args.lock_fd),'a') if args.lock_fd is not None else (logs/'gpu3_sequence.lock').open('a')
        try:
            if args.lock_fd is None:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            elif os.fstat(lock.fileno()).st_ino!=(logs/'gpu3_sequence.lock').stat().st_ino:raise RuntimeError('Inherited lock is not the shared GPU lock')
        except BlockingIOError:
            state(status='BLOCKED_CONCURRENT_SEQUENCE');raise RuntimeError('Another sequence owns logs/gpu3_sequence.lock; no server started or stopped')
        recorded=verify_package(root)
        for name in ([] if args.shared_qualification else list(recorded['files'])+['PARALLEL_REFERENCE_PACKAGE_MANIFEST.json']):
            target=out/'source'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/name,target)
        if args.shared_qualification:write(out/'source_reference.json',dict(package_manifest_sha256=file_hash(root/'PARALLEL_REFERENCE_PACKAGE_MANIFEST.json'),shared_snapshot=str(args.shared_qualification.parent/'source'),rule='Parent retains one complete immutable source snapshot for both models'))
        write(out/'execution_environment.json',dict(python=sys.version,executable=sys.executable,prefix=sys.prefix,
            dependencies={n:importlib.metadata.version(n) for n in ['agentdojo','openai','pydantic','httpx','tenacity']},
            research_cuda_visible_devices=os.environ.get('CUDA_VISIBLE_DEVICES'),model=MODEL,model_family=MODEL_FAMILY,mode=status['mode']))
        t=threading.Thread(target=beat,daemon=True);threads.append(t);t.start()
        signal.signal(signal.SIGTERM,lambda *_:(_ for _ in ()).throw(KeyboardInterrupt('SIGTERM: preserving partial evidence')))
        signal.signal(signal.SIGUSR1,deadline_signal)
        budget_thread=threading.Thread(target=watch_budget,daemon=True);budget_thread.start()
        write(out/'TIME_BUDGET.json',dict(default_limit=None,user_max_collection_hours=args.max_collection_hours,rule='No default clock cutoff. Optional user limit preserves partial evidence and unexecuted slots. Per-workflow technical watchdogs always apply.'))
        state(status='CPU_QUALIFICATION')
        if args.shared_qualification:
            from .runtime_receipt import runtime_digest
            receipt=read(args.shared_qualification/'receipt.json')
            q=read(args.shared_qualification/'qualification.json');origin=None
            if q['status']!='PASS' or receipt['package_sha256']!=file_hash(root/'PARALLEL_REFERENCE_PACKAGE_MANIFEST.json') or receipt['qualification_sha256']!=file_hash(args.shared_qualification/'qualification.json') or receipt['python']!=sys.executable or receipt['runtime_source_digest']!=runtime_digest():
                raise RuntimeError('Shared CPU qualification does not match current code/runtime')
            write(out/'shared_qualification.json',dict(path=str(args.shared_qualification),receipt=receipt,scope='Same frozen code and source runtime qualified once by parent; no model-specific native semantics are assumed'))
        else:q,origin=qualify(out/'cpu_qualification')
        print(f'CPU QUALIFICATION: {q["status"]} ({q["tests_run"]} tests; zero model inference)',flush=True)
        if q['status']!='PASS':raise RuntimeError('CPU qualification failed; see cpu_qualification/qualification.log')
        if args.cpu_only:
            state(status='CPU_QUALIFICATION_COMPLETE_ZERO_MODEL_INFERENCE')
        else:
            require_budget()
            if not args.mock:
                write(out/'pid_namespace.json',serving.verify_pid_namespace())
                python=root/'.venv-serving/bin/python'
                if not python.is_file():raise RuntimeError('Missing existing .venv-serving/bin/python; no install attempted')
                row=next((r for r in serving.gpu_table() if r[0].strip()=='3'),None)
                if not row or row[1].strip()!=GPU_UUID:raise RuntimeError('Frozen physical GPU-3 UUID differs')
                serving.ensure_free(GPU_UUID);serving.ensure_port_free()
                snap,identity=serving.inspect_snapshot(Path(args.cache)/('models--'+__import__(__package__+'.models',fromlist=['PROFILES']).PROFILES[MODEL_FAMILY]['hub'].replace('/','--')),__import__(__package__+'.models',fromlist=['PROFILES']).PROFILES[MODEL_FAMILY]['hub'],REVISION)
                write(out/'snapshot_identity.json',identity)
                serv=out/'serving';serv.mkdir()
                env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES=GPU_UUID,CUDA_DEVICE_ORDER='PCI_BUS_ID',
                    HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',VLLM_NO_USAGE_STATS='1',DO_NOT_TRACK='1',HF_HUB_DISABLE_TELEMETRY='1',
                    PATH=str(python.parent)+os.pathsep+env.get('PATH',''))
                env.pop('VLLM_API_KEY',None)
                version_cmd=[str(python),'-c','import torch,vllm,sys,json; print(json.dumps(dict(python=sys.version,torch=torch.__version__,vllm=vllm.__version__)))']
                versions=json.loads(serving.command(version_cmd,timeout=60));write(serv/'versions.json',versions)
                if versions['vllm']!='0.26.0' or not versions['torch'].startswith('2.11.0'):raise RuntimeError('Unqualified serving versions; expected vLLM 0.26.0 / torch 2.11.0; no modification attempted')
                ninja=subprocess.run([str(python.parent/'ninja'),'--version'],capture_output=True,text=True,timeout=20,check=True)
                (serv/'ninja_version.txt').write_text(ninja.stdout)
                cmd=server_command(python,snap);write(serv/'command.json',dict(command=cmd,cuda_visible_devices=GPU_UUID,
                    chat_template='Unmodified snapshot' if MODEL_FAMILY=='qwen' else 'Explicit Gemma tagged-JSON adapter; separately qualified profile',server_output_cap=8192,server_seed=20261025,
                    model_request_seed=None,model_defaults='generation-config=vllm; source request settings retained'))
                server_log=(serv/'server.log').open('w');server=subprocess.Popen(cmd,cwd=root,env=env,stdout=server_log,stderr=subprocess.STDOUT,start_new_session=True)
                owned={server.pid:serving.proc_start(server.pid)};write(serv/'owned_process.json',dict(pid=server.pid,start=owned[server.pid],process_group=server.pid))
                t=threading.Thread(target=serving.telemetry,args=(out,stop),daemon=True);threads.append(t);t.start()
                state(status='STARTING_'+MODEL_FAMILY.upper());started=time.monotonic();last=-30
                while True:
                    require_budget()
                    if server.poll() is not None:raise RuntimeError('Owned vLLM exited; inspect serving/server.log')
                    for pid in serving.descendant_pids(server.pid):owned.setdefault(pid,serving.proc_start(pid))
                    try:
                        models=serving.read_json_url('http://127.0.0.1:18080/v1/models')
                        if models.get('data') and models['data'][0].get('id')==MODEL:break
                    except Exception:pass
                    elapsed=time.monotonic()-started
                    if elapsed>1800:raise RuntimeError('Server startup watchdog expired after 1800s')
                    if elapsed-last>=30:print(f'Waiting for owned {MODEL_FAMILY}: {int(elapsed)}s; {serv}/server.log',flush=True);last=elapsed
                    time.sleep(2)
                write(serv/'placement.json',placement(server));write(serv/'models.json',models)
                try:write(serv/'server_info.json',serving.read_json_url('http://127.0.0.1:18080/server_info?config_format=json'))
                except Exception as exc:write(serv/'server_info.json',dict(status='UNAVAILABLE',error=str(exc)))
                from .live_profile import qualify as qualify_live
                qualify_live(out/'live_profile_qualification')
                print(f'QUALIFIED owned {MODEL_FAMILY} on physical GPU 3. Running344 autonomous workflows and up to30 authentic matched recovery continuations.',flush=True)
            state(status='RUNNING_STUDY')
            run_study(out,origin,frozen,progress,mock=args.mock,failure_block=args.inject_failure_block,deadline=collection_deadline,
                drain_needed=lambda:server is not None and (server.poll() is not None or restart_reason is not None))
            state(status='MOCK_COMPLETE_ZERO_MODEL_INFERENCE' if args.mock else 'COMPLETE_REVIEW_PENDING',active=None)
    except BaseException as exc:
        timed_out=isinstance(exc,CampaignBudgetStop)
        rc=0 if timed_out else 2 if status['status']=='BLOCKED_CONCURRENT_SEQUENCE' else 1
        state(status='TIME_BUDGET_REACHED' if timed_out else status['status'] if rc==2 else 'INTERRUPTED' if isinstance(exc,KeyboardInterrupt) else 'FAILED',error=str(exc),active=None)
        write(out/('budget_stop.json' if timed_out else 'fatal_error.json'),dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc(),scientific_negative=False if timed_out else None))
        print('STOP:',str(exc),flush=True)
    finally:
        collection_done.set()
        if server is not None:
            try:serving.stop_owned(server,owned,out/'serving/shutdown.json');print('STOPPED owned '+MODEL_FAMILY+'.',flush=True)
            except Exception as exc:rc=1;state(status='OWNED_CLEANUP_FAILED',cleanup_error=str(exc))
        if server_log:server_log.close()
        for mapping in census.values():
            for ident,value in mapping.items():
                if value in ['SCHEDULED','RUNNING']:mapping[ident]='NOT_COMPLETED_'+status['status']
        write(out/'census.json',census);state(exit_code=rc,finished_epoch=time.time(),active=None,active_cases=[])
        try:
            if args.defer_finalization:
                write(out/'DEFERRED_FINALIZATION.json',dict(status='PENDING_PARENT_ANALYSIS',model_family=MODEL_FAMILY,raw_evidence_preserved=True))
                summary=None;checks=dict(status='DEFERRED')
            else:summary=analyze(out);checks=verify_results(out)
            if checks['status'] not in ('PASS','DEFERRED'):rc=1
            if summary is not None and status['mode']!='CPU_ONLY' and status['status'] in ['COMPLETE_REVIEW_PENDING','MOCK_COMPLETE_ZERO_MODEL_INFERENCE'] and (summary['conditional']['qualified']!=frozen['counts']['conditional_admissions'] or summary['autonomous']['qualified']!=frozen['counts']['autonomous_workflows']):
                rc=1;state(status='COMPLETE_WITH_TECHNICAL_ISSUES_REVIEW_PENDING')
            if summary is not None and status['mode']!='CPU_ONLY' and status['status'] in ['COMPLETE_REVIEW_PENDING','MOCK_COMPLETE_ZERO_MODEL_INFERENCE'] and summary['matched_recovery']['technical_or_censored']:
                rc=1;state(status='COMPLETE_WITH_TECHNICAL_ISSUES_REVIEW_PENDING')
        except Exception as exc:rc=1;write(out/'analysis_failure.json',dict(error=str(exc),traceback=traceback.format_exc()))
        state(exit_code=rc)
        stop.set()
        for t in threads:t.join(timeout=35)
        controller=logs/(args.run_id+'.log')
        if controller.is_file():shutil.copy2(controller,out/'controller.log')
        try:
            archive_stop=threading.Event()
            def archive_beat():
                while not archive_stop.wait(20):print('HEARTBEAT stage=ARCHIVING raw_directory='+str(out),flush=True)
            archive_thread=threading.Thread(target=archive_beat,daemon=True);archive_thread.start()
            target=None;uploads=dict(review_bundle=None,raw_parts=None)
            if not args.defer_finalization:
                target=archive(out)
                from .uploads import make_uploads
                uploads=make_uploads(out)
            archive_stop.set();archive_thread.join(timeout=1)
            (logs/(args.run_id+'.status')).write_text(f'exit_code={rc}\nstatus={status["status"]}\nresults={out}\narchive={target}\nreview_bundle={uploads["review_bundle"]}\nraw_parts={uploads["raw_parts"]}\n')
        except Exception as exc:
            archive_stop.set()
            rc=1;state(status='ARCHIVE_FAILED_RAW_DIRECTORY_PRESERVED',archive_error=str(exc),exit_code=rc)
            (logs/(args.run_id+'.status')).write_text(f'exit_code=1\nstatus=ARCHIVE_FAILED\nresults={out}\n')
            print('Archive failed; preserve raw directory:',out,flush=True)
        if lock:lock.close()
    return rc

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True,type=Path);p.add_argument('--run-id',required=True)
    modes=p.add_mutually_exclusive_group();modes.add_argument('--cpu-only',action='store_true');modes.add_argument('--mock',action='store_true')
    p.add_argument('--lock-fd',type=int);p.add_argument('--shared-qualification',type=Path);p.add_argument('--defer-finalization',action='store_true');p.add_argument('--output',type=Path)
    p.add_argument('--cache',default=CACHE);p.add_argument('--inject-failure-block');p.add_argument('--max-collection-hours',type=float,default=None)
    args=p.parse_args()
    if args.max_collection_hours is not None and (not __import__('math').isfinite(args.max_collection_hours) or args.max_collection_hours<=0):p.error('Collection hours must be a positive finite number')
    if not re.fullmatch(r'[A-Za-z0-9_-]+',args.run_id):p.error('Invalid run ID')
    if args.inject_failure_block and not args.mock:p.error('Failure injection is mock-only')
    if args.inject_failure_block and args.inject_failure_block not in [b['id'] for b in manifest()['blocks']]+[w['id'] for w in manifest()['workflows']]:p.error('Unknown failure block')
    raise SystemExit(main(args))
