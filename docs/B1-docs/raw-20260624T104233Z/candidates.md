---
candidate_id: C-20260624T104233Z-A
status: promoted
source_raw: raw-20260624T104233Z
created_at: 2026-06-24
milestone: M-20260624T104233Z-A
---

## C-20260624T104233Z-A: legacy issue

- candidate_format_version: v2
- title: AGENTS.md 中测试硬编码改为 pre-tests.md 委托
- status: promoted
- decision_reason: AGENTS.md 中 hardcoded numbered steps 与"验证方式由 pre-tests.md 中的测试用例决定"的原则矛盾。修复已提交（194080e42），治理补录。
- next_action: B2_IBM 物化 I-* issue 并添加 milestones.md 条目
- revisit_trigger: 如果后续发现其他文件仍有 daemon-as-test 模式，需继续清理
- acceptance_criteria:
  - AGENTS.md 中无 hardcoded test steps（如 pre-init-runtime / freely-package / start daemon / verify Manager cycle 等步骤）
  - 测试方式统一委托给 pre-tests.md（"验证方式由 pre-tests.md 中的测试用例决定"）
  - Freely 自举上下文保留，标注为 "daemon 型项目参考"
- promotion_gate: AGENTS.md 修改已完成且语法无误，后续 B2_IBM 文档物化完成
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-agent
  - mode: subagent
  - summary: 全项目搜索确认无残留 daemon-as-test 模式。AGENTS.md hardcoded steps 已替换为 pre-tests.md 委托。自举上下文中 daemon 引用保留并标注。
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260624T104233Z-A/issue.md
- milestone: M-20260624T104233Z-A
- session_refs: []
