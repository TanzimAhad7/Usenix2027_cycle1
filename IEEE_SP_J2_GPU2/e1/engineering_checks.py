"""Edge cases that must not be mistaken for scientific evidence."""
import argparse,tempfile,json,contextlib,io
from pathlib import Path
from unittest.mock import patch
from reference_study.common import activate,write

def check(out,family):
 activate(family)
 from .design import manifest,fixture,actions
 from .cases import run,world_for,RecordPolicy,Replay
 from .checker import variant
 from reference_discovery_parallel.base.source import load_source
 from reference_discovery_parallel.base.transport import Driver,reply,httpx
 from agentdojo.functions_runtime import FunctionCall
 out=Path(out);out.mkdir(parents=True,exist_ok=True);checks=[]
 item=next(x for x in manifest()['P1']if x['setting']=='BANK'and x['policy']=='C1'and x['candidate']=='B'and x['reference']=='A'and x['criterion']=='FUZZY')
 for name,body in [('TRUNCATED',reply('{"survive":true}',finish='length')),('FENCED',reply('```json\n{"survive":true}\n```')),('MALFORMED',reply('{"survive":"false","reason":"true"}'))]:
  with patch('permission_admission.runtime.fixed_driver',lambda path,mock:Driver(path,lambda role,request:body)),contextlib.redirect_stdout(io.StringIO()):
   result=run(item,out/name,family,False)
  assert result['status']=='UNQUALIFIED_RESPONSE'and result['qualified']is False
  assert result['allowed']is True and result['native_clone_arms']['JUDGE_RELEASE']['assessment']['violation']is True
 checks.append('Truncation, fences and string boolean remain unqualified; actual source-allowed native violation retained')
 core,_=load_source();spec,query=fixture('BANK','C1');w=world_for(spec);pair=actions('BANK');c=FunctionCall(**pair['B']);r=FunctionCall(**pair['A'])
 def fallback(role,body):
  if 'logprobs'in body:return httpx.Response(400,json=dict(error=dict(message='logprobs unsupported',type='invalid_request_error',code='unsupported')))
  return reply('{"survive":false,"reason":"CPU source fallback"}')
 d=Driver(out/'fallback',fallback)
 try:
  checker=variant(core,out/'fallback','FUZZY');policy=RecordPolicy(d.policies['judge'])
  with contextlib.redirect_stdout(io.StringIO()):
   loop=checker.AttriGuardExecutionLoop(None,judge_llm=policy,survival_mode='fuzzy');assert loop._fuzzy_survive(c,[r],query,w.runtime,w.env)is False
  assert len(d.records)==2 and 'exception'in d.records[0]and 'response'in d.records[1]
  replay=Replay(policy.records);original=core.AttriGuardExecutionLoop(None,judge_llm=replay,survival_mode='fuzzy')
  assert original._fuzzy_survive(c,[r],query,w.runtime,w.env)is False and replay.index==2
 finally:d.close()
 checks.append('Only source-supported logprob rejection issues one fallback; untouched source replay preserves both query positions')
 # Terminal records cannot be overwritten even by the engineering worker.
 from .worker import run_job
 terminal=out/'no_redraw';write(terminal/'result.json',dict(status='TECHNICAL_ERROR'))
 try:run_job(item,terminal,family,True);raise AssertionError('Recorded cell redrawn')
 except RuntimeError as e:assert 'Refusing to redraw'in str(e)
 checks.append('Worker refuses to redraw a terminal cell')
 write(out/'engineering_checks.json',dict(status='PASS',family=family,checks=checks,model_inference=0,not_scientific_observations=True))
 return checks
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--family',choices=('qwen','gemma'),default='qwen');a=p.parse_args();print(json.dumps(check(a.out,a.family),indent=2))
