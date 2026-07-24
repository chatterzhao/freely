#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
WT_CLOSE = ROOT / "docs/system/workspace/scripts/worktree/wt-close"
ADAPTER = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"


def load_adapter():
    spec = importlib.util.spec_from_file_location("platform_adapter_wt_close", ADAPTER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorktreeCloseOwnershipTests(unittest.TestCase):
    def test_cleanup_command_has_no_issue_metadata_writer(self):
        source = WT_CLOSE.read_text(encoding="utf-8")
        forbidden = (
            "_fm_set_str",
            "force_closed_at",
            "force_closed_reason",
            'bin/issue-sync" --project',
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, source)
        self.assertIn("_close_issue_platforms_readonly", source)
        self.assertIn('close-multi "$platform_ids"', source)

    def test_platform_close_targets_every_configured_platform(self):
        adapter = load_adapter()
        calls = []

        class Handler:
            def __init__(self, name):
                self.name = name

            def close_issue(self, issue_id):
                calls.append((self.name, issue_id))
                return {"status": "closed"}

        handlers = {name: Handler(name) for name in ("github", "gitee")}
        adapter.configured_platforms = lambda: ["github", "gitee"]
        adapter._handler_for = handlers.get
        result = adapter.close_issue(
            "raw-example",
            {
                "github": {"issue_id": "4070"},
                "gitee": {"issue_id": "IK2WN2"},
            },
        )
        self.assertEqual(calls, [("github", "4070"), ("gitee", "IK2WN2")])
        self.assertEqual(result["github"]["status"], "closed")
        self.assertEqual(result["gitee"]["status"], "closed")

    def test_missing_configured_platform_id_fails_closed(self):
        adapter = load_adapter()

        calls = []

        class Handler:
            def __init__(self, name):
                self.name = name

            def close_issue(self, issue_id):
                calls.append((self.name, issue_id))
                return {"status": "closed"}

        handlers = {name: Handler(name) for name in ("github", "gitee")}
        adapter.configured_platforms = lambda: ["github", "gitee"]
        adapter._handler_for = handlers.get
        result = adapter.close_issue("raw-example", {"github": {"issue_id": "4070"}})
        self.assertEqual(calls, [("github", "4070")])
        self.assertEqual(result["github"]["status"], "closed")
        self.assertEqual(result["gitee"]["status"], "error")
        self.assertIn("no issue_id", result["gitee"]["error"])
    def test_platform_only_fails_closed_without_complete_local_mapping(self):
        source = WT_CLOSE.read_text(encoding="utf-8")
        self.assertIn('Error: --platform-only requires local metadata for $issue_id', source)
        self.assertIn('Error: platform close failed for $issue_id; cleanup stopped', source)
        self.assertNotIn('searching platform by raw key', source)
        self.assertNotIn('platform-adapter.py" close github', source)

    def test_normal_cleanup_stops_after_platform_close_failure(self):
        source = WT_CLOSE.read_text(encoding="utf-8")
        self.assertIn('Error: platform close failed for $_wt_i_absorbed_i; cleanup stopped', source)
        self.assertNotIn('platform close failed for $issue_id, continuing', source)
        self.assertNotIn('platform close failed for $_wt_i_absorbed_i, continuing', source)


if __name__ == "__main__":
    unittest.main()
