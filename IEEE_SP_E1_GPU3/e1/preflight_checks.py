"""Dependency-boundary regression; stub rendering is not a real-tokenizer test."""
import argparse,importlib.abc,importlib.util,json,sys,tempfile,types
from pathlib import Path
from reference_study.common import ROOT,read,write

class ResearchBlocker(importlib.abc.MetaPathFinder):
 def __init__(self):self.hits=[]
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0]in ('agentdojo','openai','cohere','anthropic'):
   self.hits.append(fullname);raise ModuleNotFoundError('Research-only dependency blocked: '+fullname)

class Tokenizer:
 chat_template='STUB_TEMPLATE_FOR_BOUNDARY_TEST_ONLY'
 @classmethod
 def from_pretrained(cls,*args,**kwargs):return cls()
 def apply_chat_template(self,conversation,tokenize=False,**kwargs):
  text=json.dumps(conversation,sort_keys=True)
  return [ord(c)for c in text]if tokenize else text

def check(prepared,family,out,before=None):
 # Run as its own Python process: no already-loaded research dependencies.
 for name in ('agentdojo','openai','cohere','anthropic'):
  if name in sys.modules:raise RuntimeError('Boundary check requires fresh process')
 sys.path.insert(0,str(ROOT/'retained'));blocker=ResearchBlocker();sys.meta_path.insert(0,blocker)
 def module(name):
  m=types.ModuleType(name);sys.modules[name]=m;return m
 module('transformers').AutoTokenizer=Tokenizer
 for name in ('vllm','vllm.entrypoints','vllm.renderers'):module(name)
 module('vllm.entrypoints.chat_utils').parse_chat_messages=lambda messages,config,content_format:(messages,None,None)
 module('vllm.renderers.hf').resolve_chat_template_content_format=lambda **kwargs:'string'
 from .rendering import render
 with tempfile.TemporaryDirectory()as tmp:
  render(Path(tmp)/'stub_snapshot',family,Path(tmp)/'rendered',prepared)
  q=read(Path(tmp)/'rendered/qualification.json')
  assert q['unique_inputs']==60 and q['research_dependencies_loaded']is False and blocker.hits==[]
  data=read(prepared);key=next(iter(data['unique_requests']));data['unique_requests'][key]['request']['model']='tampered'
  write(Path(tmp)/'tampered.json',data)
  try:render(Path(tmp)/'stub_snapshot',family,Path(tmp)/'tampered_render',Path(tmp)/'tampered.json');raise AssertionError('Tampered prepared body accepted')
  except RuntimeError as e:assert 'digest mismatch'in str(e)
  if before:
   spec=importlib.util.spec_from_file_location('e1._old_preflight',before);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
   try:old.rendering(Path(tmp)/'stub_snapshot',family,Path(tmp)/'old');raise AssertionError('Old preflight unexpectedly survived missing research dependencies')
   except (RuntimeError,ModuleNotFoundError):pass
   assert any(x.startswith('agentdojo')or x.startswith('openai')for x in blocker.hits)
 write(out,dict(status='PASS',family=family,prepared_positions=180,unique_inputs=60,model_inference=0,
  fixed_renderer_research_dependency_imports=0,old_defect_reproduced=bool(before),tampered_body_rejected=True,
  scope='Real source-serialized requests; AgentDojo/OpenAI/cohere/anthropic imports blocked. Stub HF/vLLM rendering verifies dependency separation only, not real cached tokenizer/server compatibility.'))
 print('BOUNDARY CHECK PASS',family,'old defect reproduced='+str(bool(before)),'zero GPU/model inference',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--prepared',type=Path,required=True);p.add_argument('--family',choices=('qwen','gemma'),required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--before',type=Path);a=p.parse_args();check(a.prepared,a.family,a.out,a.before)
