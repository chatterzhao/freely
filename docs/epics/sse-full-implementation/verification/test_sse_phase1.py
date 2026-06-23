"""Phase 1 SSE client unit tests. Run: python3 test_sse_phase1.py"""
import json, os, sys, threading, time, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..',
    'docs', 'system', 'workspace', 'scripts', 'runtime'))
from a2a_task import SSEPool

class TestSSEPool(unittest.TestCase):
    def test_add_remove(self):
        pool = SSEPool("/tmp/test", max_connections=3)
        self.assertEqual(0, pool.active_count())
        self.assertTrue(pool.add("task-1"))
        self.assertEqual(1, pool.active_count())
        self.assertTrue(pool.add("task-1"))  # Already in pool, no error
        self.assertTrue(pool.add("task-2"))
        self.assertTrue(pool.add("task-3"))
        self.assertFalse(pool.add("task-4"))  # At max
        pool.remove("task-2")
        self.assertEqual(2, pool.active_count())
        self.assertTrue(pool.add("task-4"))   # Now room
        pool.close_all()
        self.assertEqual(0, pool.active_count())

    def test_concurrent_adds(self):
        pool = SSEPool("/tmp/test", max_connections=3)
        errors = []
        def add_task(tid):
            try:
                pool.add(tid)
            except Exception as e:
                errors.append(str(e))
        threads = [threading.Thread(target=add_task, args=(f"t-{i}",)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertLessEqual(pool.active_count(), 3)
        self.assertEqual(0, len(errors))

    def test_heartbeat_and_stale(self):
        pool = SSEPool("/tmp/test", max_connections=5)
        pool.add("task-1")
        pool.add("task-2")
        pool.heartbeat("task-1")
        # task-1 has heartbeat, task-2 has none
        # With large timeout, only task-2 (no heartbeat) is stale
        stale = pool.stale_ids(timeout_seconds=999)
        self.assertIn("task-2", stale)
        self.assertNotIn("task-1", stale)

    def test_list_active(self):
        pool = SSEPool("/tmp/test", max_connections=5)
        pool.add("a")
        pool.add("b")
        active = pool.list_active()
        self.assertEqual(2, len(active))
        self.assertIn("a", active)
        self.assertIn("b", active)

class TestSSEEventParsing(unittest.TestCase):
    def test_parse_valid_event(self):
        from a2a_task import _client
        c = _client()
        ev = c._parse_sse_event("TaskStatusUpdateEvent",
            '{"state":"completed","task_id":"x"}', "ev-001")
        self.assertEqual("TaskStatusUpdateEvent", ev["event_type"])
        self.assertEqual("completed", ev["state"])
        self.assertEqual("x", ev["task_id"])
        self.assertEqual("ev-001", ev["id"])

    def test_parse_malformed_data(self):
        from a2a_task import _client
        c = _client()
        ev = c._parse_sse_event("update", "not-json", "")
        self.assertEqual("update", ev["event_type"])
        self.assertEqual("not-json", ev["raw_data"])

if __name__ == "__main__":
    unittest.main()
