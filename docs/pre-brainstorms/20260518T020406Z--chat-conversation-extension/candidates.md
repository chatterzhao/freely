# Candidates — 20260518T020406Z--chat-conversation-extension

## C-20260518T020406Z-A: chats 表扩展 conversation_id + chat-message 类型 + scan 对齐

- candidate_format_version: v2
- title: chats 表扩展 conversation_id + chat-message 类型 + scan 对齐
- status: promoted
- decision_reason: Raw issue #539 提出 chat 体系的第三个类型（chat-message），允许自由对话消息先在数据库中积累，物化时才决定去向（新建 raw issue 或追加评论）。依赖的 #538 freely comment 已合并到 develop，comment 基础设施可用。改动范围明确（不新增表），向后兼容（conversation_id=0 默认值）。
- next_action: B2_IBM materialize → 实现 schema 扩展（ALTER TABLE）+ consume_conversation() + scan stage + --conversation CLI
- revisit_trigger: 若 chat-inbox.py 或 scan_chat_inbox 在本次 worktree 存活期间有重大重构，需同步更新；若 #538 的 materialize-comment 接口发生变化，需更新 consume_conversation 的 comment 路径
- acceptance_criteria:
  - chats 表新增 conversation_id 列（DEFAULT 0）
  - chat-message chat_type 可写入 chats 表
  - consume_conversation(conversation_id, action, target) 批量消费并物化
  - scan_chat_inbox 新增 chat_conversation_pending 分组 stage
  - scan_chat_inbox 的 WHERE 条件排除 conversation_id>0 的 chat-message（避免重复计数）
  - freely chat --conversation 可创建或追加到对话
  - conversation_id=0 的现有 new-issue / comment 行为不变
  - 首条消息的 conversation_id 赋值为自身 id 的 UPDATE 逻辑完整
- promotion_gate: schema 扩展 + consume_conversation + scan stage + CLI 触发 — 四项均实现且通过 governance-merge-gate
- open_questions:
  - consume_conversation 的 materialize 合并策略：多条对话消息合并为一条 raw issue 时，是用分隔符连接还是分别写入不同 section？
  - conversation 的"活跃状态"如何追踪？daemon 侧是否需要维护活跃 conversation 的会话状态？
- acceptance_reviews: []
- promoted_issue_path: "docs/issues/I-20260518T020406Z-A/issue.md"
- milestone: M-20260518T020406Z-A
- session_refs: []
