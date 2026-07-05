# Candidates - 20260429-2040--chat-inbox-sqlite

### C-20260429-2040-A: SQLite chat-inbox 暂存区

- title: `SQLite chat-inbox staging for protected-branch chat intake`
- status: `promoted`
- scope: |
  chat-inbox.py SQLite 模块、_write_chat_to_issue 改为 DB 写入、
  wt-create 前置检查+materialize、scan_chat_inbox 兜底、
  freely init 建表、consumed 三态(-1/0/1)
- priority: `P0`
- type: `architecture`
- milestone: `M-20260306-workspace-routing-foundation`
- route_kind: `chat_intake`
- phase_state: `done_pre_brainstorm`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/chat-inbox-sqlite/issues/I-20260429-2040-A.md`
- session_refs:
  - {tool: ccds, session_id: "20260429-chat-inbox-sqlite", role: "author"}
- acceptance_criteria:
  - `freely chat --new-issue` 不写 docs/issues/，develop git status 干净
  - `freely chat --issue <id>` 有工位时直接同步到 worktree
  - `freely init` 自动建 chat-inbox.db
  - `wt-create feature/raw-{ts}-xxx` 验证 issue 存在，从 DB materialize
  - `task-source-scan` 包含 consumed=0 的 chat_intake sources
  - 噪声可标记 consumed=-1 丢弃
- promotion_gate: `governance-merge-gate`
- open_questions: []
- next_action: `B2_IBM implementation.`
