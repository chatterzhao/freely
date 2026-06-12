---
name: A2A 协议替换 Handoff 实现决策
owner_issue: I-20260612T000223Z-A
owner_issue_path: docs/issues/I-20260612T000223Z-A/issue.md
phase_state: in_dev
---

# Implementation Decision Note: A2A 协议替换 Handoff

- **issue_id**: I-20260612T000223Z-A
- **phase**: dev-loop
- **date**: 2026-06-12
- **decision_maker**: Claude Fable 5
- **context**: Freely Manager-Worker 通信机制重构

## 决策

**采用 A2A 协议作为 Freely Manager-Worker 通信协议，保留 Handoff 作为向后兼容 fallback。**

## 背景

Freely 当前使用私有 Handoff 机制进行 Manager-Worker 通信：
- 通过 SQLite handoffs 表存储状态
- 通过 Unix Domain Socket 与 daemon 通信
- AI 输出 JSON 格式 handoff，Runtime 解析并写入 DB

问题：
1. Handoff 机制是私有协议，缺乏标准化
2. 与外部 Agent 互操作性差
3. 状态管理分散在多个地方

## 替代方案

### 方案 A: A2A 协议 (选中)

| 优点 | 缺点 |
|------|------|
| 开放标准，生态丰富 | 需要适配 Freely 扩展 |
| 原生支持 Task 状态机 | 初期实现复杂度高 |
| 外部 Agent 互操作 | 迁移成本 |

### 方案 B: 保留 Handoff

| 优点 | 缺点 |
|------|------|
| 现有实现可复用 | 私有协议，缺乏标准化 |
| 迁移成本低 | 外部 Agent 无法接入 |
| 稳定可靠 | 长期技术债务 |

### 方案 C: MCP for Agents

| 优点 | 缺点 |
|------|------|
| 工具调用友好 | 不适合 Agent 间对话 |
| Anthropic 支持 | 需要额外状态管理 |

## 决策理由

1. **标准化**: A2A 是 Linux Foundation AI Agents 工作组发布的开放协议
2. **互操作性**: 未来可与外部 Agent 无缝集成
3. **状态管理**: A2A 原生支持 Task 状态机，减少自定义代码
4. **向后兼容**: 保留 Handoff fallback，确保平滑迁移

## 实现摘要

### A2A Server (Worker 端)

```
docs/system/workspace/scripts/runtime/a2a/a2a_server.py
```

功能：
- Agent Card endpoint (`/.well-known/agent.json`)
- Task CRUD endpoints
- SSE streaming
- exit_kind → A2A Task state 映射
- Unix Domain Socket 传输

### A2A Client (Manager 端)

```
docs/system/workspace/scripts/runtime/a2a/a2a_client.py
```

功能：
- 能力发现 (discoverAgent)
- Task 创建和状态监控
- Handoff fallback (A2AHandoffAdapter)
- 等待 Task 完成

### 测试结果

```
Results: 6 passed, 0 failed, 6 total
- T1: Agent Card Discovery ✅
- T2: exit_kind Mapping ✅
- T3: Task CRUD ✅
- T4: Capability Check ✅
- T5: Wait for Completion ✅
- T6: Handoff Fallback ✅
```

## 影响

- **新增**: A2A 协议支持 (docs/system/workspace/a2a/)
- **保留**: Handoff fallback (向后兼容)
- **弃用**: 旧 handoff 逻辑 (待迁移完成后删除)
- **依赖**: A2A 协议规范 (https://github.com/A2A-Specification/A2A)

## 未决问题

1. Handoff 数据迁移到 A2A Task 格式
2. 旧 handoff 逻辑删除时间表
3. 外部 Agent 注册机制

## 参考

- [A2A 协议规范](https://github.com/A2A-Specification/A2A)
- [Linux Foundation AI Agents](https://lfai.foundation/)
- [Freely Handoff 机制](../handoff.md)