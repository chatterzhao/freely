# Pre-Test-Merge Flow

## Temporary validation batch

1. 仅在需要组合验证时启用 `pre-test-merge`
2. 仅从 `pre-test-merge` 上下文进行集成工作
3. 合并前执行 `./bin/wt-status-all`，结果必须全 `CLEAN`
4. 使用 `git branch --no-merged develop` 收集候选项
5. 按语义依赖构建队列，而不是按提交时间：
   - 治理/策略变更
   - 共享基础设施
   - 产品行为变更
6. 串行 `git merge --no-ff <branch>` 并立即运行冒烟/回归检查

## Promotion to `develop`

1. 并入 `develop` 前再次执行 `./bin/wt-status-all`
2. 确认每个分支都已在自己的 dedicated worktree 中完成“merge 上游 -> 解决冲突 -> 自测”
3. 派生分支先确认父分支已进入要求路径，再 restack / rebase / merge 上游并重跑测试
4. 运行 [semantic-regression-checklist.md](semantic-regression-checklist.md)
5. 运行要求的 `TEST` 证据检查
6. `PRE_TEST` 只作基线，不替代提升测试结果
