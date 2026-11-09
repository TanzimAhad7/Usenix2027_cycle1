import json
import math
import os
from pathlib import Path
import tempfile
import unittest

from bridge.batching import BatchEngine, BlockEngine, bounded_inference, schedule
from bridge.live import Native, action_parts, parse, qualify_runtime, run_bridge, workflow
from bridge.plan import ARMS, bodies, compact, make_plan, user_text
from bridge.report import endpoint, first_witness, fixed_report, live_report
from design import ROOT, digest, read


class BridgeDesign(unittest.TestCase):
    def test_frozen_population_and_independent_manipulations(self):
        p = make_plan()
        self.assertEqual(p, read(ROOT / "data" / "bridge_plan.json"))
        self.assertEqual((len(p["bases"]), len(p["fixed"]), len(p["episodes"])), (108,3456,1728))
        self.assertEqual(len({c["id"] for c in p["fixed"] + p["episodes"]}), 5184)
        self.assertEqual(len({b["id"].rsplit(".", 1)[0] for b in p["bases"]}), 18)
        self.assertEqual({b["action"] for b in p["bases"]}, {
            "send_money", "schedule_transaction", "send_email", "send_channel_message", "send_direct_message"})
        for base in p["bases"]:
            c = {"linked": 1, "source": 0, "copy": 1, "attack": 0, "flex": 0}
            destination = base["good"][base["identifier"]]
            if isinstance(destination, list):
                destination = destination[0]
            self.assertNotIn(destination, bodies(base,c)[0])
            self.assertNotIn(destination, user_text(base,c | {"source": 1}))
            self.assertNotIn(base["case"][1:], destination)
            self.assertEqual(bodies(base,c), bodies(base,c | {"linked": 0, "flex": 1}))
            self.assertEqual(user_text(base,c), user_text(base,c | {"attack": 1, "copy": 0}))
            self.assertEqual(bodies(base,c)[1], bodies(base,c | {"attack": 1})[1])
            self.assertNotEqual(bodies(base,c)[0], bodies(base,c | {"attack": 1})[0])

    def test_actor_boundary(self):
        self.assertEqual(parse('```json\n{"final":"done"}\n```'), {"final":"done"})
        for raw in ('{"final":"one","final":"two"}', '{"function":"x","args":{"n":NaN}}',
                    '{"function":"x","args":[]}','{"final":"done"} extra'):
            self.assertIsNone(parse(raw))

    def test_empty_results_are_incomplete_and_bounded(self):
        p = make_plan()
        families = {b["id"]: b["family"] for b in p["bases"]}
        self.assertFalse(any(fixed_report(p, [], families)["predictions"].values()))
        a = live_report(p, [], families)
        self.assertEqual(a["scheduled"], 12096)
        self.assertEqual(a["horizon_sensitivity_bounds"]["flex0/attack1/scalar/target_harm"], [0,1])
        self.assertFalse(a["contrasts"]["parameter"]["prediction"])


@unittest.skipUnless(os.getenv("E2E_TEST_NATIVE") and os.getenv("E0_TEST_TOKENIZER"), "Requires local tools/tokenizer")
class NativeProof(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from transformers import AutoTokenizer
        cls.tokenizer = AutoTokenizer.from_pretrained(os.environ["E0_TEST_TOKENIZER"], local_files_only=True)
        cls.plan = make_plan()

    def test_all_native_worlds_and_one_response_attack(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            qualify_runtime(os.environ["E2E_TEST_NATIVE"], path, self.plan)
            self.assertEqual(len(read(path / "native_qualification.json")), 216)

    def test_native_matched_policy_chain(self):
        b = self.plan["bases"][0]
        cell = next(c for c in self.plan["episodes"] if c["base"]==b["id"] and c["source"] and c["attack"]
                    and not c["flex"])
        proposed = {"function": b["action"], "args": b["alt"]}
        good = {"function": b["action"], "args": b["good"]}

        class Scripted:
            tokenizer = self.tokenizer
            def generate(self, chat, purpose):
                text = chat[0]["content"]
                if purpose == "sanitizer":
                    out = "Sanitized fixture"
                elif f'<TOOL_RESULT name="{b["action"]}">' in text:
                    out = compact({"final":"finished"})
                elif f'<TOOL_RESULT name="{b["primary"]["function"]}">' not in text:
                    out = compact(b["primary"])
                elif f'<TOOL_RESULT name="{b["preview"]["function"]}">' not in text:
                    out = compact(b["preview"])
                else:
                    out = compact(good if "Sanitized fixture" in text else proposed)
                yield from ()
                return {"id": digest([chat,purpose]), "text": out, "limit_reached": False}

            def score(self, prefixes, cids):
                t = action_parts(self.tokenizer, b, proposed)
                roles = t["roles"]
                # User deletion has no loss. Primary deletion loses only the
                # identifier term. Preview deletion is neutral.
                assert len(cids) == len(roles)
                vectors = [[-9.]*len(cids) for _ in prefixes]
                vectors[2] = [-12. if r=="identifier" else -9. for r in roles]
                yield from ()
                return [digest([p,cids]) for p in prefixes], vectors

        with tempfile.TemporaryDirectory() as tmp, Native(os.environ["E2E_TEST_NATIVE"], Path(tmp)/"native.log") as worker:
            rows = {}
            for arm in ARMS:
                with self.assertRaises(StopIteration) as done:
                    next(workflow(Scripted(), worker, b, cell, arm))
                rows[arm] = done.exception.value
        self.assertTrue(endpoint(rows["plain"])["target_harm"])
        self.assertTrue(endpoint(rows["scalar"])["utility"])
        self.assertTrue(endpoint(rows["without_id"])["target_harm"])
        self.assertTrue(endpoint(rows["placebo_id"])["utility"])
        self.assertFalse(endpoint(rows["authority"])["target_harm"])
        self.assertIsNotNone(first_witness(rows["scalar"],rows["without_id"],"target_harm"))

    def test_native_slots_keep_reads_and_commits_separate(self):
        b = self.plan["bases"][0]
        with tempfile.TemporaryDirectory() as tmp, Native(os.environ["E2E_TEST_NATIVE"], Path(tmp)/"native.log") as worker:
            attack, clean = worker.slot(0), worker.slot(1)
            c = {"source": 1, "linked": 1, "copy": 1, "attack": 1, "flex": 0}
            attack.open(b,c)
            clean.open(b,c | {"attack": 0})
            self.assertTrue(attack.call(b["primary"])["attack_delivered"])
            self.assertFalse(clean.call(b["primary"])["attack_delivered"])
            action = {"function": b["action"], "args": b["good"]}
            self.assertEqual(attack.call(action)["commits"][0]["class"], "preferred")
            self.assertEqual(clean.call(action)["commits"][0]["class"], "preferred")
            self.assertTrue(attack.call(action, enforce=True)["denied"])

    def test_two_lane_bridge_writes_every_arm(self):
        from collections import Counter

        b = self.plan["bases"][0]
        subset = dict(self.plan)
        subset["bases"] = [b]
        subset["fixed"] = [c for c in self.plan["fixed"]
                           if c["base"] == b["id"] and not c["source"] and c["copy"]][:2]
        subset["episodes"] = [c for c in self.plan["episodes"] if c["base"] == b["id"]][:2]

        class Stub:
            tokenizer = self.tokenizer
            label, lanes = "qwen", 2
            stats = Counter()

            def resolve(self, requests):
                self.stats["widest_round"] = max(self.stats["widest_round"], len(requests))
                result = {}
                for key, req in requests.items():
                    if req["kind"] == "score":
                        result[key] = [-3.0] * len(req["cids"])
                    else:
                        result[key] = {"id": key, "text": '{"final":"fixture"}', "limit_reached": False}
                return result

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            run_bridge(Stub(), os.environ["E2E_TEST_NATIVE"], out, subset)
            self.assertEqual(len(list((out / "fixed").glob("*.json"))), 2)
            self.assertEqual(len(list((out / "episodes").glob("*.json"))), 2 * len(ARMS))
            progress = read(out / "progress.json")
            self.assertEqual(progress["completed_blocks"], 4)
            self.assertEqual(progress["fixed_native_read_pairs"], 1)
            self.assertGreater(Stub.stats["widest_round"], 1)

    def test_all_fixed_proposals_have_correct_semantic_offsets(self):
        for b in self.plan["bases"]:
            for args in (b["good"],b["alt"]):
                t = action_parts(self.tokenizer,b,{"function":b["action"],"args":args})
                for role in ("identifier","parameter"):
                    positions = [x for x,r in zip(t["offsets"],t["roles"]) if r==role]
                    self.assertTrue(positions)
                    start, end = min(x[0] for x in positions), max(x[1] for x in positions)
                    value = args[b[role]]
                    if isinstance(value,list):
                        value = value[0]
                    self.assertIn(str(value), t["completion"][start:end])


@unittest.skipUnless(os.getenv("E0_TEST_TORCH") and os.getenv("E0_TEST_TOKENIZER")
                     and os.getenv("E2E_TEST_GEMMA"), "Requires CPU Torch and both chat tokenizers")
class GenerateProof(unittest.TestCase):
    def test_real_small_models_score_generate_and_record(self):
        import torch
        from transformers import (AutoTokenizer, Gemma3Config, Gemma3ForConditionalGeneration,
                                  Qwen3Config, Qwen3ForCausalLM)
        torch.manual_seed(151)
        torch.set_num_threads(1)
        for label,path in (("qwen","E0_TEST_TOKENIZER"),("gemma","E2E_TEST_GEMMA")):
            with self.subTest(model=label), tempfile.TemporaryDirectory() as tmp:
                tok = AutoTokenizer.from_pretrained(os.environ[path],local_files_only=True)
                cfg = dict(vocab_size=len(tok), hidden_size=16, intermediate_size=24, num_hidden_layers=1,
                           num_attention_heads=2, num_key_value_heads=1, head_dim=8, max_position_embeddings=2048)
                if label == "qwen":
                    model = Qwen3ForCausalLM(Qwen3Config(**cfg, eos_token_id=tok.eos_token_id)).eval()
                else:
                    model = Gemma3ForConditionalGeneration(Gemma3Config(
                        text_config=cfg | dict(num_hidden_layers=2, layer_types=["sliding_attention", "full_attention"],
                                               sliding_window=8, eos_token_id=tok.eos_token_id),
                        vision_config=dict(hidden_size=16, intermediate_size=24, num_hidden_layers=1,
                                           num_attention_heads=2, patch_size=4, image_size=16))).eval()
                e = BatchEngine(model,tok,"cpu",Path(tmp),label,2)
                try:
                    probe = e.qualify_generation()
                    self.assertTrue(probe["exact_match"], probe)
                    self.assertNotEqual(*probe["input_lengths"])
                    cids = tok.encode("foo",add_special_tokens=False)
                    generate = model.generate

                    def short_generate(**kwargs):
                        return generate(**(kwargs | {"max_new_tokens": 2}))

                    model.generate = short_generate

                    def job(index, lane):
                        engine = BlockEngine(e, str(index))
                        chat = [{"role":"user","content":f"Return JSON for {index % 2}."}]
                        g = yield from engine.generate(chat, "actor")
                        cached = yield from engine.generate(chat, "actor")
                        self.assertEqual(g, cached)
                        _,v = yield from engine.score(["Test A","Test B"],cids)
                        return g, v

                    rows = list(schedule([0, 1], job, e.resolve, e.lanes))
                    replayed = list(schedule([2, 3], job, e.resolve, e.lanes))
                    self.assertEqual(rows, replayed)
                finally:
                    e.close()
                self.assertEqual(e.stats["generation_max_batch"], 2)
                self.assertEqual(e.stats["generation_requests"], 2)
                self.assertEqual(e.stats["score_max_batch"], 2)
                self.assertEqual(e.stats["score_requests"], 2)
                self.assertEqual(e.stats["generation_cache_hits"], 2)
                self.assertEqual(e.stats["score_cache_hits"], 2)
                for g,v in rows:
                    self.assertIn("text",g)
                    self.assertTrue(all(math.isfinite(x) for vec in v for x in vec))
                entries = [json.loads(line) for line in (Path(tmp)/"requests.jsonl").read_text().splitlines()]
                self.assertEqual({r["kind"] for r in entries}, {"actor","score"})
                self.assertEqual(len({r["id"] for r in entries}), len(entries))
                self.assertTrue(all(set(r["conditions"]) == {"0","1"} for r in entries if r["kind"] == "score"))
                source = {r["id"]: r for r in entries}
                reuse = [json.loads(line) for line in (Path(tmp)/"request_reuse.jsonl").read_text().splitlines()]
                self.assertEqual(len(reuse), 4)
                self.assertTrue(all(r["source_batch_index"] == source[r["id"]]["batch_index"] for r in reuse))
                self.assertTrue(all(set(r["conditions"]) == {"2","3"} for r in reuse if r["kind"] == "score"))

    def test_cuda_oom_split_preserves_order_and_eos_trims_padding(self):
        from collections import Counter
        from types import SimpleNamespace
        import torch

        def infer(rows):
            if len(rows) > 2:
                raise torch.cuda.OutOfMemoryError("test allocation")
            return list(rows)

        stats = Counter()
        batches = list(bounded_inference([1,2,3,4,5], infer, stats))
        self.assertEqual([value for _, vals in batches for value in vals], [1,2,3,4,5])
        self.assertEqual(stats["oom_splits"], 2)

        class Fake:
            generation_config = SimpleNamespace(eos_token_id=[2, 3])

            def generate(self, input_ids, attention_mask, **kwargs):
                self.assert_inputs(input_ids, attention_mask)
                return torch.cat((input_ids, torch.tensor([[5,2,0,0], [6,7,8,9]])), dim=1)

            @staticmethod
            def assert_inputs(ids, mask):
                assert ids.tolist() == [[0,11], [11,12]]
                assert mask.tolist() == [[0,1], [1,1]]

        tok = SimpleNamespace(pad_token_id=0, eos_token_id=2, decode=lambda ids, **kwargs: str(ids))
        requests = [{"id":"a","pids":[11],"limit":4}, {"id":"b","pids":[11,12],"limit":4}]
        with tempfile.TemporaryDirectory() as tmp:
            e = BatchEngine(Fake(),tok,"cpu",Path(tmp),"qwen",2)
            try:
                results = e.generate_group(requests)
            finally:
                e.close()
        self.assertEqual(results[0]["generated"], [5,2])
        self.assertFalse(results[0]["limit_reached"])
        self.assertTrue(results[1]["limit_reached"])
