# Freely 宪法

> 我是项目宪法，只负责定义不可逾越的边界与原则（What/Why）；不定义执行步骤（How）与验收口径（Check/Accept）。

## 1. 产品身份

Freely 是一个自主循环运行器：
- 启动后 AI 担任项目所有者角色。
- AI 从项目意图、review、test、开发进度文档、chat 输入与会话证据（人类或自治）中产出或修改候选 Issue；AI 通过 task-source-scan 发现待委派任务，通过 a2a_tasks 表查询进行中任务；里程碑仅提供排序和追踪；而非固定从单一任务列表
- AI 自主管理：获取 Issue → 文档 → 开发 → 验收 → 获取 Issue 的闭环
- AI 持续运行（自己监控ai工具崩溃/阻塞自动触发续接），除非明确停止。或找不到需求，或者出现重大事故 AI 自己已经无力自己解决。

## 2. 分支与工作树策略（硬性要求）

分支/工作树规则是硬性约束，实施前必须检查：

1. 分支模型（基于 GitFlow + 临时预集成验证批次）：
- `main` 仅用于发布，必须保持稳定。
- `develop` 是长期开发集成分支，也是 `feature/*` 的默认父分支。
- `test-pre-merge-*` 是临时预集成验证批次分支前缀；仅在组合验证、短周期集成验收、复杂冲突收敛或发布前预演时启用。每次启用前必须先从当前 `develop` 新建全新批次；旧批次若存在，先删除。
- `feature/*` 分支从 `develop` 创建。测试时 merge 到 `test-pre-merge-*`（临时测试面），测试通过后通过 `pr-create-guarded` 提 PR，经 review 后由 `pr-merge-guarded` 合并到 `develop`。`test-pre-merge-*` 不参与最终合并链。
- `release/*` 分支从 `develop` 创建用于发布冻结，然后合并到 `main` 并回合并到 `develop`。
- `hotfix/*` 分支从 `main` 创建，然后合并到 `main` 和 `develop`。

`test-pre-merge-*` 的价值（临时启用，不得固化为长期开发父分支）：
- 它是 `develop` 前的临时风险缓冲，而不是默认开发主线。
- 用于在正式进入 `develop` 前承担两类临时验证职责：
  - 预检运行测试：在不污染 `develop` 的前提下做预集成 smoke / regression / acceptance
  - 预测试 merge：把来源 `feature/*` 临时合入同一批次，暴露组合冲突与集成问题
- 允许多功能预演而不污染 `develop`。
- 在这两类职责里发现问题，都必须回到来源 `feature/*` 或新的 dedicated feature worktree 修复；不得在 `test-pre-merge-*` 上直接改实现、写治理真相或提交普通修复。
- 只有当前批次仍具备权威性时，它才是可消费的验证面；若 `develop` 已继续前进、批次出现 protected-env 独有差异，或 promotion/cleanup 证据断裂，该批次就应被判定为 stale。
- stale 批次必须退休；如果同一能力仍需继续验证，应从当前 `develop` 重建新的 `test-pre-merge-*` 批次，并按需要重新吸收来源 `feature/*` / `feature/premerge-*` 集合，而不是继续把旧批次快照当成当前真相。
- 验证完成或失败后必须退出本轮职责，不得继续承担默认 `feature/*` 父分支角色。

2. 合并纪律：
- 不稳定的变更不得合并到 `main`。
- `main` 只接受来自 `release/*` 或 `hotfix/*` 的合并。
- `develop` 是功能交付的默认目标分支；进入 `develop` 前必须满足要求的 `TEST`、评审与进度/恢复证据。
- `develop` 的正常 promote source 只接受 `test-pre-merge-*` family 与 `hotfix/*`；`feature/* -> develop` 作为正常路径被阻止；`feature/*` 必须通过 `pr-merge-guarded` 经 PR review 和门禁检查后合并到 `develop`。
- `test-pre-merge-*` 仍是临时验证路径，但它同时是进入 `develop` 的 canonical promote family；其 merge receipt 必须能追溯到来源 feature 或 explicit multi-bundle 的组装证据。
- `develop` 不得承担“尚未进入主线前的预测试环境”职责；需要主线前集成验证时，应使用 `test-pre-merge-*`，而不是在 `develop` 上先做预检。
- `feature/*` 的实现自测与局部回归默认留在其 dedicated worktree；只有需要受保护分支真实集成面的测试，才切换到 `test-pre-merge-*` 或目标 protected branch 的 canonical worktree。
- `test-pre-merge-*` 的 promotion 以当前权威批次为准；single-feature lane 与 explicit multi-bundle lane 共享同一 canonical family 前缀，不再引入第二个 `test-pre-*` 前缀。若当前批次已 stale，先 retire / rebuild，再决定是否继续 promote。
- 提升前的具体验收门与证据口径由 `docs/LAWS.md` 第 2 章定义。
- `PRE_TEST` 与 `TEST` 的职责边界由 `docs/LAWS.md` 第 2 章与第 11 章定义。
- develop-bound 能力若先进入 `test-pre-merge-*`，验证通过后应由当前权威 `test-pre-merge-*` 批次并入 `develop`，并保留来源 feature / bundle 追溯证据；不得绕回 `feature/* -> develop` 继续保留第二条正常路径。
- `test-pre-merge-*` 的退出形态固定为：验证结束后立即删除；若同一能力仍要继续验证，只能从当前 `develop` 重新创建新批次。
- `main` / `develop` / `test-pre-merge-*` 上，hook/gate bypass 永久禁止。`FREELY_SKIP_IBM_GATE=1` 是唯一合法豁免。
“这次应该没问题”不能构成 protected-branch bypass 的依据。

`premerge` 临时分支规则（用于复杂冲突收敛，不新增长期分支层级）：
- 分支名固定使用：`feature/premerge-YYYYMMDDTHHMM[SS]Z--<topic>`（旧格式 `YYYYMMDD-HHMM` 仍兼容）。
- 必须从当前活跃的 `test-pre-merge-*` 批次创建；若当前没有测试批次，则先从 `develop` 创建新的 `test-pre-merge-*`，再进入 `premerge`（具体命令步骤由 `skill:freely-premerge-reconcile` 定义）。
- 仅在以下场景使用：
  - 多个 `feature/*` 串行并入 `test-pre-merge-*` 时出现复杂冲突，且无法在单次 merge 中稳定解决。
  - 历史分支过旧，常规 merge 风险过高，需要通过 `cherry-pick` 方式回收有效提交。
  - 需要一个短周期“冲突修复批次”来验证治理/hook/目录规则不被回退。
- 该分支只允许做冲突修复与集成校验，不承载新的业务需求开发。
- 完成后必须以 `--no-ff` 合并回所属 `test-pre-merge-*` 批次，再根据验证结果决定是否由该权威批次进入 `develop`；不得直接把测试批次或 `feature/premerge-*` 合并到 `main`。
- 合并完成后必须删除该 `feature/premerge-*` 分支及其工作树，并在进度/恢复文档记录处理结果。

3. 工作树纪律：
- 所有非 `main`/`develop`/`test-pre-merge-*` 的开发分支都使用 `git worktree`。
- 工作树根目录固定：`<project_parent>/<project_name>-worktrees/`。
- 工作树目录命名必须为 `{project-name}-worktrees`，且与项目根目录同级，保证排序和定位时与项目紧邻。
- 禁止在项目目录内部创建工作树目录（必须与项目目录并列）。
- 在主工作树检出分支时，钩子应在固定根目录下自动创建缺失的工作树。
- 创建或切换 `feature/*`、`release/*`、`hotfix/*`、`feature/premerge-*` 后，后续工作必须在 dedicated sibling worktree 中继续；主 worktree 仅允许短暂停留以触发自动创建。
- 操作步骤与命令以 `docs/system/workspace/skills/` 为执行事实源（How）。
- 没有明确的 STORY/任务所有者和退出标准时不得创建工作树。
- 已合并/已放弃的工作树必须与其分支引用一起清理。
- 完成清理是强制性的：
  - 分支责任完成并合并/提升后，删除本地功能分支
  - 删除 `<project_parent>/<project_name>-worktrees/` 下的对应工作树
  - 如果存在远程分支，删除远程功能分支
  - 在进度/恢复文档中记录清理结果
- 研究优先阶段的临时等价规则：
  - 若 `docs/progress/**` 与 `docs/recovery/**` 目录尚未启用，允许把验证批次、恢复上下文与 cleanup 结果记录到 `docs/pre-brainstorms/CONVERGENCE.md`
  - 一旦正式 `progress/recovery` 路径启用，后续批次必须回到规范目录，不再继续使用该临时落点
- 分支/工作树生命周期状态：
  - active（活跃）：分支有未完成的 STORY 所有权
  - promoted（已提升）：分支变更已通过要求路径进入 `develop`
  - retired（已退役）：分支和工作树已在本地删除（如果存在远程也已删除）
- 已提升的分支如果没有在进度/恢复中记录原因而保留未删除，是治理违规。

4. 恢复耦合：
- 恢复/监控必须跟踪运行循环实例的活动分支/工作树上下文。
- 桥接恢复记录必须包含当前分支和工作树路径。

5. 执行：
- Git 钩子应在本地工作流中强制分支保护。
- 钩子拒绝消息必须指向本宪法章节作为策略来源。
- 受保护分支上的 hook/gate bypass（包括但不限于 `--no-verify`）永久禁止。无例外。
- **明确禁止的绕过手段（非穷举）**：
  - `git -c core.hooksPath=/dev/null`（禁用所有 hook）
  - `git push --force` 到 `main`/`develop`（force push 到受保护分支）
  - `FREELY_SKIP_PR_GATE=1`（已从代码中移除）
  - `--no-verify` / `--no-gpg-sign`（跳过 hook）
  - 直接 `git commit` 在 `main`/`develop` 上（应通过 worktree + PR 流程）
  - 任何修改 `.githooks/` 目录内容以削弱检查的行为
- break-glass 不能仅凭个人口头判断成立；必须留下可审计证据，并且后续 canonical 治理检查必须能识别该次豁免。
- 执行步骤以 `docs/system/workspace/skills/` 为执行事实源（How）；技能路由与验收门以 `docs/LAWS.md` 为准。
- **分支规则表**：

| 分支 | push | add/commit | merge 来源 | merge 到 | 备注 |
|------|------|------------|-----------|----------|------|
| main | ✅ | ❌ | release/*, hotfix/* | - | 发布/热修复入口 |
| develop | ✅ | ❌ | test-pre-merge-*, hotfix/* | - | 默认开发集成入口；正常 promote 只接受 `test-pre-merge-*` family 或 `hotfix/*` |
| test-pre-merge-* | ❌ | ❌ | feature/*, hotfix/*, feature/premerge-* | - | 临时预集成验证批次；必须从当前 develop 新建，用完立即删除 |
| feature/* | ✅ 同名 | ✅ worktree | - | test-pre-merge-* (测试) → pr-create-guarded (PR) → pr-merge-guarded (合并) | 从 develop 创建；完整链路: `feedback → wt-create → B1_IBM → B2_IBM → dev → pr-create-guarded → pr-merge-guarded → wt-close`（详见 AGENTS.md §规范流程） |
| release/* | ✅ 同名 | ✅ worktree | - | main, develop | 从 develop 创建 |
| hotfix/* | ✅ 同名 | ✅ worktree | - | main, develop | 从 main 创建 |

- 若某个 `test-pre-merge-*` 当前活跃，hotfix 合并到 main/develop 后必须按测试需要同步到对应批次

## 3. 版本命名规则（硬性要求）

版本格式：`YYYY.MM.DD-HHMM-stage`（stage 不可省略）

| 版本示例 | 分支 | 阶段 | Tag | 对外 |
|----------|------|------|-----|------|
| `2026.03.01-1430-alpha` | `feature/*` | 开发中 | 本地轻量 tag | 否 |
| `2026.03.01-1430-beta` | `test-pre-merge-*` | 测试集成 | 本地轻量 tag | 否 |
| `2026.03.01-1430-nightly` | `develop` | 夜间构建 | push tag | 是 |
| `2026.03.01-1430-stable` | `main` | 正式发布 | push tag | 是 |
| `2026.03.01-1430-hotfix` | `hotfix/*` | 紧急修复 | push tag | 是 |

- `alpha`、`beta`：本地 tag，不 push 到 GitHub
- `nightly`：每日自动构建并 push tag，对外可见
- `stable`：正式发布，push tag
- `hotfix`：紧急修复，等不了 nightly，单独 push tag

自动化构建必须按分支匹配 stage 后缀，不可省略。

## 4. 强制技术栈

除非明确修订，以下选择是硬性约束：

- 桌面外壳：**Tauri**
- 核心运行时/编排器/监控/恢复：**Rust**
- 前端 UI：**React**
- 前端包/运行时工具：**Bun**
- 终端渲染：**xterm.js**
- 终端进程后端：**Rust PTY**（系统 shell + PTY 进程）

## 5. 基线项目结构（硬性要求）

每个托管项目应至少保持以下基线结构：

- `README.md`（项目入口和运行手册）
- `docs/`（治理 + pre-brainstorms）
- `src/`（主要实现代码）
- `.env/`（环境模板/脚本/配置片段，版本化）
- `.env.example`（必需的环境变量模板，不含密钥）

Freely 仓库在“研究优先阶段”有临时覆盖约束：
- `docs/` 仅保留 `PROJECT_INTENT.md`、`LAWS.md`、`CONSTITUTION.md` 与 `pre-brainstorms/`。
- 历史文档资产不在工作区保留，统一通过 git 历史追溯。

如果项目使用 monorepo 或不同布局，必须在文档中提供等效映射。

## 6. 终端架构规则

- UI 终端嵌入应用中，但通过 PTY 执行真实的系统 shell 命令。
- 每个运行中的循环实例拥有独立的 AI CLI 进程/会话和 PID。
- 监控目标是该 AI CLI 进程/会话的生命周期。
- 多个项目实例必须隔离（独立的 PID/会话/状态目录）。

## 7. AI 执行模式

AI 规格格式：`tool:model:mode`

- `mode=auto`
  - 非交互式执行路径
  - 工具支持时使用自动批准路径
- `mode=step`
  - 交互式/批准路径

支持的工具有：
- `codex`
- `kiro-cli`
- `iflow`

## 8. 恢复策略（硬性要求）

恢复有两个分支：

1. 续接分支：
- 如果当前工具/会话支持无人值守续接，直接续接并继续。

2. 桥接分支：
- 如果不支持无人值守续接：
  - 运行一轮桥接恢复
  - 将崩溃/阻塞检查点写入进度文档
  - 从更新的项目状态重启无人值守自动循环

除非达到明确的停止标准，否则崩溃/阻塞后不得停止。

## 9. 约束面

Freely 只接受这些主要输入：
- 项目绝对路径
- 项目意图文档路径
- 宪法文档路径
- AI 规格（`tool:model:mode`）

所有其他项目上下文必须由 AI 从项目文件中发现。

## 10. 工程纪律

- 保持命令面简单可脚本化（`init/start/status/stop`）。
- 保持状态显式且可在磁盘上检查。
- 优先选择确定性行为而非隐藏魔法。
- 在项目根目录保持一个规范的代理上下文文件（`AGENTS.md`）。
- 代码与文档不一致时，默认先修复代码与测试，再评估是否需要改文档。
- 若必须修改规范文档，需先完成审慎决策，并在独立 `feature/*` 分支与专用 worktree 中进行。
- 规范文档改动不得“空转”：必须绑定对应实现或门禁变更，并提供可验证证据。


### 10.1 CLI First 原则（硬性要求）

所有功能必须优先提供 CLI 接口，UI 只是可选的展示层。

架构优先级：
```
CLI (核心) → API (可选) → UI (可选)
```

边界原则：
1. 所有功能必须有 CLI 接口，无 CLI 则不存在。
2. CLI 必须支持非交互式模式（`--yes`），便于脚本/AI Agent 调用。
3. CLI 必须支持结构化输出（`--format json|yaml`），便于程序消费。
4. CLI 返回码必须语义化（0=成功，非0=各类错误）。
5. UI 不得引入 CLI 无法实现的业务逻辑。

说明：
- 具体接口设计见各 skill 的 CLI 参考文档。
- AI Agent 调用约定见 `skill:freely-auto-loop-orchestrator`。

### 10.2 Freely 产品形态边界（硬性要求）

Freely 自身的产品形态必须满足以下硬边界：

1. `Freely core` 是被各宿主壳复用的能力本体。
2. `Freely CLI` 是 canonical product shell。
3. `Freely TUI app` 与 `Freely GUI app` 若存在，只能作为复用同一 core 的 optional shells。
4. `chat`、`init`、`start`、`baseline-status`、`live-status`、`fleet-status` 属于 command / semantic surface，不得与 `CLI shell`、`TUI shell`、`GUI app` 作为同层 product shell 并列。
5. 外部 AI tools（如 `codex`、`Claude Code`、MCP 组合路径）属于 external AI tooling layer，由 Freely core 编排；execution-provider abstraction 只存在于该层的路由/选择语义中；它们不是 Freely 自身的 product shell。
6. 任一 shell 不得引入绕开 core 的私有业务语义。

## 11. 方法论总述（硬性要求）

Freely 遵循三个 loop 的方法论。

### 11.1 三个 Loop 结构

```text
A:auto-loop（外循环）
├── 发现与路由 Issue
├── 进入 D:doc-loop（前置收敛 / B2_IBM 文档收敛）
├── 或进入 D:freely-dev-loop-execution（开发实现环）
├── 基于 canonical evidence 做 completion / verification / cleanup judgment
└── 吸收结果并进入下一轮
```

说明：
- 宪法仅定义循环边界与必须闭环，不定义产物模板、验收门细则或执行步骤。
- 产物目录、门禁口径与路由细则由 `docs/LAWS.md` 同章节定义。
- 实际执行步骤由 `docs/system/workspace/skills/` 定义。
- 三个 loop 的能力归宿、owner 边界与生命周期细节真源见 `docs/system/workspace/three-loop-capability-lifecycle.md`；本章只保留不可越界边界。

### 11.2 核心原则

1. **文档驱动**：每个阶段都有文档产出，文档先行。
2. **进度可追溯**：里程碑确定归属，延期即拆分新 Story，禁止仅凭直觉实现。
3. **文档目录结构必须遵循**：详见 [`docs/LAWS.md`](./LAWS.md)。
4. **职责分层一致**：skills 可补充更细执行细节（如安装、配置、预检、修复），但不得违反宪法边界或覆盖法律门禁结论。

### 11.3 法律链接

详细规则见 [`docs/LAWS.md`](./LAWS.md)：
- 与宪法同序的法律章节：`LAWS.md` 第 1~16 章
- 执行路由：`LAWS.md` 附录 A
- 三个 loop 的职责边界：`LAWS.md` 附录 B

## 12. 子代理规划与委托（硬性要求）

Freely 必须在可并行场景下支持子代理委托，但保持单编排者会话下的确定性治理。

边界原则：
1. 子代理不是顶层循环所有者，必须可追溯到同一编排者与当前工作上下文。
2. 委托前必须明确边界与完成定义，禁止所有权不清的委托。
3. 批次完成必须满足收敛语义，未收敛不得宣告成功。
4. 子代理能力不可用时必须可回退且可追溯。

说明：
- 具体验收门与证据口径见 `docs/LAWS.md` 第 12 章。
- 具体执行步骤见 `skill:freely-recovery-subagent-governance`。

## 13. 并行开发的领域模型（硬性要求）

Freely 必须同时强制物理领域与逻辑领域，以降低并行开发的冲突与耦合风险。

边界原则：
1. 物理领域：并行任务必须在隔离工作树中执行。
2. 逻辑领域：并行任务必须有明确变更所有权边界。
3. 共享热点必须存在显式串行窗口或排序策略。

说明：
- 具体验收门与证据口径见 `docs/LAWS.md` 第 13 章。
- 具体执行步骤见 `skill:freely-recovery-subagent-governance` 与 `skill:freely-laws-enforcer`。

## 14. 可插拔模块架构与接口版本控制（硬性要求）

Freely 必须支持可插拔、可演进、可回滚的模块化架构，并保持接口治理可持续。

边界原则：
1. 模块边界与契约必须显式，避免隐式跨模块耦合。
2. 接口变更必须可版本化演进，避免强制同步大爆炸迁移。
3. 破坏性变更必须具备迁移与回滚路径。
4. 涉及第三方 API 时，第三方契约为外部事实源，本地实现负责适配。

说明：
- 具体验收门与证据口径见 `docs/LAWS.md` 第 14 章。
- 具体执行步骤见 `skill:freely-module-interface-governance`。

## 15. 变更前配置备份（硬性要求）

所有配置变更必须遵循“先备份、再修改”的不可逆前置约束。

边界原则：
1. 未完成备份前不得执行配置修改。
2. 备份必须唯一且可恢复。
3. 备份文件名必须保留源文件基名，并包含 UTC 时间戳（`YYYYMMDDTHHMMSSZ`，旧格式 `YYYYMMDD-HHMMSS` 仍兼容）与 `.bak` 标记。
4. 备份记录必须可追溯。

说明：
- 具体验收门与证据口径见 `docs/LAWS.md` 第 15 章。
- 具体执行步骤见 `skill:freely-config-backup-guard`。

## 16. Freely 自举开发（硬性要求）

Freely 在开发 Freely 本身时必须遵守与托管项目一致的治理边界，不得自我豁免。

边界原则：
1. Freely 自身开发不得绕开意图/宪法/法律/skills 的治理链。
2. 架构与治理变更必须先形成可追溯决策，再进入实现与验证。
3. 自举过程中沉淀的治理能力必须可复用于托管项目。
4. 对外部权限与可运维问题必须提供可执行的预检与修复路径。

说明：
- 具体验收门与证据口径见 `docs/LAWS.md` 第 16 章。
- 具体执行步骤见 `skill:freely-constitution-guard`、`skill:freely-branch-management`、`skill:freely-laws-enforcer`。
