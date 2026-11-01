#!/usr/bin/env python3
"""RED E2E: real issue comment -> event store -> task -> owner."""
import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[5]
EVENTS = ROOT / "docs/system/workspace/scripts/runtime/discussion_events.py"
HANDOFF = ROOT / "docs/system/workspace/scripts/runtime/handoff_store.py"


def load(name, path):
    if not path.exists():
        raise AssertionError(f"missing module: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class HandoffE2ETest(unittest.TestCase):
    def test_real_issue_comment_to_owner(self):
        ev = load("discussion_events", EVENTS)
        hs = load("handoff_store", HANDOFF)
        with tempfile.TemporaryDirectory() as tmp:
            events = ev.EventStore(pathlib.Path(tmp) / "events.db")
            store = hs.HandoffStore(pathlib.Path(tmp) / "handoff.db")
            for cid in ("IC_kwDOSIGLwc8AAAABLGREcA", "IC_kwDOSIGLwc8AAAABLGcLBQ"):
                raw = {"id": cid, "issue_number": 4070, "author": {"login": "chatterzhao"}, "body": "b", "created_at": "2026-07-21T22:35:54Z"}
                events.ingest([ev.normalize("issue_comment", raw, repo="chatterzhao/freely")])
            self.assertEqual(events.count(), 2)
            task = store.create("T-4070", "github:chatterzhao/freely#4070")
            store.assign("T-4070", "worker-4070")
            self.assertEqual(store.followup("T-4070", now=5)["owner"], "worker-4070")
            self.assertEqual(len(store.messages("T-4070")), 0)


if __name__ == "__main__":
    unittest.main()
