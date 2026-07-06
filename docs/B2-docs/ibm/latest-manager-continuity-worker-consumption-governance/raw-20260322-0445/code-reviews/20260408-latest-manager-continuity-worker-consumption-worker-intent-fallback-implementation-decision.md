# Implementation Decision: latest-manager-continuity-worker-consumption-governance worker intent fallback

- issue_id: `I-20260322-0445`
- issue_path: `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`
- branch: `feature/latest-manager-continuity-worker-intent-fallback-20260408`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260408-feature-latest-manager-continuity-worker-intent-fallback`
- decision_date: `2026-04-08`
- author: `codex`

## Implementation Decision Note

- decision: `When worker-local prompt files lack machine-readable intent headers, resolve the authoritative worker prompt from the latest manager continuity and use that prompt for live-status and fleet-status intent surfaces.`
- why_this: `Canonical develop already absorbed the stale branch's other repairs. The remaining real gap was status truth only: worker status still reported prompt intent as none even though manager continuity already owned an authoritative worker prompt with intent metadata for that same worktree. The narrowest repair is to reuse the continuity-owned prompt as status truth rather than inventing a new intent source.`
- alternatives_considered: `Considered splitting a new owner from the stale mixed branch, and considered widening I-20260407-0215-A. The first would duplicate an existing continuity/prompt-consumption family for one helper-level status gap; the second would blur the separate continuity-gap status-truth owner, whose concern is degraded status output and missing prompt-required continuity rather than worker prompt intent consumption.`
- boundary_non_goals: `Do not change worker execution inputs, relaunch policy, queue/frozen selection semantics, or broader manager continuity replacement rules. This repair only changes which prompt file status commands consult when local worker prompt metadata is incomplete.`
- residual_risk: `If future manager continuities emit multiple candidate prompts for the same worker worktree with materially different intent semantics, this first-match fallback will still rely on the current continuity ordering helpers. That broader ordering contract should be handled as a separate follow-on only if evidence appears.`
