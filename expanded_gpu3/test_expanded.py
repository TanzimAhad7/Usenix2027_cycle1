"""Engineering tests with mock inference. Never research evidence."""
import argparse
import json
import os
from pathlib import Path
import re
import signal
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from unittest.mock import patch
import uuid

HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import guards
import protocol
import runner
import sequence
import transport
from world import World


class Mock(BaseHTTPRequestHandler):
    alias='mock';bad=False
    def log_message(self,*args):pass
    def do_GET(self):
        obj={'data':[{'id':self.alias}]} if self.path=='/v1/models' else {'version':'MOCK_ONLY'}
        self.send_response(200);self.end_headers();self.wfile.write(json.dumps(obj).encode())
    def do_POST(self):
        p=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        if self.path=='/tokenize':obj={'tokens':[1,2,3],'count':3}
        else:
            messages=p['messages'];text='\n'.join(m.get('content') or '' for m in messages)
            native=bool(p.get('tools'));actor=native or text.startswith('Tool interface for this development experiment:')
            ids=re.findall(r'"account_id"\s*:\s*"(acct_A_[a-z0-9]+)"',text)
            if not actor:
                content=json.dumps(dict(person='Alice',account_id=ids[-1],directory_note='')) if ids else '{"survive":true,"reason":"mock assurance"}'
                msg=dict(role='assistant',content=content);finish='stop'
            else:
                committed=any((m.get('content') or '').startswith('committed') or '\ncommitted' in (m.get('content') or '') for m in messages)
                if not ids:calls=[dict(name='get_iban',arguments={'name':'Alice'})]
                elif committed or 'ALREADY received' in text:calls=[]
                else:
                    args=dict(recipient=ids[-1],amount=10,key='retry-verified' if 'retry-verified' in text else '')
                    calls=[dict(name='pay',arguments=args)]
                    if 'retry-verified' in text or 'then pay Alice twice' in text:calls.append(dict(name='pay',arguments=dict(args)))
                if self.bad:msg=dict(role='assistant',content='not JSON');finish='stop'
                elif native:
                    msg=dict(role='assistant',content='' if calls else 'Finished.',tool_calls=[dict(id='mock-'+uuid.uuid4().hex,type='function',function=dict(name=c['name'],arguments=json.dumps(c['arguments']))) for c in calls])
                    finish='tool_calls' if calls else 'stop'
                else:msg=dict(role='assistant',content=json.dumps(dict(content='',tool_calls=calls)));finish='stop'
            obj=dict(model=p['model'],choices=[dict(message=msg,finish_reason=finish)],usage=dict(prompt_tokens=3,completion_tokens=5,total_tokens=8))
        self.send_response(200);self.end_headers();self.wfile.write(json.dumps(obj).encode())


class Tests(unittest.TestCase):
    def root(self):
        root=os.environ.get('IEEE_SP_TEST_ROOT')
        if not root:self.skipTest('Set IEEE_SP_TEST_ROOT to project root')
        return Path(root)
    def test_schedule(self):
        self.assertEqual(len(protocol.schedule('qwen')),124);self.assertEqual(len(protocol.schedule('gemma')),112)
        a=protocol.schedule('qwen');b=protocol.schedule('gemma');self.assertEqual(a[:112],b)
        self.assertEqual(len({x['episode'] for x in a}),124)
    def test_shutdown_uses_owned_group_and_rejects_reused_pid(self):
        fake=argparse.Namespace(pid=101,poll=lambda:0,wait=lambda timeout:0)
        with tempfile.TemporaryDirectory() as t,patch.object(sequence,'descendant_pids',return_value={101}),\
             patch.object(sequence,'proc_start',side_effect=lambda p:None if p==101 else 'NEW_UNRELATED_PROCESS'),\
             patch.object(sequence.os,'killpg') as groupkill,patch.object(sequence.os,'kill') as pidkill:
            sequence.stop_owned(fake,{101:'old_parent',202:'OLD_PROCESS_START'},Path(t)/'shutdown.json')
            self.assertTrue(all(call.args[0]==101 for call in groupkill.call_args_list))
            self.assertFalse(any(call.args[0]==202 for call in pidkill.call_args_list))
    def test_augmenting_matching(self):
        m=guards.maximum_matching([[0,1],[0],[1,2]],3)
        self.assertEqual(len(m),3);self.assertEqual(len(set(m.values())),3)
    def test_strict_judge(self):
        self.assertEqual(guards.strict_verdict('```json\n{"survive":false,"reason":"true is mentioned"}\n```')[0],False)
        self.assertTrue(guards.strict_verdict('{"survive":true}')[0])
        for text in ['{"survive":"false"}','{"survive":0}','false','{"survive":true,"survive":false}','{"survive":false,"extra":true}']:
            with self.assertRaises(ValueError):guards.strict_verdict(text)
    def test_canonical_identity_and_idempotency(self):
        s=protocol.scenario('safe_retry',1);w=World(s,grant_gate=True);w.lookup_calls=1;w.active_id='first'
        with self.assertRaises(ValueError):w.pay('Alice',10)
        w.pay(s['accounts']['Alice'],10,'retry-verified');w.active_id='second'
        w.pay(s['accounts']['Alice'],10,'retry-verified')
        self.assertEqual(len(w.effects),1);self.assertTrue(w.outcome(True)['secure_completion'])
        with self.assertRaises(ValueError):w.pay(s['accounts']['Alice'],5,'retry-verified')
        with self.assertRaises(PermissionError):w.pay(s['accounts']['Alice'],10,'')
    def test_real_native_assurance(self):
        from components import run
        with tempfile.TemporaryDirectory() as t:
            out=Path(t)/'assurance';run(self.root(),out)
            status=json.loads((out/'status.json').read_text());self.assertEqual(status['executions'],29);self.assertEqual(status['assertions'],36)
    def test_complete_runner_both_transports(self):
        server=ThreadingHTTPServer(('127.0.0.1',0),Mock);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            with tempfile.TemporaryDirectory() as t:
                for family in ['qwen','gemma']:
                    args=argparse.Namespace(root=self.root(),out=Path(t)/family,model=family,family=family,repeats=2,max_requests=100,base_url=f'http://127.0.0.1:{server.server_port}/v1')
                    rc=runner.main(args);rows=json.loads((args.out/'results.json').read_text())
                    self.assertEqual(rc,0,[r['error'] for r in rows if r['error']])
                    self.assertEqual(len(rows),124 if family=='qwen' else 112)
                    self.assertTrue(all(r['outcome']['secure_completion'] for r in rows),[(r['episode'],r['outcome']) for r in rows if not r['outcome']['secure_completion']])
                    self.assertEqual(sum(r['transport']=='native' for r in rows),12 if family=='qwen' else 0)
        finally:server.shutdown();server.server_close()
    def test_malformed_episode_retains_unknown_and_raw(self):
        server=ThreadingHTTPServer(('127.0.0.1',0),Mock);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();Mock.bad=True
        try:
            with tempfile.TemporaryDirectory() as t:
                root=self.root();sys.path.insert(0,str(root/'experiments/review_binding'));import diagnostic as d
                out=Path(t);(out/'generated').mkdir();item=protocol.schedule('qwen')[0]
                args=argparse.Namespace(root=root,out=out,model='qwen',family='qwen',max_requests=100,base_url=f'http://127.0.0.1:{server.server_port}/v1')
                row=runner.run_episode(args,item,d)
                self.assertEqual(row['outcome']['violation'],'UNKNOWN');self.assertIsNotNone(row['error'])
                self.assertTrue((out/item['episode']/'http_001_actor.response.json').is_file())
        finally:Mock.bad=False;server.shutdown();server.server_close()
    def test_complete_sequence_switch_and_archive(self):
        source=self.root();real_popen=subprocess.Popen;real_command=sequence.command;servers=[];order=[]
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'project';root.mkdir();cache=Path(t)/'cache'
            shutil.copytree(source/'experiments/review_binding',root/'experiments/review_binding')
            (root/'scripts').mkdir();shutil.copy2(source/'scripts/qualify_gpu.py',root/'scripts/qualify_gpu.py')
            shutil.copytree(HERE,root/'expanded_gpu3',ignore=shutil.ignore_patterns('__pycache__'))
            for venv in ['.venv','.venv-serving']:
                (root/venv/'bin').mkdir(parents=True);(root/venv/'bin/python').symlink_to(sys.executable)
            ninja=root/'.venv-serving/bin/ninja';ninja.write_text('#!/bin/sh\necho MOCK_NINJA\n');ninja.chmod(0o755)
            for _,model,_ in sequence.MODELS:
                directory=cache/('models--'+model.replace('/','--'));snap=directory/'snapshots/revision';snap.mkdir(parents=True)
                # Deliberately no refs/main: regression for the observed failure.
                for name in ['config.json','tokenizer.json','tokenizer_config.json']:(snap/name).write_text('{}')
                (snap/'chat_template.json').write_text('{"chat_template":"MOCK_TEMPLATE"}');(snap/'model.safetensors').write_bytes(b'MOCK_WEIGHTS')
            def launch(argv,*a,**kw):
                if 'vllm.entrypoints.openai.api_server' in argv:
                    self.assertTrue(all(p.poll() is not None for p in servers));alias=argv[argv.index('--served-model-name')+1]
                    self.assertEqual(kw['env']['CUDA_VISIBLE_DEVICES'],'GPU-three-test')
                    self.assertEqual(kw['env']['PATH'].split(os.pathsep)[0],str(root/'.venv-serving/bin'))
                    self.assertEqual('--tool-call-parser' in argv,alias=='qwen3-32b')
                    process=real_popen([sys.executable,str(HERE/'test_expanded.py'),'--mock-server',alias],*a,**kw)
                    servers.append(process);order.append(alias);return process
                return real_popen(argv,*a,**kw)
            def command(argv,timeout=30):
                if 'freeze' in argv:return 'MOCK_PACKAGES\n'
                if '-c' in argv:return '{}\n'
                return real_command(argv,timeout)
            def stop(server,owned,record):server.terminate();server.wait(timeout=10);sequence.write(record,{'MOCK_ONLY':True,'returncode':server.returncode})
            sys.path.insert(0,str(root/'scripts'));import qualify_gpu
            oldterm=signal.getsignal(signal.SIGTERM);oldint=signal.getsignal(signal.SIGINT);oldpath=os.environ.get('PATH','')
            try:
                with patch.object(sequence.subprocess,'Popen',side_effect=launch),patch.object(sequence,'command',side_effect=command),\
                     patch.object(sequence,'gpu_table',return_value=[['3','GPU-three-test','0','95830']]),\
                     patch.object(sequence,'gpu_applications',return_value=[]),patch.object(sequence,'telemetry',return_value=None),\
                     patch.object(sequence,'descendant_pids',side_effect=lambda p:{p}),patch.object(sequence,'stop_owned',side_effect=stop),\
                     patch.object(qualify_gpu,'qualify',side_effect=lambda g,p:dict(socket_owner_pids=[servers[-1].pid],physical_gpu=g)):
                    rc=sequence.main(argparse.Namespace(root=root,run_id='MOCK_EXPANDED_ONLY',cache=str(cache)))
                self.assertEqual(rc,0);self.assertEqual(order,['qwen3-32b','gemma3-27b-it'])
                out=root/'results/user_runs/MOCK_EXPANDED_ONLY';self.assertTrue(out.with_suffix('.tar.gz').is_file())
                self.assertEqual(json.loads((out/'assurance/status.json').read_text())['status'],'ASSURANCE_PASS')
                self.assertEqual(sum(len(json.loads((out/f/'diagnostic/results.json').read_text())) for f in ['qwen','gemma']),236)
            finally:
                signal.signal(signal.SIGTERM,oldterm);signal.signal(signal.SIGINT,oldint);os.environ['PATH']=oldpath
                if 'diagnostic' in sys.modules:sys.modules['diagnostic'].ROOT=source/'experiments/review_binding'
                for p in servers:
                    if p.poll() is None:p.terminate();p.wait()


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--mock-server':
        Mock.alias=sys.argv[2];ThreadingHTTPServer(('127.0.0.1',18080),Mock).serve_forever()
    else:unittest.main()
