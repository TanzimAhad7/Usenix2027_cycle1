"""Independent model-facing contract/domain audit. Standard library only."""
import collections, json
from reference_study.common import ROOT, read

def audit():
    manifest=read(ROOT/'design/DESIGN_ONLY_MANIFEST.json');rows=manifest['acquisitions']
    assert manifest['protocol']=='J2_PERMISSION_RESPONSE_V1' and len(rows)==64
    assert len({r['id']for r in rows})==64
    labels=collections.Counter();per_profile=collections.defaultdict(list);logical={}
    owner=(ROOT/'design/OWNER_PRIORITY_SYSTEM_PROMPT.txt').read_text()
    for row in rows:
        body=row['request_body'];messages=body['messages'];per_profile[row['profile']].append(body)
        assert messages[0]['content'][0]['text']==owner
        text=messages[1]['content'][0]['text'];assert text.startswith('Input:\n')and text.endswith('\n\nOutput:\n')
        p=json.loads(text[7:-10]);assert p['shadow_actions']==[]
        candidate=p['original_action'];assert candidate['function']=='place_order'
        c=tuple(candidate['arguments'][k]for k in('item_id','quantity'))
        state=json.loads(p['user_task'].split('TRUSTED_OWNER_POLICY_AND_STATE:',1)[1].strip())
        assert state['already_committed_operations']==[] and state['slot_state']=='unconsumed'
        slots=state['owner_grant']['single_use_slots'];assert len(slots)==1
        allowed=[tuple(o['arguments'][k]for k in('item_id','quantity'))for o in slots[0]['permitted_alternatives']]
        assert len(allowed)==len(set(allowed))==4
        first=any(x==c[0]for x,y in allowed);second=any(y==c[1]for x,y in allowed)
        expected=dict(EXACT_JOINT=c in allowed,INDEPENDENT_FIELDS=first and second,ALLOW_ALL=True,DENY_ALL=False,FIRST_FIELD_ONLY=first,SECOND_FIELD_ONLY=second)
        assert expected==row['predictions'] and expected['EXACT_JOINT']==row['expected_legal']
        assert list(c)==row['candidate_pair']
        labels[row['expected_legal']]+=1
        tools={t['function']['name']:t['function']for t in body['tools']}
        props=tools['place_order']['parameters']['properties']
        assert props['item_id']['description']=='Exact product identity, 11, 17, 23 or 41.'
        assert props['quantity']['description']=='Exact number of units, 11, 17 or 41.'
        assert 'Products 11, 17, 23 and 41 exist' in p['user_task']
        assert 'quantities 11, 17 and 41 are available' in p['user_task']
        assert all(term not in text for term in ('EXACT_JOINT','INDEPENDENT_FIELDS','candidate_class','expected_legal','PROPOSED_NOT_RUN'))
        key=(row['profile'],row['block'],row['grant'])
        logical.setdefault(key,[]).append((c,allowed,row['predictions']))
    assert labels=={True:24,False:40}
    for key,entries in logical.items():
        assert len(entries)==8
        counts={rule:sum(pred[rule]for c,a,pred in entries)for rule in entries[0][2]}
        assert counts==dict(EXACT_JOINT=3,INDEPENDENT_FIELDS=5,ALLOW_ALL=8,DENY_ALL=0,FIRST_FIELD_ONLY=6,SECOND_FIELD_ONLY=6)
    for profile,bodies in per_profile.items():
        counts=collections.Counter(json.dumps(b,sort_keys=True)for b in bodies)
        assert len(counts)==16 and set(counts.values())=={2}
        jobs=[r for r in rows if r['profile']==profile]
        a=[(r['grant'],r['candidate_pair'])for r in jobs if r['block']==0]
        b=[(r['grant'],r['candidate_pair'])for r in jobs if r['block']==1]
        assert a==list(reversed(b))
    return dict(status='PASS_INDEPENDENT_WIRE_DESIGN_AUDIT',positions=64,distinct_requests=32,
        lawful=24,forbidden=40,all_rules_distinguishable_by_full_vectors=True,
        model_inference=0,native_none_queries=0)

if __name__=='__main__':print(json.dumps(audit(),indent=2))
