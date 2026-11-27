#!/usr/bin/env python3
"""AT-001 for raw-20261127T085009Z / I-20261127T085009Z-A (#4731).

An explicit --source-platform must break the wt-create ↔ raw-issue-pull
interlock for legacy single-platform raws, and must fill missing replicas
through the issue-sync wrapper with fail-closed partial results.

Usage: python3 ...test-single-platform-materialize.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
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


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    root = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]
    src = (root / "docs/system/workspace/scripts/worktree/wt-create").read_text(encoding="utf-8")
    docs = (root / "docs/system/workspace/commands.md").read_text(encoding="utf-8")

    check("wt-create source readable", bool(src))
    check("replica gate respects explicit source platform",
          'if [[ "$using_new" -eq 1 && "$resume_mode" -eq 0 && -z "$source_platform" ]]; then' in src)
    check("explicit bypass is audited on stderr",
          '--source-platform $source_platform 已显式指定' in src)
    check("missing replicas filled via issue-sync wrapper",
          'issue-sync" --project "$fix_target" create "raw-$raw_key"' in src)
    check("partial replica failure is fatal",
          '拒绝创建工位: issue-sync create 未能补齐缺失平台副本' in src)
    check("commands.md documents --source-platform", "--source-platform" in docs)
    check("no adapter import in worktree wrapper", "import platform_adapter" not in src)

    # Behavioral: the wrapper's exit code must be propagated, not swallowed.
    with tempfile.TemporaryDirectory(prefix="freely-single-platform-") as td:
        tmp = Path(td)
        for rc, expected in ((0, 0), (1, 1)):
            stub = tmp / "issue-sync"
            stub.write_text(f'#!/usr/bin/env bash\nexit {rc}\n')
            stub.chmod(0o755)
            env = dict(os.environ, ROOT=str(tmp))
            script = '''
set -u
ROOT_DIR="$ROOT"
fix_target="$ROOT"
raw_key="20261108T134701Z"
if ! "$ROOT_DIR/bin/issue-sync" --project "$fix_target" create "raw-$raw_key"; then
  echo "拒绝创建工位: issue-sync create 未能补齐缺失平台副本" >&2
  exit 1
fi
exit 0
'''
            if not (tmp / "bin").is_dir():
                (tmp / "bin").mkdir()
            stub.rename(tmp / "bin/issue-sync")
            result = subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=env)
            check(f"issue-sync rc={rc} propagated", result.returncode == expected,
                  f"got {result.returncode}")
            if rc:
                check("failure prints actionable refusal",
                      "issue-sync create 未能补齐缺失平台副本" in result.stderr)

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
