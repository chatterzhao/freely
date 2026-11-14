#!/usr/bin/env python3
"""AT-001 (raw-20261113T115950Z): the review EXECUTION guidance must carry L0.

R33.14 wrote L0 (project-intent consistency) into freely-tdd-review/SKILL.md, but
pr-review-guarded - the only execution entry point - still asked for the four
dimensions only (red/green/adequacy/refactor). A reviewer could therefore pass on
the four layers alone and the L0 rule never ran.

This AT pins:
  * the ACP prompt asks for L0 before the four layers, with external anchors,
    Q1-Q5, and the four-part burden of proof for gate changes;
  * the prompt's JSON carries an intent dimension that can force a fail;
  * the manual fallback tells the reviewer to do L0 first and to record a
    "## L0[...]" section;
  * review_verdict.parse_verdict still behaves exactly as before (the guidance
    change must not break the merge gate's verdict contract).

Baseline (develop) must fail: neither surface mentions L0 at all.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

GUARD = SRC / "docs/system/workspace/scripts/worktree/pr-review-guarded"
VERDICT = SRC / "docs/system/workspace/scripts/worktree/review_verdict.py"

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


def section(text: str, start_marker: str, end_marker: str) -> str:
    start = text.find(start_marker)
    if start < 0:
        return ""
    end = text.find(end_marker, start)
    return text[start:end] if end > start else text[start:]


def main() -> None:
    text = read(GUARD)
    print("AT-001 source: " + str(SRC))

    prompt = section(text, "You are the Freely TDD Reviewer", "# Determine ACP launch kind")
    manual = section(text, 'echo "  审查步骤:"', 'exit 1')

    print("=== PROMPT: L0 runs before the four layers ===")
    check("L0 (project-intent consistency) BEFORE the four-layer review" in prompt,
          "S1 prompt states L0 comes before the four layers")
    check("Step 0 (MANDATORY" in prompt,
          "S2 prompt has an explicit mandatory Step 0")
    check(prompt.find("Step 0 (MANDATORY") < prompt.find("Then run the four layers"),
          "S3 Step 0 precedes the four-layer instruction")
    check("L0 failing means the whole verdict fails" in prompt,
          "S4 L0 failure forces an overall fail")

    print("=== PROMPT: external anchors and Q1-Q5 ===")
    for anchor in ("design docs", "existing acceptance tests", "gate source comments",
                   "existing implementations"):
        check(anchor in prompt, f"S5 anchor quoted in prompt: {anchor}")
    check("Quote the ACTUAL text" in prompt, "S6 anchors must be quoted verbatim, not paraphrased")
    for q in ("Q1 conflict", "Q2 gate strength", "Q3 capability downgrade",
              "Q4 second source of truth", "Q5 design drift"):
        check(q in prompt, f"S7 mandatory question present: {q}")
    for part in ("why it was designed that way", "why it must change now",
                 "implementation defect or design error", "strength is not reduced"):
        check(part in prompt, f"S8 gate-change proof present: {part}")
    check("cannot prove itself" in prompt,
          "S9 prompt forbids self-justification via B1/B2")

    print("=== PROMPT: JSON intent dimension ===")
    check('"intent": {"status": "pass"|"fail"' in prompt,
          "S10 the verdict JSON carries an intent dimension")
    check('"intent": "fail" forces "verdict": "fail"' in prompt,
          "S11 intent=fail forces verdict=fail")
    for dim in ("red", "green", "adequacy", "refactor"):
        check(f'"{dim}": {{"status"' in prompt, f"S12 four-layer dimension retained: {dim}")

    print("=== MANUAL FALLBACK: L0 first ===")
    check("先做 L0" in manual, "S13 manual steps start with L0")
    check("Q1 冲突" in manual and "Q5 设计漂移" in manual,
          "S14 manual steps enumerate Q1-Q5")
    check("四段证据" in manual, "S15 manual steps require the four-part proof")
    check("## L0：项目意图一致性" in manual,
          "S16 manual review doc must record the L0 section")
    check(manual.find("先做 L0") < manual.find("四层审查"),
          "S17 L0 comes before the four-layer step")

    print("=== CONTRACT: verdict parsing is untouched ===")
    spec = importlib.util.spec_from_file_location("review_verdict_under_test", VERDICT)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        cases = [
            ("---\nverdict: pass\n---\n", "pass"),
            ("- verdict: **pass**", "pass"),
            ("- verdict: fail", "fail"),
            ("- verdict: needs_changes", "needs_changes"),
            ("no verdict here", "unknown"),
        ]
        for body, want in cases:
            got = module.parse_verdict(body)
            check(got == want, f"S18 parse_verdict({want!r}) unchanged -> got {got!r}")
        check(module.VALID == {"pass", "fail", "needs_changes"},
              "S19 the accepted verdict vocabulary is unchanged")
    else:
        bad("S18 review_verdict module is importable")

    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
