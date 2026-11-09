from contextlib import ExitStack
from hashlib import sha256
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch
from zipfile import ZipFile

from design import read
from run import archive, reserve_gpus, run_profiles
from score import gpu_uuid, require_idle_gpu


WORKER = """
import argparse
import json
import os
from pathlib import Path
from time import monotonic, sleep

parser = argparse.ArgumentParser()
parser.add_argument("--model-dir", type=Path)
for key in ("cache", "gpu-index", "gpu-uuid", "native-python", "batch-lanes"):
    parser.add_argument("--" + key)
args = parser.parse_args()
out = args.model_dir
label = out.name.removeprefix("model_")
(out / "ready.json").write_text(json.dumps({"index": args.gpu_index, "uuid": args.gpu_uuid,
                                           "visible": os.environ["CUDA_VISIBLE_DEVICES"]}))
peer = "gemma" if label == "qwen" else "qwen"
checkpoint = out.parent.with_suffix(".after_qwen.zip")
wait_for = out.parent / ("model_" + peer) / "ready.json" if label == "qwen" else checkpoint
deadline = monotonic() + 15
while not wait_for.is_file():
    if monotonic() > deadline:
        raise RuntimeError("Expected overlap or checkpoint did not happen")
    sleep(0.02)
(out / "complete.txt").write_text(label)
raise SystemExit(int(os.environ["TEST_QWEN_EXIT"]) if label == "qwen" else 0)
"""


class ParallelRunner(TestCase):
    def test_parallel_profiles_pin_uuids_and_checkpoint_stable_files(self):
        for qwen_code in (0, 7):
            with self.subTest(qwen_code=qwen_code), TemporaryDirectory() as tmp, ExitStack() as ownership:
                root = Path(tmp)
                run = root / "run"
                (run / "source").mkdir(parents=True)
                (run / "source" / "score.py").write_text(WORKER)
                for label in ("qwen", "gemma"):
                    (run / ("model_" + label)).mkdir()
                with patch("run.gpu_uuid", side_effect=lambda idx: f"GPU-{idx}"), patch(
                    "run.require_idle_gpu"
                ), patch.dict(os.environ, {"TEST_QWEN_EXIT": str(qwen_code)}):
                    labels = ("qwen", "gemma")
                    bindings, descriptors = reserve_gpus(labels, root / "locks", ownership)
                    failed = run_profiles(run, labels, {"qwen": "a", "gemma": "b"}, bindings,
                                          descriptors, "native", 24)
                self.assertEqual(failed, ["qwen"] if qwen_code else [])
                for label, index in (("qwen", 2), ("gemma", 3)):
                    self.assertEqual(read(run / f"model_{label}/ready.json"),
                                     {"index": str(index), "uuid": f"GPU-{index}", "visible": f"GPU-{index}"})
                    self.assertTrue((run / f"model_{label}/complete.txt").is_file())
                self.assertEqual(read(run / "profile_timing.json")["profiles"]["qwen"]["exit_code"], qwen_code)
                with ZipFile(run.with_suffix(".after_qwen.zip")) as z:
                    self.assertIn("run/model_qwen/complete.txt", z.namelist())
                    self.assertFalse(any(p.startswith("run/model_gemma/") for p in z.namelist()))
                    for line in z.read("run/SHA256SUMS").decode().splitlines():
                        want, name = line.split("  ", 1)
                        self.assertEqual(sha256(z.read("run/" + name)).hexdigest(), want)
                with ZipFile(archive(run)) as z:
                    for label in labels:
                        self.assertIn(f"run/model_{label}/complete.txt", z.namelist())

    def test_reservation_checks_each_selected_gpu_and_rejects_collisions(self):
        with TemporaryDirectory() as tmp, ExitStack() as ownership, patch(
            "run.gpu_uuid", side_effect=lambda idx: f"GPU-{idx}"
        ), patch("run.require_idle_gpu") as idle:
            locks = Path(tmp)
            bindings, _ = reserve_gpus(["gemma"], locks, ownership)
            self.assertEqual(bindings, {"gemma": {"index": 3, "uuid": "GPU-3"}})
            idle.assert_called_once_with(3, "GPU-3")
            with ExitStack() as second, self.assertRaisesRegex(RuntimeError, "GPU 3 is reserved"):
                reserve_gpus(["gemma"], locks, second)

    def test_busy_peer_stops_the_launch_before_either_worker(self):
        bindings = {"qwen": {"index": 2, "uuid": "GPU-2"}, "gemma": {"index": 3, "uuid": "GPU-3"}}
        with TemporaryDirectory() as tmp, patch(
            "run.require_idle_gpu", side_effect=[None, RuntimeError("GPU 3 already has compute processes")]
        ), patch("run.subprocess.Popen") as launch, self.assertRaisesRegex(RuntimeError, "GPU 3 already"):
            run_profiles(Path(tmp), ("qwen", "gemma"), {}, bindings, {}, "native", 24)
        launch.assert_not_called()

    def test_gpu_queries_fail_closed_on_busy_or_ambiguous_output(self):
        with patch("score.subprocess.check_output", return_value="GPU-42\n") as command:
            self.assertEqual(gpu_uuid(2), "GPU-42")
            self.assertIn("2", command.call_args.args[0])
        with patch("score.subprocess.check_output", return_value="1919\n"):
            require_idle_gpu(2, "GPU-42", own_pid=1919)
            with self.assertRaisesRegex(RuntimeError, "already has compute"):
                require_idle_gpu(2, "GPU-42")
        with patch("score.subprocess.check_output", return_value="[Not Supported]"):
            with self.assertRaisesRegex(RuntimeError, "Could not verify"):
                require_idle_gpu(2, "GPU-42")
