---
name: Gate Scope Alignment Implementation Decision Note
owner_issue: I-20260616T030213Z-A
owner_issue_path: docs/issues/I-20260616T030213Z-A/issue.md
implementation_decision_note: true
phase_state: completed
review_id: gate-scope-alignment-review
decision: Remove hooks, scripts/runtime, scripts/worktree, scripts/tests from is_governance_only_path in governance-merge-gate
why_this: |
  LAWS.md limits FREELY_SKIP_IBM_GATE to docs/cleanup/format but gate
  allowed runtime script changes to skip IBM lifecycle. This created
  a compliance gap where code changes bypassed B1_IBM → candidate →
  B2_IBM → I-* chain.
alternatives_considered:
  - "Expand LAWS.md to match gate: would allow more bypasses, increases security risk"
  - "Split scripts into infra vs runtime categories: unclear boundary, complex to maintain"
  - "Align gate to LAWS.md: clearest, safest, simplest"
boundary_non_goals:
  - "Does not change how hooks execute at runtime"
  - "Does not affect full governance-merge-gate path (non-skip)"
  - "Does not touch agent/skill/quality script paths"
residual_risk: |
  Fixes to governance-merge-gate itself still allowed as meta-governance.
  All other runtime script changes now require full IBM lifecycle.
---

# Implementation Decision Note: Gate Scope Alignment

## Decision

Restrict `is_governance_only_path()` in governance-merge-gate to exclude
hooks/, scripts/runtime/, scripts/worktree/, scripts/tests/ from
FREELY_SKIP_IBM_GATE eligibility.

## Why This

LAWS.md §3 states FREELY_SKIP_IBM_GATE=1 is only for docs/cleanup/format
changes. But the gate classified all workspace scripts as governance-only,
allowing runtime code changes to skip IBM lifecycle. This is a compliance
gap between governance policy (LAWS.md) and enforcement (gate code).

## Alternatives Considered

1. Expand LAWS.md: allows more bypasses, security regression
2. Split into categories: unclear boundary between "infra" and "runtime" scripts
3. Align gate to LAWS.md: clearest contract, easiest to verify

## Boundary & Non-Goals

- Does not change hook execution behavior
- Does not affect non-skip merge path  
- Keeps agents/, skills/, quality/ as governance-only

## Residual Risk

Meta-governance fixes to governance-merge-gate itself remain governance-only.
All other runtime script changes now require IBM lifecycle.
