---
local_id: raw-20260503T093000Z00Z
kind: raw
priority: medium
- phase_state: absorbed
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
- phase_state: absorbed
source: platform
platform_ids:
  github:
    issue_id: "181"
    owner: chatterzhao
    repo: freely
created_at: "2026-05-03T09:30:00Z"
title: "feat: webhook receiver for realtime platform issue sync"
platform_state: closed
---
## 问题
平台 issue 变化 → webhook POST → freely receiver → issue-sync → docs/B1-docs/raw-*

支持 GitHub issues/issue_comment 和 Gitee issue_hooks/note_hooks。

## 要求
- Webhook receiver endpoint
- 验证签名
- 触发 issue-sync
