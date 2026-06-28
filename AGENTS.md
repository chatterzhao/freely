# Agent 上下文入口

## 权威来源（按优先级排序）
1. `docs/CONSTITUTION.md`（硬性约束）
2. `docs/LAWS.md`（操作规则）
3. `docs/PROJECT_INTENT.md`（产品方向）
4. `AGENTS.md`（仅入口指引，不得覆盖 1-3）

如果本文件中的任何陈述与上述三个核心文档冲突，以核心文档为准。

## 禁止操作

以下操作违反 `CONSTITUTION.md` §5（执行），**任何情况下不得使用**：

- `git -c core.hooksPath=/dev/null <command>` — 禁用 hook
- `git push --force` 到 `main` 或 `develop`
- `--no-verify` / `--no-gpg-sign` — 跳过 hook
- 直接在 `main`/`develop` 上 `git commit`
- 修改 `.githooks/` 目录内容以削弱检查

**没有例外。** 即使为了调试或加速迭代也不允许。
正确的做法是走标准开发流程:

```
feat: ([命令] feedback) → [命令] wt-create → [skill] B1 → [skill] B2 → [skill] dev → [skill] test → [命令] pr-create → [命令] pr-review → [命令] pr-merge → [命令] wt-close
fix:  ([命令] feedback) → [命令] wt-create → [skill] dev → [skill] test → [skill] B1 → [skill] B2 → [命令] pr-create → [命令] pr-review → [命令] pr-merge → [命令] wt-close

     反馈: freely feedback --repo <repo> --title "..." --body "..."         (raw issue 不存在时需要)
     评论: freely comment --issue raw-{key} "原话"                           (向已有 raw issue 追加评论)
     讨论: freely discuss [--continue <id>] [--archive <id>]                  (AI 群聊讨论)
     工位: wt-create --raw-key <key> --source platform --skill <skill> --slug <slug>
     B1:   skill:freely-doc-B1_IBM-execution
     B2:   skill:freely-doc-B2_IBM-execution
     dev:  skill:freely-dev-loop-execution
     test: skill:freely-test-execution
     pr:   pr-create-guarded → pr-review-guarded → pr-merge-guarded
     收口: wt-close <branch>
```

> **`[命令]`** = bin 脚本，在 shell 中直接执行。**`[skill]`** = skill:xxx，由 AI agent 通过 Skill 工具加载。
> Skill 是流程的权威来源——具体步骤见各 skill 的 SKILL.md。
> `()` = 可选步骤（raw issue 已存在则跳过）。

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
- `docs/system/workspace/ibm-framework.md`（IBM Framework 能力真源）

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
1. **分支/Worktree检查**：如在 `main`/`develop`/`test-pre-merge-*` 分支则禁止写入、提交，它们只接受 merge。若是启动 Freely runtime，应在项目根目录启动，但这不放宽 protected root 的 owner-development 禁令；实际写入必须由 Freely 委派到 dedicated worktree。先执行 `cd <your-project-path>`，再优先使用标准入口 `./bin/wt-create <branch> [--base <base>]` 创建 fix|feature worktree，并 `cd` 到该 worktree 中工作。只有在基础设施受限、必须手工执行 `git worktree add -b <branch> ../<your-project-worktrees>/<branch-dir> <base>` 时，才允许裸建树，并且随后必须立刻执行 `./bin/freely sync-tooling --source-project <your-project-path> --project ../<your-project-worktrees>/<branch-dir>`。默认 `<base>` 为 `develop`；若当前 issue 依赖未合并父分支改动，可用父 `feature/*` 作为 `<base>`，但必须在 pre-brainstorm / milestone / issue 中记录依赖关系。`<your-project-worktrees>` 指当前项目同级的 worktree 根目录，格式为 `<your-project-name>-worktrees`。`<branch-dir>` 必须与当前 worktree 派生规则一致：无日期分支使用 `<branch>` 的安全化名称；若分支名包含 `YYYYMMDD` 或 `YYYYMMDDTHHMMZ`/`YYYYMMDDTHHMMSSZ`（旧格式 `YYYYMMDD-HHMM` 仍兼容），目录名改为日期前置，例：`feature/foo-20260307T1015Z` -> `20260307T1015Z-feature-foo`
   - 先确认 `git config --get core.hooksPath` 返回 `.githooks`。仓库中“存在 hook 脚本”不代表 Git 已启用它们；只有 `core.hooksPath=.githooks` 时，根目录 `.githooks/` 包装层才会实际转发到 `docs/system/workspace/hooks/*.sh` 执行门禁。
   - `test-pre-merge-*` 是一次性本地测试批次：必须从当前 `develop` 新建，只允许 merge 装配验证，不允许普通写入/提交/push，不允许承载 owner / milestone / continuation 真相，测试结束后立即删除。
  	   - **test-pre-merge 的职责**：验证 feature 能否在真实环境中正常工作，保证 develop 只接受已验证的代码。
  	     - develop 的干净面 = 每次 merge 前都经过了 test-pre-merge 的端到端验证
  	     - 未经 test-pre-merge 验证的代码不得 merge 到 develop
  	   - **test-pre-merge 运行环境初始化**：
  	     - pre 工位从 develop 创建后是裸分支，无 config、无 session-store、无 continuity
  	     - 必须运行 `./bin/pre-init-runtime --pre-project <pre-worktree>` 从 develop 复制运行时状态
  	     - 这会复制 config.toml（修正路径）、freely.db（session-store）、tool-boundary-bootstrap
  	     - 初始化后 pre 工位具备完整的 Manager 运行能力
  	   - **test-pre-merge 的验证**：验证方式由 pre-tests.md 中的测试用例决定（pre-tests.md 由 B2_IBM 编写，test-execution 执行）。feature 合并到 test-pre-merge 后必须通过验证才能合并到 develop。具体测试步骤由项目对应的 pre-tests.md 定义。

  	     Freely 自举端到端门禁（daemon 型项目参考）的 pre-tests.md 应定义自举验证所需步骤，通过预置脚本 `./bin/test-pre-merge-selfhost <project>` 执行。成功标准：打包版本能开发 Freely 自己。这个测试落地了"编译器自举"——用上一个版本开发下一个版本。通过 → pr-merge-guarded develop <feature-branch> 合并；失败 → 丢弃 test-pre-merge，修 feature。
   - 跑测试先判 lane：dedicated `feature/*`、`feature/premerge-*`、`release/*`、`hotfix/*` writable worktree 跑 `feature-local`；`test-pre-merge-*` 跑 `premerge-integration`；受保护分支 merge 后 followthrough 跑 `post-merge-followthrough`。不要把 `develop` 当成主线前预测试环境。
   - 测 worker/feature lane 示例：`/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-startup-task-source-patrol-and-reconcile/bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-startup-task-source-patrol-and-reconcile`
   - 测未 merge 的主管态示例：`/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-startup-task-source-patrol-and-reconcile/bin/freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`
2. **大重构先做 fleet sequencing audit**：若当前任务会同时改多层真源、跨多个现有 worktree / issue，或可能重排架构主干，先运行 `git worktree list --porcelain`、`./bin/wt-fleet-status`、`./bin/freely live-status --project <project-root>`、`./bin/freely fleet-status --project <project-root>`，并把结果与 `docs/milestones.md` / 相关 `progress` 对齐。优先收束 `dirty` 或仍在 `desired=running` 的 worktree，识别必须先合并的上游治理树，再决定是否开大重构 lane；不要在 fleet 状态模糊时直接开始深层重构。
3. **首跳先判 loop，不要先判 cleanup**：
   - 如果是 Freely 自举中暴露的新共性问题，先判它是否应成为 Freely 能力发现；若边界未稳定，先进入 B1_IBM（`docs/pre-brainstorms/`）
   - 如果当前变更已落在现有 issue scope 内，优先吸收到既有 `issue / milestones / progress / code-review` 生命周期，不要为了一个新 worktree 再伪造新 candidate / issue
   - 只有当问题已经是“现有 lifecycle 走到 merge / verification / cleanup 哪一步”时，才切到 worktree promotion / retirement 判断
4. **IBM Framework 路由**：工作项按 `docs/system/workspace/ibm-framework.md` 定义的两阶段推进。
   - B1_IBM（Input → Brainstorm → Milestone）：Input source（github/gitee issue、chat 插话）→ 预研收敛 → candidate 入里程碑。文档落 `docs/pre-brainstorms/{b1-id}/`
   - B2_IBM（Input → Brainstorm → Map）：Input source（milestone committed_issues 中的正式 issue）→ 实现设计 → Map 产物（epic/story/{name}/ + PRD + pre-tests + tasks + code-review）。文档落 `docs/epics/{epic-name}/{story-name}/`

## Freely 自举首跳

Freely 开发 Freely 时，默认先问四件事：

1. 这是新问题，还是现有 issue 的 continuation？
   - 新问题：先走 B1_IBM → candidate → milestone
   - 现有 issue continuation：直接回到该 issue 的 doc-loop / dev-loop / verification
2. 这是 Freely 自身产品架构、开发治理、可复用能力，还是单纯 worktree 生命周期问题？
   - Freely 自身产品架构：先看 `PROJECT_INTENT`、`CONSTITUTION`、`LAWS`，并在需要时回写 `AGENTS.md`
   - 开发治理：先看 `CONSTITUTION`、`LAWS`、现有 milestone / issue
   - 可复用能力：先看现有 `docs/system/**`、`bin/**`、实现目录与 milestone / issue 是否已吸收
   - worktree 生命周期问题：再看 `freely-worktree-maintenance-governance` / `freely-branch-management`
3. 这次讨论首先应落到开发文档，还是已经稳定到应进入能力目录？
   - Freely 自身产品架构与开发治理，先落开发文档
   - 只有会被 runtime / agent / skill / CLI 长期消费的稳定定义，才进入能力目录
4. 这棵树是 research-only、merge-ready、companion-only，还是 verified-retirable？
   - 不要把”已经有 feature worktree”误当成”已经完成 issue materialization”
   - 不要把”已经 merge”误当成”cleanup 已完成”

## 核心开发流程

所有代码改动（feature、fix、hotfix）必须走完整流程，develop 禁止直接写入。

入口是"或"的关系：
- **feedback**：新问题摄入 → 创建 raw issue，等待 scan 发现
- **scan**：发现已有 raw issue → 创建工位继续；或发现已有工位 → 直接进入继续；或判定需要 feedback → 创建 raw issue

```
入口: feedback ──→ raw issue ──┐
      scan ──→ 已有 raw issue ─┤
      scan ──→ 已有工位 ──→ 直接进入继续
                                ↓
阶段0: (可选) [命令] freely feedback --repo <repo> --title "..." --body "..."  — 无 raw issue 时创建
阶段1: [命令] wt-create --raw-key <key> --source platform --skill <skill> --slug <slug>
阶段2: [skill] skill:freely-doc-B1_IBM-execution（brainstorm → candidate → promote/absorb/drop）
阶段3: [skill] skill:freely-doc-B2_IBM-execution（I-* → prd/pre-tests/tasks/code-reviews）
阶段4: [skill] skill:freely-dev-loop-execution（写代码 → RED-GREEN 验证 → commit）
阶段5: [skill] skill:freely-test-execution（test-pre-merge 工位逐条执行 pre-tests → 全绿）
阶段6: [命令] ./bin/pr-create-guarded → pull develop → 冲突处理 → dry-run gate → push → platform-adapter
阶段7: [命令] ./bin/pr-review-guarded → 6 维 review → verdict 文档
阶段8: CI check → Approval
阶段9: [命令] ./bin/pr-merge-guarded → PR gate → promotion gate → merge → develop-push → platform-adapter
阶段10: [命令] ./bin/wt-close
```

| 步骤 | 操作 | 类型 | 谁执行 |
|------|------|------|--------|
| 0. 反馈 | `freely feedback --repo <repo> --title "..." --body "..."` (raw issue 不存在时) | [命令] | Manager/开发者 |
| 1. 开工位 | `./bin/wt-create --raw-key <key> --source platform --skill <skill> --slug <slug>` | [命令] | Manager/开发者 |
| 2. B1_IBM 预研 | B1:IBM（brainstorm→candidate→milestone） | [skill] skill:freely-doc-B1_IBM-execution | Worker |
| 3. B2_IBM 设计 | B2:IBM（I-*→prd/pre-tests/tasks/code-reviews） | [skill] skill:freely-doc-B2_IBM-execution | Worker |
| 4. Dev 实现 | dev-loop-execution → 写代码 → RED-GREEN → commit | [skill] skill:freely-dev-loop-execution | Worker |
| 5. Test 验证 | test-pre-merge 工位逐条执行 pre-tests → 全绿 | [skill] skill:freely-test-execution | Worker |
| 6. 提 PR | `./bin/pr-create-guarded` → pull develop → 冲突处理 → dry-run gate → push → platform-adapter | [命令] | Worker/Manager |
| 7. PR review + CI | CI check → Approval | [命令] ./bin/pr-review-guarded | Manager |
| 8. 门禁合并 | `./bin/pr-merge-guarded develop <pr-branch>` → PR gate → promotion gate → merge → platform-adapter | [命令] | Worker/Manager |
| 9. 关工位 | `./bin/wt-close <branch>` 清理工位+分支 | [命令] | Worker/Manager |

- Manager 负责入口路由（feedback/scan 判定）和步骤 0-1，Worker 负责步骤 2-9 执行
- 步骤 2-9 由 Worker 在 skill 约束下完成，完成后写 handoff JSON 汇报
- wt-close 会自动消费该工位的所有 worker handoff
- **禁止在 develop 上直接修改、提交**——那是受保护主管工位

## Bug 修复：fix skill 快速通道

当发现运行时 bug，使用 `skill:freely-fix-execution` 快速修复。先判场景：

- **原 fix|feature worktree 还在** → 直接在 fix|feature 上改、提交。走 feature → [skill] test-execution → [skill] B1_IBM → [skill] B2_IBM → [命令] pr-create-guarded → [命令] pr-review-guarded → [命令] pr-merge-guarded → develop。
- **原 feature 已退役（已合并/已删）** → 建 `test-pre-merge-*` 私有工位快测（不改不提交不推送，不违背保护约束）。验证通过后 cp 修改到新建的 `fix/*` 或 `hotfix/*` 可写工位，增量提交。
- **普通 fix** 走 `fix → [skill] test-execution → [skill] B1 → [skill] B2 → [命令] pr-create → [命令] pr-review → [命令] pr-merge → develop`；**紧急 hotfix** 用 `hotfix/*` → develop（hotfix 从 main 创建，可跳过 test-pre-merge）。
- **补齐治理**：B1_IBM（`skill:freely-doc-B1_IBM-execution`：brainstorm → candidate → milestone）→ B2_IBM（`skill:freely-doc-B2_IBM-execution`：I-* → prd → pre-tests → tasks → code-review）→ milestones.md。
- **原则**：Fix first, govern later。test-pre-merge-* 私有测试不违背保护约束。fix 工位早期创建、增量提交。

详见 `skill:freely-fix-execution`

## Skill 管理

- 本项目 skill 定义在 `docs/system/workspace/skills/`，已通过 `./bin/deploy-skills` 部署到 `~/.claude/skills/` 供 Claude Code Skill 工具调用。
- **修改任何 skill 后，必须立即执行 `./bin/deploy-skills`**，否则改动不会对当前及后续会话生效。
- 项目文件中引用 skill 时只用 skill 名（如 `skill:freely-feature-execution`），不写路径；skill 文件内部互相引用除外。
- skill 内部跨 skill 引用使用相对路径（如 `../other-skill/SKILL.md`），不使用项目绝对路径。

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
- Hook/gate bypass 永久禁止，不得自行决定 `--no-verify` 或等效绕过。`FREELY_SKIP_IBM_GATE=1` 是唯一合法豁免，仅跳过 IBM 文档门禁。gate 报文档缺失就去修文档，gate 报测试缺失就去补测试；gate 误判应修正 gate 模式，不得绕过。
- 当主管委派 worker 时，worker prompt 必须带稳定的 machine-readable `Worktree:` 与 `Branch:` header；自然语言说明可以补充，但不能替代 runtime 可消费的目标工位锚点。
- 若主管同轮排多个 lane，worker prompt 还必须带 `dispatch_priority`、`parallel_safe`、`write_scope`；超出 capacity 或冲突的 lane 只能进入 queue / frozen queue，不得直接 launch。

## 执行指引
- 保持本文件简洁稳定；不要重复宪法/法律中的详细规则。
- 将细节添加到规范文档中，然后在此引用。
- 当出现不确定性时，打开/更新一个 B1_IBM 条目，先在那里收敛。按 `docs/system/workspace/ibm-framework.md` 判定当前处于 B1_IBM 还是 B2_IBM。

### 文件规模
- 脚本（.sh/.py）：500 行内优秀，1000 行警告，不得新增超过 1000 行的单体脚本。大文件应拆分为模块。
- 文档（.md）：500 行内优秀，1000 行警告。久远的头脑风暴可以保持，活跃治理文档（AGENTS/CONSTITUTION/LAWS/PROJECT_INTENT）应力求精简。
- 当前 `docs/system/workspace/scripts/runtime/freely`（~20K 行）是已知历史债务，需逐步拆分，不要在它上面追加新功能。

## 项目级 AGENTS 管理
- Freely 面向任意托管项目时，项目根目录的 `AGENTS.md` 是第一入口；应先读项目级 `AGENTS.md`，再读 Freely 的复用能力真源。
- 当前 Freely runtime 已具备最小 `AGENTS.md` 生成能力：若目标项目缺失该文件，`freely init` 路径会补一个项目级入口文件。
- 自举开发 Freely 自己时，也遵循同一规则：当前仓库根目录的 `AGENTS.md` 就是 Freely 这个项目自己的项目级入口，而 `docs/system/**`、`bin/**` 等仍是 Freely 对外可复用能力真源。
- 若未来要增强“如何生成项目 `AGENTS.md`”的模板、注入策略或长期管理能力，应进入 Freely 能力目录与对应 owner issue；不要只在当前项目的 `AGENTS.md` 里静默漂移。

## CLI 回复风格（当前实验）
- 该实验只约束开发 Freely 过程中的人类可读 CLI 输出与 chat 回答，不把它当成 Freely 对外能力定义。
- 默认使用精炼白话文，不使用文言文或刻意风格化表达。
- 先行动后汇报；能直接执行就先执行，再给必要说明。
- 结果优先，原因随后；没有必要时不要展开背景铺垫。
- 不写寒暄、口头禅和重复性过渡句。
- 代码、命令、路径、状态词和证据必须保持精确，不为了省字牺牲可判定性。
- 需要枚举时优先列表、表格或代码块；能一句说清的，不扩成多段。

## 基本命令
- `./bin/freely init|doctor|start|status|baseline-status|live-status|fleet-status|stop`
- `./bin/freely sync-tooling --source-project <project-root> --project <worktree>`
- `./bin/governance-check`
- `./bin/test-pre-push-hook`
- `cd <your-project-path>`
- `./bin/wt-create <branch> [--base <base-branch>]`
- `git worktree add -b <branch> ../<your-project-worktrees>/<branch-dir> <base> && ./bin/freely sync-tooling --source-project <project-root> --project ../<your-project-worktrees>/<branch-dir>`
- `git worktree remove ../<your-project-worktrees>/<branch-dir> && git branch -d <branch>`
- `source ./bin/wt-enter <branch>`
- `source ./bin/wt-add <branch> -- <git-add-args>`

## 常用工具路径

- `./bin/issue-sync` — 平台 issue 同步（create/close/comment/batch）
- `./bin/pr-merge-guarded` — 门禁合并
- `./bin/governance-check` — 治理门禁检查
- `./bin/wt-create` — 创建 fix|feature worktree
- `./bin/freely-package` — 打包版本
- `./bin/issue-index` — Issue 索引管理
- 这些是独立脚本，直接 `./bin/<name>` 调用，**不是** `./bin/freely <name>` 子命令
