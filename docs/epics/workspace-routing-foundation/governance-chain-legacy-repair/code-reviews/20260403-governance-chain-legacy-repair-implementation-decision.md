# Implementation Decision: governance-chain-legacy-repair

- issue_id: `I-20260403-1100-A`
- issue_path: `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
- branch: `feature/governance-doc-truth-repair-20260404-1105`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260404-1105-feature-governance-doc-truth-repair`

## decision

Restore the missing umbrella owner artifacts first, then absorb the retired historical child slices into canonical truth cleanup, instead of weakening the gate or pretending deleted slices are still live issue lanes.

## why_this

The real problem is a broken canonical governance chain, not merely a collection of field-level fixes. Without a parent owner, both restored docs and leftover slice references invent conflicting local truth and still fail the lifecycle rules the repair is supposed to restore.

## alternatives_considered

1. Weaken `governance-merge-gate` so the existing legacy drift can pass.
   - Rejected because it hides the problem instead of repairing it.
2. Recreate a full issue/progress chain for every deleted child slice before repairing the parent owner.
   - Rejected because the current need is canonical truth repair, not reviving lanes that no longer exist in the active filesystem.

## boundary_non_goals

- Do not reopen already-completed owners.
- Do not justify stale sibling worktrees as canonical truth.
- Do not turn this owner into a permanent bucket for all future governance drift.

## residual_risk

This owner is historical after the 2026-04-04 closeout. Future governance-chain drift must open a new lifecycle on current `develop` instead of reusing this repair owner.
