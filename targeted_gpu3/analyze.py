"""Read-only event/HTTP reanalysis; write derived records outside the raw run."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
from .core import independent_effects,transport,digest


def audit(run,out):
    run=Path(run).resolve();out=Path(out).resolve()
    if out==run or run in out.parents:raise ValueError('Analysis output must be outside immutable raw run')
    out.mkdir(parents=True,exist_ok=False);checks=[];errors=[]
    manifest=run/'SHA256SUMS'
    seen=set()
    if manifest.is_file():
        for line in manifest.read_text().splitlines():
            expected,relative=line.split('  ',1);rel=Path(relative)
            if rel.is_absolute() or '..' in rel.parts or relative in seen:raise ValueError('Unsafe/duplicate manifest entry')
            seen.add(relative);path=run/rel
            actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
            if actual!=expected:errors.append(dict(path=relative,error='HASH_MISMATCH_OR_MISSING'))
        extras=[str(p.relative_to(run)) for p in run.rglob('*') if p.is_file() and p.name!='SHA256SUMS'
                and str(p.relative_to(run)) not in seen]
        if extras:errors.append(dict(unmanifested_files=extras))
    else:errors.append(dict(error='MANIFEST_NOT_PRESENT_RUN_MAY_BE_ACTIVE_OR_INTERRUPTED'))
    episodes=[];calls=[];unique=collections.defaultdict(list);shapes=collections.defaultdict(list);http=[]
    from .experiment import schedule
    reuse=(run/'reused_qualification.json').is_file()
    for item in ([] if reuse else schedule()['qualification_episodes']):
        path=run/item['model']/'experiment'/item['id'];result=path/'result.json'
        if not result.is_file():
            episodes.append(dict(episode=item['id'],model=item['model'],recorded=False));continue
        events=[json.loads(x) for x in (path/'events.jsonl').read_text().splitlines()]
        spec=next(e['spec'] for e in events if e['event']=='initial_state')
        effects=next(e['effects'] for e in events if e['event']=='initial_state').copy()
        data=json.loads(result.read_text());shape=[];actor_proposal_profiles=[]
        for e in events:
            if e['event']=='commit':effects.append({k:e[k] for k in ('effect_id','occurrence_id','recipient','amount','key','origin')})
            if e['event']=='model_response':
                shape.append([e['role'],[c['function'] for c in e['calls']]])
                if e['role']=='actor':
                    projected=list(effects);known_keys={x['key']:(x['recipient'],x['amount']) for x in effects if x['key']}
                    invalid=[]
                    for c in e['calls']:
                        calls.append(dict(episode=item['id'],model=item['model'],event=e['seq'],role='actor',call=c,
                                          committed_before=len(effects)))
                        if c['function']=='pay':
                            a=c['args'];recipient=a.get('recipient');amount=a.get('amount');key=a.get('key','')
                            if recipient not in spec['accounts'].values() or type(amount) is not int or amount<=0:
                                invalid.append(c);continue
                            if key and known_keys.get(key)==(recipient,amount):continue
                            projected.append(dict(recipient=recipient,amount=amount,key=key))
                            if key:known_keys[key]=(recipient,amount)
                    actor_proposal_profiles.append(dict(event=e['seq'],calls=e['calls'],invalid_domain=invalid,
                        hypothetical_effect_violations=independent_effects(spec,projected),scope='Proposal diagnostic, not committed effects'))
            if e['event']=='runtime_result' and e.get('error'):shape.append(['error',e['function']])
            if e['event']=='native_route':shape.append(['route',e['route']])
        vs=independent_effects(spec,effects)
        if effects!=data['effects']:errors.append(dict(episode=item['id'],error='EFFECT_LEDGER_JOIN_MISMATCH'))
        if any(vs.values())!=data['independent_violation']:errors.append(dict(episode=item['id'],error='VIOLATION_RECONSTRUCTION_MISMATCH'))
        violation=True if any(vs.values()) else False if data['outcome']['lifecycle_closed'] and not data['error'] else 'UNKNOWN'
        episodes.append(dict(episode=item['id'],model=item['model'],recorded=True,violation=violation,
            observed_forbidden_commit=any(vs.values()),
            dimensions=vs,effects=effects,actor_proposal_profiles=actor_proposal_profiles,
            runtime_errors=[e for e in events if e['event']=='runtime_result' and e.get('error')],
            evidence='AUTONOMOUS_ADAPTED_DEVELOPMENT',error=data['error']))
        shapes[json.dumps(shape)].append(item['id'])
    for family in ('qwen','gemma'):
        for p in (run/family/'experiment').rglob('http_*.request.json'):
            request=json.loads(p.read_text());response=p.with_name(p.name.replace('.request.json','.response.json'))
            role=p.name.split('_')[-1].split('.')[0]
            entry=dict(file=str(p.relative_to(run)),role=role,request_sha256=digest(request),has_response=response.is_file(),
                       seed=request.get('seed'),model=request.get('model'),temperature=request.get('temperature'),
                       evidence='CONDITIONAL' if '/references/' in str(p) or '/exhaustion/' in str(p) else 'AUTONOMOUS_DEVELOPMENT')
            if response.is_file():
                data=json.loads(response.read_text());message=data['choices'][0]['message']
                normalized=json.dumps(message,sort_keys=True)
                # Only opaque account identifiers are normalized, never wording.
                normalized=re.sub(r'acct_([AM])_[0-9a-f]{10}',r'acct_\1_<ID>',normalized)
                unique[normalized].append(str(response.relative_to(run)));entry['usage']=data.get('usage',{})
            http.append(entry)
    transport.write(out/'episode_ledger.json',episodes);transport.write(out/'actor_calls.json',calls)
    transport.write(out/'http_ledger.json',http)
    transport.write(out/'response_classes.json',[dict(normalized_response=k,files=v) for k,v in unique.items()])
    transport.write(out/'trajectory_classes.json',[dict(shape=json.loads(k),episodes=v) for k,v in shapes.items()])
    with (out/'http_ledger.csv').open('w',newline='') as f:
        if http:
            fields=sorted(set().union(*(x.keys() for x in http)));w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(http)
    summary=dict(status='AUDIT_PASS' if not errors else 'AUDIT_WITH_UNRESOLVED_CHECKS',manifest_entries=len(seen),
        recorded_qualification_episodes=sum(x['recorded'] for x in episodes),scheduled_qualification_episodes=len(episodes),
        qualification_reused=bool(reuse),
        fresh_generation_attempt_files=len(http),roles=dict(collections.Counter(x['role'] for x in http)),
        normalized_response_classes=len(unique),trajectory_classes=len(shapes),errors=errors,
        human_semantic_review='PENDING',note='Engineering replays and forced components are not autonomous episode replications')
    transport.write(out/'audit.json',summary)
    (out/'READ_ME.md').write_text('# Event/HTTP audit\n\nInspect every trajectory and response class before selecting the next hypothesis. '
        'Class counts are compressions of this run, not independent samples. Actor proposal profiles preserve invalid calls, '
        'current effect state and per-dimension hypothetical violations. Actual violations are reconstructed only from committed state. '
        'Reference edits/effects and optional role probes retain their conditional/component scope. '
        'This audit does not identify attention, internal understanding, causal prevalence or external novelty.\n')
    print(json.dumps(summary,indent=2));return summary


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();audit(a.run,a.out)
