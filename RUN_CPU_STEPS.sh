#!/usr/bin/env bash
# All CPU-only steps of RUN_EVERYTHING.md, in order, into one log: logs_master/cpu_<stamp>.log
# No GPU is used (CUDA_VISIBLE_DEVICES=""). Each step is independent: a failure is logged and the next runs.
#   bash RUN_CPU_STEPS.sh            # run everything (about 5-15 min)
#   tail -F logs_master/cpu_latest.log
set -uo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
mkdir -p logs_master
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
log="$ROOT/logs_master/cpu_${stamp}.log"
ln -sfn "cpu_${stamp}.log" logs_master/cpu_latest.log
export CUDA_VISIBLE_DEVICES=""
declare -A RESULT

step() {  # step NAME DIR COMMAND...
  local name="$1" dir="$2"; shift 2
  echo "==== [$(date -u +%FT%TZ)] START $name ($dir: $*)" | tee -a "$log"
  if (cd "$ROOT/$dir" && "$@") >>"$log" 2>&1; then RESULT[$name]=OK; else RESULT[$name]="FAILED($?)"; fi
  echo "==== [$(date -u +%FT%TZ)] END $name: ${RESULT[$name]}" | tee -a "$log"
}

step gate2_package_test   IEEE_SP_GATE2_VALUE_SELECTION bash RUN_GATE2.sh test
step gate1_audit          IEEE_SP_GATE1_KILL_TEST        bash RUN_GATE1.sh audit \
     runs/20261110T180408Z_gate1_all_qwen runs/20261110T180408Z_gate1_all_gemma
step d0_package_test      IEEE_SP_FINAL_EXPERIMENT_D0    bash RUN_D0.sh test
# recover-qwen starts detached (setsid nohup) and returns at once; its PID and own log path go into this log.
step d0_recover_qwen      IEEE_SP_FINAL_EXPERIMENT_D0    bash RUN_D0.sh recover-qwen
if [[ -e IEEE_SP_D2_NATURAL/census_frozen.json ]]; then
  echo "==== d2_census: already frozen (IEEE_SP_D2_NATURAL/census_frozen.json); skipped" | tee -a "$log"
  RESULT[d2_census]="ALREADY_FROZEN"
else
  step d2_census          IEEE_SP_D2_NATURAL             bash RUN_CENSUS.sh
fi

echo "==== SUMMARY ($log)" | tee -a "$log"
for k in gate2_package_test gate1_audit d0_package_test d0_recover_qwen d2_census; do
  printf '  %-20s %s\n' "$k" "${RESULT[$k]:-not run}" | tee -a "$log"
done
