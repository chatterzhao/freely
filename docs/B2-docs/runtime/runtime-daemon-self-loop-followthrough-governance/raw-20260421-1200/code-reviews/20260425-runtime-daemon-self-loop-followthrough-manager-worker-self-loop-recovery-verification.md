# Verification: runtime-daemon-self-loop-followthrough-governance manager/worker self-loop recovery

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-25`
- verifier: `codex`
- source_branch: `feature/runtime-target-worker-role-and-starting-stuck-recovery-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-runtime-target-worker-role-and-starting-stuck-recovery`
- protected_replay_branch: `test-pre-merge-runtime-lifecycle-followthrough-20260424`
- protected_replay_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-test-pre-merge-runtime-lifecycle-followthrough`

## Scope Verdict

- `PASS`: the repair closes the exact handoff seam exposed by canonical `develop` dogfooding. Manager/worker role is assigned operationally by runtime consumption of machine-readable delegation artifacts, not by a free-text prompt label or a static branch-name role hint. Manager writes delegation/continuity artifacts, runtime consumes those artifacts to launch the next AI, and worker/manager exit contracts drive the next control-plane decision.
- `PASS`: delegated targets now derive their effective runtime role from authoritative worker verification-contract truth, which prevents `test-pre-merge-*` or other manager-default worktrees from re-entering manager-mode control planes after manager delegation.
- `PASS`: delegated targets that remain `starting` beyond startup grace without valid `ai.pid` are reclaimed, stale launched-worker slots are released on the dispatch-critical path, terminal worker truth is preserved through cleanup, and manager remains alive while runtime is still waiting for between-round or active-worker followthrough to resolve.
- `PASS`: focused feature-local regressions passed for this owner seam, including the autonomous existing-worktree loop proof:
  1. `bash docs/system/workspace/scripts/tests/test-freely-daemon-autonomous-existing-worktree-review-merge-retire-next-task-loop`
  2. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
  3. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-malformed-verification-contract`
  4. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-without-verification-contract`
  5. `bash docs/system/workspace/scripts/tests/test-freely-worker-active-stall-recovery-from-manager-watchdog`
  6. `bash docs/system/workspace/scripts/tests/test-freely-delegated-worker-starting-stuck-reclaim`
  7. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-reclaims-stale-starting-worker-slot`
  8. `bash docs/system/workspace/scripts/tests/test-freely-runtime-effective-worker-role-from-contract`
  9. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-between-rounds-relaunch-grace`
  10. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-while-worker-active`
- `PASS`: the same implementation already survived one protected replay as merge commit `08129972ab13aa9672521f1167feba279a32ec66` on `test-pre-merge-runtime-lifecycle-followthrough-20260424`, and these protected-lane checks passed there:
  1. `bash docs/system/workspace/scripts/tests/test-freely-runtime-effective-worker-role-from-contract`
  2. `bash docs/system/workspace/scripts/tests/test-freely-delegated-worker-starting-stuck-reclaim`
- `PENDING`: rerun protected replay with the owner-linked lifecycle materialization now in diff, merge into canonical `develop`, then verify real `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely` completes one full select -> finish -> merge/retire -> next-task loop without manual intervention.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-daemon-autonomous-existing-worktree-review-merge-retire-next-task-loop`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-malformed-verification-contract`
4. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-without-verification-contract`
5. `bash docs/system/workspace/scripts/tests/test-freely-worker-active-stall-recovery-from-manager-watchdog`
6. `bash docs/system/workspace/scripts/tests/test-freely-delegated-worker-starting-stuck-reclaim`
7. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-reclaims-stale-starting-worker-slot`
8. `bash docs/system/workspace/scripts/tests/test-freely-runtime-effective-worker-role-from-contract`
9. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-between-rounds-relaunch-grace`
10. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-while-worker-active`
11. `freely pr-merge-guarded test-pre-merge-runtime-lifecycle-followthrough-20260424 feature/runtime-target-worker-role-and-starting-stuck-recovery-20260424`
12. `bash docs/system/workspace/scripts/tests/test-freely-runtime-effective-worker-role-from-contract`
13. `bash docs/system/workspace/scripts/tests/test-freely-delegated-worker-starting-stuck-reclaim`

## Implementation Decision Note

- decision: `Absorb the manager/worker self-loop recovery into I-20260421-1200-A instead of materializing a new owner.`
- why_this: `The blocker sits on the same canonical daemon self-loop acceptance path. Splitting ownership would leave develop promotion blocked on missing owner evidence even though the repaired seam is still just manager/worker/runtime followthrough for the same autonomous loop.`
- alternatives_considered: `Keep C-20260424-2230-A as a new owner; merge candidate-only evidence into develop anyway; redesign roles around agent/skill naming instead of runtime artifact consumption.`
- boundary_non_goals: `No new role taxonomy, no agent/skill redesign, no exit-contract kind expansion, and no claim that canonical develop acceptance is complete before the real daemon loop closes and advances.`
- residual_risk: `Protected replay may still expose another bounded same-owner seam before canonical develop reaches full unattended looping, but the ownership chain for this repair is now explicit and merge-governed.`
