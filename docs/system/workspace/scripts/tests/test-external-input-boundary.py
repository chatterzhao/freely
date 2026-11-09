#!/usr/bin/env python3
"""AT-001 — raw-20261103T132636Z / #4156 (partial: injection + sed portability).

Two of the four surfaces in the issue are pinned here:

1. **External strings becoming code.** `pr-review-guarded` used to interpolate
   the caller-supplied branch name into a `python3 -c "..."` body
   (`try_canonicalize_raw_key('$review_branch')`). A branch name may legally
   contain `'` `;` `$` backticks (git check-ref-format accepts them), so reviewing
   an external PR could execute code on the maintainer's machine.
2. **`sed -i ''` is BSD-only.** On GNU sed the empty argument becomes a filename,
   `set -e` aborts — and in `pr-review-guarded` that happens *after* the review
   was recorded, so the phase never advances.

Not covered here (split into a separate issue): the remaining ~195 `python3 -c`
sites, `source`-ing state files, and the TSV worker-dispatch channel.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (interpolated + BSD sed -> FAIL)
  GREEN : --source-dir <this worktree>
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("INJECTION_SOURCE_ROOT", str(PROJECT))).resolve()

PAYLOAD = "fix/x');print('PWNED');#"

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


def _scan(src: Path):
    root = src
    hits_interp = []
    hits_bsd_sed = []
    hits_uncleaned = []
    for base in ("bin", "docs/system/workspace/scripts"):
        for path in (root / base).rglob("*"):
            if not path.is_file() or path.suffix == ".pyc":
                continue
            try:
                text = path.read_text(errors="replace")
            except OSError:
                continue
            rel = path.relative_to(root).as_posix()
            if "/tests/" in rel:
                continue
            if "pr-review-guarded" in rel and re.search(
                    r"try_canonicalize_raw_key\('\$", text):
                hits_interp.append(rel)
            for i, line in enumerate(text.split("\n")):
                if "sed -i ''" in line:
                    hits_bsd_sed.append(f"{rel}:{i + 1}")
                if "sed -i.bak" in line and "rm -f" not in line:
                    hits_uncleaned.append(f"{rel}:{i + 1}")
    return hits_interp, hits_bsd_sed, hits_uncleaned


def static_checks(src: Path) -> None:
    print("=== STATIC: external strings are not interpolated; sed is portable ===")
    interp, bsd_sed, uncleaned = _scan(src)
    expect(not interp,
           f"branch name is no longer interpolated into the review script body (found {interp})")
    expect(not bsd_sed,
           f"no BSD-only `sed -i ''` remains (found {len(bsd_sed)}: {bsd_sed[:3]})")
    expect(not uncleaned,
           f"every `sed -i.bak` cleans its backup in the same command (found {uncleaned[:3]})")


def injection_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: interpolation executes, argv does not ===")

    # PoC 1: the old shape really is exploitable — this keeps the check honest.
    vuln = subprocess.run(
        ["bash", "-c", f"""python3 -c "print('{PAYLOAD}')" """],
        capture_output=True, text=True, timeout=60)
    expect("PWNED" in vuln.stdout or vuln.returncode != 0,
           f"PoC: interpolated branch name executes attacker code (out={vuln.stdout.strip()[:40]!r})")

    # The safe shape receives the payload verbatim and never evaluates it.
    script = (
        "import sys\n"
        "branch = sys.argv[1]\n"
        "print('GOT=' + branch)\n"
    )
    safe = subprocess.run(["python3", "-", PAYLOAD], input=script,
                          capture_output=True, text=True, timeout=60)
    expect(safe.stdout.strip() == f"GOT={PAYLOAD}",
           f"argv passing keeps the payload inert (out={safe.stdout.strip()[:60]!r})")


def sed_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: sed -i.bak works and leaves no residue ===")
    target = tmp / "sample.txt"
    target.write_text("phase_state: done_b2_ibm\n", encoding="utf-8")
    r = subprocess.run(
        ["bash", "-c",
         f"""sed -i.bak 's/phase_state: done_b2_ibm/phase_state: completed/' "{target}"; rm -f "{target}.bak" """],
        capture_output=True, text=True, timeout=60)
    body = target.read_text(encoding="utf-8")
    expect(r.returncode == 0 and "phase_state: completed" in body,
           f"sed -i.bak rewrites the file (rc={r.returncode})")
    expect(not Path(f"{target}.bak").exists(),
           "the .bak file is removed in the same command")


def main() -> int:
    src = SRC
    if "--source-dir" in sys.argv:
        idx = sys.argv.index("--source-dir")
        if idx + 1 < len(sys.argv):
            src = Path(sys.argv[idx + 1]).resolve()

    static_checks(src)
    tmp = Path(tempfile.mkdtemp(prefix="injection-"))
    try:
        injection_checks(tmp)
        sed_checks(tmp)
    finally:
        subprocess.run(["rm", "-rf", str(tmp)], check=False)

    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())
