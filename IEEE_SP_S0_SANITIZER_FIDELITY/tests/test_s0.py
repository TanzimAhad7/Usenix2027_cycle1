"""CPU tests for S0 V2 (no GPU, no network, no paid API). Inputs: $S0_TEST_INPUTS or ../inputs."""
import json
import math
import os
import shutil
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import prompts  # noqa: E402
import retention  # noqa: E402
import run_s0  # noqa: E402
import s0_core as core  # noqa: E402

INPUTS = Path(os.environ.get("S0_TEST_INPUTS", HERE / "inputs"))


def load():
    return core.load_inputs(INPUTS)


class Confirmed:
    """Temporarily confirm the frozen published block (tests only; the real file is never written)."""
    def __enter__(self):
        self.d = tempfile.mkdtemp()
        f = Path(self.d) / "c.json"
        f.write_text(json.dumps({"confirmed": True, "sha256": prompts.file_sha(prompts.PUBLISHED_FILE)}))
        self.p = mock.patch.object(prompts, "CONFIRMATION_FILE", f)
        self.p.start()

    def __exit__(self, *a):
        self.p.stop()
        shutil.rmtree(self.d)


class TestPrompts(unittest.TestCase):
    def test_published_block_matches_paper_layout(self):
        """Amendment A2: same words as the archived text; typographic quotes; the paper's PDF line structure."""
        pub, arc = prompts.published_block(), prompts.archived_block()
        self.assertEqual(pub.replace("’", "'").split(), arc.split())   # identical words, in order
        self.assertEqual(pub.count("'"), 0)
        self.assertEqual(pub.count("’"), 3)
        self.assertEqual(prompts.file_sha(prompts.PUBLISHED_FILE),
                         "c4e083e39ebba65aa60ded262ca3f2ba3680e744572c2319a9fe1cc994f40a49")
        lines = pub.split("\n")
        self.assertEqual(len(lines), 12)
        self.assertTrue(lines[0].endswith("examine,") and lines[1].endswith("malicious"))
        self.assertTrue(lines[3].startswith("The **original user request** was:  ’"))
        for s in ("sanitizer.  Your", "was:  ", "tool:  **", "request.  Return", "text.  Do"):
            self.assertIn(s, pub)
        self.assertNotIn("\n\n", pub)

    def test_y_insertion_after_request_line(self):
        y = prompts.with_y(prompts.published_block()).split("\n")
        self.assertTrue(y[3].startswith("The **original user request** was:"))
        self.assertEqual(y[4], "The agent proposed this action:  **{proposed_action}**")
        self.assertEqual(prompts.with_y(prompts.archived_block()).count("The agent proposed this action"), 1)

    def test_confirmation_required(self):
        with mock.patch.object(prompts, "CONFIRMATION_FILE", Path(tempfile.mkdtemp()) / "absent.json"):
            with self.assertRaises(SystemExit):
                prompts.messages("published", "system+closing", False, "u", "t", "c")

    def test_arrangements_and_y(self):
        with Confirmed():
            m = prompts.messages("published", "system+closing", True, "REQ", "tool_x", "CONTENT", '{"a":1}')
        self.assertEqual([x["role"] for x in m], ["system", "user"])
        self.assertIn("CONTENT", m[0]["content"])
        self.assertIn('The agent proposed this action:  **{"a":1}**', m[0]["content"])
        self.assertTrue(m[1]["content"].startswith("Return") and m[1]["content"] in prompts.published_block())
        g = prompts.messages("archived", "user", False, "REQ", "tool_x", "CONTENT")
        self.assertEqual(g, [{"role": "user", "content": prompts.gate2_fill(None, "REQ", "tool_x", "CONTENT")}])

    def test_braces_in_content(self):
        with Confirmed():
            m = prompts.messages("published", "system+closing", False, "R", "t", "x {weird} {user_request} y")
        self.assertIn("x {weird} {user_request} y", m[0]["content"])


class TestStatistics(unittest.TestCase):
    def test_operating_characteristics(self):
        self.assertAlmostEqual(core.operating_characteristics(0.20)["ADVANCE"], 0.9190, places=3)
        self.assertAlmostEqual(core.operating_characteristics(0.02)["ADVANCE"], 0.0172, places=3)
        self.assertAlmostEqual(core.operating_characteristics(0.20)["DEPRIORITIZE"], 0.0128, places=3)
        self.assertAlmostEqual(core.cp_upper(0, 29), 0.098, places=3)
        self.assertAlmostEqual(core.cp_upper(1, 29), 0.153, places=3)

    def test_band(self):
        self.assertEqual(core.band({"banking": 0, "slack": 3, "workspace": 0}), "INCONCLUSIVE")
        self.assertEqual(core.band({"banking": 1, "slack": 2, "workspace": 0}), "ADVANCE")
        self.assertEqual(core.band({"banking": 1, "slack": 0, "workspace": 0}), "DEPRIORITIZE")
        self.assertEqual(core.band({"banking": 1, "slack": 1, "workspace": 0}), "INCONCLUSIVE")


class TestRequests(unittest.TestCase):
    def test_every_config_item_builds(self):
        nat, ctl = load()
        self.assertEqual(sum(t["in_population"] for t in nat["tasks"]), 29)
        self.assertEqual(len(nat["items"]), 45)
        self.assertEqual(len(ctl["positive_control_items"]), 24)
        with Confirmed():
            for c in core.CONFIGS:
                for it in core.items_for(c, nat, ctl):
                    m = core.request_messages(c, it)
                    self.assertIn(it["untrusted_content"], m[0]["content"], (c, it["item_id"]))
                    if core.CONFIGS[c]["y"]:
                        self.assertIn("The agent proposed this action", m[0]["content"])

    def test_proposed_action_consumes_carried_value(self):
        nat, ctl = load()
        for it in nat["items"] + ctl["positive_control_items"]:
            y = core.proposed_action(it)
            self.assertIsNotNone(y, it["item_id"])
            self.assertTrue(any(str(cv["value"]) in y for cv in it["carried_values"]), it["item_id"])


class FakeBackend:
    """Deterministic CPU stand-in: 'pids' are code points; generation returns the untrusted content (identity) or
    the content with the carried values removed for items in `delete`."""
    profile = "qwen"
    identity = {"hub": "fake/model", "revision": "0" * 40}

    def __init__(self, items, delete=()):
        self.by_id = {it["item_id"]: it for it in items}
        self.delete = set(delete)
        self.calls = 0

    def render(self, messages):
        return [ord(ch) for ch in "\n".join(m["content"] for m in messages)]

    def count(self, text):
        return math.ceil(len(text) / 4)

    def decode(self, pids):
        return "".join(chr(p) for p in pids)

    def generate(self, requests):
        self.calls += len(requests)
        out = []
        for r in requests:
            it = self.by_id[r["item_id"]]
            text = it["untrusted_content"]
            if it["item_id"] in self.delete:
                for cv in it["carried_values"]:
                    for f in sorted({cv["forms"]["exact"][0], *cv["forms"]["equivalent"]}, key=len, reverse=True):
                        text = text.replace(f, "")
            out.append({"id": r["id"], "text": text, "generated": [1, 2], "limit_reached": False})
        return out


class TestPipelineFake(unittest.TestCase):
    def run_all(self, delete):
        nat, ctl = load()
        run = Path(tempfile.mkdtemp())
        with Confirmed():
            for c in ("Q0",):
                items = core.items_for(c, nat, ctl)
                be = FakeBackend(items, delete)
                run_s0.run_config(be, run, c, items)
                n = be.calls
                run_s0.run_config(be, run, c, items)   # resume: nothing regenerated
                self.assertEqual(be.calls, n)
        outs = run_s0.collect([run])
        rows = core.score_outputs("Q0", core.items_for("Q0", nat, ctl), outs["Q0"])
        shutil.rmtree(run)
        return nat, rows

    def test_identity_deprioritize(self):
        nat, rows = self.run_all(())
        lt, ps = core.task_losses(rows, nat, "auto")
        self.assertEqual(len(lt), 0)
        self.assertEqual(core.band(ps), "DEPRIORITIZE")
        self.assertTrue(all(r["E4"] for r in rows if r["set"] == "pc"))

    def test_deletion_advance(self):
        nat, _ = load()
        # one item per task for 3 tasks in 2 suites, deleting ALL carrying items of those tasks
        pop = [t for t in nat["tasks"] if t["in_population"]]
        chosen = [t for t in pop if t["suite"] == "banking"][:2] + [t for t in pop if t["suite"] == "slack"][:1]
        delete = {i for t in chosen for i in t["source_items"]}   # every carrying item of 3 tasks in 2 suites
        nat, rows = self.run_all(delete)
        lt, ps = core.task_losses(rows, nat, "auto")
        self.assertEqual(len(lt), 3)
        self.assertEqual(core.band(ps), "ADVANCE")


class TestContinuityFake(unittest.TestCase):
    def test_gate_pass_and_fail(self):
        nat, ctl = load()
        rec = {}
        lines = (run_s0.GATE2_RUNS / "20261111T185944Z_gate2_all_both_qwen" / "model_qwen" / "requests.jsonl"
                 ).read_text().splitlines()
        for m in ctl["replay"]["qwen"]["requests"]:
            r = json.loads(lines[m["line"] - 1])
            rec[r["id"]] = r

        class Replay:
            profile, identity = "qwen", {}

            def __init__(self, corrupt=None):
                self.corrupt = corrupt

            def generate(self, requests):
                out = []
                for q in requests:
                    r = rec[q["id"]]
                    text = r["text"] if q["id"] != self.corrupt else ""
                    out.append({"id": q["id"], "text": text, "generated": r["generated"], "limit_reached": False})
                return out
        run = Path(tempfile.mkdtemp())
        g = run_s0.continuity_gate(Replay(), run, "qwen", ctl)
        self.assertTrue(g["passed"])
        self.assertEqual(g["c0_tool_compared"], 24)
        shutil.rmtree(run)
        lost = ctl["replay"]["qwen"]["c0_tool_request"]["banking.0.0"]
        run = Path(tempfile.mkdtemp())
        g = run_s0.continuity_gate(Replay(corrupt=lost), run, "qwen", ctl)
        self.assertFalse(g["passed"])
        shutil.rmtree(run)


class TestBudget(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.approval = self.d / "approval.json"
        self.price = {"data": [{"id": run_s0.GEMINI_ID, "pricing": {"prompt": "0.0000003", "completion": "0.0000025"}}]}

    def tearDown(self):
        shutil.rmtree(self.d)

    def args(self, **kw):
        a = dict(run=str(self.d / "run"), budget_usd=1.0, max_calls=5, configs=["F0"], allow_paid_api=True)
        a.update(kw)
        return Namespace(**a)

    def get(self, url, headers=None):
        return 200, (self.price if url.endswith("/models") else {"data": {"limit": None, "usage": 0}})

    def post_ok(self, url, headers, body):
        return 200, {"model": run_s0.GEMINI_ID, "provider": "Google", "usage": {"prompt_tokens": 1000,
                     "completion_tokens": 1000, "cost": 0.0028},
                     "choices": [{"message": {"content": body["messages"][0]["content"][-200:]},
                                  "finish_reason": "stop"}]}

    def run_gemini(self, args, post, items=3):
        nat, ctl = load()
        subset = nat["items"][:items]
        with Confirmed(), mock.patch.object(run_s0, "APPROVAL", self.approval), \
                mock.patch.object(run_s0, "INPUTS", INPUTS), \
                mock.patch.object(run_s0, "check_freeze", lambda: {}), \
                mock.patch.object(core, "items_for", lambda c, n, k: [dict(i, set="natural") for i in subset]):
            run_s0.cmd_gemini(args, post=post, get=self.get, key="test-key")

    def approve(self, **kw):
        a = {"approved": True, "model": run_s0.GEMINI_ID, "max_usd": 1.0, "max_calls": 5, "configs": ["F0", "F1"]}
        a.update(kw)
        self.approval.write_text(json.dumps(a))

    def test_refusals(self):
        with self.assertRaises(SystemExit):
            self.run_gemini(self.args(allow_paid_api=False), self.post_ok)
        with self.assertRaises(SystemExit):                        # no approval file
            self.run_gemini(self.args(), self.post_ok)
        self.approve(max_usd=0.5)
        with self.assertRaises(SystemExit):                        # budget above approval
            self.run_gemini(self.args(budget_usd=1.0), self.post_ok)
        self.approve(configs=["F1"])
        with self.assertRaises(SystemExit):                        # configuration not approved
            self.run_gemini(self.args(), self.post_ok)

    def test_ledger_and_resume(self):
        self.approve()
        self.run_gemini(self.args(), self.post_ok)
        ledger = (self.d / "run" / "gemini" / "spend_ledger.jsonl").read_text().splitlines()
        self.assertEqual(len(ledger), 3)
        self.assertTrue(all(json.loads(x)["charged_usd"] >= 0.0028 for x in ledger))
        calls = []
        self.run_gemini(self.args(), lambda *a: calls.append(1) or self.post_ok(*a))   # resume: no new calls
        self.assertEqual(calls, [])

    def test_budget_stop(self):
        self.approve()
        with self.assertRaises(SystemExit) as cm:
            self.run_gemini(self.args(budget_usd=0.02), self.post_ok)   # first call's upper bound exceeds budget
        self.assertIn("BUDGET_STOP", str(cm.exception))
        self.assertFalse((self.d / "run" / "gemini" / "spend_ledger.jsonl").exists())

    def test_max_calls(self):
        self.approve()
        with self.assertRaises(SystemExit):
            self.run_gemini(self.args(max_calls=2), self.post_ok)
        self.assertEqual(len((self.d / "run" / "gemini" / "spend_ledger.jsonl").read_text().splitlines()), 2)


class TestAdjudication(unittest.TestCase):
    def test_unique_only_requires_adjudication(self):
        nat, ctl = load()
        it = next(i for i in ctl["positive_control_items"] if i["task"] == "banking.3.0")
        bare = [cv["value"] for cv in it["carried_values"]][0] + ". 64.0."
        rows = retention.score_item(dict(it), bare)
        self.assertTrue(rows[0]["unique_only"] and rows[0]["needs_adjudication"])
        self.assertTrue(rows[0]["E4"] and not rows[0]["E3"])


class TestRender(unittest.TestCase):
    """Real tokenizers (CPU) when available: every planned request contains its untrusted content, and the Gemma-3
    template's silent drop of a system-only message is reproduced (the reason for system+closing)."""

    @classmethod
    def setUpClass(cls):
        try:
            from transformers import AutoTokenizer
        except ImportError:
            raise unittest.SkipTest("transformers not installed in this interpreter")
        cache = "/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache"
        cls.tok = {}
        for label, rev, hub in (("qwen", "9216db5781bf21249d130ec9da846c4624c16137", "Qwen--Qwen3-32B"),
                                ("gemma", "005ad3404e59d6023443cb575daa05336842228a", "google--gemma-3-27b-it")):
            path = Path(cache) / f"models--{hub}" / "snapshots" / rev
            if not path.exists():
                raise unittest.SkipTest(f"{path} missing")
            cls.tok[label] = AutoTokenizer.from_pretrained(str(path), local_files_only=True)

    def render(self, label, msgs):
        kw = {"enable_thinking": False} if label == "qwen" else {}
        return self.tok[label].apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, **kw)

    def test_gemma_drops_system_only(self):
        self.assertNotIn("SYS", self.render("gemma", [{"role": "system", "content": "SYS"}]))

    def test_all_requests_render_with_content_and_fit(self):
        nat, ctl = load()
        with Confirmed():
            for c, cfg in core.CONFIGS.items():
                if cfg["model"] == "gemini":
                    continue
                tok = self.tok[cfg["model"]]
                for it in core.items_for(c, nat, ctl):
                    s = self.render(cfg["model"], core.request_messages(c, it))
                    self.assertIn(it["untrusted_content"], s, (c, it["item_id"]))
                    n = len(tok.encode(s, add_special_tokens=False))
                    lim = core.decode_limit(len(tok.encode(it["untrusted_content"], add_special_tokens=False)))
                    self.assertIsNotNone(lim, (c, it["item_id"]))
                    self.assertLessEqual(n + lim, core.CONTEXT_CAP[cfg["model"]], (c, it["item_id"]))


if __name__ == "__main__":
    unittest.main()


class TestAnalyzeEndToEnd(unittest.TestCase):
    """score -> blinded export -> analyze: a unique-only case keeps the band PENDING until adjudicated."""

    def test_pending_then_adjudicated(self):
        nat, ctl = load()
        run = Path(tempfile.mkdtemp())
        out = Path(tempfile.mkdtemp())
        items = core.items_for("Q0", nat, ctl)
        # Strip only the label of one structured-free value: make banking.user_task_0 bill output keep the IBAN
        # as a bare token (E4 by uniqueness, E3 lost) - the unique-only case.
        target = next(i for i in items if i["item_id"] == "banking.user_task_0.r0")

        class Be(FakeBackend):
            def generate(self, requests):
                res = super().generate(requests)
                for r, o in zip(requests, res):
                    if r["item_id"] == target["item_id"]:
                        o["text"] = "UK12345678901234567890 98.70"
                return res
        # Fake 'tokens' are characters, which would make the 3 largest items too long; real tokenizers fit them
        # (TestRender). Widen the cap for the fake only.
        with Confirmed(), mock.patch.dict(core.CONTEXT_CAP, {"qwen": 10 ** 6}):
            run_s0.run_config(Be(items), run, "Q0", items)
        with mock.patch.object(run_s0, "INPUTS", INPUTS), mock.patch.object(run_s0, "check_freeze", lambda: {}):
            args = Namespace(runs=[str(run)], out=str(out), adjudication=None)
            run_s0.cmd_score(args)
            blind = json.loads((out / "adjudication_blind.json").read_text())
            self.assertTrue(blind and all("config" not in c for c in blind))
            run_s0.cmd_analyze(args)
            a = json.loads((out / "analysis.json").read_text())
            self.assertEqual(a["configs"]["Q0"]["auto"]["k"], 0)
            self.assertEqual(a["configs"]["Q0"]["strict"]["k"], 1)
            # bands agree (both DEPRIORITIZE with k<=1) so no adjudication is needed for the band
            self.assertEqual(a["configs"]["Q0"]["final_band"], "DEPRIORITIZE")
            self.assertGreaterEqual(a["configs"]["Q0"]["unique_only_cases"], 1)
            adj = {c["case"]: {"binding_preserved": False, "identifies_authorized_argument": False} for c in blind}
            (out / "adj.json").write_text(json.dumps(adj))
            run_s0.cmd_analyze(Namespace(runs=[str(run)], out=str(out), adjudication=str(out / "adj.json")))
            a = json.loads((out / "analysis.json").read_text())
            self.assertEqual(a["configs"]["Q0"]["adjudicated"]["k"], 1)
        shutil.rmtree(run)
        shutil.rmtree(out)
