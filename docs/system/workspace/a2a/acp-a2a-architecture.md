# Freely ACP/A2A 架构

## 角色与协议

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Freely Runtime (bash)                            │
│                                                                         │
│  scan → prompt → delegate → launch → monitor → exit_contract → loop     │
│                                                                         │
│  ┌──────────────┐  A2A (JSON-RPC/REST)  ┌─────────────────────────────┐│
│  │ A2A Server   │◄─────────────────────►│ a2a_task.py (CLI client)    ││
│  │ (Python)     │                       │                             ││
│  │ TaskStore    │                       │ a2a-exit --state submitted   ││
│  │ SSE /stream  │                       │ tasks/list --state submitted ││
│  │ AgentCard    │                       │ tasks/get, tasks/update     ││
│  └──────┬───────┘                       └─────────────────────────────┘│
│         │ JSON-RPC over Unix socket + WAL-backed tables                  │
│  ┌──────▼───────┐                                                        │
│  │ freely-db    │──► SQLite/WAL (runtime state tables)                  │
│  │ daemon       │    single writer: freely_db_manager.py                │
│  └──────────────┘                                                        │
└─────────────────────────────────────────────────────────────────────────┘
         │                                              │
         │ ACP (JSON-RPC over stdio/socket)              │ ACP
         ▼                                              ▼
┌─────────────────────┐                    ┌─────────────────────┐
│   Manager Agent     │                    │   Worker Agent      │
│   (ACP session)     │                    │   (ACP session)     │
│   develop worktree  │                    │   fix/feature       │
│                     │                    │   worktree          │
│   AI CLI Tool       │                    │   AI CLI Tool       │
│   (opencode/cc/     │                    │   (opencode/cc/     │
│    codex)           │                    │    codex)           │
└─────────────────────┘                    └─────────────────────┘
```

## 时序：Manager 委派 Worker 全链路

```
 Manager Agent        Freely Runtime          A2A Server        Worker Agent
 (ACP session)        (bash)                  (Python)           (ACP session)
      │                    │                      │                    │
      │ 1. scan/review     │                      │                    │
      │───────────────────►│                      │                    │
      │                    │ 2. build prompt      │                    │
      │◄───────────────────│                      │                    │
      │                    │                      │                    │
      │ 3. session/prompt  │                      │                    │
      │   (AI 决策委派)     │                      │                    │
      │                    │                      │                    │
      │ 4. a2a-exit ───────│─────────────────────►│                    │
      │   --state=submitted│  5. POST /tasks       │                    │
      │   --role=worker│     TaskStore.save()  │                    │
      │   --message="..."  │     → a2a_tasks table │                    │
      │                    │                      │                    │
      │ 6. end_turn        │                      │                    │
      │◄───────────────────│                      │                    │
      │                    │                      │                    │
      │                    │ 7. exit_contract     │                    │
      │                    │    kind=delegate     │                    │
      │                    │                      │                    │
      │                    │ 8. tasks/list ──────►│                    │
      │                    │   --state=submitted  │                    │
      │                    │   --role=worker  │                    │
      │                    │◄─────────────────────│                    │
      │                    │   [{task_id,         │                    │
      │                    │     message,         │                    │
      │                    │     worktree,        │                    │
      │                    │     branch, skill}]  │                    │
      │                    │                      │                    │
      │                    │ 9. for each task:    │                    │
      │                    │    message→prompt    │                    │
      │                    │    file (temp)       │                    │
      │                    │                      │                    │
      │                    │ 10. session/prompt ──────────────────────►│
      │                    │     (ACP fork)       │                    │
      │                    │                      │    11. AI works    │
      │                    │                      │    (B1→B2→dev→...) │
      │                    │                      │                    │
      │                    │                      │ 12. a2a-exit       │
      │                    │                      │   --state=completed│
      │                    │◄─────────────────────│────────────────────│
      │                    │   TaskStatusUpdate   │                    │
      │                    │   (SSE event)        │                    │
      │                    │                      │                    │
      │                    │ 13. cleanup temp     │                    │
      │                    │     prompt file      │                    │
      │                    │                      │                    │
      │                    │ 14. next cycle       │                    │
      │◄───────────────────│                      │                    │
```

## 协议分层

| 层 | 协议 | 职责 | 有无文件 |
|----|------|------|---------|
| **Agent 间协调** | A2A | Task 生命周期、Message 内容、SSE 通知 | ❌ 零文件 |
| **AI 执行** | ACP | session/prompt、stopReason、session/ping | ✅ 临时文件（协议需要） |
| **编排** | Freely Runtime | scan→prompt→delegate→launch→monitor | 生成临时文件 |
| **持久化** | freely-db daemon + SQLite/WAL | `freely_db_manager.py` 持有单 SQLite connection，通过 Unix socket JSON-RPC 读写 `a2a_tasks`、`chats`、`sessions`、`tool_*`、`task_mode_gate` | DB 文件 |

## 关键数据流

```
A2A Task.message ──(Runtime 桥接)──► 临时 prompt file ──► ACP session/prompt
        ↑                                                         │
        │                       Worker AI 产出                    │
        │                                                         ▼
        └────────────── a2a-exit --state=completed ───────────────┘
                                   (更新 Task state)
                                   (SSE → Manager 感知)
```

## 对比

| | CSV 时代（旧） | A2A 时代（新） |
|---|---|---|
| 委派 | 写 prompt 文件 + CSV 路径 | a2a-exit → Task.message |
| 发现 | 读 CSV → 开文件 | tasks/list --state=submitted |
| 交接内容 | prompt_file 字段(持久文件路径) | Task.message(A2A 标准) |
| 文件路径 | 存储在 Task 中 | Runtime 从 task_id 派生(临时) |
| 通知 | 轮询 | SSE TaskStatusUpdateEvent |
