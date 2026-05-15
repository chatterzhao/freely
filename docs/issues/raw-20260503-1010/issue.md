---
local_id: raw-20260503-1010
kind: raw
priority: high
status: open
phase_state: proposed
source: chat-inbox
created_at: '2026-05-03T10:10:00Z'
title: 'fix: SQLite busy_timeout=0 causes concurrent write failures'
platform_ids:
  github:
    issue_id: '347'
    url: https://github.com/chatterzhao/freely/issues/347
    synced_at: '2026-05-15T18:24:27Z'
updated_at: '2026-05-15T18:24:27Z'
primary_platform: github
platform_state: open
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
