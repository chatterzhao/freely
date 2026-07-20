"""E2E: Real DB daemon — Manager→Worker→Reviewer→close full cycle.

Tests the complete agent_working lifecycle with a real freely-db daemon.
Covers defect #10: existing tests are mock-only, no real DB daemon verification.

Requires: freely_db_manager.py daemon running or startable.
"""
import json, os, sys, time, unittest

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT, "docs", "system", "workspace", "scripts", "runtime"))

class TestE2ERealDBDaemon(unittest.TestCase):
    """Real DB daemon end-to-end: agent_working full lifecycle."""

    @classmethod
    def setUpClass(cls):
        from freely_db_manager import DbDaemon
        cls.daemon = DbDaemon(PROJECT)
        cls.daemon._open_db()
        cls.daemon._ensure_tables()
        cls.daemon.running = True

    @classmethod
    def tearDownClass(cls):
        cls.daemon.conn.close()

    def setUp(self):
        self.raw_key = f"e2e-test-{int(time.time())}"
        self.daemon.conn.execute("DELETE FROM agent_working WHERE raw_key LIKE 'e2e-test-%'")
        self.daemon.conn.execute("DELETE FROM reviews WHERE raw_key LIKE 'e2e-test-%'")
        self.daemon.conn.commit()

    # ── D13a: Full Manager→Worker→Reviewer→close cycle ──

    def _dispatch(self, method, params):
        """Call DB daemon dispatch directly (bypasses socket for testing)."""
        return self.daemon.dispatch(method, params)

    def test_full_trirole_cycle(self):
        """Complete Manager→Worker→Reviewer→close with real DB."""
        rk = self.raw_key
        d = self._dispatch

        # 1. Manager: assign worker (atomic next_free_and_assign)
        r = d("agent_working.next_free_and_assign",
              {"role": "worker", "pool_size": "10", "raw_key": rk})
        self.assertTrue(r.get("assigned"), f"Should assign worker: {r}")
        wid = r["agent_id"]
        self.assertTrue(wid.startswith("worker_"), f"Expected worker_NN, got {wid}")

        d("agent_working.upsert",
           {"raw_key": rk, "col": "worker_id", "val": f"{wid}:sess-wrk-001",
            "worktree": "/tmp/test-wt", "slot": "claude-apikey-default",
            "role": "worker", "agent_id": wid})

        row = d("agent_working.get", {"raw_key": rk})
        self.assertIn(wid, row.get("row", {}).get("worker_id", ""))

        # 2. Reviewer: record review verdict (uses C-A's record_review RPC)
        r = d("agent_working.record_review",
              {"raw_key": rk, "review_stage": "b1", "verdict": "PASS",
               "reviewed_by": "reviewer_07:codex",
               "findings": '[{"item":"code","status":"pass"}]'})
        self.assertEqual(r.get("status"), "ok")

        d("agent_working.record_review",
          {"raw_key": rk, "review_stage": "b2", "verdict": "PASS",
           "reviewed_by": "reviewer_07:codex", "findings": "[]"})

        # 3. Read reviews back
        reviews = d("agent_working.get_reviews", {"raw_key": rk})
        self.assertIn("b1", reviews.get("reviews", {}))
        self.assertEqual(reviews["reviews"]["b1"]["verdict"], "PASS")

        # 4. Release all
        d("agent_working.delete", {"raw_key": rk})

    # ── D13b: Atomic assignment — no duplicates ──

    def test_atomic_assignment_no_duplicates(self):
        """next_free_and_assign should never return the same agent twice."""
        d = self._dispatch
        rk1, rk2 = f"{self.raw_key}-a", f"{self.raw_key}-b"
        w1 = d("agent_working.next_free_and_assign",
               {"role": "worker", "pool_size": "10", "raw_key": rk1})
        w2 = d("agent_working.next_free_and_assign",
               {"role": "worker", "pool_size": "10", "raw_key": rk2})
        self.assertTrue(w1.get("assigned"))
        self.assertTrue(w2.get("assigned"))
        self.assertNotEqual(w1["agent_id"], w2["agent_id"],
                           "Atomic assignment must not duplicate agents")
        self.daemon.conn.execute("DELETE FROM agent_working WHERE raw_key IN (?,?)", (rk1, rk2))
        self.daemon.conn.commit()

    def test_review_persistence_across_restart(self):
        """Review records persist independently of agent_working lifecycle."""
        d = self._dispatch
        rk = self.raw_key
        d("agent_working.record_review",
          {"raw_key": rk, "review_stage": "red", "verdict": "FAIL",
           "reviewed_by": "reviewer_03:codex",
           "findings": '[{"item":"test","status":"fail"}]'})
        self.daemon.conn.close()
        self.daemon._open_db()
        reviews = d("agent_working.get_reviews", {"raw_key": rk})
        self.assertEqual(reviews["reviews"]["red"]["verdict"], "FAIL")

    def test_review_upsert_overwrites(self):
        """Re-recording a review stage should overwrite, not duplicate."""
        d = self._dispatch
        rk = self.raw_key
        d("agent_working.record_review",
          {"raw_key": rk, "review_stage": "dev", "verdict": "FAIL",
           "reviewed_by": "rv:codex", "findings": "[]"})
        d("agent_working.record_review",
          {"raw_key": rk, "review_stage": "dev", "verdict": "PASS",
           "reviewed_by": "rv:codex", "findings": "[]"})
        reviews = d("agent_working.get_reviews", {"raw_key": rk})
        self.assertEqual(len(reviews.get("reviews", {})), 1)
        self.assertEqual(reviews["reviews"]["dev"]["verdict"], "PASS")


if __name__ == "__main__":
    unittest.main()
