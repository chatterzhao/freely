---
candidate_id: C-20260701T085407Z-A
status: promoted
source_raw: raw-20260701T085407Z
created_at: 2026-07-01
milestone: M-20260701T085407Z-A
---

## C-20260701T085407Z-A: A2A reviewer restore + routing + session

- candidate_format_version: v2
- title: 修 _restore_tasks 优先级 + reviewer 专属恢复 + _ensure_reviewer_agent session
- status: promoted
- decision_reason: 泳道图揭示 3 个缺失。逐项修复 a2a_server.py 括号、新增 reviewer 恢复分支、ensure_reviewer_agent 支持参数+session
- next_action: B2 设计 → dev 实现 → test → PR
- revisit_trigger: daemon 重启时 reviewer task 恢复异常
- acceptance_criteria:
  - a2a_server.py: and/or 优先级修正 + reviewer 专属 _restore_tasks 分支
  - freely: _ensure_reviewer_agent 接受 reviewer_id 参数 + ACP session 启动
- promotion_gate: 3 项修复 + 语法验证 + 逻辑审查
- open_questions:
  - Reviewer 和 Manager 共用 ACP bridge session 有无冲突？
- promoted_issue_id: I-20260701T085407Z-A
- promoted_issue_path: docs/epics/reviewer-agent/a2a-restore-fix/raw-20260701T085407Z/issues/I-20260701T085407Z-A.md
- milestone: M-20260701T085407Z-A
- session_refs: []
