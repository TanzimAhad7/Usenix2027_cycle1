"""Recompute descriptive results from complete terminal census and raw state."""
from collections import Counter,defaultdict
import math,csv,json
from .common import read,write,digest
from .protocol import manifest

def wilson(k,n):
    if not n:return None
    z=1.95996398454;p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [max(0,c-h),min(1,c+h)]

def analyze(out):
    from .diagnostics import diagnose
    diagnostic=diagnose(out)
    frozen=manifest();conditionals=[];autonomous=[];missing=[]
    for b in frozen['blocks']:
        for ident in b['admissions']:
            p=out/'admissions'/ident/'result.json'
            if p.is_file():conditionals.append(read(p))
            else:missing.append(ident)
    items={i['id']:i for i in frozen['workflows']}
    for ident,item in items.items():
        p=out/'workflows'/ident/'result.json'
        if p.is_file():autonomous.append(read(p))
        else:missing.append(ident)
    cells=defaultdict(list)
    for r in autonomous:
        s=items[r['id']]['spec'];key=tuple(str(x) for x in [s['panel'],s['family'],s['shape'],s['grant'],s['carrier_condition'],items[r['id']]['policy'],s['fault_profile']]);cells[key].append(r)
    planned=Counter(tuple(str(x) for x in [i['spec']['panel'],i['spec']['family'],i['spec']['shape'],i['spec']['grant'],i['spec']['carrier_condition'],i['policy'],i['spec']['fault_profile']]) for i in frozen['workflows'])
    rows=[]
    for key in sorted(planned):
        values=cells[key]
        q=[r for r in values if r.get('qualified')];viol=sum(r.get('violation',False) for r in q)
        rows.append(dict(zip(['panel','family','shape','grant','carrier','policy','fault_profile'],key))|dict(scheduled=planned[key],recorded=len(values),qualified=len(q),
            violations_observed_all=sum(r.get('violation',False) for r in values),violations_qualified=viol,
            physical_goals=sum(r.get('physical_goal',False) for r in q),
            secure_completions=sum(r.get('outcome')=='SECURE_COMPLETION' for r in q),
            exposed_qualified=sum(r.get('actor_carrier_request_accepted',False) for r in q),
            fault_exposed_qualified=sum(r.get('fault_exposed',False) for r in q),
            violations_with_eventual_exposure=sum(r.get('violation',False) and r.get('actor_carrier_request_accepted',False) for r in q),
            inference='One/two authored realizations; no binomial confidence interval or prevalence estimate. Eventual exposure alone is not causal attribution.'))
    def summary(rs):return dict(recorded=len(rs),qualified=sum(r.get('qualified',False) for r in rs),
        violations_observed=sum(r.get('violation',r.get('observation',{}).get('violation',False)) for r in rs),
        qualified_violations=sum(r.get('qualified',False) and r.get('violation',r.get('observation',{}).get('violation',False)) for r in rs),
        outcomes=dict(Counter(r.get('outcome',r.get('status')) for r in rs)))
    forks=[]
    for item in frozen['forks']:
        p=out/'forks'/item['id']/'result.json'
        if p.exists():forks.append(read(p))
        else:missing.append(item['id'])
    summary_data=dict(schema='REFERENCE_DISCOVERY_ANALYSIS_1',mode=read(out/'status.json')['mode'],conditional=summary(conditionals),autonomous=summary(autonomous),matched_recovery=summary(forks),missing_result_ids=missing,
        census=read(out/'census.json'),frozen_counts=frozen['counts'],allocation_counts=frozen['allocation_counts'],profile=read(out/'execution_environment.json') if (out/'execution_environment.json').exists() else None,
        cells=rows,diagnostic_counts={k:v for k,v in diagnostic.items() if k!='dispatch_replay_disagreements'},inference='Authored exploration, one/two realizations per cell and one model. No prevalence or independent-population inference. Unrun cases are not safe results; matched continuations are not autonomous roots.')
    summary_data['panels']={panel:summary([r for r in autonomous if items[r['id']]['spec']['panel']==panel]) for panel in ['MAIN','RECOVERY']}
    summary_data['matched_recovery']['no_eligible_checkpoint']=sum(r.get('status')=='NO_ELIGIBLE_CHECKPOINT' for r in forks)
    summary_data['matched_recovery']['executed_or_attempted']=sum(r.get('status')!='NO_ELIGIBLE_CHECKPOINT' for r in forks)
    summary_data['matched_recovery']['technical_or_censored']=sum(r.get('status')!='NO_ELIGIBLE_CHECKPOINT' and not r.get('qualified') for r in forks)
    summary_data['matched_input_certificates']=read(out/'matched_input_certificates.json') if (out/'matched_input_certificates.json').exists() else []
    summary_data['conditional']['violations_by_kind']={kind:sum(r.get('observation',{}).get('violation',False) for r in conditionals if r['kind']==kind) for kind in ['ONE','EXCESS','TWO']}
    write(out/'analysis/summary.json',summary_data)
    write(out/'analysis/conditional_ledger.json',conditionals);write(out/'analysis/autonomous_ledger.json',autonomous)
    write(out/'analysis/matched_recovery_ledger.json',forks)
    with (out/'analysis/cells.csv').open('w',newline='') as f:
        if rows:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    lines=['# Reference-discovery campaign','',f"Mode: **{summary_data['mode']}**. Mock data are engineering evidence only.",'',
        'No repeated S1 conditional reproduction is scheduled.',
        f"Autonomous workflows: {len(autonomous)}/344 recorded; {summary_data['autonomous']['qualified']} qualified.",
        f"Conditional recovery slots: {len(forks)}/30 accounted; no eligible checkpoint is not safe completion.",'',
        'Inspect `summary.json`, `cells.csv`, complete ledgers, checkpoints, wire requests, responses and native states before making scientific claims.',
        '', 'Conditional fixed-candidate failures do not count as autonomous exploits. A hostile-carrier violation alone does not identify the carrier as its cause. Compare neutral/OFF controls and inspect the actual effect path.',
        '', 'Capacity is exact-signature and per-proposal only. Fuzzy admissions and later proposals remain possible. The trusted gate has privileged contract/state access. Neither comparator is claimed as a novel defense.',
        '', 'No automatic paper-ready or confirmed-mechanism verdict is generated. All missing, censored, truncated, unexposed and negative slots remain visible.']
    (out/'analysis/FINDINGS.md').write_text('\n'.join(lines)+'\n');return summary_data

def verify_results(out):
    errors=[];census=read(out/'census.json');status=read(out/'status.json');frozen=manifest()
    expected={'references':{b['id'] for b in frozen['blocks']},'admissions':{i for b in frozen['blocks'] for i in b['admissions']},'workflows':{i['id'] for i in frozen['workflows']},'forks':{i['id'] for i in frozen['forks']}}
    for group,ids in expected.items():
        if set(census[group])!=ids:errors.append('Census differs: '+group)
        if any(v in ['SCHEDULED','RUNNING'] for v in census[group].values()):errors.append('Nonterminal census: '+group)
    for p in (out/'workflows').glob('*/result.json') if (out/'workflows').exists() else []:
        r=read(p)
        if r.get('qualified') and not r.get('event_state_agreement'):errors.append('Unqualified observer reported qualified: '+r['id'])
        if r.get('qualified') and (r.get('truncated_requests') or r.get('lifecycle')!='COMPLETE'):errors.append('Truncated/censored qualified: '+r['id'])
    result=dict(status='PASS' if not errors else 'FAIL',errors=errors,scope='Census and measurement integrity; no favorable-outcome requirement')
    diagnostic=read(out/'analysis/diagnostics.json')
    if diagnostic['dispatch_replay_disagreements']:
        result['status']='FAIL';result['errors'].append('Actual native effects differ from same-checkpoint dispatch replay; inspect diagnostics.json')
    write(out/'analysis/verification.json',result);return result
