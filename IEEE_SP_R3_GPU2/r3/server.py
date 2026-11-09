import os,re,subprocess,sys,time,threading
from pathlib import Path
from .common import ALIAS,PORT,REVISION,write,read
from . import serving_base as base

class OwnedServer:
    def __init__(self,python,cache,out,heartbeat):
        self.python=python;self.cache=cache;self.out=out;self.heartbeat=heartbeat;self.process=None;self.log=None;self.owned={};self.stop_event=threading.Event();self.telemetry=None
    def refresh(self):
        if self.process and self.owned.get(self.process.pid) is not None and base.proc_start(self.process.pid)==self.owned[self.process.pid]:
            for pid in base.descendant_pids(self.process.pid):self.owned.setdefault(pid,base.proc_start(pid))
            write(self.out/'owned_identities.json',{str(k):v for k,v in self.owned.items()})
    def prepare(self):
        base.verify_pid_namespace();self.out.mkdir(parents=True,exist_ok=True)
        rows=base.gpu_table();gpu=next((r for r in rows if r[0].strip()=='2'),None)
        if gpu is None:raise RuntimeError('Physical GPU2 is unavailable; no device substitution')
        self.uuid=gpu[1].strip();base.ensure_free(self.uuid);base.ensure_port_free()
        snapshot,identity=base.inspect_snapshot(self.cache/'models--Qwen--Qwen3-32B','Qwen/Qwen3-32B',REVISION)
        for entry in identity['files']:
            f=snapshot/entry['name'];s=f.stat();entry.update(resolved_path=str(f.resolve()),device=s.st_dev,inode=s.st_ino,mtime_ns=s.st_mtime_ns)
        write(self.out/'snapshot_identity.json',identity);write(self.out/'gpu_selection.json',dict(physical_gpu=2,gpu_uuid=self.uuid,source='nvidia-smi before server launch',port=PORT))
        self.snapshot=snapshot;return snapshot
    def start(self,limits):
        from .common import ROOT
        base.ensure_free(self.uuid);base.ensure_port_free()
        cmd=[str(self.python),'-m','vllm.entrypoints.openai.api_server','--model',str(self.snapshot),'--tokenizer',str(self.snapshot),'--served-model-name',ALIAS,'--host','127.0.0.1','--port',str(PORT),'--tensor-parallel-size','1','--dtype','bfloat16','--gpu-memory-utilization','0.90','--max-model-len',str(limits['max_model_len']),'--max-num-seqs','4','--generation-config','vllm','--override-generation-config','{"max_new_tokens":'+str(limits['max_output_tokens'])+'}','--seed','20261105']
        env=dict(os.environ,CUDA_VISIBLE_DEVICES=self.uuid,CUDA_DEVICE_ORDER='PCI_BUS_ID',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',VLLM_NO_USAGE_STATS='1',DO_NOT_TRACK='1',HF_HUB_DISABLE_TELEMETRY='1',PATH=str(self.python.parent)+os.pathsep+os.environ.get('PATH',''))
        for k in ('PYTHONPATH','PYTHONHOME','VLLM_API_KEY','HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','http_proxy','https_proxy','all_proxy'):env.pop(k,None)
        write(self.out/'command.json',dict(argv=cmd,gpu_uuid=self.uuid,physical_gpu=2,interface='Official LocalLLM manual function tags; no native API tool/reasoning parser or template override'))
        self.log=(self.out/'server.log').open('w');self.process=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=self.log,stderr=subprocess.STDOUT,start_new_session=True)
        self.owned[self.process.pid]=base.proc_start(self.process.pid);self.refresh();started=time.monotonic()
        while True:
            if self.process.poll() is not None:raise RuntimeError('Owned vLLM server exited; inspect serving/server.log')
            self.refresh()
            try:
                found=base.read_json_url(f'http://127.0.0.1:{PORT}/v1/models')
                if any(d.get('id')==ALIAS for d in found.get('data',[])):break
            except Exception:pass
            if time.monotonic()-started>1800:raise RuntimeError('Server initialization watchdog expired')
            self.heartbeat();time.sleep(2)
        descendants=base.descendant_pids(self.process.pid)
        listeners={int(x) for x in re.findall(r'pid=(\d+)',base.command(['ss','-ltnp',f'( sport = :{PORT} )']))}
        apps=base.gpu_applications();workers=[r for r in apps if r[0].strip().isdigit() and int(r[0]) in descendants]
        foreign=[r for r in apps if len(r)>1 and r[1].strip()==self.uuid and r[0].strip().isdigit() and int(r[0]) not in descendants]
        if not listeners or not listeners<=descendants or not workers or foreign or any(r[1].strip()!=self.uuid for r in workers):raise RuntimeError('Owned endpoint/GPU2 placement could not be authenticated')
        write(self.out/'placement.json',dict(qualified=True,listeners=sorted(listeners),workers=workers,physical_gpu=2,gpu_uuid=self.uuid))
        self.telemetry=threading.Thread(target=base.telemetry,args=(self.out,self.stop_event),daemon=True);self.telemetry.start()
    def close(self):
        self.stop_event.set()
        if self.telemetry:self.telemetry.join(timeout=35)
        if self.process:self.refresh();base.stop_owned(self.process,self.owned,self.out/'shutdown.json')
        if self.log:self.log.close()
