"""Validate the compact reconstruction package; no raw archives or inference."""
import csv,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report=(ROOT/'IEEE_SP_Standalone_Research_Authority_Current.md').read_text()
    heads=[int(x)for x in re.findall(r'^## (\d+)\.',report,re.M)]
    assert heads==list(range(1,35)),heads
    s=read(ROOT/'derived/RECONSTRUCTION_SUMMARY.json')
    assert (s['witnesses'],s['zero_prefix'],s['bad_reference_witnesses'])==(7,7,5)
    assert s['routes']=={'EXACT':5,'FUZZY':2}
    assert s['all_candidates_outside_contract']
    assert s['paired_e2']['gemma']['same_bad_count']==56
    assert s['paired_e2']['gemma']['same_harm_changed_routes']==4
    assert s['paired_e2']['qwen']['same_bad_count']==51
    pairs=read(ROOT/'derived/PAIRED_E2.json');assert len(pairs)==112
    assert len({(x['profile'],x['origin'],x['draw'])for x in pairs})==112
    changes=[x for x in pairs if x['profile']=='gemma'and x['source']['routes']!=x['evidence']['routes']]
    assert len(changes)==4
    for x in changes:
        assert x['source']['routes']==['FUZZY','FUZZY']and x['evidence']['routes']==['EXACT','EXACT']
        assert not x['source']['bad_reference']and x['evidence']['bad_reference']
        assert x['source']['new_bad']==x['evidence']['new_bad']==2
    missing=read(ROOT/'derived/MISSINGNESS.json');g=next(x for x in missing if x['profile']=='gemma')
    assert g['failures']==43 and len(g['complete_failed_blocks'])==7
    assert sum(len(x['cases'])for x in g['complete_failed_blocks'])==42
    inputs=read(ROOT/'provenance/INSPECTED_INPUTS.json')
    before=next(x for x in inputs if x['role']=='preceding_authority')
    assert sha(ROOT/'provenance/Authority_Before_This_Audit.md')==before['sha256']
    assert sha(ROOT/'provenance/Authority_Before_This_Audit.md')==sha(ROOT/'retained_global_audit/IEEE_SP_Standalone_Research_Authority_Current.md')
    claims=list(csv.DictReader((ROOT/'derived/CLAIM_LEDGER.csv').open()));assert len(claims)==20
    assert all(all(r.values())for r in claims)
    schedule=dict(P1_sequences=19*2*2*4,P1_min_model_calls=19*2*4*(3+4),
        P2_cells=4*2*2*2*2*4+4*2*2*4,P2_max_judge_calls=320-64,
        P3_primary=32*3*2*2,P3_level3=8*3*2)
    assert schedule==dict(P1_sequences=304,P1_min_model_calls=1064,P2_cells=320,P2_max_judge_calls=256,P3_primary=384,P3_level3=48)
    manifest=ROOT/'SHA256SUMS';checked=0
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            h,name=line.split('  ',1);assert sha(ROOT/name)==h,name;checked+=1
    result=dict(status='PASS',sections=34,claims=20,paired_records=112,zero_prefix_witnesses=7,
        complete_gemma_failed_blocks=7,prospective_schedule=schedule,manifest_entries_checked=checked,
        fresh_model_inference=0,scope='CPU package validation, not semantic adjudication or future experiment execution.')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
