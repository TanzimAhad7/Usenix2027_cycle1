"""Read-only reconstruction of archived evidence. No model calls or GPU use.

The supplied latest archive retains Qwen results by hash; full Qwen traces are
resolved to the parent archive. Recomputed properties concern selected records,
not an estimate of an independent task population.
"""
import argparse, collections, hashlib, importlib.util, json
from pathlib import Path

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, x): p.write_text(json.dumps(x, indent=2, ensure_ascii=False)+'\n')

def main(a):
    a.out.mkdir(parents=True, exist_ok=True)
    s=importlib.util.spec_from_file_location('measure', a.prior/'code/permission_audit.py')
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
    paths=read(a.prior/'derived/CURRENT_SEVEN_PATHS.json')
    witnesses=[]; inputs=[]; e2=[]; comparisons=[]
    for r in paths:
        base=(a.parent if r['profile']=='qwen' else a.latest)/r['profile']/'E3'/r['id']
        source=base/'result.json'; result=read(source)
        if r['profile']=='qwen':
            retained=read(a.latest/'qwen/E3'/r['id']/'result.json')
            assert retained['_retained_from_parent']['original_sha256']==sha(source)
        io=read(base/'driver_records.json')
        for route in r['routes']:
            f=base/'checkpoints'/('proposal_%04d.json'%route['proposal']); cp=read(f)
            effects=m.extract(cp['world']['environment'])
            allowed=cp['spec']['choice_contract']
            candidate=route['candidate']
            candidate_permitted=any(m.key(candidate)==m.key(v) for slot in allowed['slots'] for v in slot['alternatives'])
            refs=route['reference']; ref_violation=m.measure(allowed,refs)['violation']
            msgs=cp['messages']; root=cp['spec']['root']
            root_facts_present=all(str(v['args'].get('body',v['args'].get('subject',''))) in root
                for slot in allowed['slots'] for v in slot['alternatives'])
            row=dict(profile=r['profile'],id=r['id'],proposal=route['proposal'],
                committed_sensitive_prefix=len(effects),prefix_oracle=m.measure(allowed,effects),
                candidate_in_permitted_alternatives=candidate_permitted,reference_violates=ref_violation,
                route=route['route'],root_contains_permitted_body_or_subject=root_facts_present,
                checkpoint_path=str(f),checkpoint_sha256=sha(f),result_path=str(source),result_sha256=sha(source),
                trusted_root=root,choice_contract=allowed,
                messages_before_proposal=[dict(role=z['role'],content=z.get('content')) for z in msgs])
            witnesses.append(row)
        for z in io:
            if z['role'] in ('attenuator','reference','judge'):
                inputs.append(dict(profile=r['profile'],id=r['id'],index=z['index'],role=z['role'],
                    request=z['request'],request_hash=z['request_hash'],response=z.get('response'),
                    driver_path=str(base/'driver_records.json'),driver_sha256=sha(base/'driver_records.json')))
    for family in ('qwen','gemma'):
        root=a.parent if family=='qwen' else a.latest
        for f in sorted((root/family/'E2').glob('*/result.json')):
            r=read(f);arm=r['native_clone_arms']['SOURCE_ADMISSION']
            e2.append(dict(profile=family,id=r['id'],origin=r['origin'],view=r['view'],
                draw=int(r['id'].rsplit('_D',1)[1]),new_bad=arm['new_unmatched_effect_count'],
                bad_reference=r['reference_proposal_oracle']['violation'],
                routes=[z['route'] for z in r['source_decisions']],
                decisions_allowed=[z['allowed'] for z in r['source_decisions']],path=str(f),sha256=sha(f)))
    groups=collections.defaultdict(dict)
    for x in e2:groups[(x['profile'],x['origin'],x['draw'])][x['view']]=x
    for (profile,origin,draw),g in sorted(groups.items()):
        assert set(g)=={'SOURCE','EVIDENCE'}
        comparisons.append(dict(profile=profile,origin=origin,draw=draw,
            same_bad_count=g['SOURCE']['new_bad']==g['EVIDENCE']['new_bad'],source=g['SOURCE'],evidence=g['EVIDENCE']))
    ledger=read(a.prior/'derived/CURRENT_E3_NATIVE_LEDGER.json'); missing=[];physical=[]
    for family in ('qwen','gemma'):
        rr=[r for r in ledger if r['profile']==family]
        blocks=collections.defaultdict(list)
        for r in rr:blocks[r['root']].append(r)
        missing.append(dict(profile=family,failures=sum(not r['qualified']for r in rr),
            complete_failed_blocks=[dict(root=k,cases=[z['id']for z in v])for k,v in blocks.items()if len(v)==6 and all(not z['qualified']for z in v)],
            failures_by_root={k:sum(not z['qualified']for z in v)for k,v in blocks.items()if any(not z['qualified']for z in v)}))
        safe=[r for r in rr if r['qualified'] and not r['violation'] and r['outcome']=='SAFE_NON_COMPLETION']
        physical.append(dict(profile=family,safe_non_completion=len(safe),
            physical_true_reporting_false=sum(r['physical'] and not r['reporting']for r in safe),
            physical_false_reporting_true=sum(not r['physical'] and r['reporting']for r in safe),
            both_false=sum(not r['physical'] and not r['reporting']for r in safe)))
    write(a.out/'ZERO_PREFIX_WITNESSES.json',witnesses)
    write(a.out/'DELIVERED_INPUTS.json',inputs)
    write(a.out/'PAIRED_E2.json',comparisons)
    write(a.out/'MISSINGNESS.json',missing)
    write(a.out/'PHYSICAL_VS_REPORTING.json',physical)
    summary=dict(witnesses=len(witnesses),zero_prefix=sum(x['committed_sensitive_prefix']==0 for x in witnesses),
        all_candidates_outside_contract=all(not x['candidate_in_permitted_alternatives']for x in witnesses),
        bad_reference_witnesses=sum(x['reference_violates']for x in witnesses),
        routes=dict(collections.Counter(x['route']for x in witnesses)),
        paired_e2={family:dict(pairs=sum(x['profile']==family for x in comparisons),
            same_bad_count=sum(x['profile']==family and x['same_bad_count']for x in comparisons),
            lawful_to_bad_reference=sum(x['profile']==family and not x['source']['bad_reference']and x['evidence']['bad_reference']for x in comparisons),
            same_harm_changed_routes=sum(x['profile']==family and x['same_bad_count']and x['source']['routes']!=x['evidence']['routes']for x in comparisons))
            for family in ('qwen','gemma')},
        scope='Fresh CPU reconstruction of archived records. No new model inference, independent task sampling, or deployment measurement.')
    write(a.out/'RECONSTRUCTION_SUMMARY.json',summary)
    print(json.dumps(summary,indent=2))
    assert summary['witnesses']==7 and summary['zero_prefix']==7
    assert summary['all_candidates_outside_contract']
    assert summary['paired_e2']['gemma']['pairs']==56 and summary['paired_e2']['gemma']['same_bad_count']==56

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--latest',type=Path,required=True)
    p.add_argument('--parent',type=Path,required=True);p.add_argument('--prior',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    main(p.parse_args())
