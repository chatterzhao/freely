---
candidate_id: C-20260624T141559Z-A
status: promoted
source_raw: raw-20260624T141559Z
created_at: 2026-06-24
milestone: M-20260624T141559Z-A
---

## C-20260624T141559Z-A: cmd_feedback 对齐 issue-sync 多平台架构

- candidate_format_version: v2
- title: cmd_feedback 改为 issue-sync 薄封装，去掉 --repo，支持多平台
- status: promoted
- decision_reason: Option B — `cmd_feedback` 作为 `issue-sync create` 的薄封装，架构对齐，加新平台零改动
- next_action: 已实现（commit 640773ddb），进入 B2_IBM 补 PRD/pre-tests/tasks/code-review
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `freely feedback --help` 不包含 `--repo` 参数
  - `freely feedback --repo foo/bar` 返回明确错误提示
  - `freely feedback --title "x" --body "y"` 创建本地 issue.md + 调用 issue-sync create
  - crash reporter 不再传 `--repo`
  - 加新平台（如 GitLab）只需在 issue-sync 加 adapter，feedback 无改动
- promotion_gate: 测试通过 + B2_IBM 文档完整
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: manual-review
  - summary: 审查 cmd_feedback 重写是否完整对齐 issue-sync，无遗留 --repo 引用
  - verdict: pass
- promoted_issue_path: docs/issues/raw-20260624T141559Z/issue.md
- milestone: M-20260624T141559Z-A
- session_refs: []
