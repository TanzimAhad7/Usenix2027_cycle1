"""Read-only reconstruction of every recorded slot; no GPU or model service.

Hash integrity and predicate recomputation do not establish human consensus,
paper-profile reproduction or truthful effects under a compromised collector.
"""
import argparse,json
from pathlib import Path
from .common import read,file_hash
from .world import World
from .observer import assess

def verify(run):
    run=Path(run).resolve();errors=[];hashes=0;recorded=0
    sums=run/'SHA256SUMS'
    if sums.exists():
        for line in sums.read_text().splitlines():
            h,name=line.split('  ',1);p=(run/name).resolve()
            if not p.is_relative_to(run):errors.append('Unsafe manifest path: '+name);continue
            if not p.is_file() or file_hash(p)!=h:errors.append('Hash mismatch: '+name)
            hashes+=1
    else:errors.append('SHA256SUMS absent: interrupted/unarchived directory or incomplete copy')
    frozen=read(run/'FROZEN_MANIFEST.json');census=read(run/'census.json')
    expected={r['id'] for r in frozen['primary']+frozen['conditional']}
    if set(census)!=expected:errors.append('Scheduled slot set differs from frozen manifest')
    keys=['violation','physical_goal','protocol_completion','reporting_completion','effects','violations','event_state_agreement','actor_carrier_request_accepted']
    for base in ['autonomous','conditional']:
        for p in sorted((run/base).glob('*/result.json')):
            recorded+=1;directory=p.parent;r=read(p);item=read(directory/'item.json');snapshot=read(directory/'final_world.json')
            world=World(item['spec'],restore=snapshot)
            records=read(directory/'driver_records.json');actors=[x for x in records if x['role']=='actor' and 'response' in x]
            raw=actors[-1]['response']['choices'][0]['message'].get('content') or '' if actors else ''
            messages=read(directory/'messages.json');terminal=r['lifecycle']=='COMPLETE' and messages and messages[-1].get('role')=='assistant' and not messages[-1].get('tool_calls')
            fresh=assess(item['spec'],world.env,snapshot['events'],raw if terminal else '',r['lifecycle'])
            expected_outcome='UNKNOWN_TECHNICAL' if r['lifecycle'] in ['ERROR','CHECKPOINT_INVALID','INTERRUPTED'] and not fresh['violation'] else fresh['outcome']
            if expected_outcome!=r['outcome']:errors.append(r['id']+': outcome differs from reconstructed dimensions/lifecycle')
            for k in keys:
                if fresh[k]!=r[k]:errors.append(f'{r["id"]}: recomputed {k} differs')
            if not fresh['event_state_agreement']:errors.append(r['id']+': native final state differs from committed-event ledger')
            if r['id'] not in census or not census[r['id']].startswith('RECORDED'):errors.append(r['id']+': result/census join missing')
    for ident,status in census.items():
        if status.startswith('RECORDED') and not any((run/b/ident/'result.json').exists() for b in ['autonomous','conditional']):errors.append(ident+': recorded status has no result')
    return dict(status='PASS' if not errors else 'FAIL',manifest_hashes_checked=hashes,recorded_slots_reconstructed=recorded,scheduled_slots=len(census),errors=errors,model_calls=0,scope='Finite native-state, event, reporting and manifest reconstruction. Not independent human adjudication or a fresh model replication.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('run',type=Path);a=p.parse_args();r=verify(a.run);print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='PASS' else 1)
