---
local_id: raw-20260630T054652Z52Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T054652Z-A
platform_ids:
  github:
    issue_id: '3641'
    url: https://github.com/chatterzhao/freely/issues/3641
    synced_at: ''
  gitee:
    issue_id: IJXSKD
    url: https://gitee.com/zhaoquan/freely/issues/IJXSKD
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T05:47:13Z'
updated_at: '2026-06-30T05:47:13Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n## 背景

PR #3640 完成后 reviewer 发现残留:
- a2a_types.py, a2a_task_parser.py, freely_db_manager.py, a2a_server.py 仍有 pending-input
- agent-card-schema.md 两处 supportedExitKinds 未改

## 改动
清理所有残留引用，schema 定义和 Manager 示例改为 supportedStates
