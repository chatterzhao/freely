# Brainstorm: token-efficient-session-continuity-and-rotation-governance

## Focus

把 session continuity 从零散的 `context warn`、`fresh_with_handoff`、watchdog 恢复提示，收敛成同一条正式控制面口径。

## Key Decisions

1. `context warn` 由当前健康会话先更新 phase-appropriate continuity artifact，不立刻 rotate。
2. `context rotate`、`context compacted`、resume 退化属于 runtime 的 `fresh_with_handoff` 触发面，不由 watchdog 代替 AI 做语义压缩。
3. manager continuity 与 worker continuity 必须分开定义：前者以 fleet / delegation 为中心，后者以 issue / phase 为中心。
4. `previous_tool_session_id`、`previous_tool_jsonl_path`、`previous_cycle_log` 是 fallback evidence refs，不是默认 prompt payload。
5. 若未来官方公开非交互压缩能力，Freely 的正式口径应优先评估并改用官方路径，而不是长期固化外部 handoff fallback。

## Open Checks

1. 现有 `continuity-watchdog`、`watchdog-control-plane` 与 `recovery-subagent-governance` 的 owner boundary 是否已经完全一致。
2. 当前 issue 文档是否已足够驱动后续 runtime / skill / prompt 实现，而不需要继续留在 `in_ibm`。
