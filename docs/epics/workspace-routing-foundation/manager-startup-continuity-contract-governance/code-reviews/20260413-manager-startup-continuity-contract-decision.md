# Contract Decision: manager-startup-continuity-contract-governance

- issue_id: `I-20260413-0420-B`
- issue_path: `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/issues/manager-startup-continuity-contract-governance.md`
- branch: `feature/manager-startup-continuity-contract-governance-20260413`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260413-feature-manager-startup-continuity-contract-governance`
- decision_date: `2026-04-13`
- author: `codex`

## Decision

- decision: `Freeze the follow-on manager startup contract around a runtime-seeded continuity claim/stub on the expected continuity path plus a separate machine-readable manager handoff state.`
- why_this: `Startup authority now gives Freely a trustworthy launch boundary. The narrowest next seam is to reuse the expected continuity path runtime already parses and the fallback continuity writer runtime already owns, instead of inventing a new artifact family or pretending prompt wording is sufficient.`
- alternatives_considered: `Keep prompt-only behavior; bind daemon ready directly to continuity in the first pass; invent a new bootstrap sidecar artifact before using the existing continuity path seam.`
- boundary_non_goals: `Do not implement the runtime stub writer or state fields in this owner. Do not fold worker continuity consumption or generic watchdog policy into this contract freeze.`
- residual_risk: `The exact markdown stub shape and bounded SLA for a missing handoff remain implementation details for the next owner, but the contract boundary and preferred seam are now frozen.`

## Frozen Contract

1. `launch_bootstrapped` and `manager_handoff_materialized` are separate truths.
2. The first handoff artifact must be created on the normal startup path.
3. The preferred first artifact is a runtime-seeded continuity claim/stub at the expected manager continuity path.
4. Manager AI is responsible for enriching or replacing that stub with semantic continuity.
5. Runtime status must expose handoff state separately from startup authority/readiness.
6. Stop fallback remains repair-only and must not count as normal startup success.
