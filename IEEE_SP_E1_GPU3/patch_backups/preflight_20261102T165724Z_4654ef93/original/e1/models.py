"""Pinned N1 local profiles, original auxiliary decoding, judge-only probes."""
from pathlib import Path
from diagnostic.models import profiles,command as original
from reference_study.common import write,activate

def command(python,snapshot,family):
 argv=original(python,snapshot,family);argv[argv.index('--max-num-seqs')+1]='8';return argv

def live(out,family):
 from .cases import world_for
 from .design import fixture,actions
 from .checker import variant
 from permission_admission.runtime import fixed_driver,strict_verdict
 from reference_discovery_parallel.base.source import load_source
 from agentdojo.functions_runtime import FunctionCall
 out=Path(out);out.mkdir(parents=True,exist_ok=False)
 spec,query=fixture('BANK','C2');w=world_for(spec);core,_=load_source();checker=variant(core,out,'DIRECT')
 d=fixed_driver(out/'model_io')
 try:
  loop=checker.AttriGuardExecutionLoop(None,judge_llm=d.policies['judge'],survival_mode='fuzzy')
  value=loop._fuzzy_survive(FunctionCall(**actions('BANK')['A']),[],query,w.runtime,w.env)
  replies=[r for r in d.records if r.get('response')]
  if not replies or replies[-1].get('finish_reason')!='stop':raise RuntimeError('Judge transport probe incomplete')
  write(out/'qualification.json',dict(status='PASS_TRANSPORT',semantic_correctness_not_gated=True,operative_decision=bool(value),
   strict_format_diagnostic=strict_verdict(replies[-1]),judge_requests=len(d.records),scope='One separate source-constructor direct-judge acquisition. No correctness gate; no actor/reference/attenuator inference.'))
 finally:d.close()

def rendering(snapshot,family,out):
 from transformers import AutoTokenizer
 from reference_discovery_parallel.models import template_path,prepare_fixture_messages,tokenization_artifact
 from reference_discovery_parallel.base.source import load_source
 from permission_admission.runtime import fixed_driver
 from .design import manifest
 from .worker import run_job
 from reference_study.common import sha,ROOT
 import tempfile,shutil
 out=Path(out);out.mkdir(parents=True,exist_ok=True);tokenizer=AutoTokenizer.from_pretrained(snapshot,local_files_only=True)
 custom=template_path(family);template=custom.read_text()if custom else tokenizer.chat_template
 if not isinstance(template,str):raise RuntimeError('Ambiguous chat template')
 # Get exact source-serialized bodies through mock SDK path, then render every unique input.
 # No actor/tool parser probe is needed for judge-only E1.
 seen=set();entries=[]
 with tempfile.TemporaryDirectory()as tmp:
  for item in manifest()['P1']:
   r=run_job(item,Path(tmp)/item['id'],family,True)
   if not r['qualified']:raise RuntimeError('CPU E1 request reconstruction failed: '+item['id'])
   from reference_study.common import read,digest
   body=read(Path(tmp)/item['id']/'model_io/driver_records.json')[0]['request'];key=digest(body)
   if key in seen:continue
   seen.add(key);messages=body['messages'];conversation,fmt=prepare_fixture_messages(tokenizer,template,messages,[])
   rendered=tokenizer.apply_chat_template(conversation,chat_template=template,tokenize=False,add_generation_prompt=True)
   tokens=tokenizer.apply_chat_template(conversation,chat_template=template,tokenize=True,add_generation_prompt=True)
   # Both the trusted grant and actual candidate arguments must survive template rendering.
   if 'TRUSTED_OWNER_POLICY_AND_STATE'not in rendered or 'original_action'not in rendered:raise RuntimeError('Template lost E1 task/candidate')
   row=dict(id=item['id'],request=body,template_messages=conversation,content_format=fmt,rendered=rendered,**tokenization_artifact(tokens))
   write(out/'inputs'/(key+'.json'),row);entries.append(dict(request_hash=key,first_position=item['id'],tokens=len(row['token_ids'])))
 (out/'effective_template.jinja').write_text(template)
 write(out/'qualification.json',dict(status='PASS',model_inference=0,profile=profiles()[family],unique_inputs=len(entries),entries=entries,
  scope='Every unique scientific input rendered through installed vLLM text path and actual cached tokenizer. Exact requests also captured on wire during generation; /tokenize diagnostics do not attest generation-consumed tokens.'))

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--snapshot',type=Path,required=True);p.add_argument('--family',choices=('qwen','gemma'),required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();activate(a.family);rendering(a.snapshot,a.family,a.out)
