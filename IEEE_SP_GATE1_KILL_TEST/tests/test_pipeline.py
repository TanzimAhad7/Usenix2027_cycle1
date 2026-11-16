"""Unattended pipeline: GPU pinning, smoke gate, control flow and evaluation bundle (no GPU, no model)."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock
import zipfile

import pipeline
from common import PINNED_GPUS


def args(tmp, mode="all"):
    return SimpleNamespace(mode=mode, profiles=["qwen", "gemma"], stamp="T_gate1_test", log=str(Path(tmp) / "p.log"),
                           cache="/c", native_python="/n", wait_gpu_hours=0.0)


class Hardware(unittest.TestCase):
    def test_gpu_3_only(self):
        self.assertEqual(PINNED_GPUS, {3: "GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6"})
        self.assertIn('"--gpu", "3"', Path(pipeline.__file__).read_text())


class Flow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        for d in ("logs", "runs"):
            (root / d).mkdir()
        (root / "code.py").write_text("print('x')\n")
        self.patch = mock.patch.object(pipeline, "ROOT", root)
        self.patch.start()
        self.root = root

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def fake_run(self, outcomes):
        def run_profile(p, profile, smoke):
            rid = f"{p.stamp}_{profile}{'_smoke' if smoke else ''}"
            d = self.root / "runs" / rid / f"model_{profile}"
            d.mkdir(parents=True)
            (d / "requests.jsonl").write_text("{}\n")
            (d.parent / "analysis.json").write_text("{}")
            r = {"run_id": rid, "smoke": smoke, **outcomes(profile, smoke)}
            p.state["runs"][rid] = r
            return r
        return run_profile

    def test_smoke_gate_blocks_full_run(self):
        bad = lambda profile, smoke: {"exit_code": 0, "episodes": 224, "expected": 224,
                                      "max_unparsed": 0.05 if profile == "gemma" else 0.0, "verdict": "x"}
        p = pipeline.Pipeline(args(self.tmp.name))
        with mock.patch.object(pipeline.Pipeline, "run_profile", self.fake_run(bad)):
            self.assertEqual(p.main(), 1)
        status = json.loads(p.status_path.read_text())
        self.assertEqual(status["phase"], "STOPPED_AT_SMOKE_GATE")
        self.assertEqual(len(status["runs"]), 2)
        self.assertTrue(Path(status["bundle"]["path"]).exists())

    def test_full_flow_writes_verdict_and_bundle(self):
        good = lambda profile, smoke: {"exit_code": 0, "episodes": 10, "expected": 10, "max_unparsed": 0.0,
                                       "verdict": "SURVIVES"}
        p = pipeline.Pipeline(args(self.tmp.name))

        def verdict(self_, full):
            self_.state["verdict"] = {"overall": "SURVIVES"}
            out = self.root / "runs" / f"gate1_verdict_{self_.stamp}.json"
            out.write_text("{}")
            return out
        with mock.patch.object(pipeline.Pipeline, "run_profile", self.fake_run(good)), \
                mock.patch.object(pipeline.Pipeline, "verdict", verdict):
            self.assertEqual(p.main(), 0)
        status = json.loads(p.status_path.read_text())
        self.assertEqual(status["phase"], "PIPELINE_COMPLETE")
        self.assertEqual(len(status["runs"]), 4)
        with zipfile.ZipFile(status["bundle"]["path"]) as z:
            names = set(z.namelist())
        self.assertIn("code/code.py", names)
        self.assertIn("BUNDLE_SHA256SUMS", names)
        self.assertIn("BUNDLE_README.txt", names)
        self.assertIn("runs/T_gate1_test_qwen/model_qwen/requests.jsonl", names)
        self.assertIn("logs/gate1_verdict_T_gate1_test.json", names)
        self.assertTrue(any(n.startswith("logs/") for n in names))


if __name__ == "__main__":
    unittest.main()
