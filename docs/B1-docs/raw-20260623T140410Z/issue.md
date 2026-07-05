---
local_id: raw-20260623T140410Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260623T140410Z-A
platform_ids:
  github:
    issue_id: '3390'
    url: https://github.com/chatterzhao/freely/issues/3390
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-23T14:04:30Z'
updated_at: '2026-06-23T14:04:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 背景

SSE 实现（#3388）中修复了 `_restore_tasks()`（`a2a_server.py` 第 340-413 行），从 no-op 改为进程 liveness 检查 + stale delegation 检测。但仍有 3 个边界未处理，且内存优先架构（`acp-a2a-refactor` 10 个 pending task）从未实现。

## 当前正确的状态处理

| 重启时状态 | 处理 | 正确？ |
|-----------|------|--------|
| working + PID 存活 | keep working | ✅ |
| working + PID 已死 | mark failed | ✅ |
| submitted + 60s + 无 Worker | auto-completed | ✅ |
| input-required | keep as-is | ✅ |
| completed/failed/canceled | skip | ✅ |

## 未处理的边界

### 1. `working` + 无 `worker_pid`
Worker task 在 `working` 状态但没有记录 `worker_pid`。当前：跳过（不处理）。应：标记 `input-required` 或 `failed`——无法验证存活，Manager 需要介入。

### 2. `submitted`（Manager task）+ 有活跃 Worker
当前：60 秒后无条件 auto-complete。但如果 Manager 的 Worker 还在运行（只是 Manager 自己还没 completed），这个 auto-complete 会错误关闭一个还在进行中的委派。应：先检查是否有活跃 Worker（`working`/`submitted` 状态），有则不 auto-complete。

### 3. `input-required` + worktree 已删除
Worker 在等待 Manager 输入，但工位已经被 wt-close 删了。当前：保持 `input-required`。应：检查 worktree 是否存在，不存在则标记 `failed`（reason: worktree_deleted_during_downtime）。

## 内存优先架构 (acp-a2a-refactor)

现有 raw issue `raw-20260617T011030Z`（ACP/A2A 架构重构），10 个任务全部 `pending`：

| 任务 | 内容 |
|------|------|
| A-1 | freely-db-cli task-upsert/restore/list |
| A-3 | A2A Server async WAL: memory-first + async DB writes |
| A-4 | 15 --db calls → JSON-RPC |

当前 `SQLiteTaskStore` 是零缓存 RPC 代理——每次 `save/get/update` 同步穿透磁盘。内存优先（1ms 内存更新 + 异步 WAL）从未实现。重启恢复目前靠 SQLite 磁盘数据，没有问题，但有延迟。

## 要做的事

1. `_restore_tasks()` 补 3 个边界处理
2. 评估是否需要推进 acp-a2a-refactor（内存优先对 Freely 的 patrol 架构是否真正必要——当前磁盘延迟在 patrol 周期粒度下可接受）

## 参考
- SSE 实现 #3388：https://github.com/chatterzhao/freely/pull/3389
- acp-a2a-refactor：`docs/B2-docs/acp-a2a-refactor/tasks.md`（10 pending）
- raw-20260617T011030Z：`docs/B1-docs/raw-20260617T011030Z/issue.md`
