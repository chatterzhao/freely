---
local_id: raw-20260618T091116Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T091116Z-A
platform_ids:
  github:
    issue_id: '2985'
    url: https://github.com/chatterzhao/freely/issues/2985
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T09:11:33Z'
updated_at: '2026-06-18T09:11:33Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Bug 描述

`cmd_daemon_start` 和 `cmd_start` 中，`write_task_mode` 在 `ensure_freely_db` 之前调用。

`write_task_mode` 通过 `freely-db-cli` 走 Unix socket 写到 `freely_db_manager.py` 管理的 SQLite。
如果 `freely_db_manager.py` 进程没在跑（如上次崩溃后没残留），写入静默失败（`|| true` 吞错误）。
`ensure_freely_db` 在后面才启动 DB daemon，但写入已经丢失。

## 影响

- 用户执行 `daemon start` 不带 `--task-mode`：期望将 task_mode 重置为 `wait`，但 SQLite 中旧值（如 `auto`）可能未被覆盖
- `cmd_start` 同样受影响

## 修复方向

在 `cmd_daemon_start` 和 `cmd_start` 中，将 `ensure_freely_db` 调用移到 `write_task_mode` 之前。

## 影响文件

- `docs/system/workspace/scripts/runtime/freely`: `cmd_daemon_start` (L21737-21809), `cmd_start` (L21558-21610)
