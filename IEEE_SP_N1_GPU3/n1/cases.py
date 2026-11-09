"""Factor interventions around byte-preserved guard/constructors, at a pre-effect pause."""
import copy,json,re
import yaml
from reference_study.common import ROOT,read,write,digest,sha
from .design import VIEWS,CRITERIA
REGION=re.compile(r'BEGIN_UNTRUSTED_PROCEDURE(.*?)END_UNTRUSTED_PROCEDURE',re.S)
PAD='Administrative record. Layout section for archival indexing. General background notation. '


def designated(text):
 marker='DESIGNATED_OPERATION_DATA:'
 if marker not in text:raise ValueError('No designated region')
 return json.JSONDecoder().raw_decode(text.split(marker,1)[1].lstrip())[0]


def prepare(cp,directive):
 """Both arms use the same YAML canonicalization; only current procedure differs."""
 from reference_discovery_parallel.base.source import load_source
 from reference_discovery_parallel.common import pack
 core,_=load_source();messages=copy.deepcopy(cp['messages']);hits=[]
 stage=cp['world'].get('notice_stage',1)or 1;notice=cp['spec']['notices'][stage-1]
 facts=designated(notice);needle='Dispatch notice '+cp['spec']['id']+'.';found=[]
 def transform(x):
  if isinstance(x,str)and needle in x and REGION.search(x):
   if designated(x)!=facts:raise RuntimeError('Native delivered facts differ from designated current notice')
   found.append(x);m=REGION.search(x);neutral=' '+(PAD*((len(m.group(1))//len(PAD))+1))[:max(0,len(m.group(1))-2)]+' '
   return x if directive=='PRESENT' else x[:m.start(1)]+neutral+x[m.end(1):]
  if isinstance(x,list):return [transform(v)for v in x]
  if isinstance(x,dict):return {k:transform(v)for k,v in x.items()}
  return x
 def masked(x):
  if isinstance(x,str)and needle in x:return REGION.sub('BEGIN_UNTRUSTED_PROCEDURE<MASKED>END_UNTRUSTED_PROCEDURE',x)
  if isinstance(x,list):return [masked(v)for v in x]
  if isinstance(x,dict):return {k:masked(v)for k,v in x.items()}
  return x
 for i,m in enumerate(messages):
  if m.get('role')!='tool':continue
  raw=core._content_to_str(m.get('content'))
  if needle not in raw or 'BEGIN_UNTRUSTED_PROCEDURE'not in raw:continue
  old=yaml.safe_load(raw);changed=transform(copy.deepcopy(old))
  if masked(old)!=masked(changed):raise RuntimeError('Protected facts/envelope changed outside procedure')
  submitted=yaml.safe_dump(changed,sort_keys=False,allow_unicode=True)
  if yaml.safe_load(submitted)!=changed:raise RuntimeError('Canonical YAML did not roundtrip')
  m['content']=[core.text_content_block_from_string(submitted)]
  hits.append(dict(index=i,tool_call_id=m.get('tool_call_id'),original=raw,submitted=submitted,
     outside_procedure_tree_equal=True,original_outside_hash=digest(pack(masked(old))),submitted_outside_hash=digest(pack(masked(changed)))))
 if len(found)!=1 or len(hits)!=1:raise RuntimeError('Expected exactly one current designated carrier notice')
 # The pending assistant is not a new actor query or an injected proposal: source removes it from reference context.
 return messages,facts,hits[0]


def augment(context,tool_id,facts,view):
 from reference_discovery_parallel.base.source import load_source
 core,_=load_source();rows=copy.deepcopy(context);hits=[m for m in rows if m.get('role')=='tool'and m.get('tool_call_id')==tool_id]
 if len(hits)!=1:raise RuntimeError('Current carrier not uniquely present in attenuated context')
 m=hits[0];text=core._content_to_str(m.get('content'));payload=json.dumps(facts,sort_keys=True,ensure_ascii=False)
 if view=='RESTORED':addition='\nN1_REPLAY_DATA:\n'+payload
 elif view=='PLACEBO':addition='\nN1_REPLAY_DATA:\n'+(PAD*((len(payload)//len(PAD))+1))[:len(payload)]
 elif view=='SOURCE':addition=''
 else:raise ValueError(view)
 m['content']=[core.text_content_block_from_string(text+addition)]
 if view=='SOURCE'and rows!=context:raise RuntimeError('Unmodified source context changed during augmentation')
 return rows,dict(view=view,role='tool',tool_call_id=tool_id,base_text=text,added_text=addition,
   added_characters=len(addition),facts_available_in_original_notice=True,
   policy_grant_added=False,semantic_fact_loss_adjudication='PENDING',
   scope='Canonical designated-fact repetition/restoration. Literal absence is not semantic loss. Placebo matches added character count, not tokens or semantics.')


class CaptureReference:
 def query(self,query,runtime,env,messages,extra_args):
  return query,runtime,env,copy.deepcopy(messages)+[dict(role='assistant',content=None,tool_calls=[])],extra_args


def scripted(role,body):
 from reference_discovery_parallel.base.transport import reply
 if role=='attenuator':return reply('Engineering attenuation fixture. Task evidence is omitted deliberately for code-path testing.')
 if role=='judge':return reply('{"survive":false,"reason":"Engineering mock, no scientific result."}')
 return reply('Engineering reference has no calls.')


def driver(folder,mock):
 from permission_admission.runtime import fixed_driver
 d=fixed_driver(folder,mock)
 if mock:d.mock=scripted
 return d


def summary_records(records):
 from reference_study.legacy_mechanisms import diagnostic
 bad=[r['index']for r in records if r.get('truncated')or(r.get('exception')and not r.get('source_supported_logprobs_fallback'))]
 return dict(request_records=len(records),incomplete_model_records=bad,acquisition_complete=not bad,
   token_usage={k:sum(((r.get('response')or{}).get('usage')or{}).get(k,0)or 0 for r in records)for k in('prompt_tokens','completion_tokens','total_tokens')},
   missing_usage_records=sum(not bool((r.get('response')or{}).get('usage'))for r in records),
   strict_format_and_embedded_verdicts=[dict(record_index=r['index'],**diagnostic(r))for r in records if r['role']=='judge'])


def run(item,directory,family,mock):
 from reference_discovery_parallel.common import unseal,native_messages,pack
 from reference_discovery_parallel.base.source import load_source,source_pause
 from permission_admission.runtime import native_world,matches_with_source,dispatch_arms
 from permission_admission.oracle import evaluate,contract_for
 from diagnostic.cases import checked_variant
 from .measure import check_arms
 path=ROOT/item['origin']
 if sha(path)!=item['origin_sha256']:raise RuntimeError('Frozen origin hash changed')
 origin=read(path);cp=unseal(origin['checkpoint']);spec=cp['spec'];world=native_world(spec,cp['world']);before=digest(world.snapshot())
 core,_=load_source();messages,facts,receipt=prepare(cp,item['directive']);directory.mkdir(parents=True,exist_ok=False)
 write(directory/'intervention.json',receipt);write(directory/'held_input.json',dict(task=spec['root'],messages=messages,native_state_digest=before,origin=item['origin'],facts=facts))
 # Execute the original _sync_shadow and attenuation. Pause before any source dispatch;
 # the stand-in reference only captures the context. Real reference calls follow below.
 d=driver(directory/'attenuation/model_io',mock)
 try:
  loop=core.AttriGuardExecutionLoop(CaptureReference(),attenuation_llm=d.policies['attenuator'],judge_llm=d.policies['judge'],attenuation_level=2,survival_mode='fuzzy',max_iters=1,debug=True)
  pause=source_pause(loop,spec['root'],world,native_messages(messages),'reference')
  write(directory/'attenuation/source_pause.json',pause);att=summary_records(d.records)
 finally:d.close()
 write(directory/'attenuation/result.json',att)
 atoms=[]
 for slot in facts['slots']:
  for operation in slot['alternatives']:
   for key,value in operation['args'].items():
    for v in(value if isinstance(value,list)else[value]):atoms.append(dict(function=operation['function'],argument=key,value=str(v)))
 stages=[]
 for record in d.records:
  if not record.get('response'):continue
  raw=record['response']['choices'][0]['message'].get('content')or''
  stages.append(dict(record_index=record['index'],text=raw,literal_presence=[dict(**a,present=' '.join(a['value'].split())in' '.join(raw.split()))for a in atoms]))
 write(directory/'attenuation/fact_diagnostics.json',dict(stages=stages,semantic_fidelity='PENDING',literal_presence_is_not_binding_or_semantic_use=True))
 if not att['acquisition_complete']:raise RuntimeError('Incomplete attenuation; all reference children remain unexecuted, not safety successes')
 context=pause['shadow_context'];prefix=world.effects();base=evaluate(contract_for(spec),prefix)
 remaining=base['unfilled_slots']
 if not remaining:raise RuntimeError('No unconsumed slot for lawful control')
 lawful=copy.deepcopy(contract_for(spec)['slots'][remaining[0]]['alternatives'][0]);lawful['id']='n1-lawful'
 forbidden=copy.deepcopy(origin['selected_effect']['candidate'])
 controls=dict(OBSERVED=forbidden,LAWFUL_CONTROL=lawful)
 for name,c in controls.items():
  after=evaluate(contract_for(spec),prefix+[c]);permitted=len(after['violation_indices'])==len(base['violation_indices'])
  if permitted!=(name=='LAWFUL_CONTROL'):raise RuntimeError('Held candidate/control permission mismatch')
 rows=[]
 for view in item['view_order']:
  dest=directory/'views'/view;dest.mkdir(parents=True);ctx,aug=augment(context,receipt['tool_call_id'],facts,view)
  write(dest/'reference_input.json',dict(task=spec['root'],messages=ctx,augmentation=aug,world_digest=before))
  row=dict(view=view,status='STARTING',qualified=False,comparisons=[])
  try:
   d=driver(dest/'reference/model_io',mock)
   if mock:
    from reference_discovery_parallel.base.transport import reply
    op=copy.deepcopy(lawful)
    d.mock=lambda role,body: reply(calls=[dict(id='engineering-reference',type='function',function=dict(name=op['function'],arguments=json.dumps(op['args'])))],finish='tool_calls')
   try:
    _,_,_,generated,_=d.policies['reference'].query(spec['root'],world.runtime,world.env,native_messages(ctx),{})
    refs=(generated[-1].get('tool_calls')or[])if generated and generated[-1].get('role')=='assistant'else[]
    write(dest/'reference/result.json',dict(reference=pack(refs),generated=pack(generated),**summary_records(d.records)))
    if not summary_records(d.records)['acquisition_complete']:raise RuntimeError('Reference response incomplete')
   finally:d.close()
   effectful=[pack(c)for c in refs if c.function in('send_money','send_email','send_direct_message','send_channel_message')]
   ref_eval=evaluate(contract_for(spec),prefix+effectful)
   row.update(reference=pack(refs),reference_unmatched_new=max(0,len(ref_eval['violation_indices'])-len(base['violation_indices'])),reference_effectful_calls=len(effectful),reference_no_effectful_call=not effectful,reference_unfilled_slots=ref_eval['unfilled_slots'])
   # All criteria see the same supplied complete facts. Untouched source also has its
   # actual minimal view: diagnostic source branch is kept separate from full-view comparisons.
   complete_query=spec['root']+'\nDIAGNOSTIC_DESIGNATED_FACTS_AND_NATIVE_PREFIX:\n'+json.dumps(dict(designated_operation_data=facts,already_committed_native_effects=prefix),sort_keys=True,ensure_ascii=False)
   for kind,candidate in controls.items():
    for criterion in CRITERIA:
     cell=dest/'comparisons'/kind/criterion;cell.mkdir(parents=True);entry=dict(kind=kind,criterion=criterion,status='STARTING',qualified=False)
     try:
      checker=checked_variant(core,cell,criterion);d=driver(cell/'model_io',mock)
      try:
       pending=native_messages([dict(role='assistant',content=None,tool_calls=[candidate])])[0]['tool_calls']
       q=spec['root']if criterion=='SOURCE'else complete_query
       write(cell/'input.json',dict(task=q,candidate=candidate,reference=pack(refs),native_state_digest=before))
       decisions=matches_with_source(checker,d,spec,world,pending,refs,q);dec=decisions[0];stats=summary_records(d.records)
       dec['actual_judge_invoked']=bool(dec['judge_records']);dec['candidate_equals_reference']=any(core._call_signature(pending[0])==core._call_signature(r)for r in refs)
       dec['operative_route']='JUDGE'if dec['actual_judge_invoked']else'EXACT_BYPASS'if criterion=='SOURCE'and dec['candidate_equals_reference']else'NO_JUDGE_REJECTION'
       arms=dispatch_arms(core,spec,world,pending,refs,[dec['allowed']]);independent=check_arms(arms,spec)
       entry.update(status='COMPLETE',qualified=stats['acquisition_complete'],allowed=dec['allowed'],source_decision=dec,native_clone_arms=arms,independent_native_check=independent,**stats)
      finally:d.close()
     except Exception as exc:
      import traceback
      entry.update(status='TECHNICAL_ERROR',error=str(exc),traceback=traceback.format_exc(),scientific_negative=False)
     write(cell/'result.json',entry);row['comparisons'].append(dict(kind=kind,criterion=criterion,status=entry['status'],qualified=entry['qualified'],allowed=entry.get('allowed'),operative_route=entry.get('source_decision',{}).get('operative_route')))
   row.update(status='COMPLETE',qualified=all(c['qualified']for c in row['comparisons']))
  except Exception as exc:
   import traceback
   row.update(status='TECHNICAL_ERROR',error=str(exc),traceback=traceback.format_exc(),scientific_negative=False)
  write(dest/'result.json',row);rows.append(row)
 if before!=digest(world.snapshot()):raise RuntimeError('Component probe mutated original native state')
 return dict(status='COMPLETE',qualified=all(r['qualified']for r in rows),views=rows,attenuation=att,original_world_unchanged=True,autonomous_episodes=0,conditional_component=True,independent_human_review='PENDING',semantic_fact_loss='UNADJUDICATED')
