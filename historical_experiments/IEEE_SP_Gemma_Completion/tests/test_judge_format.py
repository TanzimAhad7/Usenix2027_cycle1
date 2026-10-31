import ast
import copy
import json
import logging
import tempfile
import types
import unittest
from pathlib import Path

from permission_admission.judge_format import inspect, require_probe, annotate, audit
from permission_admission.util import ROOT, read, write


def record(raw, finish='stop'):
    return dict(index=1, role='judge', response=dict(choices=[dict(
        message=dict(content=raw), finish_reason=finish)]))


class JudgeFormat(unittest.TestCase):
    def test_exact_failed_probe_is_interpretable_but_not_bare_json(self):
        raw=(ROOT/'fixtures/observed_gemma_fenced_judge.txt').read_text()
        d=require_probe(record(raw))
        self.assertEqual(d['envelope'],'SINGLE_JSON_CODE_FENCE')
        self.assertFalse(d['whole_response_json_boolean'])
        self.assertTrue(d['reported_survive'])
        self.assertEqual(d['raw'],raw)

    def test_both_boolean_answers_permitted(self):
        for value in (True,False):
            for wrapper in ('{}','```json\n{}\n```','```\n{}\n```'):
                raw=wrapper.format(json.dumps(dict(survive=value)))
                self.assertIs(require_probe(record(raw))['reported_survive'],value)

    def test_refuses_ambiguous_or_malformed_or_nonboolean(self):
        for raw in ['yes', '{}', '{"survive":"false"}', '{"survive":0}',
                    '{"survive":true,"survive":false}', '{"survive":false,"x":NaN}',
                    '{"survive":false,"x":1e999}',
                    'Before\n```json\n{"survive":false}\n```',
                    '```json\n{"survive":false}\n```\nAfter',
                    '```json\n{"survive":false}\n```\n```json\n{"survive":true}\n```',
                    '```json\n{"survive":false}',
                    '<think>reason</think>{"survive":false}']:
            with self.subTest(raw=raw),self.assertRaises(RuntimeError): require_probe(record(raw))

    def test_truncation_or_tool_calls_finish_cannot_pass(self):
        for finish in ('length','tool_calls',None,'content_filter'):
            with self.subTest(finish=finish),self.assertRaises(RuntimeError):
                require_probe(record('{"survive":true}',finish))

    def test_diagnostics_never_requalify_or_change_a_source_decision(self):
        r=dict(qualified=False,allowed=True,source_decisions=[dict(allowed=True)],status='COMPLETE')
        before=copy.deepcopy(r)
        records=[record('```json\n{"survive":false,"reason":"true appears here"}\n```')]
        originals=copy.deepcopy(records)
        annotate(r,records)
        for key in before:self.assertEqual(r[key],before[key])
        self.assertEqual(records,originals)
        d=r['judge_format_diagnostics'][0]
        self.assertFalse(d['reported_survive'])
        self.assertTrue(d['source_fallback_prediction'])

    def test_exact_unmodified_source_method_retains_its_fallback(self):
        # Execute the archived method's AST, without modifying its body. Only
        # external model/runtime inputs are scripted; no dependency or GPU.
        source=ROOT/'retained/reference_discovery_parallel/base/vendor/AttriGuard.py'
        tree=ast.parse(source.read_text())
        method=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='_fuzzy_survive')
        future=ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0)
        module=ast.fix_missing_locations(ast.Module(body=[future,method],type_ignores=[]))
        env=dict(json=json,logging=logging,
                 _call_signature=lambda c:(c.function,json.dumps(c.args,sort_keys=True)),
                 UNIFIED_INPUT_TEMPLATE='{{INPUT_TEXT}}',FUZZY_SYSTEM_PROMPT='scripted runtime input',
                 text_content_block_from_string=lambda text:dict(type='text',text=text),
                 _content_to_str=lambda text:text)
        exec(compile(module,str(source),'exec'),env)
        candidate=types.SimpleNamespace(function='f',args={'x':1})
        reference=types.SimpleNamespace(function='f',args={'x':2})
        for verdict,reason,expected in [(False,'true in reason',True),(False,'denied',False),(True,'allowed',True)]:
            raw='```json\n'+json.dumps(dict(survive=verdict,reason=reason))+'\n```'
            judge=types.SimpleNamespace(query=lambda *a,**kw:('',None,None,[dict(role='assistant',content=raw)],{}))
            self_obj=types.SimpleNamespace(judge_llm=judge,debug=False)
            actual=env['_fuzzy_survive'](self_obj,candidate,[reference],'task',None,None)
            self.assertIs(actual,expected)
            self.assertIs(require_probe(record(raw))['reported_survive'],verdict)

    def test_additional_report_preserves_raw_and_strict_endpoints(self):
        manifest=dict(profiles=['gemma'],E1=[dict(id='X_FORBID_Y',permission='FORBID'),
            dict(id='X_ALLOW_Y',permission='ALLOW')],E2=[],E3_blocks=[])
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)
            for ident,allow,explicit in [('X_FORBID_Y',True,False),('X_ALLOW_Y',True,True)]:
                r=dict(id=ident,allowed=allow,qualified=False,source_path_complete=True)
                annotate(r,[record('```json\n'+json.dumps(dict(survive=explicit))+'\n```')])
                write(out/'gemma/E1'/ident/'result.json',r)
            originals={p:p.read_bytes() for p in out.rglob('result.json')}
            summary=audit(out,manifest)
            self.assertEqual(summary['panels']['gemma_E1']['original_qualified'],0)
            self.assertEqual(summary['panels']['gemma_E1']['source_path_or_workflow_complete'],2)
            pair=read(out/'analysis/RAW_SOURCE_AND_REPORTED_PERMISSION_CONTRASTS.json')[0]
            self.assertEqual(pair['raw_source_permission_response'],0)
            self.assertEqual(pair['reported_permission_response_diagnostic'],1)
            self.assertFalse(pair['both_original_qualified'])
            for p,data in originals.items():self.assertEqual(p.read_bytes(),data)
