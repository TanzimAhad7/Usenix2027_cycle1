"""Source-bound guard variants. Original vendor bytes are never edited."""
import copy
import difflib
import hashlib
import importlib.util
import json
import re


def parse_json(raw):
    """Allow one outer JSON Markdown fence, but no repair or substring verdict."""
    text=raw.strip();fenced=False
    match=re.fullmatch(r'```(?:json)?\s*\n?(.*?)\n?```',text,re.S)
    if match:text=match.group(1).strip();fenced=True
    def pairs(items):
        out={}
        for key,value in items:
            if key in out:raise ValueError('Duplicate JSON key: '+key)
            out[key]=value
        return out
    def constant(value):raise ValueError('Non-finite JSON value: '+value)
    return json.loads(text,object_pairs_hook=pairs,parse_constant=constant),fenced


def strict_verdict(raw):
    obj,fenced=parse_json(raw)
    if not isinstance(obj,dict) or set(obj)-{'survive','reason'}:raise ValueError('Judge must return survive/reason object')
    if type(obj.get('survive')) is not bool:raise ValueError('survive must be a JSON boolean')
    if not isinstance(obj.get('reason',''),str):raise ValueError('reason must be text')
    return obj['survive'],obj.get('reason',''),fenced


def canonical_signature(call):
    function=call.get('function') if isinstance(call,dict) else call.function
    args=dict(call.get('args',{}) if isinstance(call,dict) else call.args)
    if function=='pay':args.setdefault('key','')
    return function,json.dumps(args,sort_keys=True)


def maximum_matching(edges,nreferences):
    """Maximum-cardinality bipartite matching, with deterministic tie order."""
    owner={}
    def augment(actor,seen):
        for ref in edges[actor]:
            if ref<0 or ref>=nreferences:raise ValueError('Invalid reference index')
            if ref in seen:continue
            seen.add(ref)
            if ref not in owner or augment(owner[ref],seen):owner[ref]=actor;return True
        return False
    for actor in range(len(edges)):augment(actor,set())
    return {actor:ref for ref,actor in owner.items()}


def decide_capacity(module,loop,calls,references,query,runtime,env,world):
    # Idempotency is a property of our registered payment implementation,
    # verified against the trusted ledger, never a claim from model text.
    groups=[];group_for_key={};exempt=[]
    for call in calls:
        a=call.args;key=a.get('key','')
        identity=(a.get('recipient'),a.get('amount'))
        if call.function=='pay' and key and world.keys.get(key)==identity:
            exempt.append(call);continue
        sig=canonical_signature(call)
        grouping=('idempotent',key,sig) if call.function=='pay' and key else ('occurrence',call.id)
        if grouping not in group_for_key:group_for_key[grouping]=len(groups);groups.append([])
        groups[group_for_key[grouping]].append(call)
    edges=[];edge_reasons={}
    for i,group in enumerate(groups):
        candidate=group[0];allowed=[]
        for j,reference in enumerate(references):
            accepted=loop._fuzzy_survive(candidate,[reference],query,runtime,env)
            reason=loop._last_judge_reason
            world.event('reference_edge',actor_ids=[c.id for c in group],reference_id=reference.id,
                        accepted=bool(accepted),reason=reason,canonical_exact=canonical_signature(candidate)==canonical_signature(reference))
            if accepted:allowed.append(j);edge_reasons[(i,j)]=reason
        edges.append(allowed)
    assignment=maximum_matching(edges,len(references));released=[];blocked=[];reasons={}
    for call in exempt:
        released.append(call);reasons[call.id]='trusted_existing_idempotent_replay'
        world.event('reference_assignment',actor_id=call.id,reference_id=None,exemption='trusted_existing_idempotent_replay')
    for i,group in enumerate(groups):
        if i in assignment:
            ref=references[assignment[i]]
            for call in group:
                released.append(call);reasons[call.id]='capacity_witness:'+ref.id
                world.event('reference_assignment',actor_id=call.id,reference_id=ref.id,
                    allocation_unit='one_idempotent_effect' if len(group)>1 else 'one_occurrence',
                    reason=edge_reasons.get((i,assignment[i])))
        else:
            for call in group:blocked.append(call);reasons[call.id]='no_unconsumed_compatible_reference'
    # Preserve actor order in dispatch and feedback.
    allowed_ids={c.id for c in released}
    return [c for c in calls if c.id in allowed_ids],[c for c in calls if c.id not in allowed_ids],reasons


def load_guard(d,variant,directory,world):
    d.verify_runtime();original=(d.ROOT/'vendor/AttriGuard.py').read_text()
    assert hashlib.sha256((d.ROOT/'vendor/AttriGuard.py').read_bytes()).hexdigest()==d.SOURCE_HASH
    source=original
    if variant=='exact_counter':source=d.patched_source(source,'b_occurrence')
    if variant=='r_continuity':source=d.patched_source(source,'r_all_errors')
    # Repair per-occurrence feedback and flags, without using signature maps.
    old='''            executed_by_sig = {
                _call_signature(result["tool_call"]): result for result in executed_results
            }'''
    new='''            executed_by_id = {
                result["tool_call_id"]: result for result in executed_results
            }'''
    assert source.count(old)==1;source=source.replace(old,new)
    replacements={
      'call_reasons[_call_signature(call)] = reason':'call_reasons[call.id] = reason',
      'call_reasons.get(sig, "shadow_match(strict)" if sig in shadow_sigs else "shadow_block(strict)")':'call_reasons.get(call.id, "exact_signature" if sig in shadow_sigs else "source_decision")',
      '"flag": sig in {_call_signature(c) for c in blocked_calls}':'"flag": call.id in {c.id for c in blocked_calls}',
      'if sig in executed_by_sig:':'if call.id in executed_by_id:',
      'msg = executed_by_sig[sig]':'msg = copy.deepcopy(executed_by_id[call.id])',
    }
    for old,new in replacements.items():
        assert source.count(old)==1,(variant,old,source.count(old));source=source.replace(old,new)
    if variant!='baseline':
        start=source.index('        logprobs = extra.get("logprobs")')
        end=source.index('\n    def query(',start)
        source=source[:start]+'''        raw = ""
        for msg in reversed(out_messages):
            if msg.get("role") == "assistant":
                raw = _content_to_str(msg.get("content"))
                break
        return _expanded_strict(self, raw)
'''+source[end:]
    capacity=variant in ('reference_capacity','capacity_and_grant')
    if capacity:
        start=source.index('            executed_calls: list[FunctionCall] = []',source.index('            shadow_sigs ='))
        end=source.index('\n            if self.debug:',start)
        source=source[:start]+'''            executed_calls, blocked_calls, call_reasons = _expanded_decide(
                self, orig_calls, shadow_calls, query, runtime, env)
'''+source[end:]
    path=directory/f'guard_{variant}.py';path.write_text(source)
    (directory/f'{variant}.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True),source.splitlines(True),fromfile='source_original',tofile=variant)))
    spec=importlib.util.spec_from_file_location('expanded_guard_'+variant,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    if capacity:module._call_signature=canonical_signature
    def judge(loop,raw):
        try:
            survived,reason,fenced=strict_verdict(raw)
            world.event('judge_parse',status='VALID_FENCED_JSON' if fenced else 'VALID_JSON',survive=survived,reason=reason)
        except (ValueError,TypeError) as e:
            survived=False;reason='strict_judge_abstention:'+str(e)
            world.event('judge_parse',status='INVALID_ABSTAIN_BLOCK',survive=False,error=str(e),raw=raw)
        loop._last_judge_reason=reason;return survived
    module._expanded_strict=judge
    module._expanded_decide=lambda loop,calls,refs,query,runtime,env:decide_capacity(module,loop,calls,refs,query,runtime,env,world)
    original_fuzzy=module.AttriGuardExecutionLoop._fuzzy_survive
    def observed_fuzzy(loop,call,refs,query,runtime,env):
        loop._last_judge_reason=None
        exact=any(module._call_signature(call)==module._call_signature(r) for r in refs)
        decision=original_fuzzy(loop,call,refs,query,runtime,env)
        if loop._last_judge_reason is None:
            loop._last_judge_reason='exact_signature' if exact else 'legacy_fuzzy_result' if variant=='baseline' else 'no_matching_reference'
        world.event('guard_match_decision',actor_id=call.id,reference_ids=[r.id for r in refs],exact=exact,
                    survived=bool(decision),reason=loop._last_judge_reason)
        return decision
    module.AttriGuardExecutionLoop._fuzzy_survive=observed_fuzzy
    return module
