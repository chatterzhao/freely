# Verification: runtime-daemon-self-loop-followthrough-governance terminal handoff followthrough absorb

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-25`
- verifier: `codex`
- source_branch: `feature/runtime-terminal-handoff-followthrough-relaunch-guard`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-runtime-terminal-handoff-followthrough-relaunch-guard`

## Scope Verdict

- `PASS`: this continuation stays inside `I-20260421-1200-A`. The failure is still in the runtime control plane that consumes manager/worker artifacts, not in scan policy, agent taxonomy, or a new orchestration protocol.
- `FAIL`: real canonical `develop` replay had already advanced past worker-role confusion, stale `starting`, terminal-slot collapse, and finalize grace, but runtime still failed one narrower same-lane handoff seam. Manager wrote a newer authoritative followthrough prompt for the delegated target, yet that target still carried an older terminal `worker-exit-contract.env` with `EXIT_KIND="worker_handoff_needed"`. `manager_runtime_launch_workers_from_latest_handoff()` saw the stale terminal contract first and skipped relaunch, so the new followthrough prompt was never launched.
- `PASS`: the fix is narrow and same-owner. When the target lane's terminal exit contract is `worker_handoff_needed`, manager launch now absorbs that handoff into the current authoritative followthrough, clears the stale terminal exit contract after successful relaunch, records `worker_exit_contract_handoff_absorbed`, and refreshes launch bookkeeping so the lane can continue its manager->worker->manager closeout chain.
- `PASS`: focused `feature-local` verification passed for the exact seam and adjacent recovery path:
  1. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-workers-absorbs-terminal-handoff-followthrough`
  2. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-absorbs-terminal-handoff-followthrough`
  3. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-collapses-terminal-handoff-worker-slot`
- `PENDING`: canonical `develop` acceptance remains open until this owner evidence is lawfully promoted, `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely` is replayed from merged `develop`, and live runtime evidence proves the retained lane now continues through review/cleanup/retirement and then advances to another task.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-workers-absorbs-terminal-handoff-followthrough`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-absorbs-terminal-handoff-followthrough`
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-collapses-terminal-handoff-worker-slot`

## Implementation Decision Note

- decision: `Teach manager launch to absorb stale terminal worker_handoff_needed truth only when a newer authoritative followthrough prompt for the same lane already exists.`
- why_this: `The real failure was consumption order inside the runtime middleman. Terminal exit truth correctly proved the old round had ended, but it should not outrank the new authoritative followthrough prompt that manager had already written for the same worker lane. Absorbing that specific handoff preserves artifact-driven control while letting the lane continue.`
- alternatives_considered: `Ignore all terminal worker contracts during launch; redesign manager/worker handoff around a new agent registry; force manager to delete old contracts before writing any new followthrough prompt.`
- boundary_non_goals: `No scan redesign, no new supervisor taxonomy, and no claim that the full autonomous loop is done before merged-develop replay proves select -> finish -> merge upward -> retire -> next task.`
- residual_risk: `This only closes the stale terminal-handoff suppression seam. Canonical `develop` may still expose a later bounded closeout, merge, or retirement blocker before Freely reaches the full success standard.`
