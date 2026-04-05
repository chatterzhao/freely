# Progress: manager-semantic-loop-active-worker-suppression-governance

- issue_id: `I-20260405-1505-A`
- title: Manager semantic-loop active-worker suppression governance
- phase_state: `completed`
- runtime_state: `closed_for_this_batch`
- branch: `feature/manager-semantic-loop-active-worker-detection-followup-20260405-0505`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-0505-feature-manager-semantic-loop-active-worker-detection-followup`
- issue_path: `docs/epics/workspace-routing-foundation/manager-semantic-loop-active-worker-suppression-governance/issues/manager-semantic-loop-active-worker-suppression-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}
- summary: Canonical `develop` still carried a false-positive semantic-loop surface after the 2026-04-04 missing-run-dir guard. This follow-on owner keeps `I-20260322-0445` closed, materializes the active-worker suppression gap as a new lifecycle, and restores conservative behavior by letting semantic-loop suppression honor either current active PID discovery or the runtime launch-state active-worker hint.
- verification:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
  - `./bin/governance-check`

## 2026-04-05 Active Worker Suppression Follow-On

- Canonical evidence:
  - `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260404-latest-manager-continuity-worker-consumption-missing-run-dir-guard-verification.md` already recorded that the semantic-loop regression still failed on both the branch and unchanged `develop`.
  - replaying `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface` on this lane reproduced the same active-worker assertion failure before the patch.
- Repair:
  - keep `I-20260322-0445` completed; do not reopen it
  - add a bounded semantic-loop helper that takes the maximum of currently discoverable active worker lanes and the persisted launch-state `ACTIVE_RUNNING_WORKER_COUNT`
  - use that helper only to suppress semantic-loop suspicion when active worker truth already exists
- Result:
  - semantic-loop monitoring remains conservative for zero-worker loop suspicion
  - active worker execution no longer coexists with the `manager_continuity_rewrite_without_state_advance` signal
