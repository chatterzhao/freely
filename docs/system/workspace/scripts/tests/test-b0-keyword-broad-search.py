#!/usr/bin/env python3
"""AT-001 — raw-20261114T095625Z / #4652.

B1's B0 design-intent audit must require keyword broad-search across docs/bin,
multi-document layering, contradiction cross-check, and an explicit
continue-vs-dropped binary decision with a covering-issue proof for dropped.
It must stay a research method (no hard gate).

Run:
  RED   : python3 test-b0-keyword-broad-search.py --source-dir <develop>
  GREEN : python3 test-b0-keyword-broad-search.py
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
ROOT = Path(os.environ.get("B0_BROAD_SEARCH_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        ROOT = Path(sys.argv[_i + 1]).resolve()

SKILL = ROOT / "docs/system/workspace/skills/freely-doc-B1_IBM-execution/SKILL.md"
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
    skill = read(SKILL)
    check(bool(skill), "B1 skill exists")
    # B0 section only (up to 0.1 / next heading after B0 block)
    b0 = skill.split("**B0：", 1)[-1].split("## 工作流", 1)[0]
    check("关键词" in b0 and ("广搜" in b0 or "broad" in b0.lower()),
          "B0 requires keyword broad-search")
    check(all(x in b0 for x in ("docs/", "bin/")),
          "keyword families search docs/ and bin/")
    check("当前生效" in b0 and "历史" in b0 and "权威恢复点" in b0,
          "B0 requires three-way document layering")
    check("矛盾" in b0, "B0 requires contradiction cross-check")
    check(("继续" in b0 and "二元决策" in b0),
          "B0 requires explicit continue/dropped binary decision field")
    check("覆盖者" in b0 and "禁止" in b0,
          "dropped must cite covering-issue evidence (explicit rule)")
    check("刻意不做硬门禁" in skill,
          "no-hard-gate stance preserved")
    # Self-check block: from the heading up to the next top-level section
    # (`## 不负责` etc.). Do not cut on `##` because checklist items mention
    # `## 0.` inline.
    selfcheck = skill.split("### 完成自检", 1)[-1].split("\n## ", 1)[0]
    check("关键词" in selfcheck and "广搜" in selfcheck,
          "self-check includes keyword broad-search item")
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
