"""Decode the frozen, model-facing contracts. No new task generation at run time."""
import copy
import json
from reference_study.common import ROOT, read, digest


def manifest(family):
    data = read(ROOT / 'design/DESIGN_ONLY_MANIFEST.json')
    if data['protocol'] != 'J1_REVISION_2' or data['status'] != 'PROPOSED_NOT_RUN':
        raise RuntimeError('Unexpected frozen design')
    jobs = []
    for row in data['acquisitions']:
        if row['profile'] != family:
            continue
        item = copy.deepcopy(row)
        item.update(stage='J1_R2', config='RELEASE', panel=row['phase'],
                    input_key=digest(row['request_body']))
        jobs.append(item)
    if len(jobs) != 100 or sum(i['phase'] == 'MAIN' for i in jobs) != 96:
        raise RuntimeError('Frozen allocation mismatch')
    return dict(version='J1_R2_LIVE_V1', stage='J1_R2', family=family,
                jobs=jobs, planned=100, configs=['RELEASE'],
                scope='192 main component acquisitions plus eight separate sentinels; zero autonomous workflows.')


def normal(operation):
    return dict(function=operation['function'], args=copy.deepcopy(
        operation.get('arguments', operation.get('args'))))


def inputs(item):
    messages = item['request_body']['messages']
    text = messages[1]['content'][0]['text']
    prefix, suffix = 'Input:\n', '\n\nOutput:\n'
    if not text.startswith(prefix) or not text.endswith(suffix):
        raise RuntimeError('Unexpected source input envelope')
    payload = json.loads(text[len(prefix):-len(suffix)])
    task = payload['user_task']
    state = json.loads(task.split('TRUSTED_OWNER_POLICY_AND_STATE:', 1)[1].strip())
    if state['already_committed_operations']:
        raise RuntimeError('Expected an unconsumed initial state')
    grant = state['owner_grant']
    if 'single_use_slots' in grant:
        if len(grant['single_use_slots']) != 1:
            raise RuntimeError('Expected one operation slot')
        allowed = [normal(x) for x in grant['single_use_slots'][0]['permitted_alternatives']]
    else:
        allowed = [dict(function=grant['function'], args={
            grant['first_argument']: int(x), grant['second_argument']: y})
            for x, ys in grant['allowed_second_by_first'].items() for y in ys]
    candidate = normal(payload['original_action'])
    references = [normal(x) for x in payload['shadow_actions']]
    permitted = candidate in allowed
    if permitted != item['expected_legal'] or any(x not in allowed for x in references):
        raise RuntimeError('Actual contract disagrees with frozen truth/reference lawfulness')
    return task, candidate, references, allowed


def groups(m):
    """Barriers preserve sentinels, complete block 0, then reverse block 1."""
    return [('SENTINELS', [i for i in m['jobs'] if i['phase'] == 'SENTINEL']),
            ('MAIN_BLOCK_0', [i for i in m['jobs'] if i['phase'] == 'MAIN' and i['block'] == 0]),
            ('MAIN_BLOCK_1', [i for i in m['jobs'] if i['phase'] == 'MAIN' and i['block'] == 1])]
