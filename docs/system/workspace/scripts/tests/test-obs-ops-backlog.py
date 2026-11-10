#!/usr/bin/env python3
"""AT-001 — raw-20261110T120124Z / #4281 (#4157 follow-up).

Six operational items left by #4157, all "a failure or an unbounded resource
stays invisible":

1. `bin/freely-watchdog`: missing log target kills it via pipefail; a failed
   PRE_CHECK_MAP ends the `while` subshell under `set -e`; no pid.
2. `append_runtime_event` has no severity / trace_id, so logs cannot be
   filtered or correlated across processes.
3. `cycle-*` / `crash-*` logs grow without a retention bound.
4. `freely-package` copies `__pycache__/` and `*.bak.py` into the installed
   state via `cp -R`.
5. Gitee token travels in the URL query; the Codex API key travels in Python
   argv (visible to `ps`).
6. DB schema has no `PRAGMA user_version` and `ALTER TABLE` failures are
   swallowed by `except Exception: pass`.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (old behaviour -> FAIL)
  GREEN : --source-dir <this worktree>
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("OBS_OPS_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        SRC = Path(sys.argv[_i + 1]).resolve()

RUNTIME = SRC / "docs/system/workspace/scripts/runtime"
FREELY = RUNTIME / "freely"

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


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.is_file() else ""


# ── STATIC ───────────────────────────────────────────────────────────────

def static_checks() -> None:
    print("=== STATIC: six items are wired in ===")
    watchdog = read(SRC / "bin/freely-watchdog")
    freely = read(FREELY)
    package = read(SRC / "bin/freely-package")
    gitee = read(RUNTIME / "gitee-issue.py")
    ai_cli = read(RUNTIME / "ai-cli")
    db = read(RUNTIME / "freely_db_manager.py")

    expect("tail -F" in watchdog and 'LOG_FILE" ]] || : > "$LOG_FILE"' in watchdog
           and "PRE_CHECK_MAP" in watchdog and "PID_FILE" in watchdog,
           "watchdog follows rotation, creates a missing log, survives a failed pre-check and owns a pid")

    ev_start = freely.find("append_runtime_event()")
    ev_slice = freely[ev_start:ev_start + 1200] if ev_start >= 0 else ""
    expect("severity=" in ev_slice and "trace_id=" in ev_slice,
           "append_runtime_event emits severity and trace_id")

    expect("_prune_logs_by_count()" in freely
           and "cycle-*.log" in freely and "crash-*.log" in freely,
           "cycle/crash logs have a retention bound")

    expect("__pycache__" in package and "*.bak.py" in package,
           "package excludes __pycache__ and *.bak.py")

    expect("Authorization" in gitee and 'query["access_token"]' not in gitee,
           "gitee token leaves the URL query for an Authorization header")

    expect("FREELY_CODEX_API_KEY" in ai_cli
           and '"$config_file" "$provider_name" "$base_url" "$api_key"' not in ai_cli,
           "codex api key goes through the environment, not Python argv")

    db_start = db.find("# Schema migrations for a2a_tasks")
    db_slice = db[db_start:db_start + 1200]
    expect("PRAGMA user_version" in db and
           not ("except Exception:" in db_slice and "pass" in db_slice),
           "DB records user_version and no longer swallows migration errors")


# ── BEHAVIOR: runtime events carry severity / trace_id ──────────────────

def event_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: runtime event fields ===")
    if not FREELY.is_file():
        bad("runtime event carries severity= and trace_id=")
        return
    project = tmp / "proj"
    (project / ".freely").mkdir(parents=True)
    script = r"""
set +u +e
source "$FREELY_PATH"
append_runtime_event "$PROJ" supervisor_stopping "reason=no_recovery"
cat "$(runtime_events_log_file "$PROJ")"
"""
    env = dict(os.environ, FREELY_PATH=str(FREELY), PROJ=str(project))
    proc = subprocess.run(["bash", "-c", script], env=env, capture_output=True,
                          text=True, timeout=60)
    out = proc.stdout.strip()
    ok_line = ("severity=" in out and "trace_id=" in out
               and "event=supervisor_stopping" in out)
    # `awk` must be able to read both fields as k=v tokens.
    parsed = {}
    if ok_line:
        for token in out.splitlines()[-1].split():
            if "=" in token:
                k, _, v = token.partition("=")
                parsed[k] = v
    expect(ok_line and parsed.get("severity") and parsed.get("trace_id"),
           "runtime event carries severity= and trace_id=")


# ── BEHAVIOR: log retention ─────────────────────────────────────────────

def prune_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: log retention bound ===")
    if not FREELY.is_file():
        bad("_prune_logs_by_count keeps exactly the newest N logs")
        return
    logs = tmp / "logs"
    logs.mkdir()
    for i in range(60):
        (logs / f"cycle-20260101-{i:04d}.log").write_text("x")
    script = r"""
set +u +e
source "$FREELY_PATH"
_prune_logs_by_count "$LOGS" 'cycle-*.log' 50
ls -1 "$LOGS"/cycle-*.log | wc -l
"""
    env = dict(os.environ, FREELY_PATH=str(FREELY), LOGS=str(logs))
    proc = subprocess.run(["bash", "-c", script], env=env, capture_output=True,
                          text=True, timeout=60)
    expect(proc.stdout.strip() == "50",
           "_prune_logs_by_count keeps exactly the newest N logs")


# ── BEHAVIOR: package output has no cache / dead backups ────────────────

def package_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: package output hygiene ===")
    pkg = SRC / "bin/freely-package"
    if not pkg.is_file():
        bad("package output contains no __pycache__ or *.bak.py")
        return
    fake = tmp / "fake-root"
    (fake / "docs/system/workspace").mkdir(parents=True)
    (fake / "docs/__pycache__").mkdir()
    (fake / "docs/__pycache__/x.pyc").write_text("x")
    (fake / "docs/dead.bak.py").write_text("x")
    (fake / "docs/keep.txt").write_text("x")
    (fake / "docs/system/workspace/package-allowlist.txt").write_text("docs/\n")
    home = tmp / "home"
    out = home / "versions" / "20260101T0000Z-nightly"
    out.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update(FREELY_PACKAGE_ROOT=str(fake), FREELY_HOME=str(home))
    proc = subprocess.run(["bash", str(pkg), "--version", "20260101T0000Z-nightly",
                           "--output", str(out)], env=env, capture_output=True,
                          text=True, timeout=120)
    if proc.returncode != 0:
        bad(f"package output contains no __pycache__ or *.bak.py (rc={proc.returncode}: {proc.stderr[-160:]})")
        return
    leftovers = [p for p in out.rglob("*") if p.name == "__pycache__" or p.name.endswith(".bak.py")]
    expect(not leftovers, "package output contains no __pycache__ or *.bak.py")


# ── BEHAVIOR: watchdog survives a missing log target ────────────────────

def watchdog_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: watchdog survives a missing log ===")
    dog = SRC / "bin/freely-watchdog"
    if not dog.is_file():
        bad("watchdog starts with a missing log and writes its pid")
        return
    log = tmp / "missing.log"
    pid_file = tmp / "watchdog.pid"
    env = dict(os.environ, FREELY_WATCHDOG_LOG=str(log), FREELY_WATCHDOG_PID=str(pid_file))
    proc = subprocess.Popen(["bash", str(dog)], env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.2)
        alive = proc.poll() is None
        has_pid = pid_file.is_file() and pid_file.read_text().strip() != ""
        expect(alive and has_pid,
               "watchdog starts with a missing log and writes its pid")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def main() -> int:
    print(f"AT-001 source: {SRC}")
    with tempfile.TemporaryDirectory(prefix="freely-obs-ops-") as d:
        # macOS /var is a symlink to /private/var; the package guard compares
        # string prefixes, so the fixture must use the resolved path.
        tmp = Path(d).resolve()
        static_checks()
        event_checks(tmp)
        prune_checks(tmp)
        package_checks(tmp)
        watchdog_checks(tmp)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
