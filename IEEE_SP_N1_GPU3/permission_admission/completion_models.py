"""Gemma-only interface amendment. Task/template/source guard are unchanged."""
from pathlib import Path
from .util import ROOT, write, file_hash

ALIAS = 'gemma3-27b-it-strict-json-xml-v2'
PARSER_NAME = 'permission_gemma_strict_json_xml_v2'
PROFILE = dict(family='gemma', hub='google/gemma-3-27b-it', alias=ALIAS,
               revision='005ad3404e59d6023443cb575daa05336842228a',
               interface='EXPLICIT_GEMMA_TAG_TEMPLATE_STRICT_JSON_OR_NAME_OR_TOOL_NAME_ARGUMENTS_JSON_V2',
               qualification_profile='INTERFACE_GATE_BARE_OR_SINGLE_FENCED_JSON_V3_SOURCE_UNMODIFIED')
PROFILES = {'gemma': PROFILE}


def command(python, snapshot, family):
    if family != 'gemma':
        raise RuntimeError('Completion runner cannot launch a Qwen server')
    from reference_discovery_parallel.models import command as original
    result = original(python, snapshot, 'gemma')
    for option, replacement in [('--served-model-name', ALIAS), ('--tool-call-parser', PARSER_NAME),
                                ('--tool-parser-plugin', str(ROOT / 'permission_admission/gemma_parser_plugin.py'))]:
        result[result.index(option) + 1] = replacement
    return result


def qualify_rendering(snapshot, directory):
    """Real serving tokenizer/template plus new plugin, CPU only."""
    import json
    from types import SimpleNamespace
    from transformers import AutoTokenizer
    from reference_discovery_parallel.models import prepare_fixture_messages, tokenization_artifact, template_path
    from .gemma_parser_plugin import PermissionGemmaParser
    from .gemma_syntax import parse
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True)
    parser = PermissionGemmaParser(tokenizer)
    schema = [dict(type='function', function=dict(name='qualification_echo', description='Echo a marker.',
        parameters=dict(type='object', properties=dict(marker=dict(type='string')), required=['marker'])))]
    examples = [(ROOT / 'fixtures/observed_gemma_probe.txt').read_text(),
                (ROOT / 'fixtures/observed_gemma_tool_name_multi.txt').read_text(),
                '<tool_call>{"name":"qualification_echo","arguments":{"marker":"ARG"}}</tool_call>']
    examples.append('\n'.join(examples))
    for index, raw in enumerate(examples):
        expected, _ = parse(raw)
        decoded = parser.extract_tool_calls(raw, SimpleNamespace())
        actual = [{'name': call.function.name, 'arguments': json.loads(call.function.arguments)} for call in decoded.tool_calls]
        if actual != expected:
            raise RuntimeError('Installed plugin altered the parsed call')
        write(directory / f'plugin_fixture_{index}.json', {'raw': raw, 'expected': expected, 'actual': actual})
    template = template_path('gemma').read_text()
    messages = [dict(role='system', content=[dict(type='text', text='SYSTEM_SENTINEL')]),
        dict(role='user', content='USER_SENTINEL'),
        dict(role='assistant', content=None, tool_calls=[dict(id='probe_a', type='function', function=dict(name='qualification_echo',arguments='{"marker":"ARG_SENTINEL"}')),
            dict(id='probe_b', type='function', function=dict(name='qualification_echo',arguments='{"marker":"ARG_B_SENTINEL"}'))]),
        dict(role='tool', tool_call_id='probe_a', name='qualification_echo', content='TOOL_A_SENTINEL'),
        dict(role='tool', tool_call_id='probe_b', name='qualification_echo', content=[dict(type='text',text='TOOL_B_SENTINEL')])]
    fixtures = [('history', messages, schema), ('actor', messages[:2], schema),
                ('judge', [dict(role='system',content='JUDGE_SYSTEM_SENTINEL'),dict(role='user',content='JUDGE_USER_SENTINEL')], []),
                ('attenuator',[dict(role='system',content='AUX_SYSTEM_SENTINEL'),dict(role='user',content='AUX_USER_SENTINEL')], [])]
    for name, rows, tools in fixtures:
        conversation, fmt = prepare_fixture_messages(tokenizer, template, rows, tools)
        options = dict(chat_template=template, add_generation_prompt=True)
        if tools: options['tools'] = tools
        rendered = tokenizer.apply_chat_template(conversation, tokenize=False, **options)
        tokens = tokenizer.apply_chat_template(conversation, tokenize=True, **options)
        required = ['SYSTEM_SENTINEL','USER_SENTINEL'] if name=='actor' else ['SYSTEM_SENTINEL','USER_SENTINEL','ARG_SENTINEL','ARG_B_SENTINEL','TOOL_A_SENTINEL','TOOL_B_SENTINEL'] if name=='history' else ['JUDGE_SYSTEM_SENTINEL','JUDGE_USER_SENTINEL'] if name=='judge' else ['AUX_SYSTEM_SENTINEL','AUX_USER_SENTINEL']
        if not all(value in rendered for value in required):
            raise RuntimeError('Template dropped role/history data: '+name)
        write(directory / (name+'.json'), dict(messages=rows, template_messages=conversation, rendered=rendered,
            content_format=fmt, tools=tools, **tokenization_artifact(tokens)))
    write(directory/'qualification.json', dict(status='PASS', profile=PROFILE, model_inference=0,
        unchanged_template_sha256=file_hash(template_path('gemma')), parser_sha256=file_hash(ROOT/'permission_admission/gemma_parser_plugin.py'),
        scope='Installed serving plugin API, real cached tokenizer and unchanged retained template. Live probes still required.'))


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--snapshot',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();qualify_rendering(a.snapshot,a.out)
