---
candidate_id: C-20260630T095936Z-A
status: promoted
source_raw: raw-20260630T095936Z
created_at: 2026-06-30
milestone: M-20260630T095936Z-A
---

## C-20260630T095936Z-A: consistency check — cherry-pick → git merge

- candidate_format_version: v2
- title: dev↔test consistency check 改用 git merge 替代 cherry-pick
- status: promoted
- decision_reason: Option A — 改提示文本与可行操作对齐，不改 hook 保护语义
- next_action: B2_IBM → 实现修改 worktree-common.sh + wt-close
- revisit_trigger: N/A
- acceptance_criteria:
  - dev→test 不一致时提示用 `git merge --no-ff` + `Freely-Merge-Path: pr-merge-guarded`
  - test→dev 不一致时硬拦截，提示正确流程
  - test 工位有未提交修改时硬拦截
  - 4 处调用点（pr-create/pr-merge/pr-review/wt-close）提示一致
- promotion_gate: 语法验证通过 + 消息审查
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-code
  - mode: inline
  - summary: 审查 PR #3648 开发过程中触发的死锁根因
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260630T095936Z-A/issue.md
- milestone: M-20260630T095936Z-A
- session_refs: []
