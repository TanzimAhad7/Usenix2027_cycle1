"""CPU tests only. Mock inference is never scientific evidence."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import diagnostic_runner as dr
import sequence as seq


class Server(BaseHTTPRequestHandler):
    bad=False
    alias='mock-model'
    def log_message(self,*args):pass
    def do_GET(self):
        data={'data':[{'id':self.alias}]} if self.path=='/v1/models' else {'version':'MOCK_TEST_ONLY'}
        self.send_response(200);self.end_headers();self.wfile.write(json.dumps(data).encode())
    def do_POST(self):
        p=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        if self.path=='/tokenize':data={'tokens':[1,2,3],'count':3}
        else:
            text='\n'.join(x['content'] for x in p['messages'])
            if self.bad:content='broken JSON'
            elif not text.startswith(dr.ACTION_INSTRUCTION):content='Alice: account-alice.'
            else:
                if '\ncommitted' in text: calls=[]
                elif 'TOOL RESULT' in text: calls=[dict(name='pay',arguments=dict(recipient='Alice',amount=10,key=''))]
                else:calls=[dict(name='get_iban',arguments=dict(name='Alice'))]
                content=json.dumps(dict(content='',tool_calls=calls))
            data=dict(model=p['model'],choices=[dict(message=dict(content=content),finish_reason='stop')],usage=dict(prompt_tokens=10,completion_tokens=5))
        raw=json.dumps(data).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(raw)


class AutomationTests(unittest.TestCase):
    def test_complete_controller_switches_models_and_archives(self):
        source=os.environ.get('IEEE_SP_TEST_ROOT')
        if not source:self.skipTest('Set IEEE_SP_TEST_ROOT to installed project root')
        real_popen=subprocess.Popen;real_command=seq.command;servers=[];order=[]
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'project';root.mkdir();cache=Path(t)/'cache'
            shutil.copytree(Path(source)/'experiments/review_binding',root/'experiments/review_binding')
            (root/'scripts').mkdir();shutil.copy2(Path(source)/'scripts/qualify_gpu.py',root/'scripts/qualify_gpu.py')
            shutil.copytree(HERE,root/'automation_gpu3',ignore=shutil.ignore_patterns('__pycache__'))
            for name in ['.venv','.venv-serving']:
                (root/name/'bin').mkdir(parents=True);(root/name/'bin/python').symlink_to(sys.executable)
            for _,model,_ in seq.MODELS:
                d=cache/('models--'+model.replace('/','--'));s=d/'snapshots/abc';s.mkdir(parents=True)
                (d/'refs').mkdir();(d/'refs/main').write_text('abc')
                for name in ['config.json','tokenizer.json']:(s/name).write_text('{}')
                (s/'tokenizer_config.json').write_text('{}')
                (s/'chat_template.json').write_text(json.dumps({'chat_template':'mock template'}))
                (s/'model.safetensors').write_bytes(b'mock weights')
            def launch(argv,*a,**kw):
                if 'vllm.entrypoints.openai.api_server' in argv:
                    alias=argv[argv.index('--served-model-name')+1]
                    self.assertTrue(all(p.poll() is not None for p in servers))
                    self.assertEqual(kw['env']['CUDA_VISIBLE_DEVICES'],'GPU-test-three')
                    p=real_popen([sys.executable,str(HERE/'test_automation.py'),'--mock-server',alias],*a,**kw)
                    servers.append(p);order.append(alias);return p
                return real_popen(argv,*a,**kw)
            def cmd(argv,timeout=30):
                if '-m' in argv and 'freeze' in argv:return 'MOCK_PACKAGES_ONLY\n'
                if '-c' in argv:return '{}\n'
                return real_command(argv,timeout)
            sys.path.insert(0,str(root/'scripts'))
            import qualify_gpu
            oldterm=signal.getsignal(signal.SIGTERM);oldint=signal.getsignal(signal.SIGINT)
            def stop_mock_server(server,owned,record):
                # Host runner exposes synthetic PIDs; /proc is not that PID
                # namespace. OS ownership shutdown has its separate unit test.
                server.terminate();server.wait(timeout=10)
                seq.write(record,dict(mock_test_only=True,returncode=server.returncode))
            try:
                with patch.object(seq.subprocess,'Popen',side_effect=launch),patch.object(seq,'command',side_effect=cmd),\
                     patch.object(seq,'gpu_table',return_value=[['3','GPU-test-three','0','95830']]),\
                     patch.object(seq,'gpu_applications',return_value=[]),patch.object(seq,'telemetry',return_value=None),\
                     patch.object(seq,'descendant_pids',side_effect=lambda pid:{pid}),\
                     patch.object(seq,'stop_owned',side_effect=stop_mock_server),\
                     patch.object(qualify_gpu,'qualify',side_effect=lambda g,p:dict(socket_owner_pids=[servers[-1].pid],physical_gpu=g)):
                    rc=seq.main(argparse.Namespace(root=root,run_id='MOCK_TEST_ONLY',cache=str(cache)))
                self.assertEqual(rc,0);self.assertEqual(order,['qwen3-32b','gemma3-27b-it'])
                out=root/'results/user_runs/MOCK_TEST_ONLY'
                self.assertEqual(json.loads((out/'status.json').read_text())['status'],'COMPLETE')
                self.assertTrue(out.with_suffix('.tar.gz').is_file())
                for family,_,_ in seq.MODELS:
                    self.assertEqual(len(json.loads((out/family/'diagnostic/results.json').read_text())),30)
                    self.assertTrue((out/family/'shutdown.json').is_file())
            finally:
                signal.signal(signal.SIGTERM,oldterm);signal.signal(signal.SIGINT,oldint)
                if 'diagnostic' in sys.modules:sys.modules['diagnostic'].ROOT=Path(source)/'experiments/review_binding'
                for p in servers:
                    if p.poll() is None:os.killpg(p.pid,signal.SIGKILL);p.wait()
    def test_incomplete_cache_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(RuntimeError):seq.cache_snapshot(Path(t),'Qwen/Qwen3-32B')

    def test_cached_revision_pinned_and_missing_shard_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            cache=Path(t);d=cache/'models--Qwen--Qwen3-32B';s=d/'snapshots/abc'
            s.mkdir(parents=True);(d/'refs').mkdir();(d/'refs/main').write_text('abc')
            for name in ['config.json','tokenizer.json']:(s/name).write_text('{}')
            (s/'tokenizer_config.json').write_text(json.dumps({'chat_template':'template'}))
            (s/'model.safetensors.index.json').write_text(json.dumps({'weight_map':{'x':'missing.safetensors'}}))
            with self.assertRaises(RuntimeError):seq.cache_snapshot(cache,'Qwen/Qwen3-32B')
            (s/'missing.safetensors').write_bytes(b'weights')
            snap,record=seq.cache_snapshot(cache,'Qwen/Qwen3-32B')
            self.assertEqual(snap,s);self.assertEqual(record['revision'],'abc')
            (d/'refs/main').unlink()
            snap,record=seq.cache_snapshot(cache,'Qwen/Qwen3-32B')
            self.assertEqual(snap,s)
            self.assertIn('refs/main absent',record['revision_resolution'])
            # An incomplete second snapshot does not create false ambiguity.
            (d/'snapshots/incomplete').mkdir()
            snap,record=seq.cache_snapshot(cache,'Qwen/Qwen3-32B')
            self.assertEqual(snap,s);self.assertIn('incomplete',record['rejected_snapshots'])
            # Multiple complete revisions are listed, never selected by age.
            shutil.copytree(s,d/'snapshots/second')
            with self.assertRaisesRegex(RuntimeError,'2 complete snapshots'):
                seq.cache_snapshot(cache,'Qwen/Qwen3-32B')

    def test_shutdown_does_not_stop_unrelated_process(self):
        ours=subprocess.Popen([sys.executable,'-c','import time;time.sleep(120)'],start_new_session=True)
        unrelated=subprocess.Popen([sys.executable,'-c','import time;time.sleep(120)'],start_new_session=True)
        try:
            with tempfile.TemporaryDirectory() as t:
                seq.stop_owned(ours,{ours.pid:seq.proc_start(ours.pid)},Path(t)/'shutdown.json')
                self.assertIsNotNone(ours.poll());self.assertIsNone(unrelated.poll())
        finally:
            unrelated.terminate();unrelated.wait()
            if ours.poll() is None:ours.kill();ours.wait()

    def test_strict_parser_rejects_empty_and_invented_tool(self):
        runtime=argparse.Namespace(functions={})
        for raw in ['{}','[]','{"tool_calls":[{"name":"invented","arguments":{}}]}','```json\n{}\n```']:
            with self.assertRaises((ValueError,TypeError)):dr.parse_actions(raw,runtime)

    def test_native_mock_schedule_and_failed_outputs_preserved(self):
        root=os.environ.get('IEEE_SP_TEST_ROOT')
        if not root:self.skipTest('Set IEEE_SP_TEST_ROOT to installed project root')
        server=ThreadingHTTPServer(('127.0.0.1',0),Server)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            with tempfile.TemporaryDirectory() as t:
                for family,bad in [('qwen',False),('gemma',True)]:
                    Server.bad=bad;out=Path(t)/family
                    args=argparse.Namespace(root=Path(root),out=out,model=family,family=family,
                       repeats=1,max_requests=80,base_url=f'http://127.0.0.1:{server.server_port}/v1')
                    rc=dr.main(args);rows=json.loads((out/'results.json').read_text())
                    self.assertEqual(len(rows),15)
                    self.assertEqual(rc,3 if bad else 0)
                    if bad:
                        self.assertTrue(all(r['outcome']['violation']=='UNKNOWN' for r in rows))
                        self.assertTrue(all(r['error'] for r in rows))
                        self.assertEqual(len(list(out.glob('*/http_001_actor.response.json'))),15)
                    else:
                        self.assertTrue(all(r['outcome']['secure_completion'] for r in rows))
                        self.assertTrue(any(r['payload_delivered'] for r in rows))
                        self.assertTrue(any('"role": "shadow"' in p.read_text() for p in out.glob('*/events.jsonl')))
                    self.assertTrue(all((out/r['episode']/'events.jsonl').is_file() for r in rows))
        finally:Server.bad=False;server.shutdown();server.server_close()


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--mock-server':
        Server.alias=sys.argv[2];ThreadingHTTPServer(('127.0.0.1',18080),Server).serve_forever()
    else:unittest.main()
