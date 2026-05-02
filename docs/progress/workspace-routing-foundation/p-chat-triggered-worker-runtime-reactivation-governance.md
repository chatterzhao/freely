# Progress: chat-triggered-worker-runtime-reactivation-governance

- issue_id: `I-20260321-1706`
- title: Chat-triggered worker runtime reactivation governance
- phase_state: `completed`
- runtime_state: `closed_for_this_batch`
- branch: `feature/codex-session-reentry-and-pty-input-20260321`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260321-feature-codex-session-reentry-and-pty-input`
- issue_path: `docs/epics/workspace-routing-foundation/chat-triggered-worker-runtime-reactivation-governance/issues/chat-triggered-worker-runtime-reactivation-governance.md`

## Summary

- 真实狗粮发现：stopped worker + `freely chat` 会产生 delegated intake，但不会自动拉起 worker 主循环。
- 当前已完成 runtime materialization，worker-local delegated continuation / verification handoff 会在 `operator_stop` 后触发 reactivation preflight。
- 已补最小脚本验证：stopped worker 会被重新拉起；`auth_failure` 不会被误重启。
- 真实狗粮回归已通过：`freely stop -> freely chat -> freely live-status` 观察到 worker supervisor/AI 被重新拉起，状态从停止恢复为 `ai_active`。
- 当前批次已完成；后续若再出现新的 re-entry 语义缺口，应新开生命周期承接。
