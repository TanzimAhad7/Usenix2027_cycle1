"""Each spawned process owns its runtime, patches, stdout and signal timers."""
import os,signal,time,traceback,sys,threading
from pathlib import Path
from .common import read,write,append
from .budget import CampaignBudgetStop

def initialize(directory):
    from .base.serving import proc_start
    os.environ['CUDA_VISIBLE_DEVICES']=''
    signal.signal(signal.SIGTERM,lambda *_:(_ for _ in ()).throw(KeyboardInterrupt('Owned episode worker interrupted')))
    signal.signal(signal.SIGUSR1,lambda *_:(_ for _ in ()).throw(CampaignBudgetStop('Campaign collection deadline')))
    path=Path(directory);path.mkdir(parents=True,exist_ok=True)
    output=(path/(str(os.getpid())+'.log')).open('a',buffering=1)
    sys.stdout=output;sys.stderr=output
    write(path/(str(os.getpid())+'.json'),dict(pid=os.getpid(),start=proc_start(os.getpid()),cuda_visible_devices='',scope='Research episode worker; no CUDA/model weights'))

def execute(job):
    from .engine import Session
    from .mock_model import model,failure
    from .matched_recovery import execute_fork
    out=Path(job['out']);item=job['item'];mock=job.get('mock',False)
    directory=out/('forks' if job['kind']=='fork' else 'workflows')/item['id'];started=time.monotonic()
    try:
        if job.get('deadline') is not None and time.monotonic()>=job['deadline']:raise CampaignBudgetStop('Deadline before worker construction')
        if job['kind']=='fork':result=execute_fork(item,job['origin'],out,mock=mock,deadline=job.get('deadline'))
        else:
            session=Session(item,directory,mock=(failure if item['id']==job.get('failure_block') else model) if mock else None)
            result=session.run()
    except BaseException as exc:
        directory.mkdir(parents=True,exist_ok=True)
        result=dict(id=item['id'],status='WORKER_CONSTRUCTION_FAILED',outcome='UNKNOWN_TECHNICAL',qualified=False,
            violation=False,physical_goal=False,policy=item.get('policy'),family=item.get('spec',{}).get('family'),
            lifecycle='CENSORED_CAMPAIGN_TIME_BUDGET' if isinstance(exc,CampaignBudgetStop) else 'INTERRUPTED' if isinstance(exc,KeyboardInterrupt) else 'ERROR',
            mock=mock,elapsed_seconds=time.monotonic()-started,error=dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()))
        write(directory/'result.json',result)
    result.update(execution_worker_pid=os.getpid(),execution_profile='TWO_PROCESS_GPU3_BATCHED')
    write(directory/'result.json',result)
    append(directory/'execution_process.jsonl',dict(pid=os.getpid(),finished_epoch=time.time(),kind=job['kind'],id=item['id']))
    return result

def stop_workers(directory,budget=False,hard=False):
    """No global kill; authenticate worker birth identities before signaling."""
    from .base.serving import proc_start
    records=[read(p) for p in Path(directory).glob('*.json')]
    sig=signal.SIGKILL if hard else signal.SIGUSR1 if budget else signal.SIGTERM
    signaled=[]
    for row in records:
        if row.get('start') is not None and proc_start(row['pid'])==row['start']:
            try:os.kill(row['pid'],sig);signaled.append(row['pid'])
            except ProcessLookupError:pass
    return signaled

def shutdown(pool,directory,interrupted=False,budget=False):
    if not interrupted:
        pool.shutdown(wait=True,cancel_futures=True);return
    soft=stop_workers(directory,budget=budget);done=threading.Event();errors=[]
    def wait_shutdown():
        try:pool.shutdown(wait=True,cancel_futures=True)
        except BaseException as exc:errors.append(str(exc))
        finally:done.set()
    thread=threading.Thread(target=wait_shutdown,daemon=True);thread.start()
    hard=[]
    if not done.wait(60):hard=stop_workers(directory,hard=True)
    complete=done.wait(30)
    write(Path(directory)/'shutdown.json',dict(soft_signaled=soft,hard_signaled=hard,executor_stopped=complete,errors=errors,scope='Authenticated research workers only; hard stops leave partial evidence unknown'))
    if not complete:raise RuntimeError('Episode worker cleanup unconfirmed')
