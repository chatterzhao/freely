#!/usr/bin/env python3
"""AT-001 — raw-20261124T054217Z / #4671.

`issue-sync update` must aggregate both platform write results and exit
non-zero when any platform fails. Partial success must never be reported as
overall success.

Contracts (static, no platform writes):
1. cmd-update checks _gh_update's return value (not silently ignored).
2. Gitee failure is not swallowed by a bare `|| echo ...` that returns 0.
3. An overall summary and a non-zero exit path exist.

Run:
  RED   : python3 test-issue-sync-write-result.py --source-dir <develop>
  GREEN : python3 test-issue-sync-write-result.py
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
ROOT = Path(os.environ.get("ISSUE_SYNC_WRITE_RESULT_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        ROOT = Path(sys.argv[_i + 1]).resolve()

CMD_UPDATE = ROOT / "bin/issue-sync.d/cmd-update.sh"
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
    src = read(CMD_UPDATE)
    check(bool(src), "cmd-update.sh exists")
    check(
        not re.search(r'^\s*_gh_update\b[^\n]*$', src, re.M) or
        bool(re.search(r'_gh_update[^\n]*(\|\||&&|\bif\b|\breturn\b)', src)),
        "GitHub update return value is checked",
    )
    check(
        not re.search(r'_gitee_update[^\n]*>/dev/null\s*\|\|\s*echo[^\n]*FAILED', src),
        "Gitee failure is not swallowed by bare `|| echo FAILED`",
    )
    check(
        bool(re.search(r'overall\s*=|partial_failure|write_result|result:', src)),
        "per-platform result summary exists",
    )
    check(
        bool(re.search(r'return 1|exit 1|write_failed', src)),
        "non-zero exit path on failure exists",
    )
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
