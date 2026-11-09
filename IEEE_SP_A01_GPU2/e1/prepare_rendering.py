"""Research-environment request construction; no live inference or serving imports."""
import argparse,contextlib,io,tempfile
from pathlib import Path
from reference_study.common import activate,read,write,digest,sha,ROOT

def prepare(family,out):
 activate(family)
 from .design import manifest
 from .worker import run_job
 out=Path(out);out.mkdir(parents=True,exist_ok=False);positions=[];unique={}
 with tempfile.TemporaryDirectory(prefix='e1_render_inputs_')as tmp:
  for item in manifest()['P1']:
   with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    result=run_job(item,Path(tmp)/item['id'],family,True)
   if not result['qualified']:raise RuntimeError('CPU request reconstruction failed: '+item['id']+' '+str(result.get('error')))
   records=read(Path(tmp)/item['id']/'model_io/driver_records.json')
   if len(records)!=1 or records[0]['role']!='judge':raise RuntimeError('Unexpected preflight mock role or request count')
   body=records[0]['request'];key=digest(body)
   if key not in unique:unique[key]=dict(first_position=item['id'],request=body)
   positions.append(dict(id=item['id'],request_hash=key))
 write(out/'prepared_requests.json',dict(version='E1_RENDER_INPUTS_V1',family=family,model_inference=0,
  source_manifest_sha256=sha(ROOT/'PACKAGE_MANIFEST.json'),positions=positions,unique_requests=unique,
  construction='Research .venv, original source constructors/serializer, mock transport only. No server/GPU.',
  qualification='Technical reconstruction only; synthetic responses are not scientific observations.'))
 print('PREPARED',family,len(positions),'positions;',len(unique),'unique requests; zero model inference',flush=True)
 return out/'prepared_requests.json'
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--family',required=True,choices=('qwen','gemma'));p.add_argument('--out',required=True,type=Path);a=p.parse_args();prepare(a.family,a.out)
