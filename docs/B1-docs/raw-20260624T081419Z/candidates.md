# Candidates

## C-20260624T081419Z-A: fix-execution cp→git stash 工作流优化

- candidate_format_version: v2
- title: fix-execution 修改转移方式从 cp 改为 git stash push/apply
- status: promoted
- decision_reason: git stash 跨 worktree 共享，比 cp 逐个文件更原子化
- next_action: B2_IBM → pr-create → pr-merge → wt-close
- acceptance_criteria:
  - fix-execution 不出现 cp 命令作为修改转移方式
  - test 工位: git stash push --include-untracked
  - fix 工位: git stash apply → status 检查 → stash drop → 精确 add + commit
- promotion_gate: 文件修改完成，现有工作流不受影响
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260624T081419Z-A/issue.md
- milestone: M-20260624T081419Z-A
