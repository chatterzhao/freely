---
name: Gate Scope Alignment Implementation Decision Note
owner_issue: I-20260616T030213Z-A
owner_issue_path: docs/issues/I-20260616T030213Z-A/issue.md
implementation_decision_note: true
phase_state: completed
review_id: gate-scope-alignment-review
decision: Remove runtime script paths from is_governance_only_path in governance-merge-gate
why_this: LAWS.md limits FREELY_SKIP_IBM_GATE to docs/cleanup/format but gate allowed runtime scripts
alternatives_considered:
  - "Expand LAWS.md to match gate: would allow more bypasses, security risk"
  - "Split workspace scripts into infrastructure vs runtime: too complex, unclear boundary"
  - "Align gate to LAWS.md: simplest, clearest, least risk"
boundary_non_goals:
  - "Does not change how hooks run"
  - "Does not affect non-FREELY_SKIP_IBM_GATE merge path"
residual_risk: |
  Fixes to governance-merge-gate itself will still need IBM lifecycle when
  they change non-quality paths. Meta-governance changes to the gate file
  itself remain governance-only.
