---
name: A2A vs Handoff IDN
owner_issue: I-20260612T000223Z-A
owner_issue_path: docs/issues/I-20260612T000223Z-A/issue.md
implementation_decision_note: true
phase_state: completed
review_id: a2a-vs-handoff-idn
---

# Implementation Decision Note: A2A 协议替换 Freely Handoff

## Decision

**采用 A2A 协议彻底替换 Freely 私有 Handoff 机制**

## Why This

### 根因分析

Freely 自举开发中暴露大量 `launch_failed, launchable check failed`：

```
grep "launch_failed" .freely/freely.db:
大量 launch_failed, launchable check failed

根因：Manager 不知道 Worker 需要什么能力
→ 盲目委派
→ launchable check 失败
→ Worker 未启动
→ scan 列表停摆
```

### 为什么选择 A2A

1. **标准化**: Linux 基金会 AI Agents 工作组发布，业界认可
2. **能力发现**: Agent Card 解决 launchable check 问题
3. **状态机完善**: 8 种状态覆盖完整生命周期
4. **实时通信**: SSE 推送替换轮询
5. **生态互操作**: 可与外部 Agent 系统互通

### 为什么不是其他方案

- **MCP**: 用于 Agent 与工具交互，不适合 Agent 间通信
- **直接 API**: 需要自己维护协议，增加维护成本
- **保持现状**: 私有协议持续维护，无法与外部生态互通

## Alternatives Considered

### 方案 A: A2A 彻底替换 (选中)

- 优点: 标准化、生态互操作、解决根因
- 缺点: 改动较大

### 方案 B: Handoff + Agent Card 混合

- 优点: 改动小、风险低
- 缺点: 仍是私有协议、不完整

### 方案 C: 保持现状

- 优点: 无架构风险
- 缺点: 持续维护私有协议、无法与外部生态互通

## Boundary & Non-Goals

### In Scope

- A2A Server/Client 实现
- Freely Agent Card 扩展
- exit_kind → A2A Task 状态映射
- SSE 实时推送

### Out of Scope

- MCP 集成（独立项目）
- 外部 Agent 注册表（Phase 4）
- 多语言 SDK（独立项目）

### Non-Goals

- 不破坏现有 handoff 兼容（Phase 2 fallback）
- 不修改 Manager-Worker 职责边界
- 不改变现有 worktree 模型

## Residual Risk

| 风险 | 缓解措施 | 残余风险 |
|------|----------|----------|
| 同实例紧耦合 | 使用 Unix Domain Socket | 低 |
| 状态映射丢失 | 保留完整映射表 | 低 |
| 性能下降 | 基准测试监控 | 中 |
| 外部 Agent 不兼容 | 提供 adapter 层 | 中 |
| A2A 协议变更 | 锁定版本，定期更新 | 中 |

## Implementation Notes

### 渐进式迁移

1. Phase 1-2: A2A 与 Handoff 并存，Handoff 作为 fallback
2. Phase 3: 数据迁移，验证后删除旧逻辑
3. Phase 4: 增强功能，外部互操作

### 关键决策点

- 使用 Unix Domain Socket 而非 HTTP（性能考虑）
- 保留 Handoff fallback 直到 A2A 完全验证
- 锁定 A2A 版本避免协议变更风险

## Status

- **Date**: 2026-06-12
- **Status**: Proposed
- **Reviewers**: 待定
