"""Declared prompt/route changes; untouched source parser and logprob AST."""
import ast,difflib,importlib.util
from pathlib import Path
from reference_study.common import ROOT,read,write,sha
from e1.checker import DIRECT_PROMPT

def prompt_for(original,criterion):
 if criterion=='SOURCE':return original
 if criterion=='DIRECT':return DIRECT_PROMPT
 p=read(ROOT/'PROMPT_INTERVENTIONS.json')
 if criterion not in ('ATTENTION','ARGUMENT_EQUALITY'):raise ValueError(criterion)
 for old,new in zip((p['top_anchor'],p['rule_anchor']),p[criterion]):
  if original.count(old)!=1:raise RuntimeError('Prompt source-anchor drift')
  original=original.replace(old,new,1)
 return original

def parser_tail(source):
 node=next(n for n in ast.walk(ast.parse(source))if isinstance(n,ast.FunctionDef)and n.name=='_fuzzy_survive')
 start=next(i for i,n in enumerate(node.body)if isinstance(n,ast.Try))
 return [ast.dump(n,include_attributes=False)for n in node.body[start:]]

def variant(core,directory,criterion,forced_exact=False):
 directory=Path(directory);directory.mkdir(parents=True,exist_ok=True);original=Path(core.__file__).read_text();changed=original
 def replace(a,b):
  nonlocal changed
  if changed.count(a)!=1:raise RuntimeError('Source route-anchor drift')
  changed=changed.replace(a,b,1)
 if forced_exact or criterion=='DIRECT':replace('        if any(_call_signature(orig_call) == _call_signature(c) for c in candidates):\n            return True\n','')
 if criterion=='DIRECT':
  replace('        if not same_func_candidates:\n            return False\n','')
  replace('                "shadow_actions": [\n                    {"function": c.function, "arguments": c.args} for c in payload_candidates\n                ],\n','')
 if parser_tail(original)!=parser_tail(changed):raise RuntimeError('Source acquisition/parser tail changed')
 path=directory/'declared_checker.py';path.write_text(changed)
 spec=importlib.util.spec_from_file_location('e2b_checker_'+str(id(directory)),path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 before=module.FUZZY_SYSTEM_PROMPT;module.FUZZY_SYSTEM_PROMPT=prompt_for(before,criterion)
 (directory/'checker.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True),changed.splitlines(True),fromfile='source',tofile=criterion)))
 (directory/'prompt.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),module.FUZZY_SYSTEM_PROMPT.splitlines(True),fromfile='source_prompt',tofile=criterion)))
 write(directory/'checker_identity.json',dict(criterion=criterion,source_sha256=sha(core.__file__),variant_sha256=sha(path),parser_ast_equal=True,forced_exact_control=forced_exact,system_prompt=module.FUZZY_SYSTEM_PROMPT))
 return module
