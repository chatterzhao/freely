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
    def test_platform_only_resolves_missing_ids_by_raw_key(self):
        adapter = load_adapter()
        handlers = {}
        calls = []

        class Handler:
            def __init__(self, name, issue_id):
                self.name = name
                self.issue_id = issue_id

            def search_raw_issue(self, raw_key):
                calls.append((self.name, raw_key))
                return {
                    "issue_number": self.issue_id,
                    "url": f"https://example.test/{self.issue_id}",
                }

            def close_issue(self, issue_id):
                calls.append((self.name, "close", issue_id))
                return {"status": "closed"}

        handlers.update({
            "github": Handler("github", "4070"),
            "gitee": Handler("gitee", "IK2WN2"),
        })
        adapter.configured_platforms = lambda: ["github", "gitee"]
        adapter._handler_for = handlers.get
        result = adapter.close_issue_by_raw_key(
            "20260721T223133Z",
            {"github": {"issue_id": "4070"}},
        )
        self.assertEqual(calls, [
            ("github", "20260721T223133Z"),
            ("gitee", "20260721T223133Z"),
            ("github", "close", "4070"),
            ("gitee", "close", "IK2WN2"),
        ])
        self.assertEqual(result["gitee"]["status"], "closed")

    def test_raw_key_resolution_fails_closed_when_platform_has_no_unique_match(self):
        adapter = load_adapter()
        adapter.configured_platforms = lambda: ["github", "gitee"]

        class Handler:
            def __init__(self, result):
                self.result = result

            def search_raw_issue(self, _):
                return self.result

        adapter._handler_for = lambda platform: Handler(
            {"issue_number": "4070"} if platform == "github" else None
        )
        result = adapter.close_issue_by_raw_key("20260721T223133Z", {})
        self.assertEqual(result["gitee"]["status"], "error")
        self.assertIn("raw key", result["gitee"]["error"])

    def test_raw_key_resolution_rejects_ambiguous_matches_before_closing(self):
        adapter = load_adapter()
        calls = []

        class Handler:
            def __init__(self, name):
                self.name = name

            def search_raw_issue(self, _):
                if self.name == "gitee":
                    return {"matches": [{"issue_number": "A"}, {"issue_number": "B"}]}
                return {"issue_number": "4070"}

            def close_issue(self, issue_id):
                calls.append((self.name, issue_id))
                return {"status": "closed"}

        handlers = {name: Handler(name) for name in ("github", "gitee")}
        adapter.configured_platforms = lambda: ["github", "gitee"]
        adapter._handler_for = handlers.get
        result = adapter.close_issue_by_raw_key("20260721T223133Z", {})
        self.assertEqual(calls, [])
        self.assertEqual(result["gitee"]["status"], "error")
        self.assertIn("uniquely", result["gitee"]["error"])

    def test_platform_only_uses_raw_key_recovery_without_single_platform_guess(self):
        source = WT_CLOSE.read_text(encoding="utf-8")
        self.assertIn('close-raw "$raw_key" "$platform_ids"', source)
        self.assertIn('Error: platform close failed for $issue_id; cleanup stopped', source)
        self.assertNotIn('platform-adapter.py" close github', source)

    def test_normal_cleanup_stops_after_platform_close_failure(self):
        source = WT_CLOSE.read_text(encoding="utf-8")
        self.assertIn('Error: platform close failed for $_wt_i_absorbed_i; cleanup stopped', source)
        self.assertNotIn('platform close failed for $issue_id, continuing', source)
        self.assertNotIn('platform close failed for $_wt_i_absorbed_i, continuing', source)


if __name__ == "__main__":
    unittest.main()
