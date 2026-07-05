# Brainstorm: issue-sync close should use --project worktree
## 错误方案: 豁免close的protected branch guard → 破坏了保护约束
## 正确方案: 让pr-merge-guarded和wt-close传--project指向worktree
## 决策: promote 正确方案
