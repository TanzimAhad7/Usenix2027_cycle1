import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from permission_admission.gemma_syntax import parse, parse_with_receipt
from permission_admission.util import ROOT, read


class GemmaSyntax(unittest.TestCase):
    def test_actual_gpu2_multiple_probe_tool_name_envelope(self):
        raw=(ROOT/'fixtures/observed_gemma_tool_name_multi.txt').read_text()
        calls,content,formats=parse_with_receipt(raw)
        self.assertEqual(calls,[{'name':'qualification_echo','arguments':{'marker':m}}
                               for m in ('MULTI_A_4721','MULTI_B_4721')])
        self.assertEqual(formats,['TOOL_NAME_ARGUMENTS_JSON_V1']*2)
        self.assertIn('Okay, I will call',content)

    def test_tool_name_requires_exact_matching_envelope_and_strict_json(self):
        for raw in [
            '<tool_call><tool_name>f</name><arguments>{}</arguments></tool_call>',
            '<tool_call><tool_name> f </tool_name><arguments>{}</arguments></tool_call>',
            '<tool_call><tool_name>f</tool_name><arguments>{"x":1,"x":2}</arguments></tool_call>',
            '<tool_call><tool_name>f</tool_name><arguments>"{}"</arguments></tool_call>',
            '<tool_call><tool_name>f</tool_name><arguments>{"x":NaN}</arguments></tool_call>',
            '<tool_call><tool_name>f</tool_name><name>g</name><arguments>{}</arguments></tool_call>']:
            with self.subTest(raw=raw),self.assertRaises(ValueError):parse(raw)
        args={'body':'literal </tool_name> </arguments> </tool_call>', 'flag':False,'n':None}
        raw='<tool_call><tool_name>f</tool_name><arguments>'+json.dumps(args)+'</arguments></tool_call>'
        self.assertEqual(parse(raw)[0],[{'name':'f','arguments':args}])

    def test_actual_failed_probe_is_decoded_without_argument_change(self):
        raw=(ROOT/'fixtures/observed_gemma_probe.txt').read_text()
        calls,content,formats=parse_with_receipt(raw)
        self.assertEqual(calls,[{'name':'qualification_echo','arguments':{'marker':'QUALIFICATION_ARGUMENT_4721'}}])
        self.assertIsNone(content)
        self.assertEqual(formats,['NAME_ARGUMENTS_JSON_V1'])

    def test_original_json_grammar_is_unchanged(self):
        call={'name':'send_email','arguments':{'recipients':['alice@example.com'],'body':'Hello','subject':'Update'}}
        self.assertEqual(parse('<tool_call>'+json.dumps(call)+'</tool_call>')[0],[call])

    def test_multiple_mixed_calls_and_text(self):
        raw='before <tool_call>{"name":"a","arguments":{"n":1}}</tool_call> middle <tool_call><name>b</name><arguments>{"n":2}</arguments></tool_call> after'
        calls,content=parse(raw)
        self.assertEqual(calls,[{'name':'a','arguments':{'n':1}},{'name':'b','arguments':{'n':2}}])
        self.assertEqual(content,'before  middle  after')

    def test_json_delimiter_text_inside_argument_is_data(self):
        args={'body':'Quote <tool_call> and </tool_call> literally.'}
        raw='<tool_call>'+json.dumps({'name':'send_message','arguments':args})+'</tool_call>'
        self.assertEqual(parse(raw)[0][0]['arguments'],args)

    def test_xml_delimiter_text_inside_json_argument_is_data(self):
        args={'body':'Quote </arguments> and </tool_call> literally.'}
        raw='<tool_call><name>send_message</name><arguments>'+json.dumps(args)+'</arguments></tool_call>'
        self.assertEqual(parse(raw)[0][0]['arguments'],args)

    def test_plain_text_and_reasoning_are_not_rewritten(self):
        raw='<think>Keep this text exactly.</think>\n{"survive":false}'
        self.assertEqual(parse(raw),([],raw))

    def test_preserves_argument_types_and_unicode(self):
        args={'integer':1,'float':2.5,'bool':False,'list':['বাংলা'],'null':None,'nested':{'x':'y'}}
        raw='<tool_call><name>f</name><arguments>'+json.dumps(args)+'</arguments></tool_call>'
        self.assertEqual(parse(raw)[0][0]['arguments'],args)

    def test_no_duplicate_keys_or_nonfinite_values(self):
        for body in ['{"name":"a","name":"b","arguments":{}}','{"name":"a","arguments":{"x":1,"x":2}}',
                     '{"name":"a","arguments":{"x":NaN}}','{"name":"a","arguments":{"x":Infinity}}',
                     '{"name":"a","arguments":{"x":1e999}}']:
            with self.subTest(body=body),self.assertRaises(ValueError):parse('<tool_call>'+body+'</tool_call>')

    def test_no_schema_or_argument_inference(self):
        invalid=[
            '<tool_call>{"function":"f","parameters":{}}</tool_call>',
            '<tool_call>{"name":"f","arguments":"{}"}</tool_call>',
            '<tool_call><name>f</name><arguments><x>1</x></arguments></tool_call>',
            '<tool_call><name>f</name><arguments>[]</arguments></tool_call>',
            '<tool_call><name>f</name><arguments>{}</arguments><extra>1</extra></tool_call>',
            '<tool_call><name> f </name><arguments>{}</arguments></tool_call>',
            '<tool_call><name>&entity;</name><arguments>{}</arguments></tool_call>']
        for raw in invalid:
            with self.subTest(raw=raw),self.assertRaises(ValueError):parse(raw)

    def test_unclosed_or_nested_blocks_are_not_silently_dropped(self):
        for raw in ['<tool_call>{"name":"a","arguments":{}}','</tool_call>',
                    '<tool_call ><name>f</name><arguments>{}</arguments></tool_call>',
                    '<tool_call><tool_call>{"name":"a","arguments":{}}</tool_call></tool_call>']:
            with self.subTest(raw=raw),self.assertRaises(ValueError):parse(raw)

    def test_command_cannot_launch_qwen(self):
        from permission_admission.completion_models import command
        with self.assertRaises(RuntimeError):command('/venv/python','/cache','qwen')
        argv=command('/venv/python','/cache','gemma')
        self.assertEqual(argv[argv.index('--tool-call-parser')+1],'permission_gemma_strict_json_xml_v2')
        self.assertEqual(argv[argv.index('--served-model-name')+1],'gemma3-27b-it-strict-json-xml-v2')

    def test_live_profile_refuses_qwen(self):
        from permission_admission.profile import main
        from types import SimpleNamespace
        with self.assertRaises(RuntimeError):main(SimpleNamespace(family='qwen',mock=False))

    def test_real_qwen_reasoning_fixture_remains_non_json(self):
        raw=(ROOT/'fixtures/observed_qwen_false_verdict.txt').read_text()
        with self.assertRaises(ValueError):json.loads(raw)
        self.assertFalse(json.loads(raw.split('</think>',1)[1])['survive'])
        self.assertTrue('true' in raw.lower())

    def test_source_task_manifest_is_unchanged(self):
        from permission_admission.design import manifest
        self.assertEqual(manifest(),read(ROOT/'FROZEN_DESIGN.json'))

    def test_parent_detection_prefers_existing_result_directory(self):
        from permission_admission.parent_evidence import default_parent,PARENT_ID
        with tempfile.TemporaryDirectory() as temp:
            expected=Path(temp)/'results/user_runs'/PARENT_ID;expected.mkdir(parents=True)
            self.assertEqual(default_parent(temp),expected)

    def test_parent_archive_fallback(self):
        from permission_admission.parent_evidence import default_parent,PARENT_ID
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(default_parent(temp),Path(temp)/'results/user_runs'/(PARENT_ID+'.tar.gz'))

    def test_parent_retention_preserves_decisions_and_qualification(self):
        from permission_admission.parent_evidence import retain,PARENT_ID
        manifest={'E1':[{'id':'one'}],'E2':[],'E3_blocks':[]}
        result=dict(id='one',profile='qwen',mock=False,attempted=True,qualified=False,status='COMPLETE',allowed=True,
                    native_clone_arms={'SOURCE_ADMISSION':{'environment':{'synthetic':'engineering fixture'},'effects':[]}})
        blobs={'status.json':json.dumps({'run_id':PARENT_ID,'mode':'MODEL_EXPERIMENT'}).encode(),
            'qwen/status.json':json.dumps({'completed':544}).encode(),
            'gemma/status.json':json.dumps({'completed':0}).encode(),
            'qwen/census.json':json.dumps({'one':'COMPLETE'}).encode(),
            'FROZEN_MANIFEST.json':json.dumps(manifest).encode(),
            'source/PACKAGE_MANIFEST.json':(ROOT/'provenance/EXPECTED_PARENT_SOURCE_MANIFEST.json').read_bytes(),
            'qwen/E1/one/result.json':json.dumps(result).encode()}
        with tempfile.TemporaryDirectory() as temp,patch('permission_admission.parent_evidence.load_selected',return_value=(blobs,None)):
            before=copy.deepcopy(blobs)
            receipt=retain(Path(temp)/'fixture_parent',Path(temp)/'out',manifest)
            kept=read(Path(temp)/'out/qwen/E1/one/result.json')
            self.assertFalse(kept['qualified']);self.assertTrue(kept['allowed'])
            self.assertEqual(kept['status'],'COMPLETE')
            self.assertNotIn('environment',kept['native_clone_arms']['SOURCE_ADMISSION'])
            self.assertEqual(blobs,before)
            self.assertEqual(receipt['qwen_generations_in_completion'],0)

    def test_parent_task_change_fails_before_retention(self):
        from permission_admission.parent_evidence import retain,PARENT_ID
        blobs={'status.json':json.dumps({'run_id':PARENT_ID,'mode':'MODEL_EXPERIMENT'}).encode(),
               'FROZEN_MANIFEST.json':b'{"different":"task"}'}
        with tempfile.TemporaryDirectory() as temp,patch('permission_admission.parent_evidence.load_selected',return_value=(blobs,None)):
            with self.assertRaisesRegex(RuntimeError,'task bytes'):
                retain(Path(temp),Path(temp)/'out',{'E1':[],'E2':[],'E3_blocks':[]})

