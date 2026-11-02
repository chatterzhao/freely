#!/usr/bin/env python3
"""RED/GREEN contract for replica observation: unknown != missing.

Covers the 2026-11-02 incident where a transient transport failure on one
configured platform was reported as an unavailable *fact* and blocked
`wt-create` even though both replicas existed and agreed.
"""
import importlib.util
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
ADAPTER = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"
RECONCILIATION = ROOT / "docs/system/workspace/scripts/lifecycle/raw_reconciliation.py"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fake_handler_class(adapter):
    class FakeHandler(adapter.PlatformHandler):
        name = "fake"

        def __init__(self, behaviour):
            self.behaviour = list(behaviour)
            self.calls = 0

        def detect(self):
            return True

        def create_issue(self, title, body):
            return {"status": "created"}

        def close_issue(self, issue_id):
            return {"status": "closed"}

        def search_raw_issue(self, raw_key):
            self.calls += 1
            step = self.behaviour[min(self.calls - 1, len(self.behaviour) - 1)]
            if isinstance(step, Exception):
                raise step
            return step

        def fetch_issue(self, issue_id):
            step = self.behaviour[min(self.calls - 1, len(self.behaviour) - 1)]
            if isinstance(step, Exception):
                raise step
            return {"title": "feat: reconcile", "body": "scope", "state": "OPEN"}

    return FakeHandler


FOUND = {
    "issue_number": "42",
    "url": "https://example/42",
    "matches": [{"issue_number": "42", "url": "https://example/42"}],
}


class ObservationTests(unittest.TestCase):
    def setUp(self):
        self.adapter = _load("platform_adapter_under_test", ADAPTER)
        self.adapter._READ_BACKOFF = (0, 0)
        os.environ["FREELY_REPO_PLATFORMS"] = "fake"

    def tearDown(self):
        os.environ.pop("FREELY_REPO_PLATFORMS", None)

    def _install(self, behaviour):
        fake = _fake_handler_class(self.adapter)(behaviour)
        self.adapter._registry[:] = [fake]
        return fake

    def test_transport_failure_is_unknown_not_error(self):
        self._install([RuntimeError("502 proxy")])
        record = self.adapter.discover_raw_replicas("20261102T113816Z")["fake"]
        self.assertEqual(record["status"], "unknown", record)
        self.assertNotEqual(record["status"], "missing")
        self.assertIn("502", record.get("error", ""))

    def test_transport_retry_recovers_without_reporting_degraded(self):
        fake = self._install([RuntimeError("502 proxy"), RuntimeError("502 proxy"), FOUND])
        record = self.adapter.discover_raw_replicas("20261102T113816Z")["fake"]
        self.assertEqual(record["status"], "ok", record)
        self.assertGreaterEqual(fake.calls, 3)

    def test_search_success_with_no_match_is_missing(self):
        self._install([{"matches": []}])
        record = self.adapter.discover_raw_replicas("20261102T113816Z")["fake"]
        self.assertEqual(record["status"], "missing", record)


class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.subject = _load("raw_reconciliation_under_test", RECONCILIATION)
        self.record = {
            "raw_key": "raw-20261102T113816Z",
            "title": "fix: reconcile",
            "body": "scope",
            "state": "OPEN",
        }

    def test_unknown_blocks_by_default(self):
        receipt = self.subject.reconcile(
            raw_key="20261102T113816Z",
            configured_platforms=["github", "gitee"],
            replicas={"github": self.record, "gitee": {"status": "unknown", "error": "502"}},
        )
        self.assertFalse(receipt["ok"])
        self.assertEqual(receipt["decision"], "block")

    def test_unknown_allows_with_debt_when_degraded(self):
        receipt = self.subject.reconcile(
            raw_key="20261102T113816Z",
            configured_platforms=["github", "gitee"],
            replicas={"github": self.record, "gitee": {"status": "unknown", "error": "502"}},
            allow_degraded=True,
        )
        self.assertTrue(receipt["ok"], receipt)
        self.assertEqual(receipt["decision"], "allow_degraded")
        self.assertEqual([item["platform"] for item in receipt["debt"]], ["gitee"])
        self.assertIn("502", receipt["debt"][0]["reason"])

    def test_missing_still_blocks_even_when_degraded(self):
        receipt = self.subject.reconcile(
            raw_key="20261102T113816Z",
            configured_platforms=["github", "gitee"],
            replicas={"github": self.record, "gitee": {"status": "missing", "error": "absent"}},
            allow_degraded=True,
        )
        self.assertFalse(receipt["ok"], receipt)
        self.assertEqual(receipt["decision"], "block")
        self.assertIn("missing", {item["code"] for item in receipt["diagnostics"]})

    def test_divergence_still_blocks_even_when_degraded(self):
        receipt = self.subject.reconcile(
            raw_key="20261102T113816Z",
            configured_platforms=["github", "gitee"],
            replicas={"github": self.record, "gitee": {**self.record, "body": "other"}},
            allow_degraded=True,
        )
        self.assertFalse(receipt["ok"], receipt)
        self.assertIn("content_diverged", {item["code"] for item in receipt["diagnostics"]})

    def test_all_unknown_blocks_even_when_degraded(self):
        receipt = self.subject.reconcile(
            raw_key="20261102T113816Z",
            configured_platforms=["github", "gitee"],
            replicas={
                "github": {"status": "unknown", "error": "502"},
                "gitee": {"status": "unknown", "error": "502"},
            },
            allow_degraded=True,
        )
        self.assertFalse(receipt["ok"], receipt)
        self.assertEqual(receipt["decision"], "block")


if __name__ == "__main__":
    unittest.main()
