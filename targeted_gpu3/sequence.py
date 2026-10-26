"""GPU-3-only sequential serving; reuse the tested ownership/cache helpers."""
import argparse
import collections
import csv
import fcntl
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
import traceback
from types import SimpleNamespace
from .core import PACKAGE,transport,verify_sources,digest
from .experiment import run_family,run_exhaustion,schedule
import sequence as retained
from qualify_gpu import qualify

PINNED=[('qwen','Qwen/Qwen3-32B','qwen3-32b','9216db5781bf21249d130ec9da846c4624c16137'),
        ('gemma','google/gemma-3-27b-it','gemma3-27b-it','005ad3404e59d6023443cb575daa05336842228a')]
GPU_UUID='GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6'


def server_command(serving,snapshot,alias,template,family):
    cmd=[str(serving),'-m','vllm.entrypoints.openai.api_server','--model',str(snapshot),'--tokenizer',str(snapshot),
        '--served-model-name',alias,'--host','127.0.0.1','--port','18080','--tensor-parallel-size','1','--dtype','bfloat16',
        '--gpu-memory-utilization','0.90','--max-model-len','32768','--max-num-seqs','4','--generation-config','vllm',
        '--seed','20261019','--chat-template',str(template)]
    if family=='qwen':cmd+=['--enable-auto-tool-choice','--tool-call-parser','hermes']
    return cmd


def reusable_qualification(path):
    path=Path(path).resolve();records={}
    manifest={}
    for line in (path/'SHA256SUMS').read_text().splitlines():
        sha,relative=line.split('  ',1);manifest[relative]=sha
    def verified(file):
        actual=retained.hash_file(file)
        if manifest.get(str(file.relative_to(path)))!=actual:raise RuntimeError('Previous evidence hash mismatch: '+str(file))
        return actual
    for name in ('core.py','experiment.py','schedule.json','RETAINED_MANIFEST.json'):
        previous=path/'source/targeted_gpu3'/name
        if not previous.is_file() or verified(previous)!=retained.hash_file(PACKAGE/name):
            raise RuntimeError('Qualification source differs or is missing: '+str(previous))
    for family,model,alias,revision in PINNED:
        decision=path/family/'experiment/decision.json';deployment=path/family/'deployment.json'
        data=json.loads(decision.read_text());identity=json.loads(deployment.read_text())
        if not data['configuration_qualified'] or identity['revision']!=revision or identity['gpu_uuid']!=GPU_UUID:
            raise RuntimeError('Previous configuration is not qualified for '+family)
        records[family]=dict(decision=data,decision_sha256=verified(decision),
                             deployment=identity,deployment_sha256=verified(deployment))
    return dict(path=str(path),evidence='REUSED_QUALIFICATION_NOT_NEW_EPISODES',records=records)


def summarize(out):
    episodes=[];references=[]
    for family,_,_,_ in PINNED:
        p=out/family/'experiment/qualification_results.json'
        if p.is_file():
            for r in json.loads(p.read_text()):
                episodes.append(dict(model=family,episode=r['item']['id'],scheduling=r['scheduling'],
                    case=r['item']['task'],requests=r['requests'],error=(r['error'] or {}).get('type',''),
                    violation=r['outcome']['violation'],observed_forbidden_commit=r['independent_violation'],**r['outcome']['violations'],
                    completion=r['outcome']['completion'],secure_completion=r['outcome']['secure_completion'],
                    lifecycle_closed=r['outcome']['lifecycle_closed'],evidence='AUTONOMOUS_ADAPTED_DEVELOPMENT'))
        p=out/family/'experiment/reference_results.json'
        if p.is_file():
            for r in json.loads(p.read_text()):
                c=r['comparison'];references.append(dict(model=family,arm=r['item']['arm'],seed=r['item']['seed'],
                    status=c['status'],requests=r['result']['requests'],Y=c.get('Y_excess_release','UNKNOWN'),
                    V=c.get('V_forbidden_component_commit','UNKNOWN'),
                    M1=c.get('M1',{}).get('violation','UNKNOWN'),M2=c.get('M2',{}).get('violation','UNKNOWN'),
                    evidence='CONDITIONAL_REFERENCE_FORCED_BATCH'))
    for name,rows in [('episodes',episodes),('reference_probes',references)]:
        transport.write(out/(name+'.json'),rows)
        with (out/(name+'.csv')).open('w',newline='') as f:
            if rows:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    reuse=(out/'reused_qualification.json').is_file()
    planned=[] if reuse else schedule()['qualification_episodes'];recorded={x['episode'] for x in episodes}
    transport.write(out/'unrecorded_qualification_rows.json',[r for r in planned if r['id'] not in recorded])
    done={(r['model'],r['arm'],r['seed']) for r in references}
    transport.write(out/'unrecorded_reference_rows.json',[r for r in ([] if reuse else schedule()['reference_probes'])
        if (r['model'],r['arm'],r['seed']) not in done])
    text=['# Targeted GPU 3 development findings','',f'Recorded NEW configuration episodes: {len(episodes)}/{len(planned)}.',
          f'Recorded NEW conditional reference probes: {len(references)}/{0 if reuse else 45}.',
          'Qualification was reused, not rerun.' if reuse else 'Qualification belongs to this campaign.',
          'No independent task-population rate or confirmation is established.',
          'All roles change jointly with model family; native Qwen versus JSON Gemma is an interface difference.',
          'No reference checkpoint was substituted based on new probe outcomes. Unqualified rows retain reasons.',
          'Reference V is a forced batch component effect; it is not a fresh autonomous attack episode.',
          'Human semantic review remains PENDING. Inspect raw references, edit maps, receipts and per-model decision.json.',
          'Focal occurrence release is separate from excess: if an earlier sibling is blocked, a later occurrence may still be legal.',
          '', 'The next scientific decision follows the recorded gate: config repetition, reference path, matched exhaustion, native significance, or narrowing.']
    (out/'FINDINGS.md').write_text('\n'.join(text)+'\n')


def main(args):
    root=args.root.resolve();out=root/'results/user_runs'/args.run_id;out.mkdir(parents=True,exist_ok=False)
    logs=root/'logs';logs.mkdir(exist_ok=True);lock=(logs/'gpu3_sequence.lock').open('a')
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        transport.write(out/'status.json',dict(status='BLOCKED_CONCURRENT_SEQUENCE'))
        (logs/(args.run_id+'.status')).write_text(f'exit_code=2\nstatus=BLOCKED_CONCURRENT_SEQUENCE\nresults={out}\n')
        print('BLOCKED: another GPU 3 sequence holds the lock; no process was stopped.',flush=True)
        retained.archive(out);lock.close();return 2
    server=None;server_log=None;owned={};thread=None;stop=threading.Event();rc=0
    reuse_path=getattr(args,'exhaustion_from',None)
    status=dict(status='STARTING',run_id=args.run_id,gpu=3,models=[],exhaustion_selected=args.exhaustion or bool(reuse_path),
                maximum_generation_attempts=244 if reuse_path else 728 if args.exhaustion else 484)
    def state(**kw):status.update(kw);transport.write(out/'status.json',status)
    def interrupt(signum,frame):raise KeyboardInterrupt('Controller interrupted by signal '+str(signum))
    signal.signal(signal.SIGTERM,interrupt);signal.signal(signal.SIGINT,interrupt)
    def heartbeat():
        while not stop.wait(15):print('HEARTBEAT',status.get('status'),status.get('active_model',''),time.strftime('%H:%M:%S',time.gmtime()),flush=True)
    try:
        state();os.environ['CUDA_VISIBLE_DEVICES']=''
        os.environ['PATH']=str(root/'.venv-serving/bin')+os.pathsep+os.environ.get('PATH','')
        verify_sources()
        reuse=reusable_qualification(reuse_path) if reuse_path else None
        if reuse:transport.write(out/'reused_qualification.json',reuse)
        for executable in [root/'.venv/bin/python',root/'.venv-serving/bin/python']:
            if not executable.is_file():raise RuntimeError('Existing project interpreter missing: '+str(executable))
        ninja=shutil.which('ninja')
        if not ninja:raise RuntimeError('Ninja not on serving venv PATH; environments were not modified')
        (out/'ninja_version.txt').write_text(retained.command([ninja,'--version']))
        source=out/'source';source.mkdir();shutil.copytree(PACKAGE,source/'targeted_gpu3',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        transport.write(out/'frozen_protocol.json',dict(schedule=schedule(),sha256=digest(schedule()),
            exhaustion_selected=args.exhaustion or bool(reuse),qualification_reused=bool(reuse),
            fresh_qualification_rows=[] if reuse else schedule()['qualification_episodes']))
        print('CPU: running new effect-level controls; no model calls',flush=True)
        from .controls import run
        run(out/'cpu_controls')
        for name,exe in [('research',sys.executable),('serving',str(root/'.venv-serving/bin/python'))]:
            (out/(name+'_packages.txt')).write_text(retained.command([exe,'-m','pip','freeze'],timeout=90))
        devices=retained.gpu_table();chosen=[r for r in devices if int(r[0])==3]
        if len(chosen)!=1 or chosen[0][1].strip()!=GPU_UUID:raise RuntimeError('Physical GPU 3 UUID differs from qualified allocation')
        transport.write(out/'gpu_initial.json',devices);retained.ensure_free(GPU_UUID);retained.ensure_port_free()
        snapshots={}
        for family,model,alias,revision in PINNED:
            directory=Path(args.cache).expanduser().resolve()/('models--'+model.replace('/','--'))
            snapshots[family]=retained.inspect_snapshot(directory,model,revision)
        thread=threading.Thread(target=heartbeat,daemon=True);thread.start()
        telemetry=threading.Thread(target=retained.telemetry,args=(out,stop),daemon=True);telemetry.start()
        for family,model,alias,revision in PINNED:
            directory=out/family;directory.mkdir();snapshot,metadata=snapshots[family]
            retained.ensure_free(GPU_UUID);retained.ensure_port_free();state(status='STARTING_SERVER',active_model=family)
            template=directory/'server_chat_template.jinja';template.write_text(metadata['chat_template'])
            cmd=server_command(root/'.venv-serving/bin/python',snapshot,alias,template,family)
            transport.write(directory/'deployment.json',dict(**metadata,server_command=cmd,gpu_index=3,gpu_uuid=GPU_UUID,
                inference_roles='actor/shadow/attenuator/judge all active model',requested_logprobs=False,effective_logprobs=False))
            env=os.environ.copy();env.update(CUDA_DEVICE_ORDER='PCI_BUS_ID',CUDA_VISIBLE_DEVICES=GPU_UUID,
                HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONNOUSERSITE='1',PYTHONUNBUFFERED='1',
                VLLM_NO_USAGE_STATS='1',DO_NOT_TRACK='1')
            for key in ['PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','LD_PRELOAD']:env.pop(key,None)
            server_log=(directory/'server.log').open('w')
            server=subprocess.Popen(cmd,cwd=root,env=env,stdout=server_log,stderr=subprocess.STDOUT,start_new_session=True)
            owned={server.pid:retained.proc_start(server.pid)}
            transport.write(directory/'server_process.json',dict(pid=server.pid,process_group=server.pid))
            started=time.monotonic();notice=0
            while True:
                if server.poll() is not None:raise RuntimeError(f'{family} server exited; inspect {directory}/server.log')
                try:
                    models=retained.read_json_url('http://127.0.0.1:18080/v1/models')
                    if alias in [x['id'] for x in models.get('data',[])]:break
                except Exception:pass
                elapsed=time.monotonic()-started
                if elapsed>1800:raise RuntimeError('Server startup timeout')
                if elapsed-notice>=30 or notice==0:
                    print(f'Waiting for {family}: {int(elapsed)}s; {directory}/server.log',flush=True);notice=max(1,elapsed)
                time.sleep(3)
            transport.write(directory/'models_endpoint.json',models)
            qualified=qualify(3,18080);transport.write(directory/'gpu_qualification.json',qualified)
            if server.pid not in qualified['socket_owner_pids']:raise RuntimeError('Endpoint is not owned by this controller server')
            for pid in retained.descendant_pids(server.pid):owned[pid]=retained.proc_start(pid)
            try:transport.write(directory/'server_version.json',retained.read_json_url('http://127.0.0.1:18080/version'))
            except Exception as e:transport.write(directory/'server_version.json',dict(error=str(e)))
            state(status='RUNNING_EXPERIMENT',active_model=family)
            local=SimpleNamespace(family=family,model=alias,mode='native' if family=='qwen' else 'json',
                                  base_url='http://127.0.0.1:18080/v1',max_requests=32)
            if reuse:
                experiment=directory/'experiment';experiment.mkdir()
                matched=run_exhaustion(local,experiment/'exhaustion')
                decision=dict(status='DEVELOPMENT_COMPLETE_WITH_ERRORS' if matched['errors'] else 'DEVELOPMENT_COMPLETE',
                    configuration_qualified=True,qualification_reused=True,qualification_generations=0,
                    reference_generations=0,exhaustion=matched,requires_config_repair=False,human_review='PENDING')
                transport.write(experiment/'decision.json',decision)
            else:decision=run_family(local,directory/'experiment',exhaustion=args.exhaustion)
            status['models'].append(dict(family=family,decision=decision))
            if decision['status'].endswith('ERRORS') or decision['requires_config_repair']:rc=3
            state(status='STOPPING_SERVER')
            retained.stop_owned(server,owned,directory/'shutdown.json');server=None;owned={}
            server_log.close();server_log=None
            for attempt in range(30):
                try:retained.ensure_free(GPU_UUID);break
                except RuntimeError:
                    if attempt==29:raise
                    time.sleep(1)
            print('STOPPED',family,'owned server; next model uses the same physical GPU 3',flush=True)
        state(status='DEVELOPMENT_COMPLETE_WITH_ERRORS' if rc else 'DEVELOPMENT_COMPLETE')
    except BaseException as e:
        rc=1;transport.write(out/'fatal_error.json',dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc()))
        state(status='INTERRUPTED' if isinstance(e,KeyboardInterrupt) else 'FAILED',error=str(e))
        print('FAILED:',str(e),flush=True)
        if server_log:
            server_log.flush();print('\n'.join(Path(server_log.name).read_text(errors='replace').splitlines()[-30:]),flush=True)
    finally:
        if server:
            try:retained.stop_owned(server,owned,out/'emergency_shutdown.json')
            except Exception as e:transport.write(out/'shutdown_error.json',dict(error=str(e)));rc=1
        if server_log:server_log.close()
        stop.set()
        if thread:thread.join(timeout=2)
        if 'telemetry' in locals():telemetry.join(timeout=20)
        try:transport.write(out/'gpu_final.json',retained.gpu_table())
        except Exception as e:transport.write(out/'gpu_final_error.json',dict(error=str(e)))
        try:summarize(out)
        except Exception as e:transport.write(out/'summary_error.json',dict(error=str(e)));rc=1
        status.update(exit_code=rc,finished_epoch=time.time());transport.write(out/'status.json',status)
        (logs/(args.run_id+'.status')).write_text(f'exit_code={rc}\nstatus={status["status"]}\nresults={out}\n')
        controller=logs/(args.run_id+'.log')
        if controller.is_file():shutil.copy2(controller,out/'controller.log')
        try:retained.archive(out)
        except Exception as e:
            rc=1;status.update(exit_code=rc,archive_error=str(e));transport.write(out/'status.json',status)
            (logs/(args.run_id+'.status')).write_text(f'exit_code=1\nstatus=ARCHIVE_FAILED\nresults={out}\n')
            print('Archive failed; raw directory preserved:',out,str(e),flush=True)
        lock.close()
    return rc


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--run-id',required=True)
    p.add_argument('--cache',default=retained.DEFAULT_CACHE)
    select=p.add_mutually_exclusive_group();select.add_argument('--exhaustion',action='store_true')
    select.add_argument('--exhaustion-from',type=Path)
    args=p.parse_args()
    if not args.run_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in args.run_id):p.error('Invalid run ID')
    sys.exit(main(args))
