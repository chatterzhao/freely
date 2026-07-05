## Implementation Decision Note

- issue_id: I-20260624T081419Z-A
- issue_path: docs/issues/I-20260624T081419Z-A/issue.md
- decision: test-pre-merge → fix 工位修改转移从 cp 改为 git stash push/apply
- why_this: git stash 对同仓库所有 worktree 可见，push 一次性捕获全部 dirty state（含新文件 --include-untracked），比 cp 逐个文件更原子化
- alternatives_considered:
  1. 保持 cp — 需要逐个列出文件路径，容易遗漏
  2. git stash pop — 冲突时直接丢失 stash，不如 apply → check → drop 安全
  3. git diff + patch — 过于复杂
- boundary_non_goals: 不改 test-execution/feat-execution 的修改转移（它们走 merge 流程，不涉及 cp）
- residual_risk: 无。纯工作流文档优化
