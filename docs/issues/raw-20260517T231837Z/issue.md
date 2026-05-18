---
local_id: raw-20260517T231837Z
kind: raw
status: proposed
phase_state: proposed
platform_ids:
  github:
    issue_id: '533'
    url: https://github.com/chatterzhao/freely/issues/533
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-17T23:18:50Z'
updated_at: '2026-05-17T23:18:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## raw-20260517T231837Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260517T231837Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-17T23:18:37Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260517T231837Z`。实现前请用 `wt-create --raw-key 20260517T231837Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P1
status: open
source: chat-inbox
created_at: "2026-05-17T23:18:37Z"
title: "梳理 issue 状态管理：phase_state 生命周期、消费时序、写入收口"

## 问题

当前 raw issue 和 I-* issue 的 `phase_state` 管理存在断层。三种内容源（chat-inbox new-issue、chat-inbox comment、platform issue）的消费和状态转换逻辑不统一，部分转换依赖手动脚本，部分缺少自动触发。

## 三种内容源

1. **freely.db chats 表 — `chat_type=new-issue`**：用户插话无法归入已有 issue，需新建 raw issue。`consumed` 字段由 `chat-inbox.py consume` 管理
2. **freely.db chats 表 — `chat_type=comment`**：对已有 raw issue 的补充评论。`consumed` 字段同上
3. **Platform (GitHub/Gitee)**：平台上的 raw issue，无 `consumed` 字段，`phase_state` 从 labels 解析

## 当前断层

- `chat-inbox.py materialize` 写出 `status: proposed` 但没有 `phase_state`
- `wt-create` 消费后只更新 `chats.consumed=1`，不更新 `issue.md` 的 `phase_state`
- Platform raw issue 在 wt-create 后完全没有消费追踪
- 已关闭的 issue 仍可被写入评论（scan 已不再扫封闭 issue，写入即丢失）
- 已消费的 raw issue 的评论应写入其 I-* 子 issue，而非 raw issue

## 需要梳理

- `phase_state` 完整状态机和各状态的进入/退出条件
- 哪些转换由脚本/命令自动触发（确定性），哪些由 AI 语义判断
- scan 如何"收口"——封闭状态不应再被扫描
- wt-create 消费时如何根据 `--source` 自动更新状态
