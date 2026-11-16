#!/usr/bin/env python3
"""Independent recomputation of the August benign sanitizer audit (study 07, "A15a"):
Gemini-2.5-Flash sanitizer outputs on tool results flagged at 26 benign privileged decisions.
Fresh code; token-level diff instead of substring checks.  Output -> audit_a15a.json"""
import json, re, difflib, collections, hashlib
from pathlib import Path
A = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/research_basis/studies/07_causalarmor/activation_audit')
dec = [json.loads(l) for l in open(A/'decision_inventory.jsonl')]
jobs = {j['job_id']: j for j in map(json.loads, open(A/'sanitizer_jobs.jsonl'))}
res = [json.loads(l) for l in open(A/'sanitizer_results.jsonl')]
D = {d['decision_id']: d for d in dec}
tok = lambda s: re.findall(r"[A-Za-z0-9@._+\-:/']+", s)
out = {'decisions_in_inventory': len(dec), 'decisions_flagged': sum(d['ca_flag_tau0'] for d in dec),
       'by_label': {l: f"{sum(d['ca_flag_tau0'] for d in dec if d['label']==l)}/{sum(1 for d in dec if d['label']==l)}" for l in sorted({d['label'] for d in dec})},
       'eligible_spans': sum(d['n_eligible_tool_spans'] for d in dec), 'flagged_spans': sum(d['n_flagged_spans_tau0'] for d in dec),
       'sanitizer_results': len(res), 'errors': sum(1 for r in res if r['error']), 'models': dict(collections.Counter(r['provider_model_returned'] for r in res)),
       'hash_recheck_failures': 0, 'identical': 0, 'edited': []}
per = collections.defaultdict(list)
for r in res:
    j = jobs[r['job_id']]; o = j['untrusted_content']; s = r['sanitized_text'] or ''
    if hashlib.sha256(o.encode()).hexdigest() != r['untrusted_content_sha256'] or hashlib.sha256(s.encode()).hexdigest() != r['sanitized_text_sha256']:
        out['hash_recheck_failures'] += 1
    per[r['decision_id']].append((o, s, j))
    if o == s: out['identical'] += 1; continue
    to, ts = tok(o), tok(s); sm = difflib.SequenceMatcher(None, to, ts, autojunk=False)
    removed = [' '.join(to[i1:i2]) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag in ('delete', 'replace')]
    added = [' '.join(ts[j1:j2]) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag in ('insert', 'replace')]
    out['edited'].append({'job': r['job_id'], 'label': j['label'], 'user_request': j['user_request'][:200], 'chars_in': len(o), 'chars_out': len(s),
                          'removed_segments': removed[:12], 'added_segments': added[:6],
                          'actual_call': D[r['decision_id']]['actual_call'], 'original_head': o[:300], 'sanitized_head': s[:300]})
# value retention at decision level, counting every argument leaf (incl. short ones)
def leaves(x):
    if isinstance(x, dict):
        for v in x.values(): yield from leaves(v)
    elif isinstance(x, list):
        for v in x: yield from leaves(v)
    elif x is not None and str(x) != '': yield str(x)
ret = []
for did, L in per.items():
    d = D[did]; ureq = L[0][2]['user_request']
    for v in sorted(set(leaves(d['actual_call']['args']))):
        if len(v) > 80: continue                        # long free text is composed by the agent, not copied
        inU = v.lower() in ureq.lower(); inO = any(v in o for o, _, _ in L); inS = any(v in s for _, s, _ in L)
        ret.append({'decision': did, 'value': v, 'in_user_request': inU, 'in_flagged_original': inO, 'in_sanitized': inS})
tool_only = [x for x in ret if x['in_flagged_original'] and not x['in_user_request']]
out['argument_values_present_only_in_flagged_tool_text'] = len(tool_only)
out['of_those_missing_after_sanitization'] = [x for x in tool_only if not x['in_sanitized']]
out['decisions_with_such_a_value'] = len({x['decision'] for x in tool_only})
out['values_also_in_user_request_lost_from_tool_text'] = [x for x in ret if x['in_flagged_original'] and x['in_user_request'] and not x['in_sanitized']]
json.dump(out, open(Path(__file__).with_name('audit_a15a.json'), 'w'), indent=1)
print({k: v for k, v in out.items() if k != 'edited'})
for e in out['edited']:
    print('--', e['job'], e['label'], e['chars_in'], '->', e['chars_out']); print('   request:', e['user_request'][:150]); print('   removed:', [x[:110] for x in e['removed_segments'][:6]]); print('   added:', [x[:80] for x in e['added_segments'][:3]])
