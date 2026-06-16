---
local_id: raw-20260511T1343Z
kind: raw
priority: medium
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
source: chat-inbox
created_at: '2026-05-11T13:43:00Z'
title: 'fix: empty scan should trigger stop_ai, not restart loop'
platform_state: closed
platform_ids:
  github:
    issue_id: '370'
    url: https://github.com/chatterzhao/freely/issues/370
    synced_at: '2026-05-16T13:20:51Z'
updated_at: 2026-05-17T04:47:25Z
primary_platform: github
---

## 问题

scan 没有发现待办任务时，AI 会循环重启而不是正常停止。需要在 AI prompt 和 AGENTS.md.example 中明确：scan 空不是错误，写 stop_ai。

## 修复

- `docs/system/workspace/scripts/runtime/freely`: AI prompt 模板增加空 scan 指导
- `docs/system/workspace/AGENTS.md.example`: 增加 "scan 空不是错误" 章节
