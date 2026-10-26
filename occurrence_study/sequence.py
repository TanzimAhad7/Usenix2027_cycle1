"""Own local vLLM servers on physical GPU 3; finite, staged, archived runs."""
from __future__ import annotations
import argparse
import csv
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import threading
import time
import traceback
from types import SimpleNamespace
from .common import PACKAGE,write,digest
from .protocol import protocol,schedule
from .engine import Session,verify_runtime
from .study import probe_workflow,qualification,lawful_recovery,feedback_sensitivity

sys.path.insert(0,str(PACKAGE/'vendor'))
from .vendor import serving_helpers as serving
from .vendor.qualify_gpu import qualify

GPU_UUID='GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6'
MODELS=[('qwen','Qwen/Qwen3-32B','qwen3-32b','9216db5781bf21249d130ec9da846c4624c16137'),
        ('gemma','google/gemma-3-27b-it','gemma3-27b-it','005ad3404e59d6023443cb575daa05336842228a')]

def verify_process_namespace():
    if int(Path('/proc/self/stat').read_text().split(' ',1)[0])!=os.getpid():
        raise RuntimeError('PID namespace and /proc disagree; safe server ownership cannot be established')

def server_command(python,snapshot,alias,template,family):
    result=[str(python),'-m','vllm.entrypoints.openai.api_server','--model',str(snapshot),'--tokenizer',str(snapshot),
        '--served-model-name',alias,'--host','127.0.0.1','--port','18080','--tensor-parallel-size','1',
        '--dtype','bfloat16','--gpu-memory-utilization','0.90','--max-model-len','32768','--max-num-seqs','4',
        '--generation-config','vllm','--seed','20261022','--chat-template',str(template)]
    if family=='qwen':result+=['--enable-auto-tool-choice','--tool-call-parser','hermes']
    return result

def summarize(out):
    rows=[]
    for path in sorted(out.glob('*/workflows/*/result.json')):
        r=json.loads(path.read_text());rows.append(dict(id=r['item']['id'],model=r['item']['model_family'],
          structure=r['item']['spec']['structure'],instance=r['item']['spec']['instance'],
          condition=r['item']['spec']['condition'],defense=r['item']['defense'],
          outcome=r['outcome']['status'],effects=r['outcome']['effects'],secure_completion=r['outcome']['secure_completion'],
          error=(r['error'] or {}).get('type'),carrier_reached=r['carrier_reached'],
          checkpoint=r['checkpoint_disposition'],fresh_generations=r['fresh_model_generations'],feedback=r['feedback']))
    write(out/'episodes.json',rows)
    with (out/'episodes.csv').open('w',newline='') as f:
        if rows:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    done={r['id'] for r in rows}
    attempt_file=out/'attempts.jsonl'
    attempted={json.loads(line)['id'] for line in attempt_file.read_text().splitlines()} if attempt_file.exists() else set()
    write(out/'unexecuted_schedule.json',[dict(**r,disposition='STARTED_WITHOUT_RESULT_SEE_FATAL' if r['id'] in attempted else
        'NOT_EXECUTED_BY_STAGE_GATE_OR_FAILURE') for r in schedule() if r['id'] not in done])
    lines=['# Prospective occurrence-attribution study findings','',f'Recorded core workflows: {len(rows)}/96.',
       f'Observed violation workflows: {sum(r["outcome"]=="VIOLATION" for r in rows)}.',
       f'Secure completions: {sum(r["secure_completion"] for r in rows)}.',
       f'Unknown workflows: {sum(r["outcome"]=="UNKNOWN" for r in rows)}.','',
       'These are authored tasks and joint actor/reference/auxiliary configurations. Qwen native and Gemma JSON differ.',
       'No population rate, commercial deployment claim, independent confirmation or complete-defense claim is established.',
       'The email sink is stock AgentDojo; task construction, transport, hooks and any feedback correction are documented adaptations.',
       'Component checkpoints, scripted lawful prefixes and reused responses are not additional autonomous episodes.',
       'Inspect stage decisions, every protected/failed attempt, primitive commits and UNKNOWN reasons before interpreting totals.',
       'Human semantic review: PENDING.']
    (out/'FINDINGS.md').write_text('\n'.join(lines)+'\n')

def main(args):
    root=args.root.resolve();out=root/'results/user_runs'/args.run_id;out.mkdir(parents=True,exist_ok=False)
    logs=root/'logs';logs.mkdir(exist_ok=True);lock=(logs/'gpu3_sequence.lock').open('a')
    server=None;server_log=None;owned={};rc=0;stop=threading.Event();status=dict(status='STARTING',run_id=args.run_id,
        gpu=3,scope=args.scope,feedback=args.feedback,models=[],completed=0,diagnostic_failures=0,workflow_errors=0)
    def state(**kw):status.update(kw);write(out/'status.json',status)
    def diagnostic(operation,directory):
        try:
            result=operation()
            if isinstance(result,dict) and result.get('diagnostic_failures'):
                status['diagnostic_failures']+=result['diagnostic_failures'];state()
            return result
        except Exception as exc:
            row=dict(status='DIAGNOSTIC_FAILED',error=dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()))
            write(directory/'failure.json',row);status['diagnostic_failures']+=1;state()
            print('DIAGNOSTIC FAILED; remaining scheduled work continues:',directory,str(exc),flush=True);return row
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        state(status='BLOCKED_CONCURRENT_SEQUENCE',exit_code=2)
        (logs/(args.run_id+'.status')).write_text('exit_code=2\nstatus=BLOCKED_CONCURRENT_SEQUENCE\n')
        serving.archive(out);lock.close();print('BLOCKED: existing sequence retained; no process stopped.',flush=True);return 2
    def interrupted(sig,frame):raise KeyboardInterrupt('Signal '+str(sig))
    signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    def heartbeat():
        while not stop.wait(15):print('HEARTBEAT',status['status'],status.get('active_model',''),status['completed'],'workflows recorded',flush=True)
    thread=threading.Thread(target=heartbeat,daemon=True);thread.start()
    telemetry=None
    try:
        os.environ['CUDA_VISIBLE_DEVICES']='';os.environ['PYTHONNOUSERSITE']='1'
        os.environ['PATH']=str(root/'.venv-serving/bin')+os.pathsep+os.environ.get('PATH','')
        verify_runtime();state(status='CPU_QUALIFICATION')
        shutil.copytree(PACKAGE,out/'source/occurrence_study',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        frozen=protocol();requested_feedback=args.feedback
        from .cpu import run as cpu_run
        cpu=cpu_run(out/'cpu_qualification')
        if cpu['status']!='PASS':raise RuntimeError('CPU integration qualification failed')
        if requested_feedback=='auto':args.feedback='occurrence' if cpu['source_feedback_alias_detected'] else 'original'
        selection=dict(requested=requested_feedback,selected=args.feedback,admission='ORIGINAL_M0',
            reason='PRE_INFERENCE_CPU_RECEIPT_COMPATIBILITY' if requested_feedback=='auto' else 'EXPLICIT_PROFILE',
            source_feedback_alias_detected=cpu['source_feedback_alias_detected'])
        write(out/'feedback_selection.json',selection);state(feedback=args.feedback)
        write(out/'frozen_protocol.json',dict(protocol=frozen,sha256=digest(frozen),selected_scope=args.scope,
            feedback_selection=selection,source_admission='ORIGINAL',configuration_scope='RESEARCH_ADAPTATION_NOT_BENCHMARK_REPRODUCTION'))
        print('PROFILE:',json.dumps(selection),flush=True)
        for name,python in [('research',root/'.venv/bin/python'),('serving',root/'.venv-serving/bin/python')]:
            if not python.is_file():raise RuntimeError('Existing environment missing: '+str(python))
            (out/(name+'_packages.txt')).write_text(serving.command([str(python),'-m','pip','freeze'],90))
        ninja=shutil.which('ninja')
        if not ninja:raise RuntimeError('Ninja absent from existing serving PATH; environments not modified')
        (out/'ninja_version.txt').write_text(serving.command([ninja,'--version']))
        verify_process_namespace()
        gpu=[r for r in serving.gpu_table() if int(r[0])==3]
        if len(gpu)!=1 or gpu[0][1].strip()!=GPU_UUID:raise RuntimeError('Physical GPU 3 UUID differs from pinned allocation')
        serving.ensure_free(GPU_UUID);serving.ensure_port_free()
        write(out/'gpu_initial.json',serving.gpu_table())
        telemetry=threading.Thread(target=serving.telemetry,args=(out,stop),daemon=True);telemetry.start()
        global_feedback_parents=set()
        # All requested instances per model before shutdown: two server starts,
        # no task-success/positive-result gate and no resume/import of old data.
        jobs=[(*m,1) for m in MODELS if args.scope!='qualification' or m[0]=='qwen']
        for family,model,alias,revision,instance in jobs:
            directory=out/family;directory.mkdir(exist_ok=True)
            deployment_dir=directory/f'serving_i{instance}';deployment_dir.mkdir()
            state(status='STARTING_SERVER',active_model=family,instance=instance)
            snapshot,metadata=serving.inspect_snapshot(Path(args.cache)/('models--'+model.replace('/','--')),model,revision)
            template=deployment_dir/'server_chat_template.jinja';template.write_text(metadata['chat_template'])
            cmd=server_command(root/'.venv-serving/bin/python',snapshot,alias,template,family)
            write(deployment_dir/'deployment.json',dict(**metadata,server_command=cmd,physical_gpu=3,gpu_uuid=GPU_UUID,
                actor=alias,reference=alias,attenuator=alias,judge=alias,transport='native' if family=='qwen' else 'json',
                declared_deviations='Authored tasks, fixed simulator clock, local-role configuration, transport/hooks; feedback='+args.feedback))
            env=os.environ.copy();env.update(CUDA_DEVICE_ORDER='PCI_BUS_ID',CUDA_VISIBLE_DEVICES=GPU_UUID,
                HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONUNBUFFERED='1',VLLM_NO_USAGE_STATS='1',DO_NOT_TRACK='1')
            for key in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','LD_PRELOAD'):env.pop(key,None)
            server_log=(deployment_dir/'server.log').open('w')
            server=subprocess.Popen(cmd,cwd=root,env=env,stdout=server_log,stderr=subprocess.STDOUT,start_new_session=True)
            owned={server.pid:serving.proc_start(server.pid)};write(deployment_dir/'server_process.json',dict(pid=server.pid,process_group=server.pid))
            start=time.monotonic();last_notice=-30
            while True:
                if server.poll() is not None:raise RuntimeError(f'{family} server exited; see {deployment_dir}/server.log')
                try:
                    models=serving.read_json_url('http://127.0.0.1:18080/v1/models')
                    if alias in [r['id'] for r in models.get('data',[])]:break
                except Exception:pass
                elapsed=time.monotonic()-start
                if elapsed>1800:raise RuntimeError('Serving startup exceeded 1800s')
                if elapsed-last_notice>=30:print(f'Waiting for {family}: {int(elapsed)}s; {deployment_dir}/server.log',flush=True);last_notice=elapsed
                time.sleep(3)
            write(deployment_dir/'models_endpoint.json',models)
            placement=qualify(3,18080);write(deployment_dir/'gpu_qualification.json',placement)
            if server.pid not in placement['socket_owner_pids']:raise RuntimeError('Endpoint is not this owned server')
            for pid in serving.descendant_pids(server.pid):owned[pid]=serving.proc_start(pid)
            local=SimpleNamespace(model=alias,base_url='http://127.0.0.1:18080/v1',max_requests=64,feedback=args.feedback)
            rows=[];diagnostics=[];feedback_count=0
            planned=[r for r in schedule() if r['model_family']==family]
            phases=[('qualification6',[r for r in planned if r['spec']['instance']==1 and r['spec']['structure']=='E-BEFORE'])]
            if args.scope!='qualification':
                phases.append(('structural48',[r for r in planned if r['spec']['instance']==1 and r['spec']['structure']!='E-BEFORE']))
            if args.scope=='full':phases.append(('expansion96',[r for r in planned if r['spec']['instance']==2]))
            qualified=False
            for phase,items in phases:
                for item in items:
                    state(status='RUNNING_'+phase.upper(),active_episode=item['id'],instance=item['spec']['instance'])
                    print('START',item['id'],flush=True)
                    with (out/'attempts.jsonl').open('a') as ledger:
                        ledger.write(json.dumps(dict(id=item['id'],stage=phase,status='STARTED',epoch=time.time()))+'\n');ledger.flush()
                    session=Session(local,item,directory/'workflows'/item['id']);result=session.run();rows.append(result)
                    if result['error'] or result['generation_failures']:status['workflow_errors']+=1
                    status['completed']+=1;state();print('DONE',item['id'],result['outcome']['status'],result['requests'],'requests',flush=True)
                    if item['defense']=='ON' and item['spec']['condition']=='hostile':
                        state(status='CHECKPOINT_DIAGNOSIS')
                        target=directory/'diagnostics'/item['id']
                        diagnosis=diagnostic(lambda:probe_workflow(local,session.directory,target),target);diagnostics.append(diagnosis)
                    key=(family,item['spec']['family'])
                    if session.feedback_checkpoint and key not in global_feedback_parents:
                        global_feedback_parents.add(key);feedback_count+=1;state(status='FEEDBACK_SENSITIVITY')
                        target=directory/'feedback'/item['id']
                        diagnostic(lambda:feedback_sensitivity(local,session.directory,target),target)
                if phase=='qualification6':
                    decision=qualification(rows);write(directory/'qualification_decision.json',decision);qualified=decision['qualified']
                    print('CONTROL PANEL:',json.dumps(decision),'Remaining scheduled workflows continue.',flush=True)
                    write(out/f'{family}_breadth_decision.json',dict(advance=args.scope!='qualification',
                        model_family=family,outcome_independent=True,task_success_gate=False,
                        reason='REQUESTED_SCHEDULE_EXECUTED_WITH_TASK_FAILURES_RETAINED'))
            if args.scope!='qualification':
                state(status='LAWFUL_RECOVERY');target=directory/'lawful_recovery'
                diagnostic(lambda:lawful_recovery(local,family,target),target)
            write(directory/'model_decision.json',dict(execution_controls_valid=qualified,workflows=len(rows),
                diagnostics=len(diagnostics),feedback_parent_count=feedback_count,human_review='PENDING'))
            status['models'].append(dict(family=family,qualified=qualified,workflows=len(rows)))
            state(status='STOPPING_SERVER');serving.stop_owned(server,owned,deployment_dir/'shutdown.json')
            server=None;owned={};server_log.close();server_log=None
            for attempt in range(30):
                try:serving.ensure_free(GPU_UUID);break
                except RuntimeError:
                    if attempt==29:raise
                    time.sleep(1)
            print('STOPPED',family,'owned server; GPU 3 remains the only inference device.',flush=True)
        expected={'full':96,'structural':48,'qualification':6}[args.scope]
        if status['completed']!=expected:raise RuntimeError('Scheduled-workflow census incomplete')
        state(status='COMPLETE_WITH_RECORDED_ERRORS_REVIEW_PENDING' if status['workflow_errors'] or status['diagnostic_failures'] else
            'COMPLETE_REVIEW_PENDING',expected_workflows=expected)
    except BaseException as e:
        rc=1;write(out/'fatal_error.json',dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc()))
        state(status='INTERRUPTED' if isinstance(e,KeyboardInterrupt) else 'FAILED',error=str(e));print('FAILED:',e,flush=True)
        if server_log:
            server_log.flush();print('\n'.join(Path(server_log.name).read_text(errors='replace').splitlines()[-35:]),flush=True)
    finally:
        if server:
            try:serving.stop_owned(server,owned,out/'emergency_shutdown.json')
            except Exception as e:write(out/'shutdown_error.json',dict(error=str(e)));rc=1
        if server_log:server_log.close()
        stop.set();thread.join(timeout=2)
        if telemetry:telemetry.join(timeout=15)
        try:
            summarize(out)
            from .analyze import analyze
            analysis=analyze(out)
            state(unresolved_diagnostic_cells=analysis['unresolved_diagnostic_cells'],
                lawful_continuations_recorded=analysis['lawful_continuations_recorded'])
            if status['status']=='COMPLETE_REVIEW_PENDING' and analysis['unresolved_diagnostic_cells']:
                state(status='COMPLETE_WITH_RECORDED_ERRORS_REVIEW_PENDING')
        except Exception as e:
            write(out/'summary_error.json',dict(error=str(e)));rc=1;state(status='SUMMARY_FAILED')
        try:write(out/'gpu_final.json',serving.gpu_table())
        except Exception as e:write(out/'gpu_final_error.json',dict(error=str(e)))
        state(exit_code=rc,finished_epoch=time.time())
        (logs/(args.run_id+'.status')).write_text(f'exit_code={rc}\nstatus={status["status"]}\nresults={out}\n')
        log=logs/(args.run_id+'.log')
        if log.is_file():shutil.copy2(log,out/'controller.log')
        try:serving.archive(out)
        except Exception as e:
            rc=1;state(status='ARCHIVE_FAILED',exit_code=1,archive_error=str(e))
            (logs/(args.run_id+'.status')).write_text(f'exit_code=1\nstatus=ARCHIVE_FAILED\nresults={out}\n')
            print('Raw results preserved:',out,e,flush=True)
        lock.close()
    return rc

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True)
    p.add_argument('--run-id',required=True);p.add_argument('--cache',default=serving.DEFAULT_CACHE)
    p.add_argument('--scope',choices=['qualification','structural','full'],default='full')
    p.add_argument('--feedback',choices=['auto','original','occurrence'],default='auto')
    a=p.parse_args()
    if not a.run_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in a.run_id):p.error('Invalid run ID')
    raise SystemExit(main(a))
