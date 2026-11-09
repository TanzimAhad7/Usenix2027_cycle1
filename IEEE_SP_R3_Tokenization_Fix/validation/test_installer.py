import fcntl,hashlib,importlib.util,json,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
BASE=Path(__file__).resolve().parent;FIX=BASE/'IEEE_SP_R3_Tokenization_Fix';ORIGINAL=BASE/'input/IEEE_SP_R3_GPU2.zip'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
class Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);root=Path(self.temp.name)
        with zipfile.ZipFile(ORIGINAL) as z:z.extractall(root)
        self.project=root/'IEEE_SP_R3_GPU2';self.original_manifest=(self.project/'PACKAGE_MANIFEST.json').read_bytes();self.original_render=(self.project/'r3/render.py').read_bytes()
    def apply(self):return subprocess.run([sys.executable,str(FIX/'APPLY_FIX.py'),'--project-root',str(self.project)],capture_output=True,text=True,timeout=60)
    def test_apply_preserve_and_idempotence(self):
        frozen=self.project/'results/user_runs/retained/source/r3/render.py';frozen.parent.mkdir(parents=True);frozen.write_bytes(b'old evidence')
        env=self.project/'.venv/PRESERVE';env.parent.mkdir();env.write_bytes(b'existing environment')
        first=self.apply();self.assertEqual(first.returncode,0,first.stdout+first.stderr)
        self.assertEqual(frozen.read_bytes(),b'old evidence');self.assertEqual(env.read_bytes(),b'existing environment')
        m=json.loads((self.project/'PACKAGE_MANIFEST.json').read_text())
        for n,h in m['files'].items():self.assertEqual(sha(self.project/n),h)
        old=json.loads(self.original_manifest)
        for n,h in old['files'].items():
            if n!='r3/render.py':self.assertEqual(m['files'][n],h)
        self.assertEqual(len(list((self.project/'patch_backups').iterdir())),1)
        second=self.apply();self.assertEqual(second.returncode,0,second.stderr);self.assertIn('ALREADY APPLIED',second.stdout)
        self.assertEqual(len(list((self.project/'patch_backups').iterdir())),1)
    def test_active_controller_refuses_patch(self):
        logs=self.project/'logs';logs.mkdir()
        with (logs/'.r3_gpu2.lock').open('w') as lock:
            fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB);result=self.apply()
        self.assertNotEqual(result.returncode,0);self.assertIn('active',result.stderr);self.assertEqual((self.project/'r3/render.py').read_bytes(),self.original_render)
    def test_modified_package_refuses_patch(self):
        p=self.project/'r3/guard.py';p.write_text(p.read_text()+'\n# unrelated change\n')
        result=self.apply();self.assertNotEqual(result.returncode,0);self.assertIn('verification failed',result.stderr)
        self.assertEqual((self.project/'r3/render.py').read_bytes(),self.original_render)
    def test_failed_regression_restores_old_files(self):
        spec=importlib.util.spec_from_file_location('apply_r3_fix',FIX/'APPLY_FIX.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with patch.object(module.subprocess,'run',return_value=subprocess.CompletedProcess([],1)):
            with self.assertRaises(RuntimeError):module.main(self.project)
        self.assertEqual((self.project/'PACKAGE_MANIFEST.json').read_bytes(),self.original_manifest)
        self.assertEqual((self.project/'r3/render.py').read_bytes(),self.original_render)
        self.assertFalse((self.project/'tests/test_render.py').exists())
        self.assertFalse((self.project/'R3_TOKENIZATION_FIX.json').exists())
if __name__=='__main__':unittest.main()
