---
candidate_id: C-20260625T084522Z-A
status: promoted
source_raw: raw-20260625T084522Z
created_at: 2026-06-25
milestone: M-20260625T084522Z-A
---

## C-20260625T084522Z-A: legacy issue

- candidate_format_version: v2
- title: test-execution skill 增加 pre-tests.md 可执行性检查
- status: promoted
- decision_reason: 在执行端拦截糊弄测试方案，形成写-审-跑三道防线
- next_action: 合并到 develop → 关闭 #3495
- revisit_trigger: N/A
- acceptance_criteria:
  - test-execution SKILL.md: 新增步骤 4（可执行性检查）
  - 5 项检查清单 + 占位符检测模式
  - 门禁拦截表新增 3 个硬拦截项
  - 糊弄测试是导致项目失败的严重失职行为
- promotion_gate: 修改完成且语法无误
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - summary: 检查 test-execution 可执行性检查逻辑完整性
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260625T084522Z-A/issue.md
- milestone: M-20260625T084522Z-A
- session_refs: []
