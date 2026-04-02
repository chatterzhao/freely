# Verification: worktree-exclusive-ownership-and-promotion-lease-governance

- issue_id: `I-20260402-0455-A`
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
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-hard-stale-intent-reclaim`
- `bash docs/system/workspace/scripts/tests/test-freely-fleet-status-recorded-ownership-conflict-surface`
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
- `docs/system/workspace/scripts/worktree/merge-guarded`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/epics/workspace-routing-foundation/worktree-exclusive-ownership-and-promotion-lease-governance/pre-tests.md`
