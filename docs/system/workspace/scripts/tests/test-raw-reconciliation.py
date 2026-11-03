#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
MODULE = ROOT / "docs/system/workspace/scripts/lifecycle/raw_reconciliation.py"


def load():
    spec = importlib.util.spec_from_file_location("raw_reconciliation", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RawReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.subject = load()
        self.record = {
            "raw_key": "raw-20260725T030511Z",
            "title": "feat: reconcile replicas",
            "body": "Required behavior.\n\n### comment-1\naccepted",
            "state": "OPEN",
            "labels": ["phase/proposed"],
        }

    def test_normalizes_case_and_ignores_transport_fields(self):
        second = {**self.record, "raw_key": "RAW-20260725t030511z", "issue_id": "2", "updated_at": "later"}
        receipt = self.subject.reconcile(
            raw_key="20260725T030511Z",
            configured_platforms=["github", "gitee"],
            replicas={"github": self.record, "gitee": second},
        )
        self.assertTrue(receipt["ok"])
        self.assertEqual(receipt["raw_key"], "20260725T030511Z")

    def test_blocks_missing_or_unreachable_configured_replica(self):
        receipt = self.subject.reconcile(
            raw_key="20260725T030511Z",
            configured_platforms=["github", "gitee"],
            replicas={"github": self.record, "gitee": {"status": "error", "error": "timeout"}},
        )
        self.assertFalse(receipt["ok"])
        self.assertEqual(receipt["decision"], "block")
        # Unreadable is not a content fact: it is reported as degraded, and the
        # default receipt still refuses to allow the operation.
        self.assertEqual([item["scope"] for item in receipt["degraded"]], ["gitee"])
        self.assertNotIn("gitee", receipt["observations"])

    def test_blocks_divergent_local_or_platform_content(self):
        changed = {**self.record, "body": "different scope"}
        receipt = self.subject.reconcile(
            raw_key="20260725T030511Z",
            configured_platforms=["github", "gitee"],
            replicas={"github": self.record, "gitee": changed},
            local=self.record,
        )
        self.assertFalse(receipt["ok"])
        self.assertIn("content_diverged", {item["code"] for item in receipt["diagnostics"]})


if __name__ == "__main__":
    unittest.main()
