#!/usr/bin/env python3
"""AT-001 — raw-20261114T111702Z / #4654.

`freely comment` must not reference the undefined PROJECT_ROOT in the
ACP worker-notification block of cmd_comment(). It must reuse the globally
defined SELF_ROOT, preserve both platform write and ACP notification, and
keep runtime/freely within its line budget.

Static contract (no platform writes):
1. cmd_comment() body contains no ${PROJECT_ROOT}.
2. The notification block uses ${SELF_ROOT} at least 4 times.
3. SELF_ROOT is defined globally near the top of the runtime.
4. agent_working.agent_list_by_raw_key call is preserved.
5. run-acp-prompt.py invocation is preserved.
6. platform-adapter comment write is preserved.
7. `bash -n runtime/freely` succeeds.
8. line count <= runtime/.size-budget.

Run:
  RED   : python3 test-comment-root-variable.py --source-dir <develop>
  GREEN : python3 test-comment-root-variable.py
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
ROOT = Path(os.environ.get("COMMENT_ROOT_VARIABLE_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        ROOT = Path(sys.argv[_i + 1]).resolve()

RUNTIME = ROOT / "docs/system/workspace/scripts/runtime/freely"
BUDGET = ROOT / "docs/system/workspace/scripts/runtime/.size-budget"
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


def cmd_comment_body(src: str) -> str:
    lines = src.splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith("cmd_comment()")), None)
    if start is None:
        return ""
    end = next((i for i in range(start + 1, len(lines)) if lines[i] == "}"), len(lines))
    return "\n".join(lines[start:end])


def main() -> int:
    print(f"source: {ROOT}")
    src = read(RUNTIME)
    body = cmd_comment_body(src)
    check(bool(src), "runtime/freely exists")
    check(bool(body), "cmd_comment() body extracted")
    check("${PROJECT_ROOT}" not in body, "cmd_comment() has no ${PROJECT_ROOT}")
    check(body.count("${SELF_ROOT}") >= 4, "notification block reuses ${SELF_ROOT} (>=4 refs)")
    check(
        bool(re.search(r'^SELF_ROOT="\$\(cd "\$\(dirname "\$\{BASH_SOURCE\[0\]\}"\)', src, re.M)),
        "SELF_ROOT defined globally at runtime head",
    )
    check("agent_list_by_raw_key" in body, "agent_working lookup preserved")
    check("run-acp-prompt.py" in body, "ACP worker notification preserved")
    check(bool(re.search(r'"\$?_?adapter"\s+comment|_adapter\s+comment|\bcomment\b.*adapter', body)),
          "platform-adapter comment write preserved")
    if src:
        proc = subprocess.run(["bash", "-n", str(RUNTIME)], capture_output=True, text=True)
        check(proc.returncode == 0, f"bash -n runtime/freely rc={proc.returncode}")
    else:
        check(False, "bash -n runtime/freely (source missing)")
    lines_n = len(src.splitlines())
    budget_raw = read(BUDGET).strip()
    budget = int(budget_raw) if budget_raw.isdigit() else -1
    check(budget > 0 and lines_n <= budget, f"runtime lines {lines_n} <= budget {budget}")

    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
