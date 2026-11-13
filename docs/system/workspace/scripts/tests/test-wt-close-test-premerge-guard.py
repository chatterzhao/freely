#!/usr/bin/env python3
"""AT-001 (raw-20261113T074432Z): retiring a disposable test-pre-merge sandbox.

`wt-close` refused EVERY test-pre-merge-* branch at the protected-branch guard,
even with --force --discard-unmerged and a valid reason. R33.9 fixed branch
resolution (the sandbox branch is now found), but the guard still blocked the
only sanctioned way to retire a leftover test worktree - forcing a manual
`git worktree remove` / `branch -D`, which the goal forbids.

The behavioural check extracts the REAL guard block and _is_protected_branch
helper from the source under test and runs them in a sandbox bash process:
  * main/develop stay refused even with both flags;
  * test-pre-merge stays refused without BOTH flags;
  * test-pre-merge is allowed with --force --discard-unmerged;
  * develop baseline must still refuse it (RED is real).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()
BASE = Path(sys.argv[sys.argv.index("--baseline") + 1]) if "--baseline" in sys.argv else None

WT_CLOSE = SRC / "docs/system/workspace/scripts/worktree/wt-close"

OK = 0
BAD = 0


def ok(label: str) -> None:
    global OK
    OK += 1
    print("  [ok] " + label)


def bad(label: str) -> None:
    global BAD
    BAD += 1
    print("  [FAIL] " + label)


def check(cond: bool, label: str) -> None:
    (ok if cond else bad)(label)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def guard_block(text: str) -> str:
    start = text.find("# ── Guard: protected branch")
    if start < 0:
        return ""
    end = text.find("# ── Resolve worktree path", start)
    if end < 0:
        return ""
    return text[start:end]


def protected_helper(text: str) -> str:
    start = text.find("_is_protected_branch() {")
    if start < 0:
        return ""
    end = text.find("\n}\n", start)
    if end < 0:
        return ""
    return text[start:end + 3]


def run_guard(source: Path, branch: str, force: bool, discard: bool) -> subprocess.CompletedProcess:
    text = read(source)
    helper = protected_helper(text)
    block = guard_block(text)
    if not helper or not block:
        return subprocess.CompletedProcess([], 99, "", "guard/helper not found")
    with tempfile.TemporaryDirectory(prefix="at-guard-") as td:
        script = Path(td) / "probe.sh"
        script.write_text(
            "set -uo pipefail\n"
            + helper + "\n"
            + f"branch='{branch}'\n"
            + f"FORCE={'true' if force else 'false'}\n"
            + f"DISCARD_UNMERGED={'true' if discard else 'false'}\n"
            + block
            + "\necho GUARD_PASSED\n",
            encoding="utf-8",
        )
        return subprocess.run(
            ["bash", str(script)], capture_output=True, text=True, timeout=60
        )


def static_checks() -> None:
    print("=== STATIC: guarded exception for disposable sandboxes ===")
    text = read(WT_CLOSE)
    block = guard_block(text)
    check(bool(block), "S1 guard block found")
    check("test-pre-merge-*" in block and "$FORCE" in block and "$DISCARD_UNMERGED" in block,
          "S2 exception requires both --force and --discard-unmerged on test-pre-merge only")
    check("_is_protected_branch" in block, "S3 still consults the protected-branch helper")
    check("retiring disposable test sandbox" in block, "S4 allowed case is reported explicitly")
    check("main/develop" in text.split("# ── Guard: protected branch")[1][:200],
          "S5 main/develop remain documented as never closable")


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: extracted guard block ===")
    tp = "test-pre-merge-20261112T040108Z-r336-selfproof"

    p = run_guard(WT_CLOSE, tp, True, True)
    check(p.returncode == 0 and "GUARD_PASSED" in p.stdout,
          "B1 test-pre-merge with --force --discard-unmerged passes the guard")
    check("retiring disposable test sandbox" in p.stdout,
          "B2 the exception is announced, not silent")

    for force, discard in ((False, False), (True, False), (False, True)):
        p = run_guard(WT_CLOSE, tp, force, discard)
        check(p.returncode != 0 and "cannot close" in p.stdout + p.stderr,
              f"B3 test-pre-merge refused without both flags (force={force} discard={discard})")

    for branch in ("develop", "main"):
        p = run_guard(WT_CLOSE, branch, True, True)
        check(p.returncode != 0 and "cannot close" in p.stdout + p.stderr,
              f"B4 {branch} stays refused even with both flags")


def baseline_checks() -> None:
    if BASE is None:
        return
    print("=== BASELINE CONTROL: develop guard ===")
    p = run_guard(BASE / "docs/system/workspace/scripts/worktree/wt-close",
                  "test-pre-merge-20261112T040108Z-r336-selfproof", True, True)
    check(p.returncode != 0 and "cannot close" in p.stdout + p.stderr,
          "R1 develop guard really refuses the sandbox (RED is real)")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    static_checks()
    behaviour_checks()
    baseline_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
