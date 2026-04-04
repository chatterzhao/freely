# Implementation Decision: governance-chain-legacy-repair

- issue_path: `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
- branch: `feature/governance-chain-legacy-repair-20260403-1100`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-1100-feature-governance-chain-legacy-repair`

## decision

Materialize one umbrella owner first, then absorb or legalize the active child repair slices, instead of weakening the gate or pretending each child slice already has an independent issue chain.

## why_this

The real problem is a broken canonical governance chain, not merely a collection of field-level fixes. Without a parent owner, every child slice ends up inventing its own local truth and still fails the lifecycle rules the repair is supposed to restore.

## alternatives_considered

1. Weaken `governance-merge-gate` so the existing legacy drift can pass.
   - Rejected because it hides the problem instead of repairing it.
2. Create a full issue/progress chain for every child slice before materializing the parent owner.
   - Rejected because the current dependence is clearly umbrella-first; modeling the leaves first would further fragment authority.

## boundary_non_goals

- Do not reopen already-completed owners.
- Do not justify stale sibling worktrees as canonical truth.
- Do not turn this owner into a permanent bucket for all future governance drift.

## residual_risk

Even after the umbrella owner is materialized, promotion is still unsafe until the child slices are normalized and the fleet cleanup obligations are reviewed against the current dirty/stale worktree set.
