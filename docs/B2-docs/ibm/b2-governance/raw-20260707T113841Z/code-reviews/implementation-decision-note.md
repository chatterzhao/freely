# Implementation Decision Note
- issue_id: I-20260707T113841Z-A
- milestone: M-20260707T113841Z-A

- decision: 在现有 A2A/SSE/ACP 架构上补三层：提示词层(phase-definitions) + 指南层(review-guidelines) + 命令层(pr-create-guarded gate + agent_working review functions)
- why_this: 不推倒重建——复用已有 InputRequiredReason/A2A/SSE/agent_working。阶段指南独立注入。命令兜底硬拦截。
- alternatives_considered: Watchdog 扫描文件（不可靠，文件可伪造）；Worker 自行触发审查（已确认可跳过）；新表 review_signatures（多一张表，不选）
- boundary_non_goals: 不修改 A2A/SSE/ACP 基础设施；不改变 agent-table 结构；不修改 watchdog_sse.py 审查路由
- residual_risk: Worker 仍可跳过 A2A PATCH；跨模型强制当前 warning-only；agent_working.record_review 依赖 DB daemon RPC

## Decision
在现有 A2A/SSE/ACP 架构上补三层：提示词层(phase-definitions) + 指南层(review-guidelines) + 命令层(pr-create-guarded gate + agent_working review functions)

## Why This
1. 不推倒重建——复用现有 InputRequiredReason/A2A/SSE/agent_working
2. 阶段指南独立注入——同一 Reviewer agent，不同阶段不同指南
3. 命令兜底——Worker 跳过审查时，pr-create-guarded 硬拦截

## Alternatives Considered
- Watchdog 扫描文件检测阶段完成 → 不可靠（文件可伪造）
- Worker 自行触发审查 → 已确认不可靠（可跳过）

## Boundary Non-Goals
- 不修改 A2A/SSE/ACP 基础设施
- 不改变 agent-table 结构
- 不修改 watchdog_sse.py 审查路由

## Residual Risk
- Worker 仍可跳过 A2A PATCH（提示词层不是硬约束）
- 跨模型强制当前为 warning-only（agent-table slot 配置可改）
- agent_working.record_review 依赖 DB daemon RPC（daemon 不可用时降级）
