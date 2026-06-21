---
local_id: raw-20260617T121221Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2920'
    url: https://github.com/chatterzhao/freely/issues/2920
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T12:12:38Z'
updated_at: '2026-06-21T18:25:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-06-17T14:28:55Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
absorbed_into: I-20260617T121221Z-A
platform_state: closed
---

## 问题
PR #2914 移除了 CSV 委派机制和 --workers 参数，但 worker_prompts_csv 字段仍在 A2A 层 7 处残留。

## 遗漏清单
- a2a_server.py: execute()/POST/PATCH handler 仍写 worker_prompts_csv
- a2a_types.py: Task dataclass/to_dict/from_dict 仍有此字段
- a2a_task.py: L418 worker_prompts_csv=fields.get(workers)
- freely_db_manager.py: DB schema+insert 仍有（保留列，停止写）
- exit-kind-mapping.md + protocol-design.md: 文档仍引用 CSV

## 修复
移除所有 worker_prompts_csv 读写代码。DB 列保留向后兼容，停止写。
