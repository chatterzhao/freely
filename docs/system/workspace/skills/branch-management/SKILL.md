---
name: branch-management
description: 管理 Freely 风格开发的完整自主分支生命周期，支持默认 feature worktree 与依赖未合并父分支的派生 worktree。
---

# skill:branch-management

## 工作流

1. 先跑固定门禁：`skill:constitution-guard` -> `skill:laws-enforcer`。
2. 按场景选择唯一 reference：
   - 功能开发 / 派生 worktree：读 [feature-worktree-flow.md](references/feature-worktree-flow.md)
   - 临时验证批次与提升：读 [pre-test-merge-flow.md](references/pre-test-merge-flow.md)
   - 发布 / 热修 / 标签：读 [release-hotfix-flow.md](references/release-hotfix-flow.md) 和 [release-tag-policy.md](references/release-tag-policy.md)
   - 清理：读 [cleanup-lifecycle.md](references/cleanup-lifecycle.md)
3. 若冲突复杂或回滚风险出现，停止并切换到 `skill:premerge-reconcile`。

## 硬性规则
- 绝不绕过要求的 `TEST`、评审和进度/恢复证据将功能分支直接推送或违规合并到 `develop`。
- 绝不跳过“先把上游合进当前分支并在本 worktree 里处理冲突”这一步，就直接把功能分支往上游目标提升。
- 保持治理意图稳定：分支策略、worktree 约束、命名策略。
- 如语义检查失败，不提升；返回协调流程。
- 绝不通过提交时间戳排序解决冲突。
- 绝不推送 `alpha`/`beta` 标签。
- 对于规范文档变更，在专用 feature/worktree 中工作，并要求关联实现或门禁变更证据。
- 对于依赖未合并父分支的子任务，不把 `develop` 伪装成执行基线；必须记录依赖并在提升前完成 restack / rebase / merge 上游。
- `develop` / `main` / `pre-test-merge` 可以存在 canonical worktree，但它们只承担受保护分支的管理/集成/验收环境，不承担真实 feature 开发。
- `post-merge acceptance` 默认直接在目标受保护分支自己的 canonical worktree 中执行：
  - `develop`：项目主 worktree
  - `pre-test-merge`：同名 sibling worktree
- 不为一次 `post-merge acceptance` 再额外创建匿名 companion worktree；若验收暴露缺陷，回到现有 feature worktree 或新建 feature worktree 修复，再重新走提升路径。

## 完成
- 临时验证批次完成后，无需继续保留的分支不会滞留在 `pre-test-merge` 中。
- 语义回归检查清单全部为绿色。
- 提升/标签/发布动作已完成或显式阻止并记录原因。
