"""D2 step 1: eligibility census of the unmodified AgentDojo v1 user tasks (CPU, no model).

For every user task in banking, slack, workspace and travel, the census takes the benchmark's own
ground-truth calls on the task's default environment, keeps the privileged (state-changing) calls
under the frozen detector rule, and labels where each argument value comes from:

  prompt       the value appears in the user prompt (the user specified it)
  environment  the value is absent from the prompt but present in the task's environment
               (the user delegated it to tool content)
  derived      neither (composed, normalized or computed by the agent)

A task is ELIGIBLE for the D2 primary analysis if at least one privileged ground-truth call takes an
authority-relevant argument (who / where / how much / which object) from the environment: the
natural counterpart of the bridge's tool-supplied identifier. The census is deterministic and is
frozen before any D2 model run; its output fixes the D2 sampling frame.

Usage (AgentDojo 0.1.35 interpreter):  python census.py --out census.json
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path

from agentdojo.task_suite.load_suites import get_suite

SUITES = ("banking", "slack", "workspace", "travel")
# Frozen detector privileged rule (IEEE_SP_GATE1_KILL_TEST/data/historical_guard.json).
EXPLICIT = {"add_calendar_event_participants", "add_user_to_channel", "book_hotel", "book_restaurant", "book_flight",
            "cancel_calendar_event", "create_calendar_event", "delete_calendar_event", "delete_email", "delete_file",
            "invite_user_to_slack", "move_file", "remove_calendar_event_participants", "remove_user_from_channel",
            "reserve_restaurant", "send_email", "send_message", "send_money", "send_slack_message", "share_file",
            "transfer_money", "update_calendar_event", "update_file", "update_password",
            "update_scheduled_transaction"}
PREFIXES = ("send_", "post_", "create_", "update_", "add_", "remove_", "delete_", "reserve_", "cancel_",
            "schedule_", "transfer_", "book_", "pay_", "invite_", "share_", "move_")
# Strong authority-relevant arguments decide who receives an effect, where it goes, how much, or which
# object it touches. Weak ones (time, place) are recorded but do not make a task eligible on their own.
STRONG_KEYS = {"recipient", "recipients", "cc", "bcc", "channel", "user", "user_email", "email", "participants",
               "url", "iban", "amount", "file_id", "event_id", "email_id", "id", "hotel", "restaurant",
               "company", "password"}
WEAK_KEYS = {"date", "start_time", "end_time", "start_day", "end_day", "location"}
AUTHORITY_KEYS = STRONG_KEYS | WEAK_KEYS


def privileged(name):
    if name in EXPLICIT:
        return True
    if name.startswith(("get_", "search_", "list_")):
        return False
    return name.startswith(PREFIXES)


def atoms(value):
    """Leaf values of an argument, as comparable strings."""
    if value is None or isinstance(value, bool):
        return []
    if isinstance(value, (list, tuple)):
        return [a for v in value for a in atoms(v)]
    if isinstance(value, dict):
        return [a for v in value.values() for a in atoms(v)]
    if isinstance(value, float):
        forms = {repr(value), f"{value:.2f}"}
        if value == int(value):
            forms.add(str(int(value)))
        return [sorted(forms)]
    if isinstance(value, int):
        return [[str(value)]]
    text = str(value).strip()
    return [[text]] if text else []


def provenance(forms, prompt, environment):
    low_prompt, low_env = prompt.lower(), environment.lower()
    if any(f.lower() in low_prompt for f in forms):
        return "prompt"
    if any(f.lower() in low_env for f in forms):
        return "environment"
    return "derived"


def census_task(suite, task_id, task):
    env = suite.load_and_inject_default_environment({})
    env = task.init_environment(env)
    dump = json.dumps(env.model_dump(mode="json"), ensure_ascii=False, default=str)
    prompt = task.PROMPT
    calls = []
    for index, call in enumerate(task.ground_truth(env.model_copy(deep=True))):
        if not privileged(call.function):
            continue
        args = []
        for key, value in sorted(dict(call.args).items()):
            for forms in atoms(value):
                args.append({"key": key, "value": forms[0], "source": provenance(forms, prompt, dump),
                             "authority_relevant": key in AUTHORITY_KEYS})
        chars = {s: sum(len(a["value"]) for a in args if a["source"] == s) for s in ("prompt", "environment", "derived")}
        total = sum(chars.values())
        fraction = chars["prompt"] / total if total else None
        label = (None if fraction is None else "SPECIFIED" if fraction == 1 else
                 "DELEGATED" if chars["prompt"] == 0 and chars["environment"] > 0 else "PARTIAL")
        calls.append({"index": index, "function": call.function, "args": args, "specified_fraction": fraction,
                      "label": label,
                      "delegated_authority_args": sorted({a["key"] for a in args
                                                          if a["authority_relevant"] and a["source"] == "environment"}),
                      "delegated_strong_args": sorted({a["key"] for a in args
                                                       if a["key"] in STRONG_KEYS and a["source"] == "environment"})})
    eligible = any(c["delegated_strong_args"] for c in calls)
    return {"suite": suite.name, "task": task_id, "prompt": prompt, "privileged_calls": calls,
            "n_privileged": len(calls), "eligible_delegated_authority": eligible,
            "weak_only_delegation": (not eligible) and any(c["delegated_authority_args"] for c in calls)}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    if version("agentdojo") != "0.1.35":
        raise SystemExit("AgentDojo 0.1.35 is required")
    rows, failures = [], []
    for name in SUITES:
        suite = get_suite("v1", name)
        for task_id, task in sorted(suite.user_tasks.items(), key=lambda kv: int(kv[0].rsplit("_", 1)[1])):
            try:
                rows.append(census_task(suite, task_id, task))
            except Exception as exc:  # recorded, never silently dropped
                failures.append({"suite": name, "task": task_id, "error": repr(exc)})
    summary = {}
    for name in SUITES:
        mine = [r for r in rows if r["suite"] == name]
        labels = [c["label"] for r in mine for c in r["privileged_calls"]]
        summary[name] = {"tasks": len(mine), "tasks_with_privileged_call": sum(r["n_privileged"] > 0 for r in mine),
                         "eligible_delegated_authority": sum(r["eligible_delegated_authority"] for r in mine),
                         "weak_only_delegation": sum(r["weak_only_delegation"] for r in mine),
                         "privileged_calls": len(labels),
                         "labels": {str(k): labels.count(k) for k in ("SPECIFIED", "PARTIAL", "DELEGATED", None)}}
    body = {"census": "D2_NATURAL_CENSUS_V1", "agentdojo": version("agentdojo"),
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "census_script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "rule": {"privileged_explicit": sorted(EXPLICIT), "privileged_prefixes": list(PREFIXES),
                     "strong_keys": sorted(STRONG_KEYS), "weak_keys": sorted(WEAK_KEYS),
                     "eligibility": "a privileged ground-truth call takes a strong key's value from the environment"},
            "summary": summary, "failures": failures, "tasks": rows}
    args.out.write_text(json.dumps(body, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"summary": summary, "failures": len(failures), "out": str(args.out)}, indent=1))


if __name__ == "__main__":
    main()
