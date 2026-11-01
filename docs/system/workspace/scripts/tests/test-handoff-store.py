#!/usr/bin/env python3
"""RED tests for handoff ownership (C-B)."""
import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[5]
MOD = ROOT / "docs/system/workspace/scripts/runtime/handoff_store.py"


def load():
    if not MOD.exists():
        raise AssertionError(f"missing module: {MOD}")
    spec = importlib.util.spec_from_file_location("handoff_store", MOD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class HandoffStoreTest(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.tmp = tempfile.TemporaryDirectory()
        self.store = self.m.HandoffStore(pathlib.Path(self.tmp.name) / "handoff.db")

    def tearDown(self):
        self.tmp.cleanup()

    def test_owner_lifecycle(self):
        t = self.store.create("T1", "github:o/r#1")
        self.assertEqual(t["owner"], "manager")
        self.store.assign("T1", "worker-1", lease=10)
        self.assertEqual(self.store.followup("T1", now=5)["owner"], "worker-1")
        self.store.complete("T1")
        self.assertEqual(self.store.followup("T1", now=5)["owner"], "worker-1")
        self.assertEqual(self.store.followup("T1", now=20)["owner"], "manager")

    def test_handback_once(self):
        self.store.create("T1", "github:o/r#1")
        self.store.assign("T1", "worker-1")
        self.assertEqual(self.store.handback("T1", "T2")["action"], "handback_once")
        self.assertEqual(self.store.handback("T1", "T2")["action"], "duplicate_handback_rejected")

    def test_terminal_stop(self):
        self.store.create("T1", "github:o/r#1")
        self.store.assign("T1", "worker-1")
        self.assertEqual(self.store.stop("T1")["owner"], "human")
        self.assertEqual(self.store.state("T1"), "canceled")

    def test_worker_death(self):
        self.store.create("T1", "github:o/r#1")
        self.store.assign("T1", "worker-1")
        self.assertEqual(self.store.worker_died("T1")["task_state"], "working")

    def test_reviewer_three_rounds(self):
        self.store.create("T1", "github:o/r#1")
        self.assertEqual(self.store.reviewer_fail("T1", 2)["action"], "changes_requested")
        self.assertEqual(self.store.reviewer_fail("T1", 3)["action"], "handback_manager")


if __name__ == "__main__":
    unittest.main()
