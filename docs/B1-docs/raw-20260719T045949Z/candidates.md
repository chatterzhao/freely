---
candidate_id: C-20260719T045949Z-A
status: promoted
source_raw: raw-20260719T045949Z
created_at: '2026-07-19'
milestone: M-20260719T045949Z-A
---

## C-20260719T045949Z-A: B1/B2 skill 补充三环能力生命周期交叉引用

- candidate_format_version: v2
- title: B1/B2 skill 补充三环能力生命周期交叉引用
- status: promoted
- decision_reason: 两个 skill 定义了 B1→B2→dev 的完整工作流，但从未显式引用三环生命周期总图。Option B（链接+上下文说明）是最小可理解方案。
- next_action: B2 物化 → dev（修改两个 SKILL.md） → 验证
- revisit_trigger: N/A
- acceptance_criteria:
  - B1 skill 末尾有"能力生命周期参考"段，说明 B1 是 doc-loop 第一阶段
  - B2 skill 末尾有"关键参考"段，聚合质量门槛+派生约束+三环引用
  - 内容方向和质量经评审确认
- promotion_gate: 两个 skill 修改完成
- open_questions: []
- acceptance_reviews:
  - reviewer: self-review
  - mode: inline
  - summary: 纯文档改进，方向正确，内容精准，无风险
  - verdict: pass
- promoted_issue_id: I-20260719T045949Z-A
- promoted_issue_path: docs/B2-docs/ibm/skill-lifecycle-reference/raw-20260719T045949Z/issues/I-20260719T045949Z-A.md
- milestone: M-20260719T045949Z-A
- session_refs: []
