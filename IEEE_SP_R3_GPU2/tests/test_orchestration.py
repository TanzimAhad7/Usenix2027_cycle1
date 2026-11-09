"""CPU-only controller/archives tests with fake processes and no model endpoint."""
import argparse,hashlib,json,os,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
import r3.controller as controller
from r3.common import read,write
class Tests(unittest.TestCase):
    def simulate(self,fail_qualification=False):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);project=Path(temp.name);out=project/'results/user_runs/engineering'
        source=out/'source';source.mkdir(parents=True);(project/'logs').mkdir();lock=(project/'logs/.r3_gpu2.lock').open('w');self.addCleanup(lock.close)
        class FakeServer:
            def __init__(self,*args):self.out=args[2]
            def prepare(self):self.out.mkdir();return project/'fake_snapshot'
            def refresh(self):pass
            def start(self,*args):pass
            def close(self):pass
        class FakeProcess:
            def __init__(self,cmd,**kw):
                self.pid=os.getpid();self.returncode=1 if fail_qualification and 'unittest' in cmd else 0
                if 'r3.qualification' in cmd:
                    mode=cmd[cmd.index('r3.qualification')+1];dest=Path(cmd[cmd.index('--out')+1]);dest.mkdir(parents=True,exist_ok=True)
                    write(dest/('prepared_requests.json' if mode=='prepare' else 'qualification.json'),[] if mode=='prepare' else dict(status='PASS',engineering_only=True))
                elif 'r3.render' in cmd:
                    dest=Path(cmd[cmd.index('--out')+1]);write(dest/'qualification.json',dict(status='PASS',engineering_only=True))
                elif 'r3.episode' in cmd:
                    job=read(Path(cmd[cmd.index('--job')+1]));dest=Path(cmd[cmd.index('--out')+1]);dest.mkdir(parents=True);write(dest/'job.json',job)
                    write(dest/'result.json',dict(id=job['id'],kind=job['kind'],status='COMPLETE',qualified=True,attempted=True,new_unauthorized_effects=0,anytime_violation=False,new_model_queries=0,engineering_only=True))
                    if job['kind']=='FULL' and job['setting']=='A' and job['task']=='BANK' and job['carrier']=='PARAMETER':write(dest/'checkpoint.json',dict(engineering_only=True))
            def poll(self):return self.returncode
        a=argparse.Namespace(project_root=project,run_id='engineering',serving_python=project/'fake_python',cache=project/'fake_cache',lock_fd=lock.fileno(),workers=4,frozen=True)
        with patch.object(controller,'ROOT',source),patch.object(controller,'verify_package',lambda:None),patch.object(controller,'OwnedServer',FakeServer),patch.object(controller.subprocess,'Popen',FakeProcess):code=controller.main(a)
        return code,out
    def test_all_positions_branches_and_archives(self):
        code,out=self.simulate();self.assertEqual(code,0);summary=read(out/'SUMMARY.json')
        self.assertEqual(summary['rows'],64);self.assertEqual(summary['full_completed'],32);self.assertEqual(summary['conditional_attempted'],8)
        self.assertEqual(read(out/'status.json')['completed'],64)
        for suffix in ['.zip','.review.zip','.after_full.zip','.after_full.review.zip']:
            with zipfile.ZipFile(out.parent/(out.name+suffix)) as z:
                self.assertIsNone(z.testzip())
                for line in z.read(out.name+'/SHA256SUMS').decode().splitlines():
                    expected,rel=line.split('  ',1);self.assertEqual(hashlib.sha256(z.read(out.name+'/'+rel)).hexdigest(),expected)
    def test_qualification_failure_retains_unexecuted_positions(self):
        code,out=self.simulate(True);self.assertEqual(code,1)
        summary=read(out/'SUMMARY.json');self.assertEqual(summary['rows'],64);self.assertEqual(summary['full_completed'],0)
        self.assertTrue(all(g['attempted']==0 and g['unknown_effect_endpoint']==g['scheduled'] for g in summary['groups']))
        self.assertTrue((out/'fatal_error.json').is_file())
if __name__=='__main__':unittest.main()
