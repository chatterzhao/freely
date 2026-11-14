#!/usr/bin/env python3
"""AT-001 — raw-20261114T101138Z / #4653: dropped closeout.

Design intent (verified against project sources, not guessed):
  * `wt-close --force --discard-unmerged` already skips the dirty/phase/
    platform_state gates and closes+deletes the worktree/branch.  It is the
    natural home of the "dropped" terminal path; we must NOT open a second
    close channel or add a new flag (R33.12 lesson).
  * A dropped raw's research is abandoned and never merged, so the only
    durable audit trail is the platform closing comment.  `wt-close --force`
    must therefore (a) write the business reason + B1 research as a platform
    comment, (b) close the platform issue as `not planned`, and (c) fail
    atomically: a comment failure must not close, a close failure must not
    delete the worktree.
  * After the local doc is deleted, `wt-create` must not re-materialize a
    CLOSED raw (re-open-by-accident). `pull_raw_issue` must fail-closed when
    every configured replica is already CLOSED.

RED  : `close_dropped` absent / wrong close reason / no re-materialization
       guard -> AttributeError or close without --reason.
GREEN: close_dropped comments-then-closes with not-planned; guard blocks
       re-materialization.
"""
from __future__ import annotations

import importlib.util
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PA_PATH = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"
_spec = importlib.util.spec_from_file_location("platform_adapter_dropped", PA_PATH)
pa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pa)


class FakeHandler:
    """Records every platform call so close_dropped's ordering is observable."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.calls: list[tuple] = []
        self.state = "OPEN"
        self.search_result: object = None
        self.comment_status = "created"

    def search_raw_issue(self, raw_key):
        return self.search_result or {
            "matches": [{"issue_number": "99", "title": f"[RAW-{raw_key}] x"}]
        }

    def add_comment(self, issue_number, comment_body):
        self.calls.append(("comment", issue_number, comment_body))
        return {"status": self.comment_status}

    def close_issue(self, issue_number, close_reason="", comment_body=""):
        self.calls.append(("close", issue_number, close_reason, comment_body))
        return {"status": "closed"}

    def get_issue_state(self, issue_number):
        return self.state


def install(gh: FakeHandler, gt: FakeHandler) -> None:
    pa.configured_platforms = lambda: ["github", "gitee"]
    pa._handler_for = lambda p: gh if p == "github" else gt
    pa._handlers = lambda: [gh, gt]


class CloseDroppedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.gh = FakeHandler("github")
        self.gt = FakeHandler("gitee")
        install(self.gh, self.gt)

    def test_comments_before_close(self):
        pa.close_dropped("20261114T101138Z", {}, "reason text")
        order = [c[0] for c in self.gh.calls + self.gt.calls]
        self.assertIn("comment", order)
        self.assertIn("close", order)
        self.assertLess(order.index("comment"), order.index("close"),
                        "comment must precede close")

    def test_github_close_uses_not_planned(self):
        pa.close_dropped("20261114T101138Z", {}, "reason text")
        close_calls = [c for c in self.gh.calls if c[0] == "close"]
        self.assertTrue(close_calls, "github close called")
        self.assertEqual(close_calls[0][2], "not planned",
                         "github closed with state reason not planned")

    def test_gitee_close_receives_comment_body(self):
        pa.close_dropped("20261114T101138Z", {}, "the closing note")
        close_calls = [c for c in self.gt.calls if c[0] == "close"]
        self.assertTrue(close_calls)
        self.assertEqual(close_calls[0][3], "the closing note",
                         "gitee close receives the comment body")

    def test_comment_failure_blocks_close(self):
        self.gt.comment_status = "error"
        pa.close_dropped("20261114T101138Z", {}, "reason text")
        self.assertNotIn("close", [c[0] for c in self.gh.calls],
                         "no platform closed when a comment fails")
        self.assertNotIn("close", [c[0] for c in self.gt.calls])


class HandlerSignatureTests(unittest.TestCase):
    def _capture(self, *call_args):
        captured = {}

        def fake_run(args, **kw):
            captured["args"] = list(args)
            class R:
                returncode = 0
                stderr = ""
                stdout = ""
            return R()

        orig = subprocess.run
        subprocess.run = fake_run
        try:
            pa.GitHubHandler.__new__(pa.GitHubHandler).close_issue(*call_args)
        finally:
            subprocess.run = orig
        return captured.get("args", [])

    def test_github_close_without_reason(self):
        args = self._capture("123")
        self.assertNotIn("--reason", args,
                         "github close without reason omits --reason")

    def test_github_close_with_reason(self):
        args = self._capture("123", "not planned")
        self.assertIn("--reason", args)
        self.assertEqual(args[args.index("--reason") + 1], "not planned")


class RematerializationGuardTests(unittest.TestCase):
    def test_all_closed_blocks_pull(self):
        pa.discover_raw_replicas = lambda key: {
            "github": {"status": "ok", "issue_id": "1", "state": "CLOSED"},
            "gitee": {"status": "ok", "issue_id": "2", "state": "CLOSED"},
        }
        out = pa.pull_raw_issue("20261114T101138Z", Path("/tmp/nonexistent-target"))
        self.assertIsNone(out, "pull must fail-closed when every replica is CLOSED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
