---
local_id: raw-20260617T063755Z55Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260617T063755Z-B
platform_ids:
  github:
    issue_id: '2897'
    url: https://github.com/chatterzhao/freely/issues/2897
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T06:38:12Z'
updated_at: '2026-06-21T01:40:17Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 问题

raw-20260617T011030Z30Z Phase A 规定的 A2A 目标架构未完全实现：

### 1. _db_rpc 绕过 A2A Server
a2a_task.py 的 6 个 Freely 特有方法通过 _db_rpc 直连 db_manager → SQLite，完全绕过 A2A Server：
- latest_manager()
- pending_delivery()
- launched_pids()
- add_message()
- mark_delivered()
- set_worker_pid()

而设计意图是：所有操作 → A2A Server (内存权威) → 异步 db-cli → SQLite WAL

### 2. SQLite 角色错误
_db_rpc 在热路径上被同步调用，SQLite 变成了实时协调通道。设计意图是 SQLite 仅作为异步持久化 WAL（fire-and-forget，崩溃恢复用），不阻塞 A2A Server。

### 3. SSE 零实现
protocol-design.md 明确了 /tasks/{id}/stream SSE 端点，当前 streaming=False，无任何 SSE 实现。Manager 通过轮询 _db_rpc 获取 Worker 状态变更。

## 修复

### Phase 1: 将 6 个方法迁移到 A2A Server
- a2a_server.py: 已有 latest_manager/pending_delivery/launched_pids/add_message/mark_delivered/set_worker_pid 的 REST 路由
- a2a_task.py: 将这 6 个方法从 _db_rpc 改为通过 _unix_request 调用 A2A Server 对应端点
- 移除 a2a_task.py 中的 _db_rpc 方法（客户端不应直连 db_manager）

### Phase 2: 启用 SSE 流式推送
- a2a_server.py: AgentCard streaming=True, push_notifications=True
- a2a_server.py: 新增 /tasks/{id}/stream SSE 端点
- Worker 状态变更 → A2A Server TaskStore → SSE event → Manager 收到推送

### Phase 3: SQLite 回归异步 WAL
- A2A Server 的 SQLiteTaskStore 保持异步写（已是 fire-and-forget 模式）
- 启动时 WAL replay 恢复 TaskStore（_restore_tasks 已实现）
- db_manager 不可用时降级为纯内存模式（不阻塞）

## 影响文件
- docs/system/workspace/scripts/runtime/a2a/a2a_server.py
- docs/system/workspace/scripts/runtime/a2a_task.py
- docs/system/workspace/scripts/runtime/freely（若 _db_path 引用残留）
