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
            "search_raw_issue": adapter.search_raw_issue,
            "fetch_issue": adapter.fetch_issue,
            "check_and_claim_assignee": adapter.check_and_claim_assignee,
        }
        adapter.search_raw_issue = lambda _: {
            "github": {"issue_number": "4070", "url": "https://example.test/4070"}
        }
        adapter.fetch_issue = lambda *_: {
            "title": "[RAW-20260721T223133Z] fix: example",
            "body": platform_body,
            "created_at": created_at,
            "updated_at": "2026-07-21T23:00:00Z",
            "labels": ["phase/proposed"],
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


if __name__ == "__main__":
    unittest.main()
