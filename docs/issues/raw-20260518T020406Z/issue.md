---
local_id: raw-20260518T020406Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260518T020406Z-A
platform_ids:
  github:
    issue_id: '539'
    url: https://github.com/chatterzhao/freely/issues/539
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-18T02:04:19Z'
updated_at: '2026-06-13T10:47:18Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## raw-20260518T020406Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260518T020406Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-05-18T02:04:06Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260518T020406Z`。实现前请用 `wt-create --raw-key 20260518T020406Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
phase_state: proposed
source: feedback
created_at: "2026-05-18T02:04:06Z"
title: "chats 表扩展 conversation_id + chat-message 类型 + scan 对齐"

## 依赖

- #538 freely comment 命令（聊天模型和评论命令共同构成 chat 体系）

## 改动

### 1. chats 表扩展（不新增表）

```sql
ALTER TABLE chats ADD COLUMN conversation_id INTEGER DEFAULT 0;
```

- `conversation_id=0`：独立消息（new-issue / comment），不属对话
- `conversation_id=N`：属于对话，N=首条消息 id

### 2. 新增 `chat-message` 类型

- 自由对话中的消息，物化时才决定去向（新建 raw issue 还是追加评论）
- 新增 `consume_conversation(conversation_id)` 函数：批量消费对话所有消息

### 3. scan 新增 stage

- `chat_conversation_pending`：未消费的对话（`conversation_id>0 AND consumed=0`）

## 位置

- `docs/system/workspace/scripts/runtime/chat-inbox.py`
- `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py` — `scan_chat_inbox`
- `docs/system/workspace/scripts/runtime/freely` — `cmd_chat`

## 参考

B1 文档：`docs/pre-brainstorms/issue-state-lifecycle.md` §6, §7.3
