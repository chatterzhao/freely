---
candidate_id: C-20260717T090202Z-A
status: promoted
source_raw: raw-20260717T090202Z
created_at: 2026-07-17
milestone: M-20260717T090202Z-A
---

# Candidates

## C-20260717T090202Z-A: peak 口径限定为死亡记录

- candidate_format_version: v2
- title: storm window kind 列 + peak 死亡行口径
- status: promoted
- decision_reason: 健康态恒 3 使 PEAK 失真；death 行计峰恢复 churn 语义。见 brainstorms Option B
- next_action: 收敛 PR → merge → wt-close
- revisit_trigger: N/A
- acceptance_criteria:
  - 沙箱：cycle 记录不触发 peak；death 记录触发
  - E2E：真实 daemon auto 短窗零 restart_storm_pause
  - capability-lifecycle 口径说明在位
- promotion_gate: 生产实抓 + 口径分析
- open_questions: []
- acceptance_reviews:
  - reviewer: inline-regression-audit
  - mode: inline
  - summary: 自查回归；awk OR→AND 条件缺陷在 GREEN 前自纠并留痕
  - verdict: pass
- promoted_issue_id: I-20260717T090202Z-A
- promoted_issue_path: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T090202Z/issues/I-20260717T090202Z-A.md
- milestone: M-20260717T090202Z-A
- session_refs: []
