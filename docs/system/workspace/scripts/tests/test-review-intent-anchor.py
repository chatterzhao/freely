#!/usr/bin/env python3
"""AT-001 (raw-20261113T113100Z): the review skill must carry an L0 intent anchor.

Context: `freely-tdd-review` used to audit ONLY fidelity between adjacent IBM
nodes (raw→B1→B2→implementation→tests). R33.8 / R33.9 / R33.10 passed that audit
while drifting from the project's own design (bypassing the batch-driven linked
retirement, weakening the protected-branch gate). This AT pins the new L0 layer
so a future edit cannot silently drop it.

Baseline (develop) must fail: no L0 section at all.
"""
from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

SKILL = SRC / "docs/system/workspace/skills/freely-tdd-review/SKILL.md"

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


def main() -> None:
    text = SKILL.read_text(encoding="utf-8", errors="replace") if SKILL.is_file() else ""
    print("AT-001 source: " + str(SRC))

    check("## L0：项目意图一致性" in text, "S1 L0 section exists")
    check("## 核心方法" in text, "S2 four-layer core method still present")
    check(text.find("## L0：") >= 0 and text.find("## L0：") < text.find("## 核心方法"),
          "S3 L0 is evaluated BEFORE the four layers")

    for q in ("Q1 冲突", "Q2 门禁强度", "Q3 能力降级", "Q4 第二套语义", "Q5 设计漂移"):
        check(q in text, f"S4 mandatory question present: {q}")

    check("既有验收测试" in text and "门禁的源码注释" in text,
          "S5 external anchors include existing acceptance tests and gate rationale")
    check("外部锚点" in text and "不能用自己证明自己" in text,
          "S6 anchors take precedence over the round's own B1/B2")

    for part in ("当初为什么这样设计", "现在为什么必须改", "判定", "强度不降"):
        check(part in text, f"S7 gate-change evidence present: {part}")

    check("失败判据" in text and "补数据" in text,
          "S8 fail criteria include 'making a gate pass by hand-patching data'")

    check("## L0：项目意图一致性（先于四层；失败则整体 fail）" in text,
          "S9 review output format carries the L0 findings block")

    for case in ("R33.8", "R33.9", "R33.10"):
        check(case in text, f"S10 real-world case retained: {case}")

    check("四层全绿仍可能整体漂移" in text,
          "S11 skill states the structural blind spot explicitly")

    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
