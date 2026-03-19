# Pre-Tests: token-efficient-session-continuity-and-rotation-governance

1. 只命中 `context warn` 且当前会话仍健康时，当前 AI 先更新 phase-appropriate continuity artifact，而不是立刻 rotate。
2. 命中 `context compacted`、`context_ratio >= rotate` 或 resume 质量退化时，runtime 触发 `fresh_with_handoff`，而不是要求 watchdog 做语义压缩。
3. 新会话默认消费 continuity artifact 与 handoff；`previous_tool_session_id`、`previous_tool_jsonl_path`、`previous_cycle_log` 只作为按需读取的证据路径。
4. manager continuity 与 worker continuity 的默认内容结构不同，前者面向 fleet supervision，后者面向 issue continuation。
5. 若未来 Codex 公开非交互压缩参数，Freely 的正式治理口径要求优先评估并改用官方能力。
