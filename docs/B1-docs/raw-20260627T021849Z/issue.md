---
local_id: raw-20260627T021849Z49Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260627T021849Z-A
platform_ids:
  github:
    issue_id: '3575'
    url: https://github.com/chatterzhao/freely/issues/3575
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-27T02:19:09Z'
updated_at: '2026-06-27T02:19:09Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 现象

`wt-close --platform-only` 报错找不到本地 issue.md，
但 --platform-only 就是"只操作平台 API"，不应依赖本地文件。

## 修复

--platform-only 模式跳过本地文件检查，直接通过 raw_key 关闭平台 issue。
