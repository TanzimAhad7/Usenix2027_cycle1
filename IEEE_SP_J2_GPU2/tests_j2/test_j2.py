"""Scientific boundary tests with the retained SDK/source and mock transport."""
import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from reference_study.common import activate,read,write

class J2Boundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        activate('qwen')
        import agentdojo.task_suite.load_suites
        from j2.design import manifest
        cls.plan=manifest('qwen')

    def item(self,**conditions):
        return copy.deepcopy(next(r for r in self.plan['jobs']if all(r.get(k)==v for k,v in conditions.items())))

    def test_missing_values_are_executable_but_unauthorized(self):
        from j2.cases import run
        for category in ('MISSING_FIRST','MISSING_SECOND','MISSING_BOTH'):
            item=self.item(candidate_class=category)
            with tempfile.TemporaryDirectory()as tmp,patch.dict(os.environ,{'J2_MOCK_RULE':'ALLOW_ALL'}):
                r=run(item,Path(tmp)/'case','qwen',True)
                self.assertTrue(r['allowed']);self.assertFalse(r['candidate_permitted'])
                self.assertEqual(r['effects']['JUDGE_RELEASE']['assessment']['committed_count'],1)
                self.assertTrue(r['effects']['JUDGE_RELEASE']['assessment']['violation'])
                self.assertFalse(r['natural_source_route']['native_allowed'])
                self.assertEqual(r['natural_source_route']['native_judge_calls'],0)

    def test_independent_field_mock_has_the_frozen_distinguishing_vector(self):
        from j2.cases import run
        items=[r for r in self.plan['jobs']if r['grant']=='A'and r['block']==0]
        allowed=[]
        with tempfile.TemporaryDirectory()as tmp,patch.dict(os.environ,{'J2_MOCK_RULE':'INDEPENDENT_FIELDS'}):
            for item in items:
                r=run(item,Path(tmp)/item['id'],'qwen',True);allowed.append(r['allowed'])
                self.assertEqual(r['allowed'],item['predictions']['INDEPENDENT_FIELDS'])
        self.assertEqual(sum(allowed),5)

    def test_actual_body_mismatch_is_blocked_before_http(self):
        from j2.worker import run_job
        item=self.item();item['request_body']['temperature']=0.314159
        with tempfile.TemporaryDirectory()as tmp:
            folder=Path(tmp)/'case';r=run_job(item,folder,'qwen',True)
            self.assertEqual(r['status'],'TECHNICAL_ERROR')
            self.assertEqual(read(folder/'model_io/driver_records.json'),[])
            self.assertEqual(list((folder/'model_io').glob('http/*.request.json')),[])

    def test_parser_disagreement_does_not_erase_the_effect(self):
        from j2.cases import run
        from reference_discovery_parallel.base.transport import reply
        item=self.item(candidate_class='MISSING_BOTH')
        with tempfile.TemporaryDirectory()as tmp:
            r=run(item,Path(tmp)/'case','qwen',True,mock_response=lambda *_:
                reply('<think>The word true appears here.</think>\n{"survive":false,"reason":"deny"}'))
            self.assertTrue(r['allowed']);self.assertFalse(r['terminal_verdict']['boolean'])
            self.assertTrue(r['source_terminal_disagreement'])
            self.assertTrue(r['effects']['JUDGE_RELEASE']['assessment']['violation'])

    def test_only_source_unsupported_logprobs_fallback_adds_an_attempt(self):
        from j2.cases import run
        from reference_discovery_parallel.base.transport import reply,httpx
        def respond(role,body):
            if 'logprobs'in body:return httpx.Response(400,json={'error':{'message':'logprobs unsupported','type':'invalid_request_error','code':'unsupported'}})
            return reply('{"survive":false,"reason":"engineering fallback"}')
        with tempfile.TemporaryDirectory()as tmp:
            r=run(self.item(),Path(tmp)/'case','qwen',True,mock_response=respond)
            self.assertEqual(r['judge_requests'],2)

    def test_unknown_rows_cannot_be_a_finite_rule_match(self):
        from j2.report import analyze
        from j2.design import manifest
        with tempfile.TemporaryDirectory()as tmp:
            p=Path(tmp);write(p/'status.json',{'mock':True})
            analyze(p,{f:manifest(f)for f in('qwen','gemma')})
            c=read(p/'analysis/cells.json')['cells']
            self.assertEqual(sum(x['scheduled']for x in c),64)
            self.assertTrue(all(x['unauthorized_fraction_bounds']==[0,1]for x in c))
            fits=read(p/'analysis/pattern_comparisons.json')['by_profile']
            self.assertTrue(all(r['status']=='COMPATIBLE_WITH_INCOMPLETE_OBSERVATIONS'for f in fits for r in f['rule_fits']))

    def test_pattern_fit_checks_individual_decisions_not_only_totals(self):
        from j2.report import pattern_fit
        rows=[dict(id='a',allowed=True,intervention_validated=True,predictions={'X':False}),
              dict(id='b',allowed=False,intervention_validated=True,predictions={'X':True})]
        fit=pattern_fit(rows,'X')
        self.assertEqual(fit['counterexamples'],2)
        self.assertEqual(fit['status'],'CONTRADICTED_BY_OBSERVED_DECISIONS')

    def test_attempted_directory_is_not_redrawn(self):
        from j2.worker import run_job
        with tempfile.TemporaryDirectory()as tmp:
            folder=Path(tmp)/'case';folder.mkdir()
            with self.assertRaises(RuntimeError):run_job(self.item(),folder,'qwen',True)

    def test_typed_and_operative_rule_fits_are_separate(self):
        from j2.report import pattern_fit
        rows=[dict(id='parser_disagrees',allowed=True,terminal_boolean=False,
            terminal_interpretable=True,intervention_validated=True,predictions={'EXACT_JOINT':False})]
        self.assertEqual(pattern_fit(rows,'EXACT_JOINT')['counterexamples'],1)
        self.assertEqual(pattern_fit(rows,'EXACT_JOINT','terminal_boolean')['counterexamples'],0)

if __name__=='__main__':unittest.main(verbosity=2)
