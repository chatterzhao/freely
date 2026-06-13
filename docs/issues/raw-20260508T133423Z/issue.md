---
local_id: raw-20260508T133423Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260508T133423Z-A
platform_ids:
  github:
    issue_id: '372'
    url: https://github.com/chatterzhao/freely/issues/372
    synced_at: '2026-05-16T13:21:27Z'
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-08T13:34:23Z'
updated_at: '2026-06-13T10:50:03Z'
intake_id: ''
author: zhaoquan
channel: local
session_refs: []
platform_state: closed
---

## 问题

raw-issue-pull 在非项目根目录执行时 git 路径解析错误。

## 修复

调整 git CWD 引用方式，并排除 .scan-state 文件。
