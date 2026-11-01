# Freely

**一个自主的项目循环运行器：AI 是项目所有者，人负责定意图和验收。**

Freely 不是“帮你写一段代码”的聊天工具，也不是固定 TODO 列表的执行器。它把 `issue → 调研 → 设计 → 实现 → 测试 → PR → 合并 → 收口` 做成一个持续运行的闭环：AI 自己发现下一步、自己在隔离工位里干活、自己跑门禁，人类只在需要决策或验收时出现。

[![架构图](docs/assets/freely-architecture.svg)](docs/assets/freely-architecture.html)

> 交互版：[docs/assets/freely-architecture.html](docs/assets/freely-architecture.html)（支持主题切换、搜索、聚焦与导出）

## 为什么需要它

单个 coding agent 已经能完成“一个任务”；真正难的是让它**持续对一个项目负责**：

- **注意力瓶颈**：人不可能每天盯着 agent 决定下一步做什么。
- **上下文漂移**：长任务里，目标、约束、历史决策很容易丢。
- **治理缺口**：能写代码不等于能合并代码；没有门禁的自治就是事故。
- **连续性**：AI 工具会崩溃、卡住、被切走；项目不能因此停摆。

Freely 的答案是：把“项目意图、宪法、门禁、工位、评审、审计”做成运行时的一部分，让 AI 在约束内自主循环，而不是靠一段超长提示词祈祷它别跑偏。

## 它长什么样

| 层 | 组成 | 作用 |
| --- | --- | --- |
| 宿主壳 | CLI、TUI、GUI | 同一套 core 的不同入口；命令、状态、人工插话 |
| Freely core | runtime、three-loop、scan、A2A、门禁 | 调度、路由、状态、审计；不把业务语义绑在某个 shell 上 |
| 角色 | Manager、Worker、Reviewer | 常驻调度者、隔离执行者、独立审查者 |
| 执行基座 | worktree + AI harness（ACP） | 每个 issue 独立工位；Claude Code / Codex / OpenCode / Cline 等可切换 |
| 外部界面 | GitHub / Gitee | issue、PR、review、CI；人类真实工作发生的地方 |

## 它是怎么运转的

```
issue / chat / 治理漂移
        │
        ▼
   auto-loop（Manager）
   巡检 → 判断 → 建 raw issue → 建工位 → 派工 → 收口
        │
        ├── doc-loop（Worker）
        │     B1 预研 → candidate → B2 PRD / pre-tests / tasks
        │
        └── dev-loop（Worker）
              RED → 实现 → test-GREEN → 独立 review → PR
                                      │
                                      ▼
                          pr-create / pr-review / pr-merge / wt-close
```

三个 loop 的分工：

- **auto-loop**：唯一调度中枢。决定“现在做什么、派给谁、什么时候收口”。
- **doc-loop**：先把问题收敛成可执行的 issue，再写清验收与测试方案。
- **dev-loop**：在独立 worktree 里按 pre-tests 实现，在 `test-pre-merge` 工位验证，最后由 Reviewer 审查。

验证不是“agent 说完成了”，而是**门禁 + 证据**：B1/B2 文档、RED/GREEN 记录、独立 review verdict、PR gate、merge gate、closeout。

## 快速开始

### 依赖

- macOS / Linux，`bash`、`git`
- Python 3.11+（runtime 与 `freely-db`）
- 一个支持 ACP 的 AI CLI：Claude Code、Codex、OpenCode 或 Cline
- Node.js 20+（仅 TUI/GUI 构建需要）

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
freely fleet-status --project "$PWD"   # 多项目/多工位
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

1. **一个项目一个 supervisor**：Manager 常驻，Worker/Reviewer 按需派生；不靠人肉轮询。
2. **状态有唯一真源**：issue、milestone、`phase_state`、A2A task、测试证据各司其职。
3. **工位隔离**：每个 issue 独立 worktree；`develop`/`main` 只接受门禁合并。
4. **证据优先**：测试要有命令与输出，review 要有 verdict，合并要有 gate 记录。
5. **基座可替换**：AI harness 是执行层，不是 Freely 的宿主；优先换 harness，不把 core 绑死在某一家 CLI。
6. **禁止绕过**：`--no-verify`、`--force`、`--admin` 一律拦截；门禁误判就修门禁，不绕门禁。

## 可观测性

```bash
freely live-status      # 当前项目运行态
freely fleet-status     # 所有项目/工位
freely baseline-status  # 基线与漂移
freely harness-status   # 每个角色用什么 harness、支持 fork/resume/usage 吗、最近 cache 情况
```

`harness-status` 是只读探针：它不启动会话，只回答“当前配置能不能干这件事”。例如 `--require fork` 会在 Reviewer 使用不支持 fork 的 CLI 时直接失败，避免运行时才发现降级。

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
docs/assets/                 README 架构图
```

## 边界与现状

- Freely 是**活跃开发中的治理型 runtime**，不是“装完就无人值守”的成品；首次接入需要配置 AI CLI、平台凭据与项目宪法。
- 它**不替代** Claude Code / Codex / OpenCode 等 harness；它负责编排、隔离、门禁与审计。
- 当前主路径是 ACP harness；DSH 等宿主需要 adapter，不会假装“加个配置就能换”。
- 自主模式默认开启，但人类仍可通过 `chat`、`stop`、PR review、merge gate 介入。
- 多项目通过 fleet 管理，每个项目有独立 runtime 与工位。

## 深入阅读

- [项目意图](docs/PROJECT_INTENT.md)：为什么做、产品边界
- [宪法](docs/CONSTITUTION.md)：不可协商的硬约束
- [法律](docs/LAWS.md)：分支、工位、门禁、状态机规则
- [Three-Loop 生命周期](docs/system/workspace/three-loop-capability-lifecycle.md)：唯一的生命周期真源
- [命令参考](docs/system/workspace/commands.md)：封装命令与绕过禁令
- [Agent 角色](docs/system/workspace/agents/)：Manager / Worker / Reviewer
- [A2A 协议](docs/system/workspace/a2a/)：角色间任务与状态
- [Super-agent 对比研究](docs/B1-docs/raw-20261101T031502Z/brainstorms.md)：与 DeepSeek Super-agent 的实现级对比与任务拆分

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
