"""Finite selected-set summaries, all missingness retained, no causal verdict automation."""
import csv,collections,json
from reference_study.common import read,write

def analyze(out,manifest):
 profiles={};trials=[];cells=[];cost=[]
 for family in ('qwen','gemma'):
  counts=collections.Counter()
  for item in manifest['P1']:
   folder=out/family/'P1'/item['id'];p=folder/'result.json';r=read(p)if p.exists()else{}
   counts['scheduled_blocks']+=1;counts['recorded_blocks']+=bool(r);counts['qualified_blocks']+=bool(r.get('qualified'))
   for view in ('SOURCE','RESTORED','PLACEBO'):
    p=folder/'views'/view/'result.json';v=read(p)if p.exists()else{}
    trials.append(dict(profile=family,id=item['id'],template=item['template'],directive=item['directive'],draw=item['draw'],view=view,status=v.get('status','NOT_RECORDED'),qualified=v.get('qualified',False),reference_unmatched_new=v.get('reference_unmatched_new'),reference_effectful_calls=v.get('reference_effectful_calls'),reference_no_effectful_call=v.get('reference_no_effectful_call')))
    for kind in ('OBSERVED','LAWFUL_CONTROL'):
     for criterion in ('SOURCE','FORCED_SUPPORT','PERMISSION'):
      p=folder/'views'/view/'comparisons'/kind/criterion/'result.json';c=read(p)if p.exists()else{}
      source=c.get('source_decision',{});arms=c.get('native_clone_arms',{})
      cells.append(dict(profile=family,id=item['id'],template=item['template'],directive=item['directive'],draw=item['draw'],view=view,kind=kind,criterion=criterion,status=c.get('status','NOT_RECORDED'),qualified=c.get('qualified',False),allowed=c.get('allowed'),operative_route=source.get('operative_route'),new_forbidden_effects=arms.get('SOURCE_ADMISSION',{}).get('new_unmatched_effect_count'),independent_native_check_pass=all(x['native_effects_agree']and x['strict_oracle_agrees']for x in c.get('independent_native_check',[]))if c.get('independent_native_check') else None))
   for p in folder.rglob('driver_records.json'):
    for a in read(p):
     usage=(a.get('response')or{}).get('usage')or{}
     cost.append(dict(profile=family,id=item['id'],path=str(p.relative_to(out)),index=a['index'],role=a['role'],truncated=a.get('truncated',False),exception=bool(a.get('exception')),source_supported_fallback=a.get('source_supported_logprobs_fallback',False),seconds=(a.get('finished_epoch',0)-a.get('started_epoch',0)),prompt_tokens=usage.get('prompt_tokens'),completion_tokens=usage.get('completion_tokens')))
  profiles[family]=dict(counts)
 summaries=[]
 for key in sorted({(r['profile'],r['directive'],r['view'])for r in trials}):
  rr=[r for r in trials if(r['profile'],r['directive'],r['view'])==key]
  observed=[r for r in rr if r['reference_unmatched_new']is not None]
  summaries.append(dict(profile=key[0],directive=key[1],view=key[2],scheduled=len(rr),recorded=sum(r['status']!='NOT_RECORDED'for r in rr),qualified=sum(r['qualified']for r in rr),known_reference_violations=sum(r['reference_unmatched_new']>0 for r in observed),no_effectful_reference=sum(r['reference_no_effectful_call']is True for r in observed),unknown_reference_outcomes=len(rr)-len(observed)))
 paired=[]
 for family in ('qwen','gemma'):
  lookup={(r['id'],r['view']):r for r in trials if r['profile']==family}
  for item in manifest['P1']:
   a,b,p=(lookup[item['id'],v]for v in ('SOURCE','RESTORED','PLACEBO'))
   paired.append(dict(profile=family,id=item['id'],template=item['template'],directive=item['directive'],draw=item['draw'],source_bad=a['reference_unmatched_new'],restored_bad=b['reference_unmatched_new'],placebo_bad=p['reference_unmatched_new'],all_qualified=all(r['qualified']for r in(a,b,p))))
 write(out/'analysis/census.json',profiles);write(out/'analysis/reference_trials.json',trials);write(out/'analysis/decision_cells.json',cells);write(out/'analysis/request_costs.json',cost);write(out/'analysis/reference_summary.json',summaries);write(out/'analysis/paired_views.json',paired)
 for name,rows in [('reference_trials',trials),('decision_cells',cells),('reference_summary',summaries),('paired_views',paired)]:
  p=out/'analysis'/(name+'.csv');p.parent.mkdir(exist_ok=True)
  with p.open('w',newline='')as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 write(out/'analysis/interpretation_limits.json',dict(autonomous_episodes=0,semantic_fact_loss_review='PENDING',independent_human_review='PENDING',prevalence_inference=False,causal_model_internal_claim=False,
  source_vs_permission_changes_information_and_branch=True,forced_support_vs_permission_equal_information=True,
  restorative_effect_not_proof_of_fact_loss=True,missing_rows_not_safe=True,source_outcome_selected_six_templates=True))
 totals=dict(scheduled_reference_trials=len(trials),recorded_reference_trials=sum(r['status']!='NOT_RECORDED'for r in trials),scheduled_decision_cells=len(cells),recorded_decision_cells=sum(r['status']!='NOT_RECORDED'for r in cells),known_forbidden_clone_cells=sum((r['new_forbidden_effects']or 0)>0 for r in cells),unknown_decision_cells=sum(r['allowed']is None for r in cells),request_records=len(cost),mock=read(out/'status.json').get('mode','').startswith('MOCK'),copied_parent_rows_are_not_new_trials=True)
 write(out/'analysis/totals.json',totals)
 return profiles
