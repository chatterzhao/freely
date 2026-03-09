# Release And Hotfix Flow

## Release

1. 发布/打标签前执行 `./bin/wt-status-all`，结果必须全 `CLEAN`
2. 从 `develop` 创建 `release/*`
3. 在 `release/*` dedicated worktree 中完成冻结与验证
4. 合并到 `main`
5. 将发布结果回合并到 `develop`

## Hotfix

1. 从 `main` 创建 `hotfix/*`
2. 在 `hotfix/*` dedicated worktree 中完成修复
3. 合并到 `main` 和 `develop`
4. 若 `pre-test-merge` 当前活跃，同步热修复结果到该临时分支

## Failure rule

- 任一必需验证为红色，阻止发布、热修或标签推进
