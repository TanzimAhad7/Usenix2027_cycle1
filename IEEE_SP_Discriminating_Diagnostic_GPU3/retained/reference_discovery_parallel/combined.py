"""Descriptive, profile-separated results; matched task IDs are not new tasks."""
from collections import Counter
from .common import read,write
from .protocol import manifest
from .models import PROFILES

def finalize(out):
    from .report import analyze,verify_results
    result=dict(schema='DUAL_REFERENCE_ANALYSIS_1',models={},technical_issues=[],
        interpretation='Two model/interface profiles, same authored conditions. No pooling into a prevalence estimate. Conditional origins differ by profile and are not paired independent tasks. Cross-profile differences do not identify a model-weight effect.')
    ledgers={}
    for family in PROFILES:
        local=out/'models'/family
        if not (local/'census.json').exists():
            result['models'][family]=dict(status='NOT_EXECUTED',profile=PROFILES[family]);result['technical_issues'].append(family+': missing worker census');ledgers[family]={};continue
        try:
            summary=analyze(local);check=verify_results(local)
            status=read(local/'status.json')
            incomplete=summary['autonomous']['qualified']!=344 or summary['matched_recovery']['technical_or_censored']>0
            if check['status']!='PASS' or incomplete or status.get('exit_code',0):result['technical_issues'].append(family+': incomplete/technical cases; inspect per-profile records')
            result['models'][family]=dict(profile=PROFILES[family],worker_status=status,summary=summary,verification=check)
            ledgers[family]={r['id']:r for r in read(local/'analysis/autonomous_ledger.json')}
            write(local/'DEFERRED_FINALIZATION.json',dict(status='COMPLETE',parent_analysis=str(out/'analysis'),raw_observations_unchanged=True))
        except Exception as exc:
            import traceback
            result['technical_issues'].append(family+': '+str(exc));result['models'][family]=dict(status='ANALYSIS_FAILED',error=str(exc),traceback=traceback.format_exc());ledgers[family]={}
    comparisons=[]
    for item in manifest()['workflows']:
        row=dict(id=item['id'],condition=dict(family=item['spec']['family'],shape=item['spec']['shape'],grant=item['spec']['grant'],carrier=item['spec']['carrier_condition'],policy=item['policy'],fault=item['spec']['fault_profile']),profiles={})
        for family in PROFILES:
            r=ledgers[family].get(item['id'])
            row['profiles'][family]=dict(recorded=r is not None,qualified=bool(r and r.get('qualified')),outcome=r.get('outcome') if r else None,violation=r.get('violation') if r else None,physical_goal=r.get('physical_goal') if r else None)
        row['both_qualified']=all(r['qualified'] for r in row['profiles'].values())
        row['same_outcome']=len({r['outcome'] for r in row['profiles'].values()})==1 if row['both_qualified'] else None
        comparisons.append(row)
    result['matched_conditions']=dict(scheduled=344,both_qualified=sum(r['both_qualified'] for r in comparisons),outcome_pairs=dict(Counter(str((r['profiles']['qwen']['outcome'],r['profiles']['gemma']['outcome'])) for r in comparisons if r['both_qualified'])))
    audit_path=out/'gpu2_audit/status.json'
    if audit_path.exists():
        audit_status=read(audit_path);result['auxiliary_audit']=audit_status
        if audit_status.get('status')!='COMPLETE' or audit_status.get('errors') or audit_status.get('disagreements'):
            result['technical_issues'].append('Auxiliary native-accounting audit incomplete or disagrees; primary observations are preserved unchanged')
    elif (out/'gpu2_audit/owned_process.json').exists():
        result['auxiliary_audit']=dict(status='MISSING_COMPLETION_RECORD')
        result['technical_issues'].append('Auxiliary audit has no completion record; inspect its process log')
    if (out/'gpu2_audit/drain_incomplete.json').exists():result['technical_issues'].append('Auxiliary audit drain incomplete')
    write(out/'analysis/summary.json',result);write(out/'analysis/cross_profile_conditions.json',comparisons)
    performance={}
    for family in PROFILES:
        local=out/'models'/family;events=local/'phase_events.jsonl'
        import json
        phase_rows=[json.loads(line) for line in events.read_text().splitlines()] if events.exists() else []
        phases={}
        for row in phase_rows:
            value=phases.setdefault(row['phase'],{})
            value[row['event']]=row['epoch'];value['jobs']=row['jobs']
        times={name:r['DRAINED']-r['START'] for name,r in phases.items() if 'DRAINED' in r and 'START' in r}
        results=[read(p) for kind in ['workflows','forks'] for p in (local/kind).glob('*/result.json')]
        sum_durations=sum(r.get('elapsed_seconds',0) for r in results);phase_wall=sum(times.values())
        performance[family]=dict(phase_wall_seconds=times,sum_case_elapsed_seconds=sum_durations,
            observed_overlap_ratio=sum_durations/phase_wall if phase_wall else None,
            scope='Observed overlapping case durations / observed phase wall time; not measured speedup against an otherwise identical serial run. Queueing and sampling can differ.')
    write(out/'analysis/performance.json',performance)
    if (out/'gpu2_audit/status.json').exists():write(out/'analysis/gpu2_audit_status.json',read(out/'gpu2_audit/status.json'))
    (out/'analysis/FINDINGS.md').write_text('# Parallel two-profile discovery campaign\n\nNo paper-ready verdict is automated. Read the per-profile event/effect ledgers and actual requests.\n\nThe same task conditions are repeated on Qwen and Gemma; their interfaces differ and independent workflows overlap on GPU3. Interpret treatment contrasts within each profile first. A between-profile difference is not a causal effect of model weights. Missing/censored cases are not safe outcomes. Authenticated conditional continuations remain separate from autonomous roots.\n')
    return result
