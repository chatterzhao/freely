---
local_id: raw-20260503T101000Z
kind: raw
priority: high
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
source: chat-inbox
created_at: '2026-05-03T10:10:00Z'
title: 'fix: SQLite busy_timeout=0 causes concurrent write failures'
platform_state: closed
platform_ids:
  github:
    issue_id: '373'
    url: https://github.com/chatterzhao/freely/issues/373
    synced_at: '2026-05-16T13:21:36Z'
updated_at: '2026-06-17T00:23:37Z'
primary_platform: github
---
## 问题
chat-inbox.py 和 session-store.py 设了 WAL 但 busy_timeout=0。
worker delegation 并发写时第二个 writer 立即 SQLITE_BUSY。

## 根因
- 两个独立进程同时写同一个 SQLite DB
- WAL 模式允许并发读但不允许并发写
- busy_timeout=0 意味着写冲突时立即失败，不重试

## 修复
对所有 DB 操作设 PRAGMA busy_timeout=5000，让写冲突时等待最多 5 秒。
涉及文件: handoff.py, chat-inbox.py, session-store.py 等。
