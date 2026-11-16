import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from permission_admission.device import GPU_UUID, LOCK_NAME, qualify_available


class Placement(unittest.TestCase):
    def test_pinned_gpu2_and_no_fallback(self):
        serving = Mock()
        serving.gpu_table.return_value = [['2', GPU_UUID, '0', '95830']]
        serving.gpu_applications.return_value = []
        self.assertEqual(qualify_available(serving)[0], '2')
        self.assertEqual(serving.GPU, 2)
        self.assertEqual(LOCK_NAME, 'gpu2_sequence.lock')
        for rows in ([], [['3', GPU_UUID]], [['2', 'WRONG_UUID']]):
            serving.gpu_table.return_value = rows
            with self.assertRaisesRegex(RuntimeError, 'no other GPU'):
                qualify_available(serving)

    def test_foreign_gpu2_process_blocks_but_gpu3_does_not(self):
        serving = Mock()
        serving.gpu_table.return_value = [['2', GPU_UUID]]
        serving.gpu_applications.return_value = [['123', 'GPU-other', '50000']]
        qualify_available(serving)
        serving.gpu_applications.return_value = [['456', GPU_UUID, '1']]
        with self.assertRaisesRegex(RuntimeError, 'none were stopped'):
            qualify_available(serving)

    def test_retained_telemetry_filters_gpu2_after_binding(self):
        # Load the exact stdlib-only helper without importing a model runtime.
        import importlib.util
        from permission_admission.util import ROOT
        spec = importlib.util.spec_from_file_location('placement_serving_test',
            ROOT / 'retained/reference_discovery_parallel/base/serving.py')
        serving = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(serving)
        with patch.object(serving, 'gpu_table', return_value=[['2', GPU_UUID]]), \
             patch.object(serving, 'gpu_applications', return_value=[]):
            qualify_available(serving)
        stop = Mock()
        stop.is_set.side_effect = [False, True]
        rows = '2,' + GPU_UUID + ',selected\n3,GPU-other,excluded\n'
        with tempfile.TemporaryDirectory() as folder, patch.object(serving, 'command', return_value=rows):
            serving.telemetry(Path(folder), stop)
            self.assertEqual((Path(folder) / 'gpu_telemetry.csv').read_text(),
                             '2,' + GPU_UUID + ',selected\n')
