#!/usr/bin/env python3
"""Own two sequential vLLM processes on physical GPU 3 and retain evidence."""
import argparse
import collections
import csv
import fcntl
import hashlib
import importlib.metadata
import io
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import tarfile
import threading
import time
import traceback
import urllib.request

GPU=3
PORT=18080
DEFAULT_CACHE='/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache'
MODELS=[('qwen','Qwen/Qwen3-32B','qwen3-32b'),('gemma','google/gemma-3-27b-it','gemma3-27b-it')]


def write(path,value):
    path=Path(path);tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(value,indent=2,default=str)+'\n');tmp.replace(path)


def command(argv,timeout=30):
    r=subprocess.run(argv,capture_output=True,text=True,timeout=timeout)
    if r.returncode: raise RuntimeError(f'{argv[0]} failed ({r.returncode}): {r.stderr}')
    return r.stdout


def hash_file(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def cache_snapshot(cache,model):
    directory=cache/('models--'+model.replace('/','--'))
    ref=directory/'refs/main'
    if ref.is_file():
        snap,record=inspect_snapshot(directory,model,ref.read_text().strip())
        record['revision_resolution']='cached refs/main'
        return snap,record
    valid=[];rejected={}
    for candidate in sorted((directory/'snapshots').glob('*')):
        if not candidate.is_dir():continue
        try:valid.append(inspect_snapshot(directory,model,candidate.name))
        except (RuntimeError,ValueError,OSError,KeyError) as exc:rejected[candidate.name]=str(exc)
    if len(valid)!=1:
        raise RuntimeError(f'{model}: refs/main absent; found {len(valid)} complete snapshots. '
                           f'Complete: {[str(p) for p,r in valid]}; rejected: {rejected}')
    snap,record=valid[0]
    record['revision_resolution']='unique complete local snapshot; refs/main absent'
    record['rejected_snapshots']=rejected
    return snap,record


def inspect_snapshot(directory,model,revision):
    if not revision or '/' in revision or revision in ('.','..'):
        raise RuntimeError('Invalid cached model revision')
    snap=directory/'snapshots'/revision
    if not snap.is_dir(): raise RuntimeError(f'Cached snapshot missing: {snap}')
    required=['config.json','tokenizer_config.json','tokenizer.json']
    for name in required:
        if not (snap/name).is_file(): raise RuntimeError(f'Incomplete cache: {snap/name}')
    indices=list(snap.glob('*.safetensors.index.json'))
    shards=set()
    for index in indices: shards.update(json.loads(index.read_text())['weight_map'].values())
    if not shards: shards={p.name for p in snap.glob('*.safetensors')}
    if not shards: raise RuntimeError(f'No cached safetensors weights for {model}')
    for name in shards:
        p=snap/name
        if not p.is_file() or p.stat().st_size==0: raise RuntimeError(f'Missing/empty weight shard: {p}')
    files=[]
    for p in sorted(snap.rglob('*')):
        if p.is_file():
            entry=dict(name=str(p.relative_to(snap)),bytes=p.stat().st_size,symlink=os.readlink(p) if p.is_symlink() else None)
            if p.stat().st_size<20_000_000: entry['sha256']=hash_file(p)
            files.append(entry)
    tc=json.loads((snap/'tokenizer_config.json').read_text())
    template=tc.get('chat_template')
    tj=snap/'chat_template.json'
    if tj.is_file(): template=json.loads(tj.read_text()).get('chat_template',template)
    tf=snap/'chat_template.jinja'
    if tf.is_file(): template=tf.read_text()
    if template is None: raise RuntimeError(f'No cached chat template for {model}')
    if isinstance(template,dict):template=template.get('default')
    if not isinstance(template,str):raise RuntimeError(f'A single default text template is required for {model}')
    serialized=template
    return snap,dict(hub_model=model,revision=revision,snapshot=str(snap),files=files,
                     weight_hash_policy='Cache blob names and shard presence/size; large weights not reread for digest',
                     chat_template=template,chat_template_sha256=hashlib.sha256(serialized.encode()).hexdigest())


def gpu_table():
    return list(csv.reader(io.StringIO(command(['nvidia-smi','--query-gpu=index,uuid,memory.used,memory.total','--format=csv,noheader,nounits']))))


def gpu_applications():
    return list(csv.reader(io.StringIO(command(['nvidia-smi','--query-compute-apps=pid,gpu_uuid,used_gpu_memory','--format=csv,noheader,nounits']))))


def ensure_free(uuid):
    occupied=[r for r in gpu_applications() if len(r)>1 and r[1].strip()==uuid]
    if occupied: raise RuntimeError('GPU 3 has existing compute processes; none were stopped: '+str(occupied))


def ensure_port_free():
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        try: s.bind(('127.0.0.1',PORT))
        except OSError as e: raise RuntimeError(f'Port {PORT} occupied; existing service is not used or stopped') from e


def read_json_url(url):
    with urllib.request.urlopen(url,timeout=5) as r: return json.load(r)


def descendant_pids(parent):
    pairs={int(p):int(pp) for p,pp in (line.split() for line in command(['ps','-eo','pid=,ppid=']).splitlines() if len(line.split())==2)}
    found={parent}
    while True:
        updated=found|{p for p,pp in pairs.items() if pp in found}
        if updated==found:return found
        found=updated


def proc_start(pid):
    try:
        fields=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
        return None if fields[0]=='Z' else fields[19]
    except (FileNotFoundError,IndexError): return None


def stop_owned(server,owned,record):
    if server is None:return
    # Capture child identity before parent exits. Never use a global pkill.
    try:
        for pid in descendant_pids(server.pid): owned.setdefault(pid,proc_start(pid))
    except Exception: pass
    for sig,wait in [(signal.SIGTERM,40),(signal.SIGKILL,15)]:
        try: os.killpg(server.pid,sig)
        except ProcessLookupError: pass
        for pid,start in owned.items():
            if start is not None and proc_start(pid)==start:
                try: os.kill(pid,sig)
                except ProcessLookupError: pass
        end=time.time()+wait
        while time.time()<end:
            server.poll()
            if not any(start is not None and proc_start(pid)==start for pid,start in owned.items()):break
            time.sleep(.5)
    try: server.wait(timeout=5)
    except subprocess.TimeoutExpired: pass
    remaining=[pid for pid,start in owned.items() if start is not None and proc_start(pid)==start]
    write(record,dict(server_pid=server.pid,returncode=server.poll(),remaining_owned_pids=remaining))
    if remaining:raise RuntimeError('Owned server processes did not stop: '+str(remaining))


def telemetry(out,stop):
    while not stop.is_set():
        try:
            rows=command(['nvidia-smi','--query-gpu=index,uuid,timestamp,utilization.gpu,memory.used,memory.total,power.draw','--format=csv,noheader,nounits'])
            with (out/'gpu_telemetry.csv').open('a') as f:
                for row in csv.reader(io.StringIO(rows)):
                    if row and row[0].strip()==str(GPU):f.write(','.join(row)+'\n');f.flush()
        except Exception as e:
            with (out/'telemetry_errors.log').open('a') as f:f.write(str(e)+'\n')
        stop.wait(10)


def summarize(out):
    rows=[]
    for family,_,_ in MODELS:
        path=out/family/'diagnostic/results.json'
        if path.is_file():rows.extend(json.loads(path.read_text()))
    by=collections.defaultdict(list)
    for r in rows:by[(r['model'],r['condition'],r['variant'])].append(r)
    table=[]
    for key,rs in sorted(by.items()):
        table.append(dict(zip(['model','condition','variant'],key),episodes=len(rs),
             violations=sum(r['outcome']['violation'] is True for r in rs),
             unknown=sum(r['outcome']['violation']=='UNKNOWN' for r in rs),
             secure_completion=sum(bool(r['outcome']['secure_completion']) for r in rs),
             errors=sum(bool(r['error']) for r in rs),payload_delivered=sum(bool(r['payload_delivered']) for r in rs),
             requests=sum(r['requests'] for r in rs)))
    write(out/'summary.json',table)
    with (out/'summary.csv').open('w',newline='') as f:
        if table:
            writer=csv.DictWriter(f,fieldnames=list(table[0]));writer.writeheader();writer.writerows(table)
    lines=['# GPU 3 sequential development diagnostic','',
           'Custom simulated payment workflows. Human semantic review remains pending.',
           'Actor, shadow, and auxiliaries all change together between models; differences are not an isolated actor-model causal effect.',
           'Two temperature-zero repetitions are repeated executions, not independent tasks. No population inference or holdout claim.','',
           f'Recorded episodes: {len(rows)}',f'Observed unauthorized-effect episodes: {sum(r["outcome"]["violation"] is True for r in rows)}',
           f'Unknown-effect-free episodes: {sum(r["outcome"]["violation"]=="UNKNOWN" for r in rows)}','',
           'Inspect summary.csv, each result.json and effects.json, then events.jsonl and HTTP request/response files.',
           'A fixed-payload null does not rule out the mechanism. Inspect payload delivery, proposal reachability, review decisions, release, and commit separately.']
    (out/'FINDINGS.md').write_text('\n'.join(lines)+'\n')


def archive(out):
    hashes=[]
    for p in sorted(out.rglob('*')):
        if p.is_file() and p.name!='SHA256SUMS': hashes.append(hash_file(p)+'  '+str(p.relative_to(out)))
    (out/'SHA256SUMS').write_text('\n'.join(hashes)+'\n')
    target=out.with_suffix('.tar.gz')
    with tarfile.open(target,'w:gz') as z:z.add(out,arcname=out.name)
    Path(str(target)+'.sha256').write_text(hash_file(target)+'  '+target.name+'\n')
    print('UPLOAD ARCHIVE:',target,flush=True)


def main(args):
    root=args.root.resolve();out=root/'results/user_runs'/args.run_id
    out.mkdir(parents=True,exist_ok=False)
    logs=root/'logs';logs.mkdir(exist_ok=True)
    lock=(logs/'gpu3_sequence.lock').open('a')
    try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        write(out/'status.json',dict(status='BLOCKED_CONCURRENT_SEQUENCE'));lock.close();return 2
    server=None;owned={};runner=None;server_log=None;telemetry_stop=threading.Event();thread=None;exitcode=0
    status=dict(status='STARTING',gpu=GPU,run_id=args.run_id,started_epoch=time.time(),models=[])
    def state(**values):status.update(values);write(out/'status.json',status)
    def interrupted(signum,frame):raise KeyboardInterrupt('Sequence interrupted by signal '+str(signum))
    signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    try:
        os.environ['CUDA_VISIBLE_DEVICES']='' # Research/client process is CPU-only.
        (out/'controller.log').touch()
        source=out/'source';source.mkdir()
        for rel in ['automation_gpu3','experiments/review_binding','scripts/qualify_gpu.py','requirements-research.lock.txt','docs/RESEARCH_PLAN.md']:
            p=root/rel
            if p.is_dir():shutil.copytree(p,source/rel,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            elif p.is_file():
                dest=source/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
        # Early source verification; no repetition of completed historical studies.
        sys.path.insert(0,str(root/'experiments/review_binding'))
        import diagnostic
        diagnostic.verify_runtime()
        serving=root/'.venv-serving/bin/python'
        if not serving.is_file():raise RuntimeError('Existing serving venv is missing')
        packages=command([str(serving),'-m','pip','freeze'],timeout=90)
        (out/'serving_packages.txt').write_text(packages)
        (out/'research_packages.txt').write_text(command([sys.executable,'-m','pip','freeze'],timeout=90))
        rows=gpu_table();selected=[r for r in rows if int(r[0])==GPU]
        if len(selected)!=1:raise RuntimeError('Physical GPU 3 not found')
        uuid=selected[0][1].strip();write(out/'gpu_initial.json',rows)
        ensure_free(uuid);ensure_port_free()
        # Check BOTH caches before spending time on either experiment.
        snapshots={}
        for family,model,alias in MODELS:
            snap,record=cache_snapshot(Path(args.cache).resolve(),model)
            snapshots[family]=(snap,record)
        write(out/'schedule.json',dict(models=MODELS,repeats=2,episodes_per_model=30,total_planned_episodes=60,
             conditions=3,variants=5,gpu_index=GPU,gpu_uuid=uuid,port=PORT,cache=args.cache,
             transport='SHARED_TEXT_JSON_ACTIONS_V1',stage='DEVELOPMENT',retry=False,
             launch_context='Existing local caches; no network download or external old source/venv dependency'))
        thread=threading.Thread(target=telemetry,args=(out,telemetry_stop),daemon=True);thread.start()
        for family,model,alias in MODELS:
            directory=out/family;directory.mkdir();snap,record=snapshots[family]
            ensure_free(uuid);ensure_port_free()
            state(status='STARTING_SERVER',active_model=family)
            template_path=directory/'server_chat_template.jinja';template_path.write_text(record['chat_template'])
            shutil.copy2(snap/'config.json',directory/'model_config.json')
            if (snap/'generation_config.json').is_file():shutil.copy2(snap/'generation_config.json',directory/'cached_generation_config.json')
            cmd=[str(serving),'-m','vllm.entrypoints.openai.api_server','--model',str(snap),'--tokenizer',str(snap),
                 '--served-model-name',alias,'--host','127.0.0.1','--port',str(PORT),
                 '--tensor-parallel-size','1','--dtype','bfloat16','--gpu-memory-utilization','0.90',
                 '--max-model-len','32768','--max-num-seqs','4','--generation-config','vllm','--seed','20261019',
                 '--chat-template',str(template_path)]
            write(directory/'deployment.json',dict(**record,model_id=alias,model_revision=record['revision'],
                 tokenizer_revision=record['revision'],server_command=cmd,gpu_index=GPU,gpu_uuid=uuid,
                 transport='SHARED_TEXT_JSON_ACTIONS_V1',qwen_enable_thinking=False,exact_logprobs=False))
            env=os.environ.copy()
            env.update(CUDA_DEVICE_ORDER='PCI_BUS_ID',CUDA_VISIBLE_DEVICES=uuid,HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',
                       PYTHONNOUSERSITE='1',PYTHONUNBUFFERED='1',VLLM_NO_USAGE_STATS='1',DO_NOT_TRACK='1')
            for key in ['PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','LD_PRELOAD']:env.pop(key,None)
            server_log=(directory/'server.log').open('w')
            print('START',family,'GPU',GPU,uuid,'snapshot',snap,flush=True)
            server=subprocess.Popen(cmd,stdout=server_log,stderr=subprocess.STDOUT,env=env,start_new_session=True,cwd=root)
            owned={server.pid:proc_start(server.pid)}
            write(directory/'server_process.json',dict(pid=server.pid,process_group=server.pid))
            started=time.time();last_notice=0
            while True:
                if server.poll() is not None:raise RuntimeError(f'{family} server exited; see {directory}/server.log')
                try:
                    data=read_json_url(f'http://127.0.0.1:{PORT}/v1/models')
                    if alias in [m['id'] for m in data.get('data',[])]:break
                except Exception:pass
                if time.time()-started>1800:raise RuntimeError(f'{family} startup timeout; logs preserved')
                if time.time()-last_notice>30:
                    print('Waiting for',family,'server; elapsed',int(time.time()-started),'seconds',flush=True);last_notice=time.time()
                time.sleep(3)
            write(directory/'models_endpoint.json',data)
            try:write(directory/'server_version.json',read_json_url(f'http://127.0.0.1:{PORT}/version'))
            except Exception as e:write(directory/'server_version.json',dict(error=str(e)))
            sys.path.insert(0,str(root/'scripts'))
            from qualify_gpu import qualify
            qualification=qualify(GPU,PORT);write(directory/'gpu_qualification.json',qualification)
            if server.pid not in qualification['socket_owner_pids']:
                raise RuntimeError('Endpoint socket not owned by this server process')
            for pid in descendant_pids(server.pid):owned[pid]=proc_start(pid)
            # Save effective native chat template via local tokenizer. This is
            # provenance, not a second model load or inference.
            code='''import sys,json,hashlib
from pathlib import Path
from transformers import AutoTokenizer
t=AutoTokenizer.from_pretrained(sys.argv[1],local_files_only=True)
loaded=t.chat_template
template=Path(sys.argv[2]).read_text()
t.chat_template=template
render=t.apply_chat_template([dict(role='system',content='System example.'),dict(role='user',content='User example.')],tokenize=False,add_generation_prompt=True)
print(json.dumps(dict(tokenizer_class=type(t).__name__,loaded_template=loaded,server_cli_template=template,rendered_example=render,chat_template_sha256=hashlib.sha256(template.encode()).hexdigest())))
'''
            (directory/'effective_tokenizer_template.json').write_text(command([str(serving),'-c',code,str(snap),str(template_path)],timeout=120))
            state(status='RUNNING_DIAGNOSTIC',active_model=family)
            run_cmd=[sys.executable,'-u',str(root/'automation_gpu3/diagnostic_runner.py'),'--root',str(root),
                 '--out',str(directory/'diagnostic'),'--model',alias,'--family',family,'--repeats','2']
            write(directory/'runner_command.json',run_cmd)
            with (directory/'diagnostic.log').open('w') as log:
                runner=subprocess.Popen(run_cmd,stdout=log,stderr=subprocess.STDOUT,cwd=root,env={**os.environ,'CUDA_VISIBLE_DEVICES':''},start_new_session=True)
                while runner.poll() is None:
                    try:
                        partial=json.loads((directory/'diagnostic/results.json').read_text()); n=len(partial)
                    except (FileNotFoundError,json.JSONDecodeError):n=0
                    print(f'{family}: {n}/30 episodes recorded; diagnostic log: {directory}/diagnostic.log',flush=True)
                    time.sleep(15)
                rc=runner.returncode;runner=None
            status['models'].append(dict(family=family,runner_exit_code=rc));state(status='STOPPING_SERVER')
            exitcode=max(exitcode,rc)
            stop_owned(server,owned,directory/'shutdown.json');server=None;owned={}
            server_log.close();server_log=None
            # Wait for the exact owned GPU workers to disappear before next model.
            ensure_free(uuid);print('STOPPED',family,flush=True)
        state(status='COMPLETE_WITH_ERRORS' if exitcode else 'COMPLETE',finished_epoch=time.time())
    except BaseException as e:
        exitcode=1
        write(out/'fatal_error.json',dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc()))
        state(status='INTERRUPTED' if isinstance(e,KeyboardInterrupt) else 'FAILED',error=str(e),finished_epoch=time.time())
        print('FAILED:',str(e),flush=True)
    finally:
        if runner is not None:
            try:os.killpg(runner.pid,signal.SIGTERM);runner.wait(timeout=20)
            except subprocess.TimeoutExpired:
                os.killpg(runner.pid,signal.SIGKILL);runner.wait()
            except ProcessLookupError:pass
        if server is not None:
            try:stop_owned(server,owned,out/'emergency_shutdown.json')
            except Exception as e:write(out/'shutdown_error.json',dict(error=str(e)));exitcode=1
        if server_log is not None:server_log.close()
        telemetry_stop.set()
        if thread:thread.join(timeout=20)
        try:
            write(out/'gpu_final.json',gpu_table())
            summarize(out)
        except Exception as e:write(out/'summary_error.json',dict(error=str(e)));exitcode=1
        source_log=logs/(args.run_id+'.log')
        if source_log.is_file():shutil.copy2(source_log,out/'controller.log')
        status['exit_code']=exitcode;write(out/'status.json',status)
        (logs/(args.run_id+'.status')).write_text(f'exit_code={exitcode}\nstatus={status["status"]}\nresults={out}\n')
        try:archive(out)
        except Exception as e:
            print('Archive failed; raw directory remains:',out,str(e),flush=True);exitcode=1
            status['exit_code']=exitcode;status['archive_error']=str(e);write(out/'status.json',status)
            (logs/(args.run_id+'.status')).write_text(f'exit_code={exitcode}\nstatus=ARCHIVE_FAILED\nresults={out}\n')
        lock.close()
    return exitcode


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--run-id',required=True)
    p.add_argument('--cache',default=DEFAULT_CACHE)
    args=p.parse_args()
    if not args.run_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in args.run_id):p.error('Invalid run ID')
    sys.exit(main(args))
