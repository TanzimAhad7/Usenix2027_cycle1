"""Gate 1 tests. CPU only. Template tests need GATE1_CACHE (model cache with tokenizers);
native end-to-end tests need GATE1_NATIVE (AgentDojo 0.1.35 interpreter)."""
import json
import os
from pathlib import Path
import tempfile
import unittest

from analyze import decide, paired
from bridge import base_plan
from bridge.adapters import parse_json_action, parse_qwen_native, render
from bridge.gate1_plan import (ARMS, BASE_IDS, BASE_PLAN_DIGEST, CARRIER_FAMILIES, PROSE_COMMENT, bodies,
                               effective_base, make_plan, oracle_clean, user_text)
from bridge.gate1_plan import compact
from common import ROOT, digest, read

PLAN = make_plan()
BASES = {b["id"]: b for b in PLAN["bases"]}


class PlanTests(unittest.TestCase):
    def test_frozen_population(self):
        self.assertEqual(digest(base_plan.make_plan()), BASE_PLAN_DIGEST)
        self.assertEqual(PLAN, read(ROOT / "data" / "gate1_plan.json"))
        self.assertEqual(len(PLAN["bases"]), 12)
        self.assertIn("banking.3.0", BASES)  # E13/E14 witness
        self.assertEqual(len(PLAN["cells"]), 384)
        self.assertEqual(len({c["id"] for c in PLAN["cells"]}), 384)
        self.assertEqual(len(ARMS), 7)
        self.assertEqual({b["family"] for b in PLAN["bases"]}, {"banking", "workspace", "slack"})
        for c in PLAN["cells"]:
            self.assertIn(BASES[c["base"]]["family"], CARRIER_FAMILIES[c["carrier"]])
            self.assertEqual((c["flex"], c["attack"], c["copy"]), (0, 0, 1))
        full = {b["id"]: b for b in base_plan.make_plan()["bases"]}
        for bid in BASE_IDS:
            self.assertEqual(BASES[bid], full[bid])

    def test_contract_and_instruction_do_not_change_with_carrier(self):
        for b in PLAN["bases"]:
            for source in (0, 1):
                texts = {user_text(b, {"source": source, "linked": 0, "flex": 0, "carrier": c})
                         for c in CARRIER_FAMILIES if b["family"] in CARRIER_FAMILIES[c] and c != "text_only"}
                self.assertEqual(len(texts), 1)
                if b["family"] in CARRIER_FAMILIES["text_only"]:
                    cell = {"source": source, "linked": 0, "flex": 0, "carrier": "text_only"}
                    eb = effective_base(b, cell)
                    self.assertEqual((eb["good"], eb["alt"], eb["action"]), (b["good"], b["alt"], b["action"]))
                    self.assertIn(eb["primary"]["function"], ("read_file", "get_webpage"))
                    # Only the named read call differs in the instruction.
                    plain = user_text(b, cell).replace(compact(b["primary"]), "R").replace(compact(b["preview"]), "P")
                    text = user_text(eb, cell).replace(compact(eb["primary"]), "R").replace(compact(eb["preview"]), "P")
                    self.assertEqual(plain, text)

    def test_carrier_bodies(self):
        for b in PLAN["bases"]:
            for source in (0, 1):
                cell = {"source": source, "copy": 1, "attack": 0, "linked": 0}
                built = bodies(b, cell | {"carrier": "as_built"})
                for carrier in ("neutral", "structured"):
                    self.assertEqual(bodies(b, cell | {"carrier": carrier}), built)
                if b["family"] in CARRIER_FAMILIES["text_only"]:
                    self.assertEqual(bodies(b, cell | {"carrier": "text_only"}), bodies(b, cell | {"carrier": "prose"}))
                primary, preview = bodies(b, cell | {"carrier": "prose"})
                good, alt, i, p = b["good"], b["alt"], b["identifier"], b["parameter"]
                self.assertNotIn("alternate", primary + preview)
                self.assertNotIn(str(alt[p]), primary + preview)
                ident = good[i][0] if isinstance(good[i], list) else good[i]
                self.assertEqual(ident in primary, bool(source))
                self.assertIn(PROSE_COMMENT, primary)

    def test_oracle_deletes_only_the_comment(self):
        for b in PLAN["bases"]:
            for carrier in ("as_built", "prose"):
                cell = {"source": 1, "copy": 1, "attack": 0, "linked": 0, "carrier": carrier}
                primary, clean = oracle_clean(b, cell)
                self.assertLess(len(clean), len(primary))
                self.assertNotIn("comment", clean)
                self.assertNotIn(PROSE_COMMENT, clean)
                good, i, p = b["good"], b["identifier"], b["parameter"]
                for value in (good[i][0] if isinstance(good[i], list) else good[i], good[p]):
                    rendered = value if isinstance(value, str) else json.dumps(value)
                    self.assertIn(rendered, clean)


class SmokeRegression(unittest.TestCase):
    """Real Qwen outputs that the V2 parsers rejected in smoke run 20261110T170146Z (amendment A1)."""
    def test_recorded_outputs_parse(self):
        rows = json.loads((Path(__file__).parent / "fixtures" / "qwen_smoke_unparsed.json").read_text())
        self.assertEqual({r["adapter"] for r in rows}, {"flat", "role"})
        for r in rows:
            got = (parse_qwen_native if r["adapter"] == "role" else parse_json_action)(r["text"])
            self.assertIsNotNone(got, r["text"][:200])
            if r["adapter"] == "flat":
                self.assertEqual(set(got), {"function", "args"})
            else:
                self.assertEqual(len(got["calls"]), 2)

    def test_limit_after_closed_turn(self):
        from bridge.adapters import actor
        text = ('<TOOL_CALL>send_channel_message({"body":"b","channel":"c"})</TOOL_CALL>\n</ASSISTANT>\n</think>\n'
                '<TOOL_RESULT name="x">\n{}\n</TOOL_RESULT>\n<ASSISTANT><think>\nOkay, let')

        class Engine:
            label = "qwen"

            def __init__(self, text):
                self.text = text

            def generate(self, chat, purpose, tools=None):
                if False:
                    yield
                return {"text": self.text, "limit_reached": True}
        messages, schemas = transcript(BASES["slack.0.0"])
        for adapter, text_, expected in (("flat", text, {"function": "send_channel_message",
                                                          "args": {"body": "b", "channel": "c"}}),
                                         ("flat", '<TOOL_CALL>send_channel_message({"body":"b', None),
                                         ("role", text, None)):
            gen = actor(Engine(text_), messages, adapter, schemas)
            try:
                next(gen)
            except StopIteration as done:
                self.assertEqual(done.value[1], expected, adapter)

    def test_flat_end_of_turn(self):
        call = '<TOOL_CALL>send_money({"amount":1.0})</TOOL_CALL>'
        self.assertEqual(parse_json_action(call + '\n</ASSISTANT>\n<think>\n</think>\n\n{"final":"x"}'),
                         {"function": "send_money", "args": {"amount": 1.0}})
        self.assertIsNone(parse_json_action("Sure: " + call + "\n</ASSISTANT>"))


class ParserTests(unittest.TestCase):
    def test_flat_parser(self):
        call = {"function": "send_money", "args": {"amount": 1.0}}
        self.assertEqual(parse_json_action(json.dumps(call)), call)
        self.assertEqual(parse_json_action("```json\n" + json.dumps(call) + "\n```"), call)
        self.assertEqual(parse_json_action('<TOOL_CALL>send_money({"amount":1.0})</TOOL_CALL>'), call)
        for bad in ('{"final":"a","final":"b"}', 'Sure. {"final":"x"}', '{"function":"x","args":[]}'):
            self.assertIsNone(parse_json_action(bad))

    def test_qwen_native_parser(self):
        text = '<tool_call>\n{"name": "send_money", "arguments": {"amount": 1.0}}\n</tool_call>'
        self.assertEqual(parse_qwen_native(text), {"function": "send_money", "args": {"amount": 1.0}})
        self.assertEqual(parse_qwen_native("<think>\n\n</think>\n\n" + text), parse_qwen_native(text))
        self.assertEqual(parse_qwen_native("Done."), {"final": "Done."})
        two = parse_qwen_native(text + "\n" + text)  # amendment A1: several native calls in one turn
        self.assertEqual(two, {"calls": [parse_qwen_native(text)] * 2})
        self.assertIsNone(parse_qwen_native("Sure. " + text))
        self.assertIsNone(parse_qwen_native('<tool_call>{"name": "x"}</tool_call>'))
        self.assertIsNone(parse_qwen_native(""))


def transcript(base):
    """System, user, one read call and its result, as the bridge stores them."""
    from bridge.live import initial
    schemas = {base["primary"]["function"]: {"type": "object", "properties": {}},
               base["action"]: {"type": "object", "properties": {}}}
    cell = {"source": 1, "linked": 0, "flex": 0, "carrier": "as_built", "copy": 1, "attack": 0}
    messages = initial(base, cell, schemas)
    messages += [{"role": "assistant", "content": "", "tool_calls": [base["primary"]]},
                 {"role": "tool", "content": "[{\"subject\":\"x\"}]", "error": None, "tool_call": base["primary"],
                  "primary_delivered": True}]
    return messages, schemas


@unittest.skipUnless(os.getenv("GATE1_CACHE"), "Needs GATE1_CACHE with the cached tokenizers")
class TemplateTests(unittest.TestCase):
    def test_both_models_render_both_adapters(self):
        from transformers import AutoTokenizer
        from bridge.batching import generation_request
        from common import MODELS
        from score import snapshot
        for label in ("qwen", "gemma"):
            tok = AutoTokenizer.from_pretrained(snapshot(os.environ["GATE1_CACHE"], label)["path"],
                                                local_files_only=True, use_fast=True)
            for base in PLAN["bases"]:
                messages, schemas = transcript(base)
                for adapter in ("flat", "role"):
                    chat, tools, _ = render(label, adapter, messages, schemas)
                    req = generation_request(tok, label, chat, "actor", 160, tools)
                    text = tok.decode(req["pids"])
                    if adapter == "role":
                        self.assertNotIn("<TOOL_RESULT", text)
                        self.assertIn(base["primary"]["function"], text)
                        if label == "qwen":
                            self.assertIn("<tools>", text)
                            self.assertIn("<tool_response>", text)
                    else:
                        self.assertIn("<TOOL_RESULT", text)
            self.assertIn(label, MODELS)

    def test_sanitizer_system_role_is_identical_for_gemma_only(self):
        from transformers import AutoTokenizer
        from bridge.batching import generation_request
        from score import snapshot
        det = read(ROOT / "data" / "historical_guard.json")["detector"]
        text = det["sanitizer_user_template"].format(user_request="u", tool_name="t", untrusted_content="c")
        flat = [{"role": "user", "content": det["sanitizer_system_prompt"] + "\n\n" + text}]
        role = [{"role": "system", "content": det["sanitizer_system_prompt"]}, {"role": "user", "content": text}]
        for label, same in (("gemma", True), ("qwen", False)):
            tok = AutoTokenizer.from_pretrained(snapshot(os.environ["GATE1_CACHE"], label)["path"],
                                                local_files_only=True, use_fast=True)
            a = generation_request(tok, label, flat, "sanitizer", 384)["pids"]
            b = generation_request(tok, label, role, "sanitizer", 384)["pids"]
            self.assertEqual(a == b, same, label)


class Scripted:
    """Deterministic stand-in for the model. It reads the primary record, then the preview, then
    writes using the identifier it can still see in the transcript; if the identifier is gone it
    falls back to the account's own IBAN (the substitution the bridge observed). The sanitizer
    returns the record without its value blob."""
    label = "qwen"

    def __init__(self, base, multi=False):
        self.base, self.multi = base, multi

        class Tok:
            def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
                return {"input_ids": [ord(c) for c in text], "offset_mapping": [(i, i + 1) for i in range(len(text))]}

            def encode(self, text, add_special_tokens=True):
                return [ord(c) for c in text]
        self.tokenizer = Tok()

    def generate(self, chat, purpose, tools=None):
        if False:
            yield
        text = json.dumps(chat)
        if purpose == "sanitizer":
            return {"text": '[{"amount":0.0,"recipient":"DE0000000000","subject":"record"}]', "limit_reached": False}
        b = self.base
        flat = len(chat) == 1
        tool_turns = (chat[0]["content"].count("<TOOL_RESULT") if flat else
                      sum(m["role"] == "tool" for m in chat))
        if tool_turns == 0:
            call = b["primary"]
        elif tool_turns == 1:
            call = b["preview"]
        elif tool_turns == 2:
            args = dict(b["good"])
            if b["good"][b["identifier"]] not in text:
                args[b["identifier"]] = "DE0000000000"
            call = {"function": b["action"], "args": args}
        else:
            return {"text": "Done." if not flat else '{"final":"done"}', "limit_reached": False}
        if flat:
            return {"text": json.dumps(call), "limit_reached": False}
        native = lambda c: "<tool_call>\n" + json.dumps({"name": c["function"], "arguments": c["args"]}) + "\n</tool_call>"
        if self.multi and tool_turns == 0:  # both reads in one native turn (amendment A1)
            return {"text": native(b["primary"]) + "\n" + native(b["preview"]), "limit_reached": False}
        return {"text": native(call), "limit_reached": False}

    def score(self, prefixes, cids):
        if False:
            yield
        n = len(cids)
        vectors = [[0.0] * n, [-0.1] * n, [-1.0] * n] + [[-0.05] * n for _ in prefixes[3:]]
        return [f"r{i}" for i in range(len(prefixes))], vectors


@unittest.skipUnless(os.getenv("GATE1_NATIVE"), "Needs GATE1_NATIVE (AgentDojo 0.1.35 interpreter)")
class NativeEndToEnd(unittest.TestCase):
    def run_arm(self, base, cell, arm, multi=False):
        from bridge.live import Native, workflow
        with tempfile.TemporaryDirectory() as tmp, Native(os.environ["GATE1_NATIVE"], Path(tmp) / "n.log") as rt:
            # The scripted model must follow the cell's own read calls (text_only uses plain-document reads).
            gen = workflow(Scripted(effective_base(base, cell), multi), rt.slot(0), base, cell, arm)
            try:
                next(gen)
            except StopIteration as done:
                return done.value
        raise AssertionError("Scripted engine should never yield")

    def classes(self, result):
        return [c["class"] for e in result["events"] for c in ((e.get("result") or {}).get("commits") or [])]

    def test_every_arm_on_the_witness(self):
        base = BASES["banking.3.0"]
        for adapter in ("flat", "role"):
            for carrier in ("as_built", "prose", "text_only"):
                cell = {"id": "t", "base": base["id"], "carrier": carrier, "adapter": adapter, "source": 1,
                        "linked": 0, "copy": 1, "flex": 0, "attack": 0}
                got = {arm: self.run_arm(base, cell, arm) for arm in ARMS}
                self.assertEqual(self.classes(got["plain"]), ["preferred"], (adapter, carrier))
                self.assertEqual(self.classes(got["oracle_clean"]), ["preferred"], (adapter, carrier))
                self.assertEqual(self.classes(got["forced_sanitize"]), ["other_out_of_contract"])
                self.assertEqual(self.classes(got["forced_sanitize_sysrole"]), ["other_out_of_contract"])
                self.assertEqual(self.classes(got["null_clean"]), ["other_out_of_contract"])
                self.assertEqual(self.classes(got["scalar"]), ["other_out_of_contract"])
                self.assertEqual(self.classes(got["authority"]), ["preferred"])
                forced = next(e for e in got["forced_sanitize"]["events"] if e.get("transform"))
                self.assertNotIn(base["good"]["recipient"], forced["primary_after"])

    def test_multi_call_turn_runs_in_order(self):
        base = BASES["banking.3.0"]
        cell = {"id": "t", "base": base["id"], "carrier": "text_only", "adapter": "role", "source": 1,
                "linked": 0, "copy": 1, "flex": 0, "attack": 0}
        for arm, expected in (("plain", ["preferred"]), ("forced_sanitize", ["other_out_of_contract"]),
                              ("oracle_clean", ["preferred"])):
            got = self.run_arm(base, cell, arm, multi=True)
            self.assertEqual(self.classes(got), expected, arm)
            self.assertTrue(got["events"][1]["actor"].get("from_multi_call"))
            self.assertTrue(got["events"][0]["result"]["primary_delivered"])
            self.assertTrue(got["events"][1]["result"]["preview_seen"])

    def test_qualification_covers_every_world(self):
        from bridge.live import qualify_runtime
        with tempfile.TemporaryDirectory() as tmp:
            receipts = qualify_runtime(os.environ["GATE1_NATIVE"], Path(tmp), PLAN)
        self.assertEqual(len(receipts), sum(2 for b in PLAN["bases"] for c in CARRIER_FAMILIES
                                            if b["family"] in CARRIER_FAMILIES[c]))


class DecisionTests(unittest.TestCase):
    def rows(self, arm_violation):
        rows = []
        for base in ("b1", "b2", "b3"):
            for linked in (0, 1):
                for arm, v in (("plain", 0), ("forced_sanitize", arm_violation)):
                    rows.append({"adapter": "role", "carrier": "prose", "source": 1, "base": base,
                                 "linked": linked, "arm": arm, "violation": v})
        return rows

    def test_paired(self):
        c = paired(self.rows(1), "role", "prose", 1, "forced_sanitize")
        self.assertEqual((c["mean"], c["bases"], c["cells"]), (1.0, 3, 6))

    def contrasts(self, anchor, role_forced, role_scalar, text_only=None):
        c = {"flat|as_built|s1|scalar-plain|violation": {"mean": anchor}}
        for carrier in ("neutral", "prose", "text_only"):
            forced = text_only if (carrier == "text_only" and text_only is not None) else role_forced
            for arm, value in (("forced_sanitize", forced), ("forced_sanitize_sysrole", forced), ("scalar", role_scalar)):
                c[f"role|{carrier}|s1|{arm}-plain|violation"] = {"mean": value}
        return c

    def test_rule(self):
        ok = {"a": 0.0}
        self.assertEqual(decide(self.contrasts(0.2, 0.15, 0.1), ok, 10, 10)[0], "SURVIVES")
        self.assertEqual(decide(self.contrasts(0.2, 0.15, 0.1, text_only=0.0), ok, 10, 10)[0], "INCONCLUSIVE")
        self.assertEqual(decide(self.contrasts(0.2, 0.0, 0.02), ok, 10, 10)[0], "KILLED")
        self.assertEqual(decide(self.contrasts(0.2, 0.06, 0.0), ok, 10, 10)[0], "INCONCLUSIVE")
        self.assertEqual(decide(self.contrasts(0.0, 0.3, 0.3), ok, 10, 10)[0], "ANCHOR_NOT_REPLICATED")
        self.assertEqual(decide(self.contrasts(0.2, 0.3, 0.3), {"a": 0.02}, 10, 10)[0], "INVALID_INTERFACE")
        self.assertEqual(decide(self.contrasts(0.2, 0.3, 0.3), ok, 9, 10)[0], "INCOMPLETE")


if __name__ == "__main__":
    unittest.main()
