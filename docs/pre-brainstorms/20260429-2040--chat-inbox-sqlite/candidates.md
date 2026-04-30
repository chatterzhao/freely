# Candidates - 20260429-2040--chat-inbox-sqlite

### C-20260429-2040-A: SQLite chat-inbox 替代 docs/issues/ 直接写入

- title: `SQLite chat-inbox with script-driven consumption`
- status: `proposed`
- scope: |
  1. `.freely/chat-inbox.db` — SQLite，`chats` 表，id=UTC时间戳，consumed=0/1
  2. `freely chat` → INSERT，不写 docs/issues/
  3. `task-source-scan.py` → SELECT pending → 消费 → UPDATE consumed=1
  4. 消费时按 chat_type 分三路：new-issue / comment+absorb / orphan
  5. AI agent 只消费 scan JSON，不接触 SQLite
- priority: `P0`
- type: `architecture`
- milestone: `M-20260306-workspace-routing-foundation`
- route_kind: `chat_intake`
- phase_state: `pre_brainstorm`
- session_refs:
  - {tool: ccds, session_id: "20260429-chat-inbox-sqlite", role: "author"}
- acceptance_criteria:
  - `freely chat` 不污染 develop
  - SQLite 索引扫描 O(log n)
  - raw→I absorb 重定向正确
  - 已关闭 issue 评论不丢失（标 orphan 或转 new-issue）
- promotion_gate: `governance-merge-gate`
- open_questions: []
- next_action: `User confirms design, promote to B2_IBM implementation.`
