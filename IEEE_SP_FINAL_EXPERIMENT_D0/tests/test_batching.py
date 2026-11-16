from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from bridge.batching import BatchEngine
from design import make_plan
from run import phase_attempts, score_qualification
from score import logprobs, padded_logprobs

try:
    import torch
except ImportError:
    torch = None


class ReplayTests(unittest.TestCase):
    def test_replay_groups_seeds_without_dropping_attempts(self):
        plan = make_plan()
        attempts = phase_attempts(plan, "replay", "local")
        self.assertEqual(len(attempts), 9216)
        self.assertEqual(len({(cell["id"], seed) for cell, seed in attempts}), 9216)
        for start in range(0, len(attempts), 3):
            group = attempts[start:start + 3]
            self.assertEqual(len({cell["id"] for cell, _ in group}), 1)
            self.assertEqual(tuple(seed for _, seed in group), tuple(plan["seeds"]))
        self.assertEqual(len(phase_attempts(plan, "live", "local")), 2880)

    def test_score_gate_keeps_guard_decision_and_numeric_check(self):
        def row(scalar):
            span = {"index": 2, "primary": True, "scalar": scalar, "delta_tool": scalar,
                    "delta_user": 0.0, "parts": {"identifier": scalar},
                    "patched": {"remove_id": scalar, "equal_placebo": scalar, "margin_placebo": scalar},
                    "patch_tokens": None}
            result = {"spans": [span], "flags": [2] if scalar > 0 else []}
            return {"cell": {"id": "a"}, "status": "calibration_only", "scores": result,
                    "alternate_scores": result}

        self.assertTrue(score_qualification([row(0.01)], [row(0.011)])["pass"])
        self.assertFalse(score_qualification([row(0.01)], [row(0.02)])["pass"])
        self.assertFalse(score_qualification([row(0.0005)], [row(-0.0005)])["pass"])

    def test_resolver_batches_mixed_lengths_and_reuses_exact_inputs(self):
        requests = {str(i): {"id": str(i), "kind": "score", "conditions": ["a", "b", "c"],
                             "pids": list(range(i + 1)), "cids": [6]} for i in range(4)}
        batches = []

        def infer(_model, rows, _device, _pad):
            batches.append([row["id"] for row in rows])
            return [[-0.5] for _ in rows]

        fake_torch = SimpleNamespace(cuda=SimpleNamespace(OutOfMemoryError=MemoryError))
        with TemporaryDirectory() as directory:
            tokenizer = SimpleNamespace(pad_token_id=0, eos_token_id=0)
            engine = BatchEngine(None, tokenizer, None, Path(directory), "qwen", 48, score_mode="batch")
            try:
                with patch.dict("sys.modules", torch=fake_torch), patch("bridge.batching.padded_logprobs", infer):
                    first = engine.resolve(requests)
                    self.assertEqual(first, engine.resolve(requests))
                self.assertEqual(batches, [["3", "2", "1", "0"]])
                self.assertEqual(engine.stats["score_max_batch"], 4)
                self.assertEqual(engine.stats["score_cache_hits"], 4)
                self.assertEqual(first, {key: [-0.5] for key in requests})
            finally:
                engine.close()


@unittest.skipIf(torch is None, "PyTorch is unavailable")
class TensorTests(unittest.TestCase):
    def test_padding_preserves_positions_and_completion_alignment(self):
        class Toy:
            def __call__(self, input_ids, use_cache, logits_to_keep, attention_mask=None, position_ids=None):
                if attention_mask is None:
                    attention_mask = torch.ones_like(input_ids)
                    position_ids = torch.arange(input_ids.shape[1])[None, :]
                history = (input_ids * attention_mask).cumsum(-1)
                center = (history + position_ids) % 11
                logits = -(center[:, -logits_to_keep:, None] - torch.arange(11)[None, None, :]).float().square()
                return SimpleNamespace(logits=logits)

        rows = [{"pids": [2], "cids": [3]},
                {"pids": [3, 4, 5, 6], "cids": [7, 8, 9]},
                {"pids": [1, 2, 3], "cids": [6, 7]}]
        self.assertEqual(padded_logprobs(Toy(), rows, "cpu", 10),
                         [logprobs(Toy(), [row], "cpu")[0] for row in rows])
