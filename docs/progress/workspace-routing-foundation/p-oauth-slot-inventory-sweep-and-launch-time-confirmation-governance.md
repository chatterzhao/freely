# Progress: oauth-slot-inventory-sweep-and-launch-time-confirmation-governance

- issue_id: `I-20260327-1115`
- title: OAuth slot inventory sweep and launch-time confirmation governance
- phase_state: `in_dev`
- runtime_state: `stopped`
- branch: `feature/oauth-api-usage-query`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-oauth-api-usage-query`
- issue_path: `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "dev-loop-initial-slice"}

## Summary

- 2026-03-27 这条 follow-on issue 已从 pre-brainstorm materialize 进入 dev-loop。当前第一刀不是一次性重写全部 watchdog contract，而是先把 OAuth `wham/usage` full sweep 接成新的 inventory truth slice：
  - `availability-watchdog.sh` 增加 OAuth slot sweep、availability cache writeback 与 cooldown overwrite
  - `freely ai switch codex auto` 优先走 OAuth sweep，保留 legacy real-probe fallback
  - `freely ai status` 开始展示 availability cache 摘要，避免 status 面继续完全不知道 inventory sweep 结果
- 当前仍未完成的后续切口：
  - `ensure_codex_slot_ready_for_manager()` 与 watchdog hold/wake 路径仍需进一步围绕 cache / launch-time confirmation 收紧
  - focused regressions 还需补上 OAuth sweep 不触碰活跃 auth、cooldown overwrite 与 fallback 邻接面

## Verification

- `./bin/governance-check`
