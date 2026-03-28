# Progress: watchdog-live-status-surface-and-manager-supervision

- issue_id: `I-20260320-1945`
- issue_path: `docs/epics/workspace-routing-foundation/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md`
- phase_state: `completed`
- summary: 修复 `live-status` 当前态 surface 中的陈旧字段冲突：当 project-owned AI 已活跃时，不再继续显示 `last_ai_state: down` / `last_exit_reason: starting`。
- current_focus:
  - none
- closure_status: `merged-pending-verify`
- closure_evidence:
  - `branch: feature/fix-last-ai-state-down-20260328-0745`
  - `worktree_path: /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260328-0745-feature-fix-last-ai-state-down`
  - `scope: read-only reconciliation in live-status output only`
  - `tests: bash docs/system/workspace/scripts/tests/test-freely-live-status; bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival; bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
  - `review: docs/epics/workspace-routing-foundation/watchdog-live-status-surface-and-manager-supervision/code-reviews/20260328-watchdog-live-status-surface-and-manager-supervision-reconciliation-verification.md`
