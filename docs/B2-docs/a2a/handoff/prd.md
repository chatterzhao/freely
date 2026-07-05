# PRD: A2A 协议替换 Freely Handoff 架构重构

## Goal

用 Linux 基金会 A2A (Agent-to-Agent) 协议替换 Freely 现有的私有 Handoff 机制，实现：

1. **标准化能力发现**：Manager 能通过 Agent Card 发现 Worker 能力
2. **完整状态机**：8 种 A2A Task 状态覆盖 Manager-Worker 完整生命周期
3. **实时通信**：SSE 推送替换轮询，Manager 实时感知 Worker 状态
4. **开放互操作**：与外部 Agent 系统互通

## Background

### 当前问题

Freely 自举开发中暴露大量 `launch_failed, launchable check failed`：

```
根因：Manager 不知道 Worker 需要什么能力
→ 盲目委派
→ launchable check 失败
→ Worker 未启动
→ scan 列表停摆
```

### Handoff 机制缺陷

| 能力 | A2A | Freely Handoff |
|------|-----|----------------|
| Agent 能力发现 | ✅ Agent Card 标准 | ❌ 无 |
| 完整状态机 | ✅ 8 种状态 | ❌ 3 种状态 |
| 实时推送 | ✅ SSE/Streaming | ❌ 无 |
| 能力协商 | ✅ Capability negotiation | ❌ 无 |
| 开放互操作 | ✅ Linux 基金会标准 | ❌ 私有 |

## A2A 协议概述

### 核心概念

1. **Agent Card**
   - JSON 描述 Agent 能力、技能、端点
   - URL: `/.well-known/agent.json`
   - 字段：name, description, skills, url, version, capabilities...

2. **Task**
   - 任务状态机
   - 状态：submitted, working, completed, failed, input-required, pending-input...
   - 消息：text, data, artifact

3. **Message**
   - 任务消息
   - 类型：text, data, artifact
   - 支持 streaming

### A2A vs MCP

| 特性 | A2A | MCP |
|------|-----|-----|
| 用途 | Agent 间通信 | Agent 与工具交互 |
| 模式 | 双向对话 | 工具调用 |
| 状态管理 | 有 | 无 |
| 生态 | 开放标准 | Anthropic 主导 |

## Freely 适配设计

### Freely Agent Card 扩展

```json
{
  "name": "Freely Worker",
  "description": "Freely Worker Agent with worktree isolation",
  "url": "http://localhost:7890",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true
  },
  "skills": [
    {
      "id": "freely-fix-execution",
      "name": "Bug Fix Execution",
      "description": "快速修复 bug"
    },
    {
      "id": "freely-feat-execution", 
      "name": "Feature Execution",
      "description": "新功能/大型改动"
    }
  ],
  // Freely 扩展
  "freely": {
    "worktreeIsolation": true,
    "supportedExitKinds": [
      "worker_done", "worker_blocked", 
      "worker_handoff_needed", "worker_working"
    ],
    "handoffJsonSchema": "..."
  }
}
```

### exit_kind → A2A Task 状态映射

```
Freely exit_kind          → A2A Task state        → 说明
──────────────────────────────────────────────────────────────
manager_working           → submitted             → Manager 已提交
worker_working            → working               → Worker 正在执行
worker_done               → completed             → 任务完成
worker_blocked            → input-required        → 需要输入
worker_handoff_needed     → pending-input         → 需要 Manager 介入
delegate_workers         → submitted             → 委派新 Worker
resume_manager           → completed             → 返回 Manager
stop_ai                   → failed                → AI 停止
```

### Freely 特有 artifact 类型

```json
{
  "type": "freely_handoff",
  "artifact": {
    "handoff_json": {
      "exit_kind": "worker_done",
      "completion_summary": "...",
      "evidence_paths": ["..."],
      "next_action": "..."
    }
  }
}
```

## 实现计划

### Phase 1: 协议设计 (M1)

- [ ] 设计 Freely Agent Card 扩展 JSON Schema
- [ ] 定义 exit_kind → A2A Task 状态映射表
- [ ] 定义 Freely 特有 artifact 类型
- [ ] 架构评审

### Phase 2: 原型实现 (M2)

- [ ] 实现 A2A Server (Worker 端)
  - [ ] Agent Card endpoint
  - [ ] Task CRUD endpoints
  - [ ] SSE streaming
- [ ] 实现 A2A Client (Manager 端)
  - [ ] 能力发现
  - [ ] Task 创建和状态监控
- [ ] 保留 Handoff 作为 fallback
- [ ] Basic handoff 测试通过

### Phase 3: 状态迁移 (M3)

- [ ] 将 handoff table 迁移到 A2A Task
- [ ] 迁移脚本和验证
- [ ] 删除旧 handoff 逻辑
- [ ] 性能基准测试

### Phase 4: 增强功能 (M4)

- [ ] SSE 实时推送
- [ ] 能力协商自动化
- [ ] 外部 Agent 互操作

## Dev-Loop Handoff

B2_IBM 完成后，进入 `skill:freely-dev-loop-execution`：

1. 实现 Phase 1-2 原型
2. pre-tests 验证
3. 提交 code-review
4. 通过后合并到 develop

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 同实例紧耦合 | 使用 Unix Domain Socket |
| 状态映射丢失 | 保留完整映射表 |
| 性能下降 | 基准测试监控 |
| 外部 Agent 不兼容 | 提供 adapter 层 |
