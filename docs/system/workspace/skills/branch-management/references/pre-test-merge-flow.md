# Pre-Test-Merge Flow

## Temporary validation batch

1. 仅在需要组合验证时启用 `pre-test-merge`
2. 仅从 `pre-test-merge` 上下文进行集成工作
3. `pre-test-merge` 一旦启用，就应有自己的 canonical sibling worktree；进入该环境做验证时，直接 `cd` / `source ./bin/wt-enter pre-test-merge` 到这棵树，而不是停留在其他工位假装“当前就是 pre-test-merge 环境”
4. 这棵 `pre-test-merge` worktree 是只读集成/验收环境：
   - 允许 merge、smoke、regression、post-merge acceptance
   - 不允许直接 add/commit 新实现
   - 若在这里发现缺陷，返回对应 feature worktree 修复，再重新并回 `pre-test-merge`
5. 合并前执行 `./bin/wt-status-all`，结果必须全 `CLEAN`
6. 使用 `git branch --no-merged develop` 收集候选项
7. 按语义依赖构建队列，而不是按提交时间：
   - 治理/策略变更
   - 共享基础设施
   - 产品行为变更
8. 串行 `git merge --no-ff <branch>` 并立即运行冒烟/回归检查

## Post-merge acceptance environment

1. 若 issue 的 `pre-tests.md` 显式声明 `post-merge acceptance`，先看它的 `integration_target`：
   - `develop`：在 `develop` canonical worktree 验证
   - `pre-test-merge`：在 `pre-test-merge` canonical worktree 验证
2. `post-merge acceptance` 的目的是真实观察目标集成环境，不是绕过受保护分支规则继续开发。
3. 在 protected worktree 中运行验收时：
   - 允许 `cd` 到目标环境
   - 允许运行真实 `freely` / test / smoke / patrol / verification
   - 不允许顺手修实现并提交
4. 若验收暴露问题，下一跳必须显式回到：
   - 原 feature worktree 继续修复；或
   - 新建 feature worktree 承接该 post-merge finding
5. 只有当 `post-merge acceptance` 明确通过后，才允许把该批次继续 promote 到更高一层或进入 cleanup。

## Promotion to `develop`

1. 并入 `develop` 前再次执行 `./bin/wt-status-all`
2. 确认每个分支都已在自己的 dedicated worktree 中完成“merge 上游 -> 解决冲突 -> 自测”
3. 派生分支先确认父分支已进入要求路径，再 restack / rebase / merge 上游并重跑测试
4. 运行 [semantic-regression-checklist.md](semantic-regression-checklist.md)
5. 运行要求的 `TEST` 证据检查
6. `PRE_TEST` 只作基线，不替代提升测试结果
