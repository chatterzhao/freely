---
candidate_id: C-20260625T084506Z-A
status: promoted
source_raw: raw-20260625T084506Z
created_at: 2026-06-25
milestone: M-20260625T084506Z-A
---

## C-20260625T084506Z-A: legacy issue

- candidate_format_version: v2
- title: B2_IBM skill 加入 pre-tests.md 反糊弄铁律 + gate 端到端/集成测试层级检查
- status: promoted
- decision_reason: AI 写 pre-tests.md 时缺乏反糊弄约束，容易全 mock 绕过；gate 已有反作弊但 skill 层缺失预防性指导
- next_action: 合并到 develop → 关闭 #3494
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - B2_IBM SKILL.md: pre-tests.md 模板前有醒目反糊弄铁律警告
  - 警告包含：禁止全 mock、禁止 ghost pass、not_applicable 必须写理由
  - 警告包含：端到端测试和集成测试是 AI 编程防失败最重要保证
  - 警告语言：糊弄是导致项目失败的严重失职行为
  - pretests-retirement-gate: 新增端到端/集成测试层级充分性硬拦截
- promotion_gate: 修改完成且语法无误
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - summary: 检查 B2_IBM SKILL.md 反糊弄铁律语言力度和 gate E2E/集成检查逻辑
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260625T084506Z-A/issue.md
- milestone: M-20260625T084506Z-A
- session_refs: []
