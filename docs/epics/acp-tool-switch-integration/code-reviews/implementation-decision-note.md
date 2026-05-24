---
owner_issue: I-20260524T053214Z-A
issue_id: I-20260524T053214Z-A
---
## Implementation Decision Note

- issue_id: I-20260524T053214Z-A
- decision: 在 ACP 路径中接入 `tool_switch_events`，不引入新抽象。4 个集成断点 + 2 个兜底，全部在已有代码路径内，改动最小（118 行）。
- why_this: `tool_switch_events` 表是已实现的统一真相源，只需补齐 ACP 路径缺失的集成。`select_launch_kind()` 的 ACP 路径（commit `0e4923c1`）和 `_tool_switch_launch_kind()`（commit `ca422fed`）是两个独立提交，从未在同一代码路径中集成——ACP 的早期 return 使 `_ts_launch` 成为死代码。补齐集成即可，无需重写。
- alternatives_considered:
  - `重写 ACP session 管理 — 否决，改动过大，引入新 bug 风险`
  - `仅在 run-acp-prompt.py 兜底 — 不完整，上游 select_launch_kind() 仍拿错 session`
  - `清除 session-store 数据重新开始 — 治标，下次 bridge 重启仍复现`
- boundary_non_goals:
  - `不改变非 ACP（direct）路径`
  - `不改变 tool_switch_events 表结构`
  - `不改变 session-store.py 的公共 API 语义（只新增 tool_switch_update_session_id）`
  - `不改变 _tool_switch_launch_kind() 核心逻辑`
- residual_risk:
  - `claude-agent-acp 的 prompt 响应超时（如 ai98pro 代理 tool use 问题）可能导致单个 cycle 失败，已通过 prompt 模式 fallback 缓解——失败后自动 session/new 重试`
  - `run-acp-prompt.py send_prompt 仅在 prompt 模式失败时 fallback；fresh/resume 模式的失败由现有 try/except 覆盖`
