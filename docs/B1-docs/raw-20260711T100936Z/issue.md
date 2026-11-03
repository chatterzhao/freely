---
local_id: raw-20260711T100936Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260711T100936Z-A
platform_ids:
  github:
    issue_id: '3885'
    url: https://github.com/chatterzhao/freely/issues/3885
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-11T10:09:36Z'
updated_at: '2026-07-11T10:09:36Z'
intake_id: ''
author: zhaoquan
channel: freely
session_refs: []
platform_state: closed
---

# fix: daemon stop rc=143 与意外崩溃区分

## 问题
daemon stop 和 AI crash 都产生 SIGTERM/rc=143，monitor 无法区分。

## 修复
monitor-ai-acp.sh: stop_reason=unknown 时检查 stop_marker 文件
