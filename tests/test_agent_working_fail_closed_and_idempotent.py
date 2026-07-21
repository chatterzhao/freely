"""RED→GREEN tests for agent_working fail-closed, idempotent assign, raw_key canon.

Continuation of raw-20260720T120329Z (follow-up raw-20260720T171146Z).
"""
import os
import runpy
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


class TestAcpSessionRegistrationFailClosed(unittest.TestCase):
    def test_force_new_registers_scalar_session_id(self):
        import agent_working as aw

        with mock.patch.object(aw, "_acp_bridge_call", return_value={"sessionId": "sess-123"}), \
             mock.patch.object(aw, "acp_session_register") as register:
            session_id, action = aw.acp_session_connect(
                PROJECT,
                "raw-20260720T171146Z",
                "worker",
                "worker_01",
                "claude-slot-01",
                force_new=True,
            )

        self.assertEqual((session_id, action), ("sess-123", "new"))
        register.assert_called_once_with(
            PROJECT,
            "raw-20260720T171146Z",
            "worker",
            "worker_01",
            "sess-123",
            "claude-slot-01",
        )

    def test_new_without_session_id_fails_closed(self):
        import agent_working as aw

        with mock.patch.object(aw, "_acp_bridge_call", return_value={}), \
             mock.patch.object(aw, "acp_session_register") as register:
            with self.assertRaises(aw.AgentWorkingError):
                aw.acp_session_connect(
                    PROJECT,
                    "raw-20260720T171146Z",
                    "worker",
                    "worker_01",
                    "claude-slot-01",
                    force_new=True,
                )

        register.assert_not_called()

    def test_reviewer_resume_reads_session_for_exact_agent(self):
        import agent_working as aw

        with mock.patch.object(
            aw, "agent_list_by_raw_key",
            return_value={"reviewer_id": "reviewer_01:sess-1,reviewer_02:sess-2"},
        ), mock.patch.object(
            aw, "agent_get_session", return_value="sess-1",
        ) as get_session, mock.patch.object(
            aw, "_acp_bridge_ping", return_value=True,
        ):
            session_id, action = aw.acp_session_connect(
                PROJECT,
                "raw-20260720T171146Z",
                "reviewer",
                "reviewer_01",
                "claude-slot-01",
            )

        self.assertEqual((session_id, action), ("sess-1", "return"))
        get_session.assert_called_once_with(
            PROJECT, "raw-20260720T171146Z", "reviewer", "reviewer_01"
        )


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

    def test_atomic_assignment_stores_bare_reservation(self):
        d = self.daemon.dispatch
        assigned = d("agent_working.next_free_and_assign", {
            "role": "worker", "pool_size": "10", "raw_key": self.rk,
        })
        row = d("agent_working.get", {"raw_key": self.rk})["row"]
        self.assertEqual(row["worker_id"], assigned["agent_id"])
        session = d("agent_working.get_session", {
            "raw_key": self.rk, "role": "worker", "agent_id": assigned["agent_id"],
        })
        self.assertIsNone(session["session_id"])

    def test_release_removes_stale_bare_worker_reservation(self):
        d = self.daemon.dispatch
        assigned = d("agent_working.next_free_and_assign", {
            "role": "worker", "pool_size": "10", "raw_key": self.rk,
        })
        d("agent_working.release", {
            "raw_key": self.rk, "role": "worker", "agent_id": assigned["agent_id"],
        })
        row = d("agent_working.get", {"raw_key": self.rk})["row"]
        self.assertIsNone(row["worker_id"])

    def test_release_preserves_worker_assignment_when_clearing_session(self):
        d = self.daemon.dispatch
        d("agent_working.upsert", {
            "raw_key": self.rk, "col": "worker_id", "val": "worker_01:sess-1",
        })
        d("agent_working.release", {
            "raw_key": self.rk, "role": "worker", "agent_id": "worker_01",
        })
        row = d("agent_working.get", {"raw_key": self.rk})["row"]
        self.assertEqual(row["worker_id"], "worker_01")

    def test_reviewer_upsert_preserves_bare_and_session_entries(self):
        d = self.daemon.dispatch
        self.daemon.conn.execute(
            "INSERT INTO agent_working (raw_key, reviewer_id, updated_at) VALUES (?,?,datetime('now'))",
            (self.rk, "reviewer_01"),
        )
        self.daemon.conn.commit()
        d("agent_working.upsert", {
            "raw_key": self.rk,
            "col": "reviewer_id",
            "val": "reviewer_02:sess-2",
        })
        row = d("agent_working.get", {"raw_key": self.rk})["row"]
        self.assertEqual(row["reviewer_id"], "reviewer_01,reviewer_02:sess-2")
        self.assertIsNone(d("agent_working.get_session", {
            "raw_key": self.rk, "role": "reviewer", "agent_id": "reviewer_01",
        })["session_id"])
        self.assertEqual(d("agent_working.get_session", {
            "raw_key": self.rk, "role": "reviewer", "agent_id": "reviewer_02",
        })["session_id"], "sess-2")

    def test_reviewer_release_removes_bare_entry_only(self):
        d = self.daemon.dispatch
        self.daemon.conn.execute(
            "INSERT INTO agent_working (raw_key, reviewer_id, updated_at) VALUES (?,?,datetime('now'))",
            (self.rk, "reviewer_01,reviewer_02:sess-2"),
        )
        self.daemon.conn.commit()
        d("agent_working.release", {
            "raw_key": self.rk, "role": "reviewer", "agent_id": "reviewer_01",
        })
        row = d("agent_working.get", {"raw_key": self.rk})["row"]
        self.assertEqual(row["reviewer_id"], "reviewer_02:sess-2")


class TestStorageReadSymmetryProductionPaths(unittest.TestCase):
    def test_codec_preserves_session_id_suffix(self):
        from agent_identity_value import parse_agent_entries, session_entry

        value = "reviewer_01:provider:session-1,reviewer_02:session-2"
        self.assertEqual(parse_agent_entries(value)["reviewer_01"], "provider:session-1")
        self.assertEqual(session_entry(value, "reviewer_01"),
                         ("reviewer_01", "provider:session-1"))
        self.assertEqual(session_entry(value),
                         ("reviewer_01", "provider:session-1"))

    @mock.patch("subprocess.run")
    @mock.patch("agent_working._db_rpc")
    def test_liveness_clears_each_reviewer_session_with_valid_upsert(self, rpc, run):
        import watchdog_sse

        rpc.side_effect = [
            {"rows": [{
                "raw_key": "raw-20260720T171146Z",
                "worker_id": "",
                "reviewer_id": "reviewer_01:sess-1,reviewer_02:sess-2",
                "manager_id": "",
            }]},
            {"status": "ok"},
            {"status": "ok"},
        ]
        run.return_value = mock.Mock(returncode=1)

        watchdog_sse._check_agent_liveness(PROJECT)

        self.assertEqual(run.call_count, 2)
        self.assertEqual(
            [call.args[2] for call in rpc.call_args_list[1:]],
            [
                {"raw_key": "raw-20260720T171146Z", "col": "reviewer_id",
                 "val": "reviewer_01"},
                {"raw_key": "raw-20260720T171146Z", "col": "reviewer_id",
                 "val": "reviewer_02"},
            ],
        )

    def test_message_delivery_selects_requested_reviewer_session(self):
        import watchdog_sse

        fake_db = mock.MagicMock()
        fake_db.execute.return_value.fetchone.return_value = (
            "raw-20260720T171146Z", "reviewer_01"
        )
        with mock.patch("sqlite3.connect", return_value=fake_db), \
             mock.patch.object(
                 watchdog_sse, "agent_list_by_raw_key",
                 return_value={
                     "reviewer_id": "reviewer_01:sess-1,reviewer_02:sess-2"
                 },
             ), \
             mock.patch.object(watchdog_sse, "_get_agent_slot",
                               return_value="cline-slot-01"), \
             mock.patch.object(watchdog_sse, "_acp_rpc",
                               return_value={"result": {}}) as acp_rpc:
            watchdog_sse._handle_message_delivery(PROJECT, {
                "task_id": "task-1",
                "role": "reviewer",
                "agent_id": "reviewer_01",
                "content": "review",
            })

        acp_rpc.assert_called_once_with(
            PROJECT,
            "session/prompt",
            {"sessionId": "sess-1", "prompt": "review"},
            base_tool="cline",
        )

    def test_restart_resumes_each_exact_session_and_skips_bare_reservation(self):
        import agent_session_restore as restore

        rows = [{
            "raw_key": "raw-20260720T171146Z",
            "worker_id": "worker_01",
            "reviewer_id": "reviewer_01:sess-1,reviewer_02:provider:sess-2",
            "manager_id": "manager_01:sess-manager",
        }]
        slots = {
            "reviewer_01": "cline-slot-01",
            "reviewer_02": "opencode-slot-02",
            "manager_01": "claude-slot-01",
        }
        with mock.patch.object(
            restore, "_db_rpc", return_value={"rows": rows}
        ), mock.patch.object(restore, "_acp_bridge_call") as bridge_call:
            outcomes = restore.resume_persisted_sessions(
                PROJECT, lambda _project, agent_id: slots.get(agent_id, "")
            )

        self.assertEqual([item["agent_id"] for item in outcomes], [
            "manager_01", "reviewer_01", "reviewer_02",
        ])
        self.assertEqual(
            [call.args[1:4] for call in bridge_call.call_args_list],
            [
                ("claude", "session/resume",
                 {"sessionId": "sess-manager", "cwd": PROJECT}),
                ("cline", "session/resume",
                 {"sessionId": "sess-1", "cwd": PROJECT}),
                ("opencode", "session/resume",
                 {"sessionId": "provider:sess-2", "cwd": PROJECT}),
            ],
        )

    def test_lifecycle_scanner_reads_worker_id_through_codec(self):
        scanner_path = os.path.join(RUNTIME, "task-lifecycle-scan.py")
        scanner = runpy.run_path(scanner_path, run_name="task_lifecycle_scan_test")

        self.assertEqual(
            scanner["_bound_worker_agent_id"]({
                "worker_id": "worker_01:provider:session-1"
            }),
            "worker_01",
        )
        self.assertEqual(
            scanner["_bound_worker_agent_id"]({"worker_id": "worker_02"}),
            "worker_02",
        )

    def test_restore_cli_accepts_project_as_explicit_argument(self):
        import agent_session_restore as restore

        with mock.patch.object(
            restore, "resume_persisted_sessions", return_value=[{"status": "resumed"}]
        ) as resume, mock.patch("builtins.print") as output:
            result = restore.main([PROJECT])

        self.assertEqual(result, 0)
        resume.assert_called_once_with(os.path.abspath(PROJECT))
        self.assertIn('"status": "resumed"', output.call_args.args[0])

    def test_pr_review_guarded_reads_worker_id_through_codec(self):
        script_path = os.path.join(PROJECT, "bin", "pr-review-guarded")
        with open(script_path, encoding="utf-8") as source_file:
            source = source_file.read()

        self.assertEqual(source.count("from agent_identity_value import first_agent_id"), 2)
        self.assertEqual(source.count("first_agent_id(row.get('worker_id', ''))"), 2)
        self.assertNotIn("wid.split(':')", source)

    def test_a2a_restore_invokes_module_file_without_inline_script(self):
        server_path = os.path.join(RUNTIME, "a2a", "a2a_server.py")
        with open(server_path, encoding="utf-8") as source_file:
            source = source_file.read()

        self.assertNotIn("_aw_resume_script", source)
        self.assertNotIn("[_sys.executable, '-c'", source)
        self.assertIn("[_sys.executable, restore_py, str(self.project)]", source)
        self.assertIn('"runtime", "agent_session_restore.py"', source)


if __name__ == "__main__":
    unittest.main()
