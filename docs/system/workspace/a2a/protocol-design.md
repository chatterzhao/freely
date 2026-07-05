# Freely A2A 协议设计

> 本文档定义 Freely Agent 如何使用 A2A (Agent-to-Agent) 协议进行 Manager-Worker 通信。

## 概述

A2A 是 Linux 基金会 AI Agents 工作组发布的开放协议，用于 Agent 间通信。Freely 将其用于 Manager-Worker 交接，替换现有的私有 Handoff 机制。

## A2A 核心概念

### 1. Agent Card

Agent Card 是 JSON 描述的 Agent 能力声明，URL: `/.well-known/agent.json`

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
      "id": "freely-workflow-guarded-execution",
      "name": "Bug Fix Execution",
      "description": "快速修复 bug 的特殊高效策略"
    },
    {
      "id": "freely-workflow-guarded-execution",
      "name": "Feature Execution",
      "description": "新功能/大型改动的完整开发流程"
    },
    {
      "id": "freely-doc-B1_IBM-execution",
      "name": "B1_IBM Pre-Research",
      "description": "I→B→M 第一阶段预研收敛"
    },
    {
      "id": "freely-doc-B2_IBM-execution",
      "name": "B2_IBM Design",
      "description": "I→B→M 第二阶段实现设计"
    }
  ]
}
```

### 2. Task

Task 是 A2A 的核心任务单元，包含完整状态机。

#### Task 状态机

```
          ┌─────────────┐
          │   submitted │
          └──────┬──────┘
                 │
          ┌──────▼──────┐
    ┌─────│   working   │─────┐
    │     └─────────────┘     │
    │                        │
┌───▼───┐              ┌─────▼────┐
│failed │              │completed │
└───────┘              └──────────┘
    │
┌───▼────────┐   ┌──────────────┐
│input-required│◄─│input-required│
└────────────┘   └──────────────┘
```

### 3. Message

Message 是 Task 内的消息，支持 text、data、artifact 类型。

## Freely Agent Card 扩展

Freely Agent Card 扩展 A2A 标准，声明 Freely 特有能力：

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
  "skills": [...],
  "freely": {
    "worktreeIsolation": true,
    "worktreeRoot": "/path/to/project-worktrees",
    "supportedStates": [
      "submitted",
      "working",
      "input-required",
      "completed",
      "failed",
      "canceled"
    ],
    "a2aSchema": "https://freely.dev/schemas/a2a-task-v1",
    "supportedSkills": [
      "freely-workflow-guarded-execution",
      "freely-workflow-guarded-execution",
      "freely-doc-B1_IBM-execution",
      "freely-doc-B2_IBM-execution"
    ],
    "transport": "unix-domain-socket",
    "socketPath": "/tmp/freely-a2a-{project-hash}.sock"
  }
}
```

## A2A Task 状态（Google A2A 标准）

`a2a-exit --state <value>` 直接写入标准 A2A Task.state。

| A2A Task state | 含义 | Freely 使用场景 |
|---------------|------|----------------|
| `submitted` | 任务已提交 | Manager 创建任务 |
| `working` | Agent 执行中 | Worker/Reviewer 工作中 |
| `input-required` | 需要外部输入 | Worker 完成 phase，等 reviewer GO/FIX |
| `completed` | 任务成功 | wt-close 后 |
| `failed` | 任务失败 | 崩溃/超时 |
| `canceled` | 任务被取消 | Manager 主动放弃 |

> 旧 `exit_kind` (worker_blocked, worker_done 等) 已废弃。直接使用标准 state 名。

## Freely 特有 artifact 类型

### 1. handoff_json artifact

```json
{
  "type": "a2a_task",
  "name": "Freely A2A Task JSON",
  "description": "Freely Manager-Worker A2A task document",
  "parts": [
    {
      "type": "data",
      "data": {
        "exit_kind": "worker_done",
        "completion_summary": "...",
        "evidence_paths": ["..."],
        "next_action": "...",
        "session_id": "...",
        "consumed_by": "manager"
      }
    }
  ]
}
```

### 2. completion_summary artifact

```json
{
  "type": "text",
  "name": "Completion Summary",
  "description": "Worker completion summary",
  "parts": [
    {
      "type": "text",
      "text": "任务完成，修复了 XXX 问题"
    }
  ]
}
```

### 3. evidence_paths artifact

```json
{
  "type": "file",
  "name": "Evidence Files",
  "description": "Worker 产出证据文件列表",
  "parts": [
    {
      "type": "data",
      "data": {
        "paths": [
          "docs/progress/xxx/evidence.md",
          "docs/B1-docs/xxx/issue.md"
        ]
      }
    }
  ]
}
```

## A2A Endpoints

### Worker 端 (A2A Server)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/.well-known/agent.json` | GET | 获取 Agent Card |
| `/tasks/send` | POST | 发送任务 |
| `/tasks/{id}` | GET | 获取任务状态 |
| `/tasks/{id}/stream` | GET | SSE 流式推送 |

### Manager 端 (A2A Client)

| 操作 | 说明 |
|------|------|
| discoverAgent() | 发现 Worker Agent Card |
| createTask() | 创建 A2A Task |
| sendMessage() | 发送消息到 Task |
| streamTask() | 订阅 Task SSE 流 |
| getTaskStatus() | 获取任务状态 |

## 传输层

### Unix Domain Socket (同实例)

Freely Manager 和 Worker 在同一机器上运行时，使用 Unix Domain Socket：

```python
SOCKET_PATH = "/tmp/freely-a2a-{project_hash}.sock"
```

优点：
- 低延迟 (< 1ms)
- 无网络开销
- 同机器安全

### HTTP (跨实例)

跨机器通信时使用 HTTP：

```python
AGENT_URL = "http://worker-host:7890"
```

## 与 MCP 的关系

| 特性 | A2A | MCP |
|------|-----|-----|
| 用途 | Agent 间通信 | Agent 与工具交互 |
| 模式 | 双向对话 | 工具调用 |
| 状态管理 | 有 (Task) | 无 |
| 生态 | 开放标准 | Anthropic 主导 |
| Freely 角色 | Manager↔Worker | Worker↔工具 |

**A2A 用于 Manager-Worker 通信，MCP 用于 Worker 与外部工具交互。**

## 实现状态

- [x] 协议设计文档
- [ ] Freely Agent Card JSON Schema
- [ ] exit_kind → A2A Task 映射表
- [ ] A2A Server 实现 (Worker 端)
- [ ] A2A Client 实现 (Manager 端)
- [ ] Handoff fallback
- [ ] 集成测试

## 参考

- [A2A 协议规范](https://github.com/A2A-Specification/A2A)
- [Linux Foundation AI Agents](https://lfai.foundation/)