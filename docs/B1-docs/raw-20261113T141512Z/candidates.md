---
candidate_id: C-20261113T141512Z-A
status: promoted
source_raw: raw-20261113T141512Z
created_at: 2026-11-13
milestone: M-20261113T141512Z-A
---

## C-20261113T141512Z-A: 只读视图不因空 agent_working 失败
- candidate_format_version: v2
- title: status 空表降级 + scan 负向控制
- status: promoted
- design_verdict: 实现偏差
- anchor_refs:
  - runtime/freely:4535-4538（空表 fail-closed）
  - owner_lane.py:127（claim 语义）
  - #4699/_already_on_platform（scan 平台判据）
- decision_reason: 空表是正常状态；只读视图不应复用写入路径的 fail-closed。
- acceptance_criteria:
  - status --view live 在空 agent_working 时 rc=0 且输出 issue 段。
  - 写入/委派路径仍 fail-closed（回归）。
  - scan 无 scan-state 时不误报历史 legacy CREATE（#4699 平台判据）。
- promotion_gate: 实证 status rc=1 与 scan 现状。
- next_action: B2 → RED → dev。
- revisit_trigger: 若 agent-table 改为可空身份契约，重新审视。
- open_questions: []
- acceptance_reviews:
  - reviewer: main-agent
  - mode: B0-five-layer-audit
  - verdict: pass
- promoted_issue_id: I-20261113T141512Z-A
- promoted_issue_path: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261113T141512Z/issues/I-20261113T141512Z-A.md
- milestone: M-20261113T141512Z-A
- session_refs: []
