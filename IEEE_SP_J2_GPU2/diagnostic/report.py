from __future__ import annotations
import collections,csv,json
from pathlib import Path
from reference_study.common import read,write,digest

def analyze(out,m):
    out=Path(out);rows=[];comparisons=[];integrity=[]
    for profile in ('qwen_native','gemma27_recorded','gemma12_sensitivity'):
        folder=out/profile
        for item in m['P1']+m['P2']:
            p=folder/item['panel']/item['id']/'result.json'
            if not p.exists():
                rows.append(dict(profile=profile,id=item['id'],panel=item['panel'],status='NOT_EXECUTED',qualified=False));continue
            result=read(p);row=dict(profile=profile,id=item['id'],panel=item['panel'],status=result['status'],qualified=result.get('qualified',False),
                criterion=item.get('criterion'),view=item.get('view'),draw=item.get('draw'),
                candidate_kind=item.get('candidate_kind'),origin=item.get('origin','CONSTRUCTED'),explicit_rule=item.get('explicit_rule'),permitted=item.get('permitted'),
                allowed=result.get('allowed'),candidate_permitted=result.get('candidate_permitted'),
                model_generation_records=result.get('model_generation_records'),elapsed_seconds=result.get('elapsed_seconds'),
                operative_route=result.get('source_decision',{}).get('operative_route'))
            rows.append(row)
        # Compare actual complete request views across opposite-policy controls.
        indexed={}
        for item in m['P2']:
            if item['stage']!='X3_CONSTRUCTED_INFORMATION_CONTROL':continue
            records=folder/'P2'/item['id']/'model_io/driver_records.json'
            if records.exists():
                data=read(records);requests=[x['request']for x in data if x['role']=='judge']
                key=(item['explicit_rule'],item['view'],item['criterion'],item['draw'])
                indexed.setdefault(key,{})[item['permitted']]=requests
        for key,pair in indexed.items():
            if set(pair)=={False,True}:
                # Empty lists mean source exact bypass: no checker request existed.
                same=pair[False]==pair[True];expected=not key[0]and key[1]!='DESIGNATED_FACTS_AND_PREFIX'
                both_have_requests=bool(pair[False])and bool(pair[True])
                integrity.append(dict(profile=profile,explicit_rule=key[0],view=key[1],criterion=key[2],draw=key[3],
                    both_judge_requests_exist=both_have_requests,requests_equal=same,expected_equal=expected if both_have_requests else None,
                    premise_verified=expected and both_have_requests and same,
                    scope='Byte-equal structured generation requests within profile. No inference from absent fields alone; exact bypass has no judge request.'))
    # Per-origin matched local effects, no cross-panel multiplication or pooled ASR.
    for profile in ('qwen_native','gemma27_recorded','gemma12_sensitivity'):
        groups=collections.defaultdict(dict)
        for r in rows:
            if r['profile']==profile and r['panel']=='P2'and r.get('origin')not in(None,'CONSTRUCTED'):
                groups[(r['origin'],r.get('candidate_kind'),r.get('draw'))][(r.get('view'),r.get('criterion'))]=r
        for key,g in groups.items():
            comparisons.append(dict(profile=profile,origin=key[0],candidate_kind=key[1],draw=key[2],cells=[dict(view=v,criterion=c,qualified=r['qualified'],allowed=r.get('allowed'),candidate_permitted=r.get('candidate_permitted'),route=r.get('operative_route'))for(v,c),r in g.items()]))
    counts={p:dict(scheduled=len(m['P1'])+len(m['P2']),recorded=sum(r['status']!='NOT_EXECUTED'for r in rows if r['profile']==p),qualified=sum(bool(r['qualified'])for r in rows if r['profile']==p))for p in ('qwen_native','gemma27_recorded','gemma12_sensitivity')}
    write(out/'analysis/conditional_comparisons.json',comparisons);write(out/'analysis/equal_input_controls.json',integrity)
    write(out/'analysis/summary.json',dict(counts=counts,rows=rows,autonomous_episodes=0,human_semantic_review='PENDING',
        principal_published_profile_reproduction=False,scope='Outcome-selected conditional diagnostics. Do not report these rows as autonomous attack success or independent tasks.'))
    lines=['# Focused diagnostic results','', 'All model comparisons are conditional on held proposals and archived state. Independent human review remains pending. No autonomous workflows were launched.','', '| Profile | Planned | Recorded | Qualified |','|---|---:|---:|---:|']
    for profile,c in counts.items():lines.append(f"| {profile} | {c['scheduled']} | {c['recorded']} | {c['qualified']} |")
    lines+=['','Use conditional_comparisons.json to separate information, criterion and exact-bypass effects. PLACEBO length is character-matched, not token/semantic matched. Information augmentation uses fixture-designated facts/native prefix and is not a practical permission system.','', 'X2 source/native CPU cells are in cpu_qualification/skip. Repaired judge responses were not silently substituted for source decisions. Failed and not-executed rows remain visible.','', 'Optional Gemma12 is a local adapted auxiliary sensitivity; if its cache is absent it is explicitly not executed. This is not principal published-profile reproduction.','', 'No fresh transfer/confirmation claim is available. Write and freeze reviewed new structures, predictions and precision choices before collecting that separate cohort.']
    p=out/'analysis/REPORT.md';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(lines)+'\n');return counts
