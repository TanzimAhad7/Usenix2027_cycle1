"""Prospective deterministic discovery schedule; no outcome-based redraws."""
import random,ast
from reference_study.common import ROOT,read,sha
ORIGINS={
 'BANK_SINGLE_J1':'gemma__P3_BANK_SINGLE_J1_RECIPIENT_RELEASE_L2.json',
 'CHANNEL_SINGLE_J4':'gemma__P3_CHANNEL_SINGLE_J4_RECIPIENT_RELEASE_L2.json',
 'EMAIL_SINGLE_J2':'gemma__P3_EMAIL_SINGLE_J2_PARAMETER_RELEASE_L3.json',
 'BANK_MULTI_J2':'gemma__P3_BANK_MULTI_J2_PARAMETER_RELEASE_L2.json',
 'DM_MULTI_J2':'qwen__P3_DM_MULTI_J2_PARAMETER_RELEASE_L2.json',
 'CHANNEL_MULTI_J2':'gemma__P3_CHANNEL_MULTI_J2_RECIPIENT_RELEASE_L2.json'}
VIEWS=('SOURCE','RESTORED','PLACEBO')
CRITERIA=('SOURCE','FORCED_SUPPORT','PERMISSION')

def manifest():
 items=[];eligible=[]
 source=ROOT/'retained/reference_discovery_parallel/base/vendor/AttriGuard.py'
 for node in ast.parse(source.read_text()).body:
  if isinstance(node,ast.AnnAssign)and isinstance(node.target,ast.Name)and node.target.id=='EXTERNAL_OUTPUT_TOOLS':eligible=ast.literal_eval(node.value)
 if not eligible:raise RuntimeError('Source eligible-tool set not found')
 for root,name in ORIGINS.items():
  p=ROOT/'diagnostic_inputs'/name;x=read(p)
  if x['checkpoint']['spec']['id']!=root:raise RuntimeError('Origin/template mismatch')
  observations=sum(1 for msg in x['checkpoint']['messages'] if msg.get('role')=='tool' and (not(msg.get('tool_call')or{}).get('function')or(msg.get('tool_call')or{}).get('function')in eligible) and any(b.get('content',b.get('text','')).strip()for b in msg.get('content',[])if isinstance(b,dict)))
  for directive in ('PRESENT','NEUTRAL'):
   for draw in range(3):
    order=list(VIEWS);random.Random('n1-20261101-'+root+directive+str(draw)).shuffle(order)
    items.append(dict(id=f'N1_{root}_{directive}_D{draw}',panel='P1',origin='diagnostic_inputs/'+name,
       origin_sha256=sha(p),template=root,directive=directive,draw=draw,level=2,view_order=order,eligible_observations=observations))
 random.Random(20261101).shuffle(items)
 return dict(version='N1_20261101_v1',P1=items,P2=[],P3_blocks=[],profiles=['qwen','gemma'],
   primary_reference_trials=144,placebo_reference_trials=72,block_units_per_profile=36,
   downstream_decision_cells=1296,maximum_scientific_model_requests=2*sum(2*x['eligible_observations']+3+18 for x in items),
   request_bound_assumptions='72 source attenuation chains; two calls per source-eligible tool observation,216 reference calls,up to1296 judges; excludes qualification,tokenize diagnostics and source-supported logprob fallbacks. Actual calls recorded; no scientific redraws.',
   attenuation_reuse='SOURCE/RESTORED/PLACEBO share one acquired source attenuation within each template/directive/draw/profile block',
   selection='Six outcome-selected historical templates. CHANNEL_SINGLE_J4 canonical is Gemma L2; duplicate L3 origins excluded from primary schedule.',
   draw_policy='Three new request draws; retained source role decoding and server seed. No paired random-number or population-rate claim.',
   semantic_fact_loss='Not automatically adjudicated; restoration repeats original designated facts, not proof those facts were semantically lost.',
   autonomous_workflows=0,independent_human_review='PENDING')
