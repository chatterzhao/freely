"""RED→GREEN tests for agent_working fail-closed, idempotent assign, raw_key canon.

Continuation of raw-20260720T120329Z (follow-up raw-20260720T171146Z).
"""
import os
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNTIME = os.path.join(PROJECT, "docs", "system", "workspace", "scripts", "runtime")
sys.path.insert(0, RUNTIME)


class TestRawKeyCanon(unittest.TestCase):
    def test_canonicalize_variants(self):
        from raw_key_canon import canonicalize_raw_key
        self.assertEqual(canonicalize_raw_key("raw-20260720T171146Z"), "raw-20260720T171146Z")
        self.assertEqual(canonicalize_raw_key("20260720T171146Z"), "raw-20260720T171146Z")
        self.assertEqual(
            canonicalize_raw_key("fix/raw-20260720T171146Z-agent-working-single-truth-followup"),
            "raw-20260720T171146Z",
        )
        self.assertEqual(canonicalize_raw_key("__manager__"), "__manager__")

    def test_canonicalize_empty_raises(self):
        from raw_key_canon import canonicalize_raw_key
        with self.assertRaises(ValueError):
            canonicalize_raw_key("")
        with self.assertRaises(ValueError):
            canonicalize_raw_key(None)


class TestDbRpcFailClosed(unittest.TestCase):
    def test_db_rpc_raises_on_socket_error(self):
        import agent_working as aw
        with mock.patch.object(aw.socket, "socket") as msock:
            inst = mock.MagicMock()
            msock.return_value = inst
            inst.connect.side_effect = FileNotFoundError("no socket")
            with self.assertRaises(aw.AgentWorkingError):
                aw._db_rpc("/tmp/nonexistent-project-xyz", "agent_working.get", {"raw_key": "x"})

    def test_db_rpc_raises_on_jsonrpc_error(self):
        import agent_working as aw
        import json
        with mock.patch.object(aw.socket, "socket") as msock:
            inst = mock.MagicMock()
            msock.return_value = inst
            err_body = (json.dumps({"jsonrpc": "2.0", "id": 1, "error": {"code": -1, "message": "db down"}}) + "\n").encode()
            inst.recv.side_effect = [err_body, b""]
            with self.assertRaises(aw.AgentWorkingError) as cm:
                aw._db_rpc(PROJECT, "agent_working.get", {"raw_key": "x"})
            self.assertIn("db down", str(cm.exception))

    def test_agent_next_free_no_silent_manager_fallback(self):
        """Production helper must not invent manager_01/worker_01 on failure."""
        import agent_working as aw
        with mock.patch.object(aw, "_db_rpc", side_effect=aw.AgentWorkingError("rpc failed")):
            with self.assertRaises(aw.AgentWorkingError):
                aw.agent_next_free(PROJECT, "worker", 10, raw_key="raw-20260720T171146Z")


class TestNextFreeAndAssignIdempotent(unittest.TestCase):
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
        self.rk = f"raw-idem-{int(time.time()*1000)}"
        self.daemon.conn.execute("DELETE FROM agent_working WHERE raw_key LIKE 'raw-idem-%'")
        self.daemon.conn.commit()

    def test_idempotent_same_raw_role_returns_existing(self):
        d = self.daemon.dispatch
        r1 = d("agent_working.next_free_and_assign",
               {"role": "worker", "pool_size": "10", "raw_key": self.rk})
        self.assertTrue(r1.get("assigned"), r1)
        r2 = d("agent_working.next_free_and_assign",
               {"role": "worker", "pool_size": "10", "raw_key": self.rk})
        self.assertTrue(r2.get("assigned"), r2)
        self.assertEqual(r1["agent_id"], r2["agent_id"])
        self.assertTrue(r2.get("idempotent") or r2["agent_id"] == r1["agent_id"])
        # Must not overwrite with a different pending agent
        row = d("agent_working.get", {"raw_key": self.rk})["row"]
        agent_part = row["worker_id"].split(":")[0]
        self.assertEqual(agent_part, r1["agent_id"])

    def test_occupied_parses_bare_and_session(self):
        d = self.daemon.dispatch
        # Seed occupied as bare agent_id (no session)
        self.daemon.conn.execute(
            "INSERT INTO agent_working (raw_key, worker_id, updated_at) VALUES (?,?,datetime('now'))",
            (f"{self.rk}-seed", "worker_01"),
        )
        # And as agent_id:session
        self.daemon.conn.execute(
            "INSERT INTO agent_working (raw_key, worker_id, updated_at) VALUES (?,?,datetime('now'))",
            (f"{self.rk}-seed2", "worker_02:sess-abc"),
        )
        self.daemon.conn.commit()
        r = d("agent_working.next_free_and_assign",
              {"role": "worker", "pool_size": "10", "raw_key": self.rk})
        self.assertTrue(r.get("assigned"), r)
        self.assertNotIn(r["agent_id"], ("worker_01", "worker_02"))

    def test_reviewer_occupied_parses_bare_agent_id(self):
        d = self.daemon.dispatch
        self.daemon.conn.execute(
            "INSERT INTO agent_working (raw_key, reviewer_id, updated_at) VALUES (?,?,datetime('now'))",
            (f"{self.rk}-rseed", "reviewer_01"),
        )
        self.daemon.conn.commit()
        r = d("agent_working.next_free_and_assign",
              {"role": "reviewer", "pool_size": "5", "raw_key": self.rk})
        self.assertTrue(r.get("assigned"), r)
        self.assertNotEqual(r["agent_id"], "reviewer_01")


if __name__ == "__main__":
    unittest.main()
