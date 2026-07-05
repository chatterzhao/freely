---
candidate_id: C-20260627T062554Z-A
status: promoted
source_raw: raw-20260627T062554Z54Z
created_at: 2026-06-27
milestone: M-20260627T062554Z-A
---

## C-20260627T062554Z-A: legacy issue

- candidate_format_version: v2
- title: task-lifecycle-scan v3 — 三分类重构
- status: promoted
- decision_reason: 旧 scan 8 项 source_family 归结为 3 类，数据验证通过
- next_action: B2_IBM → dev → pr-merge
- revisit_trigger: N/A
- acceptance_criteria:
  - 三类分叉正确（实测 5 类测试用例全部通过）
  - 不再产生 push=176 误报
  - Chat inbox 正确扫描
  - 平台检测不硬编码
  - 性能：冷 ~11s，热 0.04s
- promotion_gate: scan 输出与手动统计一致，freely daemon 可用新 scan 结果
- open_questions: []
- acceptance_reviews:
  - reviewer: claude; mode: subagent; verdict: pass
- promoted_issue_path: docs/issues/I-20260627T062554Z-A/issue.md
- milestone: M-20260627T062554Z-A
- session_refs: []
