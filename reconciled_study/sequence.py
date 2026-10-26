"""One detached campaign: qualify, Qwen, owned shutdown, Gemma, audit, archive."""
from __future__ import annotations
import argparse,fcntl,json,os,re,shutil,signal,subprocess,sys,tarfile,threading,time,traceback
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from .util import write,read,PACKAGE,hash_file,Budgets
from .protocol import protocol
from .runner import execute_family
from .execution import MockHTTP
from .analysis import analyze
from .cpu import qualify
from . import serving
from .placement import qualify as placement

GPU_UUID='GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6'
CACHE='/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache'
MODELS=[('qwen','Qwen/Qwen3-32B','qwen3-32b','9216db5781bf21249d130ec9da846c4624c16137'),
        ('gemma','google/gemma-3-27b-it','gemma3-27b-it','005ad3404e59d6023443cb575daa05336842228a')]

class ModeComplete(Exception):
    def __init__(self,code):self.code=code

def server_command(python,snapshot,alias,template,family):
    cmd=[str(python),'-m','vllm.entrypoints.openai.api_server','--model',str(snapshot),'--tokenizer',str(snapshot),'--served-model-name',alias,
        '--host','127.0.0.1','--port','18080','--tensor-parallel-size','1','--dtype','bfloat16','--gpu-memory-utilization','0.90',
        '--max-model-len','32768','--max-num-seqs','4','--generation-config','vllm','--seed','20261019','--chat-template',str(template)]
    if family=='qwen':cmd+=['--enable-auto-tool-choice','--tool-call-parser','hermes']
    return cmd

def archive(out):
    sums=[hash_file(p)+'  '+str(p.relative_to(out)) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='SHA256SUMS']
    (out/'SHA256SUMS').write_text('\n'.join(sums)+'\n');target=out.with_suffix('.tar.gz');tmp=Path(str(target)+'.partial')
    print('ARCHIVING raw evidence:',out,flush=True)
    with tarfile.open(tmp,'w:gz',compresslevel=3) as t:t.add(out,arcname=out.name)
    tmp.replace(target);Path(str(target)+'.sha256').write_text(hash_file(target)+'  '+target.name+'\n')
    print('UPLOAD ARCHIVE:',target,flush=True)

def verify_package(root):
    manifest=root/'RECONCILED_PACKAGE_MANIFEST.json'
    if not manifest.is_file():raise RuntimeError('Package manifest missing')
    for name,expected in read(manifest)['files'].items():
        p=root/name
        if not p.is_file() or hash_file(p)!=expected:raise RuntimeError('Package source/asset modified: '+name)

def main(args):
    root=args.root.resolve();out=root/'results/user_runs'/args.run_id;out.mkdir(parents=True,exist_ok=False);logs=root/'logs';logs.mkdir(exist_ok=True)
    frozen=protocol();write(out/'frozen_protocol.json',frozen)
    census={s['slot_id']:'SCHEDULED_CONDITIONAL' if s['activation']!='MANDATORY' else 'SCHEDULED' for s in frozen['slots']}
    status=dict(status='STARTING',run_id=args.run_id,controller_pid=os.getpid(),gpu=3,gpu_uuid=GPU_UUID,stage='MOCK_ENGINEERING_ONLY' if args.mock else 'DEVELOPMENT',
        started_epoch=time.time(),slots=census,mandatory_workflows=120,conditional_repeats_max=12,fixed_conditions=24)
    lock=None;server=None;server_log=None;owned={};stop=threading.Event();rc=0
    def state(**kw):status.update(kw);write(out/'status.json',status)
    def progress(ident,value):
        census[ident]=value;state(active_slot=ident,status='RUNNING')
        with (out/'progress.jsonl').open('a') as f:f.write(json.dumps(dict(epoch=time.time(),id=ident,status=value))+'\n')
        print(value,ident,dict(Counter(census.values())),flush=True)
    def heartbeat():
        while not stop.wait(15):print('HEARTBEAT',status['status'],status.get('active_model',''),status.get('active_slot',''),dict(Counter(census.values())),flush=True)
    def interrupted(sig,frame):raise KeyboardInterrupt('Signal '+str(sig))
    state();signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    thread=threading.Thread(target=heartbeat,daemon=True);thread.start();telemetry=None
    try:
        lock=(logs/'gpu3_sequence.lock').open('a')
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            state(status='BLOCKED_CONCURRENT_SEQUENCE');print('Another sequence owns the GPU-3 lock. No process was stopped.',flush=True);raise ModeComplete(2)
        os.environ['CUDA_VISIBLE_DEVICES']='';os.environ['PYTHONNOUSERSITE']='1'
        verify_package(root)
        shutil.copytree(PACKAGE,out/'source/reconciled_study',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        shutil.copytree(root/'docs',out/'docs');shutil.copy2(root/'RECONCILED_PACKAGE_MANIFEST.json',out/'input_package_manifest.json')
        write(out/'research_environment.json',read_versions(sys.executable))
        state(status='CPU_QUALIFICATION')
        q=qualify(out/'cpu_qualification')
        if q['status']!='PASS':raise RuntimeError('CPU qualification failed. No model server was started.')
        if args.cpu_only:
            state(status='CPU_ONLY_COMPLETE_ZERO_MODEL_REQUESTS');raise ModeComplete(0)
        snapshots={}
        if not args.mock:
            python=root/'.venv-serving/bin/python'
            if not python.is_file():raise RuntimeError('Serving venv absent; run SETUP_RECONCILED.sh --all')
            serving_versions=read_versions(python);write(out/'serving_environment.json',serving_versions)
            installed={p['name'].lower():p['version'] for p in serving_versions}
            if installed.get('vllm')!='0.26.0':raise RuntimeError('This package requires the previously qualified vllm==0.26.0; no automatic upgrade')
            envpath=str(root/'.venv-serving/bin')+os.pathsep+os.environ.get('PATH','');os.environ['PATH']=envpath
            ninja=shutil.which('ninja')
            if not ninja:raise RuntimeError('Ninja missing from serving venv PATH')
            write(out/'ninja.json',dict(path=ninja,version=serving.command([ninja,'--version'])))
            gpu=[r for r in serving.gpu_table() if int(r[0])==3]
            if len(gpu)!=1 or gpu[0][1].strip()!=GPU_UUID:raise RuntimeError('Physical GPU 3 does not match pinned UUID; no fallback')
            if shutil.disk_usage(out).free<4*1024**3:raise RuntimeError('Less than 4 GiB free for raw evidence/archive')
            # Validate BOTH exact cached revisions before loading either model.
            for family,repo,alias,revision in MODELS:
                snapshots[family]=serving.inspect_snapshot(Path(args.cache)/('models--'+repo.replace('/','--')),repo,revision)
            write(out/'snapshot_preflight.json',{f:meta for f,(p,meta) in snapshots.items()})
            telemetry=threading.Thread(target=serving.telemetry,args=(out,stop),daemon=True);telemetry.start()
        budget=Budgets(out/'fresh_request_budget.json');write(out/'fresh_request_budget.json',dict(limits=budget.limits,used=budget.used,total=0,ceiling=8720))
        for family,repo,alias,revision in MODELS:
            serving_dir=out/family/'serving';serving_dir.mkdir(parents=True,exist_ok=True)
            try:
                if not args.mock:
                    serving.ensure_free(GPU_UUID);serving.ensure_port_free()
                    snapshot,meta=snapshots[family];template=serving_dir/'chat_template.jinja';template.write_text(meta['chat_template'])
                    cmd=server_command(root/'.venv-serving/bin/python',snapshot,alias,template,family)
                    write(serving_dir/'deployment.json',dict(**meta,command=cmd,gpu_uuid=GPU_UUID,roles=dict(actor=alias,reference=alias,judge=alias,attenuator=alias)))
                    env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES=GPU_UUID,CUDA_DEVICE_ORDER='PCI_BUS_ID',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONUNBUFFERED='1',VLLM_NO_USAGE_STATS='1',DO_NOT_TRACK='1')
                    for key in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','LD_PRELOAD'):env.pop(key,None)
                    server_log=(serving_dir/'server.log').open('w');server=subprocess.Popen(cmd,cwd=root,env=env,stdout=server_log,stderr=subprocess.STDOUT,start_new_session=True)
                    owned={server.pid:serving.proc_start(server.pid)};write(serving_dir/'owned_process.json',dict(pid=server.pid,process_group=server.pid,start=owned[server.pid]))
                    state(status='STARTING_SERVER',active_model=family);start=time.monotonic();notice=-30
                    while True:
                        if server.poll() is not None:raise RuntimeError('Owned vLLM exited. Inspect '+str(serving_dir/'server.log'))
                        try:
                            if alias in [r['id'] for r in serving.read_json_url('http://127.0.0.1:18080/v1/models').get('data',[])]:break
                        except Exception:pass
                        elapsed=time.monotonic()-start
                        if elapsed>=1800:raise RuntimeError('Server startup watchdog expired')
                        if elapsed-notice>=30:print('Waiting for',family,int(elapsed),'seconds',flush=True);notice=elapsed
                        for pid in serving.descendant_pids(server.pid):owned.setdefault(pid,serving.proc_start(pid))
                        time.sleep(3)
                    place=placement(3,18080);write(serving_dir/'placement.json',place)
                    if place['gpu_uuid']!=GPU_UUID or server.pid not in place['socket_owner_pids']:raise RuntimeError('Endpoint is not owned by this run on GPU 3')
                    for pid in serving.descendant_pids(server.pid):owned.setdefault(pid,serving.proc_start(pid))
                state(status='RUNNING',active_model=family)
                local=SimpleNamespace(root=root,model=alias,base_url='http://127.0.0.1:18080/v1',max_requests=64,generation_seed=20261019,watchdog_seconds=3600)
                from .qualification import live_transport_probes
                live_transport_probes(local,family,out/family/'published_transport_probes',budget,MockHTTP if args.mock else None)
                execute_family(local,family,out,frozen,budget,progress,MockHTTP if args.mock else None)
            except Exception as exc:
                rc=1;write(serving_dir/'failure.json',dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()));print('MODEL INFRASTRUCTURE FAILURE:',family,str(exc),flush=True)
                for s in frozen['slots']:
                    if s['model_family']==family and census[s['slot_id']].startswith('SCHEDULED'):
                        progress(s['slot_id'],'BLOCKED_MODEL_INFRASTRUCTURE')
            finally:
                if server is not None:
                    state(status='STOPPING_OWNED_SERVER',active_model=family)
                    serving.stop_owned(server,owned,serving_dir/'shutdown.json');server=None;owned={}
                if server_log is not None:server_log.close();server_log=None
                if not args.mock:
                    for attempt in range(30):
                        try:serving.ensure_free(GPU_UUID);break
                        except RuntimeError:
                            if attempt==29:raise
                            time.sleep(1)
                print('STOPPED',family,'owned server; remaining model proceeds automatically',flush=True)
        any_errors=any(v not in ('RECORDED','NOT_TRIGGERED') for v in census.values())
        state(status='MOCK_ENGINEERING_COMPLETE_NO_MODEL_EVIDENCE' if args.mock else 'FINISHED_WITH_INFRASTRUCTURE_FAILURES' if rc else 'COMPLETE_WITH_RECORDED_ERRORS_REVIEW_PENDING' if any_errors else 'COMPLETE_REVIEW_PENDING')
    except ModeComplete as done:
        rc=done.code
    except BaseException as exc:
        rc=1;state(status='INTERRUPTED' if isinstance(exc,KeyboardInterrupt) else 'FAILED',error=str(exc));write(out/'fatal_error.json',dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()));print('FAILED:',str(exc),flush=True)
    finally:
        if server is not None:
            try:serving.stop_owned(server,owned,out/'emergency_shutdown.json')
            except Exception as exc:write(out/'shutdown_failure.json',dict(error=str(exc)));rc=1
        if server_log is not None:server_log.close()
        stop.set();thread.join(timeout=2)
        if telemetry:telemetry.join(timeout=15)
        for ident,value in list(census.items()):
            if value.startswith('SCHEDULED') or value=='RUNNING':census[ident]='NOT_COMPLETED_'+status['status']
        state(exit_code=rc,finished_epoch=time.time())
        try:analyze(out,frozen)
        except Exception as exc:write(out/'analysis_failure.json',dict(error=str(exc),traceback=traceback.format_exc()));rc=1
        state(exit_code=rc)
        (logs/(args.run_id+'.status')).write_text(f'exit_code={rc}\nstatus={status["status"]}\nresults={out}\n')
        controller=logs/(args.run_id+'.log')
        if controller.is_file():shutil.copy2(controller,out/'controller.log')
        try:archive(out)
        except Exception as exc:
            rc=1;state(status='ARCHIVE_FAILED_RAW_DIRECTORY_PRESERVED',archive_error=str(exc),exit_code=rc)
            (logs/(args.run_id+'.status')).write_text(f'exit_code=1\nstatus=ARCHIVE_FAILED\nresults={out}\n');print('Archive failed; preserve raw directory:',out,flush=True)
        if lock is not None:lock.close()
    return rc

def read_versions(python):
    result=subprocess.run([str(python),'-m','pip','list','--format=json'],check=True,capture_output=True,text=True,timeout=90);return json.loads(result.stdout)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--run-id',required=True);p.add_argument('--cache',default=CACHE);p.add_argument('--cpu-only',action='store_true');p.add_argument('--mock',action='store_true');a=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+',a.run_id):p.error('Invalid run ID')
    raise SystemExit(main(a))
