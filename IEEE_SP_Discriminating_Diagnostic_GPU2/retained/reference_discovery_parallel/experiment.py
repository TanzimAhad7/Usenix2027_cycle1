"""Two isolated workflow processes; all dependent model/tool steps stay ordered."""
import multiprocessing,time,traceback
from concurrent.futures import ProcessPoolExecutor
from .common import write,append
from .budget import CampaignBudgetStop
from .rolling import collect
from .episode_worker import execute,initialize,shutdown
from .execution_config import WORKERS

def run_study(out,origin,frozen,progress,mock=False,failure_block=None,deadline=None,drain_needed=lambda:False):
    from . import matched_recovery
    if frozen['blocks']:raise RuntimeError('This allocation must not reschedule S1 inference')
    registry=out/'episode_workers';pool=ProcessPoolExecutor(max_workers=WORKERS,
        mp_context=multiprocessing.get_context('spawn'),initializer=initialize,initargs=(str(registry),))
    error=None;selected={}
    def job(item,kind='workflow',origin=None):
        return dict(kind=kind,item=item,origin=origin,out=str(out),mock=mock,failure_block=failure_block,deadline=deadline)
    def consume(j,result):
        print(f'{j["item"]["id"]}: {result["outcome"]}; qualified={result.get("qualified")}; effects={len(result.get("effects",[]))}; worker concurrency limit={WORKERS}',flush=True)
    def phase(name,jobs):
        for value in jobs:value['phase']=name
        append(out/'phase_events.jsonl',dict(phase=name,event='START',epoch=time.time(),jobs=len(jobs),workers=WORKERS))
        values=collect(pool,jobs,execute,consume,progress,out,deadline,drain_needed)
        append(out/'phase_events.jsonl',dict(phase=name,event='DRAINED',epoch=time.time(),jobs=len(jobs)))
        return values
    try:
        core=[i for i in frozen['workflows'] if i['allocation_phase']=='CORE']
        phase('CORE',[job(i) for i in core])
        for item in core:
            try:matched_recovery.choose_from_disk(item,selected,out)
            except Exception as exc:write(out/'workflows'/item['id']/'recovery_selection_error.json',dict(error=str(exc),traceback=traceback.format_exc()))
        forks=[]
        for item in frozen['forks']:
            selected_origin=selected.get((item['family'],item['carrier']))
            if selected_origin is None:
                result=matched_recovery.unexposed(item,out);progress('fork',item['id'],result['status'])
            else:forks.append(job(item,'fork',selected_origin))
        phase('MATCHED_RECOVERY',forks);matched_recovery.certificates(out,selected)
        for name in ['RECOVERY','BOUNDARY']:
            phase(name,[job(i) for i in frozen['workflows'] if i['allocation_phase']==name])
    except BaseException as exc:error=exc;raise
    finally:
        shutdown(pool,registry,interrupted=error is not None,budget=isinstance(error,CampaignBudgetStop))
