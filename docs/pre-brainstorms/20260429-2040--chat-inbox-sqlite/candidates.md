# Candidates - 20260429-2040--chat-inbox-sqlite

### C-20260429-2040-A: SQLite chat-inbox 替代 docs/issues/ 直接写入

- title: `SQLite chat-inbox for protected-branch chat intake`
- status: `proposed`
- scope: |
  1. `.freely/chat-inbox.db` — SQLite 数据库，chats 表
  2. `freely chat --new-issue` → INSERT chat（不写入 docs/issues/）
  3. `freely chat --issue <id>` → INSERT chat（同上）
  4. `task-source-scan.py::scan_chat_inbox()` → SELECT pending chats
  5. AI agent 消费后：new-issue → worktree materialize；comment → 追加+absorb 重定向
- priority: `P0`
- type: `architecture`
- milestone: `M-20260306-workspace-routing-foundation`
- route_kind: `chat_intake`
- phase_state: `pre_brainstorm`
- promoted_issue_path: `pending://`
- session_refs:
  - {tool: ccds, session_id: "20260429-chat-inbox-sqlite", role: "author"}
- acceptance_criteria:
  - `freely chat --new-issue` 不写入 `docs/issues/`，develop 无变更
  - SQLite 写入 + 索引查询，pending scan O(log n)
  - raw issue 被 absorb 后，评论自动重定向到 I-*
  - 已关闭 issue 的评论有明确处理策略
- promotion_gate: `governance-merge-gate`
- open_questions:
  - 已关闭 issue 的评论：自动转 new-issue 还是标 error？
  - materialized 记录保留策略（定期 VACUUM？）
- acceptance_reviews: []
- next_action: `Resolve open questions, then promote to B2_IBM implementation.`
