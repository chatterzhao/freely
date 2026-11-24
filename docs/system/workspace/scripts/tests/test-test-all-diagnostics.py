#!/usr/bin/env python3
"""AT-001 — raw-20261124T054201Z / #4670.

test-all must preserve diagnostic output for failing tests while keeping the
SUMMARY line format stable for downstream gates.

Contracts:
1. bin/test-all no longer redirects each test's stdout+stderr to /dev/null.
2. A predictable per-test log directory exists and failing output is surfaced.
3. SUMMARY line format is unchanged (downstream gates parse it).

Run:
  RED   : python3 test-test-all-diagnostics.py --source-dir <develop-baseline>
  GREEN : python3 test-test-all-diagnostics.py
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
ROOT = Path(os.environ.get("TEST_ALL_DIAG_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        ROOT = Path(sys.argv[_i + 1]).resolve()

TEST_ALL = ROOT / "bin/test-all"
OK = 0
BAD = 0


def check(cond: bool, label: str) -> None:
    global OK, BAD
    if cond:
        OK += 1
        print(f"  ok   {label}")
    else:
        BAD += 1
        print(f"  FAIL {label}")


def read(p: Path) -> str:
    return p.read_text(errors="replace") if p.is_file() else ""


def main() -> int:
    print(f"source: {ROOT}")
    src = read(TEST_ALL)
    check(bool(src), "bin/test-all exists")
    # 1. no stdout/stderr suppression on the test execution lines
    check(
        not re.search(r'(python3|bash)\s+"?\$path"?\s*>/dev/null\s+2>&1', src),
        "test execution does not discard stdout/stderr to /dev/null",
    )
    # 2. per-test log capture with a predictable directory
    check(
        bool(re.search(r'LOG_DIR|test-all-logs|log_dir|TEST_LOG', src)),
        "per-test log directory is defined",
    )
    check(
        bool(re.search(r'>\s*"\$\{?[^}]*log', src, re.I)) or bool(re.search(r'tee|log_file|\.log', src)),
        "test output is written to a per-test log",
    )
    # 3. failing output surfaced to stdout
    check(
        bool(re.search(r'tail|cat .*log|print.*log|sed.*log', src, re.I)),
        "failing test log is surfaced on failure",
    )
    # 4. SUMMARY format unchanged (downstream dependency)
    check(
        'SUMMARY: $passed ok, $failed failed, known-broken=$known_broken' in src,
        "SUMMARY line format preserved",
    )
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
