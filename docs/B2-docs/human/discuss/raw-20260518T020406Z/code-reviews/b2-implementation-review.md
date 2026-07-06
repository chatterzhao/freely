# Code Review
- issue_id: I-20260518T020406Z-A
- issue_path: docs/issues/I-20260518T020406Z-A/issue.md
## Implementation Decision Note
- decision: chats 表新增 conversation_id 列（DEFAULT 0），chat-message 类型支持自由对话，consume_conversation 批量消费，scan_chat_inbox 新增 chat_conversation_pending 分组 stage，freely chat --conversation CLI 触发
- why_this: chat 体系的第三个类型（chat-message）允许自由对话消息先在数据库中积累，物化时才决定去向（新建 raw issue 或追加评论）。conversation_id=0 默认值确保向后兼容，不需新增表
- alternatives_considered: (1) 新增独立 conversation 表 — 更规范化但引入新表复杂度 (2) daemon 侧维护活跃 conversation 状态 — 增加 daemon 复杂度，本次不实现 (3) TUI 内隐式对话检测 — 增加交互复杂度，作为备选方案
- boundary_non_goals: 不新增表，不实现 TUI 内隐式对话检测，不修改 daemon 侧活跃 conversation 状态管理，不修改 ACP bridge 或 fleet supervision
- residual_risk: conversation_id 首条消息 auto-update 依赖 INSERT 后的 UPDATE 时序，若中间有并发插入可能错位 — 缓解：chat-inbox 单线程写入，并发风险低
