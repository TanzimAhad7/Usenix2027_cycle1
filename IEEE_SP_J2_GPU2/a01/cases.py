"""Source-supported local acquisition and independent effect accounting."""
import copy
from pathlib import Path
from reference_study.common import read, write, digest
from e1.cases import RecordPolicy, Replay, world_for
from e2b.cases import observed_call
from e2b.terminal import inspect as terminal_inspect
from .design import inputs, key_for, permitted
from .checker import variant

def world_for_item(item):
    if item['stage'] == 'A0':
        from e2b.design import native_spec
        return world_for(native_spec())
    from .simulation import World
    return World()

def run(item, directory, family, mock=False, frozen=None):
    from permission_admission.runtime import fixed_driver
    from reference_discovery_parallel.base.source import load_source
    from reference_discovery_parallel.base.transport import reply
    from agentdojo.functions_runtime import FunctionCall
    from e2b.measure import dispatch as bank_dispatch
    from .simulation import dispatch as custom_dispatch
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    if key_for(item) != item['input_key']:
        raise RuntimeError('Frozen logical input differs')
    core, _ = load_source()
    task, candidate, references, allowed = inputs(item)
    world = world_for_item(item)
    before = world.snapshot()
    write(directory / 'held_input.json', dict(task=task, candidate=candidate, references=references,
        allowed_operations=allowed, initial_state=before, initial_state_hash=digest(before),
        effect_scope='AgentDojo-native banking' if item['stage'] == 'A0' else 'Custom effectful simulator',
        input_key=item['input_key'], semantic_human_review='PENDING'))
    driver = fixed_driver(directory / 'model_io', mock)
    if mock:
        driver.mock = lambda role, body: reply('{"survive":' + str(permitted(item)).lower() + ',"reason":"ENGINEERING MOCK ONLY"}')
    if not mock and frozen is None:
        raise RuntimeError('Missing frozen source request')
    if frozen:
        if frozen['state_hash'] != digest(before):
            raise RuntimeError('Prepared state mismatch')
        original_create = driver.create
        def checked_create(create, kwargs):
            from reference_discovery_parallel.base.transport import wire
            body = wire(kwargs)
            expected = frozen['body']
            fallback = {k: v for k, v in expected.items() if k not in ('logprobs', 'top_logprobs')}
            if body != expected and not (body == fallback and driver.records and driver.records[-1].get('source_supported_logprobs_fallback')):
                raise RuntimeError('Body mismatch; rejected before HTTP')
            return original_create(create, kwargs)
        driver.create = checked_create
    recorder = RecordPolicy(driver.policies['judge'])
    forced_exact = candidate in references and item['criterion'] != 'DIRECT'
    try:
        checker = variant(core, directory, item['criterion'], forced_exact)
        call = FunctionCall(**copy.deepcopy(candidate))
        refs = [FunctionCall(**copy.deepcopy(r)) for r in references]
        loop = checker.AttriGuardExecutionLoop(None, judge_llm=recorder, survival_mode='fuzzy', max_iters=1, debug=True)
        admit, branch = observed_call(loop, call, refs, task, world)
        responses = [r for r in driver.records if r.get('response')]
        if not responses or len(driver.records) > 2 or any(r['role'] != 'judge' for r in driver.records):
            raise RuntimeError('Acquisition role/budget mismatch')
        if len(driver.records) == 2 and not driver.records[0].get('source_supported_logprobs_fallback'):
            raise RuntimeError('Undeclared second request')
        last = responses[-1]
        choice = last['response']['choices'][0]
        terminal = terminal_inspect(choice['message'].get('content') or '', choice.get('finish_reason'))
        dispatch = bank_dispatch if item['stage'] == 'A0' else custom_dispatch
        arms = dict(JUDGE_RELEASE=dispatch(core, world, candidate, allowed, admit, directory / 'effects/JUDGE_RELEASE'),
                    FORCE_COMMIT=dispatch(core, world, candidate, allowed, True, directory / 'effects/FORCE_COMMIT'))
        calibration = arms['FORCE_COMMIT']['assessment']
        if calibration['committed_count'] != 1 or calibration['violation'] == permitted(item):
            raise RuntimeError('Effect calibration disagrees with contract')
        if digest(world.snapshot()) != digest(before):
            raise RuntimeError('Initial state mutated')
        natural = dict(status='INTERVENTION', new_inference=0)
        if forced_exact:
            deny = Replay([])
            natural_loop = core.AttriGuardExecutionLoop(None, judge_llm=deny, survival_mode='fuzzy')
            result = natural_loop._fuzzy_survive(FunctionCall(**copy.deepcopy(candidate)), refs, task, world.runtime, world.env)
            if result is not True or deny.index:
                raise RuntimeError('Source exact-route control differs')
            natural = dict(status='EXACT_BYPASS', allowed=True, judge_invoked=False, new_inference=0)
        elif item['criterion'] == 'SOURCE':
            replay = Replay(recorder.records)
            natural_loop = core.AttriGuardExecutionLoop(None, judge_llm=replay, survival_mode='fuzzy')
            result = natural_loop._fuzzy_survive(FunctionCall(**copy.deepcopy(candidate)), refs, task, world.runtime, world.env)
            if result != admit or replay.index != len(recorder.records):
                raise RuntimeError('Unchanged source same-reply replay differs')
            natural = dict(status='INTACT_FUZZY_SAME_REPLY', allowed=admit, new_inference=0)
        write(directory / 'policy_transcript.json', recorder.records)
        return dict(status='COMPLETE', technical_complete=True, allowed=admit, candidate_permitted=permitted(item),
            terminal_verdict=terminal, source_branch=branch, natural_source_route=natural,
            source_terminal_disagreement=terminal['interpretable'] and terminal['boolean'] != admit,
            source_reason=loop._last_judge_reason, finish_reason=choice.get('finish_reason'),
            judge_requests=len(driver.records), request_sha256=digest(last['request']),
            effects=arms, protocol_complete=choice.get('finish_reason') == 'stop',
            argument_order=sorted(candidate['args']), prepared_request_verified=frozen is not None,
            autonomous_workflows=0, semantic_human_review='PENDING')
    finally:
        driver.close()
