# PRD: raw-20261125T094104Z

## Goal
pr-merge-guarded 在 issue-sync 自动 commit 后 push 源分支时，逐 configured platform 校验结果：失败可见、非零退出、可操作重试；消除 `|| true` + 无条件 "pushed" 的虚假回执。

## 实现方案
仅改 `_sync_issues_changed_in_merge` 的 push 块（:623-629）：
- 用 `git remote` 遍历，跳过 `all`；
- 逐 remote `git push <remote> <branch>`，捕获 rc；
- 汇总 failed_remotes；
- 失败 → echo 含失败清单与重试命令 + return 1（非零）；成功 → 逐 remote 回执 ok。
沿用同文件 develop-push 段（:401-423）范式。

## Dev-Loop Handoff
- 测试先行：AT-001（test-pr-merge-push-receipt.py）静态断言 + mock 行为断言，develop 基线 RED。
- 实现：只改 push 块，不动 develop-push 段与 adapter。
- 验证：test 工位 merge 后 test-gate run；pr-create → review → merge → wt-close。
- 边界：保留自动 push 必要性；不改 PR 创建/合并门禁顺序。
