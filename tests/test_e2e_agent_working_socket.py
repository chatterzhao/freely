"""Real AF_UNIX socket client/server E2E for agent_working.

Must NOT call daemon.dispatch directly from tests — uses live Unix socket only.
Continuation acceptance for raw-20260720T171146Z / I-20260720T120329Z-C.
"""
import json
import os
import socket
import sys
import tempfile
import threading
import time
import unittest
import unittest.mock

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNTIME = os.path.join(PROJECT, "docs", "system", "workspace", "scripts", "runtime")
sys.path.insert(0, RUNTIME)


class _SocketDaemon:
    """Foreground AF_UNIX JSON-RPC server; SQLite owned by the accept thread."""

    def __init__(self, project_dir: str):
        self.project = project_dir
        self.db_path = os.path.join(project_dir, ".freely", "freely.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.socket_path = os.path.join(project_dir, "test-db.sock")
        self.running = False
        self._thread = None
        self._ready = threading.Event()
        self._error = None
        self.daemon = None

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        if not self._ready.wait(timeout=5):
            raise RuntimeError(f"socket server failed to start: {self._error}")
        if self._error:
            raise RuntimeError(self._error)

    def _run(self):
        try:
            from freely_db_manager import DbDaemon
            self.daemon = DbDaemon(self.project)
            self.daemon.db_path = self.db_path
            self.daemon.socket_path = self.socket_path
            # check_same_thread=False only needed if we ever multi-accept;
            # keep single-thread accept+handle to mirror production.
            self.daemon._open_db()
            self.daemon._ensure_tables()
            self.daemon.running = True

            if os.path.exists(self.socket_path):
                os.unlink(self.socket_path)
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.bind(self.socket_path)
            sock.listen(32)
            sock.settimeout(0.3)
            self._ready.set()
            while self.running:
                try:
                    conn, _ = sock.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break
                try:
                    data = b""
                    conn.settimeout(5)
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                        if b"\n" in data:
                            break
                    if not data:
                        continue
                    req = json.loads(data.decode().strip())
                    try:
                        result = self.daemon.dispatch(req.get("method", ""), req.get("params", {}))
                        resp = {"jsonrpc": "2.0", "id": req.get("id", 0), "result": result}
                    except Exception as e:
                        resp = {
                            "jsonrpc": "2.0",
                            "id": req.get("id", 0),
                            "error": {"code": -32000, "message": str(e)},
                        }
                    conn.sendall((json.dumps(resp, default=str) + "\n").encode())
                finally:
                    try:
                        conn.close()
                    except OSError:
                        pass
            sock.close()
        except Exception as e:
            self._error = e
            self._ready.set()
        finally:
            if self.daemon and self.daemon.conn:
                try:
                    self.daemon.conn.close()
                except Exception:
                    pass
            if os.path.exists(self.socket_path):
                try:
                    os.unlink(self.socket_path)
                except OSError:
                    pass

    def stop(self):
        self.running = False
        if self.daemon:
            self.daemon.running = False
        if self._thread:
            self._thread.join(timeout=3)


class TestE2ESocketAgentWorking(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmpdir = tempfile.mkdtemp(prefix="freely-aw-sock-")
        cls.srv = _SocketDaemon(cls._tmpdir)
        cls.srv.start()
        import agent_working as aw
        cls.aw = aw
        cls._orig_socket_path = aw._socket_path
        sock = cls.srv.socket_path
        aw._socket_path = lambda _project: sock
        cls.project = cls._tmpdir

    @classmethod
    def tearDownClass(cls):
        cls.aw._socket_path = cls._orig_socket_path
        cls.srv.stop()
        import shutil
        shutil.rmtree(cls._tmpdir, ignore_errors=True)

    def setUp(self):
        self.rk = f"raw-20260720T{int(time.time()) % 1000000:06d}Z"
        try:
            self.aw.agent_release_all(self.project, self.rk)
        except Exception:
            pass

    def test_manager_worker_reviewer_close_cycle(self):
        aw = self.aw
        m = aw.agent_next_free_and_assign(self.project, "manager", 1, self.rk)
        self.assertTrue(m.get("assigned"), m)
        mid = m["agent_id"]
        aw.agent_assign(self.project, self.rk, "manager", mid, session_id="sess-m")

        w = aw.agent_next_free_and_assign(self.project, "worker", 10, self.rk)
        self.assertTrue(w.get("assigned"), w)
        wid = w["agent_id"]
        aw.agent_assign(self.project, self.rk, "worker", wid, session_id="sess-w",
                        worktree="/tmp/wt", slot="claude-apikey-default")

        r = aw.agent_next_free_and_assign(self.project, "reviewer", 10, self.rk)
        self.assertTrue(r.get("assigned"), r)
        rid = r["agent_id"]
        aw.agent_assign(self.project, self.rk, "reviewer", rid, session_id="sess-r")

        aw.agent_record_review(self.project, self.rk, "b1", "PASS", f"{rid}:codex", [])
        reviews = aw.agent_get_reviews(self.project, self.rk)
        self.assertEqual(reviews["b1"]["verdict"], "PASS")

        aw.agent_release_all(self.project, self.rk)
        reviews2 = aw.agent_get_reviews(self.project, self.rk)
        self.assertEqual(reviews2["b1"]["verdict"], "PASS")

    def test_concurrent_assign_no_duplicate(self):
        aw = self.aw
        results = []
        errors = []
        lock = threading.Lock()
        stamp = int(time.time() * 1000)

        def _assign(i):
            try:
                # Opaque keys (no shared timestamp) so each request is a distinct raw_key
                rk = f"e2e-conc-{stamp}-{i}"
                r = aw.agent_next_free_and_assign(self.project, "worker", 20, rk)
                with lock:
                    results.append(r.get("agent_id"))
            except Exception as e:
                with lock:
                    errors.append(e)

        threads = [threading.Thread(target=_assign, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=15)
        self.assertEqual(errors, [], f"errors: {errors}")
        self.assertEqual(len(results), 5)
        self.assertEqual(len(set(results)), 5, f"duplicate agents: {results}")

    def test_same_raw_idempotent(self):
        aw = self.aw
        r1 = aw.agent_next_free_and_assign(self.project, "worker", 10, self.rk)
        r2 = aw.agent_next_free_and_assign(self.project, "worker", 10, self.rk)
        self.assertEqual(r1["agent_id"], r2["agent_id"])
        self.assertTrue(r2.get("idempotent") or r1["agent_id"] == r2["agent_id"])

    def test_raw_key_canon_across_ops(self):
        from raw_key_canon import canonicalize_raw_key
        bare = "20260720T123456Z"
        aw = self.aw
        aw.agent_next_free_and_assign(self.project, "worker", 10, bare)
        row = aw.agent_list_by_raw_key(self.project, canonicalize_raw_key(bare))
        self.assertTrue(row.get("worker_id"), row)
        aw.agent_record_review(self.project, f"raw-{bare}", "dev", "PASS", "reviewer_01:x", [])
        reviews = aw.agent_get_reviews(self.project, bare)
        self.assertEqual(reviews["dev"]["verdict"], "PASS")

    def test_db_unavailable_fail_closed(self):
        aw = self.aw
        with unittest.mock.patch.object(aw, "_socket_path", return_value="/tmp/freely-db-DOES-NOT-EXIST.sock"):
            with self.assertRaises(aw.AgentWorkingError):
                aw.agent_next_free_and_assign(self.project, "worker", 10, self.rk)


if __name__ == "__main__":
    unittest.main()
