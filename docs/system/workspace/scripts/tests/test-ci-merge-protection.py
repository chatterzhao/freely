#!/usr/bin/env python3
"""AT-001 — raw-20261124T054145Z / #4669.

CI merge protection chain must be fail-closed:
1. `.github/workflows/pr-merge-guard.yml` declares `checks: write`.
2. `pr-merge-guarded._set_governance_check_pass()` never self-creates a
   `conclusion=success` check and never swallows API failures with `|| true`.
3. When the governance check is absent, the helper fails closed (non-zero),
   instead of minting its own success check.

Run:
  RED   : python3 test-ci-merge-protection.py --source-dir <develop-baseline>
  GREEN : python3 test-ci-merge-protection.py
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
ROOT = Path(os.environ.get("CI_MERGE_PROTECTION_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        ROOT = Path(sys.argv[_i + 1]).resolve()

WORKFLOW = ROOT / ".github/workflows/pr-merge-guard.yml"
MERGE_SCRIPT = ROOT / "docs/system/workspace/scripts/worktree/pr-merge-guarded"

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


def static_workflow() -> None:
    print("=== STATIC: workflow permissions ===")
    wf = read(WORKFLOW)
    check(bool(wf), "workflow file exists")
    perm = re.search(r"^permissions:\s*$", wf, re.M)
    check(bool(perm), "workflow declares a top-level permissions: block")
    checks_write = re.search(r"^\s+checks:\s*write\s*$", wf, re.M)
    check(bool(checks_write), "permissions block grants checks: write")
    contents_read = re.search(r"^\s+contents:\s*read\s*$", wf, re.M)
    check(bool(contents_read), "permissions block grants contents: read")


def static_merge_script() -> None:
    print("=== STATIC: pr-merge-guarded fail-closed ===")
    src = read(MERGE_SCRIPT)
    check(bool(src), "pr-merge-guarded implementation exists")
    m = re.search(
        r"_set_governance_check_pass\(\)\s*\{(.*?)\n\}", src, re.S
    )
    fn = m.group(1) if m else ""
    check(bool(fn), "locate _set_governance_check_pass() body")
    # Self-minting a success check is the bypass. It appears as a POST to
    # repos/{owner}/{repo}/check-runs (no -X PATCH) with a success conclusion,
    # typically in the else-branch when no existing check run was found.
    post_create = bool(
        re.search(r'gh api\s+"repos/\{owner\}/\{repo\}/check-runs"', fn)
    )
    success_or_local = bool(
        re.search(r"created locally", fn) or re.search(r'--field conclusion="success"', fn)
    )
    check(not (post_create and success_or_local), "no self-created success check fallback")
    # Swallowing API failures.
    check("|| true" not in fn, "no `|| true` swallowing API failures in check helper")
    # Fail-closed signal: an explicit error return path.
    fail_closed = bool(
        re.search(r"return 1|exit 1|fail \"", fn)
    )
    check(fail_closed, "check helper has an explicit non-zero fail-closed path")


def main() -> int:
    print(f"source: {ROOT}")
    static_workflow()
    static_merge_script()
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
