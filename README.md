# Freely

**一个文档驱动（SDD）、测试驱动（TDD）的项目循环运行器。目标态：AI 是项目所有者，人负责定意图和验收。**

Freely 不是“帮你写一段代码”的聊天工具，也不是固定 TODO 列表的执行器。它用 B1-IBM 把 issue/chat 收敛成 candidate，用 B2-IBM 生成 I-* + PRD + pre-tests + tasks（SDD/TDD 合同）；Manager 按 scan/文档派工，Worker 按合同用 agent harness 实现并跑 RED→GREEN，Reviewer 独立验收；最后经 PR/merge gates 合并、收口。目标是让人只在需要决策或验收时出现。

> 这是目标态，不是已量化事实：当前还没有“注意力成本/打断精度”的基线（见 [attention-metrics](docs/B1-docs/raw-20261101T031502Z/attention-metrics.md)）。

[![交付闭环](docs/assets/freely-delivery-loop.svg)](docs/assets/freely-delivery-loop.html)

> 交付主脊：B1/B2 生成 SDD/TDD 文档 → Manager/Worker/Reviewer 按文档执行 → PR 收口。交互版：[freely-delivery-loop.html](docs/assets/freely-delivery-loop.html)；系统五平面见 [freely-architecture.html](docs/assets/freely-architecture.html)。

## 为什么需要它

单个 coding agent 已经能完成“一个任务”；真正难的是让它**持续对一个项目负责**：

- **注意力瓶颈**：人不可能每天盯着 agent 决定下一步做什么。
- **上下文漂移**：长任务里，目标、约束、历史决策很容易丢。
- **治理缺口**：能写代码不等于能合并代码；没有门禁的自治就是事故。
- **连续性**：AI 工具会崩溃、卡住、被切走；项目不能因此停摆。

Freely 的答案是：把“项目意图、宪法、门禁、工位、评审、审计”做成运行时的一部分，让 AI 在约束内自主循环，而不是靠一段超长提示词祈祷它别跑偏。

## 它长什么样

| 平面 | 组成 | 回答什么问题 |
| --- | --- | --- |
| 界面面 | GitHub/Gitee issue/comment、`freely chat`/discuss、CLI（主入口）/TUI/GUI（Tauri probe） | 人从哪里进来、从哪里看结果 |
| 规格面（SDD） | Intent/Constitution/LAWS、raw issue、B1 brainstorm/candidate、B2 PRD/pre-tests/tasks、code-review | 做什么、为什么、怎么验、边界在哪 |
| 控制面 | scan（派生视图，不写回）、Manager、three-loop、A2A、gates、watchdog、freely-db | 现在轮到谁、下一步是什么、能不能过 |
| 执行面（TDD） | Worker、Reviewer、dev/test worktree、RED/GREEN、commands/scripts/skills | 实际怎么干、怎么验证 |
| 基座面 | ACP harness（Claude/Codex/OpenCode/Cline）、GitHub/Gitee | 用什么执行、外部世界在哪 |

### 交付主脊：谁在什么时候做什么

| 阶段 | 主体 | 读什么 | 产出 | 门禁/循环 |
| --- | --- | --- | --- | --- |
| B1-IBM | Worker（doc-loop） | issue/chat、Intent/Constitution/LAWS、验收 | `brainstorms.md`、`candidates.md`、milestone candidate | B1 skill；Reviewer `needs-review:b1` |
| B2-IBM | Worker（doc-loop） | candidate、实现面、验收标准 | `I-*.md`、`prd.md`、`pre-tests.md`、`tasks.md` | B2 skill；Reviewer `needs-review:b2`；pretests-gate |
| 派工 | Manager（auto-loop） | scan、milestone、phase、A2A、fleet | A2A task / 工位 | 不读代码、不下实现指令 |
| 实现 | Worker（dev-loop） | I-*、PRD、pre-tests、tasks | 代码、测试、证据、commit | Reviewer `needs-review:red/dev/test`；test-lane |
| 阶段评审 | Reviewer（watchdog 触发，独立 session） | 每阶段产物、diff、测试证据 | verdict、required fixes | fail→Worker；pass→下一阶段 |
| PR 评审 | Reviewer（`pr-review-guarded`） | PR diff、pre-tests、证据 | 四问 verdict | 3 轮不过 escalate |
| 收口 | Manager + gates | PR、test-gate、review verdict | merge、phase 更新、closeout | pr-merge-guarded / wt-close |

这张表的顺序就是 README 主图的顺序；`Manager` 只拥有“下一步”，`Worker` 拥有“怎么实现”，`Reviewer` 拥有“是否达标”。Reviewer 不是只在最后出现：B1/B2/RED/dev/test 每个阶段都可 `needs-review`，PR 前还有 `pr-review-guarded` 的四问 review。阶段评审是反馈环，PR review 才是硬合并门禁。

### 两条硬约束：SDD 与 TDD

**SDD：文档是规格与生命周期的真相。**

- 平台只是对外界面；AI 永远不直接读平台，`scan` 把 issue/comment 下载到本地 `docs/B1-docs/`，出站写平台统一走封装命令（`issue-sync` / `platform-adapter`），不直接调 `gh`/Gitee API。
- “谁在做”看 A2A，“代码/工位在不在”看 git，“测试有没有在 HEAD 跑”看 test-gate；文档负责规格与生命周期。
- B1 先把问题收敛为 candidate；B2 再物化为 I-* + PRD + pre-tests + tasks。没有规格与验收，不进入实现。
- Manager 读 scan 得到 `stage/next_action`；Worker 读 issue/PRD/pre-tests 得到任务与验收；Reviewer 读产物做独立判断。

**TDD：先证明失败，再证明通过。**

- B2 先写 pre-tests；dev 工位按 skill 先跑 RED（证明未实现/可复现），再实现。RED 是流程约束，GREEN/证据是门禁强制。
- 在 `test-pre-merge` 工位跑 GREEN；测试证据（或带理由的 not_applicable）是 PR 与 merge 的前提。
- 全部 not_applicable 是否合理由 review/skill 判断，gate 只检查理由与替代证据；不要把它当成默认免检。
- Reviewer 独立审查，不站在 Manager 或 Worker 一边。

**B1/B2 与 SDD/TDD 不是同义词**：B1 收敛“问题规格”（为什么做、边界、优先级），B2 产出“实现规格 + 验收规格”（PRD、pre-tests、tasks）。PRD 是 SDD 的合同，pre-tests 是 TDD 的合同；Worker 按合同实现，Reviewer 按合同验收。

这不是“提示词里建议写文档/写测试”，而是 runtime、skill、command、gate 一起强制的交付方式。

### 工具面：命令、脚本、skill、MCP、harness 各做什么

| 名字 | 职责 | 不是什么 |
| --- | --- | --- |
| command | 封装多步治理动作（feedback/wt-create/pr-*/wt-close） | 不是普通 `git` 糖；绕过会触发门禁 |
| script | 确定性执行 scan、状态搬运、gate、恢复 | 不做价值判断 |
| skill | 把流程、角色、门禁知识编码给 agent 加载 | 不是权限，改 skill 改不了 gate |
| MCP | 由底层 AI CLI 提供/启用；Freely 目前传 `mcpServers: []`，不编排 MCP | 不是 Freely 的编排层，也不是权限边界 |
| harness（ACP） | 真正跑模型会话的执行提供层 | 不是 Freely 的宿主，可替换 |

## 它是怎么运转的

```
issue / chat / 治理漂移
        │
        ▼
   auto-loop（Manager）
   巡检 → 判断 → 建 raw issue / 工位 → 派工 → 收口
        │
        ├── doc-loop（Worker）
        │     B1 预研 → candidate → B2 I-*/PRD/pre-tests/tasks
        │
        ├── dev-loop（Worker）
        │     RED → 实现 → test-GREEN → commit
        │
        └── delivery gate（Reviewer + gates）
              review verdict → PR → merge → closeout
```

三个常驻 loop + 两段交付门禁：

- **auto-loop**：唯一调度中枢。决定“现在做什么、派给谁、什么时候收口”。
- **doc-loop**：B1 收敛问题，B2 生成 SDD/TDD 合同；它不是“写文档”，是生成可执行的规格与验收。
- **dev-loop**：Worker 按合同在独立 worktree 实现，在 `test-pre-merge` 工位验证。
- **delivery gate**：Reviewer 独立审查，PR/merge/closeout 门禁执行；它不是第四个常驻 loop，而是 dev-loop 完成后的交付段。

验证不是“agent 说完成了”，而是**门禁 + 证据**：B1/B2 文档、RED/GREEN 记录、独立 review verdict、PR gate、merge gate、closeout。

## 快速开始

### 依赖

- macOS / Linux，`bash`、`git`
- Python 3.11+（runtime 与 `freely-db`）
- 一个支持 ACP 的 AI CLI：Claude Code、Codex、OpenCode 或 Cline
- Node.js 20+（仅 TUI/GUI 构建需要；GUI 仍是 Tauri probe）

### 初始化一个项目

```bash
git clone <this-repo> freely
cd freely
export PATH="$PWD/bin:$PATH"

freely init \
  --project "$PWD" \
  --intent "$PWD/docs/PROJECT_INTENT.md" \
  --constitution "$PWD/docs/CONSTITUTION.md" \
  --auto

freely doctor --project "$PWD"
```

`init` 会自动探测本机 AI CLI、写入 `.freely/config.toml`，并在缺少 ACP binary 时提示下载。`doctor` 用来确认工具链、凭据与运行时状态。

### 启动自主循环

```bash
freely start --project "$PWD" --task-mode auto
```

查看状态：

```bash
freely live-status  --project "$PWD"
freely fleet-status --project "$PWD"   # 本项目所有工位/分支
freely daemon logs  --project "$PWD" --follow
```

停止：

```bash
freely stop --project "$PWD"
```

### 给项目第一个任务

```bash
freely feedback \
  --title "feat: 增加导出 CSV 的能力" \
  --kind feature \
  --body "## 背景
当前只能查看列表，无法导出。

## 期望
在列表页增加导出按钮，导出当前筛选结果为 CSV。

## 验收
- 导出内容与当前筛选一致
- 空结果不产生空文件"
```

之后 Manager 会把它纳入 scan、建工位、走 B1→B2→dev→test→PR。

## 常用命令

| 我想做什么 | 命令 |
| --- | --- |
| 初始化 / 体检 | `freely init ...`、`freely doctor` |
| 启动 / 停止自主循环 | `freely start`、`freely stop` |
| 看当前状态 | `freely live-status`、`freely fleet-status` |
| 提需求 / 报 bug | `freely feedback --title ... --kind fix\|feature --body ...` |
| 开一个工位 | `freely wt-create --raw-key <key> --source platform --kind feature --slug <slug>` |
| 提 PR | `freely pr-create-guarded` |
| 独立 review | `freely pr-review-guarded <branch>` |
| 门禁合并 | `freely pr-merge-guarded develop <branch>` |
| 收口 | `freely wt-close --raw-key <key>` |
| 看 harness 能力/缓存 | `freely harness-status --project .` |

> 不要用裸 `git` / `gh` 替代这些封装命令。它们各自封装了门禁、双平台同步、工位清理和审计步骤；绕过会直接触发 hook 拦截。

## 核心概念

| 概念 | 一句话 |
| --- | --- |
| **raw issue** | 平台上的原始问题/需求；先收敛，不直接写代码 |
| **candidate** | B1 预研后的候选方案；决定是否进入正式 issue |
| **I-* issue** | B2 物化后的正式工作单元；绑定 PRD、pre-tests、tasks |
| **worktree** | 每个 issue 的隔离工作区；dev 工位写代码，test 工位做可丢弃验证 |
| **A2A task** | Manager/Worker/Reviewer 之间的任务状态机 |
| **gate** | IBM 文档门禁、测试门禁、PR review、merge gate、closeout |
| **harness** | 实际执行 AI 会话的 CLI；Freely 通过 ACP 适配，可替换 |
| **scan** | 从文档、issue、milestone、运行时推导“下一步该做什么” |

## 设计原则

1. **文档是规格与生命周期的真相**：平台只是界面；执行中的“谁在做”以 A2A 为准，环境以 git/worktree 为准，scan 只做对账与派生。
2. **TDD 是验收**：先 RED 再实现，GREEN 在 test 工位跑；测试证据不是可选项。
3. **一个项目一个 supervisor**：Manager 常驻，Worker/Reviewer 按需派生；不靠人肉轮询。
4. **状态有唯一真源**：issue、milestone、`phase_state`、A2A task、测试证据各司其职。
5. **工位隔离**：每个 issue 独立 worktree；`develop`/`main` 只接受门禁合并。
6. **证据优先**：测试要有命令与输出，review 要有 verdict，合并要有 gate 记录。
7. **基座可替换**：AI harness 是执行层，不是 Freely 的宿主；优先换 harness，不把 core 绑死在某一家 CLI。
8. **禁止绕过**：`--no-verify`、`--force`、`--admin` 一律拦截；门禁误判就修门禁，不绕门禁。

## 可观测性

```bash
freely live-status      # 当前项目运行态
freely fleet-status     # 本项目所有工位/分支
freely baseline-status  # 基线与漂移
freely harness-status   # 每个角色用什么 harness、fork 是 native/degraded、最近 cache 情况
```

`harness-status` 是只读探针：它不启动会话，只回答“当前配置能不能干这件事”。例如 `--require fork` 会在 Reviewer 的 CLI 只能 `degraded` fork（尝试后回退 session/new）时直接失败，避免运行时才发现降级。

## 仓库结构

```
bin/                         CLI 封装命令
docs/
  CONSTITUTION.md            硬约束
  LAWS.md                    操作规则
  PROJECT_INTENT.md          产品方向
  system/workspace/          Freely 能力真源：runtime、skills、agents、hooks、A2A
  B1-docs/                   预研、candidate、对比研究
  B2-docs/                   正式 issue、PRD、pre-tests、code-review
src/                         TUI/GUI
docs/assets/                 README 交付闭环 + 五平面图
```

### Dogfooding 与目录边界

- 本仓库正在用同一套 B1/B2、SDD/TDD 开发 Freely 自己；这是 dogfooding，不是架构组件。
- `docs/B1-docs/`、`docs/B2-docs/`、`docs/milestones.md` 是本仓库的**自开发过程产物**，不属于 runtime。
- `docs/system/`、`bin/`、`src/` 是 **Freely 产品能力**，会被 runtime/agent/skill/CLI 长期消费。
- README 主图描述的是**产品交付闭环**，不是当前仓库的 issue 列表或工位状态。

## 边界与现状

- Freely 是**活跃开发中的治理型 runtime**，不是“装完就无人值守”的成品；首次接入需要配置 AI CLI、平台凭据与项目宪法。
- 它**不替代** Claude Code / Codex / OpenCode 等 harness；它负责编排、隔离、门禁与审计。
- 当前主路径是 ACP harness；DSH **不做 harness adapter**——那会把 DSH 的 Router/Thread/Mandate 阉割成执行器。若要进 DSH 生态，方向是 `@freely/dsh-freely` 治理插件（单独立项评估）。
- 自主模式默认开启，但人类仍可通过 `chat`、`stop`、PR review、merge gate 介入。
- 多项目通过全局 `~/.freely/projects.tsv` 登记，每个项目有独立 runtime 与工位；`fleet-status` 目前是“本项目工位视图”，不是跨项目统一调度台。
- GUI 目前是 Tauri probe（`src-tauri/`），不是完整产品面；CLI 是主入口。

## 深入阅读

- [项目意图](docs/PROJECT_INTENT.md)：为什么做、产品边界
- [宪法](docs/CONSTITUTION.md)：不可协商的硬约束
- [法律](docs/LAWS.md)：分支、工位、门禁、状态机规则
- [Three-Loop 生命周期](docs/system/workspace/three-loop-capability-lifecycle.md)：唯一的生命周期真源
- [命令参考](docs/system/workspace/commands.md)：封装命令与绕过禁令
- [Agent 角色](docs/system/workspace/agents/)：Manager / Worker / Reviewer
- [A2A 协议](docs/system/workspace/a2a/)：角色间任务与状态
- [B1 预研索引](docs/B1-docs/raw-20261101T031502Z/research-index.md)：研究地图、关键事实、未解问题
- [逐项判定总表](docs/B1-docs/raw-20261101T031502Z/synthesis.md)：问题/方案/谁更优/为什么/代价
- [Freely 交付闭环概念模型](docs/B1-docs/raw-20261101T031502Z/delivery-model.md)：B1/B2、SDD/TDD、三角色、3 loop + 2 门禁
- [Super-agent 对比研究](docs/B1-docs/raw-20261101T031502Z/research.md)：理念/架构/实现/场景对比
- [文章映射与 Reviewer 纠偏](docs/B1-docs/raw-20261101T031502Z/super-agent-article.md)：Router/Worker/Reviewer 不是一一对应
- [失效模式对比](docs/B1-docs/raw-20261101T031502Z/failure-modes.md)：漏单、重复、越权、交接丢失、缓存误判等
- [文档目录审计](docs/B1-docs/raw-20261101T031502Z/docs-directory-audit.md)：预研归位、遗留目录与规范

## 参与开发

Freely 用 Freely 开发自己（dogfooding）：

```bash
freely feedback --title "..." --kind fix|feature --body "..."
freely wt-create --raw-key <key> --source platform --kind feature --slug <slug>
# 在工位内按 skill 走 B1 → B2 → RED → dev → test
freely pr-create-guarded
freely pr-review-guarded <branch>
freely pr-merge-guarded develop <branch>
freely wt-close --raw-key <key>
```

不要直接在 `develop` 上提交，也不要跳过测试与 review。流程细节见 [AGENTS.md](AGENTS.md) 与 `docs/system/workspace/skills/freely-workflow-guarded-execution/SKILL.md`。
