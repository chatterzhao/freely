#!/usr/bin/env python3
"""AT-001 — raw-20261103T132605Z / #4153.

`runtime/freely` is both an executable and a library sourced by 4 control-plane
scripts. It carried top-level `set -euo pipefail` and two top-level `exit 1`s, so
sourcing it changed the caller's shell options and a single missing library file
killed the caller (watchdog / dispatcher / promotion gate / supervisor) — which
the supervisor then reported as "watchdog won't start" and stopped the daemon.

This AT pins the source-safety contract:

1. no `exit N` in the library-load section;
2. sourcing does not alter the caller's shell options;
3. a missing library returns a code + FREELY_LIB_LOAD_ERROR instead of killing
   the caller;
4. direct execution still exits 1 (unchanged);
5. library functions return codes instead of exiting (`stop_project_runtime`).

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (top-level exit -> FAIL)
  GREEN : --source-dir <this worktree>
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("SOURCE_SAFE_ROOT", str(PROJECT))).resolve()

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


def static_checks(src: Path) -> None:
    print("=== STATIC: no exit in the load section, library returns codes ===")
    freely = src / "docs/system/workspace/scripts/runtime/freely"
    if not freely.is_file():
        for label in ("load section has no top-level exit",
                      "stop_project_runtime returns instead of exiting"):
            bad(f"{label} (freely missing)")
        return
    lines = freely.read_text(errors="replace").split("\n")
    head = lines[:70]
    exits = [(i + 1, line.strip()) for i, line in enumerate(head)
             if re.match(r"^\s*exit [0-9]", line)]
    expect(not exits, f"load section (first 70 lines) has no top-level exit (found {exits[:3]})")

    text = "\n".join(lines)
    stop_returns = 'acquire_project_start_lock_or_wait "$project" "freely_stop" || return 1' in text
    stop_exits = 'acquire_project_start_lock_or_wait "$project" "freely_stop" || exit 1' in text
    expect(stop_returns and not stop_exits,
           "stop_project_runtime returns a code instead of exiting")


def _mk_sandbox(src: Path, tmp: Path, drop_lib: bool) -> Path:
    """Copy `freely` into a 5-level tree so SELF_ROOT resolves to `tmp`."""
    freely = src / "docs/system/workspace/scripts/runtime/freely"
    nest = tmp / "a" / "b" / "c" / "d" / "e"
    nest.mkdir(parents=True)
    target = nest / "freely"
    shutil.copy(freely, target)
    if not drop_lib:
        # Provide the two libraries so the happy path can be exercised.
        for rel in (
            "docs/system/workspace/skills/freely-watchdog-control-plane/scripts/availability-watchdog.sh",
            "docs/system/workspace/scripts/runtime/session-evidence-resolver.sh",
        ):
            dst = tmp / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src / rel, dst)
    return target


def behavior_checks(src: Path, tmp: Path) -> None:
    print("=== BEHAVIOR: sourcing is safe ===")
    freely = src / "docs/system/workspace/scripts/runtime/freely"
    if not freely.is_file():
        for label in ("source succeeds on the happy path", "sourcing keeps caller shell options",
                      "missing library does not kill the caller", "direct execution still exits 1"):
            bad(f"{label} (freely missing)")
        return

    happy = _mk_sandbox(src, tmp / "happy", drop_lib=False)
    r = subprocess.run(
        ["bash", "-c", f'source "{happy}"; echo "MARKER err=${{FREELY_LIB_LOAD_ERROR:-none}}"'],
        capture_output=True, text=True, timeout=120)
    expect("MARKER err=none" in r.stdout,
           f"source succeeds on the happy path (out={r.stdout.strip()[:60]!r})")

    r2 = subprocess.run(
        ["bash", "-c",
         f'set +e; before="$(set +o)"; source "{happy}"; after="$(set +o)"; '
         '[ "$before" = "$after" ] && echo OPTIONS_UNCHANGED || echo OPTIONS_CHANGED'],
        capture_output=True, text=True, timeout=120)
    expect("OPTIONS_UNCHANGED" in r2.stdout,
           f"sourcing keeps the caller's shell options (out={r2.stdout.strip()[:60]!r})")

    broken = _mk_sandbox(src, tmp / "broken", drop_lib=True)
    r3 = subprocess.run(
        ["bash", "-c",
         f'source "{broken}"; rc=$?; echo "SURVIVED rc=$rc err=${{FREELY_LIB_LOAD_ERROR:-none}}"'],
        capture_output=True, text=True, timeout=120)
    survived = "SURVIVED" in r3.stdout
    got_rc = re.search(r"rc=(\d+)", r3.stdout)
    has_error = "missing watchdog availability module" in r3.stdout
    expect(survived and got_rc and got_rc.group(1) != "0" and has_error,
           f"missing library returns a code and keeps the caller alive (out={r3.stdout.strip()[:70]!r})")

    r4 = subprocess.run(["bash", str(broken)], capture_output=True, text=True, timeout=120)
    expect(r4.returncode == 1,
           f"direct execution still exits 1 when a library is missing (rc={r4.returncode})")


def main() -> int:
    src = SRC
    if "--source-dir" in sys.argv:
        idx = sys.argv.index("--source-dir")
        if idx + 1 < len(sys.argv):
            src = Path(sys.argv[idx + 1]).resolve()

    static_checks(src)
    tmp = Path(tempfile.mkdtemp(prefix="source-safe-"))
    try:
        behavior_checks(src, tmp)
    finally:
        subprocess.run(["rm", "-rf", str(tmp)], check=False)

    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())
