---
local_id: raw-20260630T113839Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T113839Z-A
platform_ids:
  github:
    issue_id: '3655'
    url: https://github.com/chatterzhao/freely/issues/3655
    synced_at: ''
  gitee:
    issue_id: IJXX17
    url: https://gitee.com/zhaoquan/freely/issues/IJXX17
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T11:39:00Z'
updated_at: '2026-06-30T11:39:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

daemon start 时报 `develop working tree is dirty`，因为 `.freely/run/workcell-state.env` 被修改。该文件是运行时状态文件，daemon 正常运行时会修改它，不应计入 dirty 检查。

## 根因

`git_status_entry_path_is_disposable_runtime_residue()` 只排除 `__pycache__` 和 `.pyc`，没有排除 `.freely/run/*` 运行时文件。

## 改动

`docs/system/workspace/scripts/runtime/freely` line 7601-7608:
- `git_status_entry_path_is_disposable_runtime_residue()` 增加 `.freely/run/*` 和 `.freely/logs/*` 模式
