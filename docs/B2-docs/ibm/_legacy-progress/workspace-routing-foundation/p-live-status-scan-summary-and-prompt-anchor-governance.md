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
- The follow-on runtime repair in commit `db4178c1` keeps continuity fallback lawful: once continuity search crosses the latest explicit operator stop boundary it stops, while stale runtime-worktree refs still fall back to older launchable continuity in the same post-stop era.
- The next follow-on runtime repair keeps `ensure-manager` from misclassifying an active startup as idle: when the current supervisor is still in lifecycle checkpoints `L020/L021/L022`, watchdog recovery now treats prompt build / startup stub work as in-flight instead of killing the supervisor before `ai_launch_begin`.
- Focused regressions passed in the feature worktree and in the guarded `test-pre-merge-20260421-live-status-scan-summary` batch after that repair.
- Canonical `develop` replay is still open: prompt build no longer fails early, but the stricter user success bar now requires proving `daemon start` proceeds into real scan-driven task selection and standards-compliant Freely execution.

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-freely-live-status-includes-scan-summary`
2. `bash docs/system/workspace/scripts/tests/test-freely-live-status-prefers-session-state-prompt-anchor`
3. `bash docs/system/workspace/scripts/tests/test-freely-live-status`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
5. `bash -n docs/system/workspace/scripts/runtime/freely`
6. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-prompt-build`
7. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-does-not-double-launch-during-degraded-starting-grace`
8. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-waits-for-supervisor-teardown-before-fallback`
9. `./bin/governance-check`

## Next Action

1. Carry the updated owner chain through guarded merge into `develop`.
2. Run canonical `daemon start` on `develop` until there is direct evidence of scan consumption, task selection, and standards-compliant Freely execution rather than only successful prompt build.
3. Keep the dedicated feature worktree retained after merge in case later runtime-ops followthrough wants a narrower fix.
