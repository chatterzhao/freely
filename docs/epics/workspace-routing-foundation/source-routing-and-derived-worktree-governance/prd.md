# PRD - source-routing-and-derived-worktree-governance

## Problem

Freely 在自举和多 worktree / 多 agent 条件下，仍缺一套稳定的来源分层、路由边界和派生 worktree 口径，导致 AI 可能在错误目录、错误基线或错误环节写入产物。

## Product Requirement

系统必须让 AI 稳定做到：
1. 区分原始发现源、编排来源、延续来源。
2. 把新问题先收敛为 candidate，并同步到 milestone。
3. 只让 milestone-owned issue 进入 IBM。
4. 只让 ready issue 进入 dev-loop。
5. 只让 `progress` 跟踪 dev-loop。
6. 在需要写入时，先判断并进入合适 worktree。
7. 在 issue 依赖未合并父分支时，允许 derived worktree。
8. 在 IBM 中先确认 `epic-name/story-name/issue-name`，再写正式目录。
9. 首跳完成工具选择后，若 `selected_tool` 与当前运行工具一致，必须在当前会话继续执行第二跳，而不是只返回 `next_prompt`。
10. 首跳 prompt、`lead-agent`、`workspace/tools.md` 与脚本回归必须对上述语义保持一致。

## Non-Goals

- 这轮不实现完整的自动派生 worktree 编排器。
- 这轮不定义新的业务功能需求。
