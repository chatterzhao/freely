# Feature Worktree Flow

## Route A: feature development

1. 判断执行基线：
   - 独立 issue：`execution_base=develop`
   - 依赖未合并父分支：`execution_base=<parent feature branch>`
   - `integration_target` 默认仍是 `develop`
2. 回到项目根目录后创建 dedicated worktree：
   - 推荐：`freely wt-create feature/<topic> --base <execution_base>`
   - 手工兜底：`git worktree add -b feature/<topic> ../<your-project-worktrees>/<branch-dir> <execution_base> && freely sync-tooling --source-project <your-project-path> --project ../<your-project-worktrees>/<branch-dir>`
3. `<branch-dir>` 规则：
   - `feature/my-topic` -> `feature-my-topic`
   - `feature/my-topic-20260307-1015` -> `20260307-1015-feature-my-topic`
4. 只在该分支 worktree 中变更。
5. 若依赖父 feature，必须在 docs 中记录：
   - `execution_base`
   - `integration_target`
   - `depends_on`
6. 暂存与提交：
   - `source ./bin/wt-add feature/<topic> -- <paths or -A>`
   - 若暂存内容混合多个关注点，先拆分
7. 提升前，先在当前 dedicated worktree 中把真正上游合进自己分支再处理冲突。

## Upstream alignment

- 独立 issue：通常对齐 `develop`
- 派生 issue：先跟随父 feature 结果，再对齐 `develop`
- `feature/premerge-*`：默认上游是当前活跃的 `test-pre-merge-*` 批次
