"""Engineering regression checks for failure retention and packaging, no inference."""
import argparse,fcntl,json,os,shutil,subprocess,tempfile
from pathlib import Path
from reference_study.common import ROOT,read,write,sha

def main(out):
 out.mkdir(parents=True,exist_ok=False);checks=[]
 def ok(name,value):
  if not value:raise AssertionError(name)
  checks.append(dict(check=name,passed=True))
 from n1.design import manifest
 from n1.resume import validate,retain
 m=manifest()
 with tempfile.TemporaryDirectory(prefix='n1-failure-retention-')as d:
  base=Path(d);parent=base/'parent';target=base/'target';shutil.copytree(ROOT,parent/'source',ignore=shutil.ignore_patterns('.venv','.venv-serving','.tools','results','logs','__pycache__'))
  write(parent/'status.json',dict(mode='MOCK_ZERO_INFERENCE',status='INTERRUPTED'))
  validate(parent,True)
  failed=m['P1'][0]['id'];completed=m['P1'][1]['id'];write(parent/'qwen/P1'/failed/'result.json',dict(status='TECHNICAL_ERROR',qualified=False,mock=True));write(parent/'qwen/P1'/failed/'partial_request.json',dict(partial=True));write(parent/'qwen/P1'/completed/'result.json',dict(status='COMPLETE',qualified=True,mock=True))
  n=retain(parent,target,'qwen',m);ok('completed and failed rows both retained',n==2)
  ok('failed terminal bytes unchanged',sha(target/'qwen/P1'/failed/'result.json')==sha(parent/'qwen/P1'/failed/'result.json'))
  ok('partial raw request retained',(target/'qwen/P1'/failed/'partial_request.json').is_file())
  ok('unrecorded block not silently fabricated',not(target/'qwen/P1'/m['P1'][2]['id']).exists())
  try:validate(parent,False)
  except RuntimeError:ok('mock/live resume rejected',True)
  else:raise AssertionError('mock/live parent accepted')
  (parent/'source/n1/design.py').write_text('# deliberately corrupted engineering source')
  try:validate(parent,True)
  except RuntimeError:ok('changed frozen parent code rejected',True)
  else:raise AssertionError('changed source accepted')
 # A negative concurrent launch must neither change LATEST nor alter a running cohort.
 lock=(ROOT/'logs/bootstrap.lock');lock.parent.mkdir(exist_ok=True)
 with lock.open('a')as f:
  fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);before=(ROOT/'logs/LATEST_N1').read_text()if(ROOT/'logs/LATEST_N1').exists()else None
  r=subprocess.run(['bash',str(ROOT/'RUN_N1.sh'),'--cpu-only'],capture_output=True,text=True,timeout=15)
  ok('concurrent launcher refuses while lock held',r.returncode==2)
  after=(ROOT/'logs/LATEST_N1').read_text()if(ROOT/'logs/LATEST_N1').exists()else None
  ok('concurrent launch preserves LATEST',before==after)
 for p in ROOT.glob('*.sh'):
  r=subprocess.run(['bash','-n',str(p)],capture_output=True,text=True);ok('bash syntax '+p.name,r.returncode==0)
 write(out/'checks.json',dict(status='PASS',checks=checks,model_inference=0));print('PASS',len(checks),'engineering checks')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();main(a.out)
