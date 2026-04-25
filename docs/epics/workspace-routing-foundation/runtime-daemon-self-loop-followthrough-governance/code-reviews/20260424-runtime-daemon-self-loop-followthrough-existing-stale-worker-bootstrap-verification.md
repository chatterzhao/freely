# Verification: runtime-daemon-self-loop-followthrough-governance existing stale worker bootstrap followthrough

- date: `2026-04-24`
- issue: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-worker-launch-bootstrap-repair`
- premerge_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-test-pre-merge-worker-launch-bootstrap-repair`

## Scope

- Repair the same-owner launch seam where manager-selected worker worktrees already exist on disk but still lack managed tooling or `.freely/run` baseline state.
- Keep the fix bounded to worker launch/bootstrap repair; do not widen task routing, ownership policy, or unrelated branch-only launch gating.

## Failure Observed

- Canonical daemon replay after the earlier missing-worktree materialization repair reached a narrower seam: manager selected `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-runtime-lifecycle-receipt-closeout-reconcile`, the directory existed, `.freely/config.env` existed, but `.freely/run` did not.
- Runtime treated that half-bootstrap directory as an already-ready worker because `materialize_worker_prompt_worktree_if_needed()` only repaired missing directories and `ensure_runtime_workcell_initialized_for_launch()` returned early once config existed.
- Result: the selected lane stayed `activity_state: idle` and manager could not materialize real worker runtime state for the retained receipt-closeout task.

## Decision

- If the authoritative target worktree already exists, manager launch must verify bootstrap surfaces rather than trusting directory existence alone.
- Missing managed tooling surfaces remain repairable via `sync-tooling --source-project <manager> --project <worktree>`.
- Missing runtime baseline state remains repairable in-place by writing baseline `workcell-state.env`; `.freely/run` should be created by the state writer instead of assuming some earlier bootstrap call created it.

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

## Residual Risk

- `PENDING`: guarded `develop` merge still requires the refreshed owner evidence to clear merge governance.
- `PENDING`: canonical daemon replay still must prove the real retained receipt-closeout worker launches from this repaired stale-existing-worktree shape and Freely continues to the next task after closeout.
- `KNOWN ADJACENT`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-branch-only-prompt` fails on both pristine `develop` and this worktree with `expected launch-time hard gate to block branch-only prompt, got 1 launched workers`; this pre-existing branch-only gating defect is outside the scope of the current repair.
