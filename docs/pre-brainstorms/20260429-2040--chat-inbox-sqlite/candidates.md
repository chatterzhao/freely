# Candidates - 20260429-2040--chat-inbox-sqlite

### C-20260429-2040-A: SQLite chat-inbox 暂存区

- title: `SQLite chat-inbox staging for protected-branch chat intake`
- status: `proposed`
- scope: |
  **新增**: `chat-inbox.py` 模块（init/insert/query/consume）
  **修改**: `_write_chat_to_issue` → SQLite 写入, `freely init` → 建表, `task-source-scan.py` → 新增 scan_chat_inbox
  **不变**: scan_raw_issues, scan_linked_issues, governance-merge-gate, AI agent, issue-sync, B1/B2 全流程
- priority: `P0`
- type: `architecture`
- milestone: `M-20260306-workspace-routing-foundation`
- route_kind: `chat_intake`
- phase_state: `pre_brainstorm`
- session_refs:
  - {tool: ccds, session_id: "20260429-chat-inbox-sqlite", role: "author"}
- acceptance_criteria:
  - `freely chat` 不污染 develop
  - `freely init` 自动建表
  - 消费后 chat 原样进入 `docs/issues/`，Git 可跟踪
  - raw→I absorb 评论重定向正确
  - 已有组件（gate/AI/sync）零改动
- promotion_gate: `governance-merge-gate`
- open_questions: []
- next_action: `Confirm scope, promote to B2_IBM.`
