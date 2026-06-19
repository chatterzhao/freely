---
candidate_id: C-20260619T043000Z-A
status: promoted
source_raw: raw-20260619T043000Z
created_at: 2026-06-19
milestone: M-20260619T043000Z-A
---

## C-20260619T043000Z-A: IBM治理快速达标

- candidate_format_version: v2
- title: IBM治理快速达标 — skill门禁常见坑速查+规范模板+gate报错引导
- status: promoted
- decision_reason: B1/B2 skill 示例正确但无速查表，gate报错无skill引导，PR #3021因## heading问题失败10+次
- next_action: 修改B1/B2 skill加门禁常见坑速查和规范模板；改gate报错加skill footer引导
- revisit_trigger: N/A（已promote）
- acceptance_criteria:
  - B1 skill: 门禁常见坑速查表含5+条目 + candidates.md完整模板 + brainstorms.md模板
  - B2 skill: 门禁常见坑速查表含5+条目 + I-* issue模板 + Implementation Decision Note模板 + code-review模板
  - gate: 报错后打印分组footer指向B1/B2 skill对应章节
  - 格式约定: 沿用fix-execution已有`## 门禁常见坑速查`命名
- promotion_gate: 修改完成且格式校验通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.8
  - mode: plan-subagent
  - summary: 评审通过，修正5处：heading命名、表格条目扩展、gate footer替代逐条追加、模板完整性、FREELY_SKIP_IBM_GATE适用性
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260619T043000Z-A/issue.md
- milestone: M-20260619T043000Z-A
- session_refs: []
