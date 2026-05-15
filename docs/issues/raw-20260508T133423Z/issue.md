---
local_id: raw-20260508T133423Z
kind: raw
title: 'fix: raw-issue-pull git path resolution error on non-root CWD'
status: proposed
phase_state: proposed
platform_ids:
  github:
    issue_id: '348'
    url: https://github.com/chatterzhao/freely/issues/348
    synced_at: '2026-05-15T18:24:34Z'
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-08T13:34:23Z'
updated_at: '2026-05-15T18:24:34Z'
intake_id: ''
author: zhaoquan
channel: local
session_refs: []
platform_state: open
---

## 问题

raw-issue-pull 在非项目根目录执行时 git 路径解析错误。

## 修复

调整 git CWD 引用方式，并排除 .scan-state 文件。
