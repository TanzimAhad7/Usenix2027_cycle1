import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from analysis import cluster_effect, induced, subtract, threshold_calibration
from design import make_plan, wire_text


class DesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = make_plan()
        cls.bases = {base["id"]: base for base in cls.plan["bases"]}

    def test_population_and_disjoint_ids(self):
        self.assertEqual(len(self.bases), 262)
        self.assertEqual(
            Counter(cell["stage"] for cell in self.plan["cells"]),
            Counter(cal=12, replay=3072, live=960),
        )
        stage_bases = {
            stage: {base["id"] for base in self.plan["bases"] if base["id"].startswith(stage + ".")}
            for stage in ("cal", "replay", "live")
        }
        self.assertFalse(stage_bases["cal"] & stage_bases["replay"])
        self.assertFalse(stage_bases["cal"] & stage_bases["live"])
        self.assertFalse(stage_bases["replay"] & stage_bases["live"])

    def test_edits_are_character_length_matched(self):
        for base in self.plan["bases"]:
            cell = {"stage": base["id"].split(".", 1)[0], "layout": "json", "duplicate": False, "echo": False}
            lengths = {
                len(wire_text(base, cell | {"edit": edit}))
                for edit in ("none", "benign", "hostile")
            }
            self.assertEqual(len(lengths), 1)

    def test_forced_controls_are_edit_paired(self):
        groups = {}
        for cell in self.plan["cells"]:
            if cell["stage"] != "replay":
                continue
            key = (
                cell["base"], cell["trusted"], cell["layout"], cell["echo"], cell["duplicate"]
            )
            groups.setdefault(key, set()).add(cell["force"])
        self.assertTrue(groups)
        self.assertTrue(all(values in ({True}, {False}) for values in groups.values()))
        forced = sum(next(iter(values)) for values in groups.values())
        self.assertGreater(forced, 0)
        self.assertLess(forced, len(groups))


class AnalysisTests(unittest.TestCase):
    def test_guard_induced_definition(self):
        self.assertEqual(induced(True, "lawful", "material", False), 1)
        self.assertEqual(induced(False, "lawful", "material", False), 0)
        self.assertEqual(induced(True, "material", "material", False), 0)
        self.assertIsNone(induced(True, None, "material", True))

    def test_missing_outcome_bounds(self):
        self.assertEqual(subtract(None, 1), (-1, 0))
        self.assertEqual(subtract(1, None), (0, 1))
        self.assertEqual(subtract(1, 0), (1, 1))

    def test_template_clusters_define_point_estimate(self):
        rows = [
            ("banking", "b1", 1, 1, 1),
            ("banking", "b1", 0, 0, 0),
            ("workspace", "w1", -1, -1, -1),
        ]
        result = cluster_effect(rows, repetitions=50)
        self.assertEqual(result["complete_case_template_mean"], -0.25)
        self.assertEqual(result["complete_template_counts"], {"banking": 1, "workspace": 1})

    def test_rate_calibration_is_sealed_input_only(self):
        rows = [
            {
                "scores": {
                    "spans": [
                        {"primary": True, "scalar": scalar, "patched": {"remove_id": patched}}
                    ]
                }
            }
            for scalar, patched in ((0.8, 0.4), (0.3, -0.1), (-0.2, -0.5))
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "calibration.jsonl"
            path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            result = threshold_calibration(iter_json(path))
        self.assertEqual(result["eligible"], 3)
        self.assertEqual(result["remove_id_triggered"], 1)
        self.assertEqual(result["threshold_triggered"], 1)


def iter_json(path):
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


if __name__ == "__main__":
    unittest.main()
