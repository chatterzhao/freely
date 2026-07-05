# Entry And Worktree Checks

## Before writing

- 只读分析可以先在当前上下文判断
- 一旦要写 `docs/B1-docs/**`，必须确认当前 worktree 合法

## Worktree rules

- 当前已承载该问题上下文的 dedicated worktree：可继续
- 当前位于 `main/develop/test-pre-merge-*` 或主 worktree：必须先创建/进入 dedicated feature worktree
- 若问题依赖未合并父分支：优先在父分支上下文或其派生 worktree 中继续

## Stop conditions

- 还没找到稳定问题边界：允许继续 pre-brainstorm
- 已经具备清晰 issue 边界：准备转入 IBM
