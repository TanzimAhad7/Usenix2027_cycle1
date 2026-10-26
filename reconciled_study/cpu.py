"""Real-runtime engineering qualification. Zero model inference or GPU access."""
import argparse,copy,io,json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from .util import write,read,ASSETS,digest
from .protocol import protocol,load_parents,live_item
from .execution import Session,MockHTTP,make_session
from .runner import continuation,historical_matrix,autonomous,select_repeat
from .graphs import certificate,choose
from .analysis import effect_check,certify_e3
from .qualification import qualify_profiles

def args():return SimpleNamespace(model='qwen3-32b',base_url='http://127.0.0.1:18080/v1',max_requests=64,generation_seed=20261019,watchdog_seconds=60)

CASE_OUTPUT_ROOT=None

class Tests(unittest.TestCase):
    def setUp(self):
        if CASE_OUTPUT_ROOT is None:self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        else:self.tmp=None;self.root=CASE_OUTPUT_ROOT/self._testMethodName;self.root.mkdir(parents=True,exist_ok=False)
        self.parents=load_parents()
    def tearDown(self):
        if self.tmp is not None:self.tmp.cleanup()
    def test_pinned_runtime_and_assets(self):
        from .legacy_a.engine import verify_runtime
        verify_runtime();self.assertEqual(len(self.parents),8)
    def test_reserved_protocol_and_original_core_ids(self):
        p=protocol();self.assertEqual(len(p['slots']),156);self.assertEqual(sum(s['workflow'] and s['activation']=='MANDATORY' for s in p['slots']),120)
        self.assertEqual(sum(s['activation']!='MANDATORY' for s in p['slots']),12)
    def test_known_full_cover_survives_unknown_cross_edges(self):
        c=certificate([[0],[1]],[(0,1),(1,0)],2);self.assertEqual(c['status'],'IDENTIFIED');self.assertTrue(c['full_actor_cover'])
    def test_partial_ambiguity_is_not_silently_resolved(self):
        c=certificate([[],[0]],[(0,0)],1);self.assertEqual(c['status'],'UNKNOWN_UNIDENTIFIED_ALLOCATION')
    def test_reuse_vs_injective_same_edges(self):
        self.assertEqual(choose([[True],[True]],1,'PAIR_M0')[0],[0,1]);self.assertEqual(choose([[True],[True]],1,'PAIR_M1')[0],[0])
    def _world(self,name='qwen_A-P10_arm0'):
        from .legacy_a.world import World
        p=self.root/(name+'-'+str(len(list(self.root.iterdir()))));p.mkdir();w=World(self.parents[name]['checkpoint']['item']['spec'],p);return w,w.make_runtime()
    def test_omitted_empty_default_future_effect_and_retry_semantics(self):
        results=[]
        for variant in ('omitted','empty'):
            w,rt=self._world('qwen_A-P10_arm0')
            recipient=w.spec['recipient'];kw={'recipient':recipient,'amount':2}
            if variant=='empty':kw['key']=''
            for i,extra in enumerate([kw,kw,dict(recipient=recipient,amount=3,key='registered'),dict(recipient=recipient,amount=3,key='registered')]):
                w.queue=[f'o{i}'];_,err=rt.run_function(w.env,'pay',extra);self.assertIsNone(err)
            results.append(([e['amount'] for e in w.payments],[e['key'] for e in w.payments],w.retries,len(w.keys)))
        self.assertEqual(results[0],results[1]);self.assertEqual(results[0],([2,2,3],['','','registered'],1,1))
    def test_conflicting_registered_retry_rejected(self):
        w,rt=self._world();r=w.spec['recipient'];w.queue=['a'];rt.run_function(w.env,'pay',dict(recipient=r,amount=3,key='k'))
        w.queue=['b'];_,err=rt.run_function(w.env,'pay',dict(recipient=r,amount=4,key='k'));self.assertIsNotNone(err);self.assertEqual(len(w.payments),1)
    def test_lost_ack_consumes_actual_effect(self):
        w,rt=self._world();w.fail_after_commit=True;r=w.spec['recipient'];w.queue=['a'];_,err=rt.run_function(w.env,'pay',dict(recipient=r,amount=4,key='k'))
        self.assertIsNotNone(err);self.assertEqual(sum(e['amount'] for e in w.payments),4)
        w.fail_after_commit=False;w.queue=['b'];rt.run_function(w.env,'pay',dict(recipient=r,amount=4,key='k'));self.assertEqual(len(w.payments),1)
    def test_trusted_ledger_denies_excess_allows_residual_and_retry(self):
        p=self.parents['qwen_A-P10_arm0'];item=copy.deepcopy(p['checkpoint']['item'])
        s=make_session(args(),item,self.root/'gate',config={'trusted_ledger':True},client_factory=MockHTTP)
        r=s.spec['recipient']
        for ident,amount,key,denied in [('a',6,'k',False),('b',6,'',True),('c',4,'',False),('d',6,'k',False)]:
            s.world.queue=[ident];_,err=s.runtime.run_function(s.env,'pay',dict(recipient=r,amount=amount,key=key));self.assertEqual(err is not None,denied)
        self.assertEqual(sum(e['amount'] for e in s.world.payments),10);self.assertEqual(s.world.retries,1)
    def test_service_failure_is_before_second_dispatch_effect(self):
        p=self.parents['qwen_O96_L3'];slot=next(s for s in protocol()['slots'] if s['panel']=='E3' and s['model_family']=='qwen' and s['policy']=='PRE_DISPATCH_SERVICE_FAILURE')
        r=continuation(args(),slot,p,historical_matrix(p,'qwen'),self.root/'service',None,MockHTTP)
        first=read(self.root/'service/batch_000_result.json')['world_after']
        self.assertEqual([e['amount'] for e in first['payments']],[4]);self.assertEqual(r['comparison_validity'],'EXPECTED_FOUR_UNIT_PREFIX_REACHED')
        ev=[json.loads(x) for x in (self.root/'service/events.jsonl').read_text().splitlines()];self.assertTrue(any(e['event']=='service_pre_dispatch_failure' for e in ev))
    def test_live_natural_off_keeps_archived_first_payload(self):
        for family in ('qwen','gemma'):
            s=next(s for s in protocol()['slots'] if s['panel']=='E4a-OFF' and s['model_family']==family and s['task_or_parent']=='A-P10')
            a=args();a.model='qwen3-32b' if family=='qwen' else 'gemma3-27b-it';d=self.root/family
            autonomous(a,s,d,None,MockHTTP);c=read(d/'profile_certificate.json');self.assertEqual(c['status'],'EXACT_FIRST_REQUEST_FIELDS')
    def test_repeat_trigger_ignores_final_outcome(self):
        a={'initial_admission':{'selected_indices':[1]},'outcome':{'status':'SECURE_COMPLETION'}}
        b={'initial_admission':{'selected_indices':[0,1]},'outcome':{'status':'VIOLATION'}}
        r=select_repeat({'SOURCE_M0':a,'DEFAULT_M0':b});self.assertEqual(r['left'],'SOURCE_M0');self.assertEqual(r['right'],'DEFAULT_M0')
        a['outcome'],b['outcome']=b['outcome'],a['outcome'];self.assertEqual(r,select_repeat({'SOURCE_M0':a,'DEFAULT_M0':b}))
    def test_primitive_checker_distinguishes_effects_and_reporting(self):
        w,rt=self._world();r=w.spec['recipient']
        for i,n in enumerate((6,6)):w.queue=[str(i)];rt.run_function(w.env,'pay',dict(recipient=r,amount=n))
        result=effect_check(w.spec,w.snapshot(),'payment-1 payment-2');self.assertTrue(result['violation']);self.assertTrue(result['excess_total']);self.assertTrue(result['reported_ids'])
    def test_native_email_sink_real_commit(self):
        from .legacy_o.world import World
        roots=read(ASSETS/'roots.json');spec=roots['qwen_O96_EMAIL_BEFORE_CLEAN']['item']['spec'];p=self.root/'email';p.mkdir();w=World(spec,p);rt=w.make_runtime();w.queue=['send']
        _,err=rt.run_function(w.env,'send_email',dict(recipients=[spec['recipient']],subject=spec['subject'],body=spec['body']))
        self.assertIsNone(err);self.assertEqual(w.count(),1);self.assertFalse(effect_check(spec,w.snapshot())['violation'])
    def test_authentic_partial_release_then_controlled_overpay_and_gate(self):
        class Overpay(MockHTTP):
            attempted=False
            def request(self,payload,role):
                w=self.session.world;paid=sum(e['amount'] for e in w.payments)
                if role in ('actor','reference') and paid==6:
                    self.count+=1;self.models.append(payload['model']);self.usage.append({'mock':True})
                    if role=='actor' and self.attempted:return dict(content='Fixture stops after denied attempt.',tool_calls=[])
                    if role=='actor':self.attempted=True
                    return dict(content='',tool_calls=[dict(id=f'overpay-{role}-{self.count}',type='function',function=dict(name='pay',arguments=json.dumps(dict(recipient=self.session.spec['recipient'],amount=6))))])
                return super().request(payload,role)
        p=self.parents['qwen_A-P10_arm0'];initial=dict(source_vector=[False,True],default_vector=[True,True],matrix=[[True,False],[False,True]])
        results={}
        for policy,gate in [('SOURCE_M0',False),('DEFAULT_M0',False),('SOURCE_M0',True)]:
            slot=dict(slot_id=f'case-{policy}-{gate}',panel='E2-G' if gate else 'E2',model_family='qwen',policy=policy,seed=20261019,origin='CONTROLLED_CPU_FIXTURE')
            results[(policy,gate)]=continuation(args(),slot,p,initial,self.root/slot['slot_id'],None,Overpay)
        self.assertEqual(sum(e['amount'] for e in results[('SOURCE_M0',False)]['snapshot']['payments']),12)
        self.assertTrue(effect_check(p['checkpoint']['item']['spec'],results[('SOURCE_M0',False)]['snapshot'])['violation'])
        self.assertEqual(sum(e['amount'] for e in results[('DEFAULT_M0',False)]['snapshot']['payments']),10)
        self.assertEqual(sum(e['amount'] for e in results[('SOURCE_M0',True)]['snapshot']['payments']),6)
        self.assertFalse(results[('SOURCE_M0',True)]['scientific_evidence'])
    def test_auxiliary_input_difference_invalidates_e3_certificate(self):
        p=protocol();base=self.root/'qwen'
        slots=[s for s in p['slots'] if s['model_family']=='qwen' and s['panel']=='E3' and s['feedback']=='IDENTICAL_NEUTRAL']
        for i,s in enumerate(slots):
            d=base/'slots'/s['slot_id'];d.mkdir(parents=True)
            write(d/'fork_after_initial.json',dict(world={},messages=[],loop_attributes={},source_frame_flags={},shadow_history=[],pending_ids=[],seen_ids=[]))
            es=[dict(event='feedback_identity'),dict(event='model_request_context',role='actor',native_messages=[],effective_payload={'messages':['same']},route_state={}),
                dict(event='model_request_context',role='attenuator',native_messages=[str(i)],effective_payload={'messages':[str(i)]},route_state={})]
            (d/'events.jsonl').write_text('\n'.join(json.dumps(e) for e in es)+'\n')
        c=next(c for c in certify_e3(base,p) if c['feedback']=='IDENTICAL_NEUTRAL');self.assertEqual(c['status'],'PRE_RESPONSE_INPUT_DIFFERENCE')
    def test_published_logprobs_do_not_change_archival_judge_profile(self):
        class Capture(MockHTTP):
            def request(self,payload,role):self.last_payload=payload;return super().request(payload,role)
        p=self.parents['qwen_A-P10_arm0'];item=copy.deepcopy(p['checkpoint']['item'])
        from .execution import calls
        for enabled in (False,True):
            s=make_session(args(),item,self.root/str(enabled),parent=p,config={'published_logprobs':enabled},client_factory=Capture,pub_closest=True)
            s._judge(calls(p['checkpoint']['pending_calls'])[0],calls(p['batch']['reference']))
            self.assertEqual('logprobs' in s.client.last_payload,enabled)
    def test_cleanup_never_signals_reused_process_identity(self):
        from unittest.mock import patch,Mock
        from . import serving
        server=SimpleNamespace(pid=987654,poll=lambda:0,wait=lambda timeout:0)
        with patch.object(serving,'descendant_pids',return_value={987654}),patch.object(serving,'proc_start',return_value=None),patch.object(serving.os,'killpg') as groupkill,patch.object(serving.os,'kill') as kill:
            serving.stop_owned(server,{987654:'old-start-time'},self.root/'shutdown.json')
            groupkill.assert_not_called();kill.assert_not_called()
    def test_all_four_fixed_full_release_batches_are_lawful(self):
        for name in ('qwen_A-P10_arm0','qwen_A-P17_arm0','qwen_O96_L3','gemma_O96_L3'):
            p=self.parents[name];item=copy.deepcopy(p['checkpoint']['item']);item['id']='legal-'+name
            s=make_session(args(),item,self.root/name,legacy=p['legacy'],parent=p,config={'policy':'RELEASE_LAWFUL_BATCH'},client_factory=MockHTTP)
            for c in p['checkpoint']['pending_calls']:
                s.world.queue=[c['id']];_,err=s.runtime.run_function(s.env,c['function'],c['args']);self.assertIsNone(err)
            self.assertFalse(effect_check(s.spec,s.world.snapshot())['violation'])
    def test_http_capture_and_published_logprob_roundtrip(self):
        from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
        import threading
        from .util import Budgets
        from .execution import calls
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                self.rfile.read(int(self.headers['Content-Length']))
                data={'tokens':[1,2]} if self.path=='/tokenize' else dict(model='qwen3-32b',choices=[dict(message=dict(role='assistant',content='{"survive":true,"reason":"CPU fake endpoint"}'),finish_reason='stop',logprobs={'content':[]})],usage={'prompt_tokens':2,'completion_tokens':3})
                body=json.dumps(data).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            a=args();a.base_url=f'http://127.0.0.1:{server.server_port}/v1';p=self.parents['qwen_A-P10_arm0'];item=copy.deepcopy(p['checkpoint']['item']);d=self.root/'http'
            s=make_session(a,item,d,parent=p,config={'published_logprobs':True},budget=Budgets(self.root/'budget.json'),group='PUB',pub_closest=True)
            self.assertTrue(s._judge(calls(p['checkpoint']['pending_calls'])[0],calls(p['batch']['reference'])))
            self.assertEqual(s.client.fresh_count,1);self.assertEqual(s.client.last_logprobs,{'content':[]})
            self.assertTrue(read(d/'http_001_judge.request.json')['logprobs']);self.assertTrue((d/'http_001_judge.response.json').exists())
        finally:server.shutdown();server.server_close();thread.join(timeout=2)
    def test_server_command_has_one_gpu_loopback_and_pinned_context(self):
        from .sequence import server_command
        c=server_command('/project/.venv-serving/bin/python','/cache/snap','qwen3-32b','/template','qwen')
        self.assertEqual(c[c.index('--tensor-parallel-size')+1],'1');self.assertEqual(c[c.index('--host')+1],'127.0.0.1')
        self.assertEqual(c[c.index('--port')+1],'18080');self.assertEqual(c[c.index('--tool-call-parser')+1],'hermes')
    def test_unidentified_singletons_do_not_erase_independent_source_control(self):
        p=self.parents['qwen_A-P10_arm0'];initial=dict(source_vector=[False,True],default_vector=[True,True],matrix=[[None,None],[None,None]])
        for policy in ('SOURCE_M0','RELEASE_LAWFUL_BATCH','PAIR_M1'):
            slot=dict(slot_id='partial-'+policy,panel='E2',model_family='qwen',policy=policy,seed=20261019,origin='CPU_PARTIAL_EVIDENCE_FIXTURE')
            r=continuation(args(),slot,p,initial,self.root/slot['slot_id'],None,MockHTTP)
            if policy=='PAIR_M1':self.assertEqual(r['error']['type'],'UnidentifiedAllocation')
            else:self.assertIsNone(r['error']);self.assertEqual(sum(e['amount'] for e in r['snapshot']['payments']),10)

def qualify(out):
    global CASE_OUTPUT_ROOT
    out=Path(out);out.mkdir(parents=True,exist_ok=False);CASE_OUTPUT_ROOT=out/'cases'
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests));CASE_OUTPUT_ROOT=None
    (out/'tests.log').write_text(stream.getvalue());print(stream.getvalue(),flush=True)
    status=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),fresh_model_requests=0,scope='Real runtime/primitive/dispatch engineering tests, not scientific model results')
    write(out/'status.json',status)
    if result.wasSuccessful():qualify_profiles(args(),out/'published_profiles')
    return status

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();raise SystemExit(0 if qualify(a.out)['status']=='PASS' else 1)
