"""Serving-only CPU renderer. Research dependencies are intentionally absent."""
import argparse,sys
from pathlib import Path
from reference_study.common import ROOT,read,write,digest,sha

def render(snapshot,family,out,prepared):
 # Do not call activate(): it imports the research transport and OpenAI SDK.
 sys.path.insert(0,str(ROOT/'retained'))
 from transformers import AutoTokenizer
 from reference_discovery_parallel.models import template_path,prepare_fixture_messages,tokenization_artifact
 from diagnostic.models import profiles
 data=read(prepared)
 if data.get('version')!='E1_RENDER_INPUTS_V1'or data['family']!=family:raise RuntimeError('Prepared request profile/version mismatch')
 if data['source_manifest_sha256']!=sha(ROOT/'PACKAGE_MANIFEST.json'):raise RuntimeError('Prepared requests came from another source version')
 if data.get('model_inference')!=0 or len(data['positions'])!=180:raise RuntimeError('Unexpected request preparation scope')
 if len({r['id']for r in data['positions']})!=180:raise RuntimeError('Duplicate scheduled position')
 for p in data['positions']:
  if p['request_hash']not in data['unique_requests']:raise RuntimeError('Prepared position has no body')
 tokenizer=AutoTokenizer.from_pretrained(snapshot,local_files_only=True)
 custom=template_path(family);template=custom.read_text()if custom else tokenizer.chat_template
 if not isinstance(template,str):raise RuntimeError('Ambiguous chat template')
 out=Path(out);out.mkdir(parents=True,exist_ok=False);entries=[]
 for key,value in sorted(data['unique_requests'].items()):
  body=value['request']
  if digest(body)!=key:raise RuntimeError('Prepared body digest mismatch')
  if body['model']!=profiles()[family]['alias']:raise RuntimeError('Prepared model alias differs from serving profile')
  conversation,fmt=prepare_fixture_messages(tokenizer,template,body['messages'],[])
  rendered=tokenizer.apply_chat_template(conversation,chat_template=template,tokenize=False,add_generation_prompt=True)
  tokens=tokenizer.apply_chat_template(conversation,chat_template=template,tokenize=True,add_generation_prompt=True)
  if 'TRUSTED_OWNER_POLICY_AND_STATE'not in rendered or 'original_action'not in rendered:raise RuntimeError('Template lost E1 task/candidate')
  row=dict(id=value['first_position'],request=body,template_messages=conversation,content_format=fmt,rendered=rendered,**tokenization_artifact(tokens))
  write(out/'inputs'/(key+'.json'),row);entries.append(dict(request_hash=key,first_position=value['first_position'],tokens=len(row['token_ids'])))
 (out/'effective_template.jinja').write_text(template)
 write(out/'qualification.json',dict(status='PASS',model_inference=0,profile=profiles()[family],unique_inputs=len(entries),entries=entries,
  prepared_requests_sha256=sha(prepared),research_dependencies_loaded=any(k=='agentdojo'or k.startswith('agentdojo.')for k in sys.modules),
  scope='Research-serialized requests rendered in isolated serving environment through installed vLLM text path and actual cached tokenizer. No model inference; wire requests separately recorded during generation.'))
 print('RENDERING PASS',family,len(entries),'unique inputs; zero model inference',flush=True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--snapshot',type=Path,required=True);p.add_argument('--family',choices=('qwen','gemma'),required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--prepared',type=Path,required=True);a=p.parse_args();render(a.snapshot,a.family,a.out,a.prepared)
if __name__=='__main__':main()
