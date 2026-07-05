# 研究：标准 `git worktree` 提示与兜底边界

## Context

- 日期：2026-03-06 01:13 UTC
- 触发：当前仓库已经把 worktree 作为强制开发模式，但用户可见提示里仍混有 Freely 内部 helper 心智、机器路径或不够可移植的占位符。
- 已确认方向：规范主路径必须对齐行业通用 `git worktree`；Freely 的脚本和 hook 只做兜底与友好提示，不成为主工作流本身。

## 当前问题

1. 用户/AI 看到的提示如果先暴露 `wt-enter`、`wt-add` 这类 helper，会误以为 Freely 定义了一套特殊 worktree 语法。
2. 绝对路径或机器内路径不适合写进规范文档，用户项目无法直接复用。
3. `cd <project-root>` 这类抽象占位符不够明确；需要直接告诉用户先回到项目目录路径。
4. 规范、skills、hook 提示如果口径不一致，AI 会在不同入口学到不同流程。

## 收敛结论

### 1. 主规范必须是标准 `git worktree`

创建开发分支的标准写法应是：

```bash
cd <your-project-name-path>
git worktree add -b feature/<topic> ../<your-project-name>-worktrees/feature-<topic> develop
cd ../<your-project-name>-worktrees/feature-<topic>
```

说明：
- `develop` 作为命令最后一个参数，已经显式给出新分支基线。
- 不要求先单独 `git checkout develop`。
- 相对路径写法可以直接迁移到任意用户项目。

### 2. Freely 只保留最小约束

Freely 应只额外约束以下三件事：
- worktree 根目录位于项目同级：`../<your-project-name>-worktrees/`
- worktree 目录命名遵循分支名映射规则
- 受保护分支禁止直接开发

### 3. helper 与 hook 的职责边界

- `wt-enter` / `wt-add`：辅助命令，不是主规范入口
- `.githooks/post-checkout` / `.githooks/pre-commit`：兜底和友好提示，不是主工作流说明
- 用户/AI 按标准 `git worktree` 流程操作时，不应被 Freely 特殊约定打断

### 4. 用户可见提示必须使用可移植占位符

用户可见提示中：
- 使用 `cd <your-project-name-path>`，而不是 `cd <project-root>`
- 使用 `../<your-project-name>-worktrees/...`，而不是机器绝对路径
- 可以在运行时兜底提示中输出真实路径，以便用户直接执行

## 落地范围

以下位置必须统一到同一口径：
- `README.md`
- `AGENTS.md`
- `docs/system/workspace/skills/branch-management/SKILL.md`
- `docs/system/workspace/skills/premerge-reconcile/SKILL.md`
- `.githooks/pre-commit`
- `.githooks/post-checkout`

## 测试方案

### T1. 标准命令可用性验证

- 目标：验证标准 `git worktree add -b ... develop` 路径在真实仓库可正常工作
- 步骤：
  - 从项目目录执行标准相对路径命令
  - 检查新分支与新 worktree 是否正确创建
  - 检查主 worktree 是否保持在受保护分支
- 污染控制：
  - 使用临时 feature 分支
  - 验证后删除临时分支和临时 worktree

### T2. 提示文案一致性验证

- 目标：确保所有规范入口统一使用 `cd <your-project-name-path>` 与相对路径 worktree 提示
- 步骤：
  - 搜索 `AGENTS.md`、`README.md`、skills、hooks
  - 检查是否仍存在 `cd <project-root>` 或旧占位符
- 污染控制：
  - 纯只读搜索，无仓库污染

### T3. Hook 语法回归验证

- 目标：确保文案调整未破坏 shell 脚本语法
- 步骤：
  - 运行 `bash -n .githooks/pre-commit .githooks/post-checkout bin/worktree-common.sh`
- 污染控制：
  - 纯语法检查，无仓库污染

## 已执行验证

- 已在真实仓库执行标准 `git worktree add -b ... develop` 创建临时 feature worktree，并在验证后清理临时分支与 worktree
- 已严格搜索：
  - `cd <your-project-name>`
  - `cd <your-project-name-path>`
  - `cd <project-root>`
- 已运行：
  - `bash -n .githooks/pre-commit .githooks/post-checkout bin/worktree-common.sh`

结果：
- 标准 `git worktree` 路径可用
- 用户可见提示已收敛到可移植占位符
- shell 语法检查通过

## 结论

该问题已具备 issue-ready 条件，可作为治理文案与 hook 提示统一的直接输入。
