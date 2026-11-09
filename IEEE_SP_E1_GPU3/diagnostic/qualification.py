from __future__ import annotations
import argparse,json,traceback
from pathlib import Path
from reference_study.common import ROOT,activate,read,write

def qualify(out):
    activate('qwen')
    from reference_discovery_parallel.base.source import verify_source
    from permission_admission.runtime import native_world
    from reference_discovery_parallel.common import unseal
    from diagnostic.skip import run as skip
    from diagnostic.design import manifest
    from diagnostic.cases import held
    from reference_discovery_parallel import world as native_world_module
    identity=verify_source();write(out/'source_identity.json',identity)
    catalog=read(ROOT/'diagnostic_inputs/CATALOG.json')
    for row in catalog:
        origin=read(ROOT/row['path']);cp=unseal(origin['checkpoint']);native_world(cp['spec'],cp['world'])
    # Exercise the real source parser, force-review path and native tools in all
    # input/criterion cells on a material witness and its lawful control.
    selected=[x for x in manifest()['P2']if x.get('origin')==catalog[0]['path']or x['stage']=='X3_CONSTRUCTED_INFORMATION_CONTROL']
    for item in selected:
        folder=out/'checker_cells'/item['id'];folder.mkdir(parents=True)
        result=held(item,folder,'qwen',True)
        if not result['qualified']:raise AssertionError('Mock transport did not qualify')
        exact=result['source_decision']['candidate_equals_reference']
        if exact and item['criterion']=='SOURCE':assert result['source_decision']['operative_route']=='EXACT_BYPASS'
        if exact and item['criterion']!='SOURCE':assert result['source_decision']['actual_judge_invoked']
    s=skip(out/'skip')
    from diagnostic.report import analyze
    m=manifest();replay=out/'pair_view_checks'
    # Use actual recorded request payloads above, independently compare paired
    # views. Both grant worlds share candidate/reference/schema/model inputs.
    failures=[];pairs=0
    for explicit in (False,True):
        for view in ('MINIMAL','PLACEBO','DESIGNATED_FACTS_AND_PREFIX'):
            for criterion in ('FORCED_SUPPORT','PERMISSION'):
                requests=[]
                for permitted in (False,True):
                    item=next(x for x in selected if x.get('stage')=='X3_CONSTRUCTED_INFORMATION_CONTROL'and x['explicit_rule']==explicit and x['permitted']==permitted and x['view']==view and x['criterion']==criterion)
                    records=read(out/'checker_cells'/item['id']/'model_io/driver_records.json');requests.append([x['request']for x in records if x['role']=='judge'])
                expected=not explicit and view!='DESIGNATED_FACTS_AND_PREFIX';equal=requests[0]==requests[1];pairs+=1
                if equal!=expected:failures.append(dict(explicit=explicit,view=view,criterion=criterion,equal=equal,expected=expected))
    write(out/'equal_view_checks.json',dict(pairs=pairs,mismatches=failures))
    if failures:raise AssertionError('Opposite-policy control request equality mismatch')
    value=dict(status='PASS',checkpoint_roundtrips=len(catalog),checker_cells=len(selected),opposite_permission_request_pairs=pairs,skip_cells=s['cells'],model_inference=0,
        independent_human_semantic_review='PENDING',scope='Meaningful source/native/component software validation; not model security evidence')
    write(out/'qualification.json',value);return value

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);a=ap.parse_args()
    try:print(json.dumps(qualify(a.out),indent=2))
    except Exception as e:
        write(a.out/'qualification.json',dict(status='FAIL',error=str(e),traceback=traceback.format_exc(),model_inference=0));raise
