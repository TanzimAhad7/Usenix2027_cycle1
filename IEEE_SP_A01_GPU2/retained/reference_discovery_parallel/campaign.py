"""One detached, continuously locked Qwen -> Gemma campaign; no shared model state."""
from __future__ import annotations
import argparse,fcntl,json,os,re,shutil,signal,subprocess,sys,threading,time,traceback
from pathlib import Path
from .common import CACHE,GPU_UUID,digest,file_hash,read,write,append
from .models import PROFILES
from .protocol import manifest
from .execution_config import WORKERS,GPU2_UUID

def plan():
    one=manifest()
    p=dict(schema='DUAL_REFERENCE_DISCOVERY_1',model_order=['qwen','gemma'],profiles=PROFILES,
        per_model_manifest_hash=one['manifest_hash'],models=2,autonomous_workflows=688,conditional_continuations_max=60,
        per_model=dict(autonomous_workflows=344,conditional_continuations_max=30),
        slots=[dict(id=family+'::'+x['id'],model_family=family,workflow_id=x['id'],allocation_phase=x['allocation_phase']) for family in PROFILES for x in one['workflows']],
        conditional_slots=[dict(id=family+'::'+x['id'],model_family=family,fork_id=x['id']) for family in PROFILES for x in one['forks']],
        interpretation='Two model/interface profiles on the same authored contracts. Within-profile interventions are primary. Between-profile differences do not isolate model weights from interface. Origins are selected independently; no cross-model checkpoint substitution.',
        execution=dict(workflow_processes=WORKERS,model_generations='Up to two independent workflows overlap on the single GPU3 vLLM server; dependent steps within each remain ordered',start_method='spawn',checkpoint_selection='Frozen CORE order after full phase drain; completion order cannot choose origins',server_restart='Drain in-flight workflows before owned restart; failures retained, no redraws',gpu2='Pinned shared GPU2; model-free CUDA native-effect/reference-count audit only,256 MiB allocator cap,1 GiB measured process soft budget,CUDA process exits on pressure, then a separate CPU helper drains evidence'),
        optimization='One shared native CPU qualification, two isolated concurrent episode processes within each sequentially served model, complete asynchronous diagnostic tokenization, shared source snapshot, no inter-model archive/analysis, one final full archive plus review. No scientific condition removal, lower output cap, changed sampling parameters, quantization or response sharing. Actual batching/RNG execution changes are declared, not bit-identical to serial runs.')
    p['manifest_hash']=digest(p);return p

def child_command(args,family,out,lock_fd,remaining=None):
    cmd=[sys.executable,'-u','-m','reference_discovery_parallel.sequence','--root',str(args.root),
        '--run-id',args.run_id+'_'+family,'--cache',args.cache,'--output',str(out/'models'/family),
        '--shared-qualification',str(out/'cpu_qualification'),'--lock-fd',str(lock_fd),'--defer-finalization']
    if args.mock:cmd+=['--mock']
    if remaining is not None:cmd+=['--max-collection-hours',str(max(remaining,0.001)/3600)]
    return cmd

def main(args):
    root=args.root.resolve();out=root/'results/user_runs'/args.run_id;logs=root/'logs'
    logs.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=False)
    args.root=root;frozen=plan();write(out/'FROZEN_MANIFEST.json',frozen)
    status=dict(status='STARTING',run_id=args.run_id,controller_pid=os.getpid(),mode='MOCK' if args.mock else 'CPU_ONLY' if args.cpu_only else 'MODEL_STUDY',
        started_epoch=time.time(),physical_gpu=3,gpu_uuid=GPU_UUID,active_model=None,models={f:'SCHEDULED' for f in PROFILES},scheduled_autonomous=688,scheduled_conditional_max=60)
    census={x['id']:'SCHEDULED' for x in frozen['slots']+frozen['conditional_slots']};write(out/'census.json',census)
    lock=None;child=None;child_thread=None;rc=0;stop=threading.Event();interrupted=False
    auditor=None;auditor_log=None;auditor_start=None
    deadline=None if args.max_collection_hours is None else time.monotonic()+args.max_collection_hours*3600
    def state(**kw):
        status.update(kw);write(out/'status.json',status)
        append(out/'status_events.jsonl',dict(epoch=time.time(),**kw))
    def on_signal(sig,*_):
        nonlocal interrupted
        interrupted=True
        if child is not None and child.poll() is None:child.send_signal(signal.SIGTERM)
        raise KeyboardInterrupt('Campaign signal '+str(sig)+'; child will preserve evidence and stop its owned server')
    def beat():
        while not stop.wait(20):
            family=status.get('active_model');p=out/'models'/str(family)/'status.json'
            try:detail=read(p) if p.exists() else {}
            except Exception:detail={}
            count=0
            for f in PROFILES:
                cp=out/'models'/f/'census.json'
                try:count+=sum(v not in ('SCHEDULED','RUNNING') for v in read(cp)['workflows'].values()) if cp.exists() else 0
                except Exception:pass
            try:audit_status=read(out/'gpu2_audit/status.json') if (out/'gpu2_audit/status.json').exists() else {}
            except Exception:audit_status={}
            print(f'HEARTBEAT status={status["status"]} model={family} active={detail.get("active_cases",detail.get("active"))} terminal_autonomous={count}/688 workflow_workers={WORKERS} audit_backend={audit_status.get("backend")} audited={audit_status.get("recorded",0)} elapsed={int(time.time()-status["started_epoch"])}s',flush=True)
    def refresh_census():
        for family in PROFILES:
            p=out/'models'/family/'census.json'
            data=read(p) if p.exists() else None
            for slot in frozen['slots']+frozen['conditional_slots']:
                if slot['model_family']!=family:continue
                local=slot.get('workflow_id',slot.get('fork_id'));group='workflows' if 'workflow_id' in slot else 'forks'
                census[slot['id']]=data[group].get(local,'NOT_COMPLETED_MISSING_CENSUS') if data else 'NOT_EXECUTED_'+status['models'][family]
        write(out/'census.json',census)
    def audit_cpu_fallback():
        nonlocal auditor,auditor_start
        if auditor is None or auditor.poll()!=75:return
        from .base.serving import proc_start
        previous=auditor.pid;auditor.wait()
        env=os.environ.copy();env['CUDA_VISIBLE_DEVICES']=''
        command=[str(root/'.venv-serving/bin/python'),'-u','-m','reference_discovery_parallel.gpu2_audit','--out',str(out),'--stop-file',str(out/'AUDIT_COLLECTION_FINISHED'),'--cpu-only']
        auditor=subprocess.Popen(command,cwd=root,env=env,stdout=auditor_log,stderr=subprocess.STDOUT,start_new_session=True)
        auditor_start=proc_start(auditor.pid)
        append(out/'gpu2_audit/process_history.jsonl',dict(epoch=time.time(),previous_cuda_pid=previous,cpu_pid=auditor.pid,start=auditor_start,command=command,cuda_visible_devices='',old_cuda_process_exited=True))
        print('GPU2 audit yielded the shared device. Separate CPU helper will drain all preserved evidence; no inference changes.',flush=True)
    state();signal.signal(signal.SIGTERM,on_signal);signal.signal(signal.SIGINT,on_signal)
    heartbeat=threading.Thread(target=beat,daemon=True);heartbeat.start()
    try:
        lock=(logs/'gpu3_sequence.lock').open('a')
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            state(status='BLOCKED_CONCURRENT_SEQUENCE');raise RuntimeError('Another sequence owns GPU-3 lock; no server started or stopped')
        from .integrity import verify_package
        record=verify_package(root)
        if frozen!=read(root/'PARALLEL_REFERENCE_FROZEN_MANIFEST.json'):raise RuntimeError('Dual plan differs from executable')
        for name in list(record['files'])+['PARALLEL_REFERENCE_PACKAGE_MANIFEST.json']:
            target=out/'source'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/name,target)
        state(status='CPU_QUALIFICATION')
        import unittest,contextlib
        from .operational_tests import Operations
        with (out/'operational_tests.log').open('w') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
            operations=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Operations))
        write(out/'operational_tests.json',dict(status='PASS' if operations.wasSuccessful() else 'FAIL',tests_run=operations.testsRun,model_inference=0))
        if not operations.wasSuccessful():raise RuntimeError('Operational qualification failed; inspect operational_tests.log')
        from .qualification import qualify
        from .runtime_receipt import runtime_digest
        qualification,_=qualify(out/'cpu_qualification')
        print(f'CPU QUALIFICATION: {qualification["status"]}; {qualification["tests_run"]} tests, zero inference; shared across both profiles',flush=True)
        if qualification['status']!='PASS':
            for failure in qualification.get('failures',[]):
                print('FAILED TEST:',failure['test'],flush=True)
                print(failure['traceback'],flush=True)
            retained=read(out/'cpu_qualification/retained_source/qualification.json')
            for failure in retained.get('details',[]):
                print('FAILED RETAINED TEST:',failure['test'],flush=True)
                print(failure['traceback'],flush=True)
            raise RuntimeError('CPU qualification failed; no GPU model started')
        write(out/'cpu_qualification/receipt.json',dict(package_sha256=file_hash(root/'PARALLEL_REFERENCE_PACKAGE_MANIFEST.json'),qualification_sha256=file_hash(out/'cpu_qualification/qualification.json'),python=sys.executable,runtime_source_digest=runtime_digest()))
        if not args.cpu_only and not args.mock:
            from .base import serving
            state(status='PREFLIGHT_BOTH_MODELS')
            write(out/'pid_namespace.json',serving.verify_pid_namespace())
            serving.ensure_free(GPU_UUID);serving.ensure_port_free()
            python=root/'.venv-serving/bin/python'
            if not python.is_file():raise RuntimeError('Missing existing serving venv; no installation attempted')
            snapshots={}
            for family,profile in PROFILES.items():
                snapshot,identity=serving.inspect_snapshot(Path(args.cache)/('models--'+profile['hub'].replace('/','--')),profile['hub'],profile['revision'])
                snapshots[family]=identity
                cmd=[str(python),'-m','reference_discovery_parallel.models','--snapshot',str(snapshot),'--family',family,'--out',str(out/'template_qualification'/family)]
                env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES='',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
                (out/'template_qualification'/family).mkdir(parents=True,exist_ok=True)
                result=subprocess.run(cmd,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180)
                (out/'template_qualification'/family/'process.log').write_text(result.stdout)
                if result.returncode:
                    print('TEMPLATE PREFLIGHT ERROR ['+family+']:',flush=True)
                    print(result.stdout,flush=True)
                    raise RuntimeError('Cached template/profile qualification failed for '+family+'; inspect template_qualification')
            write(out/'snapshot_preflight.json',snapshots)
            audit_dir=out/'gpu2_audit';audit_dir.mkdir(exist_ok=True)
            audit_cmd=[str(python),'-u','-m','reference_discovery_parallel.gpu2_audit','--out',str(out),'--stop-file',str(out/'AUDIT_COLLECTION_FINISHED')]
            audit_env=os.environ.copy();audit_env.update(CUDA_VISIBLE_DEVICES=GPU2_UUID,CUDA_DEVICE_ORDER='PCI_BUS_ID',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
            auditor_log=(audit_dir/'process.log').open('w')
            auditor=subprocess.Popen(audit_cmd,cwd=root,env=audit_env,stdout=auditor_log,stderr=subprocess.STDOUT,start_new_session=True)
            auditor_start=serving.proc_start(auditor.pid)
            write(audit_dir/'owned_process.json',dict(pid=auditor.pid,start=auditor_start,command=audit_cmd,cuda_visible_devices=GPU2_UUID,model_weights=False,vllm=False))
            print('GPU2: low-memory integer evidence audit started; no model/vLLM. GPU3: two independent workflow processes per model.',flush=True)
        if args.cpu_only:state(status='CPU_QUALIFICATION_COMPLETE_ZERO_MODEL_INFERENCE')
        else:
            for family in PROFILES:
                if interrupted:break
                remaining=None if deadline is None else deadline-time.monotonic()
                if remaining is not None and remaining<=0:
                    status['models'][family]='NOT_EXECUTED_USER_TIME_LIMIT';continue
                state(status='COLLECTING',active_model=family)
                env=os.environ.copy();env['REFERENCE_DISCOVERY_MODEL_FAMILY']=family
                cmd=child_command(args,family,out,lock.fileno(),remaining)
                write(out/(family+'_worker_command.json'),dict(command=cmd,model_family=family,model_profile=PROFILES[family]))
                worker_log=logs/(args.run_id+'_'+family+'.log')
                child=subprocess.Popen(cmd,cwd=root,env=env,pass_fds=(lock.fileno(),),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
                write(out/(family+'_worker_process.json'),dict(pid=child.pid,log=str(worker_log)))
                def pump(process=child,path=worker_log,label=family):
                    with path.open('w') as log:
                        for line in process.stdout:
                            log.write(line);log.flush();print('['+label+'] '+line,end='',flush=True)
                child_thread=threading.Thread(target=pump,daemon=True);child_thread.start()
                code=child.wait();child_thread.join();child=None
                audit_cpu_fallback()
                write(out/(family+'_worker_exit.json'),dict(exit_code=code))
                p=out/'models'/family/'status.json';local=read(p) if p.exists() else {}
                status['models'][family]=local.get('status','WORKER_FAILED_BEFORE_STATUS');rc=max(rc,int(code!=0))
                refresh_census();state(active_model=None)
                # A scientific or technical failure is retained; it does not
                # suppress the other model. Ownership ambiguity DOES stop all.
                if local.get('status')=='OWNED_CLEANUP_FAILED':raise RuntimeError('Owned shutdown failed; Gemma must not start over an ambiguous server')
            limited=any(v in ('TIME_BUDGET_REACHED','NOT_EXECUTED_USER_TIME_LIMIT') for v in status['models'].values())
            state(status='USER_TIME_LIMIT_REACHED' if limited else 'COLLECTION_COMPLETE_ANALYSIS_PENDING',active_model=None)
    except BaseException as exc:
        rc=2 if status['status']=='BLOCKED_CONCURRENT_SEQUENCE' else 1
        state(status=status['status'] if rc==2 else 'INTERRUPTED' if isinstance(exc,KeyboardInterrupt) else 'FAILED',error=str(exc))
        write(out/'fatal_error.json',dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()));print('STOP:',str(exc),flush=True)
    finally:
        if child is not None and child.poll() is None:
            child.send_signal(signal.SIGTERM)
            try:child.wait(timeout=180)
            except subprocess.TimeoutExpired:
                state(status='CHILD_CLEANUP_UNCONFIRMED');print('Child did not confirm cleanup. Parent retains lock until child exits; preserve raw directory.',flush=True)
                child.wait()
        if child_thread:child_thread.join(timeout=5)
        if auditor is not None:
            audit_cpu_fallback()
            (out/'AUDIT_COLLECTION_FINISHED').write_text('Collection and owned model shutdown completed; drain available native evidence.\n')
            try:
                auditor.wait(timeout=120)
                if auditor.returncode==75:
                    audit_cpu_fallback();auditor.wait(timeout=120)
            except subprocess.TimeoutExpired:
                from .base.serving import proc_start
                if auditor_start is not None and proc_start(auditor.pid)==auditor_start:auditor.terminate()
                try:auditor.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    if auditor_start is not None and proc_start(auditor.pid)==auditor_start:auditor.kill()
                    auditor.wait(timeout=15)
                write(out/'gpu2_audit/drain_incomplete.json',dict(status='INCOMPLETE_AUDIT_RAW_EVIDENCE_PRESERVED',scope='Only authenticated audit process stopped; never a model or foreign process'))
                rc=max(rc,1)
            if auditor.returncode:rc=max(rc,1)
            if auditor_log:auditor_log.close()
            p=out/'gpu2_audit/status.json'
            if p.exists() and (read(p).get('disagreements') or read(p).get('errors')):rc=max(rc,1)
        refresh_census()
        try:
            from .combined import finalize
            if args.cpu_only:
                state(exit_code=rc,finished_epoch=time.time())
            else:
                analysis=finalize(out)
                if analysis['technical_issues']:rc=max(rc,1)
                if status['status']=='COLLECTION_COMPLETE_ANALYSIS_PENDING':
                    state(status='COMPLETE_WITH_TECHNICAL_ISSUES_REVIEW_PENDING' if rc else 'MOCK_COMPLETE_ZERO_MODEL_INFERENCE' if args.mock else 'COMPLETE_REVIEW_PENDING')
                state(exit_code=rc,finished_epoch=time.time(),active_model=None)
            # No server remains. Release GPU lock before CPU-only compression.
            if lock:lock.close();lock=None
            state(packaging='SEE_EXTERNAL_COMPLETION_RECEIPT',packaging_receipt=str(out)+'.packaging.json')
            controller=logs/(args.run_id+'.log')
            if controller.is_file():shutil.copy2(controller,out/'controller.log')
            from .packaging import package
            outputs=package(out,raw_parts=args.raw_parts)
            # Completion receipt is external to immutable archive contents.
            (logs/(args.run_id+'.status')).write_text(f'exit_code={rc}\nstatus={status["status"]}\nresults={out}\narchive={outputs["archive"]}\nreview_bundle={outputs["review_bundle"]}\nraw_parts={outputs.get("raw_parts")}\npackaging=COMPLETE\n')
            print('COMPLETE UPLOAD ARCHIVE:',outputs['archive'],flush=True);print('COMPACT REVIEW:',outputs['review_bundle'],flush=True)
        except BaseException as exc:
            rc=1;write(out/'finalization_failure.json',dict(error=str(exc),traceback=traceback.format_exc()))
            (logs/(args.run_id+'.status')).write_text(f'exit_code=1\nstatus=FINALIZATION_FAILED_RAW_PRESERVED\nresults={out}\n')
            print('Finalization failed; raw evidence preserved:',out,str(exc),flush=True)
        if lock:lock.close()
        stop.set();heartbeat.join(timeout=1)
    return rc

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True,type=Path);p.add_argument('--run-id',required=True);p.add_argument('--cache',default=CACHE)
    mode=p.add_mutually_exclusive_group();mode.add_argument('--cpu-only',action='store_true');mode.add_argument('--mock',action='store_true')
    p.add_argument('--raw-parts',action='store_true');p.add_argument('--max-collection-hours',type=float,default=None)
    a=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+',a.run_id):p.error('Invalid run ID')
    if a.max_collection_hours is not None and (not __import__('math').isfinite(a.max_collection_hours) or a.max_collection_hours<=0):p.error('Collection hours must be positive and finite')
    raise SystemExit(main(a))
