---
owner_issue: I-20260623T100903Z-A
owner_issue_path: docs/issues/I-20260623T100903Z-A/issue.md
---

# Implementation Decision Note: SSE 彻底实现

## decision
采用 5 阶段递进方案，从轮询迁移到 SSE 推送。Phase 2 双写过渡（SSE + 轮询并行）确保安全切换，Phase 3 在 SSE 稳定后删除 delivery_status。

## why_this
- A2A 官方协议用 SSE 作为标准通知机制，task state 终态 + stream close 是投递信号
- delivery_status 是手搓的 A2A 非标准字段，SSE 实现后没有存在理由
- 当前 5/6 问题（#3381 分析）直接或间接由 SSE 缺失导致
- 5 阶段递进最小化风险：每个阶段独立可测，双写过渡提供安全网

## alternatives_considered

**A: 一次性全切换（无过渡期）**
- 拒绝：风险过高。SSE 客户端是全新代码，直接替换轮询无法回退

**B: 只实现 SSE 客户端，保留 delivery_status**
- 拒绝：delivery_status 是 A2A 非标准字段，保留它增加维护负担和混淆

**C: 用 WebSocket 替代 SSE**
- 拒绝：A2A 官方协议规范用 SSE，WebSocket 不是标准路径

## boundary_non_goals
- 不实现内存优先架构（acp-a2a-refactor Phase A，10 pending tasks）
- 不实现 L0-L3 兜底检测（独立 issue）
- 不实现 CSV 清理（SSE 稳定后的后续工作）
- 不实现 Webhook push notification（A2A 协议的另一种通知方式，本 issue 范围外）

## residual_risk
- DB migration（删 delivery_status 列）不可逆——需 migration 脚本 + 回滚方案
- SSE 连接池泄漏——需心跳 + 超时 + 连接数上限
- 双写过渡期行为差异——runtime event 对比可及时发现
- 阶段 3 后无轮询 fallback——SSE 连接失败告警是唯一防线
