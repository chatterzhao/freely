#!/usr/bin/env python3
"""AT-001 (raw-20261114T031605Z): B1 must decide before it diverges.

Context
-------
`freely-doc-B1_IBM-execution` used to only "read boundary docs" and diverge;
it never asked whether the design itself was right, incomplete, unfinished,
drifted or simply buggy. Three real rounds started coding locally and only
discovered the mismatch at review time (R33.18 / R33.16), when rework had
already been paid for.

This AT pins the new B0 layer (design-intent audit + global-fit four questions),
the hand-off evidence on candidates, and the self-check items. It deliberately
does NOT add a hard gate: forced fields are bypassed by pasting empty text.
Instead it also verifies the round's own B1 artifacts actually followed B0
(self-hosting).

Baseline (develop) has none of it -> red.
"""
from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

SKILL = SRC / "docs/system/workspace/skills/freely-doc-B1_IBM-execution/SKILL.md"
GATE = SRC / "docs/system/workspace/scripts/quality/governance-merge-gate"
BRAIN = SRC / "docs/B1-docs/raw-20261114T031605Z/brainstorms.md"
CANDS = SRC / "docs/B1-docs/raw-20261114T031605Z/candidates.md"

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


def main() -> None:
    print("AT-001 source: " + str(SRC))
    text = read(SKILL)
    gate = read(GATE)

    print("=== STATIC: B0 exists and comes BEFORE divergence ===")
    check(bool(text), "S1 B1 skill readable")
    check("B0：设计意图审计" in text, "S2 B0 section declared")
    check(text.find("B0：设计意图审计") < text.find("4. 发散"),
          "S3 B0 is evaluated before diverge/converge")
    check("先于发散" in text, "S4 B0 ordering is stated explicitly")

    print("=== STATIC: the audit has substance, not just a checkbox ===")
    for anchor in ("设计文档", "既有验收测试", "门禁源码注释", "既有同类实现", "配置约束"):
        check(anchor in text, f"S5 external anchor listed: {anchor}")
    for verdict in ("设计正确", "设计不完整", "实现未完成", "实现偏差", "bug"):
        check(verdict in text, f"S6 five-way verdict present: {verdict}")
    check("与既有断言的冲突" in text and "影响面" in text,
          "S7 conflict + impact surface required")
    check("引用原文" in text, "S8 anchors must be quoted verbatim")

    print("=== STATIC: global-fit four questions ===")
    for q in ("Q1 类别", "Q2 职责边界", "Q3 结构性冲突", "Q4 门禁失配"):
        check(q in text, f"S9 global-fit question present: {q}")

    print("=== STATIC: hand-off evidence and self-check ===")
    check("design_verdict" in text and "anchor_refs" in text,
          "S10 candidates template carries design_verdict / anchor_refs")
    check("## 0. 设计意图审计" in text and "## 0.1 全局适配反思" in text,
          "S11 brainstorms template carries the audit sections")
    check("brainstorms.md` 含 `## 0. 设计意图审计" in text,
          "S12 self-check verifies the audit section")
    check("design_verdict 与 §0 判定一致" in text,
          "S13 self-check verifies verdict consistency")

    print("=== BOUNDARY: no new hard gate, L0 unchanged ===")
    check("不做硬门禁" in text and "逐字命中" in text,
          "S14 skill explicitly refuses a field-existence hard gate")
    check("design_verdict" not in gate,
          "S15 governance-merge-gate was NOT modified into a hard gate")
    check("review L0" in text or "L0" in text,
          "S16 B0 states its division of labour with review L0")

    print("=== SELF-HOSTING: this round's own B1 followed B0 ===")
    brain = read(BRAIN)
    cands = read(CANDS)
    check("## 0. 设计意图审计（先于方案）" in brain,
          "S17 this round's brainstorms.md opens with the audit")
    check("## 0.1 全局适配反思（四问）" in brain,
          "S18 the four global-fit questions were actually answered")
    check(brain.count("外部锚点") >= 1 and "判定（五分类）" in brain,
          "S19 anchors + five-way verdict recorded")
    check("- design_verdict:" in cands and "- anchor_refs:" in cands,
          "S20 this round's candidates.md carries the hand-off fields")

    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
