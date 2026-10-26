import copy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from ..common import digest
from ..protocol import protocol,item,r_conditions
from ..session import StudySession
from ..engine import identified_capacity
from agentdojo.functions_runtime import FunctionCall
from ..runner import r_parent,run_r,run_live,run_j,reconstructed_retry,fixed_route,run_p,run_historical
from ..contracts import public_policy,permit
from ..replay import Tape
from ..sequence import execute_model,atomic_archive,check_disk
from ..analyze import analyze
from .fixtures import FixtureClient

class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.args=SimpleNamespace(model='CPU_FIXTURE',base_url='',max_requests=64,generation_seed=20261019,root=Path(__file__).resolve().parents[2])
    def tearDown(self):self.tmp.cleanup()
    def test_counts_and_pairing(self):
        p=protocol();self.assertEqual(len(p['rollouts']),182)
        self.assertEqual(sum(r['panel']=='R' for r in p['rollouts']),64)
        self.assertEqual(len(p['J']),24);self.assertEqual(len(p['C_fixed']),4)
        for n in (11,19):
            clean=item('qwen',f'C-CLEAN-{n}','C')['spec'];hostile=item('qwen',f'C-HOSTILE-{n}','C')['spec']
            self.assertEqual(clean['root_request'],hostile['root_request']);self.assertEqual(clean['recipient'],hostile['recipient'])
        self.assertEqual(protocol(),p)
    def test_low_disk_blocks_inference_and_records_evidence(self):
        from unittest.mock import patch
        from collections import namedtuple
        usage=namedtuple('usage','total used free')(1000,999,1)
        with patch('authorization_study.sequence.shutil.disk_usage',return_value=usage):
            with self.assertRaisesRegex(RuntimeError,'Insufficient free disk'):
                check_disk(self.root,self.root/'disk.json',128)
        self.assertEqual(json.loads((self.root/'disk.json').read_text())['free'],1)
    def test_actual_policy_selection_and_frozen_request_replay(self):
        parent=r_parent(self.args,'qwen',10,self.root/'parent',FixtureClient)
        rows=[r for r in protocol()['rollouts'] if r['model_family']=='qwen' and r['panel']=='R' and r['spec']['max_total']==10 and r['settings']['initial_selector']=='POLICY']
        released=[]
        for row in rows:
            d=self.root/row['id'];result=run_r(self.args,row,d,parent,FixtureClient)
            self.assertIsNone(result['error']);released.append(len(json.loads((d/'initial_selection.json').read_text())['selected']))
        self.assertEqual(released,[2,1])
    def test_unidentified_compatibility_is_not_coerced_to_safe(self):
        row=item('qwen','A-P10','A');s=StudySession(self.args,row,self.root/'s',client_factory=FixtureClient)
        a=[FunctionCall(function='pay',args={'recipient':s.spec['recipient'],'amount':10,'key':''},id='actor')]
        refs=[FunctionCall(function='pay',args={'recipient':s.spec['recipient'],'amount':n,'key':''},id=str(n)) for n in (4,6)]
        graph=identified_capacity(s.module,a,refs,[dict(survived=True)])
        self.assertEqual(graph['status'],'UNKNOWN_UNIDENTIFIED_COMPATIBILITY');self.assertIsNone(graph['assignment'])
    def test_every_R_factorial_branch_completes_under_fixture(self):
        parent=r_parent(self.args,'gemma',17,self.root/'parent',FixtureClient)
        for row in protocol()['rollouts']:
            if row['model_family']=='gemma' and row['panel']=='R' and row['spec']['max_total']==17:
                result=run_r(self.args,row,self.root/row['id'],parent,FixtureClient)
                self.assertIsNone(result['error'],(row['id'],result['error']))
                self.assertEqual(result['fresh_model_generations'],0)
    def test_truthful_feedback_does_not_claim_unconsumed_full_grant(self):
        parent=r_parent(self.args,'qwen',10,self.root/'parent',FixtureClient)
        row=next(r for r in protocol()['rollouts'] if r['model_family']=='qwen' and r['panel']=='R' and r['spec']['max_total']==10 and r['settings']['initial_selector']=='FIRST' and r['settings']['truthful'])
        d=self.root/'branch';run_r(self.args,row,d,parent,FixtureClient)
        events=[json.loads(x) for x in (d/'events.jsonl').read_text().splitlines()]
        text=next(e['receipt']['error'] for e in events if e['event']=='block_feedback')
        self.assertIn('consume',text);self.assertIn('payment-1',text);self.assertNotIn("grant is unchanged",text)
        self.assertNotIn('remaining_total',text)
    def test_J_exact_fast_path_cannot_be_fixed_by_judge_card(self):
        for n in (3,4,6):
            r=run_j(self.args,dict(model_family='qwen',fixture=n,judge_card=True),self.root/str(n),FixtureClient)
            self.assertEqual(r['requests'],0)
            self.assertTrue(all(d['survived'] for d in r['decisions']))
        self.assertTrue(r['actor_truth']['outcome']['violation'])
    def test_role_cards_do_not_mutate_other_role_history(self):
        row=item('qwen','A-P10','A',dict(cards=True,v_actor=True,v_reference=False))
        s=StudySession(self.args,row,self.root/'s',client_factory=FixtureClient)
        original=copy.deepcopy(s.messages);a=s.generation_messages('actor',s.messages);b=s.generation_messages('reference',s.messages)
        self.assertEqual(s.messages,original);self.assertIn('remaining_total',json.dumps(a));self.assertNotIn('remaining_total',json.dumps(b))
    def test_replay_drift_fails_without_live_fallback(self):
        row=item('qwen','A-P10','A');s=StudySession(self.args,row,self.root/'s',client_factory=FixtureClient)
        tape=Tape(s,[dict(role='actor',request={'x':1},response={},source='fixture')])
        with self.assertRaisesRegex(ValueError,'drift'):tape.request({'x':2},'actor')
    def test_historical_first_batch_replay_with_actual_alias(self):
        for row in protocol()['rollouts']:
            if not row['panel'].endswith('HISTORY'):continue
            args=SimpleNamespace(**(vars(self.args)|{'model':'qwen3-32b' if row['model_family']=='qwen' else 'gemma3-27b-it'}))
            result=run_historical(args,row,self.root/row['id'],args.root,FixtureClient)
            self.assertIsNone(result['error'],(row['id'],result['error']))
    def test_recipient_policy_whole_message_and_registered_retry(self):
        row=item('qwen','A-E-CLEAN','A');s=StudySession(self.args,row,self.root/'email',client_factory=FixtureClient)
        s.world.queue=['first'];s.runtime.run_function(s.env,'send_email',dict(recipients=['alice@example.com'],subject=s.spec['subject'],body=s.spec['body']))
        self.assertFalse(permit(public_policy(s.spec),s.world.snapshot(),'send_email',dict(recipients=s.spec['recipients'],subject=s.spec['subject'],body=s.spec['body']))[0])
        p=item('qwen','A-RETRY','A');t=StudySession(self.args,p,self.root/'pay',client_factory=FixtureClient)
        args=dict(recipient=t.spec['recipient'],amount=9,key=t.spec['registered_key']);t.world.queue=['prior'];t.runtime.run_function(t.env,'pay',args)
        self.assertTrue(permit(public_policy(t.spec),t.world.snapshot(),'pay',args)[0])
        self.assertFalse(permit(public_policy(t.spec),t.world.snapshot(),'pay',args|{'key':''})[0])
    def test_complete_mock_schedule_and_archive(self):
        # All prospective 182 slots and J/P origins are attempted. Historical
        # response tapes intentionally reject CPU model alias substitution;
        # this test checks census retention, not historical reproduction.
        from ..common import write
        out=self.root/'campaign';out.mkdir();p=protocol();write(out/'frozen_protocol.json',dict(protocol=p))
        statuses={};progress=lambda ident,state:statuses.update({ident:state})
        for f in ('qwen','gemma'):execute_model(self.args,f,out,p,progress,FixtureClient)
        self.assertEqual(len([r for r in p['rollouts'] if statuses.get(r['id']) in ('RECORDED','RECORDED_WITH_ERROR','TECHNICAL_FAILURE','UNAVAILABLE_PARENT')]),182)
        for row in p['rollouts']:
            status=json.loads((out/row['model_family']/'rollouts'/row['id']/'slot_status.json').read_text())
            self.assertNotEqual(status['status'],'RUNNING')
            if row['panel'] in ('F','C','R','A'):
                if status['status']=='RECORDED_WITH_ERROR':
                    self.assertEqual((status.get('error') or {}).get('type'),'ReceiptIdentityFailure',(row['id'],status))
                    self.assertEqual(row['panel'],'F')
                    self.assertEqual(row['settings']['feedback'],'original')
                else:self.assertEqual(status['status'],'RECORDED',(row['id'],status))
        summary=analyze(out);self.assertEqual(summary['observer_mismatches'],0)
        self.assertEqual(analyze(out),summary)
        archive=atomic_archive(out);self.assertTrue(archive.is_file());self.assertFalse(Path(str(archive)+'.partial').exists())
    def test_monotonic_proposal_snapshots_include_unreviewed_calls(self):
        row=item('qwen','F-A-HOSTILE','F')
        run_live(self.args,row,self.root/'run',FixtureClient)
        paths=sorted((self.root/'run').glob('proposal_*_before.json'))
        indices=[json.loads(p.read_text())['proposal_index'] for p in paths]
        self.assertEqual(indices,list(range(len(paths))))
        self.assertTrue(any(not json.loads(p.read_text())['has_tool_observation'] for p in paths))

if __name__=='__main__':unittest.main()
