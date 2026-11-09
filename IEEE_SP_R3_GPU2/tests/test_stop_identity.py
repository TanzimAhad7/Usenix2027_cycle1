"""Stopping a stale or unrelated PID must never signal that process."""
import json,os,runpy,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from r3.serving_base import proc_start
class Tests(unittest.TestCase):
    def test_stale_identity_and_foreign_command_are_not_signaled(self):
        for birth in ['not-the-current-start',proc_start(os.getpid())]:
            with self.subTest(birth_matches=birth==proc_start(os.getpid())),tempfile.TemporaryDirectory() as d:
                root=Path(d);(root/'logs').mkdir();(root/'logs/latest.json').write_text(json.dumps(dict(pid=os.getpid(),start=birth,run_id='not_this_command',results=str(root/'no_results'))))
                with patch.object(sys,'argv',['r3.progress','--root',str(root),'--stop']),patch('r3.serving_base.verify_pid_namespace',return_value={}),patch('os.kill') as kill:
                    with self.assertRaises(SystemExit):runpy.run_module('r3.progress',run_name='__main__')
                    kill.assert_not_called()
if __name__=='__main__':unittest.main()
