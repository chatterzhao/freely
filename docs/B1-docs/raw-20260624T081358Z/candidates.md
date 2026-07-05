# Candidates

## C-20260624T081358Z-A: 测试文档 daemon 假设修复

- candidate_format_version: v2
- title: 修复 skills/AGENTS 中测试步骤的 daemon 硬编码假设
- status: promoted
- decision_reason: Freely 自举文档把 daemon 写成了通用要求，违背多项目类型设计
- next_action: B2_IBM → pr-create → pr-merge → wt-close
- acceptance_criteria:
  - fix-execution/test-execution/feat-execution 不出现 "stop/start daemon" 作为唯一测试方式
  - AGENTS.md test-pre-merge 验证段标注为 Freely 自举示例
  - 测试描述指向 pre-tests.md（B2_IBM 编写，test-execution 执行）
- promotion_gate: 文件修改完成，现有工具行为不变
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260624T081358Z-A/issue.md
- milestone: M-20260624T081358Z-A
