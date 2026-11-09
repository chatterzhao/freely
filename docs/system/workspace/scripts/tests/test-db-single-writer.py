#!/usr/bin/env python3
"""AT-001 — raw-20261104T075910Z / #4163.

`freely_db_manager.py` is documented as the single writer, but 20 call sites
opened `.freely/freely.db` directly: some read, some wrote, several created their
own schema. The single-writer invariant was already broken.

This AT pins the boundary and the two failure modes that matter:

- an unregistered writable connection must fail the lint;
- a reader must never observe a half-committed transaction, and two short
  writers must serialize instead of racing.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (no gate, no lint -> FAIL)
  GREEN : --source-dir <this worktree>
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import importlib.util
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
from importlib.machinery import SourceFileLoader
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("DB_WRITER_SOURCE_ROOT", str(PROJECT))).resolve()

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


class _NoCapability:
    """Baseline has no write gate: every behaviour assertion must fail per-line."""

    @staticmethod
    def connect_reader(db_path):
        return sqlite3.connect(str(db_path))

    @staticmethod
    def connect_reader_if_exists(db_path):
        return sqlite3.connect(str(db_path)) if Path(db_path).exists() else None

    @staticmethod
    def connect_writer(db_path):
        return sqlite3.connect(str(db_path))

    @staticmethod
    def write_tx(db_path, fn):
        conn = sqlite3.connect(str(db_path))
        try:
            result = fn(conn)
            conn.commit()
            return result
        finally:
            conn.close()


def load_gate(src: Path):
    path = src / "docs/system/workspace/scripts/runtime/db_write_gate.py"
    spec = importlib.util.spec_from_file_location("db_write_gate_probe", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules["db_write_gate_probe"] = module
    spec.loader.exec_module(module)
    return module


OWNER_FILES = {
    "docs/system/workspace/scripts/runtime/freely_db_manager.py",
    "docs/system/workspace/scripts/runtime/db_write_gate.py",
}


def _unregistered_connections(src: Path) -> list[str]:
    """Re-derive the boundary here so the assertion does not rely on the lint
    script existing (the lint is itself under test)."""
    root = src / "docs/system/workspace/scripts"
    offenders: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix == ".pyc" or ".bak." in path.name:
            continue
        rel = path.relative_to(src).as_posix()
        if "/tests/" in rel:
            continue
        try:
            lines = path.read_text(errors="replace").split("\n")
        except OSError:
            continue
        for i, line in enumerate(lines):
            if "sqlite3.connect" not in line:
                continue
            if rel in OWNER_FILES or "mode=ro" in line:
                continue
            if "db-writer:" in line or (i > 0 and "db-writer:" in lines[i - 1]):
                continue
            offenders.append(f"{rel}:{i + 1}")
    return offenders


def static_checks(src: Path) -> None:
    print("=== STATIC: boundary is declared and enforced ===")
    lint = src / "bin/check-db-writers"
    gate = src / "docs/system/workspace/scripts/runtime/db_write_gate.py"
    contract = (src / "docs/system/workspace/three-loop-capability-lifecycle.md")
    contract_text = contract.read_text(errors="replace") if contract.is_file() else ""

    expect(lint.is_file(), "boundary lint bin/check-db-writers exists")
    gate_text = gate.read_text(errors="replace") if gate.is_file() else ""
    expect(all(name in gate_text for name in ("def connect_reader", "def connect_writer", "def write_tx")),
           "db_write_gate exposes connect_reader / connect_writer / write_tx")
    expect("### State 契约" in contract_text
           and all(store in contract_text for store in ("agent_decisions", "delegation_tasks", "discussion_events")),
           "State contract registers the three auxiliary stores")

    offenders = _unregistered_connections(src)
    expect(not offenders,
           f"no unregistered writable connection remains (found {len(offenders)}: {', '.join(offenders[:3])})")

    if not lint.is_file():
        bad("boundary lint passes on this project (lint missing)")
        return
    result = subprocess.run([sys.executable, str(lint), "--project", str(src)],
                            capture_output=True, text=True, timeout=180)
    expect(result.returncode == 0,
           f"boundary lint passes on this project (rc={result.returncode}: {result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ''})")


def guard_checks(src: Path) -> None:
    """The baseline really did have direct connections — RED is not vacuous."""
    print("=== GUARD: baseline evidence ===")
    root = src / "docs/system/workspace/scripts"
    total = 0
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix == ".pyc":
            continue
        try:
            total += len(re.findall(r"sqlite3\.connect\s*\(", path.read_text(errors="replace")))
        except OSError:
            continue
    expect(total >= 20, f"workspace carries the direct connections this issue is about (found {total})")


def behavior_checks(gate, tmp: Path) -> None:
    print("=== BEHAVIOR: read-only + serialized writers + no half-commit reads ===")

    missing = tmp / "absent.db"
    expect(gate.connect_reader_if_exists(missing) is None,
           "connect_reader_if_exists returns None for an absent database")

    db = tmp / "probe.db"
    writer = gate.connect_writer(db)
    writer.execute("CREATE TABLE c (id INTEGER PRIMARY KEY, v INTEGER)")
    writer.execute("INSERT INTO c (id, v) VALUES (1, 0)")
    writer.commit()
    writer.close()

    reader = gate.connect_reader(db)
    try:
        try:
            reader.execute("INSERT INTO c (id, v) VALUES (2, 0)")
            reader.commit()
            bad("read-only connection refuses writes")
        except sqlite3.Error:
            ok("read-only connection refuses writes")
    finally:
        reader.close()

    # Two short writers bumping the same row must serialize (no lost update).
    def bump(_):
        gate.write_tx(db, lambda conn: conn.execute("UPDATE c SET v = v + 1 WHERE id = 1"))

    threads = [threading.Thread(target=bump, args=(i,)) for i in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)
    check = gate.connect_reader(db)
    try:
        value = check.execute("SELECT v FROM c WHERE id = 1").fetchone()[0]
    finally:
        check.close()
    expect(value == 2, f"two concurrent write_tx calls both land (v={value}, want 2)")

    # A reader must not see the first row of an uncommitted transaction.
    db2 = tmp / "halftx.db"
    w = gate.connect_writer(db2)
    w.execute("CREATE TABLE e (id INTEGER PRIMARY KEY)")
    w.commit()
    w.close()

    started = threading.Event()
    release = threading.Event()

    def half_commit():
        conn = gate.connect_writer(db2)
        try:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute("INSERT INTO e (id) VALUES (1)")
            started.set()
            release.wait(timeout=10)
            conn.execute("INSERT INTO e (id) VALUES (2)")
            conn.commit()
        finally:
            conn.close()

    t = threading.Thread(target=half_commit)
    t.start()
    try:
        started.wait(timeout=10)
        time.sleep(0.2)
        r = gate.connect_reader(db2)
        try:
            seen = r.execute("SELECT COUNT(*) FROM e").fetchone()[0]
        finally:
            r.close()
        expect(seen == 0, f"reader sees no rows from an uncommitted transaction (saw {seen})")
    finally:
        release.set()
        t.join(timeout=30)

    r2 = gate.connect_reader(db2)
    try:
        final = r2.execute("SELECT COUNT(*) FROM e").fetchone()[0]
    finally:
        r2.close()
    expect(final == 2, f"committed rows become visible after commit (saw {final})")


def main() -> int:
    src = SRC
    if "--source-dir" in sys.argv:
        idx = sys.argv.index("--source-dir")
        if idx + 1 < len(sys.argv):
            src = Path(sys.argv[idx + 1]).resolve()

    static_checks(src)
    guard_checks(src)

    try:
        gate = load_gate(src)
        if not hasattr(gate, "write_tx"):
            raise AttributeError("write_tx (write gate missing)")
    except Exception as exc:
        print(f"  [info] write gate unusable ({type(exc).__name__}); running against a no-capability stub")
        gate = _NoCapability()

    tmp = Path(tempfile.mkdtemp(prefix="db-writer-"))
    try:
        behavior_checks(gate, tmp)
    finally:
        subprocess.run(["rm", "-rf", str(tmp)], check=False)

    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())
