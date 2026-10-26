"""Primitive cross-workflow ledger. Flags are inspection leads, not mechanisms."""
import argparse
import collections
import csv
import json
from pathlib import Path
from .common import write
from .observer import assess

def signature(c):return c['function'],json.dumps(c['args'],ensure_ascii=True,sort_keys=True)

def diagnostic_coverage(run):
    from .protocol import schedule
    from .interventions import PROFILES
    workflows=[];origins=[];recovery=[]
    for item in schedule():
        if item['defense']!='ON' or item['spec']['condition']!='hostile':continue
        d=run/item['model_family']/'diagnostics'/item['id'];result=d/'result.json'
        row=json.loads(result.read_text()) if result.exists() else {'status':'NOT_RECORDED'}
        selection=d/'selection.json';selected=json.loads(selection.read_text()) if selection.exists() else {}
        workflows.append(dict(id=item['id'],diagnostic_status=row['status'],eligible=selected.get('eligible_count'),
            selected=len(row.get('origins',[])),error=row.get('error')))
        for origin in row.get('origins',[]):
            diagnosis=origin['diagnosis'];cells=diagnosis.get('cells',{})
            for profile in PROFILES:
                for policy in ('M0','M1'):
                    cell=cells.get(profile+'_'+policy,{})
                    origins.append(dict(episode=item['id'],source_batch=origin['source_batch'],profile=profile,policy=policy,
                        status=cell.get('status','NOT_RECORDED'),violation=cell.get('violation','UNKNOWN'),
                        new_effects=cell.get('new_effects'),error=cell.get('detail') or diagnosis.get('error')))
    for family in ('qwen','gemma'):
        file=run/family/'lawful_recovery/results.json'
        rows=json.loads(file.read_text()) if file.exists() else []
        indexed={r['case']:r for r in rows}
        for case in ('L1','L2','L3','L4'):
            row=indexed.get(case,{})
            for policy in ('M0','M1'):
                result=row.get(policy,{})
                recovery.append(dict(model=family,case=case,policy=policy,
                    status=result.get('outcome',{}).get('status',row.get('status','NOT_RECORDED')),
                    fresh_generations=result.get('fresh_model_generations'),error=result.get('error')))
    unresolved=sum(c['status'] not in ('RECONSTRUCTED_REFERENCE_COMPONENT','COMPONENT_COMPLETE') for c in origins)
    return dict(workflows=workflows,reconstructed_cells=origins,lawful_recovery=recovery,
        reconstructed_cells_recorded=len(origins),unresolved_reconstructed_cells=unresolved,
        lawful_continuations_recorded=sum(r['status'] not in ('NOT_RECORDED','PREFIX_FAILED') for r in recovery),
        note='Missing origins after no carrier/no proposal are not negative intervention results; conditional cells are not core episodes')

def analyze(run):
    run=Path(run);out=run/'analysis';out.mkdir(exist_ok=True)
    episodes=[];occurrences=[];batches=[];flags=[]
    for file in sorted(run.glob('*/workflows/*/result.json')):
        directory=file.parent;row=json.loads(file.read_text());ident=row['item']['id']
        events=[json.loads(line) for line in (directory/'events.jsonl').read_text().splitlines()]
        joined={};carrier=False;skipped_after_carrier=0
        def entry(callid):return joined.setdefault(callid,dict(episode=ident,occurrence_id=callid,proposed=False,
            reviewed=False,admitted=False,dispatched=False,committed_effects=0,tool_error=None,route=None))
        for e in events:
            kind=e['event']
            if kind=='carrier_delivery':carrier=True
            if kind=='model_response' and e['role']=='actor':
                for c in e['calls']:entry(c['id']).update(proposed=True,function=c['function'],args=c['args'])
            if kind=='guard_match_decision':entry(e['actor_id']).update(reviewed=True,match_decision=e['survived'],exact=e['exact'])
            if kind=='release':
                for c in e['calls']:entry(c['id']).update(admitted=True,route=e['route'])
                if carrier and e['route']=='source_no_current_review':skipped_after_carrier+=len(e['calls'])
            if kind=='dispatch':entry(e['occurrence_id']).update(dispatched=True)
            if kind=='commit':entry(e['occurrence_id'])['committed_effects']+=e['after_count']-e['before_count']
            if kind=='runtime_result' and e['error']:entry(e['occurrence_id'])['tool_error']=e['error']
        occurrences.extend(joined.values())
        summary=dict(episode=ident,model=row['item']['model_family'],structure=row['item']['spec']['structure'],
            instance=row['item']['spec']['instance'],condition=row['item']['spec']['condition'],defense=row['item']['defense'],
            outcome=row['outcome']['status'],carrier_reached=row['carrier_reached'],actor_proposals=sum(o['proposed'] for o in joined.values()),
            reviewed=sum(o['reviewed'] for o in joined.values()),admitted=sum(o['admitted'] for o in joined.values()),
            dispatched=sum(o['dispatched'] for o in joined.values()),committed_effects=sum(o['committed_effects'] for o in joined.values()),
            tool_errors=sum(bool(o['tool_error']) for o in joined.values()),
            receipt_mismatches=sum(e['event']=='feedback_identity' and e['mismatch'] for e in events),
            skipped_after_carrier=skipped_after_carrier,generation_failures=len(row['generation_failures']),
            requests=row['requests'],fresh_generations=row['fresh_model_generations'],elapsed_seconds=row['elapsed_seconds'])
        episodes.append(summary)
        if summary['tool_errors'] and row['error'] is None:flags.append(dict(episode=ident,flag='TOOL_ERRORS_WITHOUT_TOP_LEVEL_ERROR'))
        if skipped_after_carrier:flags.append(dict(episode=ident,flag='UNREVIEWED_RELEASE_AFTER_CARRIER_NOT_AUTOMATICALLY_FORBIDDEN'))
        if summary['receipt_mismatches']:flags.append(dict(episode=ident,flag='RECEIPT_OCCURRENCE_MISMATCH'))
        for path in sorted(directory.glob('batch_*_result.json')):
            b=json.loads(path.read_text());actors=b['checkpoint']['pending_calls'];refs=b['reference'];released={c['id'] for c in b['released']}
            supporting=collections.defaultdict(set)
            for c in actors:
                if c['id'] not in released:continue
                for j,r in enumerate(refs):
                    if signature(c)==signature(r):supporting[j].add(c['id'])
            witness_reuse=any(len(ids)>1 for ids in supporting.values())
            spec=b['checkpoint']['item']['spec']
            before=assess(spec,b['checkpoint']['world'],False)
            after=assess(spec,b['world_after'],False)
            batches.append(dict(episode=ident,path=str(path.relative_to(run)),actor_count=len(actors),reference_count=len(refs),
                released_count=len(released),exact_shared_support=witness_reuse,
                inherited_effects=b['checkpoint']['completed_prefix_effects'],
                remaining_count_before=spec['max_count']-before['effects'],
                effects_after=after['effects'],violation_before=before['violation'] is True,
                violation_after=after['violation'] is True,
                first_violation_in_this_batch=before['violation'] is not True and after['violation'] is True))
            if witness_reuse:flags.append(dict(episode=ident,flag='MULTIPLE_RELEASED_OCCURRENCES_SHARE_EXACT_REFERENCE_SUPPORT',batch=path.name))
    for name,rows in [('episodes',episodes),('occurrences',occurrences),('batches',batches),('inspection_flags',flags)]:
        write(out/(name+'.json'),rows)
        keys=list(dict.fromkeys(k for row in rows for k in row))
        with (out/(name+'.csv')).open('w',newline='') as f:
            if keys:
                writer=csv.DictWriter(f,fieldnames=keys);writer.writeheader();writer.writerows(rows)
    grouped=collections.defaultdict(list)
    for r in episodes:grouped[(r['model'],r['structure'],r['condition'],r['defense'])].append(r)
    table=[dict(model=k[0],structure=k[1],condition=k[2],defense=k[3],workflows=len(rows),
        violations=sum(r['outcome']=='VIOLATION' for r in rows),secure_completion=sum(r['outcome']=='SECURE_COMPLETION' for r in rows),
        unknown=sum(r['outcome']=='UNKNOWN' for r in rows),tool_errors=sum(r['tool_errors'] for r in rows))
        for k,rows in sorted(grouped.items())]
    write(out/'grouped.json',table)
    write(out/'scope.json',dict(episodes=len(episodes),occurrences=len(occurrences),
        scope='CORE_WORKFLOWS_ONLY: conditional components and continuation forks excluded',
        inference='Finite authored panel; flags are diagnostic leads; no population or causal inference'))
    coverage=diagnostic_coverage(run);write(out/'diagnostic_coverage.json',coverage)
    return dict(episodes=len(episodes),occurrences=len(occurrences),flags=len(flags),
        unresolved_diagnostic_cells=coverage['unresolved_reconstructed_cells'],
        lawful_continuations_recorded=coverage['lawful_continuations_recorded'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('run',type=Path);a=p.parse_args();print(analyze(a.run))
