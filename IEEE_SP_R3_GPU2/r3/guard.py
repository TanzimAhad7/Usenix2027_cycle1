"""Source-preserving instrumentation and explicit resumable query initialization.

Only the declared error-aware all_empty predicate changes enforcement in B/D.
C/D's contract gate is external at the native runtime, not this source method.
"""
import ast,copy,sys,types
from .common import ROOT,CHECKER_SHA,sha,source_sig

def module_for(context):
    if str(ROOT/'vendor') not in sys.path:sys.path.insert(0,str(ROOT/'vendor'))
    path=ROOT/'vendor/AttriGuard.py'
    if sha(path)!=CHECKER_SHA:raise RuntimeError('Unexpected upstream source')
    tree=ast.parse(path.read_text());cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='AttriGuardExecutionLoop');query=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='query')
    def hook(k):return ast.Expr(ast.Call(ast.Name('_R3_HOOK',ast.Load()),[ast.Constant(k),ast.Call(ast.Name('locals',ast.Load()),[],[])],[]))
    # Resume state is assigned to actual locals; no mutation of frame.f_locals.
    restore='''_r3_start_iter = 0
if getattr(self, '_r3_resume', None) is not None:
    _r3_saved = self._r3_resume
    messages = _r3_saved['messages']
    extra_args = _r3_saved['extra_args']
    shadow_history = _r3_saved['shadow_history']
    shadow_index = _r3_saved['shadow_index']
    has_tool_observation = _r3_saved['has_tool_observation']
    skip_next_audit = _r3_saved['skip_next_audit']
    last_attenuated_external = _r3_saved['last_attenuated_external']
    _r3_start_iter = _r3_saved['iteration']
    self._last_judge_reason = _r3_saved['loop_state']['_last_judge_reason']
    self._last_attenuated_external = _r3_saved['loop_state']['_last_attenuated_external']
    self._last_defense_input = _r3_saved['loop_state']['_last_defense_input']
else:
    _sync_shadow()
'''
    sync=next(i for i,n in enumerate(query.body) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='_sync_shadow')
    query.body[sync:sync+1]=ast.parse(restore).body
    loop=next(n for n in query.body if isinstance(n,ast.For) and isinstance(n.iter,ast.Call) and isinstance(n.iter.func,ast.Name) and n.iter.func.id=='range')
    loop.iter.args.insert(0,ast.Name('_r3_start_iter',ast.Load()))
    body=[];seen={'proposal':0,'reference':0,'admission':0,'empty_predicates':0}
    for n in loop.body:
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Tuple) and any(isinstance(e,ast.Name) and e.id=='shadow_query' for e in t.elts) for t in n.targets):
            body.extend([hook('reference_start'),n,hook('reference_end')]);seen['reference']+=1;continue
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='shadow_sigs' for t in n.targets):body.append(hook('reference_ready'))
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='executed_results' for t in n.targets):body.append(hook('admission'));seen['admission']+=1
        body.append(n)
        if isinstance(n,ast.If) and isinstance(n.test,ast.UnaryOp) and isinstance(n.test.operand,ast.Name) and n.test.operand.id=='orig_calls':body.append(hook('proposal'));seen['proposal']+=1
    loop.body=body
    class ErrorAware(ast.NodeTransformer):
        def visit_Assign(self,n):
            if any(isinstance(t,ast.Name) and t.id=='all_empty' for t in n.targets):
                assert isinstance(n.value,ast.Call) and n.value.func.id=='all'
                gen=n.value.args[0]
                condition=ast.parse("not self._r3_ctx.setting['error_aware'] or not m.get('error')",mode='eval').body
                gen.elt=ast.BoolOp(ast.And(),[gen.elt,condition]);seen['empty_predicates']+=1
            return self.generic_visit(n)
    tree=ErrorAware().visit(tree);assert seen==dict(proposal=1,reference=1,admission=1,empty_predicates=3),seen
    mod=types.ModuleType('r3_instrumented_guard');mod.__dict__['_R3_HOOK']=context.hook
    exec(compile(ast.fix_missing_locations(tree),str(path),'exec'),mod.__dict__)
    return mod,ast.unparse(tree)+'\n',seen

def observe_loop(loop,context):
    loop._r3_ctx=context
    loop._r3_resume=None if context.resume is None else __import__('r3.common',fromlist=['unpack']).unpack(context.resume['monitor'])
    original=loop._fuzzy_survive
    def fuzzy(self,call,candidates,query,runtime,env):
        value=original(call,candidates,query,runtime,env)
        exact=any(source_sig(call)==source_sig(c) for c in candidates)
        route='EXACT' if exact else 'FUZZY' if any(call.function==c.function for c in candidates) else 'NO_SAME_FUNCTION_REJECTION'
        context.routes[source_sig(call)]=route
        context.event('survival',proposal=context.proposal,call=call,references=candidates,route=route,allowed=value,reason=self._last_judge_reason)
        return value
    loop._fuzzy_survive=types.MethodType(fuzzy,loop)
