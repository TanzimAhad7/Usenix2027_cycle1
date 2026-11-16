#!/usr/bin/env python3
"""Read-only mining of the August 2026 CausalArmor-style live reconstruction (P0B3) and the
A15a benign sanitizer audit, both shipped in the rejected paper's artifact.
Models in those runs: Gemini-2.5-Flash agent + sanitizer (OpenRouter), Gemma-3-12B proxy.
Nothing is modified; output -> p0b3_mining.json"""
import json, collections, re, sys
from pathlib import Path
R = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/research_basis/studies/07_causalarmor')
rows = [json.loads(l) for l in open(R/'reconstruction_results/P0B3_SCIENCE_ROWS.jsonl')]
evs  = [json.loads(l) for l in open(R/'reconstruction_results/P0B3_DEFENSE_EVENTS.jsonl')]
byep = collections.defaultdict(list)
for e in evs: byep[e['episode_id']].append(e)
out = {}
def norm(c):
    m = re.match(r'^(\w+)\((.*)\)$', c, re.S)
    if not m: return c
    try: return m.group(1)+'('+json.dumps(json.loads(m.group(2)), sort_keys=True)+')'
    except Exception: return c
def cls(e):
    o=[norm(x) for x in e['original_proposal']['tool_calls']]; r=[norm(x) for x in e['regenerated_proposal']['tool_calls']]
    if o==r: return 'same'
    of=[x.split('(')[0] for x in o]; rf=[x.split('(')[0] for x in r]
    if not r: return 'dropped_all_calls'
    if of==rf: return 'same_functions_args_changed'
    return 'functions_changed'
for kind in ('benign','attack'):
    rk=[r for r in rows if (r['kind']=='benign')==(kind=='benign')]
    ek=[e for e in evs if e['episode_id'].startswith('benign:')==(kind=='benign')]
    d={'episodes':len(rk),'status':dict(collections.Counter(r['status'] for r in rk)),
       'utility_true':sum(1 for r in rk if r['utility'] is True),
       'privileged_decision_events':len(ek),
       'episodes_with_event':len({e['episode_id'] for e in ek}),
       'flagged_events':sum(e['primary_any_flag'] for e in ek),
       'intervened_events':sum(e['intervened'] for e in ek)}
    san=[s for e in ek for s in e['sanitizers']]
    d['sanitizer_calls']=len(san)
    d['sanitizer_output_identical_to_input']=sum(s['input_sha256']==s['output_sha256'] for s in san)
    iv=[e for e in ek if e['intervened']]
    d['regeneration_class']=dict(collections.Counter(cls(e) for e in iv))
    # events where every sanitizer call returned its input unchanged, yet the action changed
    d['changed_despite_all_sanitizers_identical']=sum(1 for e in iv if cls(e)!='same' and all(s['input_sha256']==s['output_sha256'] for s in e['sanitizers']))
    d['changed_with_some_sanitizer_edit']=sum(1 for e in iv if cls(e)!='same' and any(s['input_sha256']!=s['output_sha256'] for s in e['sanitizers']))
    d['same_with_some_sanitizer_edit']=sum(1 for e in iv if cls(e)=='same' and any(s['input_sha256']!=s['output_sha256'] for s in e['sanitizers']))
    # episode level
    U={r['episode_id']:r for r in rk}
    tab=collections.Counter()
    for r in rk:
        es=byep.get(r['episode_id'],[])
        g='no_privileged_decision' if not es else ('no_intervention' if not any(e['intervened'] for e in es) else ('intervened_action_unchanged' if all(cls(e)=='same' for e in es if e['intervened']) else 'intervened_action_changed'))
        tab[(g, r['utility'], r.get('attack_success'))]+=1
    d['episode_table(group,utility,attack_success)']={str(k):v for k,v in sorted(tab.items(),key=str)}
    out[kind]=d
# dossier of every benign intervened event whose action changed
dos=[]
for e in evs:
    if e['episode_id'].startswith('benign:') and e['intervened'] and cls(e)!='same':
        dos.append({'episode':e['episode_id'],'decision_index':e['decision_index'],'class':cls(e),
          'original':e['original_proposal'],'regenerated':e['regenerated_proposal'],
          'flagged_tools':[s['tool_name'] for s in e['sanitizers']],
          'sanitizer_identical':[s['input_sha256']==s['output_sha256'] for s in e['sanitizers']],
          'episode_utility':next(r['utility'] for r in rows if r['episode_id']==e['episode_id'])})
out['benign_changed_dossiers']=dos
# A15a benign sanitizer audit (sanitized text stored)
A=R/'activation_audit'
dec={json.loads(l)['decision_id']:json.loads(l) for l in open(A/'decision_inventory.jsonl')}
jobs={json.loads(l)['job_id']:json.loads(l) for l in open(A/'sanitizer_jobs.jsonl')}
res=[json.loads(l) for l in open(A/'sanitizer_results.jsonl')]
def vals(args):
    v=[]
    def walk(x):
        if isinstance(x,dict): [walk(y) for y in x.values()]
        elif isinstance(x,list): [walk(y) for y in x]
        elif x is not None and str(x)!='': v.append(str(x))
    walk(args); return v
a={'calls':len(res),'identical':0,'char_ratio':[],'per_decision':[]}
perdec=collections.defaultdict(list)
for r in res:
    j=jobs[r['job_id']]; o=j['untrusted_content']; s=r['sanitized_text'] or ''
    a['identical']+= (o==s); a['char_ratio'].append(round(len(s)/max(1,len(o)),3))
    perdec[r['decision_id']].append((o,s,j))
lost_dec=0; dec_with_tool_value=0
for did,L in perdec.items():
    d=dec[did]; V=[v for v in vals(d['actual_call']['args']) if len(v)>=3]
    ureq=L[0][2]['user_request']
    item={'decision':did,'label':d['label'],'spans':len(L),'identical_spans':sum(o==s for o,s,_ in L),'values':[]}
    for v in V:
        in_user = v in ureq
        in_orig = any(v in o for o,_,_ in L)
        in_san  = any(v in s for _,s,_ in L)
        item['values'].append({'value':v[:60],'in_user_request':in_user,'in_flagged_original':in_orig,'in_sanitized':in_san})
    tv=[x for x in item['values'] if x['in_flagged_original'] and not x['in_user_request']]
    if tv:
        dec_with_tool_value+=1
        if any(not x['in_sanitized'] for x in tv): lost_dec+=1; item['LOSS']=True
    a['per_decision'].append(item)
a['decisions']=len(perdec); a['decisions_with_tool_only_arg_value_in_flagged_span']=dec_with_tool_value
a['decisions_losing_such_a_value_after_sanitization']=lost_dec
a['char_ratio_min']=min(a['char_ratio']); a['spans_with_ratio_below_0.9']=sum(x<0.9 for x in a['char_ratio'])
out['A15a']=a
json.dump(out,open(Path(__file__).with_name('p0b3_mining.json'),'w'),indent=1)
for k in ('benign','attack'): print(k, json.dumps(out[k],indent=1))
b=dict(a); b.pop('per_decision'); b.pop('char_ratio'); print('A15a',json.dumps(b,indent=1))
print('changed benign dossiers:',len(dos))
