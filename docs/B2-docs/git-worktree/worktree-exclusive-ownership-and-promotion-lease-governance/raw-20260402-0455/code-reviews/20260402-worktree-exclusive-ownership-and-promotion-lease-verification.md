# Verification: worktree-exclusive-ownership-and-promotion-lease-governance

- issue_id: `I-20260402-0455-A`
- issue_path: `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/raw-20260402-0455issues/worktree-exclusive-ownership-and-promotion-lease-governance.md`
- branch: `feature/worktree-exclusive-ownership-governance-20260402-0455`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260402-0455-feature-worktree-exclusive-ownership-governance`
- verification_date: `2026-04-02`
- reviewer: `codex`
- verdict: `pass_for_verification`

## Commands

- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-recorded-ownership-conflict`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-ownership-conflict-recorded-owner`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-hard-stale-recorded-owner-does-not-block`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-promotion-queue-recorded-owner`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-promotion-hard-stale-owner`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-conflicting-recorded-promotion`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-hard-stale-intent-reclaim`
- `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
- `git diff --check`
- `./bin/governance-check`

## Results

1. phase-1 ownership truth is now machine-readable across launch scheduling, cleanup followthrough, promotion gating, and status surfaces; manager/worker routing no longer depends on PID-only heuristics for these mutate paths.
2. duplicate mutate targets remain blocked behind `active-owner`, `queued-owner`, `frozen-owner`, and `soft_stale recorded-owner`, while `hard_stale recorded-owner` now exits the launch/recovery blocker set.
3. cleanup followthrough preserves live or recoverable ownership claims but now reclaims merged worktrees once the only remaining holder is a `hard_stale recorded-owner`.
4. canonical worktree target normalization is preserved end-to-end, so ownership comparisons do not drift across aliased paths such as `/tmp` versus `/private/tmp`.

## Evidence

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/hooks/pre-merge-commit.sh`
- `docs/system/workspace/scripts/worktree/pr-merge-guarded`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/raw-20260402-0455/verification/pre-tests.md`

## Develop Absorption

- canonical_merge_commit: `a10f6d8`
- canonical_merge_target: `develop`
- post_merge_replay:
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status-recorded-ownership-conflict`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status-ownership-conflict-recorded-owner`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status-hard-stale-recorded-owner-does-not-block`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-promotion-queue-recorded-owner`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-promotion-hard-stale-owner`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-conflicting-recorded-promotion`
  - `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
  - `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-hard-stale-intent-reclaim`
  - `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
  - `git diff --check`
  - `./bin/governance-check`

## Implementation Decision Note

- decision: `Introduce a phase-1 ownership lease layer that normalizes mutate targets, surfaces holder state in runtime status, blocks duplicate mutate intents, and gates develop promotion on the same ownership truth.`
- why_this: `PID/session occupancy alone could not explain or prevent same-worktree edit collisions, duplicate cleanup, or duplicate promotion followthrough; phase-1 needed a machine-readable ownership surface shared by manager launch, cleanup, status, and merge paths.`
- alternatives_considered: `Considered a raw worktree lockfile, a single worktree->pid binding, and relying on worker-side courtesy checks. Those options either failed stale/takeover handling, blocked legitimate read-only concurrency, or left duplicate promotion unresolved.`
- boundary_non_goals: `This owner does not make runtime perform semantic arbitration, does not block read-only/review concurrency, and does not broaden ownership gating beyond phase-1 edit/cleanup/promotion paths.`
- residual_risk: `Future orchestration work may still need a richer reclaim workflow or broader ownership semantics, but that should reopen as a narrower follow-on owner instead of widening this completed phase-1 slice.`
