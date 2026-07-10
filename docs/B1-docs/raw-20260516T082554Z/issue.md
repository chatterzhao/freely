---
local_id: raw-20260516T082554Z54Z
kind: raw
phase_state: absorbed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '361'
    url: https://github.com/chatterzhao/freely/issues/361
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T08:26:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-16T08:31:37Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
absorbed_into: raw-20260710T005219Z---

## raw-20260516T082554Z54Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T082554Z54Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T08:25:54Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T082554Z54Z`。实现前请用 `wt-create --raw-key 20260516T082554Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T08:25:54Z"
title: "handoff.py init_db 缺少 schema migration，旧项目 DB 无新增列导致 INSERT 失败"

## 根因

#360 修复了 `stop_reason=end_turn` 导致的正则匹配失败，但 runtime 仍然报 `exit_kind=error`。

进一步调试发现真正原因：`handoff.py init_db()` 使用 `CREATE TABLE IF NOT EXISTS`——当表已存在（旧 schema）时，不会添加新列。

#344 新增了 `previous_worker_handoff_id`、`last_activity_at` 等列，但旧项目（如 evot）的 `freely.db` 是旧 schema，Manager handoff INSERT 时因缺列而崩溃。

## 修复

在 `init_db()` 的 `conn.commit()` 之前加 schema migration：
1. 用 `PRAGMA table_info(handoffs)` 检查已有列
2. 对缺失的列执行 `ALTER TABLE handoffs ADD COLUMN`
3. 合并旧版 `blocked_reason` / `handoff_reason` → `reason`

## 影响

所有用旧版 freely 初始化的项目在更新后都会遇到同样问题——Manager handoff 永远失败。
