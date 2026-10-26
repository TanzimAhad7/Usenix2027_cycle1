import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('historical',Path(__file__).resolve().parents[1]/'scripts/historical_audit.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class HistoricalCorruptionTests(unittest.TestCase):
    def corrupted_view(self,target,change):
        original=module.DirectoryView
        class Corrupted(original):
            def read(self,name):
                data=super().read(name)
                if name==target:
                    rows=[json.loads(s) for s in data.decode().splitlines() if s.strip()]
                    rows=change(rows)
                    return ('\n'.join(json.dumps(r) for r in rows)+'\n').encode()
                return data
        return Corrupted
    def test_missing_source_condition_detected(self):
        target='studies/02_controlled_source_relocation/frozen_results/scorer_llama/condition_scores.jsonl'
        with patch.object(module,'DirectoryView',self.corrupted_view(target,lambda rows:rows[:-1])):
            with self.assertRaises(AssertionError):module.primitive_reanalysis()
    def test_corrupted_source_verdicts_detected(self):
        target='studies/02_controlled_source_relocation/frozen_results/scorer_llama/condition_scores.jsonl'
        def change(rows):
            for row in rows:row['CA_FLAG_0']=False
            return rows
        with patch.object(module,'DirectoryView',self.corrupted_view(target,change)):
            with self.assertRaises(AssertionError):module.primitive_reanalysis()
    def test_duplicate_live_schedule_detected(self):
        target='studies/08_live_end_to_end/frozen_results/scientific_v1/RUN_ROWS.jsonl'
        with patch.object(module,'DirectoryView',self.corrupted_view(target,lambda rows:[rows[1],*rows[1:]])):
            with self.assertRaises(AssertionError):module.primitive_reanalysis()
