import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from reference_study.common import ROOT, activate, read, digest, sha
activate('qwen')
from reference_discovery_parallel.base.source import load_source
from a01.design import manifest, inputs, permitted, CONTRACTS
from a01.cases import run
from a01.checker import variant, prompt_for
from a01.simulation import World, dispatch
from e2b.terminal import inspect as terminal

class ProtocolTests(unittest.TestCase):
    def test_schedule_and_physical_policy_flip(self):
        self.assertEqual(len(manifest('A0','qwen')['jobs'])*2,72)
        self.assertEqual(len(manifest('A1','qwen')['jobs'])*2,192)
        jobs=manifest('A1','qwen')['jobs']
        self.assertEqual(len({j['id'] for j in jobs}),96)
        self.assertEqual(len({j['input_key'] for j in jobs}),32)
        self.assertEqual(sum(permitted(j) for j in jobs),48)
        for strict in [j for j in jobs if j['policy']=='STRICT']:
            broad=next(j for j in jobs if all(j[k]==strict[k] for k in ('structure','field','criterion','draw')) and j['policy']=='BROADER')
            t,c,r,a=inputs(strict);tb,cb,rb,ab=inputs(broad)
            self.assertEqual((c,r),(cb,rb))
            self.assertNotIn(c,a);self.assertIn(c,ab)
            self.assertTrue(all(type(v) is int for v in c['args'].values()))

    def test_vendor_source_identity(self):
        core,_=load_source()
        self.assertEqual(sha(core.__file__),'6d28e2208efbd521bf3f2e90c553e57b11c786e65564eababacb8cdf4f8050d8')
        identity=read(ROOT/'retained/reference_discovery_parallel/base/vendor/SOURCE_IDENTITY.json')
        for name,value in identity['files'].items():
            self.assertEqual(sha(ROOT/'retained/reference_discovery_parallel/base/vendor'/name),value)

    def test_installed_native_runtime_identity(self):
        import agentdojo.task_suite.load_suites
        from reference_discovery_parallel.base.source import verify_source
        self.assertEqual(len(verify_source()['runtime']),8)

    def test_source_criterion_unchanged_and_variants_declared(self):
        core,_=load_source()
        with tempfile.TemporaryDirectory() as tmp:
            for criterion in ('SOURCE','ATTENTION','OWNER_PRIORITY','DIRECT'):
                folder=Path(tmp)/criterion;folder.mkdir()
                changed=variant(core,folder,criterion)
                self.assertTrue(read(folder/'checker_identity.json')['parser_ast_equal'])
                if criterion=='SOURCE':
                    self.assertEqual(Path(changed.__file__).read_bytes(),Path(core.__file__).read_bytes())
                    self.assertEqual(changed.FUZZY_SYSTEM_PROMPT,core.FUZZY_SYSTEM_PROMPT)
                if criterion=='OWNER_PRIORITY':
                    self.assertNotIn('BENIGN by definition',changed.FUZZY_SYSTEM_PROMPT)
                    self.assertNotIn('Shadow Match (Top Priority)',changed.FUZZY_SYSTEM_PROMPT)

    def test_effectful_clones_and_single_use_budget(self):
        core,_=load_source()
        from agentdojo.functions_runtime import FunctionCall
        from e2b.measure import assess
        with tempfile.TemporaryDirectory() as tmp:
            for structure,contract in CONTRACTS.items():
                w=World();before=w.snapshot()
                candidate=dict(function=contract['function'],args={f:12 for f in contract['fields']})
                denied=dispatch(core,w,candidate,[],False,Path(tmp)/structure/'deny')
                committed=dispatch(core,w,candidate,[],True,Path(tmp)/structure/'commit')
                self.assertEqual(denied['assessment']['committed_count'],0)
                self.assertEqual(committed['assessment']['committed_count'],1)
                self.assertTrue(committed['assessment']['violation'])
                self.assertEqual(w.snapshot(),before)
                core._execute_calls([FunctionCall(**copy.deepcopy(candidate)),FunctionCall(**copy.deepcopy(candidate))],w.runtime,w.env)
                self.assertTrue(assess(w.effects(),[candidate])['violation'])

    def test_all_source_constructed_logical_inputs(self):
        # Real source constructors/SDK serializer and actual effect dispatcher;
        # mock transport cannot create scientific findings.
        with tempfile.TemporaryDirectory() as tmp:
            for stage in ('A0','A1'):
                seen=set()
                for job in manifest(stage,'qwen')['jobs']:
                    if job['input_key'] in seen:continue
                    seen.add(job['input_key'])
                    folder=Path(tmp)/(stage+job['input_key'])
                    r=run(job,folder,'qwen',True)
                    self.assertTrue(r['technical_complete'])
                    self.assertEqual(r['allowed'],permitted(job))
                    self.assertEqual(r['judge_requests'],1)
                    self.assertFalse(r['effects']['JUDGE_RELEASE']['assessment']['violation'])
                    body=read(folder/'model_io/driver_records.json')[0]['request']
                    self.assertEqual(body,read(folder/'model_io/http/0000.request.json')['body'])
                    self.assertEqual(body['temperature'],0.2)
                    self.assertEqual(body['top_p'],0.9)
                    if job['criterion']=='DIRECT':
                        self.assertNotIn('shadow_actions',json.dumps(body['messages']))

    def test_frozen_payload_rejects_before_http(self):
        job=manifest('A1','qwen')['jobs'][0]
        from a01.cases import world_for_item
        frozen=dict(state_hash=digest(world_for_item(job).snapshot()),body={'wrong':'body'})
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/'case'
            with self.assertRaises(Exception):run(job,folder,'qwen',True,frozen)
            self.assertEqual(read(folder/'model_io/transport_summary.json')['http_attempts'],0)

    def test_source_fallback_and_logprob_override_retained(self):
        core,_=load_source()
        from agentdojo.functions_runtime import FunctionCall
        from agentdojo.types import text_content_block_from_string
        class Policy:
            def __init__(self,raw,extra):self.raw=raw;self.extra=extra
            def query(self,q,r,e,m,x):
                return q,r,e,[dict(role='assistant',content=[text_content_block_from_string(self.raw)])],self.extra
        call=FunctionCall(function='place_order',args=dict(item_id=12,quantity=19))
        ref=FunctionCall(function='place_order',args=dict(item_id=12,quantity=12))
        w=World()
        raw='```json\n{"survive":false,"reason":"the word true occurs in a denial"}\n```'
        loop=core.AttriGuardExecutionLoop(None,judge_llm=Policy(raw,{}),survival_mode='fuzzy')
        self.assertTrue(loop._fuzzy_survive(call,[ref],'task',w.runtime,w.env))
        self.assertFalse(terminal(raw)['boolean'])
        lp=dict(logprobs=dict(content=[dict(token='true',logprob=-2.,top_logprobs=[dict(token='true',logprob=-3.),dict(token='false',logprob=-.1)])]))
        loop=core.AttriGuardExecutionLoop(None,judge_llm=Policy('{"survive":true,"reason":"test"}',lp),survival_mode='fuzzy')
        self.assertFalse(loop._fuzzy_survive(call,[ref],'task',w.runtime,w.env))

    def test_missingness_and_mock_not_scientific(self):
        from a01.report import analyze
        from reference_study.common import write
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);write(out/'status.json',dict(mock=True))
            m={f:manifest('A1',f) for f in ('qwen','gemma')}
            summary=analyze(out,m)
            self.assertEqual(summary['qwen']['statuses']['NOT_EXECUTED'],96)
            self.assertTrue(read(out/'analysis/summary.json')['engineering_mock'])
            self.assertEqual(sum(c['missing'] for c in read(out/'analysis/cells.json')['cells']),192)

    def test_failed_attempt_retained_and_redraw_refused(self):
        from a01.worker import run_job
        job=manifest('A1','qwen')['jobs'][0]
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/'attempt'
            with patch('a01.cases.run',side_effect=RuntimeError('injected technical failure')):
                result=run_job(job,folder,'qwen',True)
            self.assertEqual(result['status'],'TECHNICAL_ERROR')
            self.assertFalse(result['technical_complete'])
            self.assertEqual(read(folder/'item.json'),job)
            with self.assertRaises(RuntimeError):run_job(job,folder,'qwen',True)

    def test_package_drift_rejected(self):
        from reference_study.common import write,verify_package
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'source.py').write_text('original')
            write(root/'PACKAGE_MANIFEST.json',dict(files={'source.py':sha(root/'source.py')}))
            with patch('reference_study.common.ROOT',root):
                verify_package()
                (root/'source.py').write_text('changed')
                with self.assertRaises(RuntimeError):verify_package()

if __name__=='__main__':unittest.main()
