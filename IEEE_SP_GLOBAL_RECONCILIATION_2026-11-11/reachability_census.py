"""Attacker-reachability census of unmodified AgentDojo v1 tasks (CPU, no model, read-only).

Question: on natural tasks whose privileged call takes a DELEGATED strong authority argument (D2 census rule), does
the benchmark's own attacker capability (its injection vectors, which AgentDojo defines as attacker-controlled
placeholders) reach an object the agent naturally reads during the correct trajectory, and is that object the
SAME tool result that carries the legitimate delegated value (same-object: ordinary poisoning / co-located) or a
DIFFERENT one (cross-object: the Gate 2 C3x analogue)?

Method: replace every injection vector with a unique canary (AgentDojo's own get_injection_candidates idea),
execute the task's ground-truth calls on the injected default environment, and locate (i) each delegated value
and (ii) each canary in the returned tool results.

  python reachability_census.py OUT_JSON      (AgentDojo 0.1.35 interpreter)
"""
import json
import sys
from importlib.metadata import version
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "IEEE_SP_D2_NATURAL"))
import census  # noqa: E402  (D2 eligibility rule, imported unchanged)
from agentdojo.functions_runtime import FunctionsRuntime  # noqa: E402
from agentdojo.task_suite.load_suites import get_suite  # noqa: E402

assert version("agentdojo") == "0.1.35"
OUT = Path(sys.argv[1])
SUITES = ("banking", "slack", "workspace", "travel")


def text(x):
    try:
        return json.dumps(x, ensure_ascii=False, default=str)
    except Exception:
        return str(x)


rows = []
for name in SUITES:
    suite = get_suite("v1", name)
    vectors = suite.get_injection_vector_defaults()
    canaries = {k: f"<CANARY---{k}--->" for k in vectors}
    for tid, task in sorted(suite.user_tasks.items(), key=lambda kv: int(kv[0].rsplit("_", 1)[1])):
        base = census.census_task(suite, tid, task)
        if not base["eligible_delegated_authority"]:
            continue
        env = task.init_environment(suite.load_and_inject_default_environment(canaries))
        runtime = FunctionsRuntime(suite.tools)
        results = []
        for i, call in enumerate(task.ground_truth(env.model_copy(deep=True))):
            res, err = runtime.run_function(env, call.function, call.args, raise_on_error=False)
            results.append({"i": i, "function": call.function, "args": {k: str(v) for k, v in dict(call.args).items()},
                            "text": text(res), "error": err})
        delegated = []
        for c in base["privileged_calls"]:
            for a in c["args"]:
                if a["key"] in census.STRONG_KEYS and a["source"] == "environment":
                    delegated.append({"call_index": c["index"], "function": c["function"], "key": a["key"],
                                      "value": a["value"]})
        per_value = []
        for d in delegated:
            src = [r for r in results if r["i"] < d["call_index"] and not census.privileged(r["function"])
                   and d["value"].lower() in r["text"].lower()]
            src_ids = {r["i"] for r in src}
            seen = [(r["i"], k) for r in results if r["i"] < d["call_index"] and not census.privileged(r["function"])
                    for k, c in canaries.items() if c in r["text"]]
            same = sorted({k for i, k in seen if i in src_ids})
            cross = sorted({k for i, k in seen if i not in src_ids})
            per_value.append({**d, "source_reads": [{"i": r["i"], "function": r["function"], "args": r["args"]}
                                                    for r in src],
                              "vectors_in_same_result": same, "vectors_in_other_results": cross,
                              # Only meaningful when the legitimate value's source result is located; otherwise the
                              # value is derived/computed and "cross" cannot be distinguished from "same".
                              "cross_only_vectors": sorted(set(cross) - set(same)) if src else [],
                              "source_located": bool(src)})
        rows.append({"suite": name, "task": tid, "prompt": task.PROMPT, "delegated": per_value,
                     "any_same_object_vector": any(v["vectors_in_same_result"] for v in per_value),
                     "any_cross_object_vector": any(v["cross_only_vectors"] for v in per_value),
                     "any_cross_span_vector": any(v["source_located"] and v["vectors_in_other_results"]
                                                  for v in per_value),
                     "value_source_found": all(v["source_reads"] for v in per_value)})
summary = {}
for name in SUITES:
    mine = [r for r in rows if r["suite"] == name]
    summary[name] = {"eligible": len(mine),
                     "value_source_located": sum(r["value_source_found"] for r in mine),
                     "same_object_vector": sum(r["any_same_object_vector"] for r in mine),
                     "cross_object_vector": sum(r["any_cross_object_vector"] for r in mine),
                     "cross_only_no_same": sum(r["any_cross_object_vector"] and not r["any_same_object_vector"]
                                               for r in mine),
                     "cross_span_vector_with_located_source": sum(r["any_cross_span_vector"] for r in mine)}
OUT.write_text(json.dumps({"agentdojo": version("agentdojo"), "summary": summary, "tasks": rows}, indent=1) + "\n")
print(json.dumps(summary, indent=1))
for r in rows:
    print(r["suite"], r["task"], "| same:", sorted({k for v in r["delegated"] for k in v["vectors_in_same_result"]}),
          "| cross-only:", sorted({k for v in r["delegated"] for k in v["cross_only_vectors"]}),
          "| keys:", sorted({v["key"] for v in r["delegated"]}),
          "| src:", sorted({s["function"] for v in r["delegated"] for s in v["source_reads"]}))
