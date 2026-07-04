---
candidate_id: C-20260704T064539Z-A
status: promoted
source_raw: raw-20260704T064539Z
created_at: 2026-07-04
milestone: M-20260704T064539Z-A
---

## C-20260704T064539Z-A: 统一 ACP session 管理方法

- candidate_format_version: v2
- title: 抽象统一 ACP session 管理方法 + 重命名 CLAUDE_SESSION_ID_CURRENT
- status: promoted
- decision_reason: |
  三个 agent role 的 session 创建逻辑分散在 3 处，参数传递不一致。
  Option A (Python 统一封装) 是最小改动方案——只需在 agent_working.py 增加入口，
  三个调用点改为调用它，不需要跨语言协调。
- next_action: B2 设计 → dev 实现 → merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - agent_working.py 新增 acp_session_register(project, raw_key, role, agent_id, session_id, slot, worktree, branch, ...)
  - Manager 写入 session_id 不为空、slot 正确
  - Worker 写入完整（已验证 OK 的部分不变，补 slot）
  - Reviewer 写入 worktree、branch
  - CLAUDE_SESSION_ID_CURRENT → TOOL_SESSION_ID_CURRENT (3 文件 11 处)
- promotion_gate: 三个调用点改为统一入口，参数完整
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: plan-subagent
  - summary: 审查 ACP session 管理统一方案，确认抽象合理
  - verdict: pass
- promoted_issue_id: I-20260704T064539Z-A
- promoted_issue_path: docs/epics/{epic-name}/{story-name}/raw-20260704T064539Z/issues/I-20260704T064539Z-A.md
- milestone: M-20260704T064539Z-A
- session_refs: []
