"""One scheduled source judge acquisition and independently observed effects."""
import copy
import os
from pathlib import Path
from reference_study.common import digest, write
from e1.cases import RecordPolicy, Replay
from e2b.cases import observed_call
from e2b.terminal import inspect as terminal_inspect
from .design import inputs
from .checker import variant


def world_for(item):
    if item['phase'] == 'SENTINEL':
        from a01.simulation import World
    else:
        from .simulation import World
    return World()


def run(item, directory, family, mock=False, frozen=None, mock_response=None):
    from agentdojo.functions_runtime import FunctionCall
    from permission_admission.runtime import fixed_driver
    from reference_discovery_parallel.base.source import load_source
    from reference_discovery_parallel.base.transport import reply, wire
    from .simulation import dispatch
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    core, _ = load_source()
    task, candidate, references, allowed = inputs(item)
    world = world_for(item)
    before = world.snapshot()
    permitted = candidate in allowed
    expected = item['request_body']
    if frozen is not None:
        if frozen['body'] != expected or frozen['state_hash'] != digest(before):
            raise RuntimeError('CPU-prepared body/state differs')
    elif not mock:
        raise RuntimeError('Live acquisition requires frozen SDK preparation')
    write(directory / 'held_input.json', dict(task=task, candidate=candidate,
        references=references, allowed_operations=allowed, expected_legal=permitted,
        initial_state=before, initial_state_hash=digest(before),
        phase=item['phase'], semantic_human_review='PENDING',
        scope='Custom isolated simulation; researcher-supplied operations, no attacker.'))
    driver = fixed_driver(directory / 'model_io', mock)
    if mock:
        rule=os.environ.get('J2_MOCK_RULE','EXACT_JOINT')
        if rule not in item['predictions']:raise RuntimeError('Unknown engineering mock rule')
        mock_value=item['predictions'][rule]
        driver.mock = mock_response or (lambda role, body: reply(
            '{"survive":' + str(mock_value).lower() + ',"reason":"ENGINEERING MOCK ONLY"}'))
    original_create = driver.create

    def checked_create(create, kwargs):
        body = wire(kwargs)
        fallback = {k: v for k, v in expected.items() if k not in ('logprobs', 'top_logprobs')}
        supported_fallback = (body == fallback and driver.records and
                              driver.records[-1].get('source_supported_logprobs_fallback'))
        if body != expected and not supported_fallback:
            write(directory / 'request_mismatch.json', dict(expected=expected, actual=body))
            raise RuntimeError('Actual SDK body differs; HTTP/model call refused')
        return original_create(create, kwargs)

    driver.create = checked_create
    recorder = RecordPolicy(driver.policies['judge'])
    try:
        checker = variant(core, directory, item['criterion'], item['phase'] == 'MAIN')
        call = FunctionCall(**copy.deepcopy(candidate))
        refs = [FunctionCall(**copy.deepcopy(r)) for r in references]
        loop = checker.AttriGuardExecutionLoop(None, judge_llm=recorder,
            survival_mode='fuzzy', max_iters=1, debug=True)
        admit, branch = observed_call(loop, call, refs, task, world)
        responses = [r for r in driver.records if r.get('response')]
        if not responses or len(driver.records) > 2 or any(r['role'] != 'judge' for r in driver.records):
            raise RuntimeError('Acquisition role/budget mismatch')
        if len(driver.records) == 2 and not driver.records[0].get('source_supported_logprobs_fallback'):
            raise RuntimeError('Undeclared second request')
        last = responses[-1]
        choice = last['response']['choices'][0]
        terminal = terminal_inspect(choice['message'].get('content') or '', choice.get('finish_reason'))
        operative = dict(allowed=admit, candidate_permitted=permitted,
            source_branch=branch, terminal_verdict=terminal,
            source_terminal_disagreement=terminal['interpretable'] and terminal['boolean'] != admit,
            finish_reason=choice.get('finish_reason'), request_sha256=digest(last['request']),
            judge_requests=len(driver.records), mock=mock,
            request_body_verified=True, source_reason=loop._last_judge_reason,
            usage=last['response'].get('usage'), response_id=last['response'].get('id'))
        # Preserve known decisions even if a later replay or dispatch check fails.
        write(directory / 'operative_decision.json', operative)
        release = dispatch(core, world, candidate, allowed, admit, directory / 'effects/JUDGE_RELEASE')
        calibration = dispatch(core, world, candidate, allowed, True, directory / 'effects/FORCE_COMMIT')
        score = calibration['assessment']
        if score['committed_count'] != 1 or score['violation'] == permitted:
            raise RuntimeError('Candidate dispatch calibration disagrees with public contract')
        for index, ref in enumerate(references):
            result = dispatch(core, world, ref, allowed, True,
                              directory / 'effects' / ('REFERENCE_CALIBRATION_' + str(index)))
            if result['assessment']['committed_count'] != 1 or result['assessment']['violation']:
                raise RuntimeError('Lawful reference failed effect calibration')
        if digest(world.snapshot()) != digest(before):
            raise RuntimeError('Held initial state changed')
        if references:
            # Replay the same acquired reply through the original route under
            # the SAME declared policy, including OWNER_PRIORITY when selected.
            native = core if item['criterion'] == 'SOURCE' else variant(
                core, directory / 'original_route_same_policy', item['criterion'], False)
            replay = Replay(recorder.records)
            original_loop = native.AttriGuardExecutionLoop(None, judge_llm=replay, survival_mode='fuzzy')
            replayed = original_loop._fuzzy_survive(call, refs, task, world.runtime, world.env)
            if replayed != admit or replay.index != len(recorder.records):
                raise RuntimeError('Same-policy original-route same-reply replay differs')
            natural = dict(status='ORIGINAL_ROUTE_SAME_REPLY_SAME_POLICY',
                allowed=replayed, judge_calls=replay.index, new_inference=0,
                untouched_source_policy=item['criterion'] == 'SOURCE')
        else:
            no_query = Replay([])
            original_loop = core.AttriGuardExecutionLoop(None, judge_llm=no_query, survival_mode='fuzzy')
            native_answer = original_loop._fuzzy_survive(call, [], task, world.runtime, world.env)
            if native_answer is not False or no_query.index:
                raise RuntimeError('Native NONE did not reject without a query')
            natural = dict(status='COUNTERFACTUAL_NONE_JUDGE', native_allowed=False,
                native_judge_calls=0, counterfactual_allowed=admit, new_inference=0)
        write(directory / 'source_replay.json', natural)
        return dict(operative, status='COMPLETE', technical_complete=True,
            effects=dict(JUDGE_RELEASE=release, FORCE_COMMIT=calibration),
            natural_source_route=natural, source_replay_verified=True,
            initial_state_hash=digest(before), prepared_request_verified=frozen is not None,
            autonomous_workflows=0, semantic_human_review='PENDING')
    finally:
        write(directory / 'policy_transcript.json', recorder.records)
        driver.close()
