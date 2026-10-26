"""One unattended job: CPU qualification, owned Qwen, 36+eligible forks, archive."""
from __future__ import annotations
import argparse,fcntl,json,os,re,shutil,signal,subprocess,sys,tarfile,threading,time,traceback
from pathlib import Path
from .common import GPU_UUID,MODEL,REVISION,CACHE,write,read,file_hash
from .protocol import manifest
from .qualify import qualify
from .runner import run_study,analyze
from . import serving

def verify_package(root):
    recorded=read(root/'NATIVE_PACKAGE_MANIFEST.json')
    for name,h in recorded['files'].items():
        p=root/name
        if not p.is_file() or file_hash(p)!=h:raise RuntimeError('Package/source file changed: '+name)
    if read(root/'protocols/NATIVE_RELEASE_MANIFEST.json')!=manifest():raise RuntimeError('Executable protocol differs from the shipped frozen manifest')
    return recorded

def server_command(python,snapshot):
    return [str(python),'-m','vllm.entrypoints.openai.api_server','--model',str(snapshot),'--tokenizer',str(snapshot),'--served-model-name',MODEL,'--host','127.0.0.1','--port','18080','--tensor-parallel-size','1','--dtype','bfloat16','--gpu-memory-utilization','0.90','--max-model-len','32768','--max-num-seqs','4','--generation-config','vllm','--override-generation-config','{"max_new_tokens":8192}','--seed','20261025','--enable-auto-tool-choice','--tool-call-parser','hermes']

def placement(server):
    descendants=serving.descendant_pids(server.pid)
    devices=serving.gpu_table();device=next((r for r in devices if int(r[0].strip())==3),None)
    if not device or device[1].strip()!=GPU_UUID:raise RuntimeError('Physical GPU 3 does not match the frozen UUID')
    sockets=serving.command(['ss','-ltnp','( sport = :18080 )'])
    listeners={int(p) for p in re.findall(r'pid=(\d+)',sockets)}
    if not listeners or not listeners<=descendants:raise RuntimeError('Cannot bind every endpoint listener to the owned server process tree')
    workers=[]
    for r in serving.gpu_applications():
        if len(r)<2 or not r[0].strip().isdigit():continue
        pid=int(r[0]);uuid=r[1].strip()
        if pid in descendants:workers.append(dict(pid=pid,gpu_uuid=uuid))
        elif uuid==GPU_UUID:raise RuntimeError('Unexpected other GPU-3 process appeared; not stopped')
    if not workers or any(w['gpu_uuid']!=GPU_UUID for w in workers):raise RuntimeError('No exclusively GPU-3 workers attributable to this server')
    return dict(qualified=True,physical_gpu=3,gpu_uuid=GPU_UUID,socket_owners=sorted(listeners),workers=workers,scope='Observed owned process tree/port/device before science; not permanent hardware attestation')

def archive(out):
    paths=[p for p in sorted(out.rglob('*')) if p.is_file() and p.name!='SHA256SUMS']
    (out/'SHA256SUMS').write_text(''.join(file_hash(p)+'  '+str(p.relative_to(out))+'\n' for p in paths))
    target=Path(str(out)+'.tar.gz');partial=Path(str(target)+'.partial')
    print('ARCHIVING raw evidence:',out,flush=True)
    with tarfile.open(partial,'w:gz',compresslevel=3) as tar:tar.add(out,arcname=out.name)
    partial.replace(target);Path(str(target)+'.sha256').write_text(file_hash(target)+'  '+target.name+'\n')
    print('UPLOAD ARCHIVE:',target,flush=True)
    return target

def main(args):
    root=args.root.resolve();out=root/'results/user_runs'/args.run_id;out.mkdir(parents=True,exist_ok=False)
    logs=root/'logs';logs.mkdir(exist_ok=True);frozen=manifest();write(out/'FROZEN_MANIFEST.json',frozen)
    census={r['id']:'SCHEDULED' for r in frozen['primary']+frozen['conditional']}
    write(out/'census.json',census)
    status=dict(status='STARTING',run_id=args.run_id,physical_gpu=3,gpu_uuid=GPU_UUID,mode='MOCK' if args.mock else 'CPU_ONLY' if args.cpu_only else 'MODEL_STUDY',started_epoch=time.time(),active_slot=None)
    lock=None;server=None;server_log=None;owned={};rc=0;stop=threading.Event();telemetry=None;heartbeat=None;console=sys.stdout
    def state(**values):status.update(values);write(out/'status.json',status)
    def beat():
        while not stop.wait(20):print(f'HEARTBEAT status={status["status"]} active={status.get("active_slot")} recorded={sum(v.startswith("RECORDED") for v in census.values())}/48 elapsed={int(time.time()-status["started_epoch"])}s',flush=True,file=console)
    def progress(ident,value,values):
        if value=='RUNNING' and server is not None and server.poll() is not None:raise RuntimeError('Owned server exited; remaining dependent slots are retained unexecuted')
        census.update(values);state(status='RUNNING_STUDY',active_slot=ident,active_slot_status=value)
    try:
        lock=(logs/'gpu3_sequence.lock').open('a')
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            state(status='BLOCKED_CONCURRENT_SEQUENCE');raise RuntimeError('Another sequence owns logs/gpu3_sequence.lock. Nothing was started or stopped.')
        verify_package(root)
        shutil.copytree(root/'release_native_study',out/'source/release_native_study',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        for name in ['RUN_NATIVE_RELEASE_GPU3.sh','VERIFY_NATIVE_RELEASE.sh','requirements-native.lock.txt','NATIVE_PACKAGE_MANIFEST.json','SCIENTIFIC_PROTOCOL.md','README_NATIVE_RELEASE.md','SOURCE_PROVENANCE.json','THIRD_PARTY_NOTICES.md','IEEE_SP_Standalone_Research_Authority_Current.md']:
            shutil.copy2(root/name,out/'source'/name)
        shutil.copytree(root/'protocols',out/'source/protocols')
        write(out/'execution_environment.json',dict(python=sys.version,executable=sys.executable,argv=sys.argv,cuda_visible_devices=os.environ.get('CUDA_VISIBLE_DEVICES'),dependencies={n:__import__('importlib.metadata',fromlist=['version']).version(n) for n in ['agentdojo','openai','pydantic']},owned_local_endpoint='http://127.0.0.1:18080/v1',profile='Qwen only for this 36+up-to-12 study; no automatic Gemma or model substitution'))
        heartbeat=threading.Thread(target=beat,daemon=True);heartbeat.start()
        signal.signal(signal.SIGTERM,lambda *_:(_ for _ in ()).throw(KeyboardInterrupt('SIGTERM: archiving partial evidence')))
        state(status='CPU_QUALIFICATION');q=qualify(out/'cpu_qualification');print('CPU QUALIFICATION:',q['status'],f'({q["tests_run"]} tests; zero model inference)',flush=True)
        if q['status']!='PASS':raise RuntimeError('CPU qualification failed; no model server started. See cpu_qualification/qualification.log')
        if args.cpu_only:
            census={k:'NOT_RUN_CPU_ONLY' for k in census};write(out/'census.json',census);state(status='CPU_QUALIFICATION_COMPLETE_NOT_MODEL_RUN')
        else:
            if not args.mock:
                python=root/'.venv-serving/bin/python'
                if not python.is_file():raise RuntimeError('Existing .venv-serving/bin/python is missing; no install or environment replacement attempted')
                device=next((r for r in serving.gpu_table() if r[0].strip()=='3'),None)
                if not device or device[1].strip()!=GPU_UUID:raise RuntimeError('GPU-3 UUID differs from frozen allocation')
                serving.ensure_free(GPU_UUID);serving.ensure_port_free()
                snapshot,metadata=serving.inspect_snapshot(Path(args.cache)/'models--Qwen--Qwen3-32B','Qwen/Qwen3-32B',REVISION);write(out/'snapshot_identity.json',metadata)
                serv=out/'serving';serv.mkdir()
                env=os.environ.copy();env.update(CUDA_DEVICE_ORDER='PCI_BUS_ID',CUDA_VISIBLE_DEVICES=GPU_UUID,HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',VLLM_NO_USAGE_STATS='1',DO_NOT_TRACK='1',HF_HUB_DISABLE_TELEMETRY='1',PATH=str(python.parent)+os.pathsep+env.get('PATH',''))
                env.pop('VLLM_API_KEY',None)  # This owned loopback-only server uses no inherited API credential.
                versions=serving.command([str(python),'-c','import torch,vllm,sys,json; print(json.dumps(dict(python=sys.version,torch=torch.__version__,vllm=vllm.__version__)))']);(serv/'versions.json').write_text(versions)
                (serv/'ninja_version.txt').write_text(subprocess.run([str(python.parent/'ninja'),'--version'],capture_output=True,text=True,check=True,timeout=20).stdout)
                help_result=subprocess.run([str(python),'-m','vllm.entrypoints.openai.api_server','--help'],capture_output=True,text=True,env=env,timeout=120,check=True);(serv/'vllm_help.txt').write_text(help_result.stdout)
                if '--override-generation-config' not in help_result.stdout:raise RuntimeError('Serving CLI lacks required output-cap option; no silent profile substitution')
                cmd=server_command(python,snapshot);write(serv/'server_command.json',dict(command=cmd,environment={k:env[k] for k in ['CUDA_VISIBLE_DEVICES','CUDA_DEVICE_ORDER','HF_HUB_OFFLINE','TRANSFORMERS_OFFLINE','VLLM_NO_USAGE_STATS']},chat_template='Unmodified selected snapshot; no enable_thinking override; source native tool serialization retained'))
                server_log=(serv/'server.log').open('w');server=subprocess.Popen(cmd,cwd=root,env=env,stdout=server_log,stderr=subprocess.STDOUT,start_new_session=True)
                owned={server.pid:serving.proc_start(server.pid)};write(serv/'owned_process.json',dict(pid=server.pid,start=owned[server.pid],process_group=server.pid))
                telemetry=threading.Thread(target=serving.telemetry,args=(out,stop),daemon=True);telemetry.start()
                state(status='STARTING_QWEN');start=time.monotonic();last_notice=-30
                while True:
                    if server.poll() is not None:raise RuntimeError('Owned vLLM exited; see serving/server.log')
                    try:
                        models=serving.read_json_url('http://127.0.0.1:18080/v1/models')
                        if any(m.get('id')==MODEL for m in models.get('data',[])):break
                    except Exception:pass
                    elapsed=time.monotonic()-start
                    if elapsed>=1800:raise RuntimeError('Qwen startup watchdog expired after 1800 seconds')
                    if elapsed-last_notice>=30:print(f'Waiting for owned Qwen server: {int(elapsed)}s; {serv}/server.log',flush=True);last_notice=elapsed
                    for pid in serving.descendant_pids(server.pid):owned.setdefault(pid,serving.proc_start(pid))
                    time.sleep(2)
                write(serv/'placement.json',placement(server));write(serv/'models.json',models)
                for pid in serving.descendant_pids(server.pid):owned.setdefault(pid,serving.proc_start(pid))
                try:write(serv/'server_info.json',serving.read_json_url('http://127.0.0.1:18080/server_info?config_format=json'))
                except Exception as exc:write(serv/'server_info.json',dict(status='UNAVAILABLE',reason=str(exc)))
                print('QUALIFIED owned Qwen on physical GPU 3. Starting complete schedule.',flush=True)
            census=run_study(out,update=progress,mock=args.mock)
            bad=any(v in ['TECHNICAL_INVALID_INITIALIZATION','CHECKPOINT_RESTORATION_FAILED'] or v.startswith('RECORDED_ERROR') or v.startswith('RECORDED_CHECKPOINT_INVALID') for v in census.values())
            if args.mock and any(v!='RECORDED_COMPLETE' for v in census.values()):
                rc=1;state(status='MOCK_ENGINEERING_FAILED',active_slot=None)
            else:state(status='MOCK_ENGINEERING_COMPLETE_ZERO_MODEL_INFERENCE' if args.mock else 'COMPLETE_WITH_RECORDED_TECHNICAL_ERRORS_REVIEW_PENDING' if bad else 'COMPLETE_REVIEW_PENDING',active_slot=None)
    except BaseException as exc:
        rc=2 if status['status']=='BLOCKED_CONCURRENT_SEQUENCE' else 1
        state(status=status['status'] if rc==2 else 'INTERRUPTED' if isinstance(exc,KeyboardInterrupt) else 'FAILED',error=str(exc))
        write(out/'fatal_error.json',dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()));print('STOP:',str(exc),flush=True)
    finally:
        if server is not None:
            try:serving.stop_owned(server,owned,out/'serving/shutdown.json');print('STOPPED owned Qwen server.',flush=True)
            except Exception as exc:rc=1;state(status='OWNED_CLEANUP_FAILED',cleanup_error=str(exc))
        if server_log is not None:server_log.close()
        stop.set()
        if heartbeat:heartbeat.join(timeout=2)
        if telemetry:telemetry.join(timeout=15)
        # Recover the incremental ledger after interruption or initialization failure.
        if (out/'census.json').exists():census=read(out/'census.json')
        for k,v in census.items():
            if v in ['SCHEDULED','RUNNING']:census[k]='NOT_COMPLETED_'+status['status']
        write(out/'census.json',census)
        state(exit_code=rc,finished_epoch=time.time())
        try:analyze(out)
        except Exception as exc:write(out/'analysis_failure.json',dict(error=str(exc)));rc=1;state(exit_code=rc)
        (logs/(args.run_id+'.status')).write_text(f'exit_code={rc}\nstatus={status["status"]}\nresults={out}\n')
        controller=logs/(args.run_id+'.log')
        if controller.is_file():shutil.copy2(controller,out/'controller.log')
        try:archive(out)
        except Exception as exc:
            rc=1;state(status='ARCHIVE_FAILED_RAW_DIRECTORY_PRESERVED',archive_error=str(exc),exit_code=rc)
            (logs/(args.run_id+'.status')).write_text(f'exit_code=1\nstatus=ARCHIVE_FAILED\nresults={out}\n');print('Archive failed; preserve raw directory:',out,flush=True)
        if lock:lock.close()
    return rc

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--run-id',required=True);p.add_argument('--cache',default=CACHE)
    modes=p.add_mutually_exclusive_group();modes.add_argument('--mock',action='store_true');modes.add_argument('--cpu-only',action='store_true');a=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+',a.run_id):p.error('Invalid run ID')
    raise SystemExit(main(a))
