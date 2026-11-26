#!/usr/bin/env python3
"""AT-001 for raw-20261126T130151Z / #4726.

After pr-merge syncs an issue-sync commit into the test worktree, the
followthrough must call test-evidence.py attest-meta so wt-close sees an
equivalent (not stale) evidence chain.

Usage: python3 ...test-merge-followthrough-evidence.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import tempfile
from pathlib import Path

OK = FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global OK, FAIL
    if cond:
        OK += 1
        print(f"ok   {name}")
    else:
        FAIL += 1
        print(f"FAIL {name}" + (f" — {detail}" if detail else ""))


def extract_helper(source: str) -> str:
    match = re.search(r"^_attest_test_evidence_equivalent\(\) \{.*?^\}", source, re.M | re.S)
    return match.group(0) if match else ""


def run_helper(fixture: Path, helper_src: str, stub_rc: int) -> subprocess.CompletedProcess:
    capture = fixture / "capture.txt"
    script = f"""
set -u
python3() {{ printf '%s\\n' "$*" > "{capture}"; printf '%s\\n' '{{"ok": true, "verdict": "equivalent"}}'; return {stub_rc}; }}
{helper_src}
_attest_test_evidence_equivalent "{fixture}"
"""
    return subprocess.run(["bash", "-c", script], capture_output=True, text=True)


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    root = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]
    src = (root / "docs/system/workspace/scripts/worktree/pr-merge-guarded").read_text(encoding="utf-8")
    helper = extract_helper(src)

    check("helper defined", bool(helper))
    check("helper invoked after test worktree merge", "_attest_test_evidence_equivalent \"$_test_wt\"" in src)
    check("delegates to attest-meta", "attest-meta" in helper)
    check("prints stale retry guidance", "run: freely test-gate run" in helper)
    check("no write channel bypass", "import platform_adapter" not in helper)

    with tempfile.TemporaryDirectory(prefix="freely-merge-followthrough-") as td:
        fixture = Path(td)
        qdir = fixture / "docs/system/workspace/scripts/quality"
        qdir.mkdir(parents=True)
        (qdir / "test-evidence.py").write_text("# stub\n", encoding="utf-8")
        gate = fixture / ".freely/run/test-gate.env"
        gate.parent.mkdir(parents=True)
        gate.write_text('TEST_STATUS="completed"\nEQUIVALENCE_SENSITIVE_PATHS="bin/,tests/"\n', encoding="utf-8")

        ok = run_helper(fixture, helper, 0)
        check("rc=0 propagates", ok.returncode == 0, ok.stderr[:200])
        args_text = ((fixture / "capture.txt").read_text(encoding="utf-8")
                     if (fixture / "capture.txt").exists() else "")
        check("attest-meta called with gate", "--gate" in args_text and str(gate) in args_text)
        check("stored sensitive paths reused", "bin/,tests/" in args_text, args_text[:300])
        check("success receipt printed", "carried forward" in ok.stdout)

        bad = run_helper(fixture, helper, 1)
        check("rc=1 propagates", bad.returncode == 1, bad.stderr[:200])
        check("retry guidance on failure", "run: freely test-gate run" in bad.stderr, bad.stderr[:300])

        gate.unlink()
        missing = run_helper(fixture, helper, 0)
        check("missing gate fails closed", missing.returncode != 0)

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
