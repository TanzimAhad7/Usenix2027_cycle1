"""Small integer CUDA audit on shared physical GPU2; never imports vLLM/models.

Allocator cap is not a hard cap on CUDA context/driver memory. The process
additionally measures its actual nvidia-smi allocation, then exits on pressure.
The controller starts a separate pure CPU helper at the next model boundary
or final draining step, after the CUDA-owning process has exited completely.
"""
import argparse,csv,hashlib,io,json,os,signal,subprocess,sys,time,traceback
from pathlib import Path
from .common import read,write,append,file_hash
from .execution_config import GPU2_UUID,AUDIT_ALLOCATOR_MIB,AUDIT_SOFT_PROCESS_MIB,AUDIT_MIN_FREE_MIB
from .audit_core import CPU,audit

def command(args):
    r=subprocess.run(args,capture_output=True,text=True,timeout=10,check=True)
    return list(csv.reader(io.StringIO(r.stdout)))

def gpu_row():
    rows=command(['nvidia-smi','--query-gpu=index,uuid,memory.free,memory.total','--format=csv,noheader,nounits'])
    row=next((r for r in rows if r[0].strip()=='2'),None)
    if not row or row[1].strip()!=GPU2_UUID:raise RuntimeError('Shared physical GPU2 UUID mismatch')
    return dict(uuid=row[1].strip(),free_mib=int(row[2].strip()),total_mib=int(row[3].strip()))

def own_memory(require=False):
    rows=command(['nvidia-smi','--query-compute-apps=pid,gpu_uuid,used_gpu_memory','--format=csv,noheader,nounits'])
    own=[r for r in rows if r[0].strip()==str(os.getpid())]
    if require and not own:raise RuntimeError('Actual audit CUDA process memory cannot be authenticated')
    if require and any(not r[2].strip().isdigit() for r in own):raise RuntimeError('Audit process VRAM is not measurable; release shared GPU2')
    if any(r[1].strip()!=GPU2_UUID for r in own):raise RuntimeError('Audit process appeared on a GPU other than2')
    return sum(int(r[2].strip()) for r in own if r[2].strip().isdigit())

class CUDA:
    name='CUDA_GPU2'
    def __init__(self,folder):
        self.folder=folder
        row=gpu_row()
        if row['free_mib']<AUDIT_MIN_FREE_MIB:raise RuntimeError('Shared GPU2 has less than2 GiB free; do not allocate a CUDA context')
        if os.environ.get('CUDA_VISIBLE_DEVICES')!=GPU2_UUID:raise RuntimeError('Audit must expose only pinned GPU2')
        import torch
        self.torch=torch;torch.set_num_threads(1)
        if not torch.cuda.is_available() or torch.cuda.device_count()!=1:raise RuntimeError('Exactly one visible CUDA device required for auditing')
        torch.cuda.set_per_process_memory_fraction(AUDIT_ALLOCATOR_MIB/row['total_mib'],0)
        self.peak_mib=0;self.last_health=0
        # Exercise exact device arithmetic before accepting any case audit.
        if self.counts([0,0,1],[0,1,1],2)!=([2,1],[1,2]):raise RuntimeError('CUDA integer qualification disagrees')
        self.peak_mib=max(self.peak_mib,own_memory(require=True))
        append(self.folder/'health.jsonl',dict(epoch=time.time(),own_process_mib=self.peak_mib,qualification='Integer CUDA fixture complete; no model weights'))
        if self.peak_mib>AUDIT_SOFT_PROCESS_MIB:raise RuntimeError('Audit CUDA context exceeds the1 GiB measured soft budget')
    def counts(self,a,b,size):
        if size>4096 or len(a)+len(b)>16384:raise RuntimeError('Audit batch exceeds bounded GPU working set; fall back to CPU')
        if time.monotonic()-self.last_health>3:
            row=gpu_row();self.peak_mib=max(self.peak_mib,own_memory());self.last_health=time.monotonic()
            append(self.folder/'health.jsonl',dict(epoch=time.time(),own_peak_process_mib=self.peak_mib,**row))
            if row['free_mib']<AUDIT_MIN_FREE_MIB:raise RuntimeError('Shared GPU2 memory pressure; release audit context')
            if self.peak_mib>AUDIT_SOFT_PROCESS_MIB:raise RuntimeError('Measured audit process exceeds1 GiB soft budget; release context')
        t=self.torch
        if not size:return [],[]
        with t.inference_mode():
            left=t.tensor(a,dtype=t.int64,device='cuda:0');right=t.tensor(b,dtype=t.int64,device='cuda:0')
            x=t.bincount(left,minlength=size).cpu().tolist();y=t.bincount(right,minlength=size).cpu().tolist()
            del left,right
        t.cuda.empty_cache()
        return x,y

def fallback(args,reason):
    folder=args.out/'gpu2_audit';folder.mkdir(exist_ok=True)
    append(folder/'transitions.jsonl',dict(epoch=time.time(),reason=str(reason),action='EXIT_75_RELEASE_CUDA_CONTEXT_REQUEST_CPU_HELPER',no_model_or_vllm=True))
    raise SystemExit(75)

def main(args):
    out=args.out;folder=out/'gpu2_audit';folder.mkdir(parents=True,exist_ok=True);records=folder/'records';records.mkdir(exist_ok=True)
    try:os.nice(10)
    except OSError:pass
    if args.cpu_only:backend=CPU()
    else:
        try:backend=CUDA(folder)
        except Exception as exc:fallback(args,exc)
    seen={};finished=False
    def scan():
        for model in ('qwen','gemma'):
            for kind in ('workflows','forks'):
                for result_path in sorted((out/'models'/model/kind).glob('*/result.json')):
                    directory=result_path.parent;world_path=directory/'final_world.json';item_path=directory/'item.json'
                    key=str(directory.relative_to(out))
                    if not world_path.exists() or not item_path.exists():
                        result=read(result_path)
                        row=dict(status='NOT_EXECUTED_NO_ELIGIBLE_CHECKPOINT' if result.get('status')=='NO_ELIGIBLE_CHECKPOINT' else 'UNAVAILABLE_NATIVE_STATE',case=key,backend='NO_CUDA_WORK',scope='Not a successful effect-free audit; no complete native state/contract available')
                        write(records/(hashlib.sha256(key.encode()).hexdigest()+'.json'),row)
                        continue
                    stat_key=tuple((p.stat().st_mtime_ns,p.stat().st_size) for p in [world_path,item_path])
                    if seen.get(key)==stat_key:continue
                    fingerprint=(file_hash(world_path),file_hash(item_path))
                    result=read(result_path);item=read(item_path);world=read(world_path)
                    try:row=audit(item['spec'],world,result,backend)
                    except Exception as exc:
                        if backend.name=='CUDA_GPU2':fallback(args,exc)
                        row=dict(status='AUDIT_ERROR',error=str(exc),traceback=traceback.format_exc(),backend='CPU')
                    row.update(case=key,world_sha256=fingerprint[0],contract_item_sha256=fingerprint[1],epoch=time.time(),pid=os.getpid())
                    append(folder/'audits.jsonl',row)
                    write(records/(hashlib.sha256(key.encode()).hexdigest()+'.json'),row);seen[key]=stat_key
        rows=[read(p) for p in records.glob('*.json')]
        write(folder/'status.json',dict(status='COMPLETE' if finished else 'RUNNING',backend=backend.name,recorded=len(rows),
            disagreements=sum(r['status']=='DISAGREEMENT' for r in rows),errors=sum(r['status'] in ['AUDIT_ERROR','NATIVE_LEDGER_INCONSISTENT'] for r in rows),
            cuda_peak_process_mib=getattr(backend,'peak_mib',None),allocator_limit_mib=AUDIT_ALLOCATOR_MIB,measured_process_soft_limit_mib=AUDIT_SOFT_PROCESS_MIB,
            context_limit_caveat='CUDA driver/context overhead is outside the allocator cap; a measured overage triggers exec into CPU mode, not a guarantee of a hard total-memory ceiling.'))
    while True:
        finished=args.stop_file.exists();scan()
        if finished:break
        time.sleep(3)
    return 0

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--stop-file',required=True,type=Path);p.add_argument('--cpu-only',action='store_true')
    raise SystemExit(main(p.parse_args()))
