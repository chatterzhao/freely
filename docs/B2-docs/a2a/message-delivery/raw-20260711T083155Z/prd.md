# PRD: A2A→SSE→ACP 消息投递链 + SQLite 友好校验

## Goal

打通 A2A agent 间消息投递全链路，并增加 SQLite 层友好校验，使 AI agent 在写错数据时能得到明确的修复指导。

## 实现方案

### 消息投递全链路

```
发送方 Agent → a2a_task.py prompt --task-id <id> --message "..."
  → POST /tasks/{id}/messages (A2A Server REST)
  → SQLite 三层校验 (freely_db_manager.py)
    ├─ Gate 1: content 非空
    ├─ Gate 2: role ∈ {manager, worker, reviewer}
    └─ Gate 3: task 存在
  → 校验失败 → HTTP 422 + {ok:false, error, fix_hint, example} → CLI stderr
  → 校验通过 → SSE message_added 事件
  → watchdog_sse.py 接收 SSE
  → 查 a2a_tasks.raw_key → agent_working.session_id
  → ACP session/prompt → 目标 Agent 的 AI session
```

### 模块划分

| 模块 | 文件 | 职责 |
|------|------|------|
| API 层 | a2a_server.py | 接收 HTTP 请求，调用 DB RPC，emit SSE，返回友好错误 |
| 校验层 | freely_db_manager.py | SQLite 三层 gate，返回结构化错误 |
| 投递层 | watchdog_sse.py | SSE → agent_working → ACP 消息投递 |
| CLI 层 | a2a_task.py | 调用 API，失败时打印修复建议到 stderr |

## Dev-Loop Handoff

- 4 文件已修改并 commit
- 测试: 验证消息投递链路 + 友好校验返回
- PR: pr-create-guarded → pr-merge-guarded
