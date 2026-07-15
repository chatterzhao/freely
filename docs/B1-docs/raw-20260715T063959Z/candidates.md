---
candidate_id: C-20260715T063959Z-A
status: promoted
source_raw: raw-20260715T063959Z
created_at: 2026-07-15
milestone: M-20260715T063959Z-A
---

## C-20260715T063959Z-A: revert AI_MODE default wait→auto

- candidate_format_version: v2
- title: revert AI_MODE default from wait back to auto
- status: promoted
- decision_reason: AI_MODE=Claude交互姿态，只支持auto/step。wait为无效值导致tool_unproductive。task_mode默认值wait不受影响。
- next_action: B2→dev 实现
- revisit_trigger: N/A
- acceptance_criteria:
  - 6 处 AI_MODE:-wait → AI_MODE:-auto
  - 3 处 AI_MODE:-none 保持不变
  - bash -n 通过
  - daemon 启动后 AI launch 不再报 unsupported mode
- promotion_gate: bash -n + code review
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: manual
  - summary: 确认 AI_MODE/task_mode 概念区分正确
  - verdict: pass
- promoted_issue_id: I-20260715T063959Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20260715T063959Z/issues/I-20260715T063959Z-A.md
- milestone: M-20260715T063959Z-A
- session_refs: []
