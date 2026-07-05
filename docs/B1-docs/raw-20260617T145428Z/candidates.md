# Candidates

## C-20260617T145428Z-A: freely-db-cli syntax + AGENTS.md flow + hook skill routing

- candidate_format_version: v2
- title: Fix freely-db-cli IndentationError, AGENTS.md feedback entry, and pre-commit hook skill routing
- status: promoted
- decision_reason: 三个 bug 根因明确，均为低风险单行/文档修改。freely-db-cli bug 已导致 daemon 无法重启，P0 级别。
- next_action: B2_IBM → I-* issue → code-review → pr-create-guarded → pr-merge-guarded
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - freely-db-cli `db.ping` 返回 `pong` 而非 IndentationError
  - AGENTS.md §核心开发流程以 feedback/scan 分支开头，与 feat-execution skill 一致
  - pre-commit hook 拦截消息显式指向 `skill:freely-fix-execution` / `skill:freely-feat-execution`
  - Hook 消息包含反绕过警告（引用 CONSTITUTION.md §5）
- promotion_gate: 三个文件修改完成，语法正确
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 审查三个修复的正确性和完整性
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260617T145428Z-A/issue.md
- milestone: M-20260617T145428Z-A
- session_refs: []
