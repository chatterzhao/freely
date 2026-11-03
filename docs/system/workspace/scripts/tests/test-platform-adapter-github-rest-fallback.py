#!/usr/bin/env python3
"""Unit test: GitHub open-issue listing falls back to REST when GraphQL 504s."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PA_PATH = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"
_spec = importlib.util.spec_from_file_location("platform_adapter", PA_PATH)
pa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pa)


class FakeResult:
    def __init__(self, returncode, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


PAGES = [
    [
        {"number": 4135, "title": "[RAW-20261103T063348Z] fix: test-gate", "body": "body-a", "state": "open"},
        {"number": 4136, "title": "[RAW-20261103T063354Z] fix: gitee pr close", "body": "body-b", "state": "open"},
    ],
    [
        {"number": 4139, "title": "[RAW-20261103T121047Z] fix: merge guard", "body": "body-c", "state": "open"},
        {"number": 5000, "title": "a pull request", "body": "pr", "state": "open", "pull_request": {"url": "x"}},
    ],
]


class GitHubRestFallbackTests(unittest.TestCase):
    def setUp(self):
        self.handler = pa.GitHubHandler()
        self.handler._repo = lambda: "chatterzhao/freely"
        self.calls = []

    def fake_run(self, cmd, **kwargs):
        self.calls.append(list(cmd))
        if "issue" in cmd and "list" in cmd:
            return FakeResult(1, "", "HTTP 504: 504 Gateway Timeout (https://api.github.com/graphql)")
        if "api" in cmd and "--paginate" in cmd:
            return FakeResult(0, json.dumps(PAGES), "")
        return FakeResult(1, "", "unexpected")

    def test_records_fall_back_to_rest_on_graphql_504(self):
        pa.subprocess.run = self.fake_run
        records = self.handler.list_open_issue_records()
        self.assertEqual(set(records), {"4135", "4136", "4139"})
        self.assertEqual(records["4135"]["title"], "[RAW-20261103T063348Z] fix: test-gate")
        self.assertEqual(records["4136"]["body"], "body-b")
        self.assertTrue(any("api" in c and "--paginate" in c for c in self.calls), self.calls)

    def test_list_open_issues_uses_the_same_fallback(self):
        pa.subprocess.run = self.fake_run
        states = self.handler.list_open_issues()
        self.assertEqual(set(states), {"4135", "4136", "4139"})


if __name__ == "__main__":
    unittest.main()
