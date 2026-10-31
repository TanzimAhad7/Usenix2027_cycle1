"""One owned GPU2 server; isolated persistent workers with per-case watchdogs."""
from __future__ import annotations
import argparse,collections,json,os,re,selectors,signal,subprocess,sys,threading,time,traceback
from pathlib import Path
from .common import ROOT,GPU_INDEX,GPU_UUID,LOCK_NAME,activate,read,write,append

class StopRequested(BaseException):pass

def main(a):
    activate(a.family)
    from reference_discovery_parallel.base import serving
    from .models import command,profiles,live
    from .report import predictions
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=False);m=read(a.manifest)
    items=m['P1']+m['P2']+[i for b in m['P3_blocks']for i in b]
    census={i['id']:'SCHEDULED'for i in items};status=dict(status='STARTING',profile=a.family,started_epoch=time.time(),planned=len(items))
    server=None;server_log=None;owned={};workers=[];sel=selectors.DefaultSelector();completed=0
    telemetry_stop=threading.Event();telemetry_thread=None;lastbeat=0;error=None
    durations=collections.defaultdict(list);p=profiles()[a.family]
    env={**os.environ,'CUDA_VISIBLE_DEVICES':'','REFERENCE_DISCOVERY_MODEL_FAMILY':a.family,'PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1'}
    env.pop('PYTHONHOME',None);env.pop('PYTHONPATH',None)
    def update(**values):
        status.update(values,completed=completed,active=[w['item']['id']for w in workers if w.get('item')],elapsed_seconds=time.time()-status['started_epoch'])
        write(out/'status.json',status);write(out/'census.json',census)
    def refresh():
        if server and server.poll()is None and serving.proc_start(server.pid)==owned.get(server.pid):
            for pid in serving.descendant_pids(server.pid):owned.setdefault(pid,serving.proc_start(pid))
            write(out/'serving/owned_identities.json',{str(k):v for k,v in owned.items()})
    def heartbeat(force=False):
        nonlocal lastbeat
        if not force and time.monotonic()-lastbeat<20:return
        lastbeat=time.monotonic();update()
        print(f'HEARTBEAT profile={a.family} stage={status["status"]} recorded={completed}/{len(items)} active={status["active"]} elapsed={int(status["elapsed_seconds"])}s',flush=True)
    def start_server():
        nonlocal server,server_log,owned,telemetry_thread
        serving.verify_pid_namespace();serving.GPU=GPU_INDEX
        if a.lock_fd is None or os.fstat(a.lock_fd).st_ino!=(a.project_root/'logs'/LOCK_NAME).stat().st_ino:raise RuntimeError('Authenticated GPU2 project lock missing')
        gpu=next((r for r in serving.gpu_table()if r[0].strip()==str(GPU_INDEX)),None)
        if not gpu or gpu[1].strip()!=GPU_UUID:raise RuntimeError('Physical GPU2 UUID mismatch; no other GPU will be used')
        occupied=[r for r in serving.gpu_applications()if len(r)>1 and r[1].strip()==GPU_UUID]
        if occupied:raise RuntimeError('GPU2 already has compute processes; none were stopped: '+str(occupied))
        serving.ensure_port_free()
        snapshot,identity=serving.inspect_snapshot(a.cache/('models--'+p['hub'].replace('/','--')),p['hub'],p['revision'])
        folder=out/'serving';folder.mkdir();write(folder/'snapshot_identity.json',identity)
        se={**env,'CUDA_VISIBLE_DEVICES':GPU_UUID,'CUDA_DEVICE_ORDER':'PCI_BUS_ID','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1',
            'VLLM_NO_USAGE_STATS':'1','DO_NOT_TRACK':'1','HF_HUB_DISABLE_TELEMETRY':'1',
            'PATH':str(a.serving_python.parent)+os.pathsep+env.get('PATH',''),'PYTHONPATH':str(ROOT/'retained')+os.pathsep+str(ROOT)}
        for k in('VLLM_API_KEY','HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','http_proxy','https_proxy','all_proxy'):se.pop(k,None)
        cmd=command(a.serving_python,snapshot,a.family)
        write(folder/'command.json',dict(argv=cmd,physical_gpu=GPU_INDEX,gpu_uuid=GPU_UUID,profile=p,concurrent_case_workers=a.workers))
        server_log=(folder/'server.log').open('w');server=subprocess.Popen(cmd,cwd=ROOT,env=se,stdout=server_log,stderr=subprocess.STDOUT,start_new_session=True)
        owned={server.pid:serving.proc_start(server.pid)};write(folder/'owned_process.json',dict(pid=server.pid,start=owned[server.pid]))
        print('START',a.family,'physical GPU 2; log:',folder/'server.log',flush=True);update(status='STARTING_SERVER');start=time.monotonic()
        while True:
            if server.poll()is not None:raise RuntimeError('Owned server exited; inspect '+str(folder/'server.log'))
            refresh()
            try:
                found=serving.read_json_url('http://127.0.0.1:18080/v1/models')
                if found.get('data')and found['data'][0].get('id')==p['alias']:break
            except Exception:pass
            if time.monotonic()-start>1800:raise RuntimeError('1800-second server-start watchdog')
            heartbeat();time.sleep(2)
        descendants=serving.descendant_pids(server.pid)
        listeners={int(x)for x in re.findall(r'pid=(\d+)',serving.command(['ss','-ltnp','( sport = :18080 )']))}
        apps=serving.gpu_applications();gpuworkers=[r for r in apps if len(r)>1 and r[0].strip().isdigit()and int(r[0])in descendants]
        foreign=[r for r in apps if len(r)>1 and r[1].strip()==GPU_UUID and r[0].strip().isdigit()and int(r[0])not in descendants]
        if not listeners or not listeners<=descendants or not gpuworkers or foreign or any(r[1].strip()!=GPU_UUID for r in gpuworkers):raise RuntimeError('GPU/endpoint ownership qualification failed')
        write(folder/'placement.json',dict(listeners=sorted(listeners),workers=gpuworkers,physical_gpu=GPU_INDEX,gpu_uuid=GPU_UUID,qualified=True))
        write(folder/'models.json',found);refresh();update(status='LIVE_INTERFACE_QUALIFICATION')
        live(folder/'live_qualification',a.family)
        telemetry_thread=threading.Thread(target=serving.telemetry,args=(out,telemetry_stop),daemon=True);telemetry_thread.start()
        print('QUALIFIED',a.family,'on GPU2; case workers:',a.workers,flush=True)
    def new_worker(index):
        folder=out/'workers';folder.mkdir(exist_ok=True);log=(folder/f'{index}_{time.time_ns()}.log').open('w')
        cmd=[sys.executable,'-u','-m','reference_study.worker','--family',a.family]+(['--mock']if a.mock else[])
        process=subprocess.Popen(cmd,cwd=ROOT,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=log,text=True,bufsize=1,start_new_session=True)
        w=dict(process=process,identity=serving.proc_start(process.pid),log=log,index=index,item=None,started=0)
        sel.register(process.stdout,selectors.EVENT_READ,w)
        append(out/'worker_ownership.jsonl',dict(pid=process.pid,start=w['identity'],argv=cmd,index=index));return w
    def stop_worker(w):
        proc=w['process']
        try:sel.unregister(proc.stdout)
        except Exception:pass
        if proc.poll()is None and serving.proc_start(proc.pid)==w['identity']:
            proc.terminate()
            try:proc.wait(timeout=15)
            except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=10)
        for stream in(proc.stdin,proc.stdout):
            if stream:stream.close()
        w['log'].close()
    def complete(w,receipt=None,forced=None):
        nonlocal completed
        item=w['item'];path=out/item['panel']/item['id']/'result.json'
        if not path.is_file():
            write(path,dict(id=item['id'],panel=item['panel'],profile=a.family,status=forced or'WORKER_EXIT_WITHOUT_RESULT',qualified=False,
                mock=a.mock,attempted=True,scientific_negative=False,error='Worker ended before its terminal result; raw partial artifacts retained.'))
        r=read(path)
        if receipt and receipt.get('id')!=item['id']:raise RuntimeError('Persistent worker receipt identity differs')
        census[item['id']]=r['status'];completed+=1;durations[item['panel']].append(time.monotonic()-w['started'])
        append(out/'schedule_events.jsonl',dict(event='END',epoch=time.time(),id=item['id'],status=r['status'],qualified=r['qualified'],pid=w['process'].pid))
        print(a.family,f'{completed}/{len(items)}',item['id'],r['status'],'qualified='+str(r['qualified']),flush=True)
        w['item']=None
    def run_group(group,label):
        update(status=label);waiting=collections.deque(group);stage_start=time.monotonic();stage_done=0
        while waiting or any(w.get('item')for w in workers):
            if not a.mock and server.poll()is not None:raise RuntimeError('Owned model server exited; scientific cells are not redrawn')
            for i,w in enumerate(list(workers)):
                proc=w['process']
                if proc.poll()is not None:
                    if w.get('item'):complete(w,forced='WORKER_EXIT_WITHOUT_RESULT');stage_done+=1
                    stop_worker(w);workers[i]=new_worker(w['index'])
                elif w.get('item')and time.monotonic()-w['started']>1320:
                    stop_worker(w);complete(w,forced='SUPERVISOR_CASE_WATCHDOG');stage_done+=1;workers[i]=new_worker(w['index'])
            for w in workers:
                if waiting and w.get('item')is None:
                    item=waiting.popleft();w.update(item=item,started=time.monotonic());census[item['id']]='RUNNING'
                    append(out/'schedule_events.jsonl',dict(event='START',epoch=time.time(),id=item['id'],panel=item['panel'],pid=w['process'].pid))
                    write(out/'job_inputs'/(item['id']+'.json'),item)
                    w['process'].stdin.write(json.dumps(dict(item=item,out=str(out/item['panel']/item['id'])))+'\n');w['process'].stdin.flush()
            for key,_ in sel.select(timeout=.05 if a.mock else .5):
                w=key.data;line=key.fileobj.readline()
                if not line:continue
                try:receipt=json.loads(line)
                except ValueError:raise RuntimeError('Worker wrote nonprotocol stdout: '+line[:200])
                if w.get('item')is None:raise RuntimeError('Worker returned an unexpected extra receipt')
                complete(w,receipt);stage_done+=1
            if stage_done:
                update(stage_completed=stage_done,stage_planned=len(group),estimated_stage_remaining_seconds=(time.monotonic()-stage_start)/stage_done*(len(group)-stage_done))
            refresh();heartbeat()
    signal.signal(signal.SIGTERM,lambda *_:(_ for _ in()).throw(StopRequested('SIGTERM')))
    try:
        if not a.mock:start_server()
        workers.extend(new_worker(i)for i in range(a.workers))
        run_group(m['P1'],'P1_REFERENCE_INTERVENTION');run_group(m['P2'],'P2_ADMISSION_COMPARISON')
        predictions(out,m);append(out/'schedule_events.jsonl',dict(event='PREDICTIONS_FROZEN_BEFORE_P3',epoch=time.time()))
        for block in m['P3_blocks']:run_group(block,'P3_AUTONOMOUS_BLOCKS')
        update(status='MOCK_COMPLETE_ZERO_INFERENCE'if a.mock else'COMPLETE_EXPLORATORY_REVIEW_PENDING')
    except BaseException as e:
        error=dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc());write(out/'fatal_error.json',error)
        update(status='INTERRUPTED'if isinstance(e,(StopRequested,KeyboardInterrupt))else'FAILED')
        print('PROFILE STOP',a.family,str(e),flush=True)
    finally:
        for w in workers:
            stop_worker(w)
            if w.get('item'):complete(w,forced='INTERRUPTED')
        if server:
            try:refresh();serving.stop_owned(server,owned,out/'serving/shutdown.json')
            except Exception as e:error=dict(type=type(e).__name__,message=str(e));update(status='OWNED_CLEANUP_FAILED',cleanup_error=error)
        if server_log:server_log.close()
        telemetry_stop.set()
        if telemetry_thread:telemetry_thread.join(timeout=15)
        for k,v in census.items():
            if v in('SCHEDULED','RUNNING'):census[k]='NOT_EXECUTED_'+status['status']
        update(finished_epoch=time.time(),durations={k:dict(count=len(v),mean_seconds=sum(v)/len(v))for k,v in durations.items()if v})
        heartbeat(True);sel.close()
    return 1 if error else 0

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--family',choices=('qwen','gemma'),required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True);p.add_argument('--project-root',type=Path,required=True);p.add_argument('--serving-python',type=Path,required=True)
    p.add_argument('--cache',type=Path,required=True);p.add_argument('--lock-fd',type=int);p.add_argument('--workers',type=int,choices=(1,2,3,4),default=4);p.add_argument('--mock',action='store_true')
    raise SystemExit(main(p.parse_args()))
