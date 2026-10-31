"""Claim-relevant CPU tests, real source/runtime and mocked model transport."""
import copy,contextlib,io,json,tempfile,unittest,traceback
from pathlib import Path
from types import SimpleNamespace
from .common import PACKAGE,Invalid,ModelFailure,read,write,digest,native_messages
from .protocol import manifest,TWO_ROOT
from .source import verify_source,load_source,source_pause,make_loop,ReplayPolicy
from .origin import authenticate,intervene
from .native import World,effects,observe,trusted_comparator
from .transport import Driver,Mock,reply
from .experiment import fresh_reference,admission

def qualify(directory):
    directory.mkdir(parents=True,exist_ok=False)
    source=verify_source();write(directory/'source_identity.json',source)
    origin=authenticate(directory);core,factory=load_source();blocks=manifest()['blocks']
    class Qualification(unittest.TestCase):
        def setUp(self):
            self.path=directory/'fixtures'/self._testMethodName;self.path.mkdir(parents=True,exist_ok=True)
        def block(self,**kwargs):return next(b for b in blocks if all(b[k]==v for k,v in kwargs.items()))
        def generated(self,repeat=1,**values):
            block=self.block(contract='K1',carrier='HOSTILE',mode='ATTENUATE',repeat=repeat)
            return fresh_reference(origin,block,self.path/'reference',Mock(repeat,**values))
        def test_schedule_and_sharing(self):
            m=manifest();self.assertEqual(len(m['blocks']),32)
            self.assertEqual(sum(len(b['admissions']) for b in m['blocks']),48)
            self.assertEqual(len({i for b in m['blocks'] for i in b['admissions']}),48)
            self.assertEqual(m,manifest())
        def test_owned_cleanup_preserves_foreign_process(self):
            import subprocess,sys
            from . import serving
            try:serving.verify_pid_namespace()
            except RuntimeError as exc:self.skipTest(str(exc))
            server=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'],start_new_session=True)
            other=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'],start_new_session=True)
            try:
                owned={server.pid:serving.proc_start(server.pid)}
                serving.stop_owned(server,owned,self.path/'shutdown.json')
                self.assertIsNotNone(server.poll());self.assertIsNone(other.poll())
                self.assertEqual(read(self.path/'shutdown.json')['remaining_owned_pids'],[])
            finally:
                if server.poll() is None:server.kill();server.wait()
                if other.poll() is None:other.terminate();other.wait()
        def test_authentic_exposure_and_read_replay(self):
            self.assertLess(origin['certificate']['exposure_events'][0],origin['certificate']['proposal_event'])
            self.assertFalse(effects(World(origin['snapshot']).env))
            self.assertEqual(len(origin['pending']),2)
        def test_neutral_and_trusted_interventions(self):
            for block in blocks:
                root,h,cert=intervene(origin,block)
                self.assertEqual(h[-1],origin['history'][-1])
                if block['contract']=='K2':self.assertEqual(root,TWO_ROOT)
                if block['carrier']=='NEUTRAL':
                    tool=h[-2]['content'][0]['content'];self.assertIn('S1-REPLY-284',tool)
                    self.assertNotIn('second copy is required',tool)
        def test_native_independent_commits_and_clones(self):
            w=World(origin['snapshot']);calls=native_messages([origin['history'][-1]])[0]['tool_calls']
            x=w.execute(calls,core);self.assertEqual(len(x['new_effects']),2)
            self.assertTrue(observe(x,1)['violation']);self.assertFalse(observe(x,2)['violation'])
            self.assertFalse(effects(World(origin['snapshot']).env))
        def test_stateful_comparator_and_exhausted_grant(self):
            calls=native_messages([origin['history'][-1]])[0]['tool_calls']
            one=trusted_comparator(origin['snapshot'],calls,1,core);two=trusted_comparator(origin['snapshot'],calls,2,core)
            self.assertEqual(one['accepted'],[0]);self.assertEqual(one['denied'],[1]);self.assertEqual(two['accepted'],[0,1])
            w=World(origin['snapshot']);w.execute(calls[:1],core)
            spent=trusted_comparator(w.snapshot(),calls[:1],1,core);self.assertEqual(spent['accepted'],[])
        def test_exact_single_reference_reused_by_source(self):
            ref=self.generated();self.assertEqual(ref['status'],'RECORDED',ref.get('error'))
            one=admission(origin,ref,'ONE',self.path/'one',Mock())
            excess=admission(origin,ref,'EXCESS',self.path/'excess',Mock())
            self.assertEqual(one['status'],'RECORDED',one.get('error'));self.assertEqual(excess['status'],'RECORDED',excess.get('error'))
            self.assertEqual(one['reference_input_hash'],excess['reference_input_hash'])
            self.assertEqual(one['observation']['new_effects'],1);self.assertEqual(excess['observation']['new_effects'],2)
            self.assertTrue(excess['source_membership_reuse']);self.assertFalse(any(c['judge_invoked'] for c in excess['occurrences']))
        def test_native_full_source_matches_guard_predicate(self):
            ref=self.generated();result=admission(origin,ref,'EXCESS',self.path/'admission',Mock())
            self.assertEqual(result['status'],'RECORDED',result.get('error'))
            from agentdojo.functions_runtime import FunctionCall
            loop=core.AttriGuardExecutionLoop(None,judge_llm=None,survival_mode='fuzzy')
            refs=[FunctionCall(**r) for r in ref['reference']];calls=[FunctionCall(**c) for c in origin['pending']]
            expected=[c.id for c in calls if loop._fuzzy_survive(c,refs,origin['item']['spec']['root'],World(origin['snapshot']).runtime,World(origin['snapshot']).env)]
            self.assertEqual([c['id'] for c in result['released']],expected)
        def test_empty_reference_denies_without_judge(self):
            ref=self.generated(repeat=4);result=admission(origin,ref,'EXCESS',self.path/'admission',Mock(4))
            self.assertEqual(result['status'],'RECORDED',result.get('error'))
            self.assertFalse(result['released']);self.assertFalse(result['observation']['violation'])
            self.assertFalse(any(c['judge_invoked'] for c in result['occurrences']))
        def test_absent_function_source_denial(self):
            class Other(Mock):
                def __call__(self,role,body):
                    if role=='reference':return reply('',[dict(id='mock-read',type='function',function=dict(name='read_inbox',arguments='{"user":"Operator"}'))],finish='tool_calls')
                    return super().__call__(role,body)
            b=self.block(contract='K1',carrier='HOSTILE',mode='ATTENUATE',repeat=1)
            ref=fresh_reference(origin,b,self.path/'ref',Other());r=admission(origin,ref,'EXCESS',self.path/'a',Other())
            self.assertEqual(r['status'],'RECORDED',r.get('error'));self.assertTrue(all(c['route']=='ABSENT_FUNCTION' for c in r['occurrences']))
        def test_fuzzy_judge_and_parser_trace(self):
            ref=self.generated(repeat=3);result=admission(origin,ref,'EXCESS',self.path/'admission',Mock(3))
            self.assertEqual(result['status'],'RECORDED',result.get('error'))
            self.assertTrue(all(c['route']=='FUZZY' and c['judge_invoked'] for c in result['occurrences']))
            self.assertTrue(result['observation']['violation'])
        def test_fuzzy_false_verdict_denies(self):
            class Deny(Mock):
                def __call__(self,role,body):
                    if role=='judge':return reply('{"survive": false, "reason": "mock denied"}')
                    return super().__call__(role,body)
            b=self.block(contract='K1',carrier='HOSTILE',mode='ATTENUATE',repeat=3)
            ref=fresh_reference(origin,b,self.path/'ref',Deny(3));r=admission(origin,ref,'EXCESS',self.path/'a',Deny(3))
            self.assertEqual(r['status'],'RECORDED',r.get('error'));self.assertFalse(r['released'])
            self.assertTrue(all(c['judge_invoked'] and not c['survived'] for c in r['occurrences']))
        def test_source_logprobs_fallback_is_preserved(self):
            from .transport import httpx
            class Fallback(Mock):
                def __call__(self,role,body):
                    if role=='judge' and body.get('logprobs'):
                        return httpx.Response(400,json={'error':{'message':'logprobs unsupported','type':'invalid_request_error','code':'unsupported'}})
                    return super().__call__(role,body)
            b=self.block(contract='K1',carrier='HOSTILE',mode='ATTENUATE',repeat=3)
            ref=fresh_reference(origin,b,self.path/'ref',Fallback(3));r=admission(origin,ref,'EXCESS',self.path/'a',Fallback(3))
            self.assertEqual(r['status'],'RECORDED',r.get('error'));records=read(self.path/'a/model_io/driver_records.json')
            self.assertEqual(len(records),4);self.assertEqual(sum(x.get('source_supported_logprobs_fallback',False) for x in records),2)
            self.assertTrue(all(c['judge_invoked'] for c in r['occurrences']))
        def test_no_attenuation_in_unchanged_branch(self):
            b=self.block(contract='K1',carrier='HOSTILE',mode='UNCHANGED',repeat=1)
            ref=fresh_reference(origin,b,self.path/'ref',Mock())
            self.assertEqual(ref['status'],'RECORDED',ref.get('error'));self.assertEqual(ref['attenuation_policy'],[])
            self.assertTrue(all(t['input']==t['output'] for t in ref['transforms']))
            self.assertFalse(ref['reference_policy'][0]['input']['messages'][-1].get('tool_calls'))
        def test_legal_two_send_contract_is_preserved(self):
            b=self.block(contract='K2',carrier='NEUTRAL',mode='ATTENUATE',repeat=2)
            ref=fresh_reference(origin,b,self.path/'ref',Mock(2));r=admission(origin,ref,'TWO',self.path/'a',Mock(2))
            self.assertEqual(r['status'],'RECORDED',r.get('error'));self.assertTrue(r['observation']['physical_goal']);self.assertFalse(r['observation']['violation'])
            self.assertEqual(ref['reference_policy'][0]['input']['query'],TWO_ROOT)
        def test_replay_refuses_changed_request(self):
            ref=self.generated();policy=ReplayPolicy(ref['reference_policy'],'reference')
            w=World(origin['snapshot']);inp=ref['reference_policy'][0]['input']
            with self.assertRaises(Invalid):policy.query('Different task',w.runtime,w.env,native_messages(inp['messages']),{})
        def test_transport_failure_has_one_attempt_no_retry(self):
            ref=self.generated(failure=True)
            self.assertEqual(ref['status'],'TECHNICAL_FAILURE')
            rows=read(self.path/'reference/model_io/driver_records.json');self.assertEqual(len(rows),1)
            requests=list((self.path/'reference/model_io/http').glob('*.request.json'));self.assertEqual(len(requests),1)
        def test_truncation_retained_and_not_qualified(self):
            ref=self.generated(truncated=True);self.assertEqual(ref['status'],'RECORDED_UNQUALIFIED_TRUNCATED')
            result=admission(origin,ref,'EXCESS',self.path/'admission',Mock())
            self.assertEqual(result['status'],'RECORDED_UNQUALIFIED_TRUNCATED');self.assertIn('observation',result)
        def test_candidate_excluded_from_reference_and_wire_parity(self):
            ref=self.generated();self.assertEqual(ref['status'],'RECORDED',ref.get('error'))
            req=next(r for r in read(self.path/'reference/model_io/driver_records.json') if r['role']=='reference')
            requests=[read(p) for p in (self.path/'reference/model_io/http').glob('*.request.json')]
            wire=next(r for r in requests if r['role']=='reference')
            self.assertEqual(req['request'],wire['body']);self.assertEqual(wire['body']['temperature'],0)
            self.assertNotIn('max_tokens',wire['body']);self.assertNotIn('seed',wire['body'])
            self.assertFalse(any(c['id'] in json.dumps(wire['body']) for c in origin['pending']))
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Qualification)
    with (directory/'qualification.log').open('w') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
        result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    report=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests_run=result.testsRun,
        failures=len(result.failures),errors=len(result.errors),model_inference=0,scope='Real source/runtime; scripted HTTP responses, no GPU',
        skipped=[dict(test=str(t),reason=reason) for t,reason in result.skipped],
        details=[dict(test=str(test),traceback=text) for test,text in result.failures+result.errors])
    write(directory/'qualification.json',report);return report,origin
