# Implementation Decision Note

## decision

采用“新模块 + additive 表 + 最小接线”：`discussion_events.py` 负责事件归一化/准入/存储；`handoff_store.py` 负责 Task/Handoff/Message 与 owner；`agent_working.py` 只修 new/fork 发 message；Reviewer 统一 `a2a-exit --summary <json>`。

## why_this

- 现有 `a2a_tasks` 单行无法承载 message/artifact/owner；直接改它会破坏旧查询。
- 新表 append-only + 双写兼容，能渐进迁移，不需要一次性重写 A2A。
- 事件与 handoff 分开，C-F/C-B 可独立 GREEN，减少耦合。
- 不碰 `freely` 20K 行单体，符合文件规模约束。

## alternatives_considered

- 直接重写 `a2a_tasks`：风险高、迁移不可逆、旧 SSE/查询全断。
- 引入完整 A2A RPC：超出主意图，且当前不需要跨组织。
- webhook Source：需要公网/签名/重放，先用轮询 + event_id。
- DSH 插件承载：C-E 未 promote，且不是当前优先级。

## boundary_non_goals

- 不做 UI、IM/Feishu、事件溯源、Mandate、完整 A2A。
- 不做 Reviewer 自动修复；只统一 verdict 契约。
- 不做 Gitee PR review/CI（不支持时返回 unsupported）。

## residual_risk

- 双写期间新旧表可能不一致；新表为写权威，旧表 best-effort + 日志。
- 角色 prompt 只随 message 注入，不是 preset；后续 C-D 再收敛。
- Reviewer summary JSON 解析失败需 fallback；E2E 覆盖。
- 真实平台字段缺失（actor/id）只能 observe。
