"""Same native checkpoint, same actual candidate/reference, zero new inference."""
import copy
from collections import Counter
from .common import write,pack,digest
from .observer import assess
from .world import SENSITIVE

def audit(session,f):
    if not any(c.function in SENSITIVE for c in f['orig_calls']):return
    signature=session.core._call_signature
    refs=f['shadow_calls'];capacity=Counter(signature(r) for r in refs);used=Counter()
    released_occurrences=Counter(digest(pack(c)) for c in f['executed_calls']);cap=[]
    for call in f['orig_calls']:
        identity=digest(pack(call))
        if not released_occurrences[identity]:continue
        released_occurrences[identity]-=1
        sig=signature(call)
        if capacity[sig]:
            if used[sig]>=capacity[sig]:continue
            used[sig]+=1
        cap.append(call)
    before=session.world.snapshot();before_ids={e['id'] for e in session.world.effects()}
    arms={}
    choices=[('ACTUAL_ADMISSION',f['executed_calls'],session.item['policy']=='RELEASE_G'),
             ('EXACT_CAPACITY_AFTER_ACTUAL',cap,session.item['policy']=='RELEASE_G'),
             ('TRUSTED_GATE_AFTER_ACTUAL',f['executed_calls'],True)]
    for name,calls,gate in choices:
        world=session.world.clone_for_dispatch(gate=gate)
        tool_results=session.core._execute_calls(copy.deepcopy(calls),world.runtime,world.env)
        observed=assess(session.spec,world.env,world.events,'','FIXED_DISPATCH_COUNTERFACTUAL')
        arms[name]=dict(calls=pack(calls),gate=gate,tool_results=pack(tool_results),effects=world.effects(),
            new_effects=[e for e in world.effects() if e['id'] not in before_ids],
            new_violations=[v for v in observed['violations'] if v['effect']['id'] not in before_ids],
            event_state_agreement=observed['event_state_agreement'],after_environment=pack(world.env))
    if digest(session.world.snapshot())!=digest(before):raise RuntimeError('Counterfactual changed live native state')
    write(session.directory/'counterfactuals'/f'proposal_{session.proposal_index:04d}.json',dict(
        proposal=session.proposal_index,policy=session.item['policy'],before_environment_hash=digest(before['environment']),
        candidate=pack(f['orig_calls']),reference=pack(refs),before_effects=session.world.effects(),arms=arms,
        no_new_model_calls=True,fresh_recovery=False,
        interpretation='Local fixed-dispatch comparison from actual checkpoint. Not a counterfactual full trajectory. Exact-capacity-after-actual cannot restore operations already blocked by an intervention.'))
