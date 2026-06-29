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
3. `pr-create-guarded` 提 PR
4. PR review 通过后：
   - `pr-merge-guarded main <hotfix-branch>`
   - `pr-merge-guarded develop <hotfix-branch>`
5. 若某个 `test-pre-merge-*` 批次当前活跃，同步热修复结果到该临时测试分支

## Failure rule

- 任一必需验证为红色，阻止发布、热修或标签推进
