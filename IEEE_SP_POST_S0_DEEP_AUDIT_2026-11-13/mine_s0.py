"""Post hoc, exploratory re-mining of the S0 open run (read-only; CPU). Every quantity here is EXPLORATORY.
  python mine_s0.py S0_PACKAGE RUN_DIR OUT_JSON      (AgentDojo 0.1.35 interpreter)
A field retention by class (free-text payload vs metadata envelope), per config
B attacker-writable slot (default injection-vector text) retention vs legitimate carried-value retention, same item
C record selection in multi-record results
D loss concentration across configs and item features; shrinkage
E candidate scorer false negatives (heavy shrinkage but E4 retained)
F +Y_t leakage (values of the proposed action that appear in the output but not in the original)
"""
import json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
import yaml
PKG, RUN, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(PKG)); import retention as R
from agentdojo.task_suite.load_suites import get_suite
nat = json.loads((PKG/"inputs/s0_inputs.json").read_text()); items = {i["item_id"]: i for i in nat["items"]}
scores = json.loads((RUN/"analysis/scores.json").read_text())
CONFIGS = ["R0","Q0","Q1","G0","G1"]
FREE = {"body","content","description","subject","title"}
def out(c,i): return json.loads((RUN/"outputs"/c/f"{i}.json").read_text())["text"]
def toks(s): return re.findall(r"[A-Za-z0-9@._'-]+", str(s).lower())
def kept(value, san):
    s = str(value).strip()
    if not s: return None
    if len(s) <= 40:
        return R.hit(san, s, re.IGNORECASE)
    t = toks(s); sset = set(toks(san))
    return sum(w in sset for w in t)/max(1,len(t)) >= 0.6
def recs(o):
    if isinstance(o, dict): yield o
    if isinstance(o, list):
        for x in o:
            if isinstance(x, dict): yield x
res = {"A":{}, "B":{}, "C":{}, "D":{}, "E":[], "F":{}}
vectors = {s: get_suite("v1", s).get_injection_vector_defaults() for s in ("banking","slack","workspace")}
for c in CONFIGS:
    fld = Counter(); slot = Counter(); rec = Counter(); shrink=[]; leak=[]
    for iid, it in items.items():
        o, s = it["untrusted_content"], out(c, iid)
        shrink.append((iid, round(len(s)/max(1,len(o)),3)))
        p = R.parse(o)
        records = list(recs(p))
        for r in records:
            for k, v in r.items():
                vals = v if isinstance(v, list) else list(v.keys()) if isinstance(v, dict) else [v]
                for x in vals:
                    if isinstance(x, bool) or x is None or isinstance(x,(dict,list)): continue
                    kk = kept(x, s)
                    if kk is None: continue
                    cls = "payload" if k in FREE else "envelope"
                    fld[(cls, bool(kk))] += 1
                    fld[(f"{cls}:{k}", bool(kk))] += 1
        if len(records) >= 2:
            n_kept = 0
            for r in records:
                ids = [v for k,v in r.items() if isinstance(v,(str,int,float)) and not isinstance(v,bool) and 2 <= len(str(v)) <= 60]
                if any(kept(v, s) for v in ids): n_kept += 1
            rec[("multi_items",)] += 1; rec[("records",)] += len(records); rec[("records_kept",)] += n_kept
            if n_kept < len(records): rec[("items_with_dropped_records",)] += 1
        # attacker-writable slot default text present in this item?
        legit = [r for r in scores if r["config"]==c and r["item_id"]==iid]
        legit_ok = all(r.get("E2") for r in legit)
        for name, default in vectors[it["suite"]].items():
            d = str(default).strip()
            if len(d) >= 8 and d in o:
                sk = bool(kept(d, s))
                slot[(f"legit_E2={legit_ok}", f"slot_kept={sk}")] += 1
                res["B"].setdefault("detail", []).append({"config": c, "item": iid, "vector": name, "slot_kept": sk, "legit_all_E2": legit_ok, "default": d[:70]})
        if c in ("Q1","G1"):
            for a in it.get("proposed_actions") or []:
                for v in a.get("args", {}).values():
                    for x in (v if isinstance(v, list) else [v]):
                        x = str(x)
                        if 3 <= len(x) <= 80 and not R.hit(o, x, re.IGNORECASE) and R.hit(s, x, re.IGNORECASE):
                            leak.append({"item": iid, "value": x})
    res["A"][c] = {f"{k[0]}|kept={k[1]}": v for k, v in sorted(fld.items(), key=str)}
    res["B"][c] = {"|".join(k): v for k, v in slot.items()}
    res["C"][c] = {k[0]: v for k, v in rec.items()}
    res["D"][c] = {"unchanged": sum(1 for i,_ in shrink if out(c,i).strip()==items[i]["untrusted_content"].strip()),
                   "ratio_lt_0.5": sum(r<0.5 for _,r in shrink), "ratio_0.5_0.95": sum(0.5<=r<0.95 for _,r in shrink),
                   "ratio_ge_0.95": sum(r>=0.95 for _,r in shrink)}
    res["F"][c] = leak
    lostitems = {r["item_id"] for r in scores if r["config"]==c and r["set"]=="natural" and not r.get("E4")}
    for iid, r in shrink:
        if r < 0.6 and iid not in lostitems:
            res["E"].append({"config": c, "item": iid, "ratio": r})
per_item = defaultdict(set)
for r in scores:
    if r["set"]=="natural" and not r.get("E4"): per_item[r["item_id"]].add(r["config"])
res["D"]["items_lost_by_n_configs"] = dict(Counter(len(v) for v in per_item.values()))
res["D"]["lost_items"] = {k: sorted(v) for k, v in sorted(per_item.items())}
feat = {}
for iid, it in items.items():
    p = R.parse(it["untrusted_content"]); n = len(list(recs(p)))
    has_free = any(k in FREE for r in recs(p) for k in r)
    feat[iid] = {"tool": it["source_tool"], "chars": len(it["untrusted_content"]), "records": n,
                 "kind": "prose" if n==0 and not isinstance(p, list) else "plain_list" if n==0 else "records_with_freetext" if has_free else "records_no_freetext",
                 "lost_in": sorted(per_item.get(iid, []))}
res["D"]["by_kind"] = {}
for k in sorted({f["kind"] for f in feat.values()}):
    sel = [f for f in feat.values() if f["kind"]==k]
    res["D"]["by_kind"][k] = {"items": len(sel), "lost_in_any": sum(bool(f["lost_in"]) for f in sel),
                              "item_config_losses": sum(len(f["lost_in"]) for f in sel), "of": len(sel)*5}
res["features"] = feat
OUT.write_text(json.dumps(res, indent=1, default=str)+"\n")
for sec in "ACD":
    print("==", sec); print(json.dumps({k: v for k, v in res[sec].items() if k not in ("lost_items",)}, indent=0)[:6000])
print("== B"); print(json.dumps({k:v for k,v in res["B"].items() if k!="detail"}, indent=0))
print("== E", len(res["E"])); print("== F", {k: v[:6] for k, v in res["F"].items()})
