#!/usr/bin/env python3
"""AT-001 — raw-20261110T064015Z / #4254.

Two real defects, both reproduced against the actual source (not a mock of the
fix):

1. Dispatch is not idempotent. `manager_runtime_launch_workers_after_ai_cycle_if_needed`
   launches a worker and only then updates the A2A task. The three
   `--expected-status` arguments on the handoff updates are silently swallowed by
   `argparse.parse_known_args()` in `a2a_task.py`: the CLI does not register that
   flag, the server PATCH handler has no compare-and-swap, and the DB handler
   updates unconditionally. Two dispatchers can therefore both win the same
   submitted task.

2. SSE watchdog pid files have no mutual exclusion. `launch_sse_watchdog`,
   `cmd_ensure_sse_watchdog_watch` and `cmd_ensure_sse_watchdog` form three
   start paths; the ensure-watch path wraps a self-looping `--watch` consumer in
   another `while true` (the outer loop is dead code) and writes its own `$$`
   into the watchdog pid file. Every pid write is a bare `echo > pid`.

This AT checks the real DB RPC handler on an isolated SQLite database, the real
CLI against a local stub A2A REST server, and the real pid-claim helper under
two concurrent bash processes. It never touches a real platform, a real DB, or
a real running watchdog.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (old behaviour -> FAIL)
  GREEN : --source-dir <this worktree>
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import http.server
import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("DISPATCH_CAS_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        SRC = Path(sys.argv[_i + 1]).resolve()

RUNTIME = SRC / "docs/system/workspace/scripts/runtime"

OK = 0
BAD = 0


def ok(label: str) -> None:
    global OK
    OK += 1
    print(f"  [ok] {label}")


def bad(label: str) -> None:
    global BAD
    BAD += 1
    print(f"  [FAIL] {label}")


def expect(cond: bool, label: str) -> None:
    (ok if cond else bad)(label)


def read(rel: str) -> str:
    p = RUNTIME / rel
    return p.read_text(errors="replace") if p.is_file() else ""


# ── STATIC: every layer of the CAS chain and the singleton owner ──────────

def static_checks() -> None:
    print("=== STATIC: CAS chain + SSE singleton wiring ===")
    cli = read("a2a_task.py")
    srv = read("a2a/a2a_server.py")
    dbm = read("freely_db_manager.py")
    free = read("freely")
    sh = read("sse-watchdog.sh")

    expect('p_update.add_argument("--expected-state"' in cli
           and 'p_update.add_argument("--expected-status"' in cli,
           "CLI registers --expected-state / --expected-status (no parse_known_args swallowing)")

    upd = cli[cli.find('elif args.cmd == "update":'):cli.find('elif args.cmd == "latest-manager":')]
    expect("expected_state" in upd and "state_conflict" in upd and "sys.exit(3)" in upd,
           "CLI forwards expected_state and exits non-zero on state_conflict")

    expect("expected_state" in srv and "status_code=409" in srv
           and "state_conflict" in srv,
           "A2A server PATCH enforces expected_state and returns 409 conflict")

    db_start = dbm.find('@_h("a2a_task.update")')
    db_slice = dbm[db_start:db_start + 1400]
    expect("expected_state" in db_slice and "AND state = ?" in db_slice,
           "DB single-writer handler makes the state transition conditional")

    fn = free.find("manager_runtime_launch_workers_after_ai_cycle_if_needed()")
    loop = free[fn:fn + 12000]
    claim = loop.find('--expected-state "submitted"')
    launch = loop.find('launch_worker_from_manager_prompt_if_needed "$project"')
    expect(claim >= 0 and launch >= 0 and claim < launch,
           "dispatch CAS claims the submitted task BEFORE launching the worker")
    expect('--status "working"' not in loop,
           "post-launch unconditional A2A state update removed")

    ensure = free.find("cmd_ensure_sse_watchdog_watch()")
    ensure_slice = free[ensure:ensure + 1300]
    expect('bash "$_sse_watchdog_sh" --project "$project" --watch' not in ensure_slice
           and 'echo "$$" >"$pid_file"' not in ensure_slice,
           "watch-in-watch dead code and self-pid impersonation removed")
    expect('launch_sse_watchdog "$project"' in ensure_slice,
           "ensure-watch supervises through the single start path")

    expect("sse_watchdog_claim_pid" in sh,
           "shell watchdog claims its pid through the mutual-exclusion helper")
    expect("def sse_watchdog_claim_pid" in free or "sse_watchdog_claim_pid() {" in free,
           "flock-backed pid claim helper exists in runtime/freely")
    py_start = free.find("_start_watchdog_sse_py()")
    expect(py_start >= 0 and "sse_watchdog_claim_pid" in free[py_start:py_start + 1800],
           "python watchdog pid also goes through the claim helper")


# ── BEHAVIOR: real DB RPC handler on an isolated database ────────────────

class _Daemon:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn


def db_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: conditional state transition (isolated SQLite) ===")
    path = RUNTIME / "freely_db_manager.py"
    if not path.is_file():
        for label in ("first CAS wins (affected=1)", "second CAS loses (affected=0)",
                      "plain update still works", "mismatched expected_state refuses"):
            bad(label)
        return
    try:
        # The daemon lazily imports sibling runtime modules; make the source
        # root importable so the real handler can be exercised in isolation.
        if str(RUNTIME) not in sys.path:
            sys.path.insert(0, str(RUNTIME))
        spec = importlib.util.spec_from_file_location("at_dispatch_db_manager", path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        assert spec.loader is not None
        spec.loader.exec_module(mod)
        handler = mod.HANDLERS.get("a2a_task.update")
    except Exception as e:
        for label in ("first CAS wins (affected=1)", "second CAS loses (affected=0)",
                      "plain update still works", "mismatched expected_state refuses"):
            bad(f"{label} (module unavailable: {e})")
        return
    if handler is None:
        for label in ("first CAS wins (affected=1)", "second CAS loses (affected=0)",
                      "plain update still works", "mismatched expected_state refuses"):
            bad(label)
        return

    conn = sqlite3.connect(str(tmp / "a2a-isolated.db"))
    conn.execute("CREATE TABLE a2a_tasks (task_id TEXT PRIMARY KEY, "
                 "state TEXT NOT NULL DEFAULT 'submitted', updated_at TEXT)")
    conn.execute("INSERT INTO a2a_tasks (task_id, state) VALUES ('T1','submitted')")
    conn.commit()
    daemon = _Daemon(conn)

    def state() -> str:
        row = conn.execute("SELECT state FROM a2a_tasks WHERE task_id='T1'").fetchone()
        return row[0] if row else "missing"

    try:
        r1 = handler(daemon, {"task_id": "T1", "state": "working",
                              "expected_state": "submitted"})
    except Exception as e:
        r1 = {"error": str(e)}
    expect(r1.get("affected") == 1 and state() == "working",
           "first CAS wins (affected=1)")

    try:
        r2 = handler(daemon, {"task_id": "T1", "state": "working",
                              "expected_state": "submitted"})
    except Exception as e:
        r2 = {"error": str(e)}
    expect(r2.get("affected") == 0 and state() == "working",
           "second CAS loses (affected=0)")

    try:
        r3 = handler(daemon, {"task_id": "T1", "state": "completed"})
    except Exception as e:
        r3 = {"error": str(e)}
    expect(r3.get("affected") == 1 and state() == "completed",
           "plain update still works")

    try:
        r4 = handler(daemon, {"task_id": "T1", "state": "failed",
                              "expected_state": "submitted"})
    except Exception as e:
        r4 = {"error": str(e)}
    expect(r4.get("affected") == 0 and state() == "completed",
           "mismatched expected_state refuses")
    conn.close()


# ── BEHAVIOR: real CLI against a local stub A2A REST endpoint ─────────────

class _Stub(http.server.BaseHTTPRequestHandler):
    records: list = []
    conflict = False

    def do_PATCH(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode())
        except Exception:
            body = {}
        type(self).records.append(body)
        conflict = type(self).conflict
        payload = ({"error": "state_conflict", "expected_state": "submitted",
                    "current_state": "working", "affected": 0} if conflict
                   else {"id": "T1", "state": "working"})
        data = json.dumps(payload).encode()
        self.send_response(409 if conflict else 200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_args) -> None:
        return


def cli_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: CLI forwards CAS and surfaces conflict ===")
    cli = RUNTIME / "a2a_task.py"
    if not cli.is_file():
        for label in ("legacy --status launched still maps to working",
                      "CLI PATCH body carries expected_state=submitted",
                      "409 conflict makes the CLI fail closed"):
            bad(label)
        return
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Stub)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    project = tmp / "isolated-project"
    project.mkdir(exist_ok=True)
    env = dict(os.environ)
    env["A2A_REMOTE_URL"] = f"http://127.0.0.1:{port}"
    env["SESSION_PARENT_PROJECT"] = str(project)
    cmd = [sys.executable, str(cli), "update", "--task-id", "T1",
           "--status", "launched", "--expected-status", "pending"]
    try:
        _Stub.records = []
        _Stub.conflict = False
        first = subprocess.run(cmd, env=env, cwd=str(project),
                               capture_output=True, text=True, timeout=30)
        body = _Stub.records[-1] if _Stub.records else {}
        expect(body.get("state") == "working",
               "legacy --status launched still maps to working")
        expect(body.get("expected_state") == "submitted",
               "CLI PATCH body carries expected_state=submitted")

        _Stub.conflict = True
        second = subprocess.run(cmd, env=env, cwd=str(project),
                                capture_output=True, text=True, timeout=30)
        expect(second.returncode != 0 and "conflict" in second.stdout,
               "409 conflict makes the CLI fail closed")
    except Exception as e:
        for label in ("legacy --status launched still maps to working",
                      "CLI PATCH body carries expected_state=submitted",
                      "409 conflict makes the CLI fail closed"):
            bad(f"{label} (cli unavailable: {e})")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


# ── BEHAVIOR: two concurrent watchdogs, one owner ─────────────────────────

CLAIM_SCRIPT = r"""
set +u +e
source "$FREELY_PATH"
set +u +e
sse_watchdog_claim_pid "$PIDFILE" "$$" ""
echo "RC=$?"
sleep 2
"""


def pid_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: concurrent pid claims ===")
    free = RUNTIME / "freely"
    pid_file = tmp / "run" / "sse-watchdog.pid"
    if not free.is_file() or "sse_watchdog_claim_pid() {" not in free.read_text(errors="replace"):
        bad("exactly one concurrent claim succeeds")
        bad("pid file records the winning owner only")
        return
    env = dict(os.environ)
    env.update(FREELY_PATH=str(free), PIDFILE=str(pid_file))
    try:
        procs = [subprocess.Popen(["bash", "-c", CLAIM_SCRIPT], env=env,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True) for _ in range(2)]
        outs = []
        for p in procs:
            out, _err = p.communicate(timeout=20)
            outs.append((p.pid, out))
        rcs = [int(line.split("=", 1)[1])
               for _pid, out in outs
               for line in out.splitlines() if line.startswith("RC=")]
        winners = [rc for rc in rcs if rc == 0]
        expect(len(rcs) == 2 and len(winners) == 1,
               "exactly one concurrent claim succeeds")
        winner_pid = next((pid for (pid, out), rc in zip(outs, rcs) if rc == 0), None)
        content = pid_file.read_text().strip() if pid_file.is_file() else ""
        expect(winner_pid is not None and content == str(winner_pid),
               "pid file records the winning owner only")
    except Exception as e:
        bad(f"exactly one concurrent claim succeeds ({e})")
        bad(f"pid file records the winning owner only ({e})")


def main() -> int:
    print(f"AT-001 source: {SRC}")
    with tempfile.TemporaryDirectory(prefix="freely-dispatch-cas-") as d:
        tmp = Path(d)
        static_checks()
        db_checks(tmp)
        cli_checks(tmp)
        pid_checks(tmp)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
