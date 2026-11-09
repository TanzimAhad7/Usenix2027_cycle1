import argparse,json
from pathlib import Path
from reference_study.common import activate,write

def qualify(out,family='qwen'):
 activate(family)
 from agentdojo.task_suite.load_suites import get_suite
 from agentdojo.functions_runtime import FunctionCall
 from agentdojo.types import text_content_block_from_string
 from reference_discovery_parallel.base.source import load_source,verify_source
 from .design import manifest,logical_conditions,inputs,native_spec,expected,key_for
 from .cases import world_for,observed_call
 from .measure import dispatch,committed,assess
 from .checker import variant,prompt_for
 from .terminal import inspect
 out=Path(out);out.mkdir(parents=True,exist_ok=True);identity=verify_source();core,_=load_source();m=manifest();states=[]
 assert len(m['P1'])==168 and sum(len(x['aliases'])for x in m['P1'])==192
 for item in m['P1']:assert all(key_for(a)==item['input_key']and expected(a)==expected(item)for a in item['aliases'])
 for i,item in enumerate(logical_conditions()):
  q,c,refs,allowed=inputs(item);w=world_for(native_spec());states.append(w.snapshot())
  if refs:assert refs[0]in allowed
  r=dispatch(core,w,c,allowed,True,out/'native'/str(i));assert r['assessment']['committed_count']==1 and r['assessment']['violation']==(not expected(item))
  clone=w.clone_for_dispatch(False)
  for _ in range(2):core._execute_calls([FunctionCall(**c)],clone.runtime,clone.env)
  assert assess(committed(clone.env),allowed)['violation_indices'][-1]==1
 assert all(s==states[0]for s in states)
 for axis in ('amount','recipient'):
  for direction in ('forward','reverse'):
   item=dict(axis=axis,direction=direction,candidate='EDIT',criterion='SOURCE');q1,c1,r1,_=inputs(dict(item,policy='STRICT'));q2,c2,r2,_=inputs(dict(item,policy='BROADER'))
   assert c1==c2 and r1==r2
   f1=json.loads(q1.split('TRUSTED_OWNER_POLICY_AND_STATE:\n')[1]);f2=json.loads(q2.split('TRUSTED_OWNER_POLICY_AND_STATE:\n')[1]);f1['owner_grant']=f2['owner_grant'];assert f1==f2
 original=core.FUZZY_SYSTEM_PROMPT;case4=original[original.index('2.  **Valid Alternative Step'):original.index('3.  **Content Abstraction')]
 assert all(case4 in prompt_for(original,k)for k in ('SOURCE','ATTENTION','ARGUMENT_EQUALITY'))
 class Stub:
  def __init__(self,raw,extra=None):self.raw=raw;self.extra=extra or {};self.calls=0
  def query(self,q,runtime,env,messages,extra):self.calls+=1;return q,runtime,env,[dict(role='assistant',content=[text_content_block_from_string(self.raw)])],self.extra
 item=dict(axis='amount',direction='forward',policy='STRICT',candidate='EDIT',criterion='SOURCE');q,c,refs,_=inputs(item);w=world_for(native_spec());c=FunctionCall(**c);refs=[FunctionCall(**r)for r in refs];checker=variant(core,out/'parser','SOURCE')
 for raw,want,path in [('{"survive":false}',False,'JSON_BOOLEAN'),('{"survive":true}',True,'JSON_BOOLEAN'),('```json\n{"survive":false,"reason":"true appears here"}\n```',True,'SUBSTRING_FALLBACK')]:
  loop=checker.AttriGuardExecutionLoop(None,judge_llm=Stub(raw),survival_mode='fuzzy');got,branch=observed_call(loop,c,refs,q,w);assert got==want and branch['path']==path
 lp=dict(content=[dict(token='true',logprob=-2,top_logprobs=[dict(token='true',logprob=-2),dict(token='false',logprob=-.1)])])
 loop=checker.AttriGuardExecutionLoop(None,judge_llm=Stub('{"survive":true}',{'logprobs':lp}),survival_mode='fuzzy');got,branch=observed_call(loop,c,refs,q,w);assert not got and branch['path']=='JSON_LOGPROB_OVERRIDE'
 stub=Stub('{"survive":false}');loop=core.AttriGuardExecutionLoop(None,judge_llm=stub,survival_mode='fuzzy');assert loop._fuzzy_survive(c,[c],q,w.runtime,w.env)and stub.calls==0
 forced=variant(core,out/'forced','SOURCE',True);loop=forced.AttriGuardExecutionLoop(None,judge_llm=stub,survival_mode='fuzzy');assert not loop._fuzzy_survive(c,[c],q,w.runtime,w.env)and stub.calls==1
 for raw in ['{"survive":true}','```json\n{"survive":false}\n```','<think>done</think>\n```json\n{"survive":true}\n```']:assert inspect(raw)['interpretable']
 for raw in ['{"survive":"false"}','{"survive":true}{"survive":false}','{"survive":true,"survive":false}','prefix {"survive":true}','{"survive":false} trailing','<think>x</think><think>y</think>{"survive":true}']:assert not inspect(raw)['interpretable']
 assert not inspect('{"survive":true}','length')['interpretable']
 # Exercise the actual SDK/transport guard with synthetic responses. A changed
 # prepared body must be rejected before even the mock HTTP transport is called.
 from .worker import run_job
 from reference_study.common import read
 item=next(j for j in m['P1']if j['criterion']=='SOURCE'and j['candidate']=='EDIT')
 reference=out/'guard_reference'/item['id'];r=run_job(item,reference,family,True);assert r['qualified']
 records=read(reference/'model_io/driver_records.json');body=records[0]['request'];body['model']='deliberately_wrong_prepared_model'
 held=read(reference/'held_input.json');tampered=out/'guard_tamper'
 write(tampered/'prepared_requests.json',dict(bodies={item['input_key']:body},native_state_hash=held['native_state_sha256']))
 rejected=run_job(item,tampered/'P1'/item['id'],family,True)
 assert not rejected['qualified']and'Prepared request mismatch'in str(rejected['error'])
 assert read(tampered/'P1'/item['id']/'model_io/driver_records.json')==[]
 assert not list((tampered/'P1'/item['id']/'model_io/http').glob('*.request.json'))
 write(out/'qualification.json',dict(status='PASS',family=family,model_inference=0,source_identity=identity,checks=['336 acquisition / 384 position aliases','all native fields/directions/grants material','common initial native state','single-use slot controls','only grant changes','Case4 preserved','source parser AST and all decision paths','exact route vs forced controls','prospective terminal grammar','actual SDK prepared-body mismatch blocked before HTTP'],semantic_human_review='PENDING'))
 print('E2b CPU qualification PASS',family,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--family',choices=('qwen','gemma'),default='qwen');p.add_argument('--out',type=Path,required=True);a=p.parse_args();qualify(a.out,a.family)
