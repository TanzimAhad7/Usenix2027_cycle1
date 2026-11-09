import argparse,contextlib,json,signal,sys,time,traceback
from pathlib import Path
from reference_study.common import activate,write

def run_job(item,directory,family,mock=False):
 from .cases import run
 directory=Path(directory);started=time.monotonic();old=None
 if directory.exists():raise RuntimeError('Refusing to redraw or overwrite attempted acquisition')
 log=directory.parent/'_diagnostic_logs'/(item['id']+'.log');log.parent.mkdir(parents=True,exist_ok=True)
 try:
  old=signal.signal(signal.SIGALRM,lambda *_:(_ for _ in()).throw(TimeoutError('660-second cell watchdog')));signal.alarm(660)
  with log.open('w')as f,contextlib.redirect_stdout(f),contextlib.redirect_stderr(f):result=run(item,directory,family,mock)
 except BaseException as e:
  directory.mkdir(parents=True,exist_ok=True);result=dict(status='INTERRUPTED'if isinstance(e,KeyboardInterrupt)else'TECHNICAL_ERROR',qualified=False,primary_observed=False,scientific_negative=False,error=dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc()))
 finally:
  if old is not None:signal.alarm(0);signal.signal(signal.SIGALRM,old)
 result.update({k:item[k]for k in ('id','axis','direction','policy','candidate','reference','criterion','draw','input_key')})
 result.update(profile=family,mock=mock,aliases=item['aliases'],elapsed_seconds=time.monotonic()-started,autonomous_episodes=0,semantic_review='PENDING')
 write(directory/'item.json',item);write(directory/'result.json',result);return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--family',choices=('qwen','gemma'),required=True);p.add_argument('--mock',action='store_true');a=p.parse_args();activate(a.family)
 signal.signal(signal.SIGTERM,lambda *_:(_ for _ in()).throw(KeyboardInterrupt('Owned stop')))
 for line in sys.stdin:
  q=json.loads(line);r=run_job(q['item'],q['out'],a.family,a.mock);print(json.dumps(dict(id=r['id'],status=r['status'],qualified=r['qualified'])),flush=True)
if __name__=='__main__':main()
