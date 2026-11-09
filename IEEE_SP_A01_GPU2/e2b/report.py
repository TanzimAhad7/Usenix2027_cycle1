import csv,itertools
from collections import Counter
from pathlib import Path
from reference_study.common import read,write
from .design import CRITERIA

def maybe(p):return read(p)if p.is_file()else{}

def analyze(out,m):
 out=Path(out);rows=[];logical=[];counts={}
 for family in m['profiles']:
  local=[]
  for item in m['P1']:
   folder=out/family/'P1'/item['id'];r=maybe(folder/'result.json');op=maybe(folder/'operative_decision.json');native=maybe(folder/'native/JUDGE_RELEASE/after_and_effects.json')
   mock=bool(r.get('mock',op.get('mock',False)));primary=bool(type(op.get('allowed'))is bool and(r.get('primary_observed')or op.get('prepared_request_verified')));science=primary and not mock;verdict=op.get('terminal_verdict',{})
   row=dict(profile=family,id=item['id'],input_key=item['input_key'],recorded=bool(r),status=r.get('status','MISSING'),mock=mock,primary_observed=primary,scientific=science,operative_allowed=op.get('allowed')if primary else None,scientific_allowed=op.get('allowed')if science else None,source_path=op.get('source_branch',{}).get('path'),terminal_boolean=verdict.get('boolean'),terminal_interpretable=verdict.get('interpretable',False),bare_json=verdict.get('bare_json',False),finish_reason=op.get('finish_reason'),source_terminal_disagrees=(op.get('allowed')!=verdict.get('boolean'))if primary and verdict.get('interpretable')else None,native_known=bool(native and'assessment'in native),native_violation=native.get('assessment',{}).get('violation'),committed_count=native.get('assessment',{}).get('committed_count'),native_effects=native.get('effects',[]),alias_count=len(item['aliases']))
   rows.append(row);local.append(row)
   for alias in item['aliases']:logical.append(dict(row,**alias,acquisition_id=item['id']))
  counts[family]=dict(scheduled_acquisitions=168,nominal_positions=192,recorded=sum(x['recorded']for x in local),primary_observed=sum(x['primary_observed']for x in local),scientific_observed=sum(x['scientific']for x in local),mock_acquisitions=sum(x['mock']for x in local),native_observed=sum(x['native_known']for x in local),statuses=dict(Counter(x['status']for x in local)))
 metrics=[]
 for family,axis,direction,criterion in itertools.product(m['profiles'],('amount','recipient'),('forward','reverse'),CRITERIA):
  row=dict(profile=family,axis=axis,direction=direction,criterion=criterion)
  for label,policy,candidate in [('F','STRICT','EDIT'),('L','BROADER','EDIT'),('K_strict','STRICT','REF'),('K_broader','BROADER','REF')]:
   selected=[r for r in logical if(r['profile'],r['axis'],r['direction'],r['criterion'],r['policy'],r['candidate'])==(family,axis,direction,criterion,policy,candidate)];assert len(selected)==3
   known=[r for r in selected if r['scientific']];accepted=sum(x['scientific_allowed']is True for x in known);unknown=3-len(known)
   row[label]=dict(scheduled=3,observed=len(known),accepts=accepted,unknown=unknown,proportion=accepted/3 if unknown==0 else None,bounds=[accepted/3,(accepted+unknown)/3],native_observed=sum(r['native_known']and not r['mock']for r in selected),native_violations=sum(r['native_violation']is True and not r['mock']for r in selected),native_unknown=sum(not r['native_known']or r['mock']for r in selected))
  row['D']=row['L']['proportion']-row['F']['proportion']if row['L']['proportion']is not None and row['F']['proportion']is not None else None
  row['D_bounds']=[row['L']['bounds'][0]-row['F']['bounds'][1],row['L']['bounds'][1]-row['F']['bounds'][0]];metrics.append(row)
 lookup={(r['profile'],r['axis'],r['direction'],r['criterion']):r for r in metrics};contrasts=[]
 for family,axis,direction in itertools.product(m['profiles'],('amount','recipient'),('forward','reverse')):
  s=lookup[family,axis,direction,'SOURCE'];a=lookup[family,axis,direction,'ATTENTION'];e=lookup[family,axis,direction,'ARGUMENT_EQUALITY']
  def difference(x,y,label):
   x=x[label];y=y[label];return dict(value=x['proportion']-y['proportion']if x['proportion']is not None and y['proportion']is not None else None,bounds=[x['bounds'][0]-y['bounds'][1],x['bounds'][1]-y['bounds'][0]])
  contrasts.append(dict(profile=family,axis=axis,direction=direction,forbidden_reduction_equality_beyond_attention=difference(a,e,'F'),lawful_alternative_change_equality_minus_attention=difference(e,a,'L'),forbidden_reduction_attention_vs_source=difference(s,a,'F')))
 folder=out/'analysis';folder.mkdir(parents=True,exist_ok=True)
 for name,data in [('unique_acquisitions',rows),('logical_positions',logical),('cell_metrics',metrics),('criterion_contrasts',contrasts)]:write(folder/(name+'.json'),data)
 write(folder/'summary.json',dict(profiles=counts,expected_scientific_acquisitions=336,nominal_positions=384,autonomous_episodes=0,semantic_review='PENDING',scope='Mock is not science. Bare JSON is separate. Aliases are dependent.'))
 fields=['profile','id','status','mock','primary_observed','scientific','operative_allowed','source_path','terminal_boolean','source_terminal_disagrees','bare_json','finish_reason','native_known','committed_count','native_violation','alias_count']
 with(folder/'acquisitions.csv').open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
 lines=['# E2b acquired decisions','', 'Mock contributes zero scientific observations. Counts are unique acquisitions.','', '| Profile | Scheduled | Recorded | Scientific | Mock | Unknown |','|---|---:|---:|---:|---:|---:|']
 for family,c in counts.items():lines.append(f"| {family} | 168 | {c['recorded']} | {c['scientific_observed']} | {c['mock_acquisitions']} | {168-c['scientific_observed']} |")
 lines+=['','cell_metrics.json contains F/L/K/D and unknown bounds. criterion_contrasts.json contains equality benefit beyond attention and lawful-alternative cost.','', 'No autonomous attack rate, population inference, neural mechanism or principal-profile replication follows from these selected component inputs.']
 (folder/'REPORT.md').write_text('\n'.join(lines)+'\n');return counts

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('run',type=Path);a=p.parse_args();analyze(a.run,read(a.run/'FROZEN_MANIFEST.json'))
