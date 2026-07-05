# Implementation Decision: manager-startup-continuity-materialization-governance

- issue_id: `I-20260413-0420-D`
- issue_path: `docs/B2-docs/ibm/manager-startup-continuity-materialization-governance/issues/manager-startup-continuity-materialization-governance.md`
- branch: `feature/manager-startup-continuity-materialization-governance-20260413`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260413-feature-manager-startup-continuity-materialization-governance`
- decision_date: `2026-04-13`
- author: `codex`

## Implementation Decision Note

- decision: `Materialize the first manager startup continuity artifact on the normal path by seeding a runtime-written stub at the prompt-required continuity path and exposing a bounded handoff-state classifier in runtime status.`
- why_this: `The contract owner already proved the defect is not generic readiness or watchdog policy; it is that the expected continuity path stays empty on the normal path. Reusing that path and the existing fallback writer seam is the smallest implementation that repairs Freely's startup handoff chain.`
- alternatives_considered: `Keep relying on prompt wording; redefine daemon readiness to wait for manager continuity now; invent a separate startup sidecar artifact family; treat stop fallback as acceptable normal startup evidence.`
- boundary_non_goals: `Do not change daemon-ready semantics, generic restart policy, worker continuation consumption, or the wider runtime phase model.`
- residual_risk: `This owner creates and classifies the first handoff artifact, but it does not yet guarantee how quickly manager enrichment will replace the seeded startup stub with fully materialized semantic continuity.`

## Why

- startup authority already solved who launched, but not whether the first continuity artifact exists on success
- stop fallback already had a writer path, which meant repair logic was unintentionally closer to the real seam than normal startup logic
- the prompt-required continuity path was already the canonical artifact location, so adding another artifact family would only increase drift

## Scope Decision

- Keep only:
  - normal-path startup stub materialization at the expected continuity path
  - writer-based handoff-state classification
  - `live-status` and `fleet-status` handoff-state surfacing
- Exclude:
  - readiness-state changes for `daemon start`
  - manager enrichment or worker-consumption policy
  - broad continuity lifecycle timeouts or repair automation
