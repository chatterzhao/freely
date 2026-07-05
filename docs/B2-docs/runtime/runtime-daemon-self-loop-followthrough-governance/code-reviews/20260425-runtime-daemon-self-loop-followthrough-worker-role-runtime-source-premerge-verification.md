# Verification: runtime-daemon-self-loop-followthrough-governance worker role and runtime-source premerge followthrough

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-25`
- verifier: `codex`
- source_branch: `feature/runtime-target-worker-role-and-starting-stuck-recovery-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-runtime-target-worker-role-and-starting-stuck-recovery`
- protected_replay_branch: `test-pre-merge-runtime-target-worker-role-and-starting-stuck-recovery-20260425`
- protected_replay_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-test-pre-merge-runtime-target-worker-role-and-starting-stuck-recovery`
- protected_replay_merge_commit: `efcf195d`

## Scope Verdict

- `PASS`: the remaining autonomy blocker is still the manager/worker/runtime handoff contract, not agent naming. Runtime launches and resumes AI roles from machine-readable workcell state, worker verification contracts, worker exit contracts, and authoritative prompt artifacts.
- `PASS`: delegated targets now derive runtime role from worker truth before branch defaults, so `test-pre-merge-*` targets can stay worker-scoped when manager has already delegated them.
- `PASS`: delegated worker launch now follows the authoritative runtime source project, and control-plane reconcile clears stale dispatcher/watchdog residue that still points at an older runtime source.
- `PASS`: terminal worker handoff followthrough is now absorbed through the authoritative local followthrough prompt instead of leaving manager pinned behind stale launched-worker state.
- `PASS`: a fresh protected replay on `test-pre-merge-runtime-target-worker-role-and-starting-stuck-recovery-20260425` completed with the current fixset merged in and the focused guarded-lane regressions all passed:
  1. `bash docs/system/workspace/scripts/tests/test-freely-control-plane-pid-validation-prefers-authoritative-runtime-source`
  2. `bash docs/system/workspace/scripts/tests/test-freely-worker-control-plane-reconcile-clears-stale-runtime-source`
  3. `bash docs/system/workspace/scripts/tests/test-freely-start-workcell-supervisor-prefers-active-runtime-source`
  4. `bash docs/system/workspace/scripts/tests/test-freely-runtime-role-hint-prefers-worker-state-and-contract`
  5. `bash docs/system/workspace/scripts/tests/test-freely-worker-launchable-verification-contract-prefers-runtime-workspace-root`
  6. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-absorbs-terminal-handoff-followthrough`
  7. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-absorbs-stopped-terminal-handoff-followthrough`
  8. `bash docs/system/workspace/scripts/tests/test-start-lead-agent-worker-reentry-scope`
  9. `bash docs/system/workspace/scripts/tests/test-start-lead-agent-test-pre-merge-worker-reentry-scope`
  10. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-collapses-terminal-handoff-worker-slot`
  11. `bash docs/system/workspace/scripts/tests/test-freely-delegated-worker-starting-stuck-reclaim`
  12. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-authoritative-worker-consumes-prompt`
  13. `bash docs/system/workspace/scripts/tests/test-freely-runtime-effective-worker-role-from-contract`
  14. `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-worker-runtime-when-startup-truth-is-ready`
  15. `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
  16. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
  17. `bash docs/system/workspace/scripts/tests/test-freely-runtime-handoff-state-reconcile`
  18. `./bin/governance-check`
- `PENDING`: canonical `develop` still needs a post-merge self-host replay that proves the full loop closes one task, merges/cleans it up, retires the temporary worktree, and moves to the next task without manual intervention.

## Commands

1. `freely wt-create test-pre-merge-runtime-target-worker-role-and-starting-stuck-recovery-20260425 --base develop`
2. `freely pr-merge-guarded test-pre-merge-runtime-target-worker-role-and-starting-stuck-recovery-20260425 feature/runtime-target-worker-role-and-starting-stuck-recovery-20260424`
3. `bash docs/system/workspace/scripts/tests/test-freely-control-plane-pid-validation-prefers-authoritative-runtime-source`
4. `bash docs/system/workspace/scripts/tests/test-freely-worker-control-plane-reconcile-clears-stale-runtime-source`
5. `bash docs/system/workspace/scripts/tests/test-freely-start-workcell-supervisor-prefers-active-runtime-source`
6. `bash docs/system/workspace/scripts/tests/test-freely-runtime-role-hint-prefers-worker-state-and-contract`
7. `bash docs/system/workspace/scripts/tests/test-freely-worker-launchable-verification-contract-prefers-runtime-workspace-root`
8. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-absorbs-terminal-handoff-followthrough`
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-absorbs-stopped-terminal-handoff-followthrough`
10. `bash docs/system/workspace/scripts/tests/test-start-lead-agent-worker-reentry-scope`
11. `bash docs/system/workspace/scripts/tests/test-start-lead-agent-test-pre-merge-worker-reentry-scope`
12. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-collapses-terminal-handoff-worker-slot`
13. `bash docs/system/workspace/scripts/tests/test-freely-delegated-worker-starting-stuck-reclaim`
14. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-authoritative-worker-consumes-prompt`
15. `bash docs/system/workspace/scripts/tests/test-freely-runtime-effective-worker-role-from-contract`
16. `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-worker-runtime-when-startup-truth-is-ready`
17. `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
18. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
19. `bash docs/system/workspace/scripts/tests/test-freely-runtime-handoff-state-reconcile`
20. `./bin/governance-check`

## Implementation Decision Note

- decision: `Bind delegated worker continuation to authoritative runtime-source and worker-truth artifacts before branch heuristics, then let manager absorb terminal handoff followthrough from the local authoritative prompt.`
- why_this: `The observed blockage was not one broken shell line; it was a contract mismatch where runtime source, worker role, and handoff prompt truth could diverge across manager restarts. Restoring that contract closes the exact seam without inventing a new control-plane architecture first.`
- alternatives_considered: `Keep inferring worker role from branch names; keep delegated launch on the requested source project even when an active runtime source already owns the control plane; redesign immediately into a new multi-agent/A2A stack before proving the current runtime contract can close the loop.`
- boundary_non_goals: `No rename of manager/worker concepts, no new agent bus, and no claim that canonical develop acceptance is already complete before the develop-side daemon replay succeeds.`
- residual_risk: `The protected replay proves merge adequacy for this contract repair, but the canonical develop replay may still expose a later-stage manager judgment or cleanup-retirement seam after this blocker is removed.`
