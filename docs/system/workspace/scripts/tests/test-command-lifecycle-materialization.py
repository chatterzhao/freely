#!/usr/bin/env python3
import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[5]
ADAPTER = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"
CONTRACT = ROOT / "docs/system/workspace/scripts/lifecycle/raw_metadata_contract.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RawIssueMaterializationTests(unittest.TestCase):
    def test_strict_platform_payload_preserves_schema_order(self):
        contract = load(CONTRACT, "raw_metadata_contract")
        adapter = load(ADAPTER, "platform_adapter")
        created_at = "2026-07-21T22:31:56Z"
        payload = contract.new_raw_metadata(
            local_id="raw-20260721T223133Z",
            platform_ids={},
            primary_platform="github",
            created_at=created_at,
            updated_at=created_at,
            author="platform",
            channel="github",
        )
        platform_body = "---\n{}\n---\n\nworkflow_kind: fix\n\n## 问题\n保留平台输入。\n".format(
            yaml.safe_dump(payload, allow_unicode=True, sort_keys=False).strip()
        )
        original = {
            "discover_raw_replicas": adapter.discover_raw_replicas,
            "check_and_claim_assignee": adapter.check_and_claim_assignee,
        }
        adapter.discover_raw_replicas = lambda _: {
            "github": {"status": "ok", "issue_id": "4070", "url": "https://example.test/4070", "title": "[RAW-20260721T223133Z] fix: example", "body": platform_body, "created_at": created_at, "updated_at": "2026-07-21T23:00:00Z", "labels": ["phase/proposed"], "state": "OPEN"}
        }
        adapter.check_and_claim_assignee = lambda *_: (True, "claimed")
        try:
            with tempfile.TemporaryDirectory() as directory:
                result = adapter.pull_raw_issue("20260721T223133Z", Path(directory) / "raw")
                metadata = yaml.safe_load(Path(result["path"]).read_text(encoding="utf-8").split("---", 2)[1])
        finally:
            for name, value in original.items():
                setattr(adapter, name, value)

        self.assertEqual(list(metadata), list(contract.RAW_METADATA_FIELDS))
        self.assertEqual(metadata["platform_ids"]["github"]["issue_id"], "4070")
        self.assertEqual(metadata["phase_state"], "proposed")
        self.assertEqual(metadata["updated_at"], "2026-07-21T23:00:00Z")
        self.assertEqual(metadata["promoted_children"], [])
    def test_github_search_matches_raw_key_case_insensitively(self):
        adapter = load(ADAPTER, "platform_adapter_search_case")
        handler = adapter.GitHubHandler()
        original = adapter.subprocess.run

        def fake_run(args, **kwargs):
            class Result:
                returncode = 0
                stderr = ""
                stdout = ""
            result = Result()
            if args[:3] == ["gh", "repo", "view"]:
                result.stdout = "chatterzhao/freely"
            elif args[:3] == ["gh", "issue", "list"]:
                result.stdout = '[{"number":4074,"title":"[raw-20260725T030511Z] example","url":"https://example.test/4074","body":""}]'
            return result

        adapter.subprocess.run = fake_run
        try:
            found = handler.search_raw_issue("20260725T030511Z")
        finally:
            adapter.subprocess.run = original
        self.assertEqual(found["issue_number"], "4074")
    def test_close_raw_re_resolves_even_complete_cached_ids(self):
        adapter = load(ADAPTER, "platform_adapter_close_resolution")
        original = {
            "configured_platforms": adapter.configured_platforms,
            "_handler_for": adapter._handler_for,
            "close_issue": adapter.close_issue,
        }
        seen = {}

        class Handler:
            def __init__(self, issue_id):
                self.issue_id = issue_id
            def search_raw_issue(self, _):
                return {"matches": [{"issue_number": self.issue_id}]}

        handlers = {"github": Handler("4074"), "gitee": Handler("IK3X79")}
        adapter.configured_platforms = lambda: list(handlers)
        adapter._handler_for = handlers.get
        adapter.close_issue = lambda _, ids: seen.setdefault("ids", ids) or {name: {"status": "closed"} for name in ids}
        try:
            adapter.close_issue_by_raw_key("20260725T030511Z", {
                "github": {"issue_id": "wrong"}, "gitee": {"issue_id": "wrong"},
            })
        finally:
            for name, value in original.items():
                setattr(adapter, name, value)
        self.assertEqual(seen["ids"]["github"]["issue_id"], "4074")
        self.assertEqual(seen["ids"]["gitee"]["issue_id"], "IK3X79")


if __name__ == "__main__":
    unittest.main()
