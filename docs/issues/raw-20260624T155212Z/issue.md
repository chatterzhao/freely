---
local_id: raw-20260624T155212Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3446'
    url: https://github.com/chatterzhao/freely/issues/3446
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T15:52:36Z'
updated_at: '2026-06-24T15:52:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

pretests-retirement-gate 在 workcell-state.env 不存在时直接 exit 1。手工执行工位无 Worker 痕迹，必须 --force。

## 修复

无 workcell-state.env 时 scan docs/epics/ 查找对应 pre-tests.md 直接验证。
