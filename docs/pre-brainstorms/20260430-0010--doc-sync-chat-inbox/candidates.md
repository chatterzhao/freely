# Candidates - 20260430-0010--doc-sync-chat-inbox

### C-20260430-0010-A

- title: `Sync docs + fix governance-only paths for architecture docs`
- status: `promoted`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/chat-inbox-sqlite/issues/I-20260429-2040-A.md`
- scope: |
  1. 添加 ibm-framework.md 等核心架构文档到 is_governance_only_path
  2. 同步 chat-issue-routing、source-classification、three-loop 文档
- priority: `P1`
- type: `documentation`
- milestone: `M-20260306-workspace-routing-foundation`
- route_kind: `continuation`
- phase_state: `done_pre_brainstorm`
- session_refs:
  - {tool: ccds, session_id: "20260430-doc-sync", role: "author"}
- acceptance_criteria:
  - 纯文档改动可通过 governance_only_merge 路径
  - ibm-framework.md 反映 chat-inbox 流程
- promotion_gate: `governance-merge-gate`
- open_questions: []
- acceptance_reviews: []
- next_action: `Merge to develop.`
