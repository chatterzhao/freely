---
name: freely-branch-management
description: 管理 Freely 风格开发的完整自主分支生命周期，支持默认 feature worktree 与依赖未合并父分支的派生 worktree。
---

# skill:freely-branch-management

## 工作流

1. 先跑固定门禁：`skill:freely-constitution-guard` -> `skill:freely-laws-enforcer`。
2. 按场景选择唯一 reference：
   - 功能开发 / 派生 worktree：读 [feature-worktree-flow.md](references/feature-worktree-flow.md)
   - 临时验证批次与 promote：读 [pre-test-merge-flow.md](references/pre-test-merge-flow.md)，其中 `test-pre-merge-*` 表示临时测试批次前缀族
   - 发布 / 热修 / 标签：读 [release-hotfix-flow.md](references/release-hotfix-flow.md) 和 [release-tag-policy.md](references/release-tag-policy.md)
   - 清理：读 [cleanup-lifecycle.md](references/cleanup-lifecycle.md)
3. 若冲突复杂或回滚风险出现，停止并切换到 `skill:freely-premerge-reconcile`。

## 硬性规则
- 绝不绕过要求的 `TEST`、评审和进度/恢复证据将功能分支直接推送或违规合并到 `develop`。
- 绝不把裸 `--no-verify`、手工跳过 hook、或其他 protected-branch gate bypass 当成正常完成路径。`FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：<业务理由>"` 是唯一合法豁免。
- 绝不跳过“先把上游合进当前分支并在本 worktree 里处理冲突”这一步，就直接把功能分支往上游目标提升。
- 保持治理意图稳定：分支策略、worktree 约束、命名策略。
- 如语义检查失败，不提升；返回协调流程。
- 绝不通过提交时间戳排序解决冲突。
- 绝不推送 `alpha`/`beta` 标签。
- 对于规范文档变更，在专用 feature/worktree 中工作，并要求关联实现或门禁变更证据。
- 对于依赖未合并父分支的子任务，不把 `develop` 伪装成执行基线；必须记录依赖并在提升前完成 restack / rebase / merge 上游。
- `develop` / `main` / `test-pre-merge-*` 可以存在 canonical worktree，但它们只承担受保护分支的管理/集成/验收环境，不承担真实 feature 开发。
- 跑测试前先选对 lane，并显式使用 `./bin/test-lane <lane> -- <command...>`：
  - writable dedicated worktree -> `feature-local`
  - `test-pre-merge-*` 批次 -> `premerge-integration`
  - 目标 protected branch 的 merge 后验收 -> `post-merge-followthrough`
- `test-pre-merge-*` 只承担两类主线前临时职责：
  - 预检运行测试
  - 预测试 merge
- 这两类职责发现问题后，都回到来源 feature worktree 或新 feature worktree 修复；不在 `test-pre-merge-*` 上直接改实现。
- `post-merge acceptance` 默认直接在目标受保护分支自己的 canonical worktree 中执行：
  - `develop`：项目主 worktree
  - `test-pre-merge-*`：对应测试批次 worktree
- 不为一次 `post-merge acceptance` 再额外创建匿名 companion worktree；若验收暴露缺陷，回到现有 feature worktree 或新建 feature worktree 修复，再重新走提升路径。

## 完成
- 临时验证批次完成后，无需继续保留的分支不会滞留在 `test-pre-merge-*` 中。
- `test-pre-merge-*` 自身不是长期资产；该批次在验证通过或失败后都应立即删除。验证通过时，由当前权威批次进入 `develop`，随后 retire 该批次。
- 语义回归检查清单全部为绿色。
- 提升/标签/发布动作已完成或显式阻止并记录原因。
