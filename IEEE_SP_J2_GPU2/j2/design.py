"""Read the frozen schedule and derive permission from the actual task."""
import copy
from reference_study.common import ROOT, read, digest
from j1.design import inputs as original_inputs, normal

def inputs(item):
    task,candidate,references,allowed=original_inputs(item)
    if references or candidate['function']!='place_order' or item['criterion']!='OWNER_PRIORITY':
        raise RuntimeError('J2 requires procurement, frozen OWNER and no reference')
    first=candidate['args']['item_id'];second=candidate['args']['quantity']
    predictions=dict(EXACT_JOINT=candidate in allowed,
        INDEPENDENT_FIELDS=any(o['args']['item_id']==first for o in allowed)and any(o['args']['quantity']==second for o in allowed),
        ALLOW_ALL=True,DENY_ALL=False,
        FIRST_FIELD_ONLY=any(o['args']['item_id']==first for o in allowed),
        SECOND_FIELD_ONLY=any(o['args']['quantity']==second for o in allowed))
    if predictions!=item['predictions']:raise RuntimeError('Frozen predictions disagree with actual grant')
    return task,candidate,references,allowed

def manifest(family):
    data=read(ROOT/'design/DESIGN_ONLY_MANIFEST.json')
    if data['protocol']!='J2_PERMISSION_RESPONSE_V1' or data['status']!='PROPOSED_NOT_RUN':
        raise RuntimeError('Unexpected J2 design')
    jobs=[]
    for row in data['acquisitions']:
        if row['profile']!=family:continue
        item=copy.deepcopy(row)
        item.update(stage='J2',config='RELEASE',panel='MAIN',input_key=digest(row['request_body']))
        inputs(item);jobs.append(item)
    if len(jobs)!=32 or sum(i['expected_legal']for i in jobs)!=12:
        raise RuntimeError('J2 allocation drift')
    return dict(version='J2_LIVE_V1',stage='J2',family=family,jobs=jobs,
        planned=32,configs=['RELEASE'],scope='Counterfactual local permission judgment; zero autonomous workflows.')

def groups(m):
    return [('BLOCK_'+str(b),[i for i in m['jobs']if i['block']==b])for b in (0,1)]
