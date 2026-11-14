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

    def test_mirrored_comment_starting_with_a_heading_is_not_body_content(self):
        """A mirrored platform comment may itself start with a `##` heading.

        `### comment-platform-N` blocks live inside the local body, so the body
        projection has to drop them entirely. Delimiting a block at "the next
        heading of any level" truncated such a comment to its metadata bullets
        and left its prose in the body, which made a healthy raw look
        `content_diverged` against every platform copy (#4653).
        """
        platform = {
            **self.record,
            "body": "Required behavior.",
            "comments": ["## 方案修正\n\n补充说明。"],
        }
        local = {
            **self.record,
            "body": (
                "Required behavior.\n\n"
                "### comment-platform-1\n"
                "- source: platform\n"
                "- event: mirrored\n\n"
                "## 方案修正\n\n补充说明。\n"
            ),
            "comments": [],
        }
        receipt = self.subject.reconcile(
            raw_key="20260725T030511Z",
            configured_platforms=["github"],
            replicas={"github": platform},
            local=local,
        )
        self.assertTrue(receipt["ok"], receipt.get("diagnostics"))

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
