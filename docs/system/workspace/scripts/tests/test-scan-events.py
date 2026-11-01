#!/usr/bin/env python3
"""RED tests for scan event summary (C-F integration)."""
import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[5]
MOD = ROOT / "docs/system/workspace/scripts/runtime/discussion_events.py"


def load():
    if not MOD.exists():
        raise AssertionError(f"missing module: {MOD}")
    spec = importlib.util.spec_from_file_location("discussion_events", MOD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ScanEventsTest(unittest.TestCase):
    def test_summary_has_unread_and_sources(self):
        m = load()
        with tempfile.TemporaryDirectory() as tmp:
            store = m.EventStore(pathlib.Path(tmp) / "events.db")
            store.ingest([m.normalize("issue_comment", {"id": "c1", "issue_number": 1, "author": {"login": "a"}, "body": "b", "created_at": "2026-01-01T00:00:00Z"}, repo="o/r")])
            summary = store.summary()
            self.assertEqual(summary["unread"], 1)
            self.assertIn("issue_comment", summary["by_source"])
            self.assertEqual(len(summary["latest"]), 1)


if __name__ == "__main__":
    unittest.main()
