---
candidate_id: C-20260705T061416Z-A
status: absorbed
source_raw: raw-20260705T061416Z
created_at: 2026-07-05
milestone: M-20260705T061416Z-A
---

## C-20260705T061416Z-A: fix dirty 提示 backtick 命令替换

- candidate_format_version: v2
- title: fix dirty 提示 backtick 命令替换
- status: absorbed
- decision_reason: Bug 1 已被 M-20260703T080443Z-A 修复，本 candidate 收窄为仅 Bug 2。去掉反引号是最简单最安全的方案，避免 bash 双引号中的转义链脆弱性。
- next_action: absorbed by I-20260705T061416Z-A
- revisit_trigger: N/A（backtick 去掉后不回退）
- acceptance_criteria:
  - `docs/system/workspace/scripts/runtime/freely:21982` 中 `\\\`freely-workflow-guarded-execution\\\`` 改为 `freely-workflow-guarded-execution`（纯文本，无反引号）
  - bash 不再尝试将 `freely-workflow-guarded-execution` 当作命令执行
  - dirty 检查输出中的提示文本可读性不变
- promotion_gate: 单行修改，语法无误，不引入新 backtick
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 验证 Bug 1 已由 M-20260703T080443Z-A 修复，Bug 2 根因确认为双引号内 `\\` + 裸反引号导致命令替换，去掉反引号是最小修复
  - verdict: pass
- promoted_issue_id: I-20260705T061416Z-A
- promoted_issue_path: docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/issues/I-20260705T061416Z-A.md
- milestone: M-20260705T061416Z-A
- session_refs: []
