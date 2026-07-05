# Brainstorms: fix-execution cp→git stash 工作流优化

## Discovery
`docs/B1-docs/raw-20260624T081419Z/issue.md`：fix-execution 中 test-pre-merge 到 fix 工位的修改转移用 `cp` 逐个文件。git stash 对同仓库所有 worktree 可见，push/apply 更原子化。

## Research
**根因**：fix-execution 最初用 cp 是因为流程先于 stash 跨 worktree 特性的发现。
**方案**：test 工位 `git stash push --include-untracked` → fix 工位 `git stash apply` → 检查 → `git stash drop` → 精确 add + commit。

## Decision
Promote。单文件修改，纯工作流优化。
