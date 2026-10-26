"""One detached Qwen→Gemma campaign, bounded requests and owned-process cleanup."""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tarfile
import threading
import time
import traceback
from types import SimpleNamespace
from .common import PACKAGE,write,digest
from .protocol import protocol
from .engine import verify_runtime
from .runner import run_live,r_parent,run_r,run_historical,reconstructed_retry,fixed_route,run_j,run_p
from .analyze import analyze

sys.path.insert(0,str(PACKAGE/'vendor'))
from .vendor import serving_helpers as serving
from .vendor.qualify_gpu import qualify

GPU_UUID='GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6'
MODELS=(('qwen','Qwen/Qwen3-32B','qwen3-32b','9216db5781bf21249d130ec9da846c4624c16137'),
        ('gemma','google/gemma-3-27b-it','gemma3-27b-it','005ad3404e59d6023443cb575daa05336842228a'))
CACHE='/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache'

def check_disk(directory,record,minimum_bytes):
    usage=shutil.disk_usage(directory)
    write(record,dict(total=usage.total,used=usage.used,free=usage.free,minimum_free=minimum_bytes))
    if usage.free<minimum_bytes:
        raise RuntimeError('Insufficient free disk for raw evidence and archive; inference not started')

def server_command(python,snapshot,alias,template,family):
    cmd=[str(python),'-m','vllm.entrypoints.openai.api_server','--model',str(snapshot),'--tokenizer',str(snapshot),
        '--served-model-name',alias,'--host','127.0.0.1','--port','18080','--tensor-parallel-size','1','--dtype','bfloat16',
        '--gpu-memory-utilization','0.90','--max-model-len','32768','--max-num-seqs','4','--generation-config','vllm',
        '--seed','20261019','--chat-template',str(template)]
    if family=='qwen':cmd+=['--enable-auto-tool-choice','--tool-call-parser','hermes']
    return cmd

def atomic_archive(out):
    sums=[]
    for p in sorted(out.rglob('*')):
        if p.is_file() and p.name!='SHA256SUMS':sums.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(out)))
    (out/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    target=out.with_suffix('.tar.gz');tmp=Path(str(target)+'.partial')
    with tarfile.open(tmp,'w:gz') as t:t.add(out,arcname=out.name)
    tmp.replace(target);Path(str(target)+'.sha256').write_text(hashlib.sha256(target.read_bytes()).hexdigest()+'  '+target.name+'\n')
    print('UPLOAD ARCHIVE:',target,flush=True);return target

def execute_model(args,family,out,frozen,progress,client_factory=None):
    modeldir=out/family;modeldir.mkdir(exist_ok=True);parents={}
    lookup={r['id']:r for r in frozen['rollouts']}
    def attempt(row,target,operation):
        target.parent.mkdir(parents=True,exist_ok=True)
        write(target/'slot_status.json',dict(status='RUNNING',id=row['id'],started=time.time()))
        # Session requires a directory it can create. Slot status is kept beside
        # it transiently, then moved into the resulting directory.
        statusfile=target/'slot_status.json';pending=statusfile.read_text();statusfile.unlink();target.rmdir()
        progress(row['id'],'RUNNING');print('START',row['id'],flush=True)
        try:
            check_disk(out,target.parent/(row['id']+'_disk.json'),256*1024**2)
            result=operation()
            error=result.get('error') if isinstance(result,dict) else None
            state='RECORDED_WITH_ERROR' if error else 'RECORDED'
        except Exception as exc:
            state='UNAVAILABLE_PARENT' if isinstance(exc,(FileNotFoundError,KeyError)) else 'TECHNICAL_FAILURE'
            error=dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc())
            write(target/'failure.json',error)
        write(target/'slot_status.json',dict(status=state,id=row['id'],error=error,finished=time.time()))
        progress(row['id'],state);print('DONE',row['id'],state,flush=True)
    # Panels stay independent. Scientific negatives never suppress later work.
    for ident in frozen['execution_order']:
        row=lookup[ident]
        if row['model_family']!=family:continue
        target=modeldir/'rollouts'/ident
        panel=row['panel']
        if panel=='R':
            total=row['spec']['max_total']
            if total not in parents:
                try:parents[total]=r_parent(args,family,total,modeldir/'R_parents'/str(total),client_factory)
                except Exception as e:
                    parents[total]=e;write(modeldir/'R_parents'/str(total)/'failure.json',dict(error=str(e),traceback=traceback.format_exc()))
            def operation(row=row,target=target,total=total):
                if isinstance(parents[total],Exception):raise KeyError('Shared parent invalid: '+str(parents[total]))
                return run_r(args,row,target,parents[total],client_factory)
        elif panel.endswith('HISTORY'):
            operation=lambda row=row,target=target:run_historical(args,row,target,args.root,client_factory)
        else:operation=lambda row=row,target=target:run_live(args,row,target,client_factory)
        attempt(row,target,operation)
    for j in frozen['J']:
        if j['model_family']==family:
            target=modeldir/'J'/j['id'];attempt(j,target,lambda j=j,target=target:run_j(args,j,target,client_factory))
    for origin in frozen['P_origins']:
        if origin['model_family']==family:
            target=modeldir/'P'/origin['id'];source=modeldir/'rollouts'/origin['source_id']
            attempt(origin,target,lambda origin=origin,source=source,target=target:run_p(args,origin,source,target,client_factory))
    if family=='gemma':
        retry={}
        for origin in (1,2):
            try:retry[origin]=reconstructed_retry(args,args.root,origin,modeldir/'C_fixed_parents'/str(origin))
            except Exception as e:
                retry[origin]=e;write(modeldir/'C_fixed_parents'/str(origin)/'failure.json',dict(error=str(e),traceback=traceback.format_exc()))
        for probe in frozen['C_fixed']:
            target=modeldir/'C_FIXED'/probe['id']
            def operation(probe=probe,target=target):
                cp=retry[probe['origin']]
                if isinstance(cp,Exception):raise KeyError('No authenticated retry: '+str(cp))
                return fixed_route(args,cp,probe['route'],target,client_factory)
            attempt(probe,target,operation)

def main(args):
    args.root=args.root.resolve();root=args.root;out=root/'results/user_runs'/args.run_id
    out.mkdir(parents=True,exist_ok=False);logs=root/'logs';logs.mkdir(exist_ok=True)
    frozen=protocol();write(out/'frozen_protocol.json',dict(protocol=frozen,sha256=digest(frozen),frozen_before_inference=True))
    # Freeze status for all rollouts and all component origins before any model starts.
    census={r['id']:'SCHEDULED' for r in frozen['rollouts']};component_census={r['id']:'SCHEDULED' for key in ('J','P_origins','C_fixed') for r in frozen[key]}
    status=dict(status='STARTING',run_id=args.run_id,physical_gpu=3,gpu_uuid=GPU_UUID,
        schedule=frozen['counts'],started_epoch=time.time(),rollouts=census,components=component_census)
    def state(**kw):status.update(kw);write(out/'status.json',status)
    def progress(ident,value):
        (census if ident in census else component_census)[ident]=value
        state(active_slot=ident,status='RUNNING');
        with (out/'attempts.jsonl').open('a') as f:f.write(json.dumps(dict(id=ident,status=value,epoch=time.time()))+'\n')
    state();lock=(logs/'gpu3_sequence.lock').open('a');server=None;owned={};server_log=None;rc=0;stop=threading.Event();thread=None;telemetry=None
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        state(status='BLOCKED_CONCURRENT_SEQUENCE');atomic_archive(out);print('BLOCKED: another sequence owns the lock; no server touched.',flush=True)
        (logs/(args.run_id+'.status')).write_text('exit_code=2\nstatus=BLOCKED_CONCURRENT_SEQUENCE\n');lock.close();return 2
    def interrupted(sig,frame):raise KeyboardInterrupt('Signal '+str(sig))
    signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    def heartbeat():
        while not stop.wait(15):print('HEARTBEAT',status['status'],status.get('active_slot',''),CounterSafe(census),flush=True)
    thread=threading.Thread(target=heartbeat,daemon=True);thread.start()
    try:
        os.environ['CUDA_VISIBLE_DEVICES']='';os.environ['PYTHONNOUSERSITE']='1'
        os.environ['PATH']=str(root/'.venv-serving/bin')+os.pathsep+os.environ.get('PATH','')
        verify_runtime();shutil.copytree(PACKAGE,out/'source/authorization_study',ignore=shutil.ignore_patterns('__pycache__','*.pyc','validation'))
        check_disk(out,out/'disk_initial.json',(128 if args.cpu_only else 4096)*1024**2)
        for name in ('IEEE_SP_Final_Experiment_Design.md','IEEE_SP_Standalone_Research_Authority_Current.md','README_AUTHORIZATION.md'):
            if (root/name).is_file():shutil.copy2(root/name,out/name)
        from .qualification import run as qualify_cpu
        state(status='CPU_QUALIFICATION');q=qualify_cpu(out/'cpu_qualification')
        if q['status']!='PASS':raise RuntimeError('CPU qualification failed; model science not executed')
        if args.cpu_only:
            state(status='CPU_ONLY_NO_MODEL_RUN');return 0
        for name,python in (('research',root/'.venv/bin/python'),('serving',root/'.venv-serving/bin/python')):
            if not python.is_file():raise RuntimeError('Required existing environment absent: '+str(python))
            (out/(name+'_packages.txt')).write_text(serving.command([str(python),'-m','pip','freeze'],90))
        if not shutil.which('ninja'):raise RuntimeError('Ninja not on serving environment PATH')
        if int(Path('/proc/self/stat').read_text().split(' ',1)[0])!=os.getpid():raise RuntimeError('Cannot authenticate process namespace')
        gpu=[r for r in serving.gpu_table() if int(r[0])==3]
        if len(gpu)!=1 or gpu[0][1].strip()!=GPU_UUID:raise RuntimeError('Physical GPU 3 UUID mismatch; no fallback')
        telemetry=threading.Thread(target=serving.telemetry,args=(out,stop),daemon=True);telemetry.start()
        for family,model,alias,revision in MODELS:
            deployment=out/family/'serving';deployment.mkdir(parents=True,exist_ok=True)
            try:
                state(status='STARTING_SERVER',active_model=family)
                serving.ensure_free(GPU_UUID);serving.ensure_port_free()
                snapshot,metadata=serving.inspect_snapshot(Path(args.cache)/('models--'+model.replace('/','--')),model,revision)
                template=deployment/'chat_template.jinja';template.write_text(metadata['chat_template'])
                cmd=server_command(root/'.venv-serving/bin/python',snapshot,alias,template,family)
                write(deployment/'deployment.json',dict(**metadata,command=cmd,roles=dict(actor=alias,reference=alias,judge=alias,attenuator=alias),
                    transport='native' if family=='qwen' else 'json',scope=frozen['fidelity'],gpu_uuid=GPU_UUID))
                env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES=GPU_UUID,CUDA_DEVICE_ORDER='PCI_BUS_ID',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONUNBUFFERED='1',VLLM_NO_USAGE_STATS='1',DO_NOT_TRACK='1')
                for key in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','LD_PRELOAD'):env.pop(key,None)
                server_log=(deployment/'server.log').open('w');server=subprocess.Popen(cmd,cwd=root,env=env,stdout=server_log,stderr=subprocess.STDOUT,start_new_session=True)
                owned={server.pid:serving.proc_start(server.pid)};write(deployment/'process.json',dict(pid=server.pid,group=server.pid,start=owned[server.pid]))
                start=time.monotonic();notice=-30
                while True:
                    if server.poll() is not None:raise RuntimeError('Owned vLLM exited; inspect '+str(deployment/'server.log'))
                    try:
                        models=serving.read_json_url('http://127.0.0.1:18080/v1/models')
                        if alias in [r['id'] for r in models.get('data',[])]:break
                    except Exception:pass
                    elapsed=time.monotonic()-start
                    if elapsed>1800:raise RuntimeError('vLLM readiness timeout')
                    if elapsed-notice>=30:print(f'Waiting for {family}: {int(elapsed)}s',flush=True);notice=elapsed
                    time.sleep(3)
                placement=qualify(3,18080);write(deployment/'qualification.json',placement)
                if server.pid not in placement['socket_owner_pids']:raise RuntimeError('Endpoint not owned by this run')
                for pid in serving.descendant_pids(server.pid):owned[pid]=serving.proc_start(pid)
                local=SimpleNamespace(root=root,model=alias,base_url='http://127.0.0.1:18080/v1',max_requests=64,generation_seed=20261019,watchdog_seconds=3600)
                execute_model(local,family,out,frozen,progress)
            except Exception as e:
                rc=1;write(deployment/'failure.json',dict(error=str(e),traceback=traceback.format_exc()))
                print('MODEL FAILED:',family,str(e),'Independent other-model slots will still be attempted after cleanup.',flush=True)
            finally:
                if server:
                    serving.stop_owned(server,owned,deployment/'shutdown.json');server=None;owned={}
                if server_log:server_log.close();server_log=None
                for _ in range(30):
                    try:serving.ensure_free(GPU_UUID);break
                    except RuntimeError:time.sleep(1)
                for r in frozen['rollouts']:
                    if r['model_family']==family and census[r['id']]=='SCHEDULED':census[r['id']]='BLOCKED_MODEL_INFRASTRUCTURE'
                for key in ('J','P_origins','C_fixed'):
                    for r in frozen[key]:
                        if r.get('model_family','gemma')==family and component_census[r['id']]=='SCHEDULED':component_census[r['id']]='BLOCKED_MODEL_INFRASTRUCTURE'
                state()
        any_errors=any(v not in ('RECORDED',) for v in (*census.values(),*component_census.values()))
        state(status=('COMPLETE_WITH_RECORDED_ERRORS_REVIEW_PENDING' if any_errors else 'COMPLETE_REVIEW_PENDING') if rc==0 else 'FINISHED_WITH_INFRASTRUCTURE_FAILURES')
    except BaseException as e:
        rc=1;state(status='INTERRUPTED' if isinstance(e,KeyboardInterrupt) else 'FAILED',error=str(e));write(out/'fatal_error.json',dict(error=str(e),traceback=traceback.format_exc()))
        print('FAILED:',e,flush=True)
    finally:
        if server:
            try:serving.stop_owned(server,owned,out/'emergency_shutdown.json')
            except Exception as e:write(out/'shutdown_failure.json',dict(error=str(e)));rc=1
        if server_log:server_log.close()
        stop.set()
        if thread:thread.join(timeout=2)
        if telemetry:telemetry.join(timeout=45)
        for k in census:
            if census[k] in ('SCHEDULED','RUNNING'):census[k]='NOT_COMPLETED_'+status['status']
        for k in component_census:
            if component_census[k] in ('SCHEDULED','RUNNING'):component_census[k]='NOT_COMPLETED_'+status['status']
        state(exit_code=rc,finished_epoch=time.time())
        try:analyze(out)
        except Exception as e:write(out/'analysis_failure.json',dict(error=str(e),traceback=traceback.format_exc()));rc=1
        state(exit_code=rc)
        (logs/(args.run_id+'.status')).write_text(f'exit_code={rc}\nstatus={status["status"]}\n')
        controller=logs/(args.run_id+'.log')
        if controller.is_file():shutil.copy2(controller,out/'controller.log')
        atomic_archive(out);fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
    return rc

def CounterSafe(rows):
    from collections import Counter
    return dict(Counter(rows.values()))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--run-id',required=True);p.add_argument('--cache',default=CACHE);p.add_argument('--cpu-only',action='store_true');a=p.parse_args()
    if not a.run_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in a.run_id):p.error('Invalid run ID')
    raise SystemExit(main(a))
