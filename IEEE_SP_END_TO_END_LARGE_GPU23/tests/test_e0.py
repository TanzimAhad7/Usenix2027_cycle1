from collections import Counter
from dataclasses import asdict
import json
import os
from pathlib import Path
import tempfile
import unittest

from analyze import analyze, load_results
from design import MODELS, Cell, ROOT, blocks, digest, make_action, make_manifest, read, write
from prepare import compile_panel
from run import archive
from score import file_hash, logprobs, snapshot


class E0Design(unittest.TestCase):
    def test_frozen_design_exact_cells_and_actions(self):
        manifest = make_manifest()
        self.assertEqual(manifest, read(ROOT / "data" / "design.json"))
        self.assertEqual(len(set(c["id"] for c in manifest["cells"])), 9984)
        self.assertEqual(Counter(c["panel"] for c in manifest["cells"]),
                         dict(relocation=6144, echo=1536, redundancy=768, serialization=768, deletion=768))
        self.assertEqual(len(manifest["bases"]), 96)
        for base in manifest["bases"]:
            a, spans = make_action(base, "compact")
            b, _ = make_action(base, "pretty")
            self.assertEqual(json.loads(a), json.loads(b))
            for role, (x, y) in spans.items():
                self.assertEqual(a[x:y], str(base[role]))

    def test_foil_and_linkage_orthogonal_to_echo_text(self):
        manifest = make_manifest()
        for base in manifest["bases"]:
            c = Cell("echo", base["base"], copy=1)
            left = blocks(base, c, "full")
            right = blocks(base, Cell(**(asdict(c) | {"bound": 1})), "full")
            self.assertNotEqual(left[0], right[0])
            self.assertEqual(left[1:], right[1:])
            self.assertNotIn(base["identifier"], left[2][1])
            for role in ("identifier", "parameter"):
                x = Cell("relocation", base["base"], focal=role, lexical="split")
                self.assertNotIn(str(base[role]), "".join(b[1] for b in blocks(base, x, "full")))

    def test_snapshot_identity_uses_pinned_hash_and_refuses_escape(self):
        with tempfile.TemporaryDirectory() as d:
            cache = Path(d)
            label = "gemma"
            base = cache / "models--google--gemma-3-27b-it"
            rev = MODELS[label]["revision"]
            root = base / "snapshots" / rev
            root.mkdir(parents=True)
            for name in ("config.json", "tokenizer.json", "tokenizer_config.json", "model.safetensors"):
                (root / name).write_text("fixture")
            self.assertEqual(snapshot(cache, label)["revision"], rev)
            alternate = "a" * 40
            root.rename(base / "snapshots" / alternate)
            self.assertEqual(snapshot(cache, label, alternate)["revision"], alternate)
            (base / "snapshots" / alternate).rename(root)
            with self.assertRaises(FileNotFoundError):
                snapshot(cache, label, alternate)
            path = root / "model.safetensors"
            path.unlink()
            path.symlink_to("/etc/passwd")
            with self.assertRaises(ValueError):
                snapshot(cache, label)

    def test_partial_and_duplicate_shards(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "run"
            root.mkdir()
            write(root / "prepared.json", {"requests": {"a": {"cids": [1]}, "b": {"cids": [2]}}})
            write(root / "freeze.json", {"prepared_sha256": file_hash(root / "prepared.json")})
            (root / "batches").mkdir()
            write(root / "batches" / "000001.json", {"a": [-1.]})
            self.assertEqual(load_results(root)[1], {"a": [-1.]})
            self.assertTrue(archive(root).is_file())
            write(root / "batches" / "000002.json", {"a": [-2.]})
            with self.assertRaises(ValueError):
                load_results(root)

    def test_snapshot_follows_shared_cache_blobs_and_rejects_other_targets(self):
        with tempfile.TemporaryDirectory() as d:
            cache = Path(d)
            for label in ("qwen", "gemma"):
                with self.subTest(label=label):
                    profile = MODELS[label]
                    repo = cache / ("models--" + profile["hub"].replace("/", "--"))
                    root = repo / "snapshots" / profile["revision"]
                    root.mkdir(parents=True)
                    own_blobs = repo / "blobs"
                    own_blobs.mkdir()
                    shared_blobs = cache / "blobs" / ("02" if label == "qwen" else "ab")
                    shared_blobs.mkdir(parents=True)
                    shard = "model-00001-of-00001.safetensors"
                    index = "model.safetensors.index.json"
                    for name, target, content in (
                        ("config.json", own_blobs / "config", "{}"),
                        ("tokenizer_config.json", root / "tokenizer_config.json", "{}"),
                        ("tokenizer.json", shared_blobs / "tokenizer", "tokenizer bytes"),
                        (index, shared_blobs / "index", json.dumps({"weight_map": {"w": shard}})),
                        (shard, shared_blobs / "shard", "weight bytes"),
                    ):
                        target.write_text(content)
                        if target != root / name:
                            (root / name).symlink_to(os.path.relpath(target, root))
                    identity = snapshot(cache, label)
                    tokenizer = identity["files"]["tokenizer.json"]
                    self.assertEqual(identity["revision"], profile["revision"])
                    self.assertEqual(tokenizer["sha256"], file_hash(shared_blobs / "tokenizer"))
                    self.assertEqual(tokenizer["cache_relative_path"],
                                     (shared_blobs / "tokenizer").relative_to(cache).as_posix())
                    self.assertEqual(identity["weights_bytes"], len("weight bytes"))

                    # A link through the shared store still cannot escape the allowed roots.
                    foreign = cache / "foreign-index"
                    foreign.write_text("{}")
                    (shared_blobs / "index").unlink()
                    (shared_blobs / "index").symlink_to(foreign)
                    with self.assertRaisesRegex(ValueError, "Invalid cached file"):
                        snapshot(cache, label)
                    foreign.unlink()
                    with self.assertRaisesRegex(ValueError, "Cannot resolve cached file"):
                        snapshot(cache, label)


class E0Analysis(unittest.TestCase):
    @staticmethod
    def scored_fixture(signal=True):
        design = make_manifest()
        observations, scores = [], {}
        for raw in design["cells"]:
            c = Cell(**{k: v for k, v in raw.items() if k != "id"})
            refs = {v: f"{c.id}/{v}" for v in c.variants()}
            observations.append({"id": c.id, "requests": refs, "action": {
                "roles": ["identifier", "parameter", "other"],
                "strict_roles": ["identifier", "parameter", "other"]}})
            for v, key in refs.items():
                x = [-10., -10., -10.]
                f = int(c.focal == "parameter")
                if signal and c.panel != "echo" and v in ("mask_" + c.source, "delete_" + c.source):
                    x[f] -= .2 if c.backup else 3
                if signal and c.panel == "echo" and v in ("mask_u", "mask_u_echo"):
                    x[1] -= 3
                    if v == "mask_u" and c.bound and c.copy:
                        x[1] += 2
                scores[key] = x
        return {"label": "mock", "observations": observations, "requests": scores, "anchors": []}, scores, design

    def test_direction_control_and_negative_result(self):
        for good, decision in ((True, "REVIEW_SAME_WORKFLOW_BRIDGE"), (False, "REASSESS_MECHANISM_BEFORE_BRIDGE")):
            data, scores, design = self.scored_fixture(good)
            result, _ = analyze(data, scores, design)
            self.assertEqual(result["decision"], decision)
        data, scores, design = self.scored_fixture()
        scores.pop(next(iter(scores)))
        result, _ = analyze(data, scores, design)
        self.assertEqual(result["decision"], "INCOMPLETE")
        self.assertEqual(result["n_complete_cells"], 9983)


@unittest.skipUnless(os.getenv("E0_TEST_TOKENIZER"), "Requires a local Qwen tokenizer path")
class TokenBoundary(unittest.TestCase):
    def test_actual_tokenizer_complete_panel(self):
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(os.environ["E0_TEST_TOKENIZER"], local_files_only=True)
        manifest = make_manifest()
        prepared = compile_panel(manifest, tokenizer, "test")
        self.assertEqual(len(prepared["observations"]), 9984)
        self.assertEqual(len(prepared["anchors"]), 64)
        for row in prepared["observations"]:
            reqs = [prepared["requests"][key] for key in row["requests"].values()]
            self.assertEqual(len({tuple(r["cids"]) for r in reqs}), 1)
            if set(row["requests"]) != {"delete_u", "delete_s"}:
                self.assertEqual(len({len(r["pids"]) for r in reqs}), 1)
        print(f"Actual tokenizer compiled {len(prepared['requests'])} distinct inputs")


@unittest.skipUnless(os.getenv("E0_TEST_TORCH"), "Requires CPU Torch and Transformers")
class TeacherForcing(unittest.TestCase):
    def test_suffix_logits_equal_full_logits_for_real_architectures(self):
        import torch
        from transformers import Gemma3Config, Gemma3ForConditionalGeneration, Qwen3Config, Qwen3ForCausalLM

        torch.manual_seed(22)
        torch.set_num_threads(1)
        base = dict(vocab_size=128, hidden_size=32, intermediate_size=48, num_hidden_layers=2,
                    num_attention_heads=4, num_key_value_heads=2, head_dim=8, max_position_embeddings=128)
        qwen = Qwen3ForCausalLM(Qwen3Config(**base)).eval()
        gemma = Gemma3ForConditionalGeneration(Gemma3Config(
            text_config=base | dict(sliding_window=32, layer_types=["sliding_attention", "full_attention"]),
            vision_config=dict(hidden_size=32, intermediate_size=48, num_hidden_layers=1,
                               num_attention_heads=4, patch_size=4, image_size=16),
            image_token_index=127, boi_token_index=125, eoi_token_index=126, mm_tokens_per_image=4,
        )).eval()
        requests = [{"pids": [2, 3, 4, 5], "cids": [6, 7, 8]}, {"pids": [2, 10, 11, 12], "cids": [13, 14, 15]}]
        inputs = torch.tensor([r["pids"] + r["cids"] for r in requests])
        for model in (qwen, gemma):
            with self.subTest(model=type(model).__name__), torch.inference_mode():
                reference = model(input_ids=inputs, use_cache=False).logits[:, 3:6].float().log_softmax(-1)
                expected = reference.gather(-1, inputs[:, 4:].unsqueeze(-1)).squeeze(-1)
                actual = torch.tensor(logprobs(model, requests, "cpu"))
                self.assertTrue(torch.allclose(expected, actual, atol=2e-6, rtol=0))


if __name__ == "__main__":
    unittest.main()
