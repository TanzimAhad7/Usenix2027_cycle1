import copy
import json
from pathlib import Path
import tempfile
import unittest
from diagnostic import Ledger, contract, load_guard, cases, execute_case

class ObserverTests(unittest.TestCase):
    def effect(self,recipient='Alice',amount=10): return dict(recipient=recipient,amount=amount)
    def test_legal_then_forbidden(self):
        s=Ledger(contract());s.effects=[self.effect(),self.effect('Mallory')]
        self.assertTrue(s.outcome()['completion']);self.assertTrue(s.outcome()['violation'])
        self.assertFalse(s.outcome()['secure_completion'])
    def test_multiple_legal(self):
        s=Ledger(contract(2));s.effects=[self.effect(),self.effect()]
        self.assertTrue(s.outcome()['secure_completion'])
    def test_unknown_closure(self):
        self.assertEqual(Ledger(contract()).outcome(False)['violation'],'UNKNOWN')
    def test_known_violation_survives_unknown_closure(self):
        s=Ledger(contract());s.effects=[self.effect('Mallory')]
        self.assertIs(s.outcome(False)['violation'],True)
    def test_success_string_does_not_commit(self):
        s=Ledger(contract());s.event('runtime_result',result='success')
        self.assertFalse(s.outcome()['completion'])
    def test_actual_runtime_idempotency_and_key_binding(self):
        s=Ledger(contract());r=s.make_runtime()
        for recipient in ('Alice','Alice','Mallory'):
            r.run_function(None,'pay',dict(recipient=recipient,amount=10,key='k'))
        self.assertEqual(len(s.effects),1);self.assertFalse(s.violation())
    def test_runtime_error_shape(self):
        s=Ledger(contract(),lookup='error');r=s.make_runtime()
        result,error=r.run_function(None,'get_iban',{'name':'Alice'})
        self.assertEqual(result,'');self.assertTrue(error.startswith('RuntimeError:'))
    def test_lookup_schedule_is_independent(self):
        schedule=['empty','error'];s=Ledger(contract(),lookup=schedule)
        s.make_runtime().run_function(None,'get_iban',{'name':'Alice'})
        self.assertEqual(schedule,['empty','error'])
    def test_gate_enforces_aggregate(self):
        s=Ledger(contract(),gate=True);r=s.make_runtime()
        for _ in range(2): r.run_function(None,'pay',dict(recipient='Alice',amount=10,key=''))
        self.assertEqual(len(s.effects),1)
    def test_wrong_amount(self):
        s=Ledger(contract());s.effects=[self.effect(amount=11)]
        self.assertTrue(s.violation())
    def test_native_partial_mutation_error_keeps_violation(self):
        s=Ledger(contract());r=s.make_runtime()
        @r.register_function
        def partial() -> str:
            """Commit a forbidden simulated effect and then fail."""
            s.effects.append(self.effect('Mallory'))
            raise RuntimeError('failure after effect')
        result,error=r.run_function(None,'partial',{})
        self.assertEqual(result,'');self.assertIn('failure after effect',error)
        self.assertIs(s.outcome(False)['violation'],True)

class ConformanceTests(unittest.TestCase):
    def test_passive_telemetry_does_not_change_outcome_or_receipts(self):
        # Compare source-bound execution with and without instrumentation for
        # every base scenario; IDs in the separate observer are not compared.
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);generated=root/'generated';generated.mkdir()
            for i,case in enumerate(cases()):
                a=root/f'a{i}';b=root/f'b{i}';a.mkdir();b.mkdir()
                x=execute_case(load_guard('original',generated),'original',copy.deepcopy(case),a,passive=True)
                y=execute_case(load_guard('original',generated),'original',copy.deepcopy(case),b,passive=False)
                self.assertEqual(x['outcome'],y['outcome'],case['name'])
                self.assertEqual(x['receipts'],y['receipts'],case['name'])
                self.assertEqual(x['shadow_queries'],y['shadow_queries'],case['name'])

if __name__=='__main__': unittest.main()
