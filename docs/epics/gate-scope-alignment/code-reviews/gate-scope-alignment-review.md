---
name: Gate Scope Alignment Implementation Decision Note
owner_issue: I-20260616T030213Z-A
owner_issue_path: docs/issues/I-20260616T030213Z-A/issue.md
implementation_decision_note: true
phase_state: completed
review_id: gate-scope-alignment-review
---

# Implementation Decision Note: Gate Scope Alignment

- issue_id: I-20260616T030213Z-A
- issue_path: docs/issues/I-20260616T030213Z-A/issue.md

## Implementation Decision Note

- decision: Remove hooks/, scripts/runtime/, scripts/worktree/, scripts/tests/ from is_governance_only_path in governance-merge-gate
- why_this: LAWS.md limits FREELY_SKIP_IBM_GATE to docs/cleanup/format but gate allowed runtime script changes to skip IBM lifecycle
- alternatives_considered: Expand LAWS.md to match gate (rejected: more bypasses); Split into categories (rejected: unclear boundary); Align gate to LAWS.md (chosen: simplest, safest)
- boundary_non_goals: Does not change hook execution behavior; Does not affect non-skip merge path
- residual_risk: Meta-governance fixes to gate itself remain governance-only. All other runtime changes require full IBM lifecycle.
