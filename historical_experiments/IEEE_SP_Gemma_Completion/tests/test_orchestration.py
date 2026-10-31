import copy
import fcntl
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from permission_admission.design import manifest
from permission_admission.util import ROOT, read, write


class Orchestration(unittest.TestCase):
    def test_lock_conflict_is_detectable_without_gpu(self):
        with tempfile.TemporaryDirectory() as temp:
            from permission_admission.device import LOCK_NAME
            path = Path(temp) / LOCK_NAME
            with path.open('a') as a, path.open('a') as b:
                fcntl.flock(a, fcntl.LOCK_EX | fcntl.LOCK_NB)
                with self.assertRaises(BlockingIOError):
                    fcntl.flock(b, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def test_recycled_pid_cannot_be_signalled(self):
        from reference_discovery_parallel.base import serving
        with tempfile.TemporaryDirectory() as temp:
            server = Mock(pid=777777)
            server.poll.return_value = 0
            with patch.object(serving, 'proc_start', return_value='NEW'), patch.object(serving.os, 'kill') as kill, \
                    patch.object(serving.os, 'killpg') as killpg, patch.object(serving, 'descendant_pids') as descendants:
                serving.stop_owned(server, {777777: 'OLD'}, Path(temp) / 'shutdown.json')
            kill.assert_not_called()
            killpg.assert_not_called()
            descendants.assert_not_called()

    def test_two_profile_subprocess_scheduling_and_raw_records(self):
        # Deliberately small ENGINEERING fixture of the real scheduler. It is
        # never a replacement scientific manifest or a model experiment.
        m = manifest()
        small = copy.deepcopy(m)
        small['E1'] = m['E1'][:2]
        small['E2'] = m['E2'][:2]
        small['E3_blocks'] = m['E3_blocks'][:1]
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            frozen = temp / 'MOCK_ENGINEERING_SUBSET.json'
            write(frozen, small)
            for family in ('qwen', 'gemma'):
                folder = temp / family
                env = os.environ.copy()
                env.update(CUDA_VISIBLE_DEVICES='', REFERENCE_DISCOVERY_MODEL_FAMILY=family)
                env.pop('PYTHONPATH', None)
                with (temp / (family + '.log')).open('w') as stream:
                    process = subprocess.run([sys.executable, '-m', 'permission_admission.profile',
                        '--family', family, '--out', str(folder), '--manifest', str(frozen),
                        '--project-root', str(temp), '--serving-python', sys.executable,
                        '--cache', str(temp / 'NO_WEIGHTS_NEEDED'), '--mock'],
                        cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=180)
                self.assertEqual(process.returncode, 0, (temp / (family + '.log')).read_text())
                status = read(folder / 'status.json')
                self.assertEqual(status['status'], 'MOCK_COMPLETE_ZERO_INFERENCE')
                self.assertEqual(status['completed'], 10)
                self.assertEqual(len(read(folder / 'census.json')), 10)
                self.assertFalse((folder / 'serving').exists())
                for path in folder.glob('E*/*/result.json'):
                    row = read(path)
                    self.assertTrue(row['mock'])
                    self.assertTrue(row['qualified'], row.get('error'))
                    self.assertEqual(row['profile'], family)
            from permission_admission.report import analyze
            summary = analyze(temp, small)
            self.assertEqual(summary, {'planned': 20, 'recorded': 20, 'qualified': 20})

