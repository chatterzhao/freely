#!/usr/bin/env python3
"""AT-001 — raw-20261124T072402Z / #4675.

The CI merge-guard workflow comment must not claim that pr-merge-guarded sets
the governance check to success. In reality the check stays in_progress by
design so the GitHub UI Merge button remains disabled; merges go through the
local pr-merge-guarded path (git merge + push), which never inspects check
status. A misleading comment previously caused a false P0 and a protection
rollback.

Contracts:
1. workflow comments no longer assert "sets it to success" for pr-merge-guarded.
2. comments state that in_progress is the designed state (UI button disabled).
3. pr-merge-guarded has no call site for _set_governance_check_pass().

Run:
  RED   : python3 test-governance-check-doc-alignment.py --source-dir <develop>
  GREEN : python3 test-governance-check-doc-alignment.py
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
ROOT = Path(os.environ.get("GOV_CHECK_DOC_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        ROOT = Path(sys.argv[_i + 1]).resolve()

WORKFLOW = ROOT / ".github/workflows/pr-merge-guard.yml"
MERGE = ROOT / "docs/system/workspace/scripts/worktree/pr-merge-guarded"
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
    wf = read(WORKFLOW)
    check(bool(wf), "workflow file exists")
    # Only look at the leading comment block (before `name:`).
    header = wf.split("\nname:", 1)[0]
    check(
        not re.search(r"sets it to\s+\"?success\"?", header, re.I),
        "no misleading 'sets it to success' claim in comment",
    )
    check(
        "in_progress" in header and ("designed" in header.lower() or "design" in header.lower()),
        "comment states in_progress is the designed state",
    )
    check(
        "local" in header.lower() and ("pr-merge-guarded" in header),
        "comment points merges to local pr-merge-guarded",
    )
    src = read(MERGE)
    # A call site is the function name followed by '(' but NOT the definition.
    calls = re.findall(r"_set_governance_check_pass\s*\(", src)
    check(len(calls) <= 1 and "_set_governance_check_pass() {" in src,
          "no call site wiring a self-signed success check")
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
