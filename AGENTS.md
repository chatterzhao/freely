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

## 会话启动检查

每次会话开始：
1. **分支/Worktree检查**：如在 `main`/`develop`/`pre-test-merge` 则禁止写入。先执行 `cd <your-project-path>`，再按标准 `git worktree add -b <branch> ../<your-project-worktrees>/<branch-dir> <base>` 创建 feature worktree，并 `cd` 到该 worktree 中工作。默认 `<base>` 为 `develop`；若当前 issue 依赖未合并父分支改动，可用父 `feature/*` 作为 `<base>`，但必须在 pre-brainstorm / milestone / issue 中记录依赖关系。`<your-project-worktrees>` 指当前项目同级的 worktree 根目录，格式为 `<your-project-name>-worktrees`。`<branch-dir>` 必须与当前 worktree 派生规则一致：无日期分支使用 `<branch>` 的安全化名称；若分支名包含 `YYYYMMDD` 或 `YYYYMMDD-HHMM/HHMMSS`，目录名改为日期前置，例：`feature/foo-20260307-1015` -> `20260307-1015-feature-foo`
2. **头脑风暴路由**：
   - 预研头脑风暴（不是基于 issue 文档）：文档放 `docs/pre-brainstorms/`
   - IBM 头脑风暴（基于 issue 文档）：文档放 `docs/epics/{epic-name}/{story-name}/brainstorms/b-{issue-name}.md`

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
- `cd <your-project-path>`
- `./bin/wt-create <branch> [--base <base-branch>]`
- `git worktree add -b <branch> ../<your-project-worktrees>/<branch-dir> <base>`
- `git worktree remove ../<your-project-worktrees>/<branch-dir> && git branch -d <branch>`
- `source ./bin/wt-enter <branch>`
- `source ./bin/wt-add <branch> -- <git-add-args>`
