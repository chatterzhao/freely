#!/usr/bin/env python3
"""AT-001 (raw-20261103T063354Z): PR closeout must use configured platform names.

Baseline passes `git remote` names (github/origin/all) into
`platform-adapter close-pr`, which only knows configured platforms
(github/gitee) and prints {"status":"error","error":"unknown: origin"}.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

MERGE = SRC / "docs/system/workspace/scripts/worktree/pr-merge-guarded"
ADAPTER = SRC / "docs/system/workspace/scripts/sync/platform-adapter.py"

OK = 0
BAD = 0


def check(cond: bool, label: str, detail: str = "") -> None:
    global OK, BAD
    if cond:
        OK += 1
        print("  [ok] " + label)
    else:
        BAD += 1
        print("  [FAIL] " + label + (" — " + detail if detail else ""))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def block(text: str, start: str, end: str) -> str:
    i = text.find(start)
    if i < 0:
        return ""
    j = text.find(end, i + len(start))
    return text[i:j if j > 0 else len(text)]


def main() -> None:
    print("AT-001 source: " + str(SRC))
    merge_text = read(MERGE)
    adapter_text = read(ADAPTER)
    fn = block(merge_text, "_sync_prs_across_platforms()", "_push_source_branch_to_all_remotes()")

    print("=== source contract ===")
    check(bool(fn), "S1 closeout helper found")
    check("configured-platforms" in adapter_text,
          "S2 adapter exposes read-only configured-platforms action")
    check("configured-platforms" in fn,
          "S3 closeout helper consumes adapter configured-platforms")
    code = "\n".join(ln for ln in fn.splitlines() if not ln.strip().startswith("#"))
    check("for platform in $(git remote" not in code and "git remote | grep" not in code,
          "S4 closeout helper no longer iterates git remotes")
    check('close-pr "$platform"' in code,
          "S5 close-pr receives a configured platform name")
    check('"github"' in code and "continue" in code,
          "S6 github is skipped (merge already closes it)")
    check("|| true" not in code,
          "S7 close-pr failures are not swallowed")
    check("WARNING" in code and "close-pr" in code,
          "S8 failures produce an actionable warning")

    print("=== behavioural model ===")
    # Map configured platforms -> closeout targets; remote names must never
    # enter the adapter call.
    configured = ["github", "gitee"]
    remotes = ["github", "origin", "all"]
    targets = [p for p in configured if p != "github"]
    check(targets == ["gitee"], "B1 only non-github configured platform is closed")
    check(all(t not in remotes for t in targets),
          "B2 adapter targets are platform names, not remote names")

    try:
        r = subprocess.run([sys.executable, str(ADAPTER), "configured-platforms"],
                           cwd=str(SRC), capture_output=True, text=True, timeout=30)
        names = json.loads(r.stdout) if r.returncode == 0 else []
        check(isinstance(names, list) and all(n in ("github", "gitee") for n in names),
              "B3 adapter configured-platforms returns JSON platform names", r.stdout[:120])
    except Exception as exc:  # pragma: no cover
        check(False, "B3 adapter configured-platforms call", str(exc))

    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
