"""Bounded rolling dispatch; source order and completion order stay distinct."""
import time
from concurrent.futures import wait,FIRST_COMPLETED
from .common import append,write
from .execution_config import WORKERS,DrainBeforeRestart
from .budget import CampaignBudgetStop

def collect(pool,jobs,execute,consume,progress,directory,deadline=None,drain_needed=lambda:False,workers=WORKERS):
    pending={};cursor=0;results={};journal=directory/'scheduler.jsonl'
    while cursor<len(jobs) or pending:
        if deadline is not None and time.monotonic()>=deadline:raise CampaignBudgetStop('Optional collection limit reached')
        while cursor<len(jobs) and len(pending)<workers:
            if pending and drain_needed():break
            job=jobs[cursor];kind=job['kind'];ident=job['item']['id']
            try:progress(kind,ident,'RUNNING')
            except DrainBeforeRestart:
                if not pending:raise RuntimeError('Restart requested drain with no pending work')
                break
            future=pool.submit(execute,job);pending[future]=(cursor,job);cursor+=1
            append(journal,dict(event='SUBMIT',epoch=time.time(),phase=job.get('phase'),frozen_phase_index=cursor-1,kind=kind,id=ident,in_flight=len(pending)))
        if not pending:continue
        done,_=wait(pending,timeout=0.5,return_when=FIRST_COMPLETED)
        # Ties have a stable controller processing order. This does not force
        # the server's actual generation or random-number consumption order.
        for future in sorted(done,key=lambda f:pending[f][0]):
            index,job=pending.pop(future);result=future.result();ident=job['item']['id'];kind=job['kind']
            results[index]=result
            consume(job,result)
            progress(kind,ident,result.get('lifecycle',result.get('status','RECORDED')))
            append(journal,dict(event='COMPLETE',epoch=time.time(),phase=job.get('phase'),frozen_phase_index=index,kind=kind,id=ident,in_flight=len(pending)))
            if result.get('lifecycle')=='INTERRUPTED':raise KeyboardInterrupt('Interrupted worker evidence preserved')
    return [results[i] for i in range(len(jobs))]
