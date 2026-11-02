- issue_id: I-20261101T140415Z-A
- issue_path: docs/B2-docs/a2a/handoff/raw-20261101T140415Z/issues/I-20261101T140415Z-A.md

## Implementation Decision Note

- decision: 采用“最小修复 + 三态存活判定”：给 `_do_new` 补 `message` 参数并统一首条消息发送，把 `_check_agent_liveness` 的 `pgrep` 换成 ACP `session/ping` 三态；新增 `test-handoff-runtime.py` 覆盖两条路径。持久 outbox 与信封留给 C-B。
- why_this: `_do_new` 的 `NameError` 是跨工具交接的必现异常，且被 `watchdog_run` 吞成一次 SSE 重连，导致交接静默丢失；`pgrep` 判活误杀健康会话又把交接推入同一路径。两处改动小、可单测、能立即降低交接失败率，是后续协议的前置。
- alternatives_considered:
  - 直接做 outbox：能根治，但需要新表、状态机、消费循环与迁移，超出本切片，且没有 P0 修复时端到端测试不稳定。
  - 保留 `pgrep` 只修 NameError：能减少异常，但假 DEAD 仍会清绑定，问题只解决一半。
  - 用 `session/resume` 代替 ping：resume 有副作用（会重建会话），不适合只读判活。
- boundary_non_goals: 不改 A2A 状态枚举、CLI 参数、`agent-table` 语义、SSE 传输形态；不实现 outbox/信封/owner；不重命名 `worker_NN`。
- residual_risk:
  - 旧版 ACP bridge 若未实现 `session/ping`，会被判 unknown（不清绑定），可能延迟恢复；这是有意 fail-open 到“人工/恢复流程”。
  - `_do_new` 的参数变更需要所有调用点同步，遗漏会在运行期暴露；测试只覆盖 `acp_session_connect` 两个入口。
  - 本修复不解决“同一 raw 消息落到不同席位”，该问题由 C-B 的 assignment/owner 设计处理。
