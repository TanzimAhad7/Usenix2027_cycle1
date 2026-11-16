"""N2 controller: for each profile (Qwen, then Gemma) start the same vLLM server the N1 run used, on physical
GPU 3 only, qualify the tool interface, run every episode, stop the server. Resumable: finished episodes
(result.json present) are kept and not redrawn.

  python -m n2.controller --run RUN_DIR [--profiles qwen gemma] [--mock] [--limit N]
"""
from __future__ import annotations
import argparse, csv, io, json, os, signal, socket, subprocess, sys, threading, time, traceback, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GPU_INDEX = 3
GPU_UUID = 'GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6'
PORT = 18081
N1_RUN = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/IEEE_SP_N1_GPU3/results/user_runs/n1_gpu3_20261102T002508Z_229688_30263')
WORKERS = 8


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def say(*a):
    print(f'[{now()}]', *a, flush=True)


def write(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp'); tmp.write_text(json.dumps(value, indent=1, default=str) + '\n'); tmp.replace(path)


def gpu_check():
    rows = list(csv.reader(io.StringIO(subprocess.check_output(
        ['nvidia-smi', '--query-gpu=index,uuid', '--format=csv,noheader'], text=True))))
    if not any(r[0].strip() == str(GPU_INDEX) and r[1].strip() == GPU_UUID for r in rows):
        raise RuntimeError('Physical GPU 3 UUID mismatch; no other GPU will be used')
    apps = subprocess.check_output(['nvidia-smi', '--query-compute-apps=pid,gpu_uuid', '--format=csv,noheader'], text=True)
    busy = [l for l in apps.splitlines() if GPU_UUID in l]
    if busy:
        raise RuntimeError('GPU 3 has compute processes; none were stopped: ' + str(busy))
    with socket.socket() as s:
        try:
            s.bind(('127.0.0.1', PORT))
        except OSError:
            raise RuntimeError(f'Port {PORT} is occupied; the existing service is neither used nor stopped')


def server_argv(profile):
    argv = json.loads((N1_RUN / profile / 'serving' / 'command.json').read_text())['argv']
    for p in argv:
        if p.startswith('/') and not Path(p).exists():
            raise RuntimeError(f'N1 server path missing: {p}')
    return argv


def start_server(profile, folder):
    argv = server_argv(profile)
    alias = argv[argv.index('--served-model-name') + 1]
    env = {k: v for k, v in os.environ.items() if k not in ('PYTHONHOME', 'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy',
                                                           'ALL_PROXY', 'all_proxy', 'VLLM_API_KEY')}
    env.update(CUDA_VISIBLE_DEVICES=GPU_UUID, CUDA_DEVICE_ORDER='PCI_BUS_ID', HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
               VLLM_NO_USAGE_STATS='1', DO_NOT_TRACK='1', HF_HUB_DISABLE_TELEMETRY='1', PYTHONNOUSERSITE='1',
               PYTHONPATH=str(N1_RUN / 'source' / 'retained') + os.pathsep + str(N1_RUN / 'source'))
    write(folder / 'command.json', dict(argv=argv, alias=alias, physical_gpu=GPU_INDEX, gpu_uuid=GPU_UUID,
                                        source=f'copied verbatim from {N1_RUN / profile / "serving" / "command.json"}'))
    log = (folder / 'server.log').open('w')
    proc = subprocess.Popen(argv, cwd=str(N1_RUN / 'source'), env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    write(folder / 'server_process.json', dict(pid=proc.pid, pgid=proc.pid))
    t0 = time.monotonic()
    while True:
        if proc.poll() is not None:
            raise RuntimeError(f'vLLM server exited (code {proc.returncode}); see {folder / "server.log"}')
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{PORT}/v1/models', timeout=5) as r:
                data = json.load(r)
            if data.get('data') and data['data'][0]['id'] == alias:
                break
        except Exception:
            pass
        if time.monotonic() - t0 > 1800:
            raise RuntimeError('vLLM server did not become ready within 1800 s')
        time.sleep(3)
    say('SERVER READY', profile, alias, f'{int(time.monotonic() - t0)} s')
    return proc, log, alias


def stop_server(proc, log, folder):
    if proc is None:
        return
    for sig, wait in ((signal.SIGTERM, 60), (signal.SIGKILL, 20)):
        if proc.poll() is not None:
            break
        try:
            os.killpg(proc.pid, sig)  # only the group this controller created (start_new_session=True)
        except ProcessLookupError:
            break
        try:
            proc.wait(timeout=wait)
        except subprocess.TimeoutExpired:
            pass
    write(folder / 'shutdown.json', dict(returncode=proc.poll(), at=now()))
    log.close()


def qualify(client, alias, folder):
    """Same two infrastructure probes as the project's live qualification. Not a scientific outcome."""
    tools = [dict(type='function', function=dict(name='qualification_echo', description='Echo the supplied marker.',
             parameters=dict(type='object', properties=dict(marker=dict(type='string')), required=['marker'])))]
    msgs = [dict(role='system', content='Follow the user task using the available tools.'),
            dict(role='user', content='Call qualification_echo once with marker "QUALIFICATION_ARGUMENT_4721". After receiving '
                                      'its result, report the exact result text without calling another tool.')]
    r1 = client.chat.completions.create(model=alias, messages=msgs, tools=tools, tool_choice='auto', temperature=0.0, max_tokens=4096)
    calls = r1.choices[0].message.tool_calls or []
    if len(calls) != 1 or json.loads(calls[0].function.arguments) != {'marker': 'QUALIFICATION_ARGUMENT_4721'}:
        raise RuntimeError('Tool-call probe failed; no scientific episode was run')
    msgs += [dict(role='assistant', content=r1.choices[0].message.content,
                  tool_calls=[c.model_dump(mode='json') for c in calls]),
             dict(role='tool', tool_call_id=calls[0].id, name='qualification_echo', content='QUALIFICATION_RESULT_4721')]
    r2 = client.chat.completions.create(model=alias, messages=msgs, tools=tools, tool_choice='auto', temperature=0.0, max_tokens=4096)
    if r2.choices[0].message.tool_calls or 'QUALIFICATION_RESULT_4721' not in (r2.choices[0].message.content or ''):
        raise RuntimeError('Tool-result continuation probe failed; no scientific episode was run')
    write(folder / 'qualification.json', dict(status='PASS', probes=2, at=now()))


def run_profile(run, design, profile, mock, limit):
    from n2.episode import run as run_episode
    out = run / profile
    (out / 'serving').mkdir(parents=True, exist_ok=True)
    units = {u['unit']: u for u in design['units']}
    import random
    eps = list(design['episodes'])
    if limit:  # smoke: greedy draw only, arms interleaved so every arm is exercised
        by_arm = {}
        for e in eps:
            if e['draw'] == 0:
                by_arm.setdefault(e['arm'], []).append(e)
        eps = [x for group in zip(*by_arm.values()) for x in group][:limit]
    random.Random(20261116).shuffle(eps)  # fixed order; arms and draws interleaved over time
    todo = [e for e in eps if not (out / 'episodes' / e['id'] / 'result.json').exists()]
    status = dict(profile=profile, planned=len(eps), already_done=len(eps) - len(todo), done=0, failed=0, started=now(), mock=mock)
    write(out / 'status.json', status)
    proc = log = client = None
    alias = 'mock'
    try:
        if not mock:
            gpu_check()
            proc, log, alias = start_server(profile, out / 'serving')
            import openai
            client = openai.OpenAI(api_key='EMPTY', base_url=f'http://127.0.0.1:{PORT}/v1', max_retries=2, timeout=900)
            qualify(client, alias, out / 'serving')
        say('START', profile, f'{len(todo)} episodes to run, {status["already_done"]} kept')
        lock = threading.Lock()

        def one(ep):
            folder = out / 'episodes' / ep['id']
            try:
                res, messages = run_episode(ep, units.get(ep['unit']), [u for u in units.values() if (u['suite'], u['task']) == (ep['suite'], ep['task'])], client, alias, mock)
            except Exception as e:
                res, messages = dict(id=ep['id'], status='HARNESS_ERROR', error=dict(type=type(e).__name__, message=str(e),
                                     traceback=traceback.format_exc()[-4000:])), []
            from agentdojo.types import get_text_content_as_str
            write(folder / 'messages.json', [dict(role=m['role'], content=get_text_content_as_str(m['content']) if m.get('content') else None,
                                                  tool_calls=[dict(function=c.function, args=c.args, id=c.id) for c in (m.get('tool_calls') or [])] if m['role'] == 'assistant' else None,
                                                  error=m.get('error'), tool=m['tool_call'].function if m['role'] == 'tool' else None)
                                             for m in messages])
            write(folder / 'result.json', res)
            return res

        with ThreadPoolExecutor(max_workers=1 if mock else WORKERS) as pool:
            futures = [pool.submit(one, e) for e in todo]
            for i, f in enumerate(as_completed(futures), 1):
                r = f.result()
                with lock:
                    status['done'] += 1
                    status['failed'] += r.get('status') not in ('COMPLETE', 'ITERATION_LIMIT')
                    status['updated'] = now()
                    write(out / 'status.json', status)
                if i % 10 == 0 or i == len(todo):
                    say(profile, f'{status["already_done"] + status["done"]}/{len(eps)} done; technical failures {status["failed"]}')
        status['phase'] = 'PROFILE_COMPLETE'
    except BaseException as e:
        status['phase'] = 'PROFILE_FAILED'
        status['error'] = dict(type=type(e).__name__, message=str(e), traceback=traceback.format_exc()[-4000:])
        say('PROFILE FAILED', profile, e)
    finally:
        write(out / 'status.json', status)
        stop_server(proc, log, out / 'serving')
    return status


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--run', type=Path, required=True)
    p.add_argument('--profiles', nargs='+', default=['qwen', 'gemma'], choices=('qwen', 'gemma'))
    p.add_argument('--mock', action='store_true')
    p.add_argument('--limit', type=int, default=0)
    a = p.parse_args()
    sys.path.insert(0, str(ROOT))
    from n2.design import build, sha, S0_INPUTS
    a.run.mkdir(parents=True, exist_ok=True)
    frozen = ROOT / 'inputs' / 'design.json'
    design = json.loads(frozen.read_text())
    rebuilt = build()
    if rebuilt['design_sha256'] != design['design_sha256'] or sha(S0_INPUTS) != design['s0_inputs_sha256']:
        raise SystemExit('Frozen design or S0 inputs changed; refusing to run')
    write(a.run / 'design_used.json', dict(design_sha256=design['design_sha256'], profiles=a.profiles, mock=a.mock, limit=a.limit))
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt('SIGTERM')))
    summary = {}
    for prof in a.profiles:
        summary[prof] = run_profile(a.run, design, prof, a.mock, a.limit)
    write(a.run / 'run_status.json', dict(finished=now(), profiles={k: v.get('phase') for k, v in summary.items()}))
    say('ALL PROFILES DONE', json.dumps({k: v.get('phase') for k, v in summary.items()}))


if __name__ == '__main__':
    main()
