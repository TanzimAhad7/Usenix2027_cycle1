"""One owned GPU-3 job, complete schedule and immutable evidence archive."""
from __future__ import annotations
import argparse,fcntl,importlib.metadata,json,os,re,shutil,signal,subprocess,sys,tarfile,threading,time,traceback
from pathlib import Path
from .common import PACKAGE,GPU_UUID,MODEL,REVISION,CACHE,read,write,file_hash
from .protocol import manifest
from .qualification import qualify
from .experiment import run_study
from .report import analyze,verify_results
from . import serving

def verify_package(root):
    recorded=read(root/'S1_PACKAGE_MANIFEST.json')
    for name,expected in recorded['files'].items():
        path=root/name
        if not path.is_file() or file_hash(path)!=expected:raise RuntimeError('Package drift: '+name)
    if manifest()!=read(root/'S1_FROZEN_MANIFEST.json'):raise RuntimeError('Protocol manifest differs from executable schedule')
    return recorded

def server_command(python,snapshot):
    return [str(python),'-m','vllm.entrypoints.openai.api_server','--model',str(snapshot),'--tokenizer',str(snapshot),
        '--served-model-name',MODEL,'--host','127.0.0.1','--port','18080','--tensor-parallel-size','1',
        '--dtype','bfloat16','--gpu-memory-utilization','0.90','--max-model-len','32768','--max-num-seqs','4',
        '--generation-config','vllm','--override-generation-config','{"max_new_tokens":8192}',
        '--seed','20261025','--enable-auto-tool-choice','--tool-call-parser','hermes']

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
    paths=[p for p in sorted(out.rglob('*')) if p.is_file() and p.name!='SHA256SUMS']
    (out/'SHA256SUMS').write_text(''.join(file_hash(p)+'  '+str(p.relative_to(out))+'\n' for p in paths))
    target=Path(str(out)+'.tar.gz');partial=Path(str(target)+'.partial')
    with tarfile.open(partial,'w:gz',compresslevel=3) as t:t.add(out,arcname=out.name,filter=lambda i:None if '__pycache__' in Path(i.name).parts else i)
    partial.replace(target);Path(str(target)+'.sha256').write_text(file_hash(target)+'  '+target.name+'\n')
    print('UPLOAD ARCHIVE:',target,flush=True);return target

def main(args):
    root=args.root.resolve();out=root/'results/user_runs'/args.run_id;out.mkdir(parents=True,exist_ok=False)
    logs=root/'logs';logs.mkdir(exist_ok=True);frozen=manifest();write(out/'FROZEN_MANIFEST.json',frozen)
    census=dict(references={b['id']:'SCHEDULED' for b in frozen['blocks']},
        admissions={i:'SCHEDULED' for b in frozen['blocks'] for i in b['admissions']})
    write(out/'census.json',census)
    status=dict(status='STARTING',mode='MOCK' if args.mock else 'CPU_ONLY' if args.cpu_only else 'MODEL_STUDY',
        started_epoch=time.time(),run_id=args.run_id,active=None,physical_gpu=3,gpu_uuid=GPU_UUID)
    lock=None;server=None;server_log=None;owned={};rc=0;stop=threading.Event();threads=[];console=sys.stdout
    def state(**values):status.update(values);write(out/'status.json',status)
    def beat():
        while not stop.wait(20):
            nr=sum(v not in ['SCHEDULED','RUNNING'] for v in census['references'].values())
            na=sum(v not in ['SCHEDULED','RUNNING'] for v in census['admissions'].values())
            print(f'HEARTBEAT stage={status["status"]} active={status.get("active")} references={nr}/32 admissions={na}/48 elapsed={int(time.time()-status["started_epoch"])}s results={out}',flush=True,file=console)
    def progress(kind,ident,value):
        if value=='RUNNING' and server is not None:
            if server.poll() is not None:raise RuntimeError('Owned model server exited; remaining slots will be marked unexecuted')
            for pid in serving.descendant_pids(server.pid):owned.setdefault(pid,serving.proc_start(pid))
        census['references' if kind=='reference' else 'admissions'][ident]=value
        write(out/'census.json',census);state(status='RUNNING_STUDY',active=ident,active_kind=kind)
    try:
        lock=(logs/'gpu3_sequence.lock').open('a')
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            state(status='BLOCKED_CONCURRENT_SEQUENCE');raise RuntimeError('Another sequence owns logs/gpu3_sequence.lock; no server started or stopped')
        verify_package(root)
        shutil.copytree(PACKAGE,out/'source/s1_reference_study',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        for name in ['RUN_S1_REFERENCE_GPU3.sh','VERIFY_S1_REFERENCE.sh','README_S1_REFERENCE.md','S1_PACKAGE_MANIFEST.json','S1_FROZEN_MANIFEST.json','requirements-s1-tested.lock.txt','THIRD_PARTY_NOTICES_S1.md','SOURCE_PROVENANCE_S1.json']:
            shutil.copy2(root/name,out/'source'/name)
        shutil.copytree(root/'docs',out/'source/docs')
        write(out/'execution_environment.json',dict(python=sys.version,executable=sys.executable,prefix=sys.prefix,
            dependencies={n:importlib.metadata.version(n) for n in ['agentdojo','openai','pydantic','httpx','tenacity']},
            research_cuda_visible_devices=os.environ.get('CUDA_VISIBLE_DEVICES'),model=MODEL,mode=status['mode']))
        t=threading.Thread(target=beat,daemon=True);threads.append(t);t.start()
        signal.signal(signal.SIGTERM,lambda *_:(_ for _ in ()).throw(KeyboardInterrupt('SIGTERM: preserving partial evidence')))
        state(status='CPU_QUALIFICATION');q,origin=qualify(out/'cpu_qualification')
        print(f'CPU QUALIFICATION: {q["status"]} ({q["tests_run"]} tests; zero model inference)',flush=True)
        if q['status']!='PASS':raise RuntimeError('CPU qualification failed; see cpu_qualification/qualification.log')
        if args.cpu_only:
            state(status='CPU_QUALIFICATION_COMPLETE_ZERO_MODEL_INFERENCE')
        else:
            if not args.mock:
                write(out/'pid_namespace.json',serving.verify_pid_namespace())
                python=root/'.venv-serving/bin/python'
                if not python.is_file():raise RuntimeError('Missing existing .venv-serving/bin/python; no install attempted')
                row=next((r for r in serving.gpu_table() if r[0].strip()=='3'),None)
                if not row or row[1].strip()!=GPU_UUID:raise RuntimeError('Frozen physical GPU-3 UUID differs')
                serving.ensure_free(GPU_UUID);serving.ensure_port_free()
                snap,identity=serving.inspect_snapshot(Path(args.cache)/'models--Qwen--Qwen3-32B','Qwen/Qwen3-32B',REVISION)
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
                    chat_template='Unmodified snapshot; no thinking override',server_output_cap=8192,server_seed=20261025,
                    model_request_seed=None,model_defaults='generation-config=vllm; source request settings retained'))
                server_log=(serv/'server.log').open('w');server=subprocess.Popen(cmd,cwd=root,env=env,stdout=server_log,stderr=subprocess.STDOUT,start_new_session=True)
                owned={server.pid:serving.proc_start(server.pid)};write(serv/'owned_process.json',dict(pid=server.pid,start=owned[server.pid],process_group=server.pid))
                t=threading.Thread(target=serving.telemetry,args=(out,stop),daemon=True);threads.append(t);t.start()
                state(status='STARTING_QWEN');started=time.monotonic();last=-30
                while True:
                    if server.poll() is not None:raise RuntimeError('Owned vLLM exited; inspect serving/server.log')
                    for pid in serving.descendant_pids(server.pid):owned.setdefault(pid,serving.proc_start(pid))
                    try:
                        models=serving.read_json_url('http://127.0.0.1:18080/v1/models')
                        if models.get('data') and models['data'][0].get('id')==MODEL:break
                    except Exception:pass
                    elapsed=time.monotonic()-started
                    if elapsed>1800:raise RuntimeError('Server startup watchdog expired after 1800s')
                    if elapsed-last>=30:print(f'Waiting for owned Qwen: {int(elapsed)}s; {serv}/server.log',flush=True);last=elapsed
                    time.sleep(2)
                write(serv/'placement.json',placement(server));write(serv/'models.json',models)
                try:write(serv/'server_info.json',serving.read_json_url('http://127.0.0.1:18080/server_info?config_format=json'))
                except Exception as exc:write(serv/'server_info.json',dict(status='UNAVAILABLE',error=str(exc)))
                print('QUALIFIED owned Qwen on physical GPU 3. Running all 32 reference blocks / 48 admissions.',flush=True)
            state(status='RUNNING_STUDY')
            run_study(out,origin,frozen,progress,mock=args.mock,failure_block=args.inject_failure_block)
            state(status='MOCK_COMPLETE_ZERO_MODEL_INFERENCE' if args.mock else 'COMPLETE_REVIEW_PENDING',active=None)
    except BaseException as exc:
        rc=2 if status['status']=='BLOCKED_CONCURRENT_SEQUENCE' else 1
        state(status=status['status'] if rc==2 else 'INTERRUPTED' if isinstance(exc,KeyboardInterrupt) else 'FAILED',error=str(exc),active=None)
        write(out/'fatal_error.json',dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()))
        print('STOP:',str(exc),flush=True)
    finally:
        if server is not None:
            try:serving.stop_owned(server,owned,out/'serving/shutdown.json');print('STOPPED owned Qwen.',flush=True)
            except Exception as exc:rc=1;state(status='OWNED_CLEANUP_FAILED',cleanup_error=str(exc))
        if server_log:server_log.close()
        stop.set()
        for t in threads:t.join(timeout=15)
        for mapping in census.values():
            for ident,value in mapping.items():
                if value in ['SCHEDULED','RUNNING']:mapping[ident]='NOT_COMPLETED_'+status['status']
        write(out/'census.json',census);state(exit_code=rc,finished_epoch=time.time(),active=None)
        try:
            summary=analyze(out);checks=verify_results(out)
            if checks['status']!='PASS':rc=1
            if status['mode']!='CPU_ONLY' and status['status'] in ['COMPLETE_REVIEW_PENDING','MOCK_COMPLETE_ZERO_MODEL_INFERENCE'] and summary['comparison_counts']['qualified']!=48:
                rc=1;state(status='COMPLETE_WITH_TECHNICAL_ISSUES_REVIEW_PENDING')
        except Exception as exc:rc=1;write(out/'analysis_failure.json',dict(error=str(exc),traceback=traceback.format_exc()))
        state(exit_code=rc)
        controller=logs/(args.run_id+'.log')
        if controller.is_file():shutil.copy2(controller,out/'controller.log')
        try:
            target=archive(out)
            (logs/(args.run_id+'.status')).write_text(f'exit_code={rc}\nstatus={status["status"]}\nresults={out}\narchive={target}\n')
        except Exception as exc:
            rc=1;state(status='ARCHIVE_FAILED_RAW_DIRECTORY_PRESERVED',archive_error=str(exc),exit_code=rc)
            (logs/(args.run_id+'.status')).write_text(f'exit_code=1\nstatus=ARCHIVE_FAILED\nresults={out}\n')
            print('Archive failed; preserve raw directory:',out,flush=True)
        if lock:lock.close()
    return rc

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True,type=Path);p.add_argument('--run-id',required=True)
    modes=p.add_mutually_exclusive_group();modes.add_argument('--cpu-only',action='store_true');modes.add_argument('--mock',action='store_true')
    p.add_argument('--cache',default=CACHE);p.add_argument('--inject-failure-block')
    args=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+',args.run_id):p.error('Invalid run ID')
    if args.inject_failure_block and not args.mock:p.error('Failure injection is mock-only')
    if args.inject_failure_block and args.inject_failure_block not in [b['id'] for b in manifest()['blocks']]:p.error('Unknown failure block')
    raise SystemExit(main(args))
