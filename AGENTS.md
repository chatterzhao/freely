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
- `docs/milestones.md`
- `docs/epics/`
- `docs/progress/`
- `docs/system/workspace/`

不要将遗留路径视为活跃工作流输入（例如：旧布局下的 `docs/brainstorms/`、`docs/planning/`、`docs/continuity/`、`docs/validation/`、`docs/reviews/`）。

## 仓库分层

先区分两类目录，不要把“文档”一概归为开发过程资产。

### 1. 指导开发 Freely 的目录

这些目录主要用于治理、收敛、排期、验收与 lifecycle 留痕；它们指导 Freely 如何开发 Freely，但不是最终要随 Freely 能力一起被消费的主交付面：

- `AGENTS.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/PROJECT_INTENT.md`
- `docs/pre-brainstorms/`
- `docs/milestones.md`
- `docs/epics/`
- `docs/progress/`

### 2. Freely 开发完成后的能力目录

这些目录属于 Freely 产品/能力本体。即使它们是文档，只要发布后会被 agent / runtime / skills / CLI 直接消费或打包，就应视为 Freely 的能力输出，而不是单纯“开发过程文档”：

- `bin/`
- `docs/system/`
- `src/`（如存在）
- TUI / GUI / 前端 / Tauri / Rust runtime 对应实现目录（如存在）

判定规则：
- 如果一个文档主要用于当前研发过程中的问题收敛、issue 生命周期推进、review / verification / cleanup 留痕，它属于“指导开发 Freely”。
- 如果一个文档主要定义 Freely 运行时、agent、skill、脚本、CLI、系统行为，并会作为产品能力被长期消费或打包，它属于“Freely 能力目录”。
- Freely 是 AI 开发工具，所以 `agent`、`skill`、runtime script、系统说明文档本身就是 Freely 的能力，不因为它们是 Markdown 就降级为“仅开发辅助”。
- 开发 Freely 过程允许调用 Freely 能力目录中的 agent / skill / runtime 真源来指导开发自己；这就是吃狗粮，而不是目录混淆。

## 会话启动检查

每次会话开始：
1. **分支/Worktree检查**：如在 `main`/`develop`/`pre-test-merge` 则禁止写入。先执行 `cd <your-project-path>`，再按标准 `git worktree add -b <branch> ../<your-project-worktrees>/<branch-dir> <base>` 创建 feature worktree，并 `cd` 到该 worktree 中工作。默认 `<base>` 为 `develop`；若当前 issue 依赖未合并父分支改动，可用父 `feature/*` 作为 `<base>`，但必须在 pre-brainstorm / milestone / issue 中记录依赖关系。`<your-project-worktrees>` 指当前项目同级的 worktree 根目录，格式为 `<your-project-name>-worktrees`。`<branch-dir>` 必须与当前 worktree 派生规则一致：无日期分支使用 `<branch>` 的安全化名称；若分支名包含 `YYYYMMDD` 或 `YYYYMMDD-HHMM/HHMMSS`，目录名改为日期前置，例：`feature/foo-20260307-1015` -> `20260307-1015-feature-foo`
2. **首跳先判 loop，不要先判 cleanup**：
   - 如果是 Freely 自举中暴露的新讨论，先判它属于：
     - 现有 issue continuation
     - Freely 自身产品架构
     - Freely 开发治理
     - Freely 可复用能力
   - 若边界未稳定，先进入 `docs/pre-brainstorms/`
   - 如果当前变更已落在现有 issue scope 内，优先吸收到既有 `issue / milestones / progress / code-review` 生命周期，不要为了一个新 worktree 再伪造新 candidate / issue
   - 只有当问题已经是“现有 lifecycle 走到 merge / verification / cleanup 哪一步”时，才切到 worktree promotion / retirement 判断
3. **头脑风暴路由**：
   - 预研头脑风暴（不是基于 issue 文档）：文档放 `docs/pre-brainstorms/`
   - IBM 头脑风暴（基于 issue 文档）：文档放 `docs/epics/{epic-name}/{story-name}/brainstorms/b-{issue-name}.md`

## Freely 自举首跳

Freely 开发 Freely 时，默认先问四件事：

1. 这是新问题，还是现有 issue 的 continuation？
   - 新问题：先走 pre-brainstorm / candidate / milestone
   - 现有 issue continuation：直接回到该 issue 的 doc-loop / dev-loop / verification
2. 这是 Freely 自身产品架构、开发治理、可复用能力，还是单纯 worktree 生命周期问题？
   - Freely 自身产品架构：先看 `PROJECT_INTENT`、`CONSTITUTION`、`LAWS`，并在需要时回写 `AGENTS.md`
   - 开发治理：先看 `CONSTITUTION`、`LAWS`、现有 milestone / issue
   - 可复用能力：先看现有 `docs/system/**`、`bin/**`、实现目录与 milestone / issue 是否已吸收
   - worktree 生命周期问题：再看 `worktree-maintenance-governance` / `branch-management`
3. 这次讨论首先应落到开发文档，还是已经稳定到应进入能力目录？
   - Freely 自身产品架构与开发治理，先落开发文档
   - 只有会被 runtime / agent / skill / CLI 长期消费的稳定定义，才进入能力目录
4. 这棵树是 research-only、merge-ready、companion-only，还是 verified-retirable？
   - 不要把“已经有 feature worktree”误当成“已经完成 issue materialization”
   - 不要把“已经 merge”误当成“cleanup 已完成”

## 吃自己的狗粮规则（Freely 构建 Freely）
Freely 必须在 Freely 治理规则下开发，不得有项目特定的例外。

“吃自己的狗粮”在本项目中的具体含义：
- Freely 开发过程中暴露的问题，不只是在修当前仓库；但不要把任何新讨论都自动沉淀为 Freely 对外可复用能力。
- 先判断它是 Freely 自身产品架构、开发治理，还是 Freely 可复用能力。
- 若某个解决方案最终会被 Freely runtime、agent、skill、CLI 或打包产物长期消费，它必须落到 Freely 能力目录中，例如 `docs/system/**`、`bin/**`、实现代码目录；不要把这类能力定义留在 `pre-brainstorms`、`epics`、`progress` 等过程文档里。
- 若某个讨论首先只是在定义 Freely 自身的产品形态、宿主壳关系或开发入口判断，它应先落在 `PROJECT_INTENT / CONSTITUTION / LAWS / AGENTS.md`，而不是直接写进能力目录。
- 过程文档可以记录“为什么要做、边界如何收敛、当前结论是什么”，但不能替代最终能力真源。
- 对已经稳定、可复用的提示词编排、角色职责、执行约束，优先拆到 `agents/**` 或 `skills/**`；runtime 脚本只保留启动、上下文注入、状态托管和恢复动作。
- 开发 Freely 时调用这些 `agents/**`、`skills/**`、runtime 真源来继续开发 Freely，自身就是 dogfooding；这不是目录混用，而是产品自举。

要求：
- 使用对用户项目期望的相同分支/worktree/钩子规范。
- Worktree 根目录遵循宪法策略：项目同级目录，命名为 `{project-name}-worktrees`。
- 架构/治理变更必须先进入 `docs/pre-brainstorms/<id>/`，然后才能进入执行循环落地。
- Freely 自举中发现的新能力，默认优先判断是否已被现有 milestone-owned issue 吸收；仅当现有 issue 无法承接时，才新开 candidate / issue。
- 若当前项目的 Freely runtime 已在运行，优先通过 `./bin/freely chat --project <project-root> <message>` 这类 human interruption / intake 入口指导它继续开发；不要绕过 runtime 另造一套平行调度。
- 若在插话驱动的开发过程中发现 bug、缺口或新的能力沉淀点，仍按同一治理规则处理：必要时让 Freely 创建/进入 dedicated worktree 修复、验证、合并到 `develop`、重启 runtime，再继续通过 interruption 推进。
- 优先使用预检 + 可操作的修复方案，而非重复的权限提示。
- 当主管委派 worker 时，worker prompt 必须带稳定的 machine-readable `Worktree:` 与 `Branch:` header；自然语言说明可以补充，但不能替代 runtime 可消费的目标工位锚点。
- 若主管同轮排多个 lane，worker prompt 还必须带 `dispatch_priority`、`parallel_safe`、`write_scope`；超出 capacity 或冲突的 lane 只能进入 queue / frozen queue，不得直接 launch。

## 执行指引
- 保持本文件简洁稳定；不要重复宪法/法律中的详细规则。
- 将细节添加到规范文档中，然后在此引用。
- 当出现不确定性时，打开/更新一个预研头脑风暴条目，先在那里收敛。

## 基本命令
- `./bin/freely init|doctor|start|status|baseline-status|live-status|fleet-status|stop`
- `./bin/governance-check`
- `./bin/test-pre-push-hook`
- `cd <your-project-path>`
- `./bin/wt-create <branch> [--base <base-branch>]`
- `git worktree add -b <branch> ../<your-project-worktrees>/<branch-dir> <base>`
- `git worktree remove ../<your-project-worktrees>/<branch-dir> && git branch -d <branch>`
- `source ./bin/wt-enter <branch>`
- `source ./bin/wt-add <branch> -- <git-add-args>`
