---
local_id: raw-20260624T151020Z20Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3440'
    url: https://github.com/chatterzhao/freely/issues/3440
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T15:10:43Z'
updated_at: '2026-06-24T15:20:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260624T151020Z-A

platform_state: closed---

## 根因

wt-close 调用 pretests-retirement-gate 时传参格式错误

## 改动

仅 docs/system/workspace/scripts/worktree/wt-close 第 322 行，一处修改。
