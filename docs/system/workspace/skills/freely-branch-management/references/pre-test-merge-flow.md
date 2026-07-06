# Test Pre-Merge Flow

## Temporary validation batch

1. 仅在需要组合验证时启用新的 `test-pre-merge-*` 批次
2. 若旧测试批次仍在，先删除；新批次必须从当前 `develop` 创建
3. 仅从对应 `test-pre-merge-*` worktree 上下文进行集成工作
4. `test-pre-merge-*` 一旦启用，就应有自己的 canonical sibling worktree；进入该环境做验证时，直接 `cd` / `source freely wt-enter <test-pre-merge-branch>` 到这棵树，而不是停留在其他工位假装“当前就是测试批次环境”
5. 这棵 `test-pre-merge-*` worktree 是只读集成/验收环境：
   - 允许 merge、smoke、regression、post-merge acceptance
   - 运行测试时显式使用 `freely test-lane premerge-integration -- <command...>`；若当前是 merge 后真实环境 followthrough，则用 `freely test-lane post-merge-followthrough -- <command...>`
   - 不允许直接 add/commit 新实现
   - 若在这里发现缺陷，返回对应 feature worktree 修复，再重新并回该测试批次
6. 合并前执行 `freely wt-status-all`，结果必须全 `CLEAN`
7. 使用 `git branch --no-merged develop` 收集候选项
8. 按语义依赖构建队列，而不是按提交时间：
   - 治理/策略变更
   - 共享基础设施
   - 产品行为变更
9. 串行 `git merge --no-ff <branch>` 并立即运行冒烟/回归检查
10. `test-pre-merge-*` 是 `develop` 前的 canonical promote family，而不是单纯 replay 证据面：
   - single-feature lane 与 explicit multi-bundle lane 共享同一 `test-pre-merge-*` 前缀
   - 当前权威批次可以直接并入 `develop`
   - merge receipt 必须能追溯到来源 feature、source shas、merge order 与 base develop sha

## Responsibilities

1. `test-pre-merge-*` 只承担两类主线前临时职责：
   - 预检运行测试：在来源 feature 还未进入 `develop` 前，执行需要真实集成面的 smoke / regression / acceptance
   - 预测试 merge：把多个来源 feature 临时合入同一批次，验证组合冲突、集成次序与交互行为
2. 这两类职责都不是开发面：
   - 在这里发现问题，统一回到来源 `feature/*` 或新的 dedicated feature worktree 修复
   - 修复后再重新 merge 回对应 `test-pre-merge-*` 批次复验
3. `develop` 不承担“先预测试”的职责：
   - 需要主线前验证时，使用新的 `test-pre-merge-*`
   - 需要主线后真实环境确认时，才在 `develop` 做 completion verification
4. 来源 feature 的实现自测、局部回归与 issue-bound 验证留在 dedicated writable worktree，并使用 `freely test-lane feature-local -- <command...>`。

## Batch freshness and replay

1. `test-pre-merge-*` 批次只有在当前仍然权威时才可作为验证面消费。
2. 若 `develop` 已继续前进、批次出现 protected-env 独有差异，或 promotion / cleanup 证据断裂，该批次就应视为 stale。
3. stale 批次必须立即删除，再决定是否重建；不能继续把旧批次快照当成当前真相面。
4. 若同一能力仍需继续验证，默认做法是从当前 `develop` 重建新的 `test-pre-merge-*` 批次，而不是保留旧批次快照继续 promote。

## Post-merge acceptance environment

1. 若 issue 的 `pre-tests.md` 显式声明 `post-merge acceptance`，先看它的 `integration_target`：
   - `develop`：在 `develop` canonical worktree 验证
   - `test-pre-merge-*`：在对应 `test-pre-merge-*` canonical worktree 验证
2. `post-merge acceptance` 的目的是真实观察目标集成环境，不是绕过受保护分支规则继续开发。
3. 在 protected worktree 中运行验收时：
   - 允许 `cd` 到目标环境
   - 允许运行真实 `freely` / test / smoke / patrol / verification
   - 运行命令时显式使用 `freely test-lane post-merge-followthrough -- <command...>`
   - 不允许顺手修实现并提交
4. 若验收暴露问题，下一跳必须显式回到：
   - 原 feature worktree 继续修复；或
   - 新建 feature worktree 承接该 post-merge finding
5. 只有当 `post-merge acceptance` 明确通过后，才允许把该批次继续 promote 到更高一层或进入 cleanup。

## Replay to `develop`

1. 并入 `develop` 前再次执行 `freely wt-status-all`
2. 确认每个来源 `feature/*` 都已在自己的 dedicated worktree 中完成“merge 上游 -> 解决冲突 -> 自测”
3. 若某条线先经过 `test-pre-merge-*`，进入 `develop` 的动作是 merge 当前权威 `test-pre-merge-*` 批次，并保留来源 feature / bundle 追溯证据
4. 派生分支先确认父分支已进入要求路径，再 restack / rebase / merge 上游并重跑测试
5. 运行 [semantic-regression-checklist.md](semantic-regression-checklist.md)
6. 运行要求的 `TEST` 证据检查
7. `PRE_TEST` 只作基线，不替代提升测试结果

## Retirement

1. `test-pre-merge-*` 验证通过后：
   - 记录批次 manifest、验证结果和 promote receipt
   - 由当前权威 `test-pre-merge-*` 批次进入 `develop`
   - 删除当前测试批次
2. `test-pre-merge-*` 验证失败后：
   - 记录失败原因和回流目标 feature worktree
   - 不在 `test-pre-merge-*` 上直接修实现
   - 视需要删除当前批次，并在后续用新批次 rebuild
3. 不允许把同一 `test-pre-merge-*` 批次长期保留为滚动真相面。
