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

def rendering(snapshot,family,out,prepared):
 from .rendering import render
 return render(snapshot,family,out,prepared)

if __name__=='__main__':
 from .rendering import main
 main()
