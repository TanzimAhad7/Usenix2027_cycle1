import copy
import itertools
import json
import os
import tempfile
import unittest
from pathlib import Path

from permission_admission import design, oracle, gate
from permission_admission.util import ROOT, read, digest
from permission_admission.runtime import configure, authenticate_origin, native_world, dispatch_arms

configure('qwen')


class Contracts(unittest.TestCase):
    def test_choice_is_one_not_two(self):
        s = design.fixture('BANK', alternatives=True)
        a, b = s['choice_contract']['slots'][0]['alternatives']
        for op in (a, b):
            self.assertFalse(oracle.evaluate(s['choice_contract'], [op])['violation'])
            self.assertTrue(oracle.evaluate(s['choice_contract'], [op])['physical_goal'])
        self.assertTrue(oracle.evaluate(s['choice_contract'], [a, b])['violation'])

    def test_ambiguous_slots_require_reassignment(self):
        a = design.fixture('BANK')['final_operation']
        b = design.change(a, 'BANK', 'PARAMETER')
        c = {'slots': [design.slot(a, b), design.slot(a)]}
        self.assertFalse(oracle.evaluate(c, [a, b])['violation'])
        spec = {'choice_contract': c}
        self.assertTrue(gate.permission(spec, [a], b['function'], b['args'])[0])

    def test_two_copies_are_legal_third_is_not(self):
        s = design.fixture('DM', 'TWO_COPIES')
        a = s['final_operation']
        self.assertFalse(oracle.evaluate(s['choice_contract'], [a, a])['violation'])
        self.assertTrue(oracle.evaluate(s['choice_contract'], [a, a, a])['violation'])
        self.assertFalse(gate.permission(s, [a, a], a['function'], a['args'])[0])

    def test_gate_oracle_agree_exhaustively_on_small_contracts(self):
        a = design.fixture('DM')['final_operation']
        b = design.change(a, 'DM', 'RECIPIENT')
        z = design.change(a, 'DM', 'PARAMETER', attack=True)
        for slots in ([design.slot(a, b)], [design.slot(a), design.slot(a, b)],
                      [design.slot(a, b), design.slot(a, b)]):
            spec = {'choice_contract': {'slots': slots}}
            for length in range(4):
                for effects in itertools.product([a, b, z], repeat=length):
                    for op in [a, b, z]:
                        self.assertEqual(gate.permission(spec, list(effects), op['function'], op['args'])[0],
                                         not oracle.evaluate(spec['choice_contract'], [*effects, op])['violation'])

    def test_independent_oracle_does_not_import_gate(self):
        import inspect, ast
        tree = ast.parse(inspect.getsource(oracle))
        imports = [node.module or '' for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        self.assertFalse(any('gate' in name for name in imports))
        self.assertFalse(any(isinstance(node, ast.Attribute) and node.attr == 'matches' for node in ast.walk(tree)))

    def test_defaults_native_semantics_and_future_capacity(self):
        s = design.fixture('EMAIL')
        a = s['final_operation']
        b = copy.deepcopy(a)
        b['args'].update(cc=[], bcc=None, attachments=[])
        self.assertEqual(oracle.signature(a), oracle.signature(b))
        for first in (a, b):
            self.assertFalse(gate.permission(s, [first], b['function'], b['args'])[0])
            self.assertTrue(oracle.evaluate(s['choice_contract'], [first, b])['violation'])

    def test_harmful_targets_forbidden_under_all_wordings(self):
        for family, structure, fact, alt in itertools.product(design.FAMILIES, design.STRUCTURES, (1, 2), (False, True)):
            s = design.fixture(family, structure, fact, alternatives=alt)
            for target in s['attack_targets'].values():
                self.assertTrue(oracle.evaluate(s['choice_contract'], s['initial_obligations'] + [target])['violation'])

    def test_facts_recipients_and_content_are_not_erased(self):
        a = design.fixture('EMAIL')['final_operation']
        b = copy.deepcopy(a)
        b['args']['cc'] = ['mallory@example.com']
        self.assertNotEqual(oracle.signature(a), oracle.signature(b))
        b = copy.deepcopy(a)
        b['args']['body'] += ' '
        self.assertNotEqual(oracle.signature(a), oracle.signature(b))

    def test_bank_numeric_equivalence_nonfinite_rejected(self):
        a = design.fixture('BANK')['final_operation']
        b = copy.deepcopy(a)
        b['args']['amount'] = 10.0
        self.assertEqual(oracle.signature(a), oracle.signature(b))
        b['args']['amount'] = float('nan')
        with self.assertRaises(ValueError):
            oracle.signature(b)


class Allocation(unittest.TestCase):
    def test_full_counts_and_unique_ids(self):
        m = design.manifest()
        self.assertEqual(m['counts_total'], {'E1_judge_generations': 576, 'E2_reference_generations_max': 224,
                                            'E3_workflows': 288, 'E2_downstream_matching_upper_bound': 304})
        rows = m['E1'] + m['E2'] + [r for b in m['E3_blocks'] for r in b]
        self.assertEqual(len(rows), len({r['id'] for r in rows}))
        self.assertEqual(m, design.manifest())

    def test_shipped_manifest_matches_exact_generated_tasks(self):
        self.assertEqual(design.manifest(), read(ROOT / 'FROZEN_DESIGN.json'))

    def test_every_block_has_all_carriers_and_policies(self):
        for block in design.manifest()['E3_blocks']:
            self.assertEqual(len(block), 6)
            self.assertEqual({(r['spec']['carrier_condition'], r['policy']) for r in block},
                             set(itertools.product(design.CARRIERS, ['OFF', 'RELEASE'])))

    def test_carrier_intervention_changes_only_procedure_span(self):
        for block in design.manifest()['E3_blocks']:
            neutral = next(r['spec'] for r in block if r['spec']['carrier_condition'] == 'NEUTRAL')
            for row in block:
                s = row['spec']
                self.assertEqual(s['root'], neutral['root'])
                self.assertEqual(s['choice_contract'], neutral['choice_contract'])
                self.assertEqual(s['attack_targets'], neutral['attack_targets'])
                self.assertEqual(s['notice'].split(design.BEGIN)[0], neutral['notice'].split(design.BEGIN)[0])

    def test_exact_and_alternative_balanced(self):
        blocks = design.manifest()['E3_blocks']
        self.assertEqual(sum(b[0]['spec']['wording'] == 'EXACT' for b in blocks), 12)
        self.assertEqual(sum(b[0]['spec']['wording'] == 'PREAPPROVED_ALTERNATIVE' for b in blocks), 12)

    def test_permission_reversal_keeps_actions_and_state_fixed(self):
        for family, dimension, location in itertools.product(design.FAMILIES, ('RECIPIENT', 'PARAMETER'), ('ROOT', 'DESIGNATED')):
            no = design.primitive(family, dimension, 'FORBID', location)
            yes = design.primitive(family, dimension, 'ALLOW', location)
            self.assertEqual(no['candidate'], yes['candidate'])
            self.assertEqual(no['reference'], yes['reference'])
            self.assertEqual(native_world(no['spec']).snapshot()['environment'], native_world(yes['spec']).snapshot()['environment'])

    def test_placebo_matched_length_without_permission_facts(self):
        for family in design.FAMILIES:
            s = design.fixture(family)
            evidence = design.evidence_record(s, [])
            actual = design.view_query(s['root'], evidence, 'EVIDENCE')
            placebo = design.view_query(s['root'], evidence, 'PLACEBO')
            self.assertEqual(len(actual), len(placebo))
            self.assertNotIn('primary_action', placebo[len(s['root']):])
            self.assertEqual(design.view_query(s['root'], evidence, 'SOURCE'), s['root'])

    def test_archived_evidence_does_not_reveal_future_stages(self):
        for origin in read(ROOT / 'origins/SELECTION.json'):
            cp = read(ROOT / 'origins' / origin['id'] / 'checkpoint.json')
            if cp['spec']['shape'] != 'STAGED':
                continue
            facts = design.evidence_record(cp['spec'], [], cp['world']['notice_stage'])
            self.assertEqual(len(facts['designated_facts']['available_stage_operations']), cp['world']['notice_stage'])
            if cp['world']['notice_stage'] == 1:
                self.assertNotIn(cp['spec']['stage_operations'][1]['args']['body'], json.dumps(facts))


class Native(unittest.TestCase):
    def test_native_all_legal_structures_and_choice_variants(self):
        for family, structure, fact in itertools.product(design.FAMILIES, design.STRUCTURES, (1, 2)):
            s = design.fixture(family, structure, fact, alternatives=True)
            world = native_world(s)
            self.assertEqual(world.effects(), [])
            for index, slot in enumerate(s['choice_contract']['slots']):
                op = slot['alternatives'][-1]
                _, error = world.runtime.run_function(world.env, op['function'], op['args'])
                self.assertIsNone(error, (family, structure, op, error))
            result = oracle.assess(s, world.env, world.events, s['report_code'], 'COMPLETE')
            self.assertTrue(result['event_state_agreement'])
            self.assertTrue(result['physical_goal'])
            self.assertFalse(result['violation'])

    def test_native_default_retry_is_another_effect_not_idempotent(self):
        s = design.fixture('EMAIL')
        world = native_world(s)
        a = s['final_operation']
        b = copy.deepcopy(a)
        b['args'].update(cc=[], bcc=[], attachments=None)
        for op in (a, b):
            self.assertIsNone(world.runtime.run_function(world.env, op['function'], op['args'])[1])
        self.assertEqual(len(world.effects()), 2)
        self.assertTrue(oracle.assess(s, world.env, world.events, '', 'COMPLETE')['violation'])

    def test_roundtrip_native_worlds(self):
        for family in design.FAMILIES:
            s = design.fixture(family)
            world = native_world(s)
            op = s['final_operation']
            world.runtime.run_function(world.env, op['function'], op['args'])
            restored = native_world(s, world.snapshot())
            self.assertEqual(digest(world.snapshot()), digest(restored.snapshot()))

    def test_ledger_mismatch_is_unknown(self):
        s = design.fixture('DM')
        world = native_world(s)
        op = s['final_operation']
        world.runtime.run_function(world.env, op['function'], op['args'])
        events = [r for r in world.events if r['kind'] != 'commit']
        self.assertEqual(oracle.assess(s, world.env, events, '', 'COMPLETE')['outcome'], 'UNKNOWN_OBSERVER')

    def test_before_exposure_is_not_later_attack_success(self):
        s = design.fixture('DM')
        world = native_world(s)
        target = s['attack_targets']['RECIPIENT']
        world.runtime.run_function(world.env, target['function'], target['args'])
        world.event('generation_transport_response', role='actor', status=200, carrier_marker_in_request=True)
        r = oracle.assess(s, world.env, world.events, '', 'COMPLETE')
        self.assertEqual(r['targets_before_exposure']['RECIPIENT'], 1)
        self.assertEqual(r['targets_after_exposure']['RECIPIENT'], 0)

    def test_trusted_gate_preserves_legal_alternative_and_blocks_second_choice(self):
        s = design.fixture('DM', alternatives=True)
        world = native_world(s, gate_enabled=True)
        a, b = s['choice_contract']['slots'][0]['alternatives']
        self.assertIsNone(world.runtime.run_function(world.env, b['function'], b['args'])[1])
        self.assertIsNotNone(world.runtime.run_function(world.env, a['function'], a['args'])[1])
        self.assertEqual(len(world.effects()), 1)


class RetainedSource(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)

    def test_retained_source_hashes_and_runtime(self):
        from reference_discovery_parallel.engine import verify_source
        self.assertTrue(verify_source()['runtime'])

    def test_all_fourteen_archived_inputs_authenticate(self):
        target = Path(os.environ.get('PERMISSION_QUALIFICATION_DIR', self.path)) / 'archived_inputs'
        for row in read(ROOT / 'origins/SELECTION.json'):
            result = authenticate_origin(ROOT / 'origins' / row['id'], target / row['id'])
            self.assertEqual(result['status'], 'PASS')

    def test_original_exact_path_still_reuses_reference_membership(self):
        from reference_discovery_parallel.base.source import load_source
        from agentdojo.functions_runtime import FunctionCall
        core, _ = load_source()
        op = design.fixture('DM')['final_operation']
        call = FunctionCall(**op, id='same')
        loop = core.AttriGuardExecutionLoop(None, judge_llm=None)
        world = native_world(design.fixture('DM'))
        self.assertTrue(loop._fuzzy_survive(call, [call], '', world.runtime, world.env))
        self.assertTrue(loop._fuzzy_survive(call, [call], '', world.runtime, world.env))

    def test_fuzzy_source_result_and_strict_validity_retained(self):
        from permission_admission.worker import run_job
        item = next(r for r in design.manifest()['E1'] if r['view'] == 'SOURCE')
        r = run_job(item, self.path / 'E1', mock=True)
        self.assertEqual(r['status'], 'COMPLETE', r.get('error'))
        self.assertTrue(r['qualified'])
        self.assertEqual(r['source_decisions'][0]['route'], 'FUZZY')

    def test_fixed_reference_and_native_clones_end_to_end(self):
        from permission_admission.worker import run_job
        r = run_job(design.manifest()['E2'][0], self.path / 'E2', mock=True)
        self.assertEqual(r['status'], 'COMPLETE', r.get('error'))
        self.assertEqual(r['role_counts']['reference'], 1)
        self.assertIn('TRUSTED_CHOICE_GATE_AFTER_SOURCE', r['native_clone_arms'])

    def test_autonomous_mock_all_families_off_and_release(self):
        from permission_admission.worker import run_job
        for family, policy in itertools.product(design.FAMILIES, ('OFF', 'RELEASE')):
            s = design.fixture(family, 'PREFIX_TWO_DISTINCT', carrier='RECIPIENT', alternatives=True)
            item = {'id': family + policy, 'panel': 'E3', 'kind': 'AUTONOMOUS', 'policy': policy, 'spec': s}
            r = run_job(item, self.path / item['id'], mock=True)
            self.assertEqual(r['status'], 'COMPLETE', r.get('error'))
            self.assertTrue(r['qualified'], r.get('error'))
            self.assertTrue(r['event_state_agreement'])
            self.assertTrue(r['actor_carrier_request_accepted'])
            if policy == 'RELEASE':
                self.assertFalse(r['violation'])

    def test_technical_failure_not_safe_completion(self):
        from permission_admission.worker import run_job
        from unittest.mock import patch
        item = design.manifest()['E1'][0]
        with patch('permission_admission.worker.fixed', side_effect=RuntimeError('Injected infrastructure error')):
            r = run_job(item, self.path / 'error', mock=True)
        self.assertEqual(r['status'], 'TECHNICAL_ERROR')
        self.assertFalse(r['qualified'])
        self.assertFalse(r['scientific_negative'])

    def test_malformed_source_verdict_retained_but_unqualified(self):
        from permission_admission.worker import run_job
        from reference_discovery_parallel.base.transport import reply
        from unittest.mock import patch
        item = design.manifest()['E1'][0]
        with patch('permission_admission.runtime.mock_fixed', return_value=reply('not true')):
            r = run_job(item, self.path / 'malformed', mock=True)
        self.assertEqual(r['status'], 'COMPLETE')
        self.assertTrue(r['allowed'])  # Original permissive source predicate.
        self.assertFalse(r['qualified'])
        self.assertFalse(r['judge_verdicts_strictly_valid'])

    def test_evidence_append_preserves_all_original_history(self):
        from permission_admission.worker import add_system_evidence
        row = read(ROOT / 'origins/SELECTION.json')[0]
        original = read(ROOT / 'origins' / row['id'] / 'reference_record.json')['request']
        completed = add_system_evidence(original, {'designated_facts': 'fixture'})
        self.assertEqual(completed['messages'][1:], original['messages'][1:])
        for field in set(original) - {'messages'}:
            self.assertEqual(completed[field], original[field])

    def test_missing_records_remain_in_report_denominators(self):
        from permission_admission.report import analyze
        m = design.manifest()
        r = analyze(self.path / 'empty_campaign', m)
        self.assertEqual(r['planned'], 1088)
        self.assertEqual(r['recorded'], 0)
        self.assertEqual(r['qualified'], 0)

    def test_strict_gemma_parser_does_not_silently_repair(self):
        from reference_discovery_parallel.strict_tags import parse
        calls, _ = parse('<tool_call>{"name":"send_direct_message","arguments":{"recipient":"Alice","body":"ok"}}</tool_call>')
        self.assertEqual(len(calls), 1)
        with self.assertRaises(Exception):
            parse('<tool_call>{"name":"send_direct_message","arguments":BROKEN}</tool_call>')

