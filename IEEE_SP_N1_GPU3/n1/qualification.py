"""CPU source/native/intervention checks, not semantic or model-result gates."""
import argparse,copy,unittest
from pathlib import Path
from reference_study.common import ROOT,activate,read,write,digest

def run(out):
 activate('qwen')
 from reference_discovery_parallel.common import unseal,native_messages
 from reference_discovery_parallel.base.source import load_source,verify_source,source_pause
 from permission_admission.runtime import native_world,dispatch_arms,matches_with_source,configure
 from .design import manifest,ORIGINS
 from .cases import prepare,augment,CaptureReference,driver,run as block
 from .measure import check_arms
 from diagnostic.cases import checked_variant
 configure('qwen');core,_=load_source();m=manifest();out.mkdir(parents=True,exist_ok=False);receipts=[]
 class Checks(unittest.TestCase):
  def test_frozen_discovery_schedule(self):
   self.assertEqual(len(m['P1']),36);self.assertEqual(len({x['id']for x in m['P1']}),36)
   self.assertEqual(len(ORIGINS),6);self.assertEqual(len(m['P1'])*2*2,144);self.assertEqual(m['P3_blocks'],[])
  def test_byte_preserved_source_and_native_runtime(self):receipts.append(verify_source())
  def test_every_origin_and_fact_preserving_directive_pair(self):
   for name in ORIGINS.values():
    cp=unseal(read(ROOT/'diagnostic_inputs'/name)['checkpoint']);w=native_world(cp['spec'],cp['world']);self.assertEqual(digest(w.snapshot()),digest(cp['world']))
    present,facts,a=prepare(cp,'PRESENT');neutral,other,b=prepare(cp,'NEUTRAL')
    self.assertEqual(facts,other);self.assertEqual(a['original_outside_hash'],b['submitted_outside_hash']);self.assertEqual(a['index'],b['index'])
    for i in range(len(present)):
     if i!=a['index']:self.assertEqual(present[i],neutral[i])
    self.assertNotEqual(present[a['index']]['content'],neutral[a['index']]['content'])
  def test_corrupted_designated_fact_is_rejected(self):
   cp=unseal(read(ROOT/'diagnostic_inputs'/ORIGINS['BANK_SINGLE_J1'])['checkpoint'])
   cp['spec']['notices'][0]=cp['spec']['notices'][0].replace('DE1111111111','DE9999999999')
   with self.assertRaises(RuntimeError):prepare(cp,'NEUTRAL')
  def test_neutral_filler_contains_no_behavioral_or_permission_instruction(self):
   from .cases import PAD
   self.assertFalse(any(v in PAD.lower()for v in ('must','should','follow','authorize','permission','approval','do not','execute')))
  def test_restoration_placebo_equal_characters_and_tool_only(self):
   cp=unseal(read(ROOT/'diagnostic_inputs'/ORIGINS['BANK_SINGLE_J1'])['checkpoint']);ctx,facts,a=prepare(cp,'PRESENT')
   restored,r=augment(ctx,a['tool_call_id'],facts,'RESTORED');placebo,p=augment(ctx,a['tool_call_id'],facts,'PLACEBO')
   self.assertEqual(r['added_characters'],p['added_characters'])
   self.assertEqual(restored[:a['index']],ctx[:a['index']]);self.assertEqual(restored[a['index']+1:],ctx[a['index']+1:])
  def test_actual_source_attenuation_pause_excludes_pending_assistant(self):
   cp=unseal(read(ROOT/'diagnostic_inputs'/ORIGINS['BANK_SINGLE_J1'])['checkpoint']);world=native_world(cp['spec'],cp['world']);msgs,facts,a=prepare(cp,'NEUTRAL');d=driver(out/'pause/model_io',True)
   try:
    loop=core.AttriGuardExecutionLoop(CaptureReference(),attenuation_llm=d.policies['attenuator'],judge_llm=d.policies['judge'],attenuation_level=2,survival_mode='fuzzy',max_iters=1)
    pause=source_pause(loop,cp['spec']['root'],world,native_messages(msgs),'reference')
    self.assertEqual(len(d.records),2);self.assertEqual(pause['shadow_context'][-1]['role'],'tool');self.assertEqual(world.effects(),[])
    write(out/'semantic_controls.json',dict(status='SOURCE_PAUSE_CONTROL_PASS',facts=facts,pending_excluded=True,model_inference=0,semantic_human_review='PENDING'))
   finally:d.close()
  def test_original_exact_bypass_and_forced_judge_are_distinct(self):
   cp=unseal(read(ROOT/'diagnostic_inputs'/ORIGINS['BANK_SINGLE_J1'])['checkpoint']);world=native_world(cp['spec'],cp['world']);origin=read(ROOT/'diagnostic_inputs'/ORIGINS['BANK_SINGLE_J1']);candidate=origin['selected_effect']['candidate'];pending=native_messages([dict(role='assistant',content=None,tool_calls=[candidate])])[0]['tool_calls'];d=driver(out/'exact/model_io',True)
   try:
    answer=matches_with_source(core,d,cp['spec'],world,pending,pending,cp['spec']['root']);self.assertTrue(answer[0]['allowed']);self.assertEqual(len(d.records),0)
    folder=out/'forced';folder.mkdir();changed=checked_variant(core,folder,'FORCED_SUPPORT');answer=matches_with_source(changed,d,cp['spec'],world,pending,pending,cp['spec']['root']);self.assertFalse(answer[0]['allowed']);self.assertEqual(len(d.records),1)
   finally:d.close()
  def test_native_forbidden_commit_and_independent_observer(self):
   cp=unseal(read(ROOT/'diagnostic_inputs'/ORIGINS['BANK_SINGLE_J1'])['checkpoint']);world=native_world(cp['spec'],cp['world']);op=read(ROOT/'diagnostic_inputs'/ORIGINS['BANK_SINGLE_J1'])['selected_effect']['candidate'];pending=native_messages([dict(role='assistant',content=None,tool_calls=[op])])[0]['tool_calls'];arms=dispatch_arms(core,cp['spec'],world,pending,pending,[True]);check_arms(arms,cp['spec']);self.assertEqual(arms['SOURCE_ADMISSION']['new_unmatched_effect_count'],1)
   altered=copy.deepcopy(arms);altered['SOURCE_ADMISSION']['effects'][0]['args']['amount']=999
   with self.assertRaises(RuntimeError):check_arms(altered,cp['spec'])
   self.assertEqual(world.effects(),[])
  def test_complete_mock_block_exercises_all_views_and_criteria(self):
   item=next(x for x in m['P1']if x['template']=='BANK_SINGLE_J1');r=block(item,out/'full_block','qwen',True)
   self.assertTrue(r['qualified']);self.assertEqual(len(r['views']),3);self.assertTrue(all(len(v['comparisons'])==6 for v in r['views']))
   self.assertEqual(r['autonomous_episodes'],0)
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(Checks);result=unittest.TextTestRunner(verbosity=2).run(suite)
 write(out/'qualification.json',dict(status='PASS'if result.wasSuccessful()else'FAIL',tests_run=result.testsRun,errors=[str(x)for x in result.errors],failures=[str(x)for x in result.failures],model_inference=0,source_runtime_identity=receipts,scope='CPU source/native/intervention tests, not human adjudication or fresh model evidence'))
 return 0 if result.wasSuccessful()else 1

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);a=p.parse_args();raise SystemExit(run(a.out))
