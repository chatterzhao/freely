---
name: branch-management
description: 管理 Freely 风格开发的完整自主分支生命周期。当 AI 需要从 develop 创建功能分支、进入 worktree、在正确位置执行 add/commit、在需要时运行临时 pre-test-merge 验证批次、执行语义回归检查、并入 develop、管理 release/hotfix 分支、应用基于阶段的标签、并在验证后清理分支/worktree 时使用。
---

# skill:branch-management

## 路由 A：功能开发
1. 运行预检门禁：
   - `skill:constitution-guard`
   - `skill:laws-enforcer`
2. 从 `develop` 创建功能分支：
   - `git branch feature/<topic> develop`
3. 进入分支 worktree（自动创建 + cd）：
   - `source ./bin/wt-enter feature/<topic>`
4. 仅在此 worktree 中进行变更。
   - 编码前，定义此周期的单一变更意图和边界（作用域说明，用于后续提交拆分）
5. 在功能 worktree 中暂存和提交：
   - `source ./bin/wt-add feature/<topic> -- <paths or -A>`
   - 语义自检：如果暂存变更包含混合关注点，在提交前拆分
   - `git commit -m "<type>: <summary>"`
6. 在 push/merge 前，重新检查提交边界，如仍有混合关注点则再次拆分。
7. 集成前运行分支本地测试。

## 路由 B：临时验证批次到 pre-test-merge
1. 仅在需要组合验证时启用 `pre-test-merge`，并从 `develop` 创建或刷新该临时分支。
2. 仅从 `pre-test-merge` 上下文进行集成工作。
3. 合并前执行 Worktree 卫生门禁：`./bin/wt-status-all`，结果必须全 `CLEAN`。
4. 使用 `git branch --no-merged develop` 收集候选项，并按本轮验证范围筛选候选项。
5. 按语义依赖构建合并队列，绝不按提交时间：
   - 治理/策略变更
   - 共享基础设施
   - 产品行为变更
6. 串行合并：
   - `git merge --no-ff <branch>`
   - 立即运行必需的冒烟/回归检查
7. 如果冲突复杂或回滚风险出现，停止并切换到 `skill:premerge-reconcile`。

## 路由 C：回归 + 提升
1. 并入 `develop` 前再次执行 Worktree 卫生门禁：`./bin/wt-status-all`，结果必须全 `CLEAN`。
2. 队列完成后，运行语义检查清单：
   - `references/semantic-regression-checklist.md`
3. 运行提升所需的 `TEST` 证据检查（包括集成验收测试）。
4. 确保 `PRE_TEST` 仅作为基线，不得替代提升测试结果。
5. 如走临时验证路径且所有检查为绿色，将 `pre-test-merge` 合并到 `develop`；否则按允许路径直接将 `feature/*` 合并到 `develop`。
6. 如有任何语义/测试不匹配出现，阻止提升并返回协调流程。

## 路由 D：发布和标签流程
1. 发布/打标签前执行 Worktree 卫生门禁：`./bin/wt-status-all`，结果必须全 `CLEAN`。
2. 遵循 `references/release-tag-policy.md` 的阶段命名：
   - 格式：`YYYY.MM.DD-HHMM-stage`
3. 按分支/阶段的标签行为：
   - `feature/*` -> `alpha`（本地轻量标签，不推送）
   - `pre-test-merge` -> `beta`（本地轻量标签，不推送）
   - `develop` -> `nightly`（推送标签）
   - `main` -> `stable`（推送标签）
   - `hotfix/*` -> `hotfix`（推送标签）
4. 发布分支路径（必须在 `release/*` 对应 worktree 中执行）：
   - 从 `develop` 创建 `release/*`
   - 通过 `source ./bin/wt-enter release/<topic>` 进入该分支 worktree
   - 在该 worktree 中完成发布冻结与验证后，合并到 `main`
   - 将发布结果回合并到 `develop`
5. 热修复分支路径（必须在 `hotfix/*` 对应 worktree 中执行）：
   - 从 `main` 创建 `hotfix/*`
   - 通过 `source ./bin/wt-enter hotfix/<topic>` 进入该分支 worktree
   - 在该 worktree 中完成修复后，合并到 `main` 和 `develop`
   - 若 `pre-test-merge` 当前活跃，同步热修复结果到 `pre-test-merge`
6. 如任何必需验证为红色，阻止推送标签/发布。

## 路由 E：清理策略
1. 清理前执行 Worktree 卫生门禁：`./bin/wt-status-all`，结果必须全 `CLEAN`。
2. 合并后不要立即删除分支/worktree。
3. 保持状态演进：
   - `active` -> `merged-pending-verify` -> `verified-retirable` -> `retired`
4. 仅在以下条件后删除分支/worktree：
   - 合并完成
   - 测试和语义回归为绿色
   - 无待处理回滚项

## 硬性规则
- 绝不绕过要求的 `TEST`、评审和进度/恢复证据将功能分支直接推送或违规合并到 `develop`。
- 保持治理意图稳定：分支策略、worktree 约束、命名策略。
- 如语义检查失败，不提升；返回协调流程。
- 绝不通过提交时间戳排序解决冲突。
- 绝不推送 `alpha`/`beta` 标签。
- 对于规范文档变更，在专用 feature/worktree 中工作，并要求关联实现或门禁变更证据。

## 完成
- 临时验证批次完成后，无需继续保留的分支不会滞留在 `pre-test-merge` 中。
- 语义回归检查清单全部为绿色。
- 提升/标签/发布动作已完成或显式阻止并记录原因。
