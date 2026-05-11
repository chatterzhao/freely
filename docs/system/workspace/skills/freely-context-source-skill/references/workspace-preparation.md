# Workspace Preparation

## When workspace prep is required

以下目标 skill 都会写仓库：

- `freely-doc-B1_IBM-execution`
- `freely-doc-B2_IBM-execution`
- `freely-dev-loop-execution`
- `freely-workspace-skill-governance`

## Rules

- 当前在 `main/develop/test-pre-merge-*` 或主 worktree：`workspace_action=create_or_enter_worktree`
- 已在承载该问题上下文的 dedicated worktree：`workspace_action=continue_current_worktree`

## Execution base

- 独立任务：`execution_base=develop`
- 依赖未合并父分支：`execution_base=<parent feature branch>`
- 默认 `integration_target=develop`
- release / hotfix / premerge 场景交给 `freely-branch-management`

## Required outputs

- `workspace_action`
- `execution_base`
- `integration_target`
- `depends_on`
