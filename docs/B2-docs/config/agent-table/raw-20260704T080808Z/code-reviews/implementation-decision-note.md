---
issue_id: I-20260704T080808Z-A
issue_path: docs/B2-docs/config/agent-table/raw-20260704T080808Z/issues/I-20260704T080808Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260704T080808Z-A
- issue_path: docs/B2-docs/config/agent-table/raw-20260704T080808Z/issues/I-20260704T080808Z-A.md

## Implementation Decision Note

- decision: |
  启用上期预留的 base_tool 参数。socket/pid 加 `-{base_tool}` 后缀。
  daemon start 扫描 agent-table 所有 slot → 提取唯一 base_tool → 逐个启 bridge。
  base_tool 不可解析 → 硬报错 exit。
  _stop_acp_bridge 参数化，切号时只停当前 tool。

- why_this: |
  最小改动方案——上期已将 base_tool 参数穿透到所有调用点，本期只需启用。
  不需要改 session 层或 agent 层代码。

- alternatives_considered: |
  1. 动态启动 bridge（按需而非预启动）：首次 session 操作时才启动 → 增加 session 延迟
  2. 共用 socket 不同 namespace：ACP 协议不支持

- boundary_non_goals: |
  - 不修改 acp_session_connect 决策树
  - 不修改 watchdog handler
  - 不修改 agent-table 结构

- residual_risk: |
  - 多 bridge 进程增加内存占用 (每个 ~50MB)
  - agent-table 只有一个 base_tool 时行为与单 bridge 完全一致 (向后兼容)
  - 旧 socket 文件清理: 首次多 bridge 启动后旧格式 socket 成为 orphan → 加 startup 清理
