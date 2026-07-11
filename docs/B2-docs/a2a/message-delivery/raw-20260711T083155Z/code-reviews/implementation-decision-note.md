# Implementation Decision Note: A2A→SSE→ACP 消息投递链 + SQLite 友好校验

- issue_id: I-20260711T083155Z-A

## Decision
在 A2A Server、freely_db_manager、watchdog_sse、a2a_task 四组件中增加消息投递链和 SQLite 友好校验层。

## Why This
- 当前 Manager→Worker 消息投递完全断裂: A2A Server 存消息但不发 SSE，watchdog 不处理 message_added 事件，消息静默丢失
- SQLite 无校验: AI 写空 content/非法 role/不存在 task 时全部静默成功，agent 不知道错在哪
- 友好校验让 AI 能自我纠正: 不是重试同样的错误数据，而是看到 fix_hint 后重新组织正确的数据再写入

## Alternatives Considered
- 仅加 SSE + watchdog 不做校验: 投递链通了但 AI 写错时仍然静默失败
- 在 API 层做校验而非 SQLite 层: API 层校验容易被绕过（直接 RPC 调用绕过 HTTP API），SQLite 层是最后防线

## Boundary / Non-Goals
- 不改 A2A SDK 协议本身
- 不改变现有 agent_working 表结构
- 不增加新的持久化存储
- 不保证消息 exactly-once（SSE at-most-once）

## Residual Risk
- SSE 连接断开期间的消息可能丢失（需后续增加消息队列或重放机制）
- ACP bridge 不在线时投递失败（已有 liveness check 兜底）
