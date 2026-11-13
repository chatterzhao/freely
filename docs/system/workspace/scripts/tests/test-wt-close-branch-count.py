#!/usr/bin/env python3
"""AT-001 (raw-20261113T084813Z): wt-close must resolve branches without a
broken count, and must NOT resolve test-pre-merge sandboxes as close targets
(those are retired by the companion-only path).

Bug: `_resolve_branch_from_raw_key` used

    _count=$(printf '%s\n' "$match_list" | grep -c . 2>/dev/null || echo 0)

`grep -c` prints "0" AND exits 1 on no match, so `|| echo 0` appended a second
"0". `_count` became "0\n0"; `[[ "$_count" -eq 0 ]]` raised a bash syntax
error and the function returned success with NO output. wt-close then printed
"no fix/feature branch found" and did nothing - exit 0, no diagnostics about
the syntax error - so a leftover test-pre-merge worktree could never be retired.

The behavioural check extracts the REAL resolver function from the source tree
under test and runs it in a sandbox git repo with stub branches. Baseline
(develop) must show the syntax error; fixed code must resolve cleanly.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

WT_CLOSE = SRC / "docs/system/workspace/scripts/worktree/wt-close"
KEY = "20261112T131130Z"

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


def resolver(text: str) -> str:
    start = text.find("_resolve_branch_from_raw_key() {")
    if start < 0:
        return ""
    end = text.find("\n}\n", start)
    if end < 0:
        return ""
    return text[start:end + 3]


def sandbox(root: Path, branches: list[str]) -> None:
    subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(root), "-c", "user.name=at", "-c", "user.email=at@local",
         "commit", "--allow-empty", "-q", "-m", "init"],
        check=True, capture_output=True,
    )
    for name in branches:
        subprocess.run(["git", "-C", str(root), "branch", name], check=True, capture_output=True)


def run_resolver(source: Path, branches: list[str]) -> subprocess.CompletedProcess:
    fn = resolver(read(source))
    if not fn:
        return subprocess.CompletedProcess([], 99, "", "resolver not found")
    with tempfile.TemporaryDirectory(prefix="at-count-") as td:
        root = Path(td) / "repo"
        sandbox(root, branches)
        script = root / "probe.sh"
        script.write_text(
            "set -uo pipefail\n" + fn + "\n_resolve_branch_from_raw_key '" + KEY + "'\n",
            encoding="utf-8",
        )
        return subprocess.run(
            ["bash", str(script)], cwd=str(root), capture_output=True, text=True, timeout=60
        )


def static_checks() -> None:
    print("=== STATIC: count guard without sandbox resolution ===")
    text = read(WT_CLOSE)
    fn = resolver(text)
    check(bool(fn), "S1 resolver function found")
    check("grep -c . 2>/dev/null || echo 0" not in fn,
          "S2 no grep -c + echo 0 double-write remains")
    check("grep -c . 2>/dev/null || true" in fn,
          "S3 count capture tolerates grep's exit 1 without appending")
    check("^[0-9]+$" in fn, "S4 count is validated as a single number")
    check("test-pre-merge-${raw_key}-*" not in fn
          and "_wt_retire_orphan_test_sandbox() {" in text,
          "S5 sandbox retirement lives in the companion-only path, not the resolver")
    check("return 1" in fn, "S6 an unparsable count fails loudly")


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: real resolver in a sandbox repo ===")
    fix = "fix/raw-" + KEY + "-slug"
    tp = "test-pre-merge-" + KEY + "-slug"

    p = run_resolver(WT_CLOSE, [])
    check(p.returncode == 0 and p.stdout.strip() == "",
          "B1 no matching branch returns empty with rc=0")
    check("syntax error in expression" not in (p.stdout + p.stderr),
          "B2 no bash syntax error leaks into the result")

    p = run_resolver(WT_CLOSE, [fix])
    check(p.returncode == 0 and p.stdout.strip() == fix,
          "B3 a single fix branch is still resolved")

    p = run_resolver(WT_CLOSE, [tp])
    check(p.returncode == 0 and p.stdout.strip() == "",
          "B4 a test-pre-merge sandbox is NOT resolved into a close target")

    other = "fix/raw-" + KEY + "-abcd"
    p = run_resolver(WT_CLOSE, [fix, other])
    check(p.returncode != 0 and "DENIED ambiguous" in (p.stdout + p.stderr),
          "B5 ambiguous matches still fail closed")


def baseline_checks() -> None:
    print("=== BASELINE CONTROL: develop resolver ===")
    base = Path(sys.argv[sys.argv.index("--baseline") + 1]) if "--baseline" in sys.argv else None
    if base is None:
        return
    tp = "test-pre-merge-" + KEY + "-slug"
    p = run_resolver(base / "docs/system/workspace/scripts/worktree/wt-close", [tp])
    check(p.returncode == 0 and p.stdout.strip() == tp,
          "R1 develop resolver really did resolve a sandbox into a close target (RED is real)")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    static_checks()
    behaviour_checks()
    baseline_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
