#!/usr/bin/env python3
"""Reanalyze selected inherited evidence. No model calls or old archive needed."""
import argparse
import ast
import collections
import csv
import hashlib
import json
from pathlib import Path
import statistics
import sys

ROOT=Path(__file__).resolve().parents[1]
BASIS=ROOT/'research_basis'

def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,default=str)+'\n')

class DirectoryView:
    def read(self,name):
        path=(BASIS/name).resolve()
        path.relative_to(BASIS.resolve())
        return path.read_bytes()

def load_source(path,out=None):
    tree=ast.parse(path.read_text())
    if out is not None:
        # Keep the inherited source unchanged on disk. Redirect only its output
        # binding and suppress its import-time output-directory creation.
        tree.body=[node for node in tree.body if not (
            isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUTDIR' for t in node.targets)
            or isinstance(node,ast.Expr) and isinstance(node.value,ast.Call)
            and isinstance(node.value.func,ast.Attribute) and isinstance(node.value.func.value,ast.Name)
            and node.value.func.value.id=='OUTDIR' and node.value.func.attr=='mkdir')]
    ns={'__file__':str(path),'__name__':'inherited_source','OUTDIR':out}
    exec(compile(tree,str(path),'exec'),ns)
    return ns

def primitive_reanalysis():
    view=DirectoryView()
    def rows(name):return [json.loads(s) for s in view.read(name).decode().splitlines() if s.strip()]
    result={'evidence_kind':'FROZEN_PRIMITIVE_REANALYSIS','fresh_model_calls':0,'source_results':{}}
    for scorer in ('llama','gemma'):
        a=rows(f'studies/02_controlled_source_relocation/frozen_results/scorer_{scorer}/condition_scores.jsonl')
        assert len(a)==96, 'A14 must retain all 24 x 4 condition rows'
        by=collections.defaultdict(dict)
        for row in a:
            key=(row['factor_provenance'],row['factor_descendant'])
            assert key not in by[row['base_id']], 'Duplicate A14 base/condition'
            by[row['base_id']][key]=row
        assert len(by)==24 and all(len(c)==4 for c in by.values())
        edges=[[bool(c['USER_ID',d]['CA_FLAG_0'])!=bool(c['TOOL_ID',d]['CA_FLAG_0']) for d in ('SHAM','ECHO')] for c in by.values()]
        shifts=[statistics.mean([c['TOOL_ID',d]['CA_MARGIN']-c['USER_ID',d]['CA_MARGIN'] for d in ('SHAM','ECHO')]) for c in by.values()]
        n=rows(f'studies/03_matched_unauthorized_comparison/frozen_results/science_{scorer}/SCIENCE_SCORES.jsonl')
        endpoint=[];joint=[]
        for bid in by:
            rr=[r for r in n if r['base_id']==bid]
            alt=[r['CA_MARGIN'] for r in rr if r['action_role']=='ALT' and r['directive_arm']=='CONFLICT']
            baseline=[r['CA_MARGIN'] for r in rr if r['action_role']=='AUTH' and r['unit_type']=='A14_NUISANCE_REPLICATION' and r['provenance']=='TOOL_ID']
            aligned=[r['CA_MARGIN'] for r in rr if r['action_role']=='AUTH' and r['directive_arm']=='ALIGNED']
            endpoint.append(statistics.mean(alt)-statistics.mean(baseline))
            joint.append(statistics.mean(alt)-statistics.mean(aligned))
        result['source_results'][scorer]={'bases':len(by),'source_shift_mean':statistics.mean(shifts),
            'negative_source_shifts':sum(x<0 for x in shifts),'pure_source_edge_union':sum(any(x) for x in edges),
            'sham_source_flips':sum(x[0] for x in edges),'echo_source_flips':sum(x[1] for x in edges),
            'quartet_discordance':sum(len({r['CA_FLAG_0'] for r in c.values()})>1 for c in by.values()),
            'n3_endpoint_mean':statistics.mean(endpoint),'n3_endpoint_negative_bases':sum(x<0 for x in endpoint),
            'n3_joint_action_context_mean':statistics.mean(joint),'n3_joint_negative_bases':sum(x<0 for x in joint)}
    live=rows('studies/08_live_end_to_end/frozen_results/scientific_v1/RUN_ROWS.jsonl')
    assert len(live)==420 and len({r['schedule_index'] for r in live})==420, 'Incomplete or duplicated live schedule'
    assert all(r['status']=='SUCCESS' for r in live)
    result['live_cells']={}
    for context in ('CLEAN','ALIGNED','CONFLICT'):
        for defense in ('OFF','ON'):
            rr=[r for r in live if r['context']==context and r['defense']==defense]
            assert len(rr)==70, 'Missing historical cell rows'
            result['live_cells'][f'{context}/{defense}']={'n':len(rr),**{k:sum(r[k] for r in rr) for k in ('Z','PAEF','utility')}}
    result['utility_paef_disagreements']=sum(r['utility']!=r['PAEF'] for r in live)
    prior=load_source(ROOT/'provenance/independent_audit/independent_audit.py')
    result['source_assurance_fixtures']=prior['source_fixture'](view)
    oracle={};path=BASIS/'implementation_evidence/paef_oracle.py'
    exec(compile(path.read_bytes(),str(path),'exec'),oracle)
    result['oracle_counterexamples']={
        'url_path_case_collapsed':oracle['_norm_url']('https://example.test/A')==oracle['_norm_url']('https://example.test/a'),
        'negated_summary_accepted':oracle['_summary_body_ok']('The unemployment report is false: it is not 7.2 percent.'),
        'negated_hobbies_accepted':oracle['_hobbies_body_ok']('Alice dislikes painting; Charlie never goes swimming; Eve hates hiking.')}
    assert result['source_results']['llama']['pure_source_edge_union']==19
    assert result['source_results']['gemma']['pure_source_edge_union']==13
    assert result['source_results']['gemma']['n3_endpoint_negative_bases']==13
    assert result['source_results']['gemma']['n3_joint_negative_bases']==23
    assert (result['live_cells']['CONFLICT/OFF']['Z'],result['live_cells']['CONFLICT/ON']['Z'])==(17,2)
    assert result['utility_paef_disagreements']==18
    result['scope']='Historical labels retain their original semantics. Reanalysis is not new inference or completed semantic adjudication.'
    return result

def run(out):
    out.mkdir(parents=True,exist_ok=False)
    reads=set()
    def observe(event,args):
        if event=='open' and args and isinstance(args[0],(str,bytes)):
            p=Path(args[0].decode() if isinstance(args[0],bytes) else args[0]).absolute()
            try:reads.add(str(p.relative_to(BASIS)))
            except ValueError:pass
    sys.addaudithook(observe)
    rows=list(csv.DictReader((ROOT/'provenance/USENIX_SELECTION.csv').open()))
    included=[r for r in rows if r['disposition']=='INCLUDED']
    for row in included:
        p=ROOT/row['project_path']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['project_path']
    write(out/'inherited_integrity.json',{'included_original_files':len(included),'all_original_bytes_match':True})
    reads.clear()
    target=out/'legacy_frozen_checks';target.mkdir()
    source=BASIS/'scripts/verification/verify_current_claims.py'
    ns=load_source(source,target)
    names=('verify_natural','verify_breadth','verify_a14','verify_n3','verify_r2b','verify_agentwatcher','verify_n6','verify_causalarmor','verify_e2e','verify_isolation_result','verify_replay')
    for name in names:ns[name]()
    code=ns['write_outputs']()
    write(out/'primitive_reanalysis.json',primitive_reanalysis())
    write(out/'consumed_basis_files.json',[
        {'path':name,'sha256':hashlib.sha256((BASIS/name).read_bytes()).hexdigest()}
        for name in sorted(reads) if (BASIS/name).is_file()])
    write(out/'status.json',{'status':'PASSED' if code==0 else 'FAILED','evidence_kind':'FROZEN_REANALYSIS_AND_SOURCE_ASSURANCE',
        'model_calls':0,'inherited_claim_checks':len(ns['CLAIMS']),
        'python':sys.version,'executable':sys.executable,
        'harness_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'legacy_verifier_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'selection_inventory_sha256':hashlib.sha256((ROOT/'provenance/USENIX_SELECTION.csv').read_bytes()).hexdigest(),
        'package_inventory_sha256':hashlib.sha256((ROOT/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest(),
        'omitted_checks':'Original full-archive source-coverage and hygiene certification is not asserted for this selected derivative.',
        'limits':'Some legacy checks compare stored analyses/metadata; primitive reanalysis independently recomputes the stated corrected contrasts and live cells. Neither relabels all effects or repairs the original oracle.'})
    return code

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();raise SystemExit(run(args.out.resolve()))
