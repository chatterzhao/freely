#!/usr/bin/env python3
"""AT-001 — raw-20261103T132622Z / #4155.

Two consequences of "pid file + timestamps + check-then-act" are covered here:

1. Project start lock TOCTOU. `mkdir` then `state.env` then a waiter that reads
   `state_file_missing` and `rm -rf`s the directory: both starters then believe
   they own the lock. Fixed by requiring `age >= stale_secs` before reclaiming,
   plus a cmdline check so a recycled PID does not hold the lock forever.

2. DB daemon double instance. Two concurrent starts both unlinked the socket and
   both bound it, so an orphan daemon could take the whole project's DB offline.
   Fixed by taking an exclusive flock on the pid file before forking, probing for
   a live daemon before bind, and only cleaning up files we own.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (old behaviour -> FAIL)
  GREEN : --source-dir <this worktree>
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("CONCURRENCY_SOURCE_ROOT", str(PROJECT))).resolve()

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


# ── static wiring ─────────────────────────────────────────────────────────

def static_checks(src: Path) -> None:
    print("=== STATIC: primitives are wired in ===")
    freestyle = (src / "docs/system/workspace/scripts/runtime/freely").read_text(errors="replace")
    dbm = (src / "docs/system/workspace/scripts/runtime/freely_db_manager.py").read_text(errors="replace")

    # The reclaim branch must consult the directory age before deleting.
    marker = 'CURRENT_PROJECT_START_LOCK_DETAIL:-unknown}" == "state_file_missing"'
    idx = freestyle.find(marker)
    window = freestyle[idx:idx + 2500] if idx >= 0 else ""
    expect(idx >= 0 and "lock_age_secs" in window and "stale_secs" in window,
           "state_file_missing reclaim is gated on lock dir age vs stale_secs")
    expect("project_start_lock_pid_belongs_to_project_for_runtime" in freestyle,
           "lock owner is validated by cmdline (PID reuse)")

    expect("fcntl.flock" in dbm, "db daemon takes an flock singleton lock")
    expect("_existing_daemon_alive" in dbm,
           "db daemon probes for a live daemon before bind")
    expect("recorded_owner" in dbm,
           "db daemon cleanup only removes files it owns")


# ── behavior: start lock ──────────────────────────────────────────────────

LOCK_SCRIPT = r"""
set +u +e
source "$FREELY_PATH"
set +u +e
acquire_project_start_lock_or_wait "$PROJ" freely_start
rc=$?
echo "RC=$rc"
echo "LOCK_EXISTS=$([[ -d "$PROJ/.freely/run/project-start.lock" ]] && echo 1 || echo 0)"
echo "LOCK_STATE=${CURRENT_PROJECT_START_LOCK_STATE:-unknown}"
echo "LOCK_DETAIL=${CURRENT_PROJECT_START_LOCK_DETAIL:-unknown}"
"""


def _run_lock(src: Path, proj: Path, wait_secs: int = 1) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.update(
        FREELY_PATH=str(src / "docs/system/workspace/scripts/runtime/freely"),
        PROJ=str(proj),
        FREELY_PROJECT_START_LOCK_WAIT_SECS=str(wait_secs),
        FREELY_PROJECT_START_LOCK_STALE_SECS="90",
        FREELY_PROJECT_START_LOCK_WAIT_INTERVAL_SECS="1",
    )
    return subprocess.run([ "bash", "-c", LOCK_SCRIPT], env=env,
                          capture_output=True, text=True, timeout=120)


def _lock_dir(proj: Path) -> Path:
    return proj / ".freely" / "run" / "project-start.lock"


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def lock_checks(src: Path, tmp_root: Path) -> None:
    print("=== BEHAVIOR: start lock reclaim ===")
    freestyle = src / "docs/system/workspace/scripts/runtime/freely"
    if not freestyle.is_file():
        for label in ("fresh lock dir is not stolen", "aged lock dir is reclaimed",
                      "live owner blocks a second starter", "recycled pid is treated as stale"):
            bad(f"{label} (freely missing)")
        return

    # 1) fresh dir without state.env must NOT be reclaimed (TOCTOU window)
    proj = tmp_root / "fresh"
    (proj / ".freely" / "run").mkdir(parents=True)
    lock = _lock_dir(proj)
    lock.mkdir()
    r = _run_lock(src, proj, wait_secs=2)
    expect("RC=1" in r.stdout and lock.is_dir(),
           f"fresh lock dir is not stolen while its owner writes state.env (rc/marker={r.stdout.strip()[:40]!r})")

    # 2) aged dir without state.env is reclaimed and acquired
    proj = tmp_root / "aged"
    (proj / ".freely" / "run").mkdir(parents=True)
    lock = _lock_dir(proj)
    lock.mkdir()
    old = time.time() - 3600
    os.utime(lock, (old, old))
    r = _run_lock(src, proj, wait_secs=3)
    state = lock / "state.env"
    expect("RC=0" in r.stdout and state.is_file(),
           f"aged lock dir is reclaimed and acquired (rc/marker={r.stdout.strip()[:40]!r})")

    # 3) a live freely process holding the lock blocks the second starter
    proj = tmp_root / "live"
    (proj / ".freely" / "run").mkdir(parents=True)
    lock = _lock_dir(proj)
    lock.mkdir()
    holder = subprocess.Popen(
        ["bash", "-c", f'source "{freestyle}"; sleep 30'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        (lock / "state.env").write_text(
            f'owner_pid="{holder.pid}"\nstarted_at="{_now_iso()}"\nreason="freely_start"\n',
            encoding="utf-8")
        r = _run_lock(src, proj, wait_secs=2)
        expect("RC=1" in r.stdout and lock.is_dir(),
               f"live owner blocks a second starter (rc/marker={r.stdout.strip()[:40]!r})")
    finally:
        holder.kill()
        holder.wait(timeout=10)

    # 4) a recycled pid (alive but not ours) is treated as stale — but only when
    # the command line is readable. Under a sandbox that forbids `ps`, the helper
    # must fall back to the conservative "still ours" answer instead of killing a
    # live lock; both outcomes are correct behaviour, so assert per environment.
    proj = tmp_root / "reused"
    (proj / ".freely" / "run").mkdir(parents=True)
    lock = _lock_dir(proj)
    lock.mkdir()
    try:
        ps_readable = bool(subprocess.run(
            ["ps", "-p", str(os.getpid()), "-o", "command="],
            capture_output=True, text=True).stdout.strip())
    except OSError:
        ps_readable = False  # sandboxed: `ps` itself is forbidden
    foreign = subprocess.Popen(["sleep", "30"])
    try:
        (lock / "state.env").write_text(
            f'owner_pid="{foreign.pid}"\nstarted_at="{_now_iso()}"\nreason="freely_start"\n',
            encoding="utf-8")
        r = _run_lock(src, proj, wait_secs=3)
        if ps_readable:
            expect("RC=0" in r.stdout,
                   f"recycled pid is treated as stale, not active (rc/marker={r.stdout.strip()[:40]!r})")
        else:
            expect("RC=1" in r.stdout and lock.is_dir(),
                   f"unreadable cmdline keeps the live lock instead of misfiring (rc/marker={r.stdout.strip()[:40]!r})")
    finally:
        foreign.kill()
        foreign.wait(timeout=10)


# ── behavior: db daemon singleton ─────────────────────────────────────────

def _db_paths(proj: Path) -> tuple[Path, Path]:
    import hashlib
    h = hashlib.sha256(str(proj).encode()).hexdigest()[:16]
    return Path(f"/tmp/freely-db-{h}.pid"), Path(f"/tmp/freely-db-{h}.sock")


def _socket_answers(path: Path) -> bool:
    if not path.exists():
        return False
    probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    probe.settimeout(2.0)
    try:
        probe.connect(str(path))
        return True
    except OSError:
        return False
    finally:
        probe.close()


def db_checks(src: Path, tmp_root: Path) -> None:
    print("=== BEHAVIOR: db daemon singleton ===")
    runtime_dir = src / "docs/system/workspace/scripts/runtime"
    dbm = runtime_dir / "freely_db_manager.py"
    if not dbm.is_file():
        for label in ("only one daemon survives", "single socket serves the project",
                      "loser reports the singleton lock"):
            bad(f"{label} (freely_db_manager.py missing)")
        return

    proj = tmp_root / "dbproj"
    (proj / ".freely" / "run").mkdir(parents=True)
    pid_file, sock_file = _db_paths(proj)
    for stale in (pid_file, sock_file):
        if stale.exists():
            stale.unlink()

    cmd = [sys.executable, str(dbm), "start", "--project", str(proj), "--foreground"]
    procs = [
        subprocess.Popen(cmd, cwd=str(runtime_dir), stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True)
        for _ in range(2)
    ]
    try:
        time.sleep(3.0)
        alive = [p for p in procs if p.poll() is None]
        exited = [p for p in procs if p.poll() is not None]
        expect(len(alive) == 1,
               f"only one daemon survives a concurrent double start (alive={len(alive)})")
        expect(_socket_answers(sock_file),
               "single socket serves the project after the race")
        loser_out = ""
        for p in exited:
            try:
                loser_out += p.stdout.read() or ""
            except Exception:
                pass
        expect(len(exited) == 1 and "singleton lock held" in loser_out,
               f"loser reports the singleton lock (out={loser_out.strip()[:60]!r})")
        if alive and pid_file.exists():
            recorded = pid_file.read_text().strip()
            expect(recorded == str(alive[0].pid),
                   f"pid file belongs to the surviving daemon ({recorded!r} vs {alive[0].pid})")
    finally:
        for p in procs:
            if p.poll() is None:
                p.terminate()
        for p in procs:
            try:
                p.wait(timeout=15)
            except subprocess.TimeoutExpired:
                p.kill()
        for stale in (pid_file, sock_file):
            if stale.exists():
                stale.unlink()


def main() -> int:
    src = Path(os.environ.get("CONCURRENCY_SOURCE_ROOT", str(SRC))).resolve()
    for arg in sys.argv[1:]:
        if arg.startswith("--source-dir="):
            src = Path(arg.split("=", 1)[1]).resolve()
    if "--source-dir" in sys.argv:
        idx = sys.argv.index("--source-dir")
        if idx + 1 < len(sys.argv):
            src = Path(sys.argv[idx + 1]).resolve()

    static_checks(src)

    tmp_root = Path(tempfile.mkdtemp(prefix="concurrency-"))
    try:
        lock_checks(src, tmp_root)
        db_checks(src, tmp_root)
    finally:
        subprocess.run(["rm", "-rf", str(tmp_root)], check=False)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())
