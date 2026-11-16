"""Own one server at a time and run two isolated jobs concurrently."""
from __future__ import annotations

import argparse
import collections
import os
import signal
import subprocess
import sys
import time
import traceback
import threading
from pathlib import Path

from .util import ROOT, activate, append, read, write


class StopRequested(BaseException):
    pass


def main(args):
    common = activate(args.family)
    from reference_discovery_parallel.base import serving
    from reference_discovery_parallel.models import command, PROFILES
    from reference_discovery_parallel.live_profile import qualify as qualify_live
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    frozen = read(args.manifest)
    jobs = frozen['E1'] + frozen['E2'] + [item for block in frozen['E3_blocks'] for item in block]
    census = {item['id']: 'SCHEDULED' for item in jobs}
    status = {'status': 'STARTING', 'profile': args.family, 'total': len(jobs), 'started_epoch': time.time()}
    server = None
    owned = {}
    server_log = None
    active = {}
    completed = 0
    durations = collections.defaultdict(list)
    interrupted = False
    error = None
    last_beat = -1e9
    epoch = 0
    telemetry_stop = threading.Event()
    telemetry_thread = None

    def checkpoint(**values):
        status.update(values, completed=completed, active=list(active), elapsed_seconds=time.time() - status['started_epoch'])
        write(out / 'status.json', status)
        write(out / 'census.json', census)

    def check_time():
        if args.deadline is not None and time.time() >= args.deadline:
            raise StopRequested('Optional collection deadline reached; remaining cells stay unexecuted')

    def heartbeat(force=False):
        nonlocal last_beat
        now = time.monotonic()
        if not force and now - last_beat < 20:
            return
        last_beat = now
        checkpoint()
        print(f'HEARTBEAT profile={args.family} status={status["status"]} recorded={completed}/{len(jobs)} '
              f'active={list(active)} elapsed={int(status["elapsed_seconds"])}s', flush=True)

    def refresh_owned():
        if server is not None and server.poll() is None and serving.proc_start(server.pid) == owned.get(server.pid):
            for pid in serving.descendant_pids(server.pid):
                owned.setdefault(pid, serving.proc_start(pid))
            write(out / 'serving' / 'owned_identities.json', {str(k): v for k, v in owned.items()})

    def start_server():
        nonlocal server, server_log, owned
        check_time()
        serving.verify_pid_namespace()
        if args.lock_fd is None:
            raise RuntimeError('Live profile requires the parent-held GPU lock')
        shared = args.project_root / 'logs/gpu3_sequence.lock'
        if os.fstat(args.lock_fd).st_ino != shared.stat().st_ino:
            raise RuntimeError('Inherited GPU lock does not match project lock')
        gpu = next((row for row in serving.gpu_table() if row[0].strip() == '3'), None)
        if not gpu or gpu[1].strip() != common.GPU_UUID:
            raise RuntimeError('Physical GPU 3 does not match pinned UUID; no other GPU will be used')
        serving.ensure_free(common.GPU_UUID)
        serving.ensure_port_free()
        p = PROFILES[args.family]
        snapshot, identity = serving.inspect_snapshot(Path(args.cache) / ('models--' + p['hub'].replace('/', '--')), p['hub'], p['revision'])
        folder = out / 'serving' / f'epoch_{epoch:02d}'
        folder.mkdir(parents=True, exist_ok=False)
        write(folder / 'snapshot_identity.json', identity)
        env = os.environ.copy()
        for name in ('PYTHONHOME', 'PYTHONPATH', 'VLLM_API_KEY', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY',
                     'http_proxy', 'https_proxy', 'all_proxy'):
            env.pop(name, None)
        env.update(CUDA_VISIBLE_DEVICES=common.GPU_UUID, CUDA_DEVICE_ORDER='PCI_BUS_ID',
                   HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', VLLM_NO_USAGE_STATS='1',
                   DO_NOT_TRACK='1', HF_HUB_DISABLE_TELEMETRY='1',
                   PATH=str(args.serving_python.parent) + os.pathsep + env.get('PATH', ''),
                   PYTHONPATH=str(ROOT / 'retained'))
        cmd = command(args.serving_python, snapshot, args.family)
        write(folder / 'command.json', {'argv': cmd, 'physical_gpu': 3, 'gpu_uuid': common.GPU_UUID,
                                       'template_profile': p['interface'], 'cwd': str(ROOT)})
        server_log = (folder / 'server.log').open('w')
        server = subprocess.Popen(cmd, cwd=ROOT, env=env, stdout=server_log, stderr=subprocess.STDOUT, start_new_session=True)
        owned = {server.pid: serving.proc_start(server.pid)}
        write(folder / 'owned_process.json', {'pid': server.pid, 'start': owned[server.pid]})
        checkpoint(status='STARTING_SERVER', server_epoch=epoch)
        started = time.monotonic()
        while True:
            check_time()
            if server.poll() is not None:
                raise RuntimeError('Owned server exited during startup: ' + str(folder / 'server.log'))
            refresh_owned()
            try:
                models = serving.read_json_url('http://127.0.0.1:18080/v1/models')
                if models.get('data') and models['data'][0].get('id') == p['alias']:
                    break
            except Exception:
                pass
            if time.monotonic() - started > 1800:
                raise RuntimeError('Owned server startup watchdog (1800 seconds)')
            heartbeat()
            time.sleep(2)
        import re
        descendants = serving.descendant_pids(server.pid)
        listeners = {int(value) for value in re.findall(r'pid=(\d+)', serving.command(['ss', '-ltnp', '( sport = :18080 )']))}
        applications = serving.gpu_applications()
        workers = [row for row in applications if len(row) > 1 and row[0].strip().isdigit() and int(row[0]) in descendants]
        foreign = [row for row in applications if len(row) > 1 and row[1].strip() == common.GPU_UUID
                   and row[0].strip().isdigit() and int(row[0]) not in descendants]
        if not listeners or not listeners <= descendants or not workers or foreign or any(row[1].strip() != common.GPU_UUID for row in workers):
            raise RuntimeError('Endpoint or GPU workers do not belong exclusively to the owned GPU-3 server')
        write(folder / 'placement.json', {'listeners': sorted(listeners), 'workers': workers,
                                         'physical_gpu': 3, 'gpu_uuid': common.GPU_UUID, 'qualified': True})
        write(folder / 'models.json', models)
        try:
            write(folder / 'server_info.json', serving.read_json_url('http://127.0.0.1:18080/server_info?config_format=json'))
        except Exception as exc:
            write(folder / 'server_info.json', {'status': 'UNAVAILABLE', 'error': str(exc)})
        qualify_live(folder / 'live_profile_qualification')
        print('QUALIFIED', args.family, 'physical GPU 3; two isolated job workers.', flush=True)
        checkpoint(status='RUNNING', server_epoch=epoch)

    def stop_server():
        nonlocal server_log
        if server is not None:
            refresh_owned()
            serving.stop_owned(server, owned, out / 'serving' / f'shutdown_epoch_{epoch:02d}.json')
        if server_log is not None:
            server_log.close()
            server_log = None

    def finish_worker(ident, entry, forced=False):
        nonlocal completed
        process, log, item, started, output = entry
        code = process.poll()
        if code is None:
            return False
        log.close()
        path = output / 'result.json'
        if path.is_file():
            result = read(path)
        else:
            output.mkdir(parents=True, exist_ok=True)
            result = dict(id=ident, panel=item['panel'], profile=args.family, attempted=True,
                          status='WORKER_DEADLINE' if forced else 'WORKER_EXIT_WITHOUT_RESULT',
                          qualified=False, exit_code=code, scientific_negative=False, mock=args.mock)
            write(path, result)
        result.update(execution_worker_pid=process.pid, server_epoch=epoch,
                      controller_exit_code=code, supervisor_forced=forced)
        write(path, result)
        census[ident] = result['status']
        durations[item['panel']].append(time.monotonic() - started)
        append(out / 'schedule_events.jsonl', dict(event='END', epoch=time.time(), id=ident,
                  panel=item['panel'], status=result['status'], qualified=result['qualified'], server_epoch=epoch))
        completed += 1
        print(f'{args.family} {completed}/{len(jobs)} {ident}: {result["status"]}; qualified={result["qualified"]}', flush=True)
        return True

    def run_group(group):
        nonlocal epoch
        waiting = collections.deque(group)
        while waiting or active:
            check_time()
            if not args.mock and server.poll() is not None:
                if not active:
                    if epoch >= 1:
                        raise RuntimeError('Owned server restart limit reached; no scientific redraws')
                    stop_server()
                    epoch += 1
                    start_server()
            while waiting and len(active) < args.workers and (args.mock or server.poll() is None):
                item = waiting.popleft()
                ident = item['id']
                input_path = out / 'job_inputs' / (ident + '.json')
                write(input_path, item)
                output = out / item['panel'] / ident
                log_path = out / 'worker_logs' / (ident + '.log')
                log_path.parent.mkdir(parents=True, exist_ok=True)
                log = log_path.open('w')
                cmd = [sys.executable, '-u', '-m', 'permission_admission.worker', '--item', str(input_path),
                       '--out', str(output), '--family', args.family] + (['--mock'] if args.mock else [])
                env = os.environ.copy()
                env.update(CUDA_VISIBLE_DEVICES='', PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1')
                env.pop('PYTHONPATH', None)
                process = subprocess.Popen(cmd, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
                active[ident] = (process, log, item, time.monotonic(), output)
                census[ident] = 'RUNNING'
                append(out / 'schedule_events.jsonl', dict(event='START', epoch=time.time(), id=ident,
                          panel=item['panel'], pid=process.pid, server_epoch=epoch,
                          argv=cmd, concurrency=args.workers))
            for ident, entry in list(active.items()):
                process = entry[0]
                forced = time.monotonic() - entry[3] > 1350
                if forced and process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=30)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                if finish_worker(ident, entry, forced):
                    del active[ident]
            refresh_owned()
            heartbeat()
            if active:
                time.sleep(.15 if args.mock else 1)

    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(StopRequested('SIGTERM')))
    try:
        if not args.mock:
            start_server()
            telemetry_thread = threading.Thread(target=serving.telemetry, args=(out, telemetry_stop), daemon=True)
            telemetry_thread.start()
        else:
            checkpoint(status='MOCK_RUNNING_ZERO_INFERENCE')
        run_group(frozen['E1'])
        run_group(frozen['E2'])
        for block in frozen['E3_blocks']:
            run_group(block)  # barrier keeps all six carrier/policy arms local
        checkpoint(status='MOCK_COMPLETE_ZERO_INFERENCE' if args.mock else 'COMPLETE_REVIEW_PENDING')
    except BaseException as exc:
        interrupted = isinstance(exc, (StopRequested, KeyboardInterrupt))
        error = {'type': type(exc).__name__, 'message': str(exc), 'traceback': traceback.format_exc()}
        write(out / 'fatal_error.json', error)
        checkpoint(status='INTERRUPTED' if interrupted else 'FAILED', error=error)
    finally:
        for entry in active.values():
            if entry[0].poll() is None:
                entry[0].terminate()
        for ident, entry in list(active.items()):
            try:
                entry[0].wait(timeout=35)
            except subprocess.TimeoutExpired:
                entry[0].kill()
                entry[0].wait()
            finish_worker(ident, entry, True)
        active.clear()
        try:
            stop_server()
        except Exception as exc:
            error = {'type': type(exc).__name__, 'message': str(exc)}
            checkpoint(status='OWNED_CLEANUP_FAILED', cleanup_error=error)
        telemetry_stop.set()
        if telemetry_thread:
            telemetry_thread.join(timeout=35)
        for ident, state in census.items():
            if state in ('SCHEDULED', 'RUNNING'):
                census[ident] = 'NOT_EXECUTED_' + status['status']
        checkpoint(finished_epoch=time.time(), durations={k: {'count': len(v), 'mean_seconds': sum(v) / len(v)}
                                                        for k, v in durations.items() if v})
        heartbeat(True)
    return 1 if error else 0


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--family', choices=['qwen', 'gemma'], required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--project-root', type=Path, required=True)
    p.add_argument('--serving-python', type=Path, required=True)
    p.add_argument('--cache', required=True)
    p.add_argument('--lock-fd', type=int)
    p.add_argument('--deadline', type=float)
    p.add_argument('--workers', type=int, default=2, choices=[1, 2])
    p.add_argument('--mock', action='store_true')
    raise SystemExit(main(p.parse_args()))

