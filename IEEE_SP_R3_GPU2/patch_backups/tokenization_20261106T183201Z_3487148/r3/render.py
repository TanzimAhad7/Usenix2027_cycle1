"""CPU rendering of actual official-client wire fixtures, no model weights."""
import argparse,hashlib,json
from pathlib import Path
from .common import read,write

def render(snapshot,prepared,out):
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(snapshot,local_files_only=True)
    template=tok.chat_template
    if not isinstance(template,str):raise RuntimeError('An unambiguous native text chat template is required')
    requests=read(prepared);records=[]
    for i,r in enumerate(requests):
        msgs=r['request']['messages'];text=tok.apply_chat_template(msgs,tokenize=False,add_generation_prompt=True)
        ids=tok.apply_chat_template(msgs,tokenize=True,add_generation_prompt=True)
        if not ids or not all(isinstance(v,int) for v in ids):raise RuntimeError('Invalid native tokenization')
        if any(m['content'].strip() and m['content'].strip() not in text for m in msgs):raise RuntimeError('Native template changed/dropped source request content')
        records.append(dict(index=i,role=r['role'],rendered=text,token_ids=ids,request=r['request']))
    write(out/'rendered_requests.json',records);(out/'native_chat_template.jinja').write_text(template)
    write(out/'qualification.json',dict(status='PASS',new_model_inference=0,requests=len(records),native_template_sha256=hashlib.sha256(template.encode()).hexdigest(),scope='Actual released LocalLLM text requests rendered/tokenized by cached tokenizer; live owned server remains a separate qualification'))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--snapshot',type=Path,required=True);p.add_argument('--prepared',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);render(a.snapshot,a.prepared,a.out)
