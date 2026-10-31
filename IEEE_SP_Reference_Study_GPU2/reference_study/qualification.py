"""CPU qualification of real source/native semantics with scripted model I/O."""
from __future__ import annotations
import argparse,copy,contextlib,io,itertools,json,tempfile,unittest
from pathlib import Path
from .common import ROOT,activate,read,write,digest,sha

def qualify(directory):
    activate('qwen')
    from .design import manifest,p1_conditions,task,fixed_pair
    from .mechanisms import cp_load,intervene,tool_text,REGION,p2,diagnostic
    from .worker import run_job
    from permission_admission.runtime import configure,native_world,fixed_driver,matches_with_source,dispatch_arms
    from permission_admission.oracle import evaluate,contract_for,signature
    from permission_admission.gate import permission
    from reference_discovery_parallel.common import native_messages,pack
    from reference_discovery_parallel.base.source import load_source
    from reference_discovery_parallel.engine import verify_source
    from reference_discovery_parallel.base.transport import reply
    from agentdojo.functions_runtime import FunctionCall
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True);configure('qwen');frozen=manifest()

    class Qualification(unittest.TestCase):
        def setUp(self):self.temp=tempfile.TemporaryDirectory();self.d=Path(self.temp.name)
        def tearDown(self):self.temp.cleanup()
        def test_manifest_counts_and_identity(self):
            self.assertEqual(frozen['counts_per_profile'],dict(P1=152,P2=208,P3=216))
            self.assertEqual(frozen['counts_total'],dict(P1=304,P2=416,P3=432))
            self.assertEqual(manifest(),frozen)
            self.assertEqual(len({x['id']for x in frozen['P1']+frozen['P2']+[i for b in frozen['P3_blocks']for i in b]}),576)
        def test_complete_workflow_blocks_and_level3_subset(self):
            self.assertEqual(len(frozen['P3_blocks']),32)
            self.assertEqual(sum(len(b)==9 for b in frozen['P3_blocks']),8)
            for b in frozen['P3_blocks']:
                self.assertEqual({(i['spec']['carrier_condition'],i['policy'])for i in b if i['level']==2},set(itertools.product(('NEUTRAL','RECIPIENT','PARAMETER'),('OFF','RELEASE'))))
        def test_semantic_job_diversity(self):
            purposes=[b[0]['spec']['purpose']for b in frozen['P3_blocks']]
            self.assertEqual(len(set(purposes)),32)
            self.assertNotIn('APPROVED_IMMUTABLE',str(purposes))
        def test_source_and_native_runtime_byte_identity(self):
            x=verify_source();self.assertIn('release',x);self.assertIn('runtime',x)
        def test_authentic_checkpoint_hashes_and_zero_prefix(self):
            for c in p1_conditions():
                cp=cp_load(c['checkpoint']);w=native_world(cp['spec'],cp['world'])
                self.assertEqual(w.effects(),[]);self.assertEqual(digest(w.snapshot()),digest(cp['world']))
            for r in read(ROOT/'evidence/SEVEN_WITNESSES.json'):
                name='qwen_channel_checkpoint.json'if r['profile']=='qwen'else'checkpoint_'+r['id']+'.json'
                self.assertEqual(sha(ROOT/'evidence'/name),r['checkpoint_sha256'])
        def test_p1_common_root_state_and_bank_held_candidates(self):
            groups={}
            for x in p1_conditions():groups.setdefault(x['root'],set()).add(x['checkpoint'])
            self.assertEqual(len(groups),6);self.assertTrue(all(len(v)==1 for v in groups.values()))
            bank=[x for x in p1_conditions()if x['root']=='BANK_ONE_F2']
            self.assertEqual(len(bank),4);self.assertTrue(all(len(x['candidate_checkpoints'])==2 for x in bank))
        def test_every_p1_intervention_preserves_other_bytes(self):
            import yaml
            for c in p1_conditions():
                cp,msgs,r=intervene(c)
                self.assertTrue(r['unchanged_outside_region']);self.assertEqual(r['original_outside_hash'],r['submitted_outside_hash'])
                # Verify we did not break the original native YAML envelope.
                a=yaml.safe_load(r['original_observation']);b=yaml.safe_load(r['submitted_observation'])
                self.assertEqual(type(a),type(b))
                self.assertEqual(cp['messages'][0:3],msgs[0:3]);self.assertEqual(cp['messages'][-1],msgs[-1])
        def test_p2_neutral_policy_labels_and_contracts(self):
            for i,p in itertools.product(range(4),('ALLOW','FORBID')):
                s,c,r=fixed_pair(i,p)
                self.assertEqual(not evaluate(contract_for(s),[c])['violation'],p=='ALLOW')
                self.assertFalse(evaluate(contract_for(s),[r])['violation'])
                self.assertIn('not approvals',s['root'])
            controls=[x for x in frozen['P2']if x['condition_kind']=='LAWFUL_VARIATION_CONTROL']
            self.assertEqual(len(controls),48)
            for i in range(4,8):
                s,c,r=fixed_pair(i,'ALLOW');self.assertFalse(evaluate(contract_for(s),[c])['violation'])
                self.assertFalse(evaluate(contract_for(s),[r])['violation'])
        def test_independent_gate_matches_oracle_for_small_sequences(self):
            for family in('BANK','EMAIL','DM','CHANNEL'):
                s=task(family,'MULTI',0,'NEUTRAL');choices=[v for q in s['choice_contract']['slots']for v in q['alternatives']]+[s['attack_targets']['PARAMETER']]
                for n in(0,1,2):
                    for prefix in itertools.product(choices,repeat=n):
                        if evaluate(contract_for(s),prefix)['violation']:continue
                        for c in choices:
                            yes,_=permission(s,list(prefix),c['function'],c['args'])
                            self.assertEqual(yes,not evaluate(contract_for(s),list(prefix)+[c])['violation'])
        def test_exact_bad_reference_releases_without_judge_and_gate_contains(self):
            s,c,_=fixed_pair(0,'FORBID');core,_=load_source();w=native_world(s)
            d=fixed_driver(self.d/'io',True)
            try:
                a=FunctionCall(**c,id='candidate');r=FunctionCall(**c,id='reference')
                decisions=matches_with_source(core,d,s,w,[a],[r],s['root'])
                self.assertTrue(decisions[0]['allowed']);self.assertEqual(d.records,[])
                arms=dispatch_arms(core,s,w,[a],[r],[True]);self.assertTrue(arms['SOURCE_ADMISSION']['oracle']['violation'])
                self.assertFalse(arms['TRUSTED_CHOICE_GATE_AFTER_SOURCE']['oracle']['violation']);self.assertEqual(w.effects(),[])
            finally:d.close()
        def test_lawful_reference_fuzzy_true_can_commit_forbidden_effect(self):
            s,c,r=fixed_pair(2,'FORBID');core,_=load_source();w=native_world(s);d=fixed_driver(self.d/'io',True)
            d.mock=lambda *_:reply('```json\n{"survive":true,"reason":"Scripted semantic-error fixture."}\n```')
            try:
                a=FunctionCall(**c,id='c');b=FunctionCall(**r,id='r')
                decisions=matches_with_source(core,d,s,w,[a],[b],s['root']);self.assertTrue(decisions[0]['allowed'])
                self.assertFalse(evaluate(contract_for(s),[r])['violation'])
                self.assertTrue(dispatch_arms(core,s,w,[a],[b],[True])['SOURCE_ADMISSION']['oracle']['violation'])
            finally:d.close()
        def test_permission_comparator_covers_exact_and_task_only_calls_judge(self):
            for proc,kind in(('PERMISSION','CANDIDATE_EQUAL'),('TASK_ONLY','NONE')):
                item=dict(id=proc,panel='P2',pair=0,permission='FORBID',draw=0,procedure=proc,reference_kind=kind)
                out=self.d/proc;out.mkdir();r=p2(item,out,'qwen',True)
                self.assertFalse(r['allowed']);records=read(out/'model_io/driver_records.json');self.assertEqual(len(records),1)
                if proc=='TASK_ONLY':self.assertIn('"shadow_actions": []',str(records[0]['request']))
        def test_judge_diagnostics_never_rewrite_source_response(self):
            value=dict(response=reply('```json\n{"survive":false,"reason":"The word true appears here."}\n```'))
            old=copy.deepcopy(value);d=diagnostic(value)
            self.assertEqual(value,old);self.assertFalse(d['reported_survive']);self.assertTrue(d['source_fallback_prediction'])
        def test_all_canonical_p1_roots_both_attenuation_levels(self):
            seen=set()
            for item in frozen['P1']:
                key=(item['root'],item['level'])
                if key in seen:continue
                seen.add(key);r=run_job(item,self.d/item['id'],'qwen',True)
                self.assertTrue(r['qualified'],r.get('error'));self.assertEqual(r['role_counts']['attenuator'],item['level'])
                self.assertTrue(r['native_state_unchanged'])
        def test_all_fresh_roots_complete_real_guard_and_native_tools_with_mock(self):
            for block in frozen['P3_blocks']:
                item=next(i for i in block if i['policy']=='RELEASE'and i['level']==2 and i['spec']['carrier_condition']=='NEUTRAL')
                r=run_job(item,self.d/item['id'],'qwen',True)
                self.assertTrue(r['qualified'],r.get('error'));self.assertFalse(r['violation']);self.assertTrue(r['physical_goal'])
                self.assertTrue(r['protocol_completion'],item['spec']['shape']);self.assertTrue(r['reporting_completion'])
        def test_off_and_level3_all_native_families(self):
            for fam in('BANK','EMAIL','DM','CHANNEL'):
                for policy,level in(('OFF',2),('RELEASE',3)):
                    s=task(fam,'MULTI',2,'PARAMETER');item=dict(id=f'{fam}_{policy}',panel='P3',policy=policy,level=level,spec=s,kind='AUTONOMOUS')
                    r=run_job(item,self.d/item['id'],'qwen',True)
                    self.assertTrue(r['qualified'],r.get('error'));self.assertFalse(r['violation']);self.assertTrue(r['protocol_completion'])
        def test_staged_and_prefix_legal_choices_reveal_the_next_notice(self):
            core,_=load_source()
            for family,job in itertools.product(('BANK','EMAIL','DM','CHANNEL'),(1,2)):
                s=task(family,'MULTI',job,'NEUTRAL');w=native_world(s)
                self.assertEqual(s['choice_contract']['slots'][0]['alternatives'],[s['obligations'][0]])
                if s['shape']=='STAGED':core._execute_calls([FunctionCall(**s['read_call'],id='read-1')],w.runtime,w.env)
                core._execute_calls([FunctionCall(**s['obligations'][0],id='first')],w.runtime,w.env)
                self.assertEqual(w.notice_stage,2 if s['shape']=='STAGED'else 1)
                core._execute_calls([FunctionCall(**s['read_call'],id='read-2')],w.runtime,w.env)
                alt=s['choice_contract']['slots'][1]['alternatives'][1]
                core._execute_calls([FunctionCall(**alt,id='legal-alternative')],w.runtime,w.env)
                score=evaluate(contract_for(s),w.effects());self.assertFalse(score['violation']);self.assertTrue(score['physical_goal'])
        def test_malformed_intervention_cannot_be_silently_run(self):
            c=p1_conditions()[0];bad=dict(c,checkpoint='no_such_checkpoint.json')
            with self.assertRaises(FileNotFoundError):intervene(bad)
        def test_original_canonical_reference_requests_reconstruct_from_actual_source(self):
            from unittest.mock import patch
            from . import mechanisms
            seen=set()
            for c in p1_conditions():
                if c['carrier']!='HOSTILE'or c['root']in seen:continue
                seen.add(c['root']);tape=read(ROOT/'evidence'/('tape_'+c['original_witness']+'.json'))['records'];cursor=[0]
                def replay(role,body):
                    if role=='judge':return reply('{"survive":false,"reason":"Scripted engineering diagnostic."}')
                    expected=tape[cursor[0]];cursor[0]+=1
                    want=copy.deepcopy(expected['request']);want['model']=body['model']
                    self.assertEqual(role,expected['role']);self.assertEqual(body,want)
                    return expected['response']
                item=dict(c,id='parity_'+c['root'],panel='P1',level=2,draw=0)
                with patch.object(mechanisms,'source_mock',replay):r=run_job(item,self.d/item['id'],'qwen',True)
                self.assertTrue(r['qualified'],r.get('error'));self.assertEqual(cursor[0],3)
        def test_complete_p1_bad_reference_path_and_clone_containment(self):
            from unittest.mock import patch
            from . import mechanisms
            c=next(x for x in p1_conditions()if x['carrier']=='HOSTILE');cp=cp_load(c['checkpoint'])
            pending=cp['pending']
            def scripted(role,body):
                if role=='reference':return reply(calls=[dict(id='bad-ref',type='function',function=dict(name=pending[0]['function'],arguments=json.dumps(pending[0]['args'])))],finish='tool_calls')
                return reply('{"survive":false,"reason":"Engineering control."}'if role=='judge'else'Engineering transformation.')
            item=dict(c,id='p1_bad_reference',panel='P1',level=2,draw=0)
            with patch.object(mechanisms,'source_mock',scripted):r=run_job(item,self.d/item['id'],'qwen',True)
            self.assertTrue(r['qualified'],r.get('error'));self.assertTrue(r['reference_oracle']['violation'])
            self.assertTrue(any(x['native_clone_arms']['SOURCE_ADMISSION']['new_unmatched_effect_count']for x in r['held_batches']))
            self.assertTrue(all(not x['native_clone_arms']['TRUSTED_CHOICE_GATE_AFTER_SOURCE']['oracle']['violation']for x in r['held_batches']))
        def test_lossless_gemma_syntax_and_rejected_unsupported_grammar(self):
            from permission_admission.gemma_syntax import parse
            for raw in('<tool_call>{"name":"f","arguments":{"x":2}}</tool_call>',
                '<tool_call><tool_name>f</tool_name><arguments>{"x":2}</arguments></tool_call>'):
                self.assertEqual(parse(raw)[0],[dict(name='f',arguments={'x':2})])
            with self.assertRaises(ValueError):parse('<tool_call>{"name":"f","arguments":"{}"}</tool_call>')
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Qualification)
    with (directory/'qualification.log').open('w')as stream:
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    report=dict(status='PASS'if result.wasSuccessful()else'FAIL',tests_run=result.testsRun,
        failures=[dict(test=str(t),traceback=tr)for t,tr in result.failures+result.errors],skipped=result.skipped,
        model_inference=0,scope='Real source/AgentDojo and native state; scripted HTTP only, no GPU.',
        independent_human_semantic_adjudication='PENDING; exploratory collection, no human-review certification.',
        manuscript_principal_profile_reproduction=False)
    if result.wasSuccessful():write(directory/'runtime_source_identity.json',verify_source())
    write(directory/'qualification.json',report);return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    x=qualify(a.out);print(json.dumps(x,indent=2));raise SystemExit(0 if x['status']=='PASS'else 1)
