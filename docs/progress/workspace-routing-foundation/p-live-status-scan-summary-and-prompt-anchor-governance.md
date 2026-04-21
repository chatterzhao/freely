# Progress: live-status-scan-summary-and-prompt-anchor-governance

- issue_id: `I-20260421-1530-A`
- issue_path: `docs/epics/workspace-routing-foundation/live-status-scan-summary-and-prompt-anchor-governance/issues/live-status-scan-summary-and-prompt-anchor-governance.md`
- title: `Live-status scan summary and prompt anchor governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-status-fast-latest-artifact-lookup-20260421`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-runtime-status-fast-latest-artifact-lookup`
- updated_at: `2026-04-21`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- The first bounded implementation slice is now materialized: `live-status` keeps prompt anchors authoritative on current-state prompt surfaces and adds advisory scan-summary fields from `manager-task-source-scan-latest.json`.
- Focused regressions passed in the feature worktree and in the guarded `test-pre-merge-20260421-live-status-scan-summary` batch.
- The remaining work is guarded-develop completion plus develop-side replay/validation.

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-freely-live-status-includes-scan-summary`
2. `bash docs/system/workspace/scripts/tests/test-freely-live-status-prefers-session-state-prompt-anchor`
3. `bash docs/system/workspace/scripts/tests/test-freely-live-status`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
5. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-includes-milestone-patrol-seed`
6. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`
7. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-suppresses-broad-patrol-while-worker-active`
8. `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
10. `bash docs/system/workspace/scripts/tests/test-start-lead-agent-verification-metadata-contract`
11. `bash -n docs/system/workspace/scripts/runtime/freely`
12. `./bin/governance-check`

## Next Action

1. Re-run guarded completion on local `develop` after this owner chain is present in the merge diff.
2. Run develop-side validation for daemon-start/status/patrol behavior.
3. If develop replay exposes a regression, fix it on the retained worktree rather than deleting the lane.
