---
local_id: raw-20260627T084545Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260627T084545Z-A
platform_ids:
  github:
    issue_id: '3585'
    url: https://github.com/chatterzhao/freely/issues/3585
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-27T08:46:05Z'
updated_at: '2026-07-06T12:27:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Scope

a2a_tasks 表 agent_id 列从通用角色（worker/manager）改为具体编号（worker_03/manager_01），支持多 agent 并发区分。

## Changes

- freely:13601: --role worker → --role $_next_worker
- a2a_task.py:607: agent_id=role → 用 --agent-id 值
- a2a_task.py:883,892: agent_id == worker → LIKE worker_%
- a2a_server.py: 6处 "worker" 硬编码 → LIKE worker_%
- freely_db_manager.py:1187,1193: = worker → LIKE worker_%
- a2a_registry.py: default="worker" → 接受具体 agent_id
- 写入 worker_pid
- 更新 delivery_status
