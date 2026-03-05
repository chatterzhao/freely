# Agent 上下文入口

## 权威来源（按优先级排序）
1. `docs/CONSTITUTION.md`（硬性约束）
2. `docs/LAWS.md`（操作规则）
3. `docs/PROJECT_INTENT.md`（产品方向）
4. `AGENTS.md`（仅入口指引，不得覆盖 1-3）

如果本文件中的任何陈述与上述三个核心文档冲突，以核心文档为准。

## 当前项目阶段
Freely 处于研究优先的整合阶段。
当前活跃文档范围：
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/PROJECT_INTENT.md`
- `docs/pre-brainstorms/`

不要将遗留路径视为活跃工作流输入（例如：旧布局下的 `docs/brainstorms/`、`docs/planning/`、`docs/continuity/`、`docs/validation/`、`docs/reviews/`）。

## 吃自己的狗粮规则（Freely 构建 Freely）
Freely 必须在 Freely 治理规则下开发，不得有项目特定的例外。

要求：
- 使用对用户项目期望的相同分支/worktree/钩子规范。
- Worktree 根目录遵循宪法策略：项目同级目录，命名为 `{project-name}-worktrees`。
- 架构/治理变更必须先进入 `docs/pre-brainstorms/<id>/`，然后才能进入执行循环落地。
- 优先使用预检 + 可操作的修复方案，而非重复的权限提示。

## 执行指引
- 保持本文件简洁稳定；不要重复宪法/法律中的详细规则。
- 将细节添加到规范文档中，然后在此引用。
- 当出现不确定性时，打开/更新一个预研头脑风暴条目，先在那里收敛。

## 基本命令
- `./bin/freely init|doctor|start|status|stop`
- `./bin/bmad-check`
- `./bin/test-pre-push-hook`
- `source ./bin/wt-enter <branch>`
- `source ./bin/wt-add <branch> -- <git-add-args>`
