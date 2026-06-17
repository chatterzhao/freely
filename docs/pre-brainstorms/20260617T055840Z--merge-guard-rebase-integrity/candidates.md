# Candidates

## C-20260617T055840Z-A: Merge Guard + Rebase Integrity

- candidate_format_version: v2
- title: GitHub branch protection 拦截直接 merge + post-rewrite hook rebase 完整性校验
- status: promoted
- decision_reason: ACP/A2A 重构中 3 个 PR 绕过 pr-merge-guarded 直接 merge，rebase 丢失 3 项代码变更。行业标准方案（branch protection + post-rewrite hook）成熟可靠。
- next_action: B2_IBM → 物化 I-issue，完成 prd/pre-tests/tasks/code-review
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - GitHub UI "Merge pull request" 按钮灰掉（check 未通过）
  - pr-merge-guarded 正常合并（check 被设为 success）
  - git rebase 丢文件时 post-rewrite hook 写入 marker
  - pr-merge-guarded 读取 marker 拒绝 merge
  - pre-rebase hook 在 rebase 前自动保存 diff 快照
- promotion_gate: 5 个 commit 已实现，语法检查通过，pre-rebase hook 实测保存快照成功
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 3 个 subagent 并行审查了 5 个设计方案，否决了过度设计的方案（safe-rebase wrapper、affected-files gate），确认了 branch protection + post-rewrite hook 的最简方案
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260617T055840Z-A/issue.md
- milestone: M-20260617T055840Z-A
- session_refs: []
