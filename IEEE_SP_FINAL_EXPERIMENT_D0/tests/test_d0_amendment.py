"""Regression tests for the D0 amendment (parser, prefill acceptance, GPU pinning)."""
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

from design import TOOLS
from model import parse
from run import (ALLOWED_GPUS, AMENDMENT, PINNED_UUIDS, compare_prefill_decisions, decision_view,
                 prefill_choice)

FIXTURES = Path(__file__).resolve().parent / "fixtures"
WRITES = {fn for family in TOOLS.values() for fn in family["writes"]}
READS = {fn for family in TOOLS.values() for fn in family["reads"]}


class ParserTests(unittest.TestCase):
    def test_json_and_fenced_forms_unchanged(self):
        call = {"function": "send_money", "args": {"amount": 47, "recipient": "DE1"}}
        self.assertEqual(parse(json.dumps(call)), call)
        self.assertEqual(parse("```json\n" + json.dumps(call) + "\n```"), call)
        self.assertEqual(parse('{"final":"done"}'), {"final": "done"})

    def test_wrapped_call_accepted(self):
        text = '<TOOL_CALL>send_email({"body":"x)","recipients":["a@example.com"],"subject":"s"})</TOOL_CALL>'
        self.assertEqual(parse(text), {"function": "send_email",
                                       "args": {"body": "x)", "recipients": ["a@example.com"], "subject": "s"}})
        self.assertEqual(parse("  \n" + text + "\n"), parse(text))

    def test_wrapped_call_rejects_extra_text_and_bad_json(self):
        good = '<TOOL_CALL>get_received_emails({})</TOOL_CALL>'
        self.assertIsNotNone(parse(good))
        for text in ("Sure. " + good, good + " done", good + good,
                     '<TOOL_CALL>send_money({"amount":1,"amount":2})</TOOL_CALL>',
                     '<TOOL_CALL>send_money({amount:1})</TOOL_CALL>',
                     '<TOOL_CALL>send money({"amount":1})</TOOL_CALL>',
                     '<FUNCTION_CALL>{"function":"send_money","args":{}}</FUNCTION_CALL>'):
            self.assertIsNone(parse(text), text)

    def test_recorded_qwen_outputs(self):
        """Real outputs that the original parser rejected in run 20261108T232225Z_3654860_31695."""
        samples = json.loads((FIXTURES / "qwen_unparsed_samples.json").read_text())
        wrapped = [s for s in samples if s["arm"] != "first_not_wrapped"]
        other = [s for s in samples if s["arm"] == "first_not_wrapped"]
        self.assertGreater(len(wrapped), 200)
        for s in wrapped:
            got = parse(s["text"])
            self.assertIsNotNone(got, s["text"][:200])
            self.assertIn(got["function"], WRITES | READS)
            match = re.search(r"<TOOL_CALL>([A-Za-z_]+)\((\{.*\})\)</TOOL_CALL>", s["text"], re.DOTALL)
            self.assertEqual(got, {"function": match[1], "args": json.loads(match[2])})
        # The seven non-wrapped E2L failures are genuine format failures and stay unparsed.
        self.assertEqual(len(other), 7)
        for s in other:
            self.assertIsNone(parse(s["text"]), s["text"][:200])


class PrefillTests(unittest.TestCase):
    def setUp(self):
        pair = json.loads((FIXTURES / "gemma_prefill_pair.json").read_text())
        self.ref, self.shared = pair["reference"], pair["shared"]

    def report(self, reference, shared, exact=False, faster=True):
        return {"accepted_exact": exact, "timings_seconds": {"reference": 118.0, "shared": 64.0 if faster else 130.0},
                "stats": {"shared": {"actor_prefill_rows_saved": 10}},
                "differences": {"technical_errors": 0, "incomplete_probe": 0},
                "decision_differences": compare_prefill_decisions([reference], [shared])}

    def test_recorded_gemma_pair_differs_only_in_number_spelling(self):
        self.assertNotEqual(self.ref, self.shared)
        self.assertEqual(decision_view(self.ref), decision_view(self.shared))
        self.assertEqual(self.ref["arms"]["force_preserve"]["write"], self.shared["arms"]["force_preserve"]["write"])
        self.assertEqual(prefill_choice(self.report(self.ref, self.shared)), ("shared", "decision_equivalent"))

    def test_changed_decision_falls_back_to_reference(self):
        changed = deepcopy(self.shared)
        changed["arms"]["force_preserve"]["regen"]["proposal"]["args"]["recipient"] = "DE00000000000000000000"
        report = self.report(self.ref, changed)
        self.assertEqual(report["decision_differences"]["decision_different_rows"], 1)
        self.assertEqual(prefill_choice(report), ("reference", "fallback_reference_decoding"))

    def test_slower_shared_path_falls_back(self):
        self.assertEqual(prefill_choice(self.report(self.ref, self.shared, faster=False)),
                         ("reference", "fallback_reference_decoding"))

    def test_exact_match_keeps_shared(self):
        self.assertEqual(prefill_choice(self.report(self.ref, self.ref, exact=True)), ("shared", "exact_match"))


class HardwareTests(unittest.TestCase):
    def test_gpu_3_only(self):
        self.assertEqual(ALLOWED_GPUS, (3,))
        self.assertEqual(set(PINNED_UUIDS), {3})
        self.assertEqual(AMENDMENT["id"], "D0-20261109")


if __name__ == "__main__":
    unittest.main()
