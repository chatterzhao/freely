#!/usr/bin/env python3
"""Unit test: Gitee raw-issue search must paginate beyond the first page."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PA_PATH = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"
_spec = importlib.util.spec_from_file_location("platform_adapter", PA_PATH)
pa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pa)

TARGET_KEY = "20260715T131531Z"


class FakeResult:
    def __init__(self, payload):
        self.returncode = 0
        self.stdout = json.dumps(payload)
        self.stderr = ""


def page_issues(page, per_page, total, target_title):
    issues = []
    start = (page - 1) * per_page
    for idx in range(start, min(start + per_page, total)):
        if idx == total - 1:  # target lives on a later page
            issues.append({"number": "IK1ATI", "title": target_title,
                           "html_url": "https://gitee.com/zhaoquan/freely/issues/IK1ATI"})
        else:
            issues.append({"number": f"IK{idx:05d}", "title": f"unrelated issue {idx}",
                           "html_url": ""})
    return issues


class GiteeSearchPaginationTests(unittest.TestCase):
    def setUp(self):
        self.handler = pa.GiteeHandler()
        self.handler._repo = lambda: "zhaoquan/freely"
        self.per_page_seen = []

    def _run(self, *args):
        state = "all"
        per_page = 50
        page = 1
        for i, arg in enumerate(args):
            if arg == "--per-page" and i + 1 < len(args):
                per_page = int(args[i + 1])
            if arg == "--page" and i + 1 < len(args):
                page = int(args[i + 1])
        self.per_page_seen.append((page, per_page))
        issues = page_issues(page, per_page, 130, f"[RAW-{TARGET_KEY}] fix: target")
        return FakeResult(issues)

    def test_search_finds_issue_on_later_page(self):
        self.handler._run = self._run
        found = self.handler.search_raw_issue(TARGET_KEY)
        matches = (found or {}).get("matches") or []
        self.assertEqual(len(matches), 1, f"expected one match, got {matches}")
        self.assertEqual(matches[0]["issue_number"], "IK1ATI")
        self.assertTrue(len(self.per_page_seen) >= 2, f"expected pagination, saw {self.per_page_seen}")


if __name__ == "__main__":
    unittest.main()
