---
candidate_id: C-20260711T083155Z-A
status: promoted
source_raw: raw-20260711T083155Z
created_at: 2026-07-11
milestone: M-20260711T083155Z-A
---

## C-20260711T083155Z-A: A2A→SSE→ACP 消息投递链修复 + SQLite 友好校验

- candidate_format_version: v2
- title: A2A→SSE→ACP 消息投递链修复 + SQLite 友好校验层
- status: promoted
- decision_reason: 消息投递是 agent 协作基础设施，断裂导致 Manager→Worker 单向通信全部丢失。SQLite 校验层让 AI 知道写错了什么、怎么改。
- next_action: 进入 B2 → dev-loop → test → PR
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - Manager a2a_task.py prompt → Worker ACP session/prompt 收到消息
  - 空 content 写入 → 返回 422 + fix_hint + example
  - 非法 role 写入 → 返回 422 + 合法值列表
  - 不存在的 task_id → 返回 422 + 如何查正确 task_id
- promotion_gate: 4 文件修改完成 + PR merge
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 审查 A2A→SSE→ACP 全链路是否打通，校验层是否友好
  - verdict: pass
- promoted_issue_id: I-20260711T083155Z-A
- promoted_issue_path: docs/B2-docs/a2a/message-delivery/raw-20260711T083155Z/issues/I-20260711T083155Z-A.md
- milestone: M-20260711T083155Z-A
- session_refs: []
