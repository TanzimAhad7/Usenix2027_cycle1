"""One isolated job process; all decisions and raw source I/O are retained."""
from __future__ import annotations

import argparse
import contextlib
import copy
import signal
import time
import traceback
from pathlib import Path

from .util import ROOT, read, write, digest
from .design import evidence_record, view_query
from .runtime import (configure, fixed_driver, native_world, matches_with_source,
                      dispatch_arms, mock_workflow)
from .oracle import contract_for, evaluate


def add_system_evidence(request, evidence):
    """Declared E2 reference-input intervention, preserves every historical turn."""
    result = copy.deepcopy(request)
    addition = '\nAUTHENTICATED_FACT_RECORD\n' + __import__('json').dumps(evidence, sort_keys=True)
    system = next((row for row in result['messages'] if row['role'] == 'system'), None)
    if system is None:
        raise ValueError('No authenticated system-message insertion point')
    if isinstance(system['content'], str):
        system['content'] += addition
    elif isinstance(system['content'], list):
        system['content'].append({'type': 'text', 'text': addition})
    else:
        raise TypeError('Unsupported archived system content')
    return result


def fixed(item, directory, family, mock):
    from reference_discovery_parallel.base.source import load_source
    from reference_discovery_parallel.common import native_messages, pack
    from agentdojo.functions_runtime import FunctionCall
    core, _ = load_source()
    driver = fixed_driver(directory / 'model_io', mock)
    try:
        if item['panel'] == 'E1':
            spec = item['spec']
            world = native_world(spec)
            candidate = FunctionCall(**item['candidate'], id='fixed-candidate')
            reference = FunctionCall(**item['reference'], id='fixed-reference')
            before = world.snapshot()
            decisions = matches_with_source(core, driver, spec, world, [candidate], [reference], item['query'])
            clones = dispatch_arms(core, spec, world, [candidate], [reference], [row['allowed'] for row in decisions])
            candidate_oracle = evaluate(contract_for(spec), [item['candidate']])
            reference_oracle = evaluate(contract_for(spec), [item['reference']])
            if candidate_oracle['violation'] == item['expected_candidate_allowed'] or reference_oracle['violation']:
                raise RuntimeError('Frozen candidate/reference permission label does not match oracle')
            result = dict(permission=item['permission'], fact_location=item['fact_location'], view=item['view'],
                          dimension=item['dimension'], family=spec['family'], draw=item['draw'],
                          allowed=decisions[0]['allowed'], source_decisions=decisions,
                          expected_candidate_allowed=item['expected_candidate_allowed'],
                          candidate_oracle=candidate_oracle, reference_oracle=reference_oracle,
                          fixed_state_digest=digest(before), native_clone_arms=clones)
        else:
            folder = ROOT / 'origins' / item['origin']
            if not item['eligible']:
                return dict(status='INELIGIBLE_ARCHIVED_ORIGIN', qualified=False,
                            attempted=False, origin=item['origin'], inference=0)
            cp = read(folder / 'checkpoint.json')
            spec = cp['spec']
            world = native_world(spec, cp['world'])
            original = read(folder / 'reference_record.json')['request']
            if mock:
                # Exercise the archived exact/fuzzy paths during engineering
                # tests. This is an explicitly scripted historical response,
                # never a fresh reference-generation research result.
                archived_response = read(folder / 'reference_record.json')['response']
                from .runtime import mock_fixed
                driver.mock = lambda role, body: copy.deepcopy(archived_response) if role == 'reference' else mock_fixed(role, body)
            request = copy.deepcopy(original)
            from reference_discovery_parallel.common import MODEL
            request['model'] = MODEL
            if item['view'] == 'EVIDENCE':
                request = add_system_evidence(request, evidence_record(spec, world.effects(), cp['world']['notice_stage']))
            write(directory / 'input_intervention.json', dict(original=original, submitted=request,
                  original_hash=digest(original), submitted_hash=digest(request),
                  changes=['model_alias'] + (['authenticated_system_fact_append'] if item['view'] == 'EVIDENCE' else []),
                  historical_assistant_reasoning_preserved=True, fresh_attenuation=False))
            driver.role = 'reference'
            # Exact captured final request, with only declared changes. Reuses
            # retained SDK interception, no synthetic reconstruction of history.
            response = driver.policies['reference'].policy.client.chat.completions.create(**request)
            if response.choices[0].finish_reason == 'length':
                raise RuntimeError('Reference truncated; no complete admission claim')
            import openai_llm_compat
            message = openai_llm_compat._openai_to_assistant_message(response.choices[0].message)
            refs = message.get('tool_calls') or []
            pending = native_messages([{'role': 'assistant', 'content': None, 'tool_calls': cp['pending']}])[0]['tool_calls']
            decisions = matches_with_source(core, driver, spec, world, pending, refs, spec['root'])
            arms = dispatch_arms(core, spec, world, pending, refs, [row['allowed'] for row in decisions])
            from reference_discovery_parallel.world import SENSITIVE
            proposed_effects = [pack(ref) for ref in refs if ref.function in SENSITIVE]
            prefix_oracle = evaluate(contract_for(spec), world.effects())
            reference_oracle = evaluate(contract_for(spec), world.effects() + proposed_effects)
            result = dict(origin=item['origin'], view=item['view'], draw=item['draw'],
                          archived_original_profile='gemma', new_reference_profile=family,
                          reference_calls=pack(refs), source_decisions=decisions,
                          prefix_oracle=prefix_oracle, reference_proposal_oracle=reference_oracle,
                          reference_added_unmatched_proposals=max(0, len(reference_oracle['violation_indices']) - len(prefix_oracle['violation_indices'])),
                          native_clone_arms=arms, actual_source_root_for_matching=spec['root'],
                          scope='Fresh final-reference output; no fresh actor/attenuation. Matching profile follows backend; '
                                'reference legality is measured independently of matcher outcomes.')
        if digest(world.snapshot()) != digest(before if item['panel'] == 'E1' else cp['world']):
            raise RuntimeError('Fixed-role experiment changed original native state')
        complete = all(not record.get('truncated') and not record.get('exception')
                       for record in driver.records if not record.get('source_supported_logprobs_fallback'))
        verdicts = [value for decision in decisions for value in decision['strict_verdicts']]
        result.update(status='COMPLETE', qualified=complete and all(value['valid'] for value in verdicts),
                      source_path_complete=complete, judge_verdicts_strictly_valid=all(value['valid'] for value in verdicts),
                      generation_records=len(driver.records), http_attempts=len(driver.http),
                      downstream_matching_evaluations=len(decisions) if item['panel'] == 'E2' else 0,
                      downstream_judge_generations=sum(record['role'] == 'judge' for record in driver.records)
                                                  if item['panel'] == 'E2' else 0,
                      role_counts={role: sum(record['role'] == role for record in driver.records)
                                   for role in ('reference', 'judge', 'attenuator')})
        return result
    finally:
        driver.close()


def run_job(item, directory, family='qwen', mock=False):
    started = time.monotonic()
    _, engine = configure(family)
    directory = Path(directory)
    result = None
    handler = None
    try:
        if item['panel'] == 'E3':
            session = engine.Session(item, directory, mock=mock_workflow if mock else None)
            result = session.run()
            result['status'] = result['lifecycle']
            result['wording'] = item['spec']['wording']
            result['structure'] = item['spec']['structure']
        else:
            directory.mkdir(parents=True, exist_ok=False)
            write(directory / 'item.json', item)
            def expired(*_):
                raise TimeoutError('Fixed-role technical watchdog: 1200 seconds')
            handler = signal.signal(signal.SIGALRM, expired)
            signal.alarm(1200)
            with (directory / 'diagnostic.log').open('w') as stream, contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                result = fixed(item, directory, family, mock)
    except BaseException as exc:
        directory.mkdir(parents=True, exist_ok=True)
        result = dict(status='INTERRUPTED' if isinstance(exc, (KeyboardInterrupt, SystemExit)) else 'TECHNICAL_ERROR',
                      qualified=False, error={'type': type(exc).__name__, 'message': str(exc),
                                               'traceback': traceback.format_exc()},
                      scientific_negative=False)
    finally:
        if handler is not None:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, handler)
    result.update(id=item['id'], panel=item['panel'], profile=family, mock=mock,
                  attempted=result.get('attempted', True), elapsed_seconds=time.monotonic() - started,
                  evaluation_mode='MOCK_ENGINEERING_ZERO_MODEL_INFERENCE' if mock else 'MODEL_EXPERIMENT')
    record_path = directory / ('driver_records.json' if item['panel'] == 'E3' else 'model_io/driver_records.json')
    if record_path.is_file():
        records = read(record_path)
        from .judge_format import annotate
        annotate(result, records)
        result['driver_records_including_errors'] = len(records)
        result['completed_response_records'] = sum('response' in record for record in records)
        result['role_counts'] = {role: sum(record['role'] == role for record in records)
                                for role in ('actor', 'reference', 'judge', 'attenuator')}
        result.setdefault('generation_records', sum(not record.get('reused', False) for record in records))
        http_folder = directory / ('http' if item['panel'] == 'E3' else 'model_io/http')
        result.setdefault('http_attempts', len(list(http_folder.glob('*.request.json'))))
        result['token_usage'] = {field: sum((record.get('response', {}).get('usage') or {}).get(field, 0) or 0
                                           for record in records)
                                 for field in ('prompt_tokens', 'completion_tokens', 'total_tokens')}
    write(directory / 'result.json', result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--item', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--family', choices=['qwen', 'gemma'], required=True)
    parser.add_argument('--mock', action='store_true')
    args = parser.parse_args()
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt('Owned controller requested shutdown')))
    result = run_job(read(args.item), args.out, args.family, args.mock)
    print(result['id'], result['status'], 'qualified=' + str(result['qualified']), flush=True)
    return 0 if result['status'] not in ('TECHNICAL_ERROR', 'INTERRUPTED') else 1


if __name__ == '__main__':
    raise SystemExit(main())

