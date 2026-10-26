"""Frozen model profiles. Changing an interface creates a different profile."""
from pathlib import Path
from collections.abc import Mapping

def prepare_fixture_messages(tokenizer,template,messages,tools):
    """Use the installed vLLM CPU text-message path before HF rendering.

    These fixtures contain text only: no MM processor or model weights are
    needed. The namespace supplies only fields read by that text-only path;
    it is not asserted to be the live server's full ModelConfig. The real
    owned-server generation probes remain mandatory before scientific cases.
    """
    import copy
    from types import SimpleNamespace
    from vllm.entrypoints.chat_utils import parse_chat_messages
    from vllm.renderers.hf import resolve_chat_template_content_format
    config=SimpleNamespace(multimodal_config=None,enable_prompt_embeds=False,
        allowed_local_media_path='',allowed_media_domains=[],
        hf_config=SimpleNamespace(use_unified_vision_chunk=False))
    content_format=resolve_chat_template_content_format(chat_template=template,
        tools=tools or None,given_format='auto',tokenizer=tokenizer,model_config=config)
    conversation,mm_data,mm_uuids=parse_chat_messages(copy.deepcopy(messages),config,content_format=content_format)
    if mm_data is not None or mm_uuids is not None:
        raise RuntimeError('Text-only qualification fixture unexpectedly produced media')
    return conversation,content_format

def tokenization_artifact(value):
    """Serialize actual tokenizer output; never change generation/tokenization.

    Transformers may return a list or a BatchEncoding mapping. Preserve the
    complete mapping, including masks, while exposing one flat input_ids list
    for this single-conversation fixture. No str/repr fallback hides bad data.
    """
    def plain(x):
        if isinstance(x,Mapping):return {k:plain(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)):return [plain(v) for v in x]
        if hasattr(x,'tolist'):return plain(x.tolist())
        if x is None or isinstance(x,(str,int,float,bool)):return x
        raise TypeError('Unsupported tokenization artifact value: '+type(x).__name__)
    data=plain(value)
    if isinstance(data,dict):
        if 'input_ids' not in data:raise ValueError('Tokenizer output has no input_ids')
        ids=data['input_ids']
    else:ids=data
    if isinstance(ids,list) and ids and isinstance(ids[0],list):
        if len(ids)!=1:raise ValueError('Expected a single conversation tokenization')
        ids=ids[0]
    if not isinstance(ids,list) or not ids or any(type(t) is not int or t<0 for t in ids):
        raise ValueError('Expected nonempty integer token IDs')
    return dict(token_ids=ids,tokenization=data,tokenizer_return_type=type(value).__name__)

PROFILES = {
    'qwen': dict(family='qwen', hub='Qwen/Qwen3-32B', alias='qwen3-32b-release-native',
        revision='9216db5781bf21249d130ec9da846c4624c16137', interface='UNMODIFIED_CACHED_QWEN_TEMPLATE_HERMES'),
    'gemma': dict(family='gemma', hub='google/gemma-3-27b-it', alias='gemma3-27b-it-tag-adapted',
        revision='005ad3404e59d6023443cb575daa05336842228a', interface='EXPLICIT_GEMMA_TAG_TEMPLATE_AND_STRICT_NONSTREAM_PARSER'),
}

def template_path(family):
    return Path(__file__).parent/'templates/gemma3_tools_adapted.jinja' if family=='gemma' else None

def command(python,snapshot,family):
    p=PROFILES[family]
    result=[str(python),'-m','vllm.entrypoints.openai.api_server','--model',str(snapshot),'--tokenizer',str(snapshot),
        '--served-model-name',p['alias'],'--host','127.0.0.1','--port','18080','--tensor-parallel-size','1',
        '--dtype','bfloat16','--gpu-memory-utilization','0.90','--max-model-len','32768','--max-num-seqs','4',
        '--generation-config','vllm','--override-generation-config','{"max_new_tokens":8192}',
        '--seed','20261025','--enable-auto-tool-choice','--tool-call-parser','hermes' if family=='qwen' else 'reference_gemma_strict_tags']
    if template_path(family):result+=['--chat-template',str(template_path(family)),'--tool-parser-plugin',str(Path(__file__).parent/'gemma_parser_plugin.py')]
    return result

def qualify_rendering(snapshot,family,directory):
    """Invoked with serving Python on CPU, before either server starts."""
    import json,hashlib
    from transformers import AutoTokenizer
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    tokenizer=AutoTokenizer.from_pretrained(snapshot,local_files_only=True)
    if family=='gemma':
        # Import and instantiate the exact plugin on CPU with the real cached
        # tokenizer. A token-dependent parser must not fail hours into the run.
        from .gemma_parser_plugin import ReferenceGemmaParser
        parser=ReferenceGemmaParser(tokenizer)
        from types import SimpleNamespace
        test=parser.extract_tool_calls('<tool_call>{"name":"qualification_echo","arguments":{"marker":"ARG"}}</tool_call>',SimpleNamespace())
        if not test.tools_called or len(test.tool_calls)!=1:raise RuntimeError('Installed parser API failed CPU extraction')
    custom=template_path(family)
    template=custom.read_text() if custom else tokenizer.chat_template
    if not isinstance(template,str):raise RuntimeError('Ambiguous effective template')
    tools=[dict(type='function',function=dict(name='qualification_echo',description='Return a supplied marker.',
        parameters=dict(type='object',properties=dict(marker=dict(type='string')),required=['marker'])))]
    fixtures=[
        ('actor', [dict(role='system',content='SYSTEM_SENTINEL'),dict(role='user',content='USER_SENTINEL')],tools),
        ('reference_history', [dict(role='system',content=[dict(type='text',text='SYSTEM_SENTINEL')]),
          dict(role='user',content=[dict(type='text',text='USER_SENTINEL')]),
          dict(role='assistant',content=None,tool_calls=[dict(id='call_probe_a',type='function',function=dict(name='qualification_echo',arguments='{"marker":"ARG_SENTINEL"}')),
          dict(id='call_probe_b',type='function',function=dict(name='qualification_echo',arguments='{"marker":"ARG_B_SENTINEL"}'))]),
          dict(role='tool',tool_call_id='call_probe_a',name='qualification_echo',content='TOOL_A_SENTINEL'),
          dict(role='tool',tool_call_id='call_probe_b',name='qualification_echo',content=[dict(type='text',text='TOOL_B_SENTINEL')])],tools),
        ('attenuator',[dict(role='system',content='AUX_SYSTEM_SENTINEL'),dict(role='user',content='AUX_USER_SENTINEL')],[]),
        ('judge',[dict(role='user',content='JUDGE_SENTINEL')],[]),
    ]
    records=[]
    for name,messages,available in fixtures:
        kwargs=dict(chat_template=template,add_generation_prompt=True)
        if available:kwargs['tools']=available
        conversation,content_format=prepare_fixture_messages(tokenizer,template,messages,available)
        rendered=tokenizer.apply_chat_template(conversation,tokenize=False,**kwargs)
        tokens=tokenizer.apply_chat_template(conversation,tokenize=True,**kwargs)
        required=['SYSTEM_SENTINEL','USER_SENTINEL','qualification_echo'] if name=='actor' else ['SYSTEM_SENTINEL','USER_SENTINEL','ARG_SENTINEL','ARG_B_SENTINEL','TOOL_A_SENTINEL','TOOL_B_SENTINEL'] if name=='reference_history' else ['AUX_SYSTEM_SENTINEL','AUX_USER_SENTINEL'] if name=='attenuator' else ['JUDGE_SENTINEL']
        if not all(s in rendered for s in required):raise RuntimeError('Template lost role/history/schema data: '+name)
        row=dict(role_fixture=name,messages=messages,template_messages=conversation,
            vllm_content_format=content_format,tools=available,rendered=rendered,**tokenization_artifact(tokens))
        (directory/(name+'.json')).write_text(json.dumps(row,indent=2)+'\n');records.append(name)
    report=dict(status='PASS',model_inference=0,profile=PROFILES[family],fixtures=records,
        effective_template_sha256=hashlib.sha256(template.encode()).hexdigest(),
        scope='CPU text-only fixtures through installed vLLM content-format resolution/message parsing and HF tokenization/rendering. Fixture-only minimal text configuration, not full live ModelConfig parity. Generation/parser behavior is checked separately on the owned live server.')
    (directory/'effective_template.jinja').write_text(template)
    (directory/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--snapshot',required=True);p.add_argument('--family',required=True,choices=PROFILES);p.add_argument('--out',required=True)
    a=p.parse_args();qualify_rendering(a.snapshot,a.family,a.out)
