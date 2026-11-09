import argparse,contextlib,io,tempfile
from pathlib import Path
from reference_study.common import ROOT,activate,read,write,digest,sha

def prepare(family,out):
 activate(family)
 from .design import manifest,logical_conditions,key_for
 from .worker import run_job
 out=Path(out);out.mkdir(parents=True,exist_ok=False);m=manifest();bodies={};states=set();checks=[]
 with tempfile.TemporaryDirectory(prefix='e2b_prepare_')as tmp:
  for i,logical in enumerate(logical_conditions()):
   key=key_for(logical);item=dict(logical,id=f'LOGICAL_{i:02}',draw=0,panel='P1',input_key=key,aliases=[dict(logical,draw=0)])
   directory=Path(tmp)/item['id']
   with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):result=run_job(item,directory,family,True)
   if not result['qualified']:raise RuntimeError('Request/native preparation failed: '+str(result.get('error')))
   records=read(directory/'model_io/driver_records.json')
   if len(records)!=1 or records[0]['role']!='judge':raise RuntimeError('Unexpected preflight request count/role')
   body=records[0]['request'];state=read(directory/'held_input.json')['native_state_sha256'];states.add(state)
   if key in bodies and bodies[key]!=body:raise RuntimeError('Logical alias differs in actual serving request')
   bodies[key]=body;checks.append(dict(logical=logical,input_key=key,request_hash=digest(body),native_state_hash=state))
 if len(states)!=1 or len(bodies)!=56 or len({digest(b)for b in bodies.values()})!=56:raise RuntimeError('Expected 56 real serving bodies and one initial state')
 unique={digest(b):dict(first_position=next(j['id']for j in m['P1']if j['input_key']==key),request=b)for key,b in bodies.items()}
 positions=[dict(id=j['id'],request_hash=digest(bodies[j['input_key']]))for j in m['P1']]
 write(out/'prepared_requests.json',dict(version='E2B_RENDER_INPUTS_V1',family=family,model_inference=0,source_manifest_sha256=sha(ROOT/'PACKAGE_MANIFEST.json'),native_state_hash=next(iter(states)),positions=positions,unique_requests=unique,bodies=bodies,logical_checks=checks))
 print('PREPARED',family,'64 conditions / 56 actual bodies / 168 acquisitions; zero inference',flush=True)
 return out/'prepared_requests.json'

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--family',choices=('qwen','gemma'),required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();prepare(a.family,a.out)
