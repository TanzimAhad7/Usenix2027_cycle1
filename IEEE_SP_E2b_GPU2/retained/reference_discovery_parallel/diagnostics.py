"""Preserve paths before interpreting them; never infer attack causality here."""
import json
from collections import Counter
from .common import read,write,digest

def signature(call):return (call.get('function'),json.dumps(call.get('args',{}),sort_keys=True))

def diagnose(out,destination=None):
    destination=destination or out/'analysis'
    admissions=[];effects=[];counterfactuals=[];disagreements=[];request_counts=Counter();tokens=Counter()
    feedback_paths=[];error_planes=Counter();error_mismatches=[]
    for directory in sorted((out/'workflows').glob('*')) if (out/'workflows').exists() else []:
        if not (directory/'result.json').exists():continue
        result=read(directory/'result.json');eventfile=directory/'events.jsonl'
        events=[json.loads(s) for s in eventfile.read_text().splitlines()] if eventfile.exists() else []
        bad={v['effect']['id'] for v in result.get('violations',[])}
        exposure_index=next((e['event_index'] for e in events if e['kind']=='generation_transport_response' and e.get('role')=='actor' and e.get('carrier_marker_in_request') and 200<=e.get('status',0)<300),None)
        proposal_indices={e['proposal_index']:e['event_index'] for e in events if e['kind']=='proposal'}
        for event in events:
            if event['kind']=='admission':
                references=Counter(signature(c) for c in event['reference_calls']);released=Counter(signature(c) for c in event['released'])
                admissions.append(dict(workflow=directory.name,policy=result.get('policy'),proposal=event['proposal_index'],
                    actor_calls=event['actor_calls'],reference_calls=event['reference_calls'],released=event['released'],blocked=event['blocked'],
                    exact_support=[dict(signature=list(sig),reference_occurrences=n,released_occurrences=released[sig],
                        support_reused=released[sig]>n) for sig,n in references.items()]))
            if event['kind']=='commit':
                occurrence=event.get('occurrence') or {};proposal_event=proposal_indices.get(occurrence.get('proposal'))
                effects.append(dict(workflow=directory.name,policy=result.get('policy'),event_index=event['event_index'],
                    effect=event['effect'],occurrence=event.get('occurrence'),violating_effect=event['effect']['id'] in bad,
                    first_accepted_actor_carrier_event=exposure_index,proposal_event_index=proposal_event,
                    carrier_exposed_before_proposal=exposure_index is not None and proposal_event is not None and exposure_index<proposal_event,
                    carrier=result.get('carrier'),caution='Temporal precedence is required but is not by itself proof that the carrier caused the proposal.'))
        for p in sorted((directory/'counterfactuals').glob('*.json')):
            certificate=read(p);actual=certificate['arms']['ACTUAL_ADMISSION'];proposal=certificate['proposal']
            committed=[e['effect'] for e in events if e['kind']=='commit' and (e.get('occurrence') or {}).get('proposal')==proposal]
            agreement=actual['new_effects']==committed
            if not agreement:disagreements.append(dict(workflow=directory.name,proposal=proposal,actual=committed,replay=actual['new_effects']))
            counterfactuals.append(dict(workflow=directory.name,proposal=proposal,policy=result.get('policy'),
                replay_effect_agreement=agreement,before_environment_hash=certificate['before_environment_hash'],
                arms={k:dict(new_effects=len(v['new_effects']),new_violations=len(v['new_violations']),event_state_agreement=v['event_state_agreement']) for k,v in certificate['arms'].items()}))
        records=read(directory/'driver_records.json') if (directory/'driver_records.json').exists() else []
        history=read(directory/'messages.json') if (directory/'messages.json').exists() else []
        feedback=[m for m in history if m.get('role')=='tool']
        wire_tools=[m for row in records if row.get('role')=='actor' and row.get('response') for m in row['request'].get('messages',[]) if m.get('role')=='tool']
        native_errors=sum(e['kind']=='tool_result' and bool(e.get('error')) for e in events)
        feedback_errors=[m for m in feedback if m.get('error')]
        blocked_errors=[m for m in feedback_errors if str(m['error']).startswith('[AttriGuardBlocked]')]
        non_guard_errors=len(feedback_errors)-len(blocked_errors)
        verified=0
        for m in feedback_errors:
            call_id=(m.get('tool_call') or {}).get('id')
            for wire in wire_tools:
                content=wire.get('content','')
                if isinstance(content,list):content='\n'.join(str(x.get('text',x.get('content',''))) for x in content if isinstance(x,dict))
                if wire.get('tool_call_id')==call_id and str(m['error']) in str(content):verified+=1;break
        error_planes.update(native_runtime_errors=native_errors,tool_feedback_error_fields=len(feedback_errors),source_guard_block_feedback=len(blocked_errors),non_guard_feedback_error_fields=non_guard_errors,feedback_errors_verified_in_actor_wire=verified)
        if native_errors!=non_guard_errors:error_mismatches.append(dict(workflow=directory.name,native_runtime_errors=native_errors,non_guard_feedback_error_fields=non_guard_errors,source_guard_block_feedback=len(blocked_errors),verified_actor_wire_errors=verified))
        feedback_paths.append(dict(workflow=directory.name,feedback=feedback,native_runtime_errors=native_errors,feedback_errors=len(feedback_errors),source_guard_block_feedback=len(blocked_errors),non_guard_feedback_error_fields=non_guard_errors,verified_actor_wire_errors=verified))
        for row in records:
            role=row['role'];request_counts[role]+=1
            tokens[role]+=row.get('response',{}).get('usage',{}).get('completion_tokens',0)
    summary=dict(reviewed_proposals=len(admissions),committed_records=len(effects),
        source_or_comparator_exact_support_reuse_proposals=sum(any(s['support_reused'] for s in a['exact_support']) for a in admissions),
        counterfactuals=len(counterfactuals),dispatch_replay_disagreements=disagreements,
        role_request_counts=dict(request_counts),completion_tokens=dict(tokens),
        error_planes=dict(error_planes),error_plane_mismatches=error_mismatches,
        caution='Support reuse is not automatically an exploit. A fresh reference can itself be excessive. Unreviewed proposals have no reference certificate. Local replays have no fresh continuation. Guard-block feedback is distinct from native execution failure; residual error-count differences can include pre-dispatch/schema errors and require inspection.')
    write(destination/'admission_paths.json',admissions);write(destination/'effect_paths.json',effects)
    write(destination/'checkpoint_comparisons.json',counterfactuals);write(destination/'tool_feedback_paths.json',feedback_paths);write(destination/'diagnostics.json',summary)
    return summary
