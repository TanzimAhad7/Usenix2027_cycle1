"""Fresh recovery from authentic, outcome-blind selected denial checkpoints.

No scripted actor proposals, no invented successful prefixes, no replacement
search when an eligible checkpoint is absent. These are conditional continuations,
never additional autonomous attack roots.
"""
import copy,time,traceback
from collections import Counter
from .common import write,read,unseal,digest
from .gate import key
from .engine import Session
from .budget import CampaignBudgetStop

def eligibility(item,candidate):
    cp=unseal(candidate['checkpoint']);spec=cp['spec']
    if item['policy']!='RELEASE' or spec['shape'] not in ('CONTINUATION','STAGED'):
        return False,'Not a source-policy continuation/staged origin'
    if spec['family'] not in ('DM','EMAIL','BANK') or spec['carrier_condition'] not in ('NEUTRAL','COUNT'):
        return False,'Not a declared primary recovery stratum'
    limits=Counter(key(o['function'],o['args']) for o in spec['obligations'])
    # Extract native state with a reconstruction, without executing any call.
    from .world import World
    world=World(spec,restore=cp['world']);effects=world.effects()
    spent=Counter(key(e['function'],e['args']) for e in effects)
    if not effects or any(n>limits[k] for k,n in spent.items()):return False,'Prefix missing or already outside contract'
    for call in cp['pending']:
        k=key(call['function'],call['args'])
        if spent[k]>=limits[k]:return False,'Denied batch is not fully permitted by remaining contract'
        spent[k]+=1
    return True,'Safe real prefix and fully denied sensitive batch within remaining trusted contract'

def choose(item,session,selected,out):
    if item['allocation_phase']!='CORE' or item['policy']!='RELEASE':return
    stratum=(item['spec']['family'],item['spec']['carrier_condition'])
    if stratum in selected:return
    for candidate in session.eligible:
        cp=unseal(candidate['checkpoint'])
        prefix=session.driver.records[:cp['driver_index']+len(candidate['evidence'])]
        def unhandled_failure(r):
            error=r.get('exception') or {};message=str(error.get('message','')).lower()
            supported=error.get('type')=='BadRequestError' and 'logprobs' in message and 'unsupported' in message
            return bool(error) and not supported
        if any(r.get('truncated') or unhandled_failure(r) for r in prefix):continue
        valid,reason=eligibility(item,candidate)
        if valid:
            selected[stratum]=dict(parent_id=item['id'],item=copy.deepcopy(item),candidate=copy.deepcopy(candidate),reason=reason,
                selection='First eligible checkpoint in frozen CORE workflow/proposal order. Final parent outcome not used.')
            write(out/'matched_origins'/('_'.join(stratum)+'.json'),selected[stratum]);break

def compare_inputs(a,b):
    ar=read(a/'driver_records.json') if (a/'driver_records.json').exists() else []
    br=read(b/'driver_records.json') if (b/'driver_records.json').exists() else []
    ar=[r for r in ar if not r.get('reused')];br=[r for r in br if not r.get('reused')]
    actors_a=[r for r in ar if r['role']=='actor'];actors_b=[r for r in br if r['role']=='actor']
    first_actor=dict(reached_both=bool(actors_a and actors_b),equal=None,accepted_both=False)
    if actors_a and actors_b:
        first_actor.update(equal=actors_a[0]['request']==actors_b[0]['request'],
            accepted_both='response' in actors_a[0] and 'response' in actors_b[0],
            left_hash=digest(actors_a[0]['request']),right_hash=digest(actors_b[0]['request']))
    role_inputs={}
    for role in ['actor','reference','attenuator','judge']:
        x=next((r for r in ar if r['role']==role),None);y=next((r for r in br if r['role']==role),None)
        role_inputs[role]=dict(reached_left=x is not None,reached_right=y is not None,
            equal=(x['request']==y['request']) if x and y else None,
            accepted_both=bool(x and y and 'response' in x and 'response' in y))
    rows=[]
    for i in range(max(len(ar),len(br))):
        x=ar[i] if i<len(ar) else None;y=br[i] if i<len(br) else None
        same=bool(x and y and x['role']==y['role'] and x['request']==y['request'])
        rows.append(dict(fresh_index=i,left_role=x['role'] if x else None,right_role=y['role'] if y else None,
            input_equal=same,left_input_hash=digest(x['request']) if x else None,right_input_hash=digest(y['request']) if y else None))
        if not same:break
    return dict(first_fresh_actor=first_actor,first_fresh_inputs_by_role=role_inputs,effective_request_prefix=rows,
        first_divergence=next((r for r in rows if not r['input_equal']),None),left_fresh_requests=len(ar),right_fresh_requests=len(br),
        scope='Actual recorded driver inputs, whose wire equality is checked during transport. No ID normalization. Unreached roles are not certified. Equality of inputs is not equality of sampled outputs or whole trajectories.')

def choose_from_disk(item,selected,out):
    """Called in frozen order only after the entire CORE phase has drained."""
    from types import SimpleNamespace
    directory=out/'workflows'/item['id']
    candidates=[read(p) for p in sorted((directory/'eligible').glob('*.json'))]
    if not candidates:return
    records=directory/'driver_records.json'
    if not records.exists():
        write(directory/'recovery_selection_error.json',dict(error='Decision records missing; checkpoint is not qualified'))
        return
    choose(item,SimpleNamespace(eligible=candidates,driver=SimpleNamespace(records=read(records))),selected,out)

def unexposed(item,out):
    directory=out/'forks'/item['id'];directory.mkdir(parents=True,exist_ok=False)
    result=dict(id=item['id'],status='NO_ELIGIBLE_CHECKPOINT',outcome='UNEXPOSED_CONDITIONAL_INTERVENTION',qualified=False,violation=False,
        evidence_class='NOT_EXECUTED_NOT_SAFE_COMPLETION',family=item['family'],carrier=item['carrier'],arm=item['arm'])
    write(directory/'result.json',result);return result

def execute_fork(item,origin,out,mock=False,deadline=None):
    """Same authenticated intervention, executed in an isolated worker."""
    from .mock_model import model
    ident=item['id'];directory=out/'forks'/ident;started=time.monotonic()
    if deadline is not None and time.monotonic()>=deadline:raise CampaignBudgetStop('Optional collection limit reached')
    arm=item['arm'];cause='SERVICE' if arm.startswith('SERVICE_') else 'GUARD';feedback=arm.split('_',1)[1]
    candidate=origin['candidate'];checkpoint=candidate['checkpoint']
    try:
        scenario=copy.deepcopy(origin['item']);scenario.update(id=ident,kind='CONDITIONAL_AUTHENTIC_RECOVERY',policy='RELEASE')
        session=Session(scenario,directory,mock=model if mock else None,restore=checkpoint,evidence=candidate['evidence'],cause=cause,feedback_mode=feedback)
        # Session has already authenticated and exactly restored the checkpoint.
        # A second normal model_validate would reset the live Inbox again.
        before_ids={e['id'] for e in session.world.effects()}
        result=session.run();fresh=[e for e in result['effects'] if e['id'] not in before_ids]
        result.update(parent_id=origin['parent_id'],arm=arm,feedback_mode=feedback,evidence_class='CONDITIONAL_CONTINUATION_NOT_AUTONOMOUS_ROOT',
            inherited_effects=len(before_ids),new_effects=fresh,initial_source_decision_reused=True)
        write(directory/'result.json',result)
    except (KeyboardInterrupt,CampaignBudgetStop):raise
    except BaseException as exc:
        directory.mkdir(parents=True,exist_ok=True)
        result=dict(id=ident,status='CONDITIONAL_CONSTRUCTION_FAILED',outcome='UNKNOWN_TECHNICAL',qualified=False,violation=False,
            evidence_class='UNRESOLVED_CONDITIONAL_CONTINUATION',parent_id=origin['parent_id'],arm=arm,
            error=dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()),elapsed_seconds=time.monotonic()-started)
        write(directory/'result.json',result)
    return result

def certificates(out,selected):
    rows=[]
    for family,carrier in sorted(selected):
        for feedback in ['NEUTRAL','COMMIT_AWARE']:
            a=out/'forks'/f'RECOVERY_{family}_{carrier}_GUARD_{feedback}'
            b=out/'forks'/f'RECOVERY_{family}_{carrier}_SERVICE_{feedback}'
            rows.append(dict(family=family,carrier=carrier,feedback=feedback,**compare_inputs(a,b)))
    write(out/'matched_input_certificates.json',rows)

def run(out,frozen,selected,progress,mock=False,deadline=None):
    """Serial engineering compatibility entry; scientific scheduler uses workers."""
    for item in frozen['forks']:
        origin=selected.get((item['family'],item['carrier']))
        if origin is None:result=unexposed(item,out)
        else:
            progress('fork',item['id'],'RUNNING')
            result=execute_fork(item,origin,out,mock=mock,deadline=deadline)
        progress('fork',item['id'],result.get('lifecycle',result.get('status','RECORDED')))
        if result.get('lifecycle')=='INTERRUPTED':raise KeyboardInterrupt('Interrupted conditional evidence preserved')
    certificates(out,selected)
