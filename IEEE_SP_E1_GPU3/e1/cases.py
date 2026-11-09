"""One acquired scientific judge decision, never an autonomous workflow."""
import copy
from reference_study.common import write,digest
from .design import fixture,actions,expected
from .checker import variant
from .measure import dispatch

def world_for(spec):
 from permission_admission.runtime import native_world
 w=native_world(spec);w.carrier_created=True # Suppress legacy notice injection in held clean state.
 return w

class RecordPolicy:
 def __init__(self,policy):self.policy=policy;self.records=[]
 def query(self,query,runtime,env,messages,extra):
  from reference_discovery_parallel.common import pack
  record=dict(query=query,messages=pack(messages),extra=pack(extra));self.records.append(record)
  try:
   answer=self.policy.query(query,runtime,env,messages,extra)
  except BaseException as e:
   record['error']=dict(type=type(e).__name__,message=str(e));raise
  record.update(output_messages=pack(answer[3]),output_extra=pack(answer[4]));return answer

class Replay:
 def __init__(self,records):self.records=copy.deepcopy(records);self.index=0
 def query(self,query,runtime,env,messages,extra):
  from reference_discovery_parallel.common import pack,native_messages
  r=self.records[self.index];self.index+=1
  if (query,pack(messages),pack(extra))!=(r['query'],r['messages'],r['extra']):raise RuntimeError('Natural source replay request differs')
  if 'error'in r:raise RuntimeError(r['error']['message']) # Replays only acquired source-supported fallback.
  return query,runtime,env,native_messages(r['output_messages']),copy.deepcopy(r['output_extra'])

def run(item,directory,family,mock=False):
 from permission_admission.runtime import fixed_driver,strict_verdict
 from reference_discovery_parallel.base.source import load_source
 from reference_discovery_parallel.base.transport import reply
 from agentdojo.functions_runtime import FunctionCall
 from reference_study.legacy_mechanisms import diagnostic
 directory.mkdir(parents=True,exist_ok=False)
 core,_=load_source();spec,query=fixture(item['setting'],item['policy']);world=world_for(spec);before=world.snapshot()
 pair=actions(item['setting']);c=copy.deepcopy(pair[item['candidate']]);c['id']='candidate'
 refs=[]if item['reference']=='NONE'else[dict(**copy.deepcopy(pair[item['reference']]),id='reference')]
 candidate=FunctionCall(**c);references=[FunctionCall(**r)for r in refs]
 write(directory/'held_input.json',dict(task=query,candidate=c,reference=refs,native_state=before,native_state_sha256=digest(before),
  origin=item['origin'],origin_sha256=item['origin_sha256'],derived_constructed_task=True,policy_is_authored=True,semantic_review='PENDING'))
 driver=fixed_driver(directory/'model_io',mock)
 if mock:
  # Engineering fixtures exercise both decisions. Never included in scientific tables.
  driver.mock=lambda role,body:reply('{"survive":'+str(expected(item)).lower()+',"reason":"ENGINEERING MOCK ONLY"}')
 recorder=RecordPolicy(driver.policies['judge'])
 try:
  checker=variant(core,directory,item['criterion'])
  loop=checker.AttriGuardExecutionLoop(None,judge_llm=recorder,survival_mode='fuzzy',max_iters=1,debug=True)
  allowed=bool(loop._fuzzy_survive(candidate,references,query,world.runtime,world.env))
  responses=[r for r in driver.records if r.get('response')]
  if not responses:raise RuntimeError('Forced-review scientific position did not acquire a judge response')
  terminal=responses[-1];strict=strict_verdict(terminal);diag=diagnostic(terminal)
  # Qualified = completed acquisition with whole JSON boolean, nontruncated response.
  # All operative decisions, including source substring fallback, remain recorded.
  qualified=bool(strict['valid']and terminal.get('finish_reason')=='stop')
  natural=dict(status='NOT_APPLICABLE_TO_CHANGED_INSTRUCTION',new_inference=0)
  if refs and item['candidate']==item['reference']:
   deny=Replay([]);nl=core.AttriGuardExecutionLoop(None,judge_llm=deny,survival_mode='fuzzy')
   natural=dict(status='EXACT_BYPASS',allowed=bool(nl._fuzzy_survive(candidate,references,query,world.runtime,world.env)),judge_invoked=False,new_inference=0)
  elif item['criterion']=='FUZZY':
   replay=Replay(recorder.records);nl=core.AttriGuardExecutionLoop(None,judge_llm=replay,survival_mode='fuzzy')
   answer=bool(nl._fuzzy_survive(candidate,references,query,world.runtime,world.env))
   if replay.index!=len(recorder.records)or answer!=allowed:raise RuntimeError('Untouched source replay mismatch')
   natural=dict(status='FUZZY_SAME_REPLY_REPLAY',allowed=answer,judge_invoked=True,new_inference=0,request_identity_verified=True)
  arms=dict(JUDGE_RELEASE=dispatch(core,world,c,item['setting'],item['policy'],allowed),
   FORCE_COMMIT_CALIBRATION=dispatch(core,world,c,item['setting'],item['policy'],True))
  if digest(world.snapshot())!=digest(before):raise RuntimeError('Original native state changed')
  if arms['FORCE_COMMIT_CALIBRATION']['assessment']['committed_count']!=1:raise RuntimeError('Force-commit native calibration did not create exactly one effect')
  if arms['FORCE_COMMIT_CALIBRATION']['assessment']['violation']==expected(item):raise RuntimeError('Independent native assessment disagrees with authored permission')
  request=terminal['request'];write(directory/'policy_transcript.json',recorder.records)
  return dict(status='COMPLETE'if qualified else'UNQUALIFIED_RESPONSE',qualified=qualified,allowed=allowed,candidate_permitted=expected(item),
   strict_verdict=strict,format_diagnostic=diag,source_reason=loop._last_judge_reason,operative_parser='Unchanged source JSON/logprobs/substring fallback',
   natural_source_route=natural,native_clone_arms=arms,judge_requests=len(driver.records),actual_judge_invoked=True,
   request_sha256=digest(request),input_sha256=digest({k:v for k,v in request.items()if k!='model'}),
   model_decoding=driver.profile['judge'],conditional_not_autonomous=True,interpretation='Authored finite discovery set; independent semantic review pending.')
 finally:driver.close()
