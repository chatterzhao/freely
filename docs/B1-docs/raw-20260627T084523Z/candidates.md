---
candidate_id: C-20260627T084523Z-A
status: promoted
source_raw: raw-20260627T084523Z
created_at: 2026-06-27
milestone: M-20260627T084523Z-A
---

## C-20260627T084523Z-A: legacy issue

- candidate_format_version: v2
- title: Agent 生命周期管理 — 僵尸清理、并发控制、session 关闭
- status: promoted
- decision_reason: 5 个 Bug 共享同一份 agent-id.env + a2a_tasks 数据面，一起修避免碎片化
- next_action: B2_IBM → dev → pr-merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - Bug A: 委派前调 reconcile，agent-id.env 僵尸条目归零
  - Bug B: sync_tooling 选空闲 worker，不再重复分配 worker_01
  - Bug C: sync_tooling 加并发检查，不绕过 10:7 限流
  - Bug D: 僵尸 session 通过 reconcile 关闭
  - Bug E: wt-close Phase6 调 _acp_session_close
  - pool=10 真正生效
- promotion_gate: 所有改动完成，freely daemon 启动后 agent-id.env 无僵尸，worker 分配均匀
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: subagent
  - summary: 审查 agent-id.env 生命周期完整性，验证 5 个 Bug 修复
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260627T084523Z-A/issue.md
- milestone: M-20260627T084523Z-A
- session_refs: []
