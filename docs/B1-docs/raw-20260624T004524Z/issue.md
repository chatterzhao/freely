---
local_id: raw-20260624T004524Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T004524Z-A
platform_ids:
  github:
    issue_id: '3398'
    url: https://github.com/chatterzhao/freely/issues/3398
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T00:45:41Z'
updated_at: '2026-06-24T00:45:41Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 现象

`daemon start` 日志：
```
[WARN] A2A server start timed out after 10s (may be TCP-only)
```

## 根因

`A2AServer.__init__`（`a2a_server.py:325-338`）中 `_restore_tasks()` 是**同步调用**：

```python
def __init__(self, ...):
    self.task_store = SQLiteTaskStore(project)
    self._restore_tasks()  # ← 同步阻塞！
```

`_restore_tasks()` 做了这些事（全部在 server 开始监听之前）：
1. `get_all_dicts()` → DB 查询全部 task
2. 对每个 `working` worker：`os.kill(pid, 0)` 检查进程存活
3. 对死进程：`raw_rpc("a2a_task.update", ...)` 标记 failed

如果 DB 里有大量 task，或者某些 PID 检查慢（僵尸进程），`__init__` 会卡住几秒。此时 Starlette 还没开始监听 Unix socket → health check 连接到 socket 失败 → 等到超时。

## 设计问题

恢复逻辑不应该阻塞 server 启动。正确做法：
- `__init__` 只创建 TaskStore，立即开始监听
- `_restore_tasks` 在后台异步运行（Starlette `asyncio.create_task`）
- health check 只验证 HTTP server 已就绪，不验证恢复完成

## 要做的事

`a2a_server.py`：
1. `_restore_tasks` 改为 `async` 方法
2. `__init__` 中不再同步调用，改为 `asyncio.ensure_future(self._restore_tasks())`
3. 或更简单：在 `_build_app` 之后、server 启动之前，用 `loop.call_soon_threadsafe` 调度

如果异步改造太复杂，备选方案：health check 超时从 10s 增大到 20s + fix 误导信息 "may be TCP-only"（实际是 Unix socket 慢启动）。

## 消息修正

"may be TCP-only" 改为 "server startup took >10s (check DB size, zombie PIDs)"

## 参考
- `a2a_server.py:325-338` — `__init__` + `_restore_tasks`
- `a2a_server.py:340-477` — `_restore_tasks` 当前实现
- `freely:8354-8386` — health check 逻辑
- SSE 实现 #3388 中修复了 `_restore_tasks` 逻辑
