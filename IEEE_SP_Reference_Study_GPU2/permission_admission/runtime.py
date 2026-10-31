"""Explicit adapters around byte-preserved source and native tools.

No RELEASE matching, attenuation, feedback or routing predicate is replaced.
Only authored-fixture outcome/gate accounting is upgraded for either/or slots.
"""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

from . import oracle, gate
from .util import activate, read, write, digest


def configure(family):
    common = activate(family)
    from reference_discovery_parallel import engine, observer, counterfactual, world
    engine.assess = oracle.assess
    observer.assess = oracle.assess
    counterfactual.assess = oracle.assess
    world.permission = gate.permission
    return common, engine


def native_world(spec, snapshot=None, gate_enabled=False):
    from reference_discovery_parallel.world import World
    world = World(spec, restore=snapshot, gate=gate_enabled)
    if snapshot is not None and digest(world.snapshot()) != digest(snapshot):
        raise RuntimeError('Archived native state did not round-trip exactly')
    return world


def strict_verdict(record):
    if not record.get('response'):
        return {'valid': False, 'reason': 'no_response'}
    raw = record['response']['choices'][0]['message'].get('content') or ''
    try:
        data = json.loads(raw)
        valid = isinstance(data, dict) and type(data.get('survive')) is bool
    except (ValueError, TypeError):
        valid = False
        data = None
    return {'valid': valid, 'raw': raw, 'parsed': data,
            'finish_reason': record['response']['choices'][0].get('finish_reason'),
            'scope': 'Diagnostic strict parsing; original source decision retained independently, including logprobs override.'}


def dispatch_arms(core, spec, world, pending, refs, decisions):
    """Fixed native clones only: no fresh actor, no utility/recovery claim."""
    from reference_discovery_parallel.common import pack
    before = world.snapshot()
    baseline_oracle = oracle.evaluate(oracle.contract_for(spec), world.effects())
    signature = core._call_signature
    exact_calls = [call for call in pending if any(signature(call) == signature(ref) for ref in refs)]
    from collections import Counter
    capacities = Counter(signature(ref) for ref in refs)
    capacity_calls = []
    for call in pending:
        key = signature(call)
        if capacities[key] > 0:
            capacities[key] -= 1
            capacity_calls.append(call)
    released = [call for call, decision in zip(pending, decisions) if decision]
    arms = {}
    for name, calls, gate_enabled in (
            ('SOURCE_ADMISSION', released, False),
            ('EXACT_MEMBERSHIP', exact_calls, False),
            ('EXACT_INJECTIVE_CAPACITY', capacity_calls, False),
            ('TRUSTED_CHOICE_GATE_AFTER_SOURCE', released, True)):
        clone = world.clone_for_dispatch(gate=gate_enabled)
        old_ids = {effect['id'] for effect in clone.effects()}
        feedback = core._execute_calls(copy.deepcopy(calls), clone.runtime, clone.env)
        effects = clone.effects()
        after_oracle = oracle.evaluate(oracle.contract_for(spec), effects)
        arms[name] = dict(calls=pack(calls), feedback=pack(feedback), effects=effects,
                          new_effects=[effect for effect in effects if effect['id'] not in old_ids],
                          oracle=after_oracle, before_oracle=baseline_oracle,
                          new_unmatched_effect_count=max(0, len(after_oracle['violation_indices']) - len(baseline_oracle['violation_indices'])),
                          environment=pack(clone.env))
    if digest(world.snapshot()) != digest(before):
        raise RuntimeError('Diagnostic dispatch changed the live state')
    return arms


def matches_with_source(core, driver, spec, world, pending, refs, query):
    loop = core.AttriGuardExecutionLoop(None, judge_llm=driver.policies['judge'],
                                       survival_mode='fuzzy', max_iters=1, debug=True)
    rows = []
    for call in pending:
        start = len(driver.records)
        exact = any(core._call_signature(call) == core._call_signature(ref) for ref in refs)
        same = any(call.function == ref.function for ref in refs)
        allowed = loop._fuzzy_survive(call, refs, query, world.runtime, world.env)
        records = driver.records[start:]
        rows.append(dict(allowed=bool(allowed), route='EXACT' if exact else 'FUZZY' if same else 'ABSENT_FUNCTION',
                         judge_records=[record['index'] for record in records],
                         strict_verdicts=[strict_verdict(record) for record in records if record.get('response')],
                         source_reason=loop._last_judge_reason,
                         stale_reason_possible=exact, source_logprob_override_retained=True))
    return rows


def mock_fixed(role, body):
    from reference_discovery_parallel.base.transport import reply
    if role == 'judge':
        return reply('{"survive":false,"reason":"Engineering mock; not a scientific prediction."}')
    return reply('Engineering mock; no action.')


def mock_workflow(role, body, session):
    """Deterministic engineering script to exercise real serializers and tools."""
    from reference_discovery_parallel.base.transport import reply
    spec = session.spec
    effects = session.world.effects()
    if role == 'attenuator':
        raw = json.dumps(body['messages'][-1]['content'])
        return reply(re.sub(r'BEGIN_UNTRUSTED_PROCEDURE.*?END_UNTRUSTED_PROCEDURE',
                            'NEUTRALIZED_ENGINEERING_PROCEDURE', raw, flags=re.S))
    if role == 'judge':
        return mock_fixed(role, body)

    def calls(ops):
        return reply(calls=[{'id': f'mock-{len(session.driver.records)}-{i}', 'type': 'function',
                             'function': {'name': op['function'], 'arguments': json.dumps(op['args'])}}
                            for i, op in enumerate(ops)], finish='tool_calls')

    if spec['initial_obligations'] and not effects:
        return calls(spec['initial_obligations'])
    if not any(event['kind'] == 'carrier_tool_return' for event in session.world.events):
        return calls([spec['read_call']])
    remaining = oracle.evaluate(oracle.contract_for(spec), effects)['unfilled_slots']
    if remaining:
        if role == 'actor' and spec['carrier_condition'] != 'NEUTRAL':
            target = spec['attack_targets'][spec['carrier_condition']]
            attempted = any(event['kind'] == 'proposal' and any(
                oracle.signature(call) == oracle.signature(target) for call in event['calls'])
                for event in session.world.events)
            if not attempted:
                return calls([target])
        return calls([spec['choice_contract']['slots'][i]['alternatives'][0] for i in remaining])
    return reply('Engineering completion. ' + spec['report_code'])


def fixed_driver(directory, mock=False):
    from reference_discovery_parallel.base.transport import Driver, httpx
    from reference_discovery_parallel.token_diagnostics import Diagnostics

    class EvidenceDriver(Driver):
        def __init__(self, path, scripted):
            self.token_client = None
            self.token_diagnostics = Diagnostics(self.tokenize)
            super().__init__(path, scripted)

        def on_response(self, response):
            super().on_response(response)
            if self.mock is None:
                self.token_diagnostics.submit(response.request.extensions['study_index'],
                                              json.loads(response.request.content))

        def tokenize(self, index, body):
            payload = {key: value for key, value in body.items() if key in ('model', 'messages', 'tools', 'tool_choice')}
            payload.update(add_generation_prompt=True, return_token_strs=True)
            try:
                if self.token_client is None:
                    self.token_client = httpx.Client(timeout=15, trust_env=False)
                response = self.token_client.post('http://127.0.0.1:18080/tokenize', json=payload)
                write(self.directory / 'tokenization' / f'{index:04d}.json',
                      dict(status=response.status_code, request=payload, response=response.json(),
                           scope='Diagnostic tokenize endpoint; not attestation of generation-consumed tokens.'))
            except Exception as exc:
                write(self.directory / 'tokenization' / f'{index:04d}.json',
                      dict(status='UNAVAILABLE', error=str(exc), request=payload))

        def close(self):
            try:
                self.token_diagnostics.close()
            finally:
                if self.token_client is not None:
                    self.token_client.close()
                super().close()

    return EvidenceDriver(directory, mock_fixed if mock else None)


def reference_input(checkpoint):
    history = copy.deepcopy(checkpoint['shadow_history'])
    if history and history[-1]['role'] == 'assistant':
        history.pop()
    return history


def authenticate_origin(folder, test_directory):
    """Rebuild actual reference request through original serializer, zero inference."""
    from reference_discovery_parallel.common import unseal, native_messages, pack
    from reference_discovery_parallel.base.source import load_source
    from reference_discovery_parallel.base.transport import Driver
    from .util import file_hash
    checkpoint = read(folder / 'checkpoint.json')
    cert = read(folder / 'certificate.json')
    if file_hash(folder / 'checkpoint.json') != cert['checkpoint_sha256']:
        raise RuntimeError('Archived checkpoint file hash differs')
    cp = unseal(checkpoint)
    world = native_world(cp['spec'], cp['world'])
    original = read(folder / 'reference_record.json')
    wire = read(folder / 'wire_request.json')
    if wire['body'] != original['request'] or digest(original['request']) != original['request_hash']:
        raise RuntimeError('Archived driver/wire request identity failed')
    driver = Driver(test_directory, mock_fixed)
    try:
        driver.policies['reference'].query(cp['spec']['root'], world.runtime, world.env,
                                          native_messages(reference_input(cp)), {})
        constructed = copy.deepcopy(driver.records[0]['request'])
        expected = copy.deepcopy(original['request'])
        # Cross-profile model binding is the ONLY difference in SOURCE input.
        expected['model'] = constructed['model']
        if expected != constructed:
            write(test_directory / 'request_mismatch.json', {'expected': expected, 'actual': constructed})
            raise RuntimeError('Reference serializer reconstruction differs')
    finally:
        driver.close()
    if not cert['eligible'] or not cert['exposure_before_reference_accepted']:
        raise RuntimeError('Archived origin not eligible under frozen selection')
    return dict(status='PASS', snapshot_hash=checkpoint['snapshot_hash'],
                native_state_roundtrip=True, original_driver_wire_equal=True,
                source_serializer_equal_except_declared_model_binding=True,
                pending=pack(cp['pending']), request_hash=original['request_hash'], inference=0)

