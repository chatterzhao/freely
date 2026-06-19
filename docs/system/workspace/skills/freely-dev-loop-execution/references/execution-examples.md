# Execution Examples

## Ready issue enters dev-loop

- scan 结果中 `phase_state=done_b2_ibm` 的 issue 或 `a2a_tasks` 中进行中的任务
- docs 已齐备
- 当前在正确 dedicated worktree
- 结论：进入实现、测试和 `progress` 回写，并把状态切到 `in_dev`

## Boundary leak discovered during implementation

- 当前 issue 中暴露出新的治理问题或新的产品边界
- 结论：在 issue / `progress` 里记录影响与 blocker，返回 `next_recommended_route=freely-doc-B1_IBM-execution`

## Derived worktree promotion

- issue 依赖未合并父分支
- 结论：父分支先进入要求路径，当前分支再 restack / rebase / merge 上游并重跑测试
