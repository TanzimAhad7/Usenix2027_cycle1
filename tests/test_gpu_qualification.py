import importlib.util
from pathlib import Path
import unittest
s=importlib.util.spec_from_file_location('gpu',Path(__file__).resolve().parents[1]/'scripts/qualify_gpu.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class GPUQualificationTests(unittest.TestCase):
    def run_check(self,apps='102, GPU-two\n',sockets='LISTEN 0 128 127.0.0.1:18080 0.0.0.0:* users:(("python",pid=100,fd=5))',gpu=2):
        return m.evaluate(gpu,18080,'0, GPU-zero\n2, GPU-two\n3, GPU-three\n',apps,'100 1\n101 100\n102 101\n999 1\n',sockets)
    def test_descendant_worker_qualifies(self):
        self.assertEqual(self.run_check()['physical_gpu'],2)
    def test_foreign_gpu_rejected(self):
        with self.assertRaises(ValueError):self.run_check(apps='102, GPU-three\n')
    def test_unrelated_worker_cannot_qualify(self):
        with self.assertRaises(ValueError):self.run_check(apps='999, GPU-two\n')
    def test_hidden_socket_owner_rejected(self):
        with self.assertRaises(ValueError):self.run_check(sockets='LISTEN 0 128 127.0.0.1:18080 0.0.0.0:*')
    def test_unauthorized_gpu_rejected(self):
        with self.assertRaises(ValueError):self.run_check(gpu=0)
