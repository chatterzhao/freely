---
local_id: raw-20260508T050922Z
kind: raw
phase_state: completed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '255'
    url: https://github.com/chatterzhao/freely/issues/255
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-08T05:09:22Z'
intake_id: ''
author: zhaoquan
channel: github
session_refs: []
platform_state: closed
---

## 问题

I-* issue 创建后 platform_ids 为空，导致 issue-sync close 无法自动关闭平台 issue。

## 修复

1. cmd_close: I-* 无 platform_ids 时向上追溯 raw-* parent
2. cmd_promote: 确保 platform_ids 写入 I-* issue
