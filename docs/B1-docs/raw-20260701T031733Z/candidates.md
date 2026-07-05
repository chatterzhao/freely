---
candidate_id: C-20260701T031733Z-A
status: promoted
source_raw: raw-20260701T031733Z
created_at: 2026-07-01
milestone: M-20260701T031733Z-A
---

## C-20260701T031733Z-A: legacy issue

- candidate_format_version: v2
- title: 修正 5 个 skill 模板/检查清单，减少门禁反复失败
- status: promoted
- decision_reason: 3 个 PR 共 15+ 次门禁失败均源于 skill 模板缺字段或漏步骤，源头修正最有效
- next_action: B2 设计 → dev 逐文件修改 → test 验证
- revisit_trigger: 下次门禁仍然反复失败时重新审视是否需要 pre-flight 代码
- acceptance_criteria:
  - B1 candidates.md 模板含 `promoted_issue_path` 示例
  - B2 pre-tests.md 模板无反引号、含 .log force-add 提醒、section 格式正确
  - B2 完成自检清单含 epics-map.svg 更新
  - dev-loop skill 含"提交后 merge 到 test"提醒
  - test-execution skill 同步步骤为 merge 优先
  - workflow-guarded skill 阶段 5 含 dev↔test 同步步骤
- promotion_gate: 5 个 skill 文档修改完成，格式正确
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-code
  - mode: subagent
  - summary: 逐文件对比 gate 规则，确认模板字段完整
  - verdict: pass
- promoted_issue_id: I-20260701T031733Z-A
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260701T031733Z-A/issue.md
- milestone: M-20260701T031733Z-A
- session_refs: []
