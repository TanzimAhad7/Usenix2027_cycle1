from __future__ import annotations
import argparse,copy,json,traceback
from pathlib import Path
from .common import write,read,digest,ReplayMismatch
from .engine import Session,verify_source
from .mock_model import model as mock_model
from .protocol import manifest,root_specs

def compare_forks(left,right,out):
    a=read(left/'driver_records.json');b=read(right/'driver_records.json')
    def fresh(rows):return [r for r in rows if not r['reused']]
    x,y=fresh(a),fresh(b)
    first={}
    http_a=[read(p) for p in sorted((left/'http').glob('*.request.json'))]
    http_b=[read(p) for p in sorted((right/'http').glob('*.request.json'))]
    for role in ['actor','reference','attenuator','judge']:
        aa=next((r for r in http_a if r['role']==role),None);bb=next((r for r in http_b if r['role']==role),None)
        first[role]=dict(status='MATCH' if aa is not None and bb is not None and aa['body']==bb['body'] and aa.get('raw_utf8_body')==bb.get('raw_utf8_body') else 'NEITHER_REACHED' if aa is None and bb is None else 'DIFFERENT_OR_UNPAIRED',left_hash=digest(aa['body'] if aa else None),right_hash=digest(bb['body'] if bb else None),actual_http_bytes_equal=bool(aa and bb and aa.get('raw_utf8_body')==bb.get('raw_utf8_body')))
    divergence=None
    for i in range(max(len(x),len(y))):
        aa=(x[i]['role'],x[i]['request']) if i<len(x) else None;bb=(y[i]['role'],y[i]['request']) if i<len(y) else None
        if aa!=bb:divergence=dict(fresh_generation_index=i,left=aa,right=bb);break
    feedback_a=read(left/'common_feedback.json') if (left/'common_feedback.json').exists() else None
    feedback_b=read(right/'common_feedback.json') if (right/'common_feedback.json').exists() else None
    certificate=dict(first_effective_requests=first,first_divergence=divergence,common_feedback_equal=bool(feedback_a and feedback_b and feedback_a['body']==feedback_b['body']),hidden_state_equal=bool(feedback_a and feedback_b and feedback_a['hidden_state']==feedback_b['hidden_state']),all_future_inputs_equal=divergence is None,scope='Certificates cover actual reached requests. Equal first requests do not certify future paths; identical-input response differences are generation variability, not proof of a hidden-cause effect.')
    write(out,certificate);return certificate

def run_study(out,update=None,mock=False):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);frozen=manifest();write(out/'FROZEN_MANIFEST.json',frozen);write(out/'SOURCE_RUNTIME_IDENTITY.json',verify_source())
    census={r['id']:'SCHEDULED' for r in frozen['primary']+frozen['conditional']};write(out/'census.json',census)
    rows=[];candidate_dirs={};fixture=mock_model if mock else None
    def state(ident,value):
        census[ident]=value;write(out/'census.json',census)
        if update:update(ident,value,census)
    for item in frozen['primary']:
        ident=item['id'];state(ident,'RUNNING');directory=out/'autonomous'/ident
        try:
            session=Session(item,directory,mock=fixture);result=session.run();rows.append(result);state(ident,'RECORDED_'+result['lifecycle'])
            if result['lifecycle']=='INTERRUPTED':raise KeyboardInterrupt('Study interrupted; partial effects and result preserved')
            if item['policy']=='RELEASE':candidate_dirs[(item['root_id'],item['carrier'])]=directory
            print(f'{ident}: {result["outcome"]}; physical={result["physical_goal"]}; reporting={result["reporting_completion"]}; requests={result["http_attempts"]}',flush=True)
        except Exception as exc:
            write(directory/'initialization_error.json',dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()));state(ident,'TECHNICAL_INVALID_INITIALIZATION')
    for root in root_specs():
        chosen=None
        for carrier in ['C0','C1']:
            directory=candidate_dirs.get((root['id'],carrier))
            eligible=sorted((directory/'eligible').glob('*.json')) if directory else []
            if eligible:chosen=read(eligible[0]);break
        fork_items=[f for f in frozen['conditional'] if f['root_id']==root['id']]
        fork_ids=[f['id'] for f in fork_items]
        if not chosen:
            for ident in fork_ids:state(ident,'NO_ELIGIBLE_CHECKPOINT')
            write(out/'parent_selection'/f'{root["id"]}.json',dict(status='NO_ELIGIBLE_CHECKPOINT',rule=frozen['parent_rule'],replacement_allowed=False));continue
        write(out/'parent_selection'/f'{root["id"]}.json',dict(rule=frozen['parent_rule'],selected_checkpoint_hash=chosen['checkpoint']['snapshot_hash'],selected_item=chosen['checkpoint']['item']['id'],proposal_index=chosen['proposal_index']))
        item=copy.deepcopy(chosen['checkpoint']['item']);item['kind']='CHECKPOINT_QUALIFICATION'
        try:
            qualifier=Session(item,out/'restoration_qualification'/root['id'],mock=fixture,restore=chosen['checkpoint'],evidence=chosen['evidence'],stop_at_admission=True)
            qualified=qualifier.run()
            if qualified['lifecycle']=='INTERRUPTED':raise KeyboardInterrupt('Interrupted during checkpoint qualification')
            valid=qualified['lifecycle']=='QUALIFICATION_PAUSED' and qualifier.driver.replay_cursor==len(chosen['evidence'])
            valid=valid and digest(qualifier.world.env.model_dump(mode='json'))==digest(chosen['checkpoint']['world']['environment'])
            write(out/'restoration_qualification'/root['id']/'RESTORE_VERDICT.json',dict(qualified=valid,replayed_responses=qualifier.driver.replay_cursor,fresh_generation_attempts=qualifier.driver.http_count,scope='Unchanged native state + exact original request/response replay through source admission, before dispatch; not full future outcome identity'))
        except (Exception,ReplayMismatch) as exc:
            valid=False;write(out/'restoration_qualification'/root['id']/'RESTORE_VERDICT.json',dict(qualified=False,error=str(exc),traceback=traceback.format_exc()))
        if not valid:
            for ident in fork_ids:state(ident,'CHECKPOINT_RESTORATION_FAILED')
            continue
        fork_dirs={}
        for entry in fork_items:
            cause,ident=entry['cause'],entry['id']
            state(ident,'RUNNING');item=copy.deepcopy(chosen['checkpoint']['item']);item.update(id=ident,kind='CONDITIONAL_CONTINUATION')
            try:
                session=Session(item,out/'conditional'/ident,mock=fixture,restore=chosen['checkpoint'],evidence=chosen['evidence'],cause=cause)
                result=session.run();rows.append(result);fork_dirs[cause]=session.directory;state(ident,'RECORDED_'+result['lifecycle'])
                if result['lifecycle']=='INTERRUPTED':raise KeyboardInterrupt('Interrupted continuation; partial result preserved')
                print(f'{ident}: {result["outcome"]}; reused={result["reused_records"]}; fresh_requests={result["http_attempts"]}',flush=True)
            except (Exception,ReplayMismatch) as exc:
                write(out/'conditional'/ident/'initialization_error.json',dict(error=str(exc),traceback=traceback.format_exc()));state(ident,'TECHNICAL_INVALID_INITIALIZATION')
        if len(fork_dirs)==2:compare_forks(fork_dirs['GUARD'],fork_dirs['SERVICE'],out/'input_equivalence'/f'{root["id"]}.json')
    analyze(out)
    return census

def analyze(out):
    import csv
    out=Path(out);rows=[read(p) for base in ['autonomous','conditional'] for p in sorted((out/base).glob('*/result.json'))]
    mode=read(out/'status.json').get('mode') if (out/'status.json').exists() else None
    label='CPU_QUALIFICATION_ONLY_NO_MODEL_RUN' if mode=='CPU_ONLY' else 'MOCK_ENGINEERING_ONLY_ZERO_MODEL_INFERENCE' if mode=='MOCK' or rows and all(r['mock'] for r in rows) else 'NO_SCIENTIFIC_EPISODES_RECORDED' if not rows else 'DEVELOPMENT_RESULTS_INDEPENDENT_REVIEW_PENDING'
    summary=dict(status=label,counts_by_kind={},roots={},recorded_rows=len(rows),census=read(out/'census.json'))
    for row in rows:
        counts=summary['counts_by_kind'].setdefault(row['kind'],{});counts[row['outcome']]=counts.get(row['outcome'],0)+1
        summary['roots'].setdefault(row['root_id'],[]).append({k:row.get(k) for k in ['id','kind','carrier','policy','cause','outcome','violation','physical_goal','protocol_completion','reporting_completion','lifecycle','http_attempts','reused_records']})
    write(out/'analysis/SUMMARY.json',summary)
    with (out/'analysis/episode_ledger.csv').open('w') as f:
        fields=['id','kind','root_id','carrier','policy','cause','outcome','violation','physical_goal','protocol_completion','reporting_completion','lifecycle','http_attempts','reused_records','mock'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:r.get(k) for k in fields} for r in rows)
    lines=['# Native release study findings','',summary['status'],'','Counts below are authored workflow realizations and shared-parent continuations, not prevalence or stochastic reliability. Native-tool tasks are authored, not official benchmark task IDs.','']
    for root,records in summary['roots'].items():
        lines+=['## '+root,'','| Slot | Kind | Safety | Physical | Protocol | Reporting | Lifecycle |','|---|---|---|---|---|---|---|']
        for r in records:lines.append('| '+' | '.join(str(r.get(k)) for k in ['id','kind','outcome','physical_goal','protocol_completion','reporting_completion','lifecycle'])+' |')
        lines+=['']
    lines+=['## Interpretation boundaries','','A recorded forbidden commit remains a violation after an error. Reporting failure differs from under-execution. No eligible checkpoint is not a demonstrated safe recovery. Original source exact/fuzzy/skip and feedback remain in RELEASE; G is a privileged conventional comparator. Read every input-equivalence certificate before a guard-specific causal claim. Empty or failed transfer is evidence, not a reason to replace roots.','']
    (out/'analysis/FINDINGS.md').write_text('\n'.join(lines));return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--mock',action='store_true');p.add_argument('--analyze-only',action='store_true');a=p.parse_args()
    if a.analyze_only:analyze(a.out)
    else:run_study(a.out,mock=a.mock)
