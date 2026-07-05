# Progress: manager-task-source-scan-idle-replan-boundary-governance

- issue_id: `I-20260420-1130-A`
- issue_path: `docs/epics/workspace-routing-foundation/manager-task-source-scan-idle-replan-boundary-governance/issues/manager-task-source-scan-idle-replan-boundary-governance.md`
- title: `Manager task-source scan idle/replan boundary governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/startup-task-source-patrol-and-reconcile-20260420`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-startup-task-source-patrol-and-reconcile`
- updated_at: `2026-04-20`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- The bounded runtime/doc/test slice for idle/replan patrol scan is already materialized in the startup/patrol feature lane and absorbed by the authoritative `test-pre-merge-20260420-autonomous-task-governance` batch.
- Live self-host replay proved the product-level success standard behind this owner: startup manager rounds can find work autonomously, broad patrol is suppressed while an active worker remains authoritative, and idle followthrough regenerates patrol scan only after continuity advances without an active worker.
- The remaining work is governance-only closeout: bind the already-landed implementation to this owner chain so guarded develop promote no longer carries candidate-only truth.

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-includes-milestone-patrol-seed`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-suppresses-broad-patrol-while-worker-active`
4. `bash docs/system/workspace/scripts/tests/test-freely-manager-task-source-scan-ignores-pre-stop-continuity-anchor`
5. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-provider-hints`
6. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-python-compat`
7. `bash docs/system/workspace/scripts/tests/test-start-lead-agent-verification-metadata-contract`
8. `bash -n docs/system/workspace/scripts/runtime/freely`
9. `./bin/governance-check`
10. `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-external-issue-source-lifecycle-governance/.freely/run/worker-continuity-20260420-200317-external-issue-verification-closeout.md`
11. `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-external-issue-source-lifecycle-governance/.freely/logs/runtime-events.log`
12. `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-test-pre-merge-autonomous-task-governance/.freely/logs/runtime-events.log`

## Next Action

1. Merge this closeout writeback into `test-pre-merge-20260420-autonomous-task-governance`.
2. Replay `freely pr-merge-guarded develop test-pre-merge-20260420-autonomous-task-governance`.
3. Run `freely pr-merge-guarded complete develop test-pre-merge-20260420-autonomous-task-governance`.
4. Retire the temporary feature and test-pre-merge worktrees once canonical develop absorbs the owner chain.
