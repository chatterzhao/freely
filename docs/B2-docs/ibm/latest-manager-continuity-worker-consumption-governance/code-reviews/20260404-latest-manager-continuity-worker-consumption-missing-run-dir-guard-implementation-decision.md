# Implementation Decision: latest-manager-continuity-worker-consumption-governance missing-run-dir guard

- issue_id: `I-20260322-0445`
- issue_path: `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`
- branch: `feature/runtime-status-missing-run-dir-guard-20260404-2120`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260404-2120-feature-runtime-status-missing-run-dir-guard`
- decision_date: `2026-04-04`
- author: `codex`

## Implementation Decision Note

- decision: `Guard the shared sibling-runtime scanning helpers in docs/system/workspace/scripts/runtime/freely so they short-circuit cleanly when a sibling worktree has no runtime or logs directory, and lock the behavior with focused status regressions.`
- why_this: `The observed stderr leak came from helper functions shared by continuity consumption, launchability checks, semantic-loop inspection, prompt discovery, and adjacent cycle-log lookup. A narrow guard at the helper boundary fixes both live-status and fleet-status without inventing a status-only fallback path or widening the blocked-intake supervision contract.`
- alternatives_considered: `Considered suppressing stderr only at the status command call sites, and considered forcing every sibling worktree to materialize an empty .freely/run tree before it can appear in fleet scans. The first would leave other helper consumers noisy and inconsistent; the second would turn an optional runtime initialization detail into a false fleet invariant.`
- boundary_non_goals: `Do not redesign broader websocket blocked-intake recovery, slot-switch busy handling, or worktree lifecycle policy. Do not change the meaning of empty latest-continuity / latest-prompt results beyond silencing missing-run-dir noise.`
- residual_risk: `Future helper paths that scan sibling runtime state outside the guarded functions could still leak similar stderr if they bypass these wrappers. This repair only covers the currently shared continuity/prompt lookup family.`
