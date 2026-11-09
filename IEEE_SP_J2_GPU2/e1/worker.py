"""Persistent process isolation: one source profile, fresh client/state per cell."""
import argparse,contextlib,json,signal,time,traceback
from pathlib import Path
from reference_study.common import activate,write

def run_job(item,directory,family,mock=False):
 from .cases import run
 directory=Path(directory);started=time.monotonic();old=None
 if (directory/'result.json').exists():raise RuntimeError('Refusing to redraw a recorded scientific position')
 log=directory.parent/'_diagnostic_logs'/(item['id']+'.log');log.parent.mkdir(parents=True,exist_ok=True)
 try:
  old=signal.signal(signal.SIGALRM,lambda *_:(_ for _ in()).throw(TimeoutError('660-second technical cell watchdog')));signal.alarm(660)
  with log.open('a')as stream,contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):result=run(item,directory,family,mock)
 except BaseException as e:
  directory.mkdir(parents=True,exist_ok=True);result=dict(status='INTERRUPTED'if isinstance(e,KeyboardInterrupt)else'TECHNICAL_ERROR',qualified=False,
   scientific_negative=False,error=dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc()))
 finally:
  if old is not None:signal.alarm(0);signal.signal(signal.SIGALRM,old)
 result.update(**{k:item[k]for k in ('id','setting','policy','candidate','reference','criterion','draw')},profile=family,mock=mock,
  evaluation_mode='MOCK_ZERO_MODEL_INFERENCE'if mock else'LIVE_CONDITIONAL_COMPONENT',elapsed_seconds=time.monotonic()-started,
  independent_human_semantic_review='PENDING',autonomous_episodes=0)
 write(directory/'item.json',item);write(directory/'result.json',result);return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--family',choices=('qwen','gemma'),required=True);p.add_argument('--mock',action='store_true');a=p.parse_args();activate(a.family)
 signal.signal(signal.SIGTERM,lambda *_:(_ for _ in()).throw(KeyboardInterrupt('Owned controller stop')))
 import sys
 for line in sys.stdin:
  q=json.loads(line);r=run_job(q['item'],q['out'],a.family,a.mock)
  print(json.dumps(dict(id=r['id'],status=r['status'],qualified=r['qualified'])),flush=True)
if __name__=='__main__':main()
