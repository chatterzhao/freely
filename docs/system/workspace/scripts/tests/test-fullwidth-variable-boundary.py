#!/usr/bin/env python3
"""AT-001 for raw-20261127T100325Z / I-20261127T100325Z-A (#4734).

Under `set -u`, a full-width colon adjacent to `$var` is parsed as part of the
variable name and masks the real failure receipt. Shell string interpolations
must use explicit `${var}` boundaries.

Usage: python3 ...test-fullwidth-variable-boundary.py [--source-dir DIR]
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


PATTERN = re.compile(r"\$[A-Za-z_][A-Za-z0-9_]*[：，。；（）]")


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    root = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]
    source = (root / "docs/system/workspace/scripts/worktree/wt-create").read_text(encoding="utf-8")

    check("wt-create source readable", bool(source))
    check("no full-width punctuation glued to a variable",
          not PATTERN.search(source), str(PATTERN.findall(source)[:3]))
    check("failure receipt uses explicit boundary", '（${raw_key}）' in source)

    with tempfile.TemporaryDirectory(prefix="freely-fullwidth-") as td:
        tmp = Path(td)
        bindir = tmp / "bin"
        bindir.mkdir()
        stub = bindir / "issue-sync"
        stub.write_text('#!/usr/bin/env bash\nexit 1\n')
        stub.chmod(0o755)
        script = '''
set -u
ROOT_DIR="$ROOT"; raw_key="20261108T134701Z"
if ! "$ROOT_DIR/bin/issue-sync" --project "$ROOT" create "raw-$raw_key"; then
  echo "拒绝创建工位: issue-sync create 未能补齐缺失平台副本（${raw_key}）" >&2
  exit 1
fi
'''
        env = dict(os.environ, ROOT=str(tmp))
        result = subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=env)
        check("nonzero wrapper fails closed", result.returncode == 1)
        check("no unbound variable in stderr", "unbound variable" not in result.stderr, result.stderr[:200])
        check("actionable refusal printed",
              "issue-sync create 未能补齐缺失平台副本（20261108T134701Z）" in result.stderr,
              result.stderr[:200])

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
