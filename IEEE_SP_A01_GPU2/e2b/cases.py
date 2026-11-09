import copy,inspect,json,sys
from pathlib import Path
from reference_study.common import digest,read,write
from e1.cases import RecordPolicy,Replay,world_for
from .design import inputs,native_spec,key_for,expected
from .checker import variant
from .terminal import inspect as terminal_inspect
from .measure import dispatch

def observed_call(loop,candidate,refs,query,world):
 method=loop._fuzzy_survive;code=method.__func__.__code__;lines,start=inspect.getsourcelines(method);source={start+i:l.strip()for i,l in enumerate(lines)}
 observed=dict(path='UNKNOWN',logprob_override=False);old=sys.gettrace()
 def trace(frame,event,arg):
  if frame.f_code is code and event=='line':
   line=source.get(frame.f_lineno,'')
   if line=='survive = true_lp >= false_lp':observed['logprob_override']=True
   if line=='return survive':observed['path']='JSON_LOGPROB_OVERRIDE'if observed['logprob_override']else'JSON_BOOLEAN'
   if line=='return "true" in raw.lower()':observed['path']='SUBSTRING_FALLBACK'
  return trace
 try:sys.settrace(trace);allow=method(candidate,refs,query,world.runtime,world.env)
 finally:sys.settrace(old)
 if type(allow)is not bool:raise RuntimeError('Non-Boolean source decision')
 return allow,observed

def run(item,directory,family,mock=False):
 from permission_admission.runtime import fixed_driver
 from reference_discovery_parallel.base.source import load_source
 from reference_discovery_parallel.base.transport import reply
 from agentdojo.functions_runtime import FunctionCall
 directory=Path(directory);directory.mkdir(parents=True,exist_ok=False);core,_=load_source()
 query,c,refs,allowed=inputs(item);world=world_for(native_spec());before=world.snapshot()
 if key_for(item)!=item['input_key']:raise RuntimeError('Logical input differs from manifest')
 planfile=directory.parents[1]/'prepared_requests.json';plan=read(planfile)if planfile.is_file()else None
 if not mock and plan is None:raise RuntimeError('Missing frozen serving request')
 write(directory/'held_input.json',dict(task=query,candidate=c,references=refs,native_state=before,native_state_sha256=digest(before),allowed_operations=allowed,input_key=item['input_key'],aliases=item['aliases'],semantic_review='PENDING'))
 driver=fixed_driver(directory/'model_io',mock)
 if plan:
  from reference_discovery_parallel.base.transport import wire
  frozen=plan['bodies'][item['input_key']]
  if digest(before)!=plan['native_state_hash']:raise RuntimeError('Native state differs before acquisition')
  original_create=driver.create
  def checked_create(create,kwargs):
   body=wire(kwargs)
   fallback={k:v for k,v in frozen.items()if k not in ('logprobs','top_logprobs')}
   if body!=frozen and not(body==fallback and driver.records and driver.records[-1].get('source_supported_logprobs_fallback')):
    raise RuntimeError('Prepared request mismatch rejected before HTTP/model inference')
   return original_create(create,kwargs)
  driver.create=checked_create
 if mock:driver.mock=lambda role,body:reply(json.dumps(dict(survive=expected(item),reason='ENGINEERING MOCK ONLY')))
 recorder=RecordPolicy(driver.policies['judge'])
 try:
  checker=variant(core,directory,item['criterion'],item['candidate']=='REF'and item['criterion']!='DIRECT')
  candidate=FunctionCall(**copy.deepcopy(c));references=[FunctionCall(**copy.deepcopy(r))for r in refs]
  loop=checker.AttriGuardExecutionLoop(None,judge_llm=recorder,survival_mode='fuzzy',max_iters=1,debug=True)
  allow,branch=observed_call(loop,candidate,references,query,world)
  responses=[r for r in driver.records if r.get('response')]
  if not responses or len(driver.records)>2 or any(r['role']!='judge'for r in driver.records):raise RuntimeError('Acquisition budget/role failure')
  if len(driver.records)==2 and not driver.records[0].get('source_supported_logprobs_fallback'):raise RuntimeError('Undeclared extra request')
  last=responses[-1];body=last['request'];choice=last['response']['choices'][0];diagnostic=terminal_inspect(choice['message'].get('content')or'',choice.get('finish_reason'))
  if plan:
   frozen=plan['bodies'][item['input_key']];fallback={k:v for k,v in frozen.items()if k not in ('logprobs','top_logprobs')}
   if any(r['request']not in (frozen,fallback)for r in driver.records)or digest(before)!=plan['native_state_hash']:raise RuntimeError('Actual body/state differs from preflight')
  write(directory/'operative_decision.json',dict(allowed=allow,source_branch=branch,terminal_verdict=diagnostic,finish_reason=choice.get('finish_reason'),request_sha256=digest(body),prepared_request_verified=plan is not None,mock=mock))
  primary=dispatch(core,world,c,allowed,allow,directory/'native/JUDGE_RELEASE')
  calibration=dispatch(core,world,c,allowed,True,directory/'native/FORCE_COMMIT')
  if calibration['assessment']['committed_count']!=1 or calibration['assessment']['violation']==expected(item):raise RuntimeError('Native calibration failed')
  if digest(world.snapshot())!=digest(before):raise RuntimeError('Initial native state mutated')
  natural=dict(status='NOT_AN_UNTOUCHED_COMPARISON',new_inference=0)
  if item['candidate']=='REF'and item['criterion']!='DIRECT':natural=dict(status='EXACT_BYPASS',allowed=True,judge_invoked=False,new_inference=0)
  elif item['criterion']=='SOURCE':
   replay=Replay(recorder.records);nl=core.AttriGuardExecutionLoop(None,judge_llm=replay,survival_mode='fuzzy')
   if nl._fuzzy_survive(candidate,references,query,world.runtime,world.env)!=allow or replay.index!=len(recorder.records):raise RuntimeError('Intact source acquired-reply replay differs')
   natural=dict(status='INTACT_FUZZY_SAME_REPLY',allowed=allow,judge_invoked=True,new_inference=0)
  write(directory/'policy_transcript.json',recorder.records)
  return dict(status='COMPLETE',qualified=True,primary_observed=True,allowed=allow,candidate_permitted=expected(item),terminal_verdict=diagnostic,source_branch=branch,natural_source_route=natural,native_clone_arms=dict(JUDGE_RELEASE=primary,FORCE_COMMIT_CALIBRATION=calibration),judge_requests=len(driver.records),source_reason=loop._last_judge_reason)
 finally:driver.close()
