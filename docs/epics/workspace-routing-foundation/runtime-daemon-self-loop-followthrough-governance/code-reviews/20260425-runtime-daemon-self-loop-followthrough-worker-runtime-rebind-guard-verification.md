# Verification: runtime-daemon-self-loop-followthrough worker runtime rebind guard

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-25`
- verifier: `codex`
- source_branch: `feature/runtime-target-worker-role-and-starting-stuck-recovery-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-runtime-target-worker-role-and-starting-stuck-recovery`

## Scope Verdict

- `PASS`: canonical `develop` observation already proved manager can now emit real worker delegation artifacts and workers can write followthrough evidence; the remaining blocker moved to runtime control-plane followthrough, not prompt generation or role labelling.
- `PASS`: `worker_runtime_control_plane_needs_manager_source_rebind()` now checks the live worker supervisor/AI process runtime source before falling back to runtime-script file comparison. If the active worker is already running from the authoritative delegated manager source, manager no longer tears it down and relaunches the same lane.
- `PASS`: `manager_semantic_loop_active_worker_count_for_project()` now trusts live process discovery whenever process inspection is available, so stale launch-state hints no longer pin `active_running_worker_count` above reality and suppress downstream followthrough.
- `PASS`: focused regressions passed for both the positive and negative rebind branches plus the stale-count seam:
  1. `bash docs/system/workspace/scripts/tests/test-freely-worker-launch-skips-rebind-when-active-runtime-already-uses-manager-source`
  2. `bash docs/system/workspace/scripts/tests/test-freely-worker-launch-rebinds-stale-active-runtime-control-plane`
  3. `bash docs/system/workspace/scripts/tests/test-freely-manager-active-worker-count-prefers-live-processes`
  4. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
  5. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-collapses-terminal-handoff-worker-slot`
- `PENDING`: replay the guarded merge path, absorb into canonical `develop`, restart `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`, and verify the same worker lane no longer loops through `manager_worker_runtime_control_plane_rebind -> delegated_runtime_handoff_stop_requested` while the daemon continues toward merge/retire/next-task followthrough.

## Implementation Decision Note

- decision: `Keep manager/worker roles runtime-artifact-driven and narrow this repair to control-plane source authority plus live worker-count truth.`
- why_this: `The field evidence shows runtime already has the correct delegation artifact chain: manager writes continuity/prompt/exit-contract truth, runtime launches the delegated lane, and the worker performs real edits. The new blocker was that runtime ignored its own live-process authority and re-opened the lane based on versioned-file drift that sync-tooling does not normalize.`
- alternatives_considered: `Rework roles around prompt labels only; redesign into a different agent taxonomy before fixing the loop; keep using max(live,hint) and try to damp the symptom elsewhere.`
- boundary_non_goals: `No new role taxonomy, no supervisor/worker prompt contract rewrite, and no claim that canonical develop autonomous looping is already complete before real daemon replay succeeds.`
- residual_risk: `Canonical develop may still expose another bounded followthrough seam after this rebind loop is removed, but repeated worker stop/restart churn and stale active-worker-count inflation are now covered by explicit regressions and should no longer mask the next real blocker.`
