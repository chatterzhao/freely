#!/usr/bin/env python3
"""RED tests for discussion event ingestion (C-F)."""
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


class DiscussionEventsTest(unittest.TestCase):
    def test_normalize_six_sources(self):
        m = load()
        cases = [
            ("issue", {"id": "1", "number": 1, "title": "t", "body": "b", "author": {"login": "a"}}),
            ("issue_comment", {"id": "c1", "issue_number": 1, "author": {"login": "a"}, "body": "b", "created_at": "2026-01-01T00:00:00Z"}),
            ("pr_review", {"id": "r1", "pr_number": 2, "author": {"login": "a"}, "state": "APPROVED", "submitted_at": "2026-01-01T00:00:00Z"}),
            ("pr_review_comment", {"id": "rc1", "pr_number": 2, "author": {"login": "a"}, "body": "b", "created_at": "2026-01-01T00:00:00Z"}),
            ("ci", {"id": "j1", "pr_number": 2, "name": "test", "conclusion": "FAILURE"}),
            ("chat", {"id": 7, "chat_type": "issue", "author": "a", "message": "hi", "created_at": "2026-01-01T00:00:00Z"}),
        ]
        for source, raw in cases:
            event = m.normalize(source, raw, repo="o/r")
            self.assertTrue(event["event_id"].startswith(source + ":"))
            self.assertTrue(event["thread_key"])
            self.assertIn("actor", event)
            self.assertIn("created_at", event)

    def test_dedupe_event_id(self):
        m = load()
        with tempfile.TemporaryDirectory() as tmp:
            store = m.EventStore(pathlib.Path(tmp) / "events.db")
            raw = {"id": "c1", "issue_number": 1, "author": {"login": "a"}, "body": "b", "created_at": "2026-01-01T00:00:00Z"}
            event = m.normalize("issue_comment", raw, repo="o/r")
            store.ingest([event])
            store.ingest([event])
            self.assertEqual(store.count(), 1)

    def test_admission_reasons(self):
        m = load()
        base = {"event_id": "issue_comment:c1", "source": "issue_comment", "actor": {"login": "bot", "is_bot": True}, "addressed": False, "strength": "inferred"}
        self.assertEqual(m.admit(base)["disposition"], "observe")
        base2 = dict(base, actor={"login": "a", "is_bot": False}, addressed=True, strength="explicit")
        self.assertEqual(m.admit(base2)["disposition"], "accept")


if __name__ == "__main__":
    unittest.main()
