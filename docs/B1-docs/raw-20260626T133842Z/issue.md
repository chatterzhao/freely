---
local_id: raw-20260626T133842Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3554'
    url: https://github.com/chatterzhao/freely/issues/3554
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T13:39:02Z'
updated_at: '2026-06-26T13:48:58Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260626T133842Z-A
source_candidate: docs/B1-docs/20260626T133842Z--feedback-exit-on-error/candidates.md#C-20260626T133842Z-A
---

## 问题

`cmd_feedback` line 23182: `|| true` 吞掉 adapter 错误。line 23187: 一个平台成功就算全过。line 23191: 全失败只是 WARNING 不 exit。

## 修复

去掉 `|| true`，逐平台检查。任一平台创建失败 → exit 1。全失败 → exit 1。
