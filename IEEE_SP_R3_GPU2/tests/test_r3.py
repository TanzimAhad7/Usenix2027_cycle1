"""CPU/native-runtime and canned-wire regressions. Zero model inference."""
import copy,importlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import httpx
from r3.common import ROOT,read,write,digest,source_sig
from r3.design import manifest,SETTINGS
from r3.context import Context
from r3.world import World
from r3.episode import execute
from r3.llm import WireTransport

class CannedServer:
    def __init__(self,job,branch=False):
        self.job=job;self.actor_index=0;self.branch=branch;self.wires=0
    def respond(self,transport,request):
        self.wires+=1;body=json.loads(request.content)
        role=transport.driver.ctx.invocation_role if transport.role=='actor_reference' else transport.role
        spec=self.job['spec'];bad=spec['attack_targets']['PARAMETER'];good=spec['obligations'][0]
        def text(op):return '<function='+op['function']+'>'+json.dumps(op['args'])+'</function>'
        if role=='judge':content='{"survive": false, "reason": "different authorized operation"}'
        elif role=='attenuator':content='Designated operation data: '+json.dumps(spec['choice_contract'])
        elif role=='reference':content=text(good)
        else:
            seq=[bad,None] if self.branch else [spec['read_call'],bad,bad,None]
            action=seq[min(self.actor_index,len(seq)-1)];self.actor_index+=1;content='Finished.' if action is None else text(action)
        return httpx.Response(200,json=dict(id='canned',object='chat.completion',created=0,model='qwen3_32b_local',choices=[dict(index=0,message=dict(role='assistant',content=content),finish_reason='stop')],usage=dict(prompt_tokens=10,completion_tokens=5,total_tokens=15)))
    def install(self):
        server=self
        def init(transport,driver,role):transport.driver=driver;transport.role=role;transport.inner=httpx.MockTransport(lambda r:server.respond(transport,r))
        return patch.object(WireTransport,'__init__',init)

class Tests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.out=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def job(self,setting='A',task='BANK'):
        return copy.deepcopy(next(j for j in manifest()['jobs'] if j['setting']==setting and j['task']==task and j['carrier']=='PARAMETER' and j['context']==0))
    def test_allocation_and_immutable_facts(self):
        m=manifest();self.assertEqual(len(m['jobs']),32);self.assertEqual(len(m['branches']),32)
        for task in ['BANK','EMAIL']:
            a=read(ROOT/'fixtures'/f'{task}_PARAMETER.json');b=read(ROOT/'fixtures'/f'{task}_NEUTRAL.json')
            self.assertEqual(a['root'],b['root']);self.assertEqual(a['choice_contract'],b['choice_contract'])
            self.assertEqual(a['obligations'],b['obligations'])
            for x,y in zip(a['notices'],b['notices']):
                strip=lambda s:s.split('BEGIN_UNTRUSTED_PROCEDURE')[0]+s.split('END_UNTRUSTED_PROCEDURE')[1]
                self.assertEqual(strip(x),strip(y))
    def test_native_denial_retry_factorial(self):
        for task in ['BANK','EMAIL']:
            for setting in SETTINGS:
                with self.subTest(task=task,setting=setting):
                    job=self.job(setting,task);server=CannedServer(job)
                    with server.install():r=execute(job,self.out/(task+setting))
                    self.assertTrue(r['qualified'],r)
                    self.assertEqual(r['new_unauthorized_effects'],1 if setting=='A' else 0)
                    if setting=='A':
                        ev=[json.loads(s) for s in (self.out/(task+setting)/'events.jsonl').read_text().splitlines()]
                        self.assertTrue(any(e['kind']=='commit' and e['route']=='SOURCE_SKIP_EMPTY' for e in ev))
    def test_checkpoint_resume_all_four_settings(self):
        job=self.job();parent=self.out/'parent'
        with CannedServer(job).install():r=execute(job,parent)
        self.assertTrue(r['eligible_checkpoint']);cp=read(parent/'checkpoint.json')
        self.assertEqual(cp['monitor']['iteration'],1);self.assertEqual(cp['prefix_effect_count'],0)
        for setting in SETTINGS:
            child=dict(id='child'+setting,kind='BRANCH',parent=job['id'],setting=setting,limits=job['limits'])
            with CannedServer(job,branch=True).install():r=execute(child,self.out/setting,parent)
            self.assertTrue(r['qualified'],r);self.assertEqual(r['frozen_model_queries'],2)
            self.assertEqual(r['new_unauthorized_effects'],1 if setting=='A' else 0)
    def test_mismatched_frozen_reply_fails_closed(self):
        job=self.job();parent=self.out/'parent'
        with CannedServer(job).install():execute(job,parent)
        cp=read(parent/'checkpoint.json');cp['frozen_model_replies'][0]['input_sha256']='wrong';cp.pop('checkpoint_digest');cp['checkpoint_digest']=digest(cp);write(parent/'checkpoint.json',cp)
        child=dict(id='mismatch',kind='BRANCH',parent=job['id'],setting='A',limits=job['limits'])
        with CannedServer(job,branch=True).install():r=execute(child,self.out/'bad',parent)
        self.assertFalse(r['qualified']);self.assertEqual(r['error']['type'],'ReplayMismatch');self.assertEqual(r['partial_effects'],[])
    def test_native_checkpoint_roundtrip_after_email_send(self):
        job=self.job(task='EMAIL');ctx=Context(job,self.out);world=World(job['spec'],ctx)
        action=job['spec']['obligations'][0];world.runtime.run_function(world.env,action['function'],action['args']);snap=world.snapshot()
        restored=World(job['spec'],Context(job,self.out/'restored'),snap)
        self.assertEqual(digest(snap),digest(restored.snapshot()));self.assertEqual(len(restored.effects()),1)
    def test_contract_one_two_and_native_duplicate_effects(self):
        job=self.job('C');ctx=Context(job,self.out);w=World(job['spec'],ctx);a=job['spec']['obligations'][0]
        self.assertTrue(w.permitted(a['function'],a['args']));w.runtime.run_function(w.env,a['function'],a['args']);self.assertFalse(w.permitted(a['function'],a['args']))
        self.assertIsNotNone(w.runtime.run_function(w.env,a['function'],a['args'])[1]);self.assertEqual(len(w.effects()),1)
        # An explicit second use authorizes another durable effect; it is not intrinsic duplicate detection.
        w.spec['choice_contract']['slots'].append(copy.deepcopy(w.spec['choice_contract']['slots'][0]))
        self.assertTrue(w.permitted(a['function'],a['args']));w.runtime.run_function(w.env,a['function'],a['args']);self.assertEqual(len(w.effects()),2)
    def test_exact_agreement_after_consumed_grant(self):
        for setting in SETTINGS:
            job=self.job(setting);job['spec']['attack_targets']['PARAMETER']=copy.deepcopy(job['spec']['obligations'][0])
            # Canned actor now repeats the individually lawful first-slot call.
            with CannedServer(job).install():r=execute(job,self.out/('exact'+setting))
            self.assertTrue(r['qualified'],r)
            self.assertEqual(r['new_unauthorized_effects'],1 if setting in ('A','B') else 0)
            events=[json.loads(s) for s in (self.out/('exact'+setting)/'events.jsonl').read_text().splitlines()]
            if setting in ('A','B'):self.assertEqual([e['route'] for e in events if e['kind']=='commit'],['EXACT','EXACT'])

    def test_original_arm_wire_and_native_state_match_uninstrumented_source(self):
        import types
        import r3.guard as guard_module
        job=self.job();real_module_for=guard_module.module_for
        outputs=[]
        for original in [False,True]:
            server=CannedServer(job);responses=[]
            spec=job['spec'];fn=lambda op:'<function='+op['function']+'>'+json.dumps(op['args'])+'</function>'
            texts=[fn(spec['read_call']),'Designated data.','Designated data.',fn(spec['attack_targets']['PARAMETER']),fn(spec['obligations'][0]),'{"survive": false}',fn(spec['attack_targets']['PARAMETER']),'Finished.']
            def respond(transport,request):
                content=texts[len(responses)];responses.append(json.loads(request.content))
                return httpx.Response(200,json=dict(id='canned',object='chat.completion',created=0,model='qwen3_32b_local',choices=[dict(index=0,message=dict(role='assistant',content=content),finish_reason='stop')],usage=dict(prompt_tokens=10,completion_tokens=5,total_tokens=15)))
            server.respond=respond
            def original_loader(ctx):
                mod=types.ModuleType('r3_original_guard');source=(ROOT/'vendor/AttriGuard.py').read_text();exec(compile(source,'original_guard','exec'),mod.__dict__)
                return mod,source,{'original_uninstrumented_differential_control':True}
            with server.install(),patch.object(guard_module,'module_for',original_loader if original else real_module_for):r=execute(job,self.out/('differential'+str(original)))
            self.assertTrue(r['qualified'],r);outputs.append((responses,r['effects']))
        self.assertEqual(outputs[0],outputs[1])

    def test_attenuation_marker_loss_is_recorded_not_excluded(self):
        from r3.qualification import live
        job=self.job();server=CannedServer(job)
        def respond(transport,request):
            role=transport.driver.ctx.invocation_role if transport.role=='actor_reference' else transport.role
            if role=='attenuator':text='No marker retained.'
            elif role=='judge':text='{"survive": false}'
            else:
                text='<function=get_iban>{}</function>' if server.actor_index==0 else 'DE0000000000';server.actor_index+=1
            return httpx.Response(200,json=dict(id='canned',object='chat.completion',created=0,model='qwen3_32b_local',choices=[dict(index=0,message=dict(role='assistant',content=text),finish_reason='stop')],usage=dict(prompt_tokens=10,completion_tokens=5,total_tokens=15)))
        server.respond=respond
        with server.install():receipt=live(self.out/'qual')
        self.assertEqual(receipt['status'],'PASS');self.assertFalse(receipt['attenuation_marker_retained'])

    def test_contract_gate_uses_native_argument_coercion(self):
        job=self.job('C');w=World(job['spec'],Context(job,self.out));a=copy.deepcopy(job['spec']['obligations'][0]);a['args']['amount']='12'
        self.assertTrue(w.permitted(a['function'],a['args']))
        value,error=w.runtime.run_function(w.env,a['function'],a['args']);self.assertIsNone(error);self.assertEqual(w.effects()[0]['args']['amount'],12.0)

    def test_transport_error_not_scientific_safety(self):
        job=self.job();server=CannedServer(job)
        server.respond=lambda *args:httpx.Response(200,json=dict(choices=[dict(index=0,message=dict(role='assistant',content='unfinished'),finish_reason='length')]))
        with server.install():r=execute(job,self.out/'truncated')
        self.assertFalse(r['qualified']);self.assertEqual(r['error']['type'],'IncompleteResponse')

if __name__=='__main__':unittest.main()
