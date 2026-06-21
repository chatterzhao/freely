---
local_id: raw-20260621T130954Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3218'
    url: https://github.com/chatterzhao/freely/issues/3218
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T13:10:12Z'
updated_at: '2026-06-21T13:10:12Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Root Cause

`a2a_task.py` 的 `_unix_request` 方法 (L155) 有一个路由剥离正则 bug:

```python
_stripped = re.sub(r'/tasks/[^/]+', '/tasks', _base)
```

此正则会剥离 `/tasks/latest-manager` 为 `/tasks`，导致 `_rpc_map` 中的专用条目成为死代码。取而代之用通用条目 `tasks/list`，调用了错误的 JSON-RPC 方法。

## Impact

- `latest_manager()` — 始终返回 `{}`
- `pending_delivery()` — 始终返回 `[]`  
- `launched_pids()` — 始终返回 `[]`

这导致 Worker 启动流水线断裂：Manager 创建 A2A 任务后，`parse_a2a_task_json_reply` 获取空状态，无法检测到 submitted workers，`exit_contract_action` 不是 `delegate_workers` → worker 永远不会被启动。

## Fix

3 个方法从 `_request` (JSON-RPC) 改为 `_rest_request` (原始 HTTP)，与 `list()`/`create()`/`update()` 使用的模式一致。

文件: `docs/system/workspace/scripts/runtime/a2a_task.py`
- L255: `latest_manager()` — `_request` → `_rest_request`
- L260: `pending_delivery()` — `_request` → `_rest_request`  
- L265: `launched_pids()` — `_request` → `_rest_request`

## Verification

1. 启动 freely daemon
2. 确认 `a2a_task.py latest-manager` 返回带 task_id 的字典
3. 观察 daemon 日志确认 worker_launch 出现
4. 确认 Worker 进程启动
5. 确认 A2A 任务从 submitted → working

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
