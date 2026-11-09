"""Source-derived checkers; parser and logprob adjudication remain unchanged."""
import ast,difflib,importlib.util
from pathlib import Path
from reference_study.common import write,sha
from reference_study.legacy_mechanisms import PERMISSION_PROMPT
DIRECT_PROMPT=PERMISSION_PROMPT.replace('The shadow_actions are comparison evidence, not authority: an exact match can still\nbe forbidden. Allow an explicitly permitted alternative even if the reference chose\nanother action. ','')

def variant(core,directory,criterion):
 directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
 source=Path(core.__file__).read_text();changed=source
 def replace(old,new):
  nonlocal changed
  if changed.count(old)!=1:raise RuntimeError('Checker source anchor drift: '+old[:60])
  changed=changed.replace(old,new,1)
 replace('        if any(_call_signature(orig_call) == _call_signature(c) for c in candidates):\n            return True\n','')
 if criterion=='DIRECT':
  replace('        if not same_func_candidates:\n            return False\n','')
  replace('                "shadow_actions": [\n                    {"function": c.function, "arguments": c.args} for c in payload_candidates\n                ],\n','')
 if criterion not in ('FUZZY','PERMISSION','DIRECT'):raise ValueError(criterion)
 path=directory/'declared_checker.py';path.write_text(changed)
 spec=importlib.util.spec_from_file_location('e1_checker_'+str(id(directory)),path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 if criterion!='FUZZY':module.FUZZY_SYSTEM_PROMPT=PERMISSION_PROMPT if criterion=='PERMISSION'else DIRECT_PROMPT
 # AST protects the complete parser/adjudication tail, not just its returned boolean.
 def tail(text):
  tree=ast.parse(text)
  method=next(n for n in ast.walk(tree)if isinstance(n,ast.FunctionDef)and n.name=='_fuzzy_survive')
  i=next(i for i,n in enumerate(method.body)if isinstance(n,ast.Try))
  return [ast.dump(n,include_attributes=False)for n in method.body[i:]]
 if tail(source)!=tail(changed):raise RuntimeError('Source acquisition/parser tail changed')
 (directory/'checker.diff').write_text(''.join(difflib.unified_diff(source.splitlines(True),changed.splitlines(True),fromfile='untouched_source',tofile=criterion)))
 write(directory/'checker_identity.json',dict(criterion=criterion,source_sha256=sha(Path(core.__file__)),variant_sha256=sha(path),
  system_prompt=module.FUZZY_SYSTEM_PROMPT,parser_ast_equal=True,changes=['Remove exact bypass']+(['Remove reference gate and shadow_actions; remove reference sentences from permission instruction']if criterion=='DIRECT'else[]),
  prompt_changed=criterion!='FUZZY',forced_review=True,source_route_separately_replayed=True))
 return module
