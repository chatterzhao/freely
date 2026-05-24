# Implementation Decision Note — I-20260524T053214Z-A

- **decision**: 在 ACP 路径中接入 `tool_switch_events`，不引入新抽象
- **why_this**: `tool_switch_events` 表是已实现的统一真相源，只需补齐 ACP 路径的 4 个集成断点。改动最小（118 行），全部在已有代码路径内
- **alternatives_considered**:
  1. 重写 ACP session 管理 — 否决，过大，引入新 bug 风险
  2. 仅在 run-acp-prompt.py 兜底 — 不完整，上游仍拿错 session
  3. 清除 session-store 数据 — 治标，下次 bridge 重启仍复现
- **boundary_non_goals**: 不改变非 ACP 路径、`tool_switch_events` 表结构、session-store API 语义
- **residual_risk**: `claude-agent-acp` 的 prompt 响应超时（如 ai98pro 代理 tool use 问题）可能导致单个 cycle 失败，但已通过 prompt 模式 fallback 缓解——失败后自动 `session/new` 重试
