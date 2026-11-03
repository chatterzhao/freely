---
candidate_id: C-20260720T023136Z-A
status: promoted
source_raw: raw-20260720T023136Z
created_at: 2026-08-07
milestone: M-20260720T023136Z-A
---

## C-20260720T023136Z-A: chat help 错误信息 shell 引号嵌套修复

- candidate_format_version: v2
- title: 修复 chat help 错误信息中的 `<描述>` 被 bash 当作文件重定向
- status: promoted
- decision_reason: `docs/system/workspace/scripts/runtime/freely` L6700 的 log_error 参数用双引号包裹但内部嵌套双引号，外层引号提前闭合，`<描述>`/`<详细描述>` 落入非引号区被 bash 解释为输入重定向，渲染时崩溃为 `line 6700: 描述: No such file or directory`。改为整体单引号包裹即规避重定向解释且保留内层双引号字面量，是最小正确修复。
- next_action: B2 物化 I-20260720T023136Z-A + pre-tests/tasks → RED/GREEN → PR
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `docs/system/workspace/scripts/runtime/freely` L6700 不再含未转义的裸 `<` `>`，bash 语法检查（`bash -n`）通过
  - 模拟执行该 log_error 行不再输出 `No such file or directory`，且完整帮助文本可读
  - 中文字符与内部双引号在渲染后保持原样
- promotion_gate: B2 issue 物化完成 + pre-tests GREEN + pr-merge-guarded 通过
- open_questions: []
- acceptance_reviews:
  - reviewer: codex
  - mode: cli
  - summary: 确认单引号整体包裹是规避 `<` 重定向解释的最小修复，仅改一个字符串字面量
  - verdict: pass
- promoted_issue_id: I-20260720T023136Z-A
- promoted_issue_path: docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/raw-20260720T023136Z/issues/I-20260720T023136Z-A.md
- milestone: M-20260720T023136Z-A
- session_refs: []
