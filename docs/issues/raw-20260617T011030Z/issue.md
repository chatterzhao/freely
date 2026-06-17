---
local_id: raw-20260617T011030Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2873'
    url: https://github.com/chatterzhao/freely/issues/2873
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T01:10:48Z'
updated_at: '2026-06-17T01:21:01Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 目标

一次性重构 ACP/A2A 架构到最标准、最优秀的形态。不渐进，不过渡。

## 现有 SQLite 抽象（必须复用，不另起炉灶）

```
freely_db_manager.py (1426行)  ← SQLite daemon，管理全部表
    ↓ Unix socket (/tmp/freely-db-{hash}.sock)
freely-db-cli (384行)          ← CLI 接口，已有 session 操作
    ↓ 需要新增：a2a task 写操作（供 A2A Server 异步 WAL 用）
    
a2a_server.py L107              ← 已知 db socket 路径
    ↓ 需要：通过 freely-db-cli 异步写 WAL
    
a2a_task.py --db                ← 当前绕过 db_manager 直连 SQLite
    ↓ 需要：改为 JSON-RPC → A2A Server → freely-db-cli → db_manager
```

## 核心架构原则

```
状态变更：
  1. 更新 A2A Server TaskStore（内存，同步，权威，不可阻塞）
  2. A2A Server 异步调 freely-db-cli → db_manager → SQLite WAL
     （fire-and-forget，尽力，失败 skip，绝不阻塞步骤 1）

崩溃恢复：WAL replay → 重建 TaskStore
降级运行：db_manager 不可用 → 纯内存，WAL 写失败 skip
```

## 当前问题

### A. a2a_task.py --db 绕过所有抽象层
```
freely 脚本中 15 处 python3 a2a_task.py ... --db "$_db_path"
  → 直接打开 SQLite 文件读写
  → 绕过 A2A Server（内存 TaskStore 空转）
  → 绕过 db_manager daemon（Unix socket 不用）
```

### B. 协议不匹配
a2a_task.py 发 REST，A2A Server 期望 JSON-RPC 2.0

### C. ACP 无状态暴露 / Worker 绕过 A2A

## 目标架构

```
freely 脚本：
  读 task 状态 → a2a_task.py → JSON-RPC → A2A Server TaskStore（内存）
  写 task 状态 → a2a_task.py → JSON-RPC → A2A Server → 内存更新
                                                   → 异步 freely-db-cli → WAL

A2A Server：
  内存 TaskStore（运行时权威）
  状态变更 → 异步调 freely-db-cli task-upsert → db_manager → SQLite WAL

启动：
  freely-db-cli task-restore → WAL replay → A2A Server TaskStore 恢复
```

## 具体改动（按优先级）

### Phase A: A2A 协议 + 持久化（P0）

**A-1. freely-db-cli 新增 a2a task 操作**
- `freely-db-cli task-upsert --task-id <> --state <> ...`（供 A2A Server 异步写）
- `freely-db-cli task-restore --role manager|worker`（启动时 WAL replay）
- `freely-db-cli task-list --state <> --role <>`（查询）
- 复用 db_manager 已有的 `a2a_tasks` 表，不新建

**A-2. a2a_task.py 客户端改为 JSON-RPC 2.0**
- `_unix_request()` 发送 `{"jsonrpc":"2.0","method":"tasks/send",...}`
- 移除 `--db` 直连 SQLite（15 处调用全部改为走 A2A Server）

**A-3. A2A Server 集成异步 WAL**
- TaskStore 状态变更 → 调 `freely-db-cli task-upsert`（异步，fire-and-forget）
- 启动时 `freely-db-cli task-restore` → replay → TaskStore
- 复用 L107 已有的 db socket 路径

**A-4. freely 脚本全部 `--db` 调用改为 JSON-RPC**
- 15 处 `a2a_task.py ... --db` → `a2a_task.py ... --server`（走 A2A Server）

### Phase B: ACP 状态暴露（P0）
- session/ping heartbeat + stopReason 正规化 + per-tool system prompt

### Phase C: State Bridge（P1）
- idle timeout 前查内存 TaskStore

### Phase D: Worker A2A 标准化（P1）
- Worker 走 tasks/send + tasks/push

## 吸收 / Out of Scope（不变）
