---
local_id: I-20260612T140944Z-A
kind: linked
phase_state: completed
completed_at: '2026-06-13'
platform_ids: {}
primary_platform: github
canonical_issue_path: docs/epics/a2a-replace-handoff/architecture-refactor/
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-13T01:20:00Z'
updated_at: '2026-06-13T01:20:00Z'
platform_state: open
linked_raw: raw-20260612T140944Z
linked_candidate: C-20260612T140944Z-A
worktree: fix/raw-20260612T140944Z-a2a-handoff-compat
---

# I-20260612T140944Z-A: 彻底 A2A 重构

## Scope

将 Freely agent 通信从 handoff 机制彻底重构为标准 A2A 协议。

## Changes

18 modified + 3 new + 3 deleted = 24 files, +1400 / -2400 lines

### 核心文件

| 文件 | 操作 | 说明 |
|------|------|------|
| `a2a/a2a_server.py` | 重写 | 官方 SDK + Starlette + Uvicorn + dual transport |
| `a2a/a2a_registry.py` | 新增 | A2X-style agent registry |
| `a2a/a2a_types.py` | 新增 | Standard A2A types |
| `a2a_task.py` | 重写 | A2A Client + 21 API + 20 CLI + dual transport |
| `a2a_task_parser.py` | 修改 | A2A state-based，无 exit_kind |
| `freely_db_manager.py` | 修改 | 15 a2a_task.* RPC + delivery_status/worker_pid |
| `freely` | 修改 | handoff→A2A 全量命名 |
| `wt-close` | 修改 | 变量/注释更新 |
| `handoff.py.bak` | 删除 | — |
| `handoff_parser.py.bak` | 删除 | — |
| `migrate_handoff_to_a2a.py.bak` | 删除 | — |
| `manager-agent.md` | 修改 | A2A Task State 文档 |
| `worker-agent.md` | 修改 | A2A Task State 文档 |

### 能力保留

原始 18 项 handoff 能力全部保留，新增 9 项 A2A 协议能力。

### 测试

- 21 项单元测试（Parser/Registry/Types/Client/Server）
- E2E 验证（create/get/update/list/extensions）
- freely bash + wt-close 语法检查

### PR

https://github.com/chatterzhao/freely/pull/2577
