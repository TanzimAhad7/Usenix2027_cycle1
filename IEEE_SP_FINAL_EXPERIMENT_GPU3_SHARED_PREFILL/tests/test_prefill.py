from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest

from bridge.batching import BatchEngine, prompt_fanout
from run import compare_prefill_probe

try:
    import torch
except ImportError:
    torch = None


class PrefillContractTests(unittest.TestCase):
    def test_fanout_only_shares_exact_token_sequences(self):
        rows = [{"pids": tokens, "seed": i} for i, tokens in
                enumerate(([4, 5], [3, 5], [4, 5], [4, 5, 0], [3, 5]))]
        self.assertEqual(prompt_fanout(rows), ([0, 1, 3], [0, 1, 0, 2, 1]))

    def test_replay_gate_rejects_any_changed_outcome_or_generated_token(self):
        row = {"cell": {"id": "probe"}, "seed": 1, "status": "complete", "policy_order": ["a", "b"]}
        reordered = row | {"policy_order": ["b", "a"]}
        same = compare_prefill_probe([row], [reordered], {"a": [1]}, {"a": [1]})
        self.assertFalse(any(same.values()))
        changed = compare_prefill_probe([row], [reordered | {"status": "unparsed"}], {"a": [1]}, {"a": [2]})
        self.assertEqual(changed["different_rows"], 1)
        self.assertEqual(changed["different_generated_tokens"], 1)


@unittest.skipIf(torch is None, "PyTorch is unavailable")
class PrefillTensorTests(unittest.TestCase):
    def test_generation_shares_first_forward_and_keeps_seeded_results(self):
        class Cache:
            def __init__(self, data):
                self.data = data

            def reorder_cache(self, indices):
                self.data = self.data.index_select(0, indices)

        class Toy(torch.nn.Module):
            generation_config = SimpleNamespace(eos_token_id=63)

            def __init__(self):
                super().__init__()
                self.shapes = []

            def forward(self, input_ids, attention_mask, position_ids, cache_position, past_key_values=None):
                self.shapes.append(tuple(input_ids.shape))
                self.assert_layout(input_ids, attention_mask, position_ids)
                center = input_ids.sum(-1) + position_ids[:, -1]
                if past_key_values is None:
                    cache = Cache(center)
                else:
                    cache = past_key_values
                    cache.data += center
                logits = -(cache.data[:, None, None] % 31 - torch.arange(64)[None, None, :]).float().abs()
                return SimpleNamespace(logits=logits, past_key_values=cache)

            @staticmethod
            def assert_layout(input_ids, attention_mask, position_ids):
                assert input_ids.shape[0] == attention_mask.shape[0] == position_ids.shape[0]

            def generate(self, input_ids, attention_mask, logits_processor, max_new_tokens, **_):
                inputs, cache = input_ids, None
                width = input_ids.shape[1]
                for step in range(max_new_tokens):
                    positions = (attention_mask.cumsum(-1) - 1).clamp_min(0)[:, -inputs.shape[1]:]
                    result = self(input_ids=inputs, attention_mask=attention_mask, position_ids=positions,
                                  cache_position=torch.arange(width) if step == 0 else torch.tensor([width + step - 1]),
                                  past_key_values=cache)
                    cache = result.past_key_values
                    scores = logits_processor[0](input_ids, result.logits[:, -1])
                    inputs = scores.argmax(-1, keepdim=True)
                    input_ids = torch.cat((input_ids, inputs), dim=1)
                    attention_mask = torch.cat((attention_mask, torch.ones_like(inputs)), dim=1)
                return input_ids

        model = Toy()
        tokenizer = SimpleNamespace(pad_token_id=0, eos_token_id=63, decode=lambda ids, **_: str(ids))
        requests = [{"id": str(i), "pids": pids, "seed": 11 + i, "limit": 4}
                    for i, pids in enumerate(([3, 5], [2, 8, 9], [3, 5], [2, 8, 9]))]
        with TemporaryDirectory() as directory:
            engine = BatchEngine(model, tokenizer, "cpu", Path(directory), "qwen", 48)
            try:
                reference = engine.generate_group(requests)
                self.assertEqual(model.shapes[0], (4, 3))
                model.shapes.clear()
                engine.shared_prefill = True
                self.assertEqual(reference, engine.generate_group(requests))
                self.assertEqual(model.shapes, [(2, 3), (4, 1), (4, 1), (4, 1)])
                self.assertEqual(engine.stats["actor_prefill_rows_saved"], 2)
                self.assertEqual(engine.stats["actor_prefill_token_slots_saved"], 6)
                self.assertFalse(model._forward_hooks or model._forward_pre_hooks)
            finally:
                engine.close()
