#!/usr/bin/env bash
set -euo pipefail
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$root"
sha256sum --quiet -c SHA256SUMS
old="$root/../IEEE_SP_FINAL_EXPERIMENT_GPU3"
if [[ -f "$old/logs/latest" ]]; then
  old="$(cd -- "$old" && pwd)"
  [[ "$root" != "$old" ]] || { echo "Run this from the new batched package directory"; exit 1; }
  run_id="$(<"$old/logs/latest")"
  [[ "$run_id" =~ ^[0-9]{8}T[0-9]{6}Z_[0-9]+_[0-9]+$ ]]
  if ! flock -n "$old/logs/study.lock" true; then
    python3 - "$old/run.py" "$old/runs/$run_id" <<'PY'
from pathlib import Path
import os
import signal
import sys

script, run = sys.argv[1:]

def command(process):
    args = process.joinpath("cmdline").read_bytes().decode().strip("\0").split("\0")
    if args[1:2] == ["-u"]:
        del args[1]
    if args[1:2] == ["run.py"]:
        args[1] = str(process.joinpath("cwd", "run.py").resolve(strict=True))
    return args

def matches(args):
    return (len(args) >= 4 and args[1] == script and "--out" in args and
            args[args.index("--out") + 1:][:1] == [run] and "--archive" in args)

workers = []
for process in Path("/proc").iterdir():
    if not process.name.isdecimal():
        continue
    try:
        if process.stat().st_uid != os.getuid():
            continue
        args = command(process)
        if not matches(args) or "--profile" not in args:
            continue
        if args[args.index("--profile") + 1:][:1] not in (["qwen"], ["gemma"]):
            continue
        ppid = next(line.split()[1] for line in (process / "status").read_text().splitlines()
                    if line.startswith("PPid:"))
        parent = command(Path("/proc") / ppid)
        if matches(parent) and "--profile" not in parent:
            workers.append((int(process.name), args))
    except (OSError, UnicodeError, StopIteration):
        continue
if len(workers) != 1:
    raise SystemExit("Expected exactly one verified serial study worker. No process was stopped.")
pid, args = workers[0]
handle = os.pidfd_open(pid)
try:
    if command(Path("/proc") / str(pid)) != args:
        raise SystemExit("Serial study worker changed. No process was stopped.")
    signal.pidfd_send_signal(handle, signal.SIGTERM)
finally:
    os.close(handle)
print(f"Stopped serial study worker {pid}. Waiting for its controller to archive {run}.")
PY
    flock -w 180 "$old/logs/study.lock" true
    [[ -s "$old/runs/$run_id.zip" ]] || { echo "Serial run archive is missing"; exit 1; }
    printf 'Previous run archive: %s/runs/%s.zip\n' "$old" "$run_id"
  fi
fi
exec bash RUN_STUDY.sh --stage all --engine local "$@"
