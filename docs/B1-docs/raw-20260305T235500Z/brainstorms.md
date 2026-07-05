# 研究：`pre-develop` 迁移为 `pre-test-merge` 的职责收敛

## 兼容说明

- 本研究形成于 `pre-test-merge` 仍被视为单例批次的阶段。
- 当前 canonical 语义已经升级为 `test-pre-merge-*` 测试批次前缀族。
- 下文出现的 `pre-test-merge`，除历史事实和当时分支名外，都按 `test-pre-merge-*` 前缀族理解。

## Context

- 日期：2026-03-05 23:55 UTC
- 触发：当前仓库把 `pre-develop` 定义为强制性的长期测试集成分支，导致分支模型偏离常见 GitFlow / merge queue 心智，AI 和人类都更容易走错路径。
- 已确认决策：长期 `pre-develop` 被收敛成测试批次语义；当前 canonical 命名为 `test-pre-merge-*` 前缀族。
- 关联问题：现有 `wt-enter` / `.githooks/post-checkout` 在创建 feature 分支后，未能稳定把执行上下文切换到对应 worktree，而可能把主 worktree 留在 feature 分支上。

## 当前问题

1. `pre-develop` 语义同时承担了：
   - feature 默认父分支
   - 长期测试集成分支
   - 提升到 `develop` 的唯一祖先路径
   - 冲突收敛起点
2. 这使分支模型不是标准 GitFlow，也不是常见 merge queue / merge train 语义。
3. hooks 和脚本因此把“所有 feature 必须从 `pre-develop` 创建”硬编码到了运行时。
4. `wt-enter` 的当前行为在“新分支先挂到主 worktree”场景缺少自愈，违背了“创建分支后应引导进入 dedicated worktree”的预期。

## 行业对照

1. 标准 GitFlow：
   - `feature/*` 从 `develop` 创建
   - `feature/*` 合并回 `develop`
   - `release/*` 从 `develop` 创建
   - `hotfix/*` 从 `main` 创建
2. 现代 PR / merge queue：
   - 以单一主集成分支为目标
   - 通过临时集成队列或系统生成的测试合并提交做组合验证
3. 结论：
   - “预集成验证”职责本身合理
   - 但它更像临时 `pre-test-merge`，而不是长期一级正式开发分支

## 收敛结论

### 1. 分支职责迁移

- `develop`：唯一长期开发集成分支
- `test-pre-merge-*`：临时预集成验证批次
- `feature/*`：从 `develop` 创建
- `feature/*`：默认目标仍是 `develop`

### 2. `test-pre-merge-*` 的使用场景

仅在以下场景启用：
- 多个 `feature/*` 需要做组合验证
- 常规合并前需要短周期集成验收
- 高风险冲突需要集中收敛
- release 前需要预演合并批次

### 3. `test-pre-merge-*` 的退出条件

- 验证成功：将已验证结果回放到来源 feature / develop 吸收路径
- 验证失败：记录失败原因并销毁本轮测试批次
- 冲突收敛完成：职责即完成，不保留为长期开发父分支

### 4. `cherry-pick` 约束

- 不作为 feature -> develop 的默认主路径
- 仅用于旧分支回收有效提交、hotfix/backport、或复杂冲突后的补救性回收

### 5. worktree 引导行为

创建或切换 feature/release/hotfix 分支后：
- 主 worktree 只能短暂停留用于触发 auto-create
- 必须稳定回到 parking branch
- 用户/AI 的后续工作目录必须切到 dedicated sibling worktree
- 如果 dedicated worktree 已存在，应直接 `cd` 进入，而不是停留在主 worktree

## 最小落地要求

1. 所有规范文档中的 `pre-develop` 角色迁移为 `test-pre-merge-*` 或 `develop`，不能只做字符串替换。
2. hooks / `bin/*` 必须同步迁移：
   - feature 基线从 `develop` 判断
  - `test-pre-merge-*` 视为受保护测试批次
  - merge guard 改为 `feature/* -> develop` 为默认路径，`feature/* -> test-pre-merge-*` 为临时验证路径
3. `wt-enter` / `post-checkout` 必须修正为“引导进入 worktree”而不是“把主 worktree 留在 feature 分支”。

## 测试方案

### T1. Hook 推送策略测试

- 脚本：`bin/test-pre-push-hook`
- 目标：
  - `test-pre-merge-*` 作为受保护测试批次禁止 push
  - `feature/*` 只允许 push 到远端同名分支
  - 阻止 `feature/* -> develop` 这类跨分支 push
- 污染控制：
  - 使用 `mktemp` 创建临时输出目录
  - 通过 `trap` 自动清理

### T2. Worktree 引导行为测试

- 脚本：`bin/test-worktree-entry-flow`
- 目标：
  - 在临时仓库中从 `develop` 创建 `feature/*`
  - 执行 `source ./bin/wt-enter feature/demo`
  - 验证主 worktree 回到 parking branch（`develop`）
  - 验证当前 shell 进入 dedicated sibling worktree
- 污染控制：
  - 使用临时 Git 仓库
  - 测试结束后删除整个临时目录

### T3. Merge Guard 路径测试

- 脚本：`bin/test-pr-merge-guarded`
- 目标：
  - 允许 `feature/* -> develop`
  - 允许 `hotfix/* -> test-pre-merge-*`
  - 阻止非法的 `feature/* -> main`
- 污染控制：
  - 使用临时 Git 仓库
  - 测试结束后删除整个临时目录

## 已执行验证

- `bash -n .githooks/post-checkout .githooks/pre-commit .githooks/pre-push bin/pr-merge-guarded bin/test-pre-push-hook bin/test-worktree-entry-flow bin/test-pr-merge-guarded bin/worktree-common.sh bin/wt-add bin/wt-enter`
- `./bin/test-pre-push-hook`
- `./bin/test-worktree-entry-flow`
- `./bin/test-pr-merge-guarded`

结果：
- 全部通过
- 当前已验证“职责迁移 + 引导进入 worktree + merge 路径门禁”三条主链

## 结论

该问题已具备 issue-ready 条件，应进入治理与脚本同步迁移。
