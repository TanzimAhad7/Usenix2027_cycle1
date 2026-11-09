"""Only the declared route edit; original acquisition/parser retained."""
import difflib
import importlib.util
from pathlib import Path
from a01.checker import prompt_for
from e2b.checker import parser_tail
from reference_study.common import ROOT, sha, write


def variant(core, directory, criterion, diagnostic=True):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    source = Path(core.__file__).read_text()
    changed = source
    anchor = '        if not same_func_candidates:\n            return False\n'
    if diagnostic:
        if source.count(anchor) != 1:
            raise RuntimeError('No-reference route anchor drift')
        changed = source.replace(anchor, '', 1)
    if parser_tail(source) != parser_tail(changed):
        raise RuntimeError('Source acquisition/parser AST changed')
    path = directory / 'declared_checker.py'
    path.write_text(changed)
    spec = importlib.util.spec_from_file_location('j1_checker_' + str(id(directory)), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original_prompt = module.FUZZY_SYSTEM_PROMPT
    module.FUZZY_SYSTEM_PROMPT = prompt_for(original_prompt, criterion)
    frozen = (ROOT / 'design' / (criterion + '_SYSTEM_PROMPT.txt')).read_text()
    if module.FUZZY_SYSTEM_PROMPT != frozen:
        raise RuntimeError('Policy differs from frozen A1 construction')
    for label, before, after in [('checker', source, changed),
                                 ('prompt', original_prompt, module.FUZZY_SYSTEM_PROMPT)]:
        (directory / (label + '.diff')).write_text(''.join(difflib.unified_diff(
            before.splitlines(True), after.splitlines(True), fromfile='source', tofile=criterion)))
    write(directory / 'checker_identity.json', dict(
        source_sha256=sha(core.__file__), variant_sha256=sha(path),
        criterion=criterion, diagnostic_no_reference_route=diagnostic,
        acquisition_parser_ast_equal=True, exact_bypass_preserved=True,
        system_prompt=module.FUZZY_SYSTEM_PROMPT,
        scope='Counterfactual NONE invocation; nonempty arms retain original route under the declared policy.'))
    return module
