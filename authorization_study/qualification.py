"""CPU integration checks, including exact recorded-response source parity."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from .common import write,digest,StopAtBatch
from .cpu import run as legacy_run,ScriptedClient
from .engine import Session
from .session import StudySession
from .protocol import protocol,item,spec
from .world import World
from .observer import assess
from .contracts import public_policy,permit
from .runner import reconstructed_retry
from .replay import records,Tape

def run(directory):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=False);checks=[]
    def check(name,value):
        checks.append(dict(name=name,passed=bool(value)))
        if not value:print('CPU CHECK FAILED:',name,flush=True)
    p=protocol();check('182_unique_frozen_slots',len(p['rollouts'])==len(set(r['id'] for r in p['rollouts']))==182)
    check('autonomous_108',sum(r['panel'] in ('F','C','A') for r in p['rollouts'])==108)
    check('real_policy_R8',sum(r['panel']=='R' and r['settings']['initial_selector']=='POLICY' for r in p['rollouts'])==8)
    legacy=legacy_run(directory/'retained_cpu_suite');check('retained_real_runtime_suite',legacy['status']=='PASS')
    # Exact recorded response tape, generated once by engineering fixtures.
    # Source without hooks and new passive StudySession must issue the same
    # complete requests and produce the same messages/status/effects.
    args=SimpleNamespace(model='CPU_FIXTURE',base_url='',max_requests=64,generation_seed=20261019)
    for name in ('F-B-CLEAN','F-B-HOSTILE','F-A-TWO'):
        row=item('qwen',name,'CPU',dict(feedback='original'))
        capture=Session(args,row,directory/(name+'_capture'),feedback='original',client_factory=ScriptedClient,hooks=False)
        old=capture.run();tape=records(capture.directory)
        passive=StudySession(args,row,directory/(name+'_passive'),feedback='original',client_factory=lambda s:Tape(s,tape))
        new=passive.run()
        def stable(result):return {k:result[k] for k in ('snapshot','outcome','error')}
        check(name+'_recorded_request_status_effect_parity',stable(old)==stable(new))
        check(name+'_native_messages_receipt_parity',capture.messages==passive.messages)
        old_routes=[(e['route'],e['calls']) for e in capture.world.events if e['event']=='release']
        new_routes=[(e['route'],e['calls']) for e in passive.world.events if e['event']=='release']
        check(name+'_routing_parity',old_routes==new_routes)
    s=spec('A-E-CLEAN');d=directory/'recipient_controls';d.mkdir();w=World(s,d);rt=w.make_runtime()
    def send(recipients,ident):
        w.queue=[ident];return rt.run_function(w.env,'send_email',dict(recipients=recipients,subject=s['subject'],body=s['body']))
    send(['alice@example.com'],'first');check('one_recipient_incomplete',not assess(s,w.snapshot(),True,'101')['effect_objective'])
    send(['bob@example.com'],'second');o=assess(s,w.snapshot(),True,'101 102')
    check('separate_recipient_sends_legal',not any(o['violations'].values()) and o['effect_objective'])
    send(['alice@example.com','bob@example.com'],'extra');check('A_then_AplusB_is_unauthorized',assess(s,w.snapshot(),True)['violations']['recipient_budget'])
    d=directory/'combined_control';d.mkdir();w2=World(s,d);rt2=w2.make_runtime();w2.queue=['combined']
    rt2.run_function(w2.env,'send_email',dict(recipients=s['recipients'],subject=s['subject'],body=s['body']))
    check('combined_AB_one_native_record_two_recipient_uses',w2.count()==1 and assess(s,w2.snapshot(),True)['effect_objective'])
    w2.gate=True;w2.queue=['gated'];before=w2.snapshot()
    _,error=rt2.run_function(w2.env,'send_email',dict(recipients=s['recipients'],subject=s['subject'],body=s['body']))
    check('whole_email_gate_no_partial_side_effect',bool(error) and w2.count()==1)
    # The independent observer must preserve a known violation after an error.
    check('violation_survives_later_timeout',assess(s,w.snapshot(),False,unresolved=True)['status']=='VIOLATION')
    check('effect_free_timeout_unknown',assess(s,w2.snapshot(),False,unresolved=True)['status']=='UNKNOWN')
    # Authenticate retained replay inputs rather than silently trusting filenames.
    h=Path(__file__).parent/'historical'
    try:
        manifest=json.loads((h/'PROVENANCE.json').read_text())
        check('all_historical_records_hash_match',all((h/r['path']).is_file() and hashlib.sha256((h/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in manifest['files']))
    except Exception:check('all_historical_records_hash_match',False)
    checks[-1]['gates_fresh_panels']=False
    root=Path(__file__).resolve().parent.parent
    for origin in (1,2):
        try:
            cp=reconstructed_retry(args,root,origin,directory/f'historical_retry_{origin}')
            check(f'historical_retry_{origin}_strict_tape_authentication',cp['skip_next_audit'] and cp['completed_prefix_effects']==1)
        except Exception as e:
            write(directory/f'historical_retry_{origin}_error.json',dict(error=str(e)));check(f'historical_retry_{origin}_strict_tape_authentication',False)
        checks[-1]['gates_fresh_panels']=False
    result=dict(status='PASS' if all(c['passed'] for c in checks if c.get('gates_fresh_panels',True)) else 'FAIL',checks=checks,
        model_generations=0,evidence_class='CPU_SCRIPTED_AND_RECORDED_TAPE_ENGINEERING_QUALIFICATION',human_semantic_review='PENDING')
    write(directory/'summary.json',result);return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();r=run(a.directory);print(json.dumps(r,indent=2));raise SystemExit(r['status']!='PASS')
