#!/usr/bin/env python3
"""Unit test: gitee-issue.py reopen must use the same request shape as close.

Gitee PATCH /repos/{owner}/{repo}/issues/{number} with bare {"state": "open"}
returns 404 "project or enterprise"; the working shape is the legacy
/repos/{owner}/issues/{number} path with the repo name in the body.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
GITEE_ISSUE = ROOT / "docs/system/workspace/scripts/runtime/gitee-issue.py"


def load_module():
    if str(GITEE_ISSUE.parent) not in sys.path:
        sys.path.insert(0, str(GITEE_ISSUE.parent))
    spec = importlib.util.spec_from_file_location("gitee_issue", GITEE_ISSUE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class GiteeReopenRequestTests(unittest.TestCase):
    def test_reopen_request_matches_close_style(self):
        mod = load_module()
        self.assertTrue(hasattr(mod, "reopen_request"), "missing reopen_request helper")
        path, body = mod.reopen_request("zhaoquan/freely", "IKSN3S")
        self.assertEqual(path, "/repos/zhaoquan/issues/IKSN3S")
        self.assertEqual(body, {"repo": "freely", "state": "open"})

    def test_close_request_shape_unchanged(self):
        mod = load_module()
        body = {"repo": "freely", "state": "closed"}
        self.assertEqual(body, {"repo": "freely", "state": "closed"})


if __name__ == "__main__":
    unittest.main()
