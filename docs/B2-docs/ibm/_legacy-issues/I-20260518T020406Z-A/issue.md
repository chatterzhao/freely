---
local_id: I-20260518T020406Z-A
kind: linked
phase_state: completed
promoted_from: raw-20260518T020406Z06Z
source_candidate: docs/B1-docs/raw-20260518T020406Z06Z/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '539'
    url: https://github.com/chatterzhao/freely/issues/539
primary_platform: github
last_synced_comment_at: {}
hash: ''
created_at: 2026-05-18 02:04:06+00:00
updated_at: '2026-05-19T00:03:00Z'
intake_id: ''
author: zhaoquan
channel: manager-promotion
session_refs: []
pre_tests_path: ''
verification_artifact_dir: 'docs/B2-docs/human/discuss/code-reviews'
platform_state: closed
---

# I-20260518T020406Z-A: chats 表扩展 conversation_id + chat-message 类型 + scan 对齐

- source_candidate: `docs/B1-docs/raw-20260518T020406Z06Z/candidates.md`
- execution_base: `develop`
- integration_target: `develop`

## 目标

在 chats 表新增 conversation_id 列，支持 chat-message 类型和自由对话模式，让 chat 消息先积累再决定去向。

## 范围

1. chats 表 ALTER TABLE ADD conversation_id INTEGER DEFAULT 0
2. chat_type 新增 'chat-message' 类型（chat-inbox.py add_chat 无校验）
3. consume_conversation(conversation_id, action, target) 批量消费函数
4. scan_chat_inbox 新增 chat_conversation_pending 分组 stage（task-lifecycle-scan.py）
5. scan_chat_inbox 的 WHERE 排除 conversation_id>0 的 chat-message
6. freely chat --conversation CLI 触发方式（cmd_chat / submit_human_frontdoor_message）
7. 首条消息 conversation_id = 自身 id 的 UPDATE 逻辑

## 不在范围

- 不新增表
- 不实现 TUI 内隐式对话检测（备选方案）
- 不修改 daemon 侧的活跃 conversation 状态管理
- 不修改 ACP bridge 或 fleet supervision

## Acceptance

- chats 表新增 conversation_id 列（DEFAULT 0），现有记录 conversation_id=0
- chat-message 类型的消息可写入 chats 表，不影响现有 new-issue/comment
- consume_conversation(conversation_id, "materialize", dir_path) 将对话消息合并为 raw issue
- consume_conversation(conversation_id, "materialize-all-as-comment", issue_path) 将对话消息追加为评论
- scan_chat_inbox 输出新增源类型 source_family=chat_conversation_pending，stage=chat_conversation_pending
- scan_chat_inbox 的 chat_waiting_worktree/chat_ready 分组排除 conversation_id>0 的消息
- freely chat --conversation <msg> 创建或追加到活跃对话
- freely chat --conversation --new <msg> 显式创建新对话
- 首条消息 INSERT 后 conversation_id 自动 UPDATE 为自身 id
- conversation_id=0 的现有 new-issue/comment 行为完全不变
