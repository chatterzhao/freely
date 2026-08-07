---
candidate_id: C-20260807T105604Z-A
status: promoted
source_raw: raw-20260807T105604Z
created_at: 2026-08-07
milestone: M-20260807T105604Z-A
---

## C-20260807T105604Z-A: 解除 .codex/config.toml 跟踪

- candidate_format_version: v2
- title: 解除 .codex/config.toml 跟踪（cleanup）
- status: promoted
- decision_reason: .gitignore 已声明 `.codex/` 忽略，但文件在规则加入前被跟踪；个人字段修改持续污染 develop working tree。正确做法是解除跟踪而不是模板化或改 clean-tree 检查。
- next_action: B2 物化 I-20260807T105604Z-A + pre-tests/tasks → RED/GREEN → PR
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `.codex/config.toml` 从 git 跟踪中移除且本地文件保留
  - 本地修改 `.codex/config.toml` 不再使 `git status --porcelain` 出现 tracked dirty
  - `.gitignore:78` 的 `.codex/` 规则继续生效
- promotion_gate: B2 issue 物化完成 + pre-tests GREEN + pr-merge-guarded 通过
- open_questions: []
- acceptance_reviews:
  - reviewer: codex
  - mode: cli
  - summary: 确认 untrack 是最小正确修复，无需 example 模板
  - verdict: pass
- promoted_issue_id: I-20260807T105604Z-A
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260807T105604Z/issues/I-20260807T105604Z-A.md
- milestone: M-20260807T105604Z-A
- session_refs: []
