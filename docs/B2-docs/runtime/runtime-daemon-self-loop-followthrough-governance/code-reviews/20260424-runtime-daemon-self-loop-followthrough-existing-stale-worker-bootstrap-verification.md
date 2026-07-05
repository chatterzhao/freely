# Verification: runtime-daemon-self-loop-followthrough-governance existing stale worker bootstrap followthrough

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`
- source_branch: `feature/worker-launch-bootstrap-repair-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-worker-launch-bootstrap-repair`
- premerge_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-test-pre-merge-worker-launch-bootstrap-repair`

## Scope Verdict

- `PASS`: repair the same-owner launch seam where manager-selected worker worktrees already exist on disk but still lack managed tooling or `.freely/run` baseline state.
- `PASS`: keep the fix bounded to worker launch/bootstrap repair; do not widen task routing, ownership policy, or unrelated branch-only launch gating.
- `PENDING`: canonical `develop` replay still must prove the retained receipt-closeout worker actually launches from this repaired stale-existing-worktree shape and Freely continues to the next task after closeout.

## Current-Window Evidence

1. After `2026-04-24T22:53:16Z`, canonical daemon replay reached a narrower seam: manager selected `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-runtime-lifecycle-receipt-closeout-reconcile`, the directory existed, `.freely/config.env` existed, but `.freely/run` did not.
2. Runtime treated that half-bootstrap directory as an already-ready worker because `materialize_worker_prompt_worktree_if_needed()` only repaired missing directories and `ensure_runtime_workcell_initialized_for_launch()` returned early once config existed.
3. The selected lane remained `activity_state: idle`, proving the failure was stale-existing-worktree bootstrap rather than task discovery or worker prompt selection.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-repairs-existing-stale-worktree`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-materializes-missing-worktree`
3. `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`

## Implementation Decision Note

- decision: `Repair authoritative existing worker worktrees in place when launch sees config-only or tooling-incomplete bootstrap state, instead of trusting directory existence as launch-ready truth.`
- why_this: `The failing replay was no longer about missing worktree creation. Manager had already selected the correct retained lane, but launch treated a half-bootstrap directory as complete because config presence short-circuited the remaining tooling/runtime repair path.`
- alternatives_considered: `Keep repairing only missing directories; copy untracked runtime files through Git worktree creation; widen the fix into broader worker launch or ownership policy changes instead of repairing the proven bootstrap seam.`
- boundary_non_goals: `No task-routing redesign, no ownership-policy relaxation, no branch-only launch-gate fix, and no claim that canonical daemon looping is complete before protected replay lands and develop self-host replay proves next-task continuation.`
- residual_risk: `Canonical replay may still expose a later retained-lane closeout or retirement blocker after this worker launches, but stale existing worktrees should no longer stall delegation just because `.freely/config.env` exists ahead of `.freely/run` or managed tooling surfaces.`

## Implementation

- Added `worker_worktree_needs_managed_tooling_repair()` to detect half-bootstrap worktrees that still miss managed tooling artifacts.
- Added `repair_existing_worker_worktree_if_needed()` so `materialize_worker_prompt_worktree_if_needed()` repairs already-existing authoritative worktrees before treating them as launchable.
- Updated `ensure_runtime_workcell_initialized_for_launch()` to backfill baseline workcell state when config already exists but runtime baseline state does not.
- Updated `write_workcell_state()` to create the parent `.freely/run` directory before writing state files.
- Added focused regression `test-freely-manager-worker-launch-repairs-existing-stale-worktree`.

## Verification

### Feature lane

- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-repairs-existing-stale-worktree`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-materializes-missing-worktree`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`

### Protected replay

- `PASS`: merged `feature/worker-launch-bootstrap-repair-20260424` into `test-pre-merge-20260424-worker-launch-bootstrap-repair`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-repairs-existing-stale-worktree`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-materializes-missing-worktree`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`

## Adjacent Risk

- `KNOWN ADJACENT`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-branch-only-prompt` fails on both pristine `develop` and this worktree with `expected launch-time hard gate to block branch-only prompt, got 1 launched workers`; this pre-existing branch-only gating defect is outside the scope of the current repair.
