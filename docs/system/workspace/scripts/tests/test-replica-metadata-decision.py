#!/usr/bin/env python3
"""AT-001 (raw-20261114T034750Z): pin the replica-metadata design decision.

The raw assumed a *structural* conflict between "sync rewrites issue docs" and
"one worktree = one raw", and proposed moving replica metadata out of the
governed documents. P0 auditing disproved that premise:

  * .freely/config.toml [skip_ibm_gate].allowed_paths ALREADY includes
    docs/B1-docs/ and docs/B2-docs/ -> a governance lane exists;
  * RAW_METADATA_FIELDS is a strict ordered 21-field tuple and validate()
    rejects any missing/extra/reordered key -> moving fields out breaks the
    contract and would require a 500+ document rewrite (R2 precedent);
  * command-wrapper-metadata-lifecycle.md Rejection requires platform_ids
    to be present in the document.

So options B/C are overturned; option A (keep fields in docs, full sweeps go
through the governance lane + field-class judgement) is the decision.

This AT pins the decision record and, crucially, asserts this round did NOT
secretly start implementing it (no contract / gate / config changes).

Baseline (develop) has none of it -> red.
"""
from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

DDR = SRC / "docs/system/workspace/replica-metadata-contract.md"
CONTRACT = SRC / "docs/system/workspace/scripts/lifecycle/raw_metadata_contract.py"
GATE = SRC / "docs/system/workspace/scripts/quality/governance-merge-gate"
BRAIN = SRC / "docs/B1-docs/raw-20261114T034750Z/brainstorms.md"
CANDS = SRC / "docs/B1-docs/raw-20261114T034750Z/candidates.md"

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
    ddr = read(DDR)

    print("=== STATIC: the decision record is complete ===")
    check(bool(ddr), "S1 replica-metadata-contract.md exists")
    check("**采用**" in ddr and "| **A**" in ddr and "保留在 issue 文档" in ddr,
          "S2 option A is selected")
    for opt in ("| **A**", "| **B**", "| **C**"):
        check(opt in ddr, f"S3 option evaluated: {opt}")
    check("推翻" in ddr and "第二真相源" in ddr,
          "S4 B/C are overturned with the second-source argument")
    check("RAW_METADATA_FIELDS" in ddr and "no bulk 824-doc rewrite" in ddr,
          "S5 the strict field contract + R2 migration lesson are cited")
    check("Rejection" in ddr and "fail-closed" in ddr,
          "S6 the Rejection clause is cited as a constraint")

    print("=== STATIC: field classes and lane rules are defined ===")
    check("生命周期字段" in ddr and "副本字段" in ddr,
          "S7 lifecycle vs replica field classes are defined")
    for field in ("platform_ids", "platform_state", "phase_state", "last_synced_comment_at"):
        check(field in ddr, f"S8 field classified: {field}")
    check("chore/sync-" in ddr and "FREELY_SKIP_IBM_GATE" in ddr,
          "S9 governance lane + marker are specified")
    check("逐文档与 base 比对" in ddr and "生命周期字段变化 → **拒绝**" in ddr,
          "S10 field-class judgement is stricter than directory allowlisting")
    check("issue-sync scan" in ddr and "batch --all --lane governance" in ddr,
          "S11 scan / scoped / full-sweep interface split is defined")
    check("禁止无参 batch" in ddr, "S12 unscoped daemon sweep is forbidden")

    print("=== BOUNDARY: this round did NOT start implementing ===")
    check("不改 GATE 1" in ddr and "不迁移" in ddr and "不改 `RAW_METADATA_FIELDS`" in ddr,
          "S13 the no-migration / no-gate-change boundary is stated")
    contract = read(CONTRACT)
    check('"platform_state",' in contract and "RAW_METADATA_FIELDS = (" in contract,
          "S14 RAW_METADATA_FIELDS still contains platform_state (contract untouched)")
    gate = read(GATE)
    check("def is_governance_only_path" in gate,
          "S15 governance-merge-gate still owns the governance-lane decision")
    check("raw-20261114T031043Z" in ddr and "raw-20261114T051655Z" in ddr,
          "S16 landing dependencies are recorded")

    print("=== SELF-HOSTING: this round followed B0 ===")
    brain = read(BRAIN)
    cands = read(CANDS)
    check("## 0. 设计意图审计（先于方案）" in brain,
          "S17 this round's brainstorms opens with the design-intent audit")
    check("## 0.1 全局适配反思（四问）" in brain,
          "S18 the four global-fit questions were answered")
    check("推翻" in brain and "不成立" in brain,
          "S19 P0 explicitly overturns the raw's original premise")
    check("- design_verdict:" in cands and "- anchor_refs:" in cands,
          "S20 candidates carries the hand-off fields")

    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
