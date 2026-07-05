---
b1_id: B1-20260627T084545Z
phase_state: completed
source_raw: raw-20260627T084545Z
source_url: https://github.com/chatterzhao/freely/issues/3585
produced_candidate: C-20260627T084545Z-A
created_at: 2026-06-27
---

# B1_IBM: a2a_tasks agent_id 改具体编号 + 字段补全

## Input
- 来源: raw-20260627T084545Z (GitHub #3585)
- 调研文档: .a2a-tasks-review.md

## 调用链追踪

### agent_id 写入路径

```
freely:13601  --role worker --raw-key ... --worktree ...
  → a2a_task.py insert
    → fields["role"] = "worker"        (通用角色)
    → agent_id=role                    (L607: 把 role 当 agent_id)
    → _client().create(agent_id=role)  → REST POST /tasks
    → a2a_tasks.agent_id = "worker"    ← 存的是 "worker"，不是 "worker_01"
```

**根因**: `freely:13601` 传 `--role worker`（通用角色），`a2a_task.py:607` 无脑存 `agent_id=role`。两处都是通用角色。

### agent_id 读取路径（全部硬编码）

| 文件 | 行 | 当前 |
|------|-----|------|
| `a2a_task.py` | 883 | `r.get('agent_id') == 'worker'` |
| `a2a_task.py` | 892 | `r.get('agent_id') == 'worker'` |
| `a2a_server.py` | 246 | `metadata.get("agent_id", "worker")` |
| `a2a_server.py` | 376 | `agent_id == "worker"` |
| `a2a_server.py` | 426 | `r.get("agent_id") == "worker"` |
| `a2a_server.py` | 563 | `body.get("agent_id", "worker")` |
| `a2a_server.py` | 588 | `body.get("role", "worker")` |
| `a2a_server.py` | 636 | `r.get("agent_id") == "worker"` |
| `freely_db_manager.py` | 1187,1193 | `WHERE agent_id = 'worker'` |

### worker_pid 基础设施已存在但未使用

```
a2a_task.py:271  set_worker_pid(task_id, worker_pid)   ✅ 已实现
a2a_task.py:735  update-worker-pid CLI                  ✅ 已实现
freely:13601     insert 时未传 --worker-pid             ❌ 未调用
```

## Problem

agent-table.toml 定义了 `worker_01~10`、`reviewer_worker_01~10` 等具体编号。agent-id.env 正确使用具体编号。但 a2a_tasks 存通用角色 `"worker"`，多 agent 并发时无法区分。worker_pid 全空。

## Brainstorm

### agent_id 改具体编号

唯一方案——改两处源头：
1. `freely:13601`: `--role worker` → `--role $_next_worker`（从 agent-id.env 分配时已有的变量）
2. `a2a_task.py:607`: 不改（`agent_id=role` 本身正确，关键是传进来的 role 值已经是具体编号）

以及改所有读取端：
3. 6 处 `== 'worker'` / `= 'worker'` → `LIKE 'worker_%'` 或 `startswith('worker_')`

### worker_pid 写入

在 `freely:13601` insert 成功拿到 task_id 后，调 `a2a_task.py update-worker-pid --task-id $_task_id --worker-pid $worker_pid`。

worker_pid 从哪里来？fork session 后 AI 进程的 PID。当前 fork session 在 `start_workcell_supervisor_async` 中，需要把 PID 传回给 insert 路径。

### delivery_status

worker a2a-exit 时调 `a2a_task.py update --task-id $_task_id --delivery-status delivered`。当前 a2a-exit 已在 worker 退出时调用，但没传 delivery_status。

## Decision

三处改动，全部独立：
1. agent_id: `--role worker` → `--role $_next_worker`（1 行）+ 6 处 LIKE
2. worker_pid: insert 后调 update-worker-pid（~3 行）
3. delivery_status: a2a-exit 时传 --delivery-status（~1 行）

## Candidate
- candidate_id: C-20260627T084545Z-A
- status: promoted
- milestone: M-20260627T084545Z-A
