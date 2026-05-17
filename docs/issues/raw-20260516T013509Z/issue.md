---
local_id: raw-20260516T013509Z
kind: raw
phase_state: completed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '353'
    url: https://github.com/chatterzhao/freely/issues/353
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T01:35:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## raw-20260516T013509Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T013509Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T01:35:09Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T013509Z`。实现前请用 `wt-create --raw-key 20260516T013509Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T01:35:09Z"
title: "规范 Manager↔Worker 语义化委派契约：因果理由 + 验证职责"

## 背景

当前 Freely 的 Manager→Worker 委派链路缺少因果推理约束：

- Manager 写 Worker prompt 时只要求 `## Task` 步骤列表，不需要解释因为什么所以做什么
- Worker 收到 prompt 后直接执行，没有验证 Manager 理由是否仍成立的职责
- 已有 `worker-agent.md` 第 6 行先审视
