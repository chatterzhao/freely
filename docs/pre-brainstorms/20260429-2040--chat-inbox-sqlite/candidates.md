# Candidates - 20260429-2040--chat-inbox-sqlite

### C-20260429-2040-A: SQLite chat-inbox 暂存区

- title: `SQLite chat-inbox staging for protected-branch chat intake`
- status: `proposed`
- scope: |
  1. `.freely/chat-inbox.db` — SQLite，id=UTC时间戳，consumed=0/1
  2. `freely chat` → INSERT，不写 `docs/issues/`
  3. `task-source-scan.py` → SELECT WHERE consumed=0 → 消费 → UPDATE consumed=1
  4. 消费后进入 `docs/issues/`（git 跟踪）→ AI 读文件 → issue-sync 推平台
- priority: `P0`
- type: `architecture`
- milestone: `M-20260306-workspace-routing-foundation`
- route_kind: `chat_intake`
- phase_state: `pre_brainstorm`
- session_refs:
  - {tool: ccds, session_id: "20260429-chat-inbox-sqlite", role: "author"}
- acceptance_criteria:
  - `freely chat` 不污染 develop
  - SQLite `WHERE consumed=0` 索引扫描 O(log n)
  - 消费后 issue 进入 `docs/issues/`，Git 可跟踪
  - raw→I absorb 重定向正确
- promotion_gate: `governance-merge-gate`
- open_questions: []
- next_action: `Confirm design, promote to B2_IBM implementation.`
