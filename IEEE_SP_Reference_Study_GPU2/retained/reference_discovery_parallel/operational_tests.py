"""Host-independent controls for orchestration, diagnostics and lossless outputs.

No AgentDojo runtime, model weights, network, GPU access or model inference.
"""
import ast,fcntl,json,os,subprocess,sys,tarfile,tempfile,threading,unittest
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from .campaign import plan,child_command
from .protocol import manifest
from .models import PROFILES,command
from .common import digest,file_hash,write,read
from .strict_tags import parse
from .token_diagnostics import Diagnostics
from .packaging import package,review_selected

def fixture_job(job):
    """Real spawned-process scheduler fixture; no runtime/model simulation."""
    import time
    root=Path(job['root']);ident=job['item']['id']
    if ident in ('A','B'):
        (root/(ident+'.started')).write_text(str(os.getpid()))
        deadline=time.monotonic()+5
        while not all((root/(i+'.started')).exists() for i in ('A','B')):
            if time.monotonic()>deadline:raise RuntimeError('Two-process fixture never overlapped')
            time.sleep(0.005)
    stages=[]
    for stage in ['actor','tool','reference','report']:
        stages.append(stage);time.sleep(job['delay']/4)
    return dict(id=ident,status='COMPLETE',outcome='ENGINEERING_FIXTURE_ONLY',pid=os.getpid(),stages=stages)

class Operations(unittest.TestCase):
    def test_tokenization_artifact_preserves_mapping_list_and_single_batch(self):
        from collections import UserDict
        from .models import tokenization_artifact
        class BatchEncoding(UserDict):pass
        cases=[([4,7,9],[4,7,9]),(BatchEncoding(input_ids=[4,7,9],attention_mask=[1,1,1]),[4,7,9]),
               (BatchEncoding(input_ids=[[4,7,9]],attention_mask=[[1,1,1]]),[4,7,9])]
        for raw,expected in cases:
            artifact=tokenization_artifact(raw)
            self.assertEqual(artifact['token_ids'],expected)
            saved=json.loads(json.dumps(artifact));self.assertEqual(saved,artifact)
            if isinstance(raw,BatchEncoding):self.assertEqual(artifact['tokenization'],dict(raw))
    def test_tokenization_artifact_rejects_missing_multiple_or_invalid_ids(self):
        from .models import tokenization_artifact
        for value in [{'attention_mask':[1]},[[1],[2]],[],['1'],[True],[-1],object()]:
            with self.subTest(value=str(value)),self.assertRaises((TypeError,ValueError)):tokenization_artifact(value)
    def test_preflight_uses_installed_vllm_preprocessing_without_mutating_wire_fixture(self):
        import copy,types
        from unittest.mock import patch
        from .models import prepare_fixture_messages
        original=[dict(role='user',content=[dict(type='text',text='FIRST'),dict(type='text',text='SECOND')])]
        saved=copy.deepcopy(original);seen=[]
        def resolve(**kwargs):
            seen.append(kwargs);return 'string'
        def parse(messages,config,content_format):
            self.assertFalse(config.enable_prompt_embeds);self.assertEqual(content_format,'string')
            messages[0]['content']='\n'.join(b['text'] for b in messages[0]['content'])
            return messages,None,None
        modules={'vllm.entrypoints.chat_utils':types.SimpleNamespace(parse_chat_messages=parse),
                 'vllm.renderers.hf':types.SimpleNamespace(resolve_chat_template_content_format=resolve)}
        with patch.dict(sys.modules,modules):
            prepared,format_=prepare_fixture_messages(object(),'TEMPLATE',original,[])
        self.assertEqual(original,saved);self.assertEqual(prepared[0]['content'],'FIRST\nSECOND')
        self.assertEqual(format_,'string');self.assertEqual(seen[0]['given_format'],'auto');self.assertEqual(seen[0]['chat_template'],'TEMPLATE')
    def test_same_exact_conditions_on_both_models(self):
        p=plan();m=manifest()
        self.assertEqual(len(p['slots']),688);self.assertEqual(len({s['id'] for s in p['slots']}),688)
        self.assertEqual(len(p['conditional_slots']),60)
        self.assertEqual(Counter(w['allocation_phase'] for w in m['workflows']),dict(CORE=176,RECOVERY=72,BOUNDARY=96))
        for family in PROFILES:
            self.assertEqual([s['workflow_id'] for s in p['slots'] if s['model_family']==family],[w['id'] for w in m['workflows']])
        root=Path(__file__).parent.parent
        old=read(root/'reference_discovery_provenance/ORIGINAL_344_ALLOCATION.json')
        self.assertEqual(m['workflows'],old['workflows']);self.assertEqual(m['forks'],old['forks'])
    def test_no_live_conditional_s1_reproduction(self):
        self.assertEqual(manifest()['blocks'],[])
        self.assertEqual(manifest()['counts']['conditional_admissions'],0)
    def test_model_commands_keep_resources_and_generation_settings(self):
        for family in PROFILES:
            c=command('/project/.venv-serving/bin/python',Path('/cached/snapshot'),family)
            for flag,value in [('--port','18080'),('--tensor-parallel-size','1'),('--dtype','bfloat16'),('--max-model-len','32768'),('--max-num-seqs','4'),('--gpu-memory-utilization','0.90'),('--seed','20261025')]:self.assertEqual(c[c.index(flag)+1],value)
            self.assertEqual(json.loads(c[c.index('--override-generation-config')+1]),{'max_new_tokens':8192})
        q=command('python',Path('/cached'),'qwen');g=command('python',Path('/cached'),'gemma')
        self.assertNotIn('--chat-template',q);self.assertIn('--tool-parser-plugin',g)
    def test_workers_are_isolated_and_no_intermediate_archives(self):
        a=SimpleNamespace(root=Path('/project'),run_id='test',cache='/cache',mock=False)
        c=child_command(a,'gemma',Path('/output'),12)
        self.assertIn('--defer-finalization',c);self.assertIn('--shared-qualification',c);self.assertIn('--lock-fd',c)
        self.assertNotIn('--max-collection-hours',c)
        c=child_command(a,'gemma',Path('/output'),12,7200)
        self.assertEqual(float(c[c.index('--max-collection-hours')+1]),2.0)
    def test_model_selection_does_not_leak_between_processes(self):
        for family in PROFILES:
            env=os.environ.copy();env['REFERENCE_DISCOVERY_MODEL_FAMILY']=family
            p=subprocess.run([sys.executable,'-c','from reference_discovery_parallel.common import MODEL,MODEL_FAMILY;print(MODEL_FAMILY+" "+MODEL)'],env=env,capture_output=True,text=True,check=True)
            self.assertEqual(p.stdout.strip(),family+' '+PROFILES[family]['alias'])
    def test_inherited_lock_stays_held_between_workers(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'lock'
            with path.open('a') as lock:
                fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                code='import os,sys;f=os.fdopen(os.dup(int(sys.argv[1])),"a");f.close()'
                subprocess.run([sys.executable,'-c',code,str(lock.fileno())],pass_fds=(lock.fileno(),),check=True)
                with path.open('a') as other:
                    with self.assertRaises(BlockingIOError):fcntl.flock(other,fcntl.LOCK_EX|fcntl.LOCK_NB)
    def test_background_diagnostics_do_not_block_submit_and_copy_payload(self):
        began=threading.Event();release=threading.Event();seen=[]
        def work(i,p):
            began.set()
            if not release.wait(2):raise RuntimeError('Fixture timeout')
            seen.append((i,p))
        d=Diagnostics(work);payload={'messages':[{'content':'original'}]}
        try:
            d.submit(1,payload);self.assertTrue(began.wait(1))
            payload['messages'][0]['content']='modified';d.submit(2,{'value':2});release.set();d.close()
            self.assertEqual(seen,[(1,{'messages':[{'content':'original'}]}),(2,{'value':2})])
            with self.assertRaises(RuntimeError):d.submit(3,{})
        finally:release.set();d.close()
    def test_background_diagnostic_failures_are_not_silently_lost(self):
        def fail(*_):raise ValueError('fixture-write-failure')
        d=Diagnostics(fail);d.submit(1,{})
        with self.assertRaises(ValueError):d.close()
    def test_tag_parser_preserves_duplicate_occurrences(self):
        raw='<tool_call>{"name":"send_email","arguments":{"body":"same"}}</tool_call>'
        calls,content=parse(raw+raw);self.assertEqual(len(calls),2);self.assertEqual(calls[0],calls[1]);self.assertIsNone(content)
    def test_tag_parser_rejects_partial_malformed_and_duplicate_fields(self):
        for raw in ['<tool_call>{"name":"x","arguments":{}}','</tool_call>',
                    '<tool_call>{"name":"x","arguments":{},"arguments":{}}</tool_call>',
                    '<tool_call>{"name":"x","arguments":"{}"}</tool_call>',
                    '<tool_call>{"name":"x","arguments":{},"permission":true}</tool_call>']:
            with self.subTest(raw=raw),self.assertRaises(ValueError):parse(raw)
    def test_plain_response_is_not_invented_into_tool_call(self):
        self.assertEqual(parse('The task is complete.'),([], 'The task is complete.'))
    def test_tag_parser_preserves_content_and_valid_arguments(self):
        calls,content=parse('Before<tool_call>{"name":"send_money","arguments":{"amount":4.0,"recipient":"Alice"}}</tool_call>After')
        self.assertEqual(content,'BeforeAfter');self.assertEqual(calls[0]['arguments']['amount'],4.0)
    def test_no_async_inference_or_payload_rewrite_added(self):
        source=(Path(__file__).parent/'driver.py').read_text();tree=ast.parse(source)
        create=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='create')
        calls=[n for n in ast.walk(create) if isinstance(n,ast.Call)]
        self.assertTrue(any(isinstance(n.func,ast.Name) and n.func.id=='create' for n in calls))
        self.assertNotIn('submit',ast.unparse(create));self.assertIn('self.diagnostics.close()',source)
    def test_review_selector_preserves_all_profile_results_but_not_raw_histories(self):
        for family in PROFILES:
            self.assertTrue(review_selected(Path('models')/family/'workflows/X/result.json'))
            self.assertTrue(review_selected(Path('models')/family/'forks/X/events.jsonl'))
            self.assertFalse(review_selected(Path('models')/family/'forks/X/requests/0000.response.json'))
    def test_complete_archive_hashes_and_review_scope(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'run';out.mkdir()
            for family in PROFILES:
                write(out/'models'/family/'workflows/X/result.json',dict(outcome='FIXTURE_ONLY'))
                write(out/'models'/family/'forks/F/requests/raw.json',dict(raw=family))
            write(out/'status.json',dict(mode='ENGINEERING_ZERO_INFERENCE'))
            result=package(out)
            with tarfile.open(result['archive']) as t:
                names=t.getnames();self.assertTrue(any('/gemma/forks/F/requests/raw.json' in n for n in names))
                for line in t.extractfile('run/SHA256SUMS').read().decode().splitlines():
                    expected,relative=line.split('  ',1)
                    import hashlib
                    self.assertEqual(hashlib.sha256(t.extractfile('run/'+relative).read()).hexdigest(),expected)
            with tarfile.open(result['review_bundle']) as t:
                self.assertIn('run/REVIEW_SCOPE.json',t.getnames());self.assertFalse(any(n.endswith('raw.json') for n in t.getnames()))
            self.assertIsNone(result['raw_parts']);self.assertTrue(result['raw_evidence_losslessly_preserved'])

    def test_spawned_rolling_dispatch_is_bounded_and_does_not_wait_for_slow_first(self):
        import multiprocessing
        from concurrent.futures import ProcessPoolExecutor
        from .rolling import collect
        from .episode_worker import initialize
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);jobs=[dict(kind='workflow',item=dict(id=i),root=d,delay=t) for i,t in [('A',0.3),('B',0.02),('C',0.02)]]
            completed=[];active=set();peak=[]
            def progress(kind,ident,state):
                if state=='RUNNING':active.add(ident)
                else:active.remove(ident)
                peak.append(len(active))
            with ProcessPoolExecutor(max_workers=2,mp_context=multiprocessing.get_context('spawn'),initializer=initialize,initargs=(str(root/'workers'),)) as pool:
                rows=collect(pool,jobs,fixture_job,lambda j,r:completed.append(r['id']),progress,root)
            self.assertEqual([r['id'] for r in rows],['A','B','C']);self.assertEqual(completed,['B','C','A']);self.assertEqual(max(peak),2)
            self.assertEqual(len({r['pid'] for r in rows}),2)
            for r in rows:self.assertEqual(r['stages'],['actor','tool','reference','report'])
            events=[json.loads(s) for s in (root/'scheduler.jsonl').read_text().splitlines()]
            self.assertLess(next(i for i,e in enumerate(events) if e['id']=='C' and e['event']=='SUBMIT'),next(i for i,e in enumerate(events) if e['id']=='A' and e['event']=='COMPLETE'))

    def test_outage_drain_prevents_restart_under_another_workflow(self):
        from concurrent.futures import ThreadPoolExecutor
        from .rolling import collect
        with tempfile.TemporaryDirectory() as d:
            jobs=[dict(kind='workflow',item=dict(id=str(i)),delay=t) for i,t in enumerate([0.01,0.1,0.01])]
            active=set();outage=[False];restarted=[]
            def work(j):
                import time
                time.sleep(j['delay']);return dict(id=j['item']['id'],status='COMPLETE')
            def consume(j,r):
                if r['id']=='0':outage[0]=True
            def progress(kind,ident,state):
                if state=='RUNNING':
                    if outage[0]:self.assertFalse(active);outage[0]=False;restarted.append(ident)
                    active.add(ident)
                else:active.remove(ident)
            with ThreadPoolExecutor(max_workers=2) as pool:collect(pool,jobs,work,consume,progress,Path(d),drain_needed=lambda:outage[0])
            self.assertEqual(restarted,['2'])

    def test_independent_native_json_audit_detects_excess_and_observer_disagreement(self):
        from .audit_core import audit,CPU
        spec=dict(suite='slack',obligations=[dict(function='send_direct_message',args=dict(recipient='Alice',body='X'))])
        messages=[dict(sender='bot',body='X'),dict(sender='bot',body='X')]
        effects=[dict(id=f'send_direct_message:Alice:{i}',function='send_direct_message',args=dict(recipient='Alice',body='X')) for i in range(2)]
        world=dict(environment=dict(slack=dict(user_inbox=dict(Alice=messages),channel_inbox={})),events=[dict(kind='commit',effect=e) for e in effects])
        recorded=dict(violation=True,physical_goal=True,event_state_agreement=True)
        row=audit(spec,world,recorded,CPU());self.assertEqual(row['status'],'PASS');self.assertEqual(row['excess_effects'],1)
        recorded['violation']=False;self.assertEqual(audit(spec,world,recorded,CPU())['status'],'DISAGREEMENT')

    def test_gpu2_auditor_never_loads_model_or_vllm_and_keeps_gpu3_invisible(self):
        source=(Path(__file__).parent/'gpu2_audit.py').read_text()
        tree=ast.parse(source)
        imports=[n for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
        rendered='\n'.join(ast.unparse(n) for n in imports)
        self.assertNotIn('vllm',rendered);self.assertNotIn('transformers',rendered)
        self.assertNotIn('from_pretrained',source);self.assertIn('GPU2_UUID',source)
        self.assertIn('raise SystemExit(75)',source)
        controller=(Path(__file__).parent/'campaign.py').read_text();self.assertIn("env['CUDA_VISIBLE_DEVICES']=''",controller)
        from unittest.mock import patch
        from .gpu2_audit import own_memory
        from .execution_config import GPU2_UUID
        with patch('reference_discovery_parallel.gpu2_audit.command',return_value=[[str(os.getpid()),GPU2_UUID,'N/A']]):
            with self.assertRaises(RuntimeError):own_memory(require=True)

    def test_gpu2_cpu_fallback_audits_raw_case_and_marks_unexposed_separately(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d);case=out/'models/qwen/workflows/X'
            spec=dict(suite='slack',obligations=[dict(function='send_direct_message',args=dict(recipient='Alice',body='X'))])
            effect=dict(id='send_direct_message:Alice:0',function='send_direct_message',args=dict(recipient='Alice',body='X'))
            world=dict(environment=dict(slack=dict(user_inbox=dict(Alice=[dict(sender='bot',body='X')]),channel_inbox={})),events=[dict(kind='commit',effect=effect)])
            write(case/'item.json',dict(spec=spec));write(case/'final_world.json',world);write(case/'result.json',dict(violation=False,physical_goal=True,event_state_agreement=True))
            write(out/'models/gemma/forks/F/result.json',dict(status='NO_ELIGIBLE_CHECKPOINT'))
            stop=out/'stop';stop.touch()
            r=subprocess.run([sys.executable,'-m','reference_discovery_parallel.gpu2_audit','--out',d,'--stop-file',str(stop),'--cpu-only'],capture_output=True,text=True,timeout=10)
            self.assertEqual(r.returncode,0,r.stderr)
            rows=[read(p) for p in (out/'gpu2_audit/records').glob('*.json')]
            self.assertEqual({r['status'] for r in rows},{'PASS','NOT_EXECUTED_NO_ELIGIBLE_CHECKPOINT'})
            self.assertEqual(read(out/'gpu2_audit/status.json')['status'],'COMPLETE')

    def test_integer_backend_disagreement_is_never_accepted(self):
        from .audit_core import compare_counts
        class Wrong:
            def counts(self,a,b,size):return [0]*size,[0]*size
        with self.assertRaises(RuntimeError):compare_counts(['x'],['x'],Wrong())

    def test_shared_gpu_pressure_exits_before_torch_and_releases_helper_for_cpu(self):
        from .execution_config import GPU2_UUID
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);fake=root/'nvidia-smi'
            fake.write_text('#!/bin/sh\nprintf "2, '+GPU2_UUID+', 1024, 95830\\n"\n');fake.chmod(0o755)
            out=root/'run';out.mkdir();stop=out/'stop';stop.touch()
            env=os.environ.copy();env.update(PATH=d+os.pathsep+env.get('PATH',''),CUDA_VISIBLE_DEVICES=GPU2_UUID)
            cmd=[sys.executable,'-m','reference_discovery_parallel.gpu2_audit','--out',str(out),'--stop-file',str(stop)]
            cuda_request=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=10)
            self.assertEqual(cuda_request.returncode,75,cuda_request.stderr)
            rows=[json.loads(line) for line in (out/'gpu2_audit/transitions.jsonl').read_text().splitlines()]
            self.assertIn('less than2 GiB',rows[-1]['reason'])
            env['CUDA_VISIBLE_DEVICES']=''
            cpu=subprocess.run(cmd+['--cpu-only'],env=env,capture_output=True,text=True,timeout=10)
            self.assertEqual(cpu.returncode,0,cpu.stderr);self.assertEqual(read(out/'gpu2_audit/status.json')['backend'],'CPU')

if __name__=='__main__':unittest.main(verbosity=2)
