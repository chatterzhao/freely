---
b1_id: B1-20261101T031502Z
phase_state: completed
source_raw: raw-20261101T031502Z
source_url: https://github.com/chatterzhao/freely/issues/4110
produced_candidate: C-20261101T031502Z-A, C-20261101T031502Z-B, C-20261101T031502Z-C, C-20261101T031502Z-D
created_at: 2026-11-01
---

# B1_IBM: DeepSeek Super-agent 架构与 Freely agent 协作模型对比研究

> **补充研究入口（2026-11-01）**：本文件是最初的 B1 收敛记录；后续对文章映射、Reviewer 阶段评审、SDD/TDD 交付闭环、DSH adapter 取舍的补充研究见同目录 [`research-index.md`](research-index.md)。若本文件与补充研究冲突，以 `research-index.md` 及其子文档为准。

## Input

- raw issue：`raw-20261101T031502Z`（GitHub #4110 / Gitee IKS0MD）。
- 研究对象一：DeepSeek Harness 团队 2026-10-31 发布的设计文章 *Exploring Super-agent Design: Towards a More Autonomous Agent System*（下称“文章”）。
- 研究对象二：配套研究原型 [`deepseek-ai/dsh-superagent-prototype`](https://github.com/deepseek-ai/dsh-superagent-prototype)（MIT，TypeScript）。本地快照为 `main` 分支，克隆于 2026-11-01。
- 研究范围：
  - 文章要点：原文未直接获取，通过[智东西报道](https://www.zhidx.com/p/606311.html)与[博客园拆解](https://www.cnblogs.com/itech/p/23508901)交叉核对；两篇均按原文结构复述，本文只在两者一致时作为“文章主张”引用。
  - 原型 `docs/000-philosophy.md` 至 `docs/008-cookbook.md` 九篇设计文档（约 2,091 行）。
  - 原型 `prompts/` 15 个提示词、`skills/` 2 个技能文件。
  - 原型 `src/core`、`src/executor`、`src/app`、`src/sources` 的关键实现与 `package.json`、`cordis.patch.yml`。
- Freely 侧事实来源：`PROJECT_INTENT.md`、`CONSTITUTION.md`、`LAWS.md`、`docs/system/workspace/three-loop-capability-lifecycle.md`、`docs/system/workspace/session-lifecycle-protocol.md`、`docs/system/workspace/a2a/*`、`docs/system/workspace/agents/*`、`docs/system/workspace/scan-lifecycle-design.md` 与当前 runtime 代码。

### 证据分级

本文把事实分成三种，比较时不混用：

| 级别 | 含义 | 用法 |
| --- | --- | --- |
| 文章主张 | 设计文章提出的机制、目标或实验数字 | 只能说明“作者认为应该这样”，不等于原型已实现 |
| 原型实现 | 快照中存在的代码、文档或提示词 | 说明“这套原型实际这样做” |
| Freely 现状 | 当前仓库文档与 runtime 行为 | 说明“Freely 实际这样做” |

原型 README 自己声明：它是研究代码、经过出版适配，**与内部版本和文章描述不完全一致，文章里有些设计是未来方向、原型未实现**。因此下文每个 Super-agent 机制都会标注它属于“文章主张”还是“原型实现”。

### 方法与局限

- 原型只做静态阅读，没有启动它跑真实 GitHub 仓库；因此“原型实现”指代码/文档中存在，不指行为已实测。
- 文章数字来自合成负载与简化环境，本文引用它们只为说明设计动机，不作为性能结论。
- Freely 侧同样以文档与代码为准，没有做跨项目运行时采样；涉及“现状”的判断都指向具体文件，便于后续复核。
- 本文是架构与协作语义比较，不做逐项 benchmark。

## Problem

要回答的不是“谁更强”，而是六个具体问题：

1. Super-agent 的五个模块各自解决什么协作问题，原型真正落地了哪几个？
2. Freely 现在用什么机制解决同一批问题，哪些是等价物、哪些是空缺？
3. 两边在 **agent 协作** 上的结构性差异是什么，各自付出什么代价？
4. 在路由、交接、缓存命中这些具体实现上，谁做得更扎实，差在哪里？
5. Harness 抽象与插件边界：Freely 应把 agent harness 当可切换基座，还是把自己做成 DSH 插件？两者能否并存？
6. 对 Freely 而言，哪些可以借用、哪些必须改造、哪些不应照搬？

非目标：不复现文章实验，不评价模型能力，不把“文章愿景”当成“原型现状”，也不把 Freely 的治理流程简单判为优于或劣于对方的运行时机制。

## 1. Super-agent 的文章主张：五个模块

| 模块 | 机制 | 要解决的问题 |
| --- | --- | --- |
| 双层架构 | 常驻 Router 层承接人类交互与全局协调，只分派不干活；上下文隔离的 Worker 层并行执行，只向 Router 汇报 | 连续性与吞吐的矛盾：单 Session 连续但串行，多 Session 并发但上下文割裂 |
| 事件驱动 | 环境事件成为 `Trigger`；程序 Fast Path 先过滤，模型 Slow Path 再研判；订阅与直通把后续事件直接送 Worker | 从“等人下指令”变成“响应环境”；同时避免每个事件都调用模型 |
| 异步多信道交互 | 工具调用改为异步 `start()`/`stop()`，前台不阻塞；不同信道用不同话术（IM 低打扰、GitHub 高密度） | 长任务阻塞对话；多个 Worker 各自对外说话造成噪音 |
| 存算分离 | 计算、持久状态、执行环境三者解耦；云端保持在线，执行环境留在用户机器或按需沙箱 | 设备休眠/离线即停；单机绑定 |
| 外部 Watchdog | 主系统之外的独立 Watchdog Session，定时驱动，既查基础设施也判断 Worker 是否有实质进展 | 进程活着不等于任务在推进；需要外部控制回路 |

文章给出的实验数字（合成负载、简化环境，作者自称仅初步参考）：Super-agent 任务完成 p50 12.4 分钟、p95 15.7 分钟；去掉订阅直通后 Router 决定数增加约 30%，读缓存 token 从 2,323 万增至 3,177 万；Router 批处理把单决定分摊推理时间从 6.4 秒降到 1.6 秒。

## 2. 原型实际落地到哪一步

| 文章模块 | 原型状态 | 证据与边界 |
| --- | --- | --- |
| 双层架构 | 已实现 | `docs/007-architecture.md` 的 `Sessions`/`DshExecutor`：主 Session 用 `dsh-superagent-router`，每个 Ticket 一个 `worker-<ticket id>` Session 与独立目录 |
| 事件驱动 | 已实现 | `Source`/`Trigger`/`Thread`/`Eval` 领域模型；`002-authorization.md` 的 gate（代码）与 assessment（模型）两层；准入表与 `off`/`observe`/`auto` 三档 |
| 订阅与直通 | 已实现 | `Subscription` 多对多；订阅消息绕过 gate、不授予新权限；`handback` 与 `followupOwners` 控制归属 |
| Inline & Spill / 链式召回 | 已实现 | `orchestrator_read` 资源分页；评估窗口首 5 条 + 前后各 5 条；文本默认 4,000 字符、列表默认 20 条；对象 ID 内联形成引用图 |
| 异步 ReAct（start/stop） | 未作为主路径 | 文章说该机制“已在 Harness 实现但尚未默认开启”；原型改用 5 秒后前台 shell 转后台 job，靠 job/subagent 完成消息唤醒 |
| 投机执行 | 未发现实现 | 原型 `docs/`、`prompts/`、`src/` 中无 speculative execution 相关代码或开关 |
| 存算分离 | 未实现 | 原型是单机 bundle：`stateDir` 放 SQLite、锁、命令 shim、worker git 配置与 Ticket 目录；执行环境就是本机 |
| 外部 Watchdog | 未发现实现 | 原型无 watchdog 组件；只有 host 重启恢复、health entries 与 Assignment 恢复提示 |
| 通用多仓 | 未实现 | README 与 `006-deployment.md` 明确只服务一个 GitHub 仓库，且不支持 GitHub Enterprise Server |
| 独立 Reviewer 角色 | 未实现 | 原型没有 reviewer 角色；自动审查机器人被当作“可错的外部输入”，由 Worker 自行评估，最多三轮 |
| 文档/设计阶段（B1/B2 类） | 未实现 | Ticket 直接进入 Worker 调查与实现；没有独立的设计产物与设计评审环 |
| 集成形态 | 深度绑定 DSH | 以 Cordis bundle 发布（`dsh.bundle.patch`），peer 依赖 `@deepseek-ai/dsh-*`，`engines.dsh` 钉版本；**没有 ACP 服务端** |
| 会话与缓存 | 每 Ticket 独立 Session | `promptVersion` 绑定、Policy 置尾；原型没有 cache hit/miss 指标；Worker 不继承 Router 上下文 |

结论：**文章是架构论文，原型是它的一个可运行子集。** 把五个模块都当成“DeepSeek 已经这么做”会误判；反过来，把原型没做当成“文章错了”也会误判。比较时必须区分“设计意图”与“落地证据”。

还有一个容易漏掉的事实：**原型的工程形态是“DSH 宿主里的一个 bundle”，不是可被别家 runtime 直接调用的服务。** 这决定了后面“Freely 把 DSH 当基座”不能只靠配置，必须走 adapter；反过来“Freely 做成 DSH 插件”也不是免费换壳。

## 3. Freely 的对应结构

| 层 | Freely 机制 | 证据 |
| --- | --- | --- |
| 角色 | Manager（项目主人，常驻）、Worker（独立工位执行）、Reviewer（独立审查） | `agents/manager-agent.md`、`worker-agent.md`、`reviewer-agent.md` |
| 会话 | Agent 全生命周期同一 session；重启 resume；委派时 fork 父 session | `session-lifecycle-protocol.md` |
| 协调协议 | A2A Task（`submitted`/`working`/`input-required`/`completed`/`failed`/`canceled`）+ SSE 状态推送 | `a2a/protocol-design.md`、`a2a/exit-kind-mapping.md` |
| 任务发现 | scan 按文档与 `phase_state` 推导生命周期阶段与 `next_action` | `scan-lifecycle-design.md` |
| 生命周期 | B1 → B2 → RED → dev → test → PR → merge → closeout；doc-loop / dev-loop / auto-loop | `three-loop-capability-lifecycle.md` |
| 授权 | 角色职责 + 阶段门禁 + 分支保护 + worktree 所有权 + 人工 stop | `CONSTITUTION.md`、`LAWS.md`、`three-loop` gate 序列 |
| 隔离 | 每个 raw issue 一个 dev worktree + 一个 test-pre-merge 工位；Manager 在 develop 只读 | `AGENTS.md`、`wt-create` 实现 |
| 监督 | supervisor heartbeat、`watchdog_sse.py`、continuation、Loop Guard L0–L3、restart storm 信号 | `three-loop` 运行时监督面 |
| 多项目 | fleet 级 `live-status`/`fleet-status`，每项目独立 runtime | `PROJECT_INTENT.md`、runtime CLI |
| 人机入口 | `freely chat`、intake、discuss、scan 的 `needs_human` | runtime 命令与 intake 表 |

但“对应”不等于“同名”。例如 Super-agent 的 Router 只路由，Freely 的 Manager 还负责巡逻、派工、纠偏与收口；Super-agent 的 Ticket 是一个聚合对象，Freely 的“工单”由 issue 文档 + 工位 + A2A task 三者共同表达。为避免逐项漏看，全部概念（含 Disposition、Input、Strength、Assignment、Effects、Outbox、Health 等）的逐条映射见 [concept-map.md](concept-map.md)；该文另列了“同名不同义”“Freely 有而 Super-agent 没有”“Super-agent 有而 Freely 没有”三张表。

## 4. 逐维比较

### 协作拓扑对比图

![Super-agent 与 Freely 协作拓扑对比](super-agent-vs-freely-collaboration.svg)

[打开交互式版本](super-agent-vs-freely-collaboration.html)（archify 生成，支持主题切换、搜索、聚焦和导出）。图中只画主路径；`report`、`SSE`、`verdict` 等回流见下方文字说明。

### 4.1 设计公理与默认姿态

| 维度 | Super-agent | Freely |
| --- | --- | --- |
| 第一目标 | 把人的注意力成本降到最低：不必要不说话、不主动干活 | 让 AI 成为项目所有者，持续自主循环推进 |
| 默认动作 | 默认不做（`observe` 只记录“would accept”），显式请求才做 | 默认推进（auto-loop 主动发现问题并派工），只有明确停止或无事可做才停 |
| 适用边界 | 一个 GitHub 仓库 + 一个团队，重“团队协作中的打扰控制” | 多项目治理，重“从问题到合并的闭环与留痕” |
| 成功判据 | 人的打断次数、结果可用性、响应时延 | issue 闭环率、门禁通过率、可恢复性、治理一致性 |

这不是同一类系统的替代关系：Super-agent 更像“团队里一个懂分寸的同事”，Freely 更像“一个按治理规则运转的项目所有者”。重叠区在 agent 协作调度，不在产品目标。

### 4.2 角色拓扑与通信图

Super-agent（原型）：

```
human (IM / GitHub)
   │  Trigger
   ▼
Router (1 个常驻 Session，只分派、不实现)
   │ assignment（Ticket + Mandate）
   ▼
Worker_n (每 Ticket 一个 Session + 目录)
   │ report / attention
   └──────────────► Router ──► human（统一对外说话）

Thread 事件 ──订阅直通（绕过 Router、绕过 gate）──► 所有订阅该 Thread 的 Worker
```

Freely：

```
human
   │ chat / intake / issue
   ▼
Manager (常驻 Session，develop 工位)
   │ A2A task submitted              ┌── Reviewer (fork Manager session)
   ▼                                 │      ▲
Worker_N (独立 worktree) ── needs-review ──┘      │ verdict (pass/fail)
   │ B1/B2/RED/dev/test/PR           │             │
   └──────── a2a-exit ───────────────┴── watchdog_sse 路由
```

三个直接差异：

1. **Super-agent 没有内建 Reviewer**；Freely 有独立 Reviewer，且 Reviewer 的 verdict 同时广播给 Manager 与 Worker。
2. **Super-agent 的 Thread 事件可以绕过 Router 直达 Worker**；Freely 的 Worker 没有线程订阅，外部后续消息要经 Manager/A2A 或重新进入 intake。
3. **Super-agent 的 Worker 之间没有点对点通信**，靠共享 Thread 的广播“看见”彼此；Freely 的 Worker 之间也没有点对点通信，靠 worktree 隔离与合并门禁“避免”彼此。

### 4.3 委派与交接协议

| 环节 | Super-agent | Freely |
| --- | --- | --- |
| 工作单元 | Ticket（授权 + 执行 + 报告） | raw issue → I-* issue → worktree/branch |
| 创建者 | Eval 接受后由 Engine 创建 | Manager 经 `wt-create` 创建 |
| 派工 | `Assignment` 绑定 Ticket 与 Executor 实例 | `a2a-exit --state submitted --role worker` 创建 A2A Task |
| 启动 | launch effect + prepare command + Session | Runtime 发现 submitted task → 启动 Worker ACP session |
| 指导 | Router 只能经 assignment/note，不得下实现指令 | Manager 可 `a2a_task.py prompt` 实时纠偏 |
| 完成报告 | `orchestrator_report`（progress/waiting/ready/blocked/failed/dropped） | `a2a-exit --state completed` + summary + evidence |
| 需人决策 | 结构化 `human_action` + Attention | `input-required` + reason 枚举（needs-review/needs-manager 等） |
| 越界请求 | Worker `orchestrator_trigger_handback`，交回 Router 重新评估 | Worker 上报 `input-required`，由 Manager 判断重派或新开 |
| 后续消息 | 订阅 Thread 直通；人消息可复活已结束 Ticket | 无订阅；后续评论重新走 intake/scan，或 Manager 主动 prompt |
| 取消/停止 | 人 stop 撤回 Mandate；面板 stop 是命令 | 人工 stop / close / `wt-close`；没有 per-ticket 撤回凭证 |

关键观察：**Super-agent 把“谁拥有这条后续消息”做成了运行时事实**（`followupOwners`、`handback`、`Subscription`），Freely 把“谁拥有这个工作项”做成了流程事实（worktree 归属、issue 阶段、Manager 调度）。前者适合长对话线程，后者适合多阶段交付。

### 4.4 授权模型

| 维度 | Super-agent | Freely |
| --- | --- | --- |
| 授权载体 | `Mandate` 不可变凭证：Policy 版本、scope、strength、matched rules、发送者身份、接收方式 | 角色 + 阶段 + 门禁 + 分支保护 + 人工指令 |
| 谁能发起 | 白名单/准入表/机器人列表，按 Source 各自的身份 | 人（chat/issue）、Manager（scan/feedback）、受限的自主发现 |
| 默认强度 | 只有“名单内 + 明确点名”是 explicit；其余最多 inferred | 发现的 issue 进入完整 B1/B2；没有 inferred 概念 |
| 版本化 | Policy 版本变化会重排 Eval、通知受影响 Ticket，但不立即吊销 Mandate | 规则变化体现为 skill/宪法/门禁更新；在途 worktree 不自动失效 |
| 复活 | 已结束 Ticket 凭原 Mandate 复活，复活前按当前 Policy 重校验 | 已关闭 issue 需要新开或重新进入流程 |
| 越权防守 | 运行时拒绝：gate、Mandate、tool 参数检查 | 流程拒绝：门禁、review、分支保护、禁止绕过 hook |
| 审计 | Decision + reason + disposition + Mandate 快照 | 文档、commit、PR、review verdict、审计日志 |

Super-agent 的授权是**数据**，可以在运行时回答“这件事凭什么被批准、批到哪、按哪版规则”。Freely 的授权是**过程**，可以在事后回答“这件事走了哪些门、谁 review 的、合进了哪个分支”。前者更细粒度、更可执行；后者更组织化、更可审计。

### 4.5 事件、状态与幂等

| 维度 | Super-agent | Freely |
| --- | --- | --- |
| 事件 | `Trigger` 不可变，带 Source 元数据；同一 Trigger 接受两次只产生一个 Ticket | chat/intake/issue/scan 事件；去重靠 scan 与 A2A 查询 |
| 状态机 | Ticket stage 由 Report/Input 等结构化事实推导；代码是唯一写者 | `phase_state` + scan stage + milestone；文档与 DB 共同承载 |
| 幂等 | accept 以 trigger ID 幂等；effect 队列按 kind/key 合并；disposition 记录去向 | `a2a_task list --raw-key` 防重复委派；`wt-create` 幂等性由脚本保证 |
| 恢复 | SQLite 单库 + effect 队列 + 未读 Input 重投 | SQLite `a2a_tasks` + session-state + watchdog + continuation |
| 漂移风险 | 低：状态由代码推导 | 中：文档声明与运行时可能不一致，靠 scan/gate 对账 |

Super-agent 的状态纪律更强（“每个状态一个写者”），Freely 的状态可读性更强（人可以直接看文档），但需要持续对账。这是典型的“机器可判定”与“人可审计”的取舍。

### 4.6 上下文组织

| 维度 | Super-agent | Freely |
| --- | --- | --- |
| 长期记忆 | SQLite 记录 Trigger/Thread/Ticket/Decision，按 ID 链式召回 | 文档（B1/B2/progress/review）+ issue + milestone |
| 工作上下文 | Inline & Spill：近期信息内联，长文截断留续读入口 | skill + 仓库文档 + scan JSON 注入 Manager prompt + worker 自行读仓库 |
| 角色上下文 | Router 提示词分层拼装（shared/role/team/dispatch/policy）；工具面 14 个 | Manager/Worker/Reviewer 三份 agent 定义 + skills；工具面由 AI CLI 提供 |
| 上下文预算 | 有明确上限（窗口、字符数、列表条数、8 个相关 Ticket） | 有 context rotation 阈值与会话 handoff，但没有 per-object 预算协议 |
| 跨会话继承 | Worker 不继承 Router 上下文，只拿 assignment | Worker/Reviewer fork Manager session，继承治理上下文（缓存命中） |

两者方向相反：Super-agent 用**裁剪与按需召回**控制上下文；Freely 用**fork 继承与文档外置**控制上下文。前者适合事件流，后者适合长流程治理。

### 4.7 并发与冲突

| 维度 | Super-agent | Freely |
| --- | --- | --- |
| 并发单位 | Worker slot（含 prepare）；人类消息可额外占一个 slot | Worker pool；Manager 派工前查空闲 worker |
| 隔离 | 每 Ticket 一个 Session + 目录 | 每 issue 一个 dev worktree + test 工位 |
| 冲突发现 | 共享 Thread 广播；Worker 可自行发现并解决；重复工作主动让位 | 合并/PR 门禁；重复委派检查；worktree 隔离 |
| 冲突解决 | 代码层自行处理；人工 review | rebase/merge + gate + review + 人工 approval |
| 上限 | 单 Router Session + 并发 slot；文章承认切分策略未定 | 多项目 fleet；单项目 worker 容量可配 |

Super-agent 的并发是“事件级并发”，Freely 的并发是“交付级并发”。前者更快发现交集，后者更强隔离与追责。

### 4.8 失败与恢复

| 维度 | Super-agent | Freely |
| --- | --- | --- |
| 进程/会话故障 | host 重启：运行中 Assignment 以 “host restarted” 结束，新 Assignment 带恢复提示，先查目录/git/GitHub 再重复外部动作 | supervisor heartbeat + watchdog + continuation；session resume |
| 任务停滞 | 无内建 watchdog；靠 Report 状态与人工 retry | `watchdog_sse.py`、Loop Guard L0–L3、restart storm 信号 |
| 投递失败 | 2 秒起翻倍到 1 分钟；连续 3 次才升系统问题 | A2A/ACP 启动失败、`input-required`、Manager 重试 |
| 阻塞语义 | `blocked`/`failed` 持有后续自动输入，直到人来消息或 retry | `input-required` + reason；Manager 判断纠偏/重试/新开 |
| 重复外部动作 | 恢复提示明确要求先核对再重做 | 宪法禁止直接改 develop；门禁与 review 降低重复风险，但恢复协议不如前者结构化 |

值得注意：**文章把外部 Watchdog 列为五模块之一，原型没有实现**。Freely 反而在运行时层有较完整的 watch/continuation 体系。这是“文章愿景 vs 原型落地”与“Freely 现状”三者不能简单对齐的典型例子。

### 4.9 人机交互与注意力

| 维度 | Super-agent | Freely |
| --- | --- | --- |
| 人类入口 | IM、GitHub；所有回复回原会话 | chat/discuss、平台 issue、intake |
| 打扰策略 | 默认沉默；只有可验收结果、必须决策、确实做不了才说话；IM 单条 ≤100 词 | Manager 主动汇报阶段结果；scan `needs_human`；CLI 状态面 |
| 提问形态 | 结构化 `human_action`，一次一个具体问题，路由回提问所在会话 | `input-required` + reason 枚举；completion_summary 说明 |
| 监督面板 | 三个问题：现在需要我吗、系统健康吗、这件工作的历史 | live-status / fleet-status / scan / milestones / progress |
| 默认自治度 | `observe` 起步，人工确认后再 `auto` | 默认自主循环，人通过 interruption/stop 介入 |

这是两边最根本的产品差异：Super-agent 把“少打扰”作为第一性约束；Freely 把“自主推进”作为第一性约束。两者的“注意力”优化方向不同——前者优化被打断次数，后者优化人工介入总时长。

### 4.10 可观测性与可审计

| 维度 | Super-agent | Freely |
| --- | --- | --- |
| 运行时视图 | 面板六个 tab；Ticket stage；Decision/reason；health board | CLI status、scan、A2A SSE、runtime 日志、DB |
| 审计链 | Trigger → Eval → Decision → Ticket → Assignment → Report | issue → B1/B2 → commit → PR → review verdict → merge |
| 单一事实源 | SQLite 单库，单写者 | 文档 + SQLite + 平台 issue；多源需对账 |
| 适合谁看 | 值班人快速判断“现在要不要我” | 管理者/审计者看“这件事为什么这么做” |

### 4.11 扩展性与部署边界

| 维度 | Super-agent | Freely |
| --- | --- | --- |
| 扩展点 | Source kind 插件（GitHub/Feishu），Prompt part 覆盖，团队 skills | skills、agent 角色、runtime 命令、ACP 工具适配、worktree 流程 |
| 部署 | 单机 DSH bundle；`stateDir` 本地；一个仓库 | 多项目 runtime；每项目独立工位与配置 |
| 跨实例 | 文章提出 A2A 跨实例，原型未实现 | A2A 已用于同项目 Manager/Worker/Reviewer；fleet 跨项目 |
| 身份 | 每个 Source 各自白名单，不跨源映射 | 项目/工位/角色身份，平台账号由 adapter 管理 |

Super-agent 的扩展是“加一个事件源”；Freely 的扩展是“加一个能力/流程/项目”。前者更轻，后者更重，但覆盖的组织面不同。

### 4.12 实现质量评估：路由、交接、缓存

理念相同不代表实现同质。下面按“可观察的机制”逐项比较，评价只看实现是否把语义做扎实，不看宣传。

| 子问题 | Super-agent 的实现 | Freely 的实现 | 评价 |
| --- | --- | --- | --- |
| 事件准入 | 代码 gate 先判发送者/来源/准入表/机器人，再交给模型 assessment；无关事件不进入模型 | scan + Manager 判断；没有 per-event 的确定性准入层 | DSH 更省、更可判定；Freely 更依赖 Manager 纪律 |
| 路由批处理 | `orchestrator_route` 一次 1–20 条，逐条校验、逐条事务、单条失败不影响其他条 | Manager 逐条 `a2a-exit`；无批量决策工具 | DSH 的批处理是真实实现，不是提示词约定 |
| 路由幂等 | accept 以 trigger ID 幂等；同一次调用内重复决策被识别；note ≤30 词、ack ≤100 词由 schema 限制 | 靠 `a2a_task list --raw-key` 查询防重复；无事件级幂等账本 | DSH 更硬；Freely 的幂等是“查一下”而非“记一笔” |
| 交接状态 | `progress/waiting/ready/blocked/failed/dropped` 六态；`human_action` 单问题；report relay 用稳定 key 去重 | A2A `submitted/working/input-required/completed/failed/canceled`；summary/evidence 为自由文本 | Freely 的状态机适合阶段路由；DSH 的 report/attention 更适合人机交接 |
| 人工问题 | 结构化 Attention，问题路由回提问所在会话，重复问题复用请求 ID | `input-required` + reason 枚举，主要面向 Reviewer/Manager 路由 | 两者目标不同：DSH 面向“人”，Freely 面向“角色” |
| 越界消息 | Worker `handback` 一次，带理由；`followupOwners` 决定谁还拥有消息 | Worker 上报 `input-required`，Manager 判断重派/新开 | DSH 的消息级归属更细；Freely 是任务级归属 |
| follow-up 归属 | 订阅 Thread 的消息直达 Ticket 的 Worker；人消息可复活已结束 Ticket；bot/CI 不复活 | 无平台线程订阅；后续消息回到 intake/scan 或由 Manager 主动 prompt | Freely 缺一个“这条消息归谁”的运行时事实 |
| 缓存复用 | Router 与 Worker 各自 Session；Worker 冷启动，不继承 Router 上下文 | Worker/Reviewer fork Manager session，继承治理上下文；文档声称首轮约 80% 命中，但 provider usage 未上报，无法独立验证 | Freely 跨角色复用更强；DSH 隔离更干净 |
| 缓存度量 | 原型无 cache hit/miss 日志或聚合 | `run-acp-prompt.py` 记录 `[CACHE]`；但 input 常由 `prompt_bytes // 4` 估算，hit/miss 常为 0 | Freely 有观测入口；真实命中率仍依赖 provider usage |
| Prompt 稳定性 | 固定段序，Policy 放最后；覆盖记录 base 版本；每次请求绑定 revision | 角色定义 + 运行时状态拼接；scan/fleet/checkpoint 追加；无显式前缀契约 | DSH 的 prefix 纪律更适合 prompt cache |
| 故障恢复 | effect 队列 + 恢复提示 + 未读 Input 重投 | supervisor/watchdog + continuation + session resume | 两者都强，语义不同 |
| 工具面约束 | Router/Worker preset 明确工具清单；Router 禁 sleep/长等待 | AI CLI 自带工具面；靠 skill/提示词约束 | DSH 的“工具面即契约”更硬 |

实现质量结论：

- **DSH 强在“把协作语义写进 schema 和状态机”**：gate、route batch、report/attention、handback、幂等 key 都有代码落点。它不靠提示词“希望模型这么做”。
- **Freely 强在“把交付语义写进生命周期”**：阶段、门禁、独立 Reviewer、多项目 fleet 都有真实产物和检查点；cache 观测入口比 DSH 原型完整，但目前多为估算，不能当真实命中率。
- **Freely 最弱的三处**：事件级准入/幂等、结构化交接载荷、prompt 前缀契约。这三处恰好是 DSH 实现最扎实的地方。
- **DSH 最弱的三处**：单仓/单机、Worker 冷启动与无 cache 度量、Cordis 插件锁定。Freely 不能为了抄路由而把这些代价一起搬进来。

### 4.13 Harness 抽象、ACP/A2A 与插件边界

这是两边最容易被误读的一层。先把协议分开：

| 协议/接口 | 连接谁 | 现状 |
| --- | --- | --- |
| ACP（Agent Client Protocol） | Freely runtime ↔ 外部 AI CLI（Claude/Codex/OpenCode/Cline） | Freely 已用；session/new、prompt、resume、fork、stopReason、usage |
| A2A | Freely Manager ↔ Worker ↔ Reviewer | Freely 已用；Task 状态 + SSE |
| MCP | Agent ↔ 工具/资源 | 两者都可接；不是编排协议 |
| DSH Cordis plugin | DSH host ↔ 插件/bundle | DSH 原型的唯一扩展面；没有 ACP 入口 |
| Freely CLI/skill | Freely runtime ↔ 角色/工位 | Freely 的流程契约面 |

关键事实：**DSH 原型没有 ACP 服务端**，它的集成面是进程内 Cordis 插件（`dsh.bundle.patch` + `@deepseek-ai/*` peer 依赖）。因此“把 DSH 当 Freely 的一个可切换 harness”不能只加一个配置项，必须写一个 DSH adapter（Cordis/SDK 桥或子进程桥）；反过来，“把 Freely 做成 DSH 插件”也不是换一个 adapter，而是把 Freely 的状态机搬进 DSH。

Harness 能力矩阵（Freely 选基座时必须逐项探测，不能假设）：

| 能力 | ACP CLI | DSH host | Freely 是否需要 |
| --- | --- | --- | --- |
| session new / resume | 有，工具差异大 | 有（SDK） | 必需 |
| session fork | Claude/OpenCode 有；Codex/Cline 降级为 new | 有（SDK 层） | 可选，缺失时降级 |
| prompt / stream / stopReason | 有 | 有 | 必需 |
| interrupt / stop | 有 | 有 | 必需 |
| 工具白名单 / 权限模式 | 各 CLI 不同 | preset 明确 | 必需 |
| skills / prompt 注入 | 各 CLI 不同 | 插件 + prompt | 必需 |
| usage / cache 指标 | 部分有 | 原型未暴露 | 必需，缺失时估算并标注 |
| subagent | 部分有 | 有 | 可选 |
| MCP | 部分有 | 有 | 可选 |
| 持久化会话 | CLI JSONL | DSH session | 必需 |

三种集成模式，优先级从高到低：

1. **Freely core + HarnessPort + ACP adapter（现状的正式化）**：Freely 拥有 three-loop、A2A、scan、门禁；harness 只负责“跑一个 session”。这是当前事实，只缺显式接口和能力探测。
2. **Freely core + DSH adapter**：把 DSH 作为可切换基座之一，通过 Cordis/SDK 或子进程桥接 session/prompt/usage；Freely 仍然拥有路由与状态。适合“想要 DSH 的 session/tool 生态，但不想把治理交给 DSH”的场景。
3. **DSH host + Freely governance plugin**：只有当 DSH 已经拥有 loop 时，才把 Freely 的“门禁/工位/issue”做成 DSH 工具插件；不能让插件再起一套 Router/Ticket。适合“团队已经在 DSH 里工作，只想借用 Freely 的治理检查”。

可外溢为 DSH 插件的 Freely 能力（按价值排序）：

- `freely-gates`：`pr-create-guarded` / `pr-review-guarded` / `pr-merge-guarded --dry-run` 的工具化，让 DSH Worker 在提交前跑门禁。
- `freely-worktree`：`wt-create` / `wt-close` 的工具化，让 DSH Ticket 有独立工位与清理语义。
- `freely-issue`：raw issue / milestone / scan 的 Source 插件，把 Freely 的生命周期暴露成 DSH 的 Trigger。
- `freely-review`：Reviewer 的审查工具化；但只在 DSH 愿意把 verdict 当权威时才有意义。

不应外溢的：three-loop 调度、A2A 角色状态机、Manager 的 scan 路由。它们和 DSH 的 Engine/Ticket 是同一层，放进去就是双 Router。

对 Freely 的产品含义：

- Freely 应该把 `AGENT_AI_TOOL`/ACP 适配器正式收敛成 **HarnessPort**：能力探测、session 生命周期、prompt/stream、usage/cache、工具策略、失败降级。
- 配置面应支持 **按角色选 harness**（Manager/Worker/Reviewer 可不同），类似截图里的 Runtime 选择器；每个 harness 有 capability probe 与 fallback，而不是全局单值。
- DSH 是“一个可选基座 + 一个可选插件宿主”，不是 Freely 的替代品。优先级是“Freely 应用内可切换”，不是“把 Freely 搬进 DSH”。

![Freely HarnessPort 与 DSH 插件边界](freely-harness-port-boundary.svg)

[打开交互式版本](freely-harness-port-boundary.html)（archify）。图中三层优先级：先做 Freely 内的 HarnessPort；再把 DSH 作为 adapter；最后才考虑把 gates/worktree/issue 外溢成 DSH 工具插件。

P0 已经落地一个可运行切片：`freely harness-status`（`bin/harness-status` → `docs/system/workspace/scripts/runtime/harness_status.py`）。它按角色读取 `agent-table.toml`，推断工具族，输出 session/fork/resume/usage/cache 能力矩阵与二进制健康，并聚合 `cycle-*.log` 里的 `[CACHE]` 行。实测主项目输出显示：Claude/OpenCode 是 native fork，Codex/Cline 是 `degraded=fork`（运行时会尝试 fork 再降级 session/new）；能力矩阵读取 `tool-registry.toml`，不再手写第二份表。最近 50 个 cycle 的 21 条 cache 记录 `input_source=estimated`、hit=0/miss=0：当前 adapter 没有 provider usage，`input` 是 `prompt_bytes // 4` 的估算，不能当真实命中率。用 `--require fork` 实测当前主项目直接 fail：reviewer 的 Cline 是 degraded，要么换 reviewer slot，要么接受冷启动；这是可执行的配置结论，不是“待研究”。


## 5. 七处结构性差异及影响

### D1 授权在运行时数据里 vs 在流程门禁里

- 事实：Super-agent 的 Mandate 是不可变凭证，记录 Policy 版本、scope、strength、匹配规则；复活前重校验。Freely 没有 per-work-item 凭证，授权由角色、阶段、门禁、分支保护与人工指令共同构成。
- 影响：Super-agent 能在运行时阻止越权与范围蔓延；Freely 能在流程上保证“没走完 B1/B2/RED/test/review 就合不进去”。前者防“做错范围”，后者防“跳过治理”。
- 对 Freely 的含义：不必复制 Mandate 运行时，但可以借鉴“把授权依据结构化记录”这一点（谁批准的、依据哪版规则、范围是什么），让事后审计不必从文档里拼。

### D2 订阅直通 vs Manager 中转

- 事实：Super-agent 的 Thread 后续事件绕过 Router 直达订阅 Worker，且不授予新权限；越界消息可 handback。Freely 的 Worker 没有面向平台线程（PR/Issue）的订阅机制，外部后续消息要经 Manager/A2A 或重新进入 intake；Freely 的 SSE 订阅对象是 A2A task 流，不是平台线程。
- 影响：Super-agent 在同一 PR/Issue 的长对话里延迟更低、上下文更连续、Router token 更省（文章实验去掉直通后 Router token +37%）。Freely 的 Manager 成为所有后续信息的汇聚点，容易上下文膨胀，也可能把“继续讨论”误判成“新任务”。
- 对 Freely 的含义：这是最值得补的协作缺口，但不必上事件总线；可以先定义“已完成工单的 follow-up ownership + handback”，让线程消息有明确归属。

### D3 独立 Reviewer vs 无内建审查角色

- 事实：Freely 的 Reviewer 是独立 agent，fork Manager 上下文，用 `freely-tdd-review` 做四层审查并给出 pass/fail，可打回 Worker；PR 阶段另有 `pr-review-guarded` 的 6 维独立 review。Super-agent 没有 Reviewer 角色，Worker 自己处理 review，自动审查机器人只是“可错输入”，每 PR 最多三轮。
- 影响：Freely 的质量分离更强、审查可追责；代价是多一个 agent、多一轮协调与 token。Super-agent 协调更轻，但把“自审”风险留给了 Worker 与外部 bot/人。
- 对 Freely 的含义：不应为了“减少角色”而移除 Reviewer；反而可以借鉴 Super-agent 对自动审查机器人的“可错输入、限轮次、不追批准”纪律。

### D4 事件驱动状态机 vs 文档驱动生命周期

- 事实：Super-agent 的 Ticket stage 由结构化事实推导，代码是唯一写者；Freely 的阶段由 `phase_state`、文档与 scan 共同表达。
- 影响：Super-agent 的状态更精确、可查询、抗重启；Freely 的状态更可读、可审计、可跨工具，但存在文档与运行时漂移，需要 scan/gate 对账。
- 对 Freely 的含义：保留文档作为治理证据，但应把“阶段推导规则”收敛为单一算法（scan 已经是雏形），避免多个脚本各自解释阶段。

### D5 单仓/单机原型 vs 多项目 runtime

- 事实：Super-agent 原型只服务一个 GitHub 仓库、单机 `stateDir`、本机执行；Freely 管理多项目、多工位、多 AI 工具适配。
- 影响：Super-agent 可以把“一个团队一个仓库”的边界写死，从而把授权与上下文做深；Freely 必须处理租户、项目、工位、平台身份的多层隔离，协调成本更高。
- 对 Freely 的含义：不能直接移植“单 Router + 单库”的简化假设；任何借鉴都要先回答多项目下的身份与状态归属。

### D6 基座绑定 vs harness-agnostic

- 事实：DSH 原型的全部能力长在 Cordis/DSH API 上；Freely 通过 ACP 适配多 CLI，但适配器契约是隐式的。DSH 没有 ACP 服务端，Freely 没有 DSH adapter。
- 影响：DSH 在自家宿主里可以做深（Session、工具 preset、面板、插件），但换宿主就要重写；Freely 天然可换 CLI，但每个 CLI 的能力差异靠代码分支兜底，缺少统一能力探测。
- 对 Freely 的含义：把 harness 抽象成显式端口，优先级高于做 DSH 插件。否则“可切换基座”只是口头承诺；插件化会先遇到两边状态机争夺所有权的问题。

### D7 缓存纪律：prefix 稳定 vs fork 复用

- 事实：DSH 的 prompt 段序固定、Policy 最后、覆盖带 base 版本，天然保护 prefix cache；但 Router/Worker 各自冷启动，原型没有 cache 指标。Freely 的 session resume/fork 复用强、有 `[CACHE]` 度量，但 prompt 由角色定义 + 运行时状态拼接，没有显式前缀契约，fork 还会把无关上下文带进 Worker。
- 影响：DSH 的缓存收益是“稳定但不可见”；Freely 的缓存收益是“可见但不可控”。两者都可能出现“命中率很高但上下文不对”的情况，只是原因不同。
- 对 Freely 的含义：短期先度量（按角色、launch_kind、prompt_bytes 分组），中期把 prompt 分成“稳定前缀 / 可变尾部”，长期把 fork 从“复制 Manager 全部上下文”改为“带治理摘要的最小继承”。

## 6. 双方代价与未解问题

### Super-agent 的代价

- **信任边界在 OS 层**：Executor 以 operator 账号免审批跑命令，文档明说“这些 wrapper 和目录只是默认值，不是安全边界”；`007` 的 open questions 也承认 Trigger 字段可信度与部署隔离未定。
- **单 Router 仍是单点**：文章承认规模扩大后如何切分、Worker 何时直接通信、跨月长程记忆都未定；批处理只是把积压摊薄，不改变单 Session 的上限。
- **Worker 冷启动、缓存不可见**：Router 与 Worker 各自 Session，Worker 不继承 Router 上下文；原型没有 cache hit/miss 指标，无法判断“省了没有”。
- **插件面锁定**：能力长在 Cordis/DSH API 上，`engines.dsh` 钉版本；换宿主不是配置问题，是重写问题。
- **单仓限制**：README 与部署文档把范围钉死在一个仓库，扩到多仓要先回答组织授权问题。
- **漏判不可见**：默认 `observe` + “不确定就安静忽略”，被漏掉的请求只留一条 Decision，缺少抽样复核流程。
- **原型缺口**：watchdog、投机执行、存算分离、异步 ReAct 主路径都未落地；文章数字来自合成负载，不能当生产结论。

### Freely 的代价

- **Manager 是注意力与上下文瓶颈**：scan、A2A 状态、文档、人工插话都汇聚到 Manager；它既要路由又要判断，容易上下文膨胀。
- **文档状态会漂移**：`phase_state`、milestone、scan、平台 issue 多源并存，需要持续对账。
- **后续线程连续性弱**：PR/Issue 上的后续讨论没有明确 owner，容易重新开单或漏接。
- **授权依据分散**：谁在什么规则下批准了这次改动，散落在 issue、review、PR、聊天里，缺少结构化凭证。
- **A2A 是任务状态协议，不是事件总线**：它擅长“任务到哪一步”，不擅长“同一线程又来了什么”。
- **HarnessPort 是隐式的**：ACP 适配器能跑，但能力差异靠分支兜底，没有统一 probe/fallback；DSH 没有 adapter。
- **缓存“可见但不可控”**：有 `[CACHE]` 日志，但 prompt 没有稳定前缀契约，fork 继承的是 Manager 全量上下文，命中率高不等于上下文对。
- **双编排风险**：若把 Freely 做成 DSH 插件又保留 three-loop，会出现两套 Router/Ticket 争夺同一工单；必须先定“一个 loop 一个 owner”。

### 共同未解问题

- Prompt injection 与不可信内容：两边都把消息正文当数据，但都还没有完整的信任分级执行面。
- 凭据隔离：Super-agent 明确让 Agent 用真实账号；Freely 用 adapter/工位隔离，但 Agent 仍有 shell 能力。
- 长程记忆：Super-agent 靠 ID 链式召回，Freely 靠文档；都缺少可验证的“跨月记忆正确性”。
- 跨实例协作：Super-agent 文章提出 A2A 但原型未实现；Freely 的 A2A 目前以同项目为主。
- 注意力度量：两边都谈“减少人的注意力”，但都没有可复现的注意力成本指标。
- Harness 能力标准化：ACP 只覆盖 session/prompt，不覆盖工具策略、skills、usage 语义；DSH 的插件协议是私有的。谁先定义稳定的 harness capability contract，谁就更容易做“可切换基座”。

## 7. 可借鉴 / 可适配 / 不照搬

| 判断 | 机制 | 实现层面的理由 |
| --- | --- | --- |
| 可借鉴 | 结构化 Attention：一个问题、目标会话、可执行动作 | DSH 用 `human_action` + 稳定 request id 把“人要不要动作”做成字段；Freely 的 `input-required` 主要面向角色路由 |
| 可借鉴 | 越界消息 handback：带理由、只交回一次 | 补 Freely 后续线程归属不清；DSH 用 `followupOwners` + `handback` 做成运行时事实 |
| 可借鉴 | 路由批处理 + 逐条拒绝 | `orchestrator_route` 1–20 条、单条失败不影响其他；Freely 目前逐条 `a2a-exit`，没有批量语义 |
| 可借鉴 | 事件级幂等键 | accept 以 trigger ID 幂等，report/attention relay 用稳定 key；Freely 靠查询防重复，重试可能重复 |
| 可借鉴 | Prompt 段序与 Policy 置尾 | DSH 的 prompt 顺序保护 prefix cache；Freely 的 scan/fleet/checkpoint 追加在尾部，但无显式契约 |
| 可借鉴 | 工具面即契约 | Router/Worker preset 明确工具清单；Freely 靠提示词约束，硬约束弱 |
| 可适配 | 订阅直通 | 不做事件总线，先做“同一工单线程的 follow-up ownership”，范围可控 |
| 可适配 | Policy 版本 | 不作为运行时 Mandate，可作为 issue/PR 元数据记录“依据哪版规则批准” |
| 可适配 | 批处理 | Manager patrol 已有批处理语义，可显式化并度量，而不是照搬 Router Session |
| 可适配 | Harness 选择器 | 借鉴 DSH Runtime picker 的 UX，按角色选 harness，但必须配 capability probe 与 fallback |
| 可适配 | DSH adapter | 通过 Cordis/SDK 或子进程桥接，把 DSH 作为 `HarnessPort` 的一个实现；不让 DSH 接管 three-loop |
| 可适配 | Freely governance 作为 DSH 工具插件 | 只外溢 `freely-gates` / `freely-worktree` / `freely-issue` 这类工具；不外溢 Router/Ticket |
| 不照搬 | 默认 observe / 默认不做 | 与 Freely “自主项目所有者”的产品目标冲突 |
| 不照搬 | 单仓/单机假设 | 与 Freely 多项目 fleet 冲突 |
| 不照搬 | 移除独立 Reviewer | 会削弱 Freely 的质量分离与可追责性 |
| 不照搬 | 11 个领域概念全量迁移 | 成本高、与 Freely 文档驱动生命周期不匹配 |
| 不照搬 | 事件溯源式重写 | Freely 的治理证据在文档与平台，不在单一事件库 |
| 不照搬 | 双 Router / 双 Ticket | 插件化时最容易犯的错：两套状态机争夺同一工单，必须一个 loop 一个 owner |

## 8. Decision（2026-11-01 预研复审后）

- **不整体迁移 Super-agent 架构，也不把 Freely 搬进 DSH。** 两者目标不同：Super-agent 优化“团队被打扰的次数”，Freely 优化“项目从问题到合并的自治闭环”。
- **保留 Freely 的四个差异优势**：文档驱动的 B1/B2 治理、独立 Reviewer、多项目 registry、harness 可替换。
- **P0 已实现 Harness 能力探针与缓存观测**：`freely harness-status` 能回答每个角色用什么 harness、fork 是 native/degraded、ACP 二进制是否可解析、cache 是 usage 还是 estimated。
- **当前不 promote、不写实现。** 复审发现 C-B/C-D 的边界被新证据推翻，C-B/C/C-D 全部回到 `needs_research`，并新增 C-E（DSH 插件）。
- **新证据（2026-11-01）**：
  1. Freely 的 A2A 实际是本地 task 表：无 contextId/messageId/artifact 历史，Manager/Worker/Reviewer 覆盖同一行；对外 A2A 任务创建即 COMPLETED，与内部状态不一致。
  2. `acp_session_connect()` 在 `session/new|fork` 路径不发送传入 message；首次 Reviewer 交接、Worker 死亡后的 fail 反馈可能丢消息。
  3. Reviewer 契约矛盾：agent 文档禁止 `a2a-exit`，watchdog 消息却要求调 `a2a-exit`，skill 又要求 JSON verdict。
  4. DSH 主插件可注入 `agents/sessionController/tools/skills/systemPrompt`；因此“Freely 保留 loop、DSH 只做 harness”的 Freely-host 插件在代码层可行，但需要 spike。
- **下一跳不是实现，是 B1 acceptance review；优先级按主意图：讨论入口 C-F → 交接 C-B/C → Harness C-D → DSH C-E。**
  - C-B：先做五类后续消息行为盘点 + handoff envelope/ownership 协议草案；修 new/fork 丢 message 的已知 bug 后再回放。
  - C-C：先写 report 六态/attention/ownership 字段契约 + prompt manifest/基线，不直接改 A2A。
  - C-D：先定 HarnessPort/RoleHarnessConfig 与 per-role probe/配置落点，不做 DSH adapter。
  - C-E：先做 `@freely/dsh-freely` P0/P1 spike，验证 DSH services、首次 session 消息、handoff、gate。
- **明确不做**：per-ticket Mandate 运行时、默认 observe、单仓绑定、移除 Reviewer、事件溯源重写、双 Router/双 Ticket。
### 8.1 预研 loop

B1 不是“写完文档就 promote”。每个 candidate 的循环是：

```
研究 → 按 acceptance_criteria 自检 → 缺口 → 回研究
     → 满足 promotion_gate → 独立 acceptance review → B2
```

当前 5 个 candidate 的 readiness matrix 在 `pre-brainstorm-review.md` §7.1；任一“仍缺”未关闭，status 保持 `needs_research`，不得 promote。主意图优先级：C-F 讨论入口 → C-B/C 交接 → C-D harness → C-E 插件。这是本轮从“准备实现”退回“继续预研”的原因。

## 9. Candidate

- `C-20261101T031502Z-A`：对比研究、概念全量对照、P0 `harness-status` 与方向立项（promoted → `I-20261101T031502Z-A`）。
- `C-20261101T031502Z-B`：follow-up ownership 与 handback（needs_research；先补行为盘点 + 协议草案 + new/fork 丢消息修复）。
- `C-20261101T031502Z-C`：类型化 report/attention、批量路由与 prompt 前缀契约（needs_research；先补字段契约 + prompt manifest/基线）。
- `C-20261101T031502Z-D`：HarnessPort 与角色级 harness 选择（Freely 主应用，needs_research；先补接口/配置/探测）。
- `C-20261101T031502Z-E`：`@freely/dsh-freely` Freely-host 插件（needs_research；先做 P0/P1 spike）。
- `C-20261101T031502Z-F`：讨论入口（issue comment/PR review/CI）（needs_research；先做来源盘点 + 真实回放）。
- milestone：`M-20261101T031502Z-A`。

## 10. 任务拆分：未来实现路线（未批准，不得直接开工）

> 以下只是通过 acceptance review 后可能进入 B2 的路线；当前状态是 needs_research，不是施工单。

| 优先级 | 任务 | 具体改动 | 验收 |
| --- | --- | --- | --- |
| P0（已完成） | Harness 能力探针 + 缓存观测 | 新增 `harness_status.py`、`bin/harness-status`、`freely harness-status`；能力矩阵、按角色读取 agent-table、二进制探针、`[CACHE]` 聚合 | 单测 7 项通过；主项目实测输出角色/能力/cache；`--require fork` 对 Codex/Cline 返回 3 |
| P1-0 | 修复交接丢消息 | `acp_session_connect` 在 new/fork 后显式 prompt；新 session 注入角色定义；统一 Reviewer verdict 契约 | 首次 Reviewer/死亡 Worker 能收到 task message + role prompt |
| P1-1 | follow-up ownership + handoff envelope | append-only `handoffs`/`handoff_messages`；ownership/handback；scan 开单前查 owner | 真实 PR 评论回放：同一线程不重复开单；越界消息只 handback 一次 |
| P1-2 | 类型化交接 | `a2a_task.py --report-state` 六态；`--attention` JSON（question/target/action）；A2A server 原样存；稳定 relay key | 六态可查询；重复 report 不重复投递；attention 路由回原会话 |
| P1-3 | prompt 缓存契约 | Manager prompt 拆 stable_prefix/volatile_tail；日志标注两段 bytes；Policy/settings 固定在尾部 | `harness-status` 对照显示 prefix 稳定；volatile 变化不影响前缀字节 |
| P2 | HarnessPort 接口 | 把能力矩阵提升为 contract；`run-acp-prompt.py` 启动前 probe + fallback；per-role harness 选择 | 缺 fork 的 harness 自动降级；能力缺失给出明确错误 |
| P3 | `@freely/dsh-freely` 插件 | Freely-host：DSH harness + bridge；不加载 dsh-superagent；handoff envelope | P0/P1 spike：首次 session 收到 task+role prompt、gate 阻断、无 ACP |

依赖关系：P1-2 依赖 P1-1 的 owner 语义；P1-3 独立可先做；P2 依赖 P0 的能力矩阵；P3 必须在 P2 之后。

## Appendix: 证据索引

| 事实 | 来源 |
| --- | --- |
| 文章五模块、实验数字 | 智东西报道 `https://www.zhidx.com/p/606311.html`；博客园拆解 `https://www.cnblogs.com/itech/p/23508901` |
| 原型范围与免责声明 | 原型 `README.md` |
| 11 个领域概念、拒绝概念表 | 原型 `docs/001-domain.md` |
| 准入表、observe/auto、Policy 版本 | 原型 `docs/002-authorization.md` |
| Ticket stage、worker slot、恢复 | 原型 `docs/003-execution.md` |
| Prompt 分层与覆盖 | 原型 `docs/004-prompts.md` |
| 面板三问 | 原型 `docs/005-panel.md` |
| 单仓库、单机 stateDir、GHES 不支持 | 原型 `docs/006-deployment.md` |
| Engine 单写者、effect 队列、工具面 | 原型 `docs/007-architecture.md` |
| Router 不读代码、不下实现指令 | 原型 `prompts/orchestrator.md`、`prompts/dispatch.md`、`prompts/shared.md` |
| 订阅直通、handback、复活 | 原型 `prompts/subscriptions.md`、`docs/002-authorization.md` |
| Freely 角色与会话 | `docs/system/workspace/agents/*.md`、`docs/system/workspace/session-lifecycle-protocol.md` |
| Freely A2A 状态与 SSE | `docs/system/workspace/a2a/protocol-design.md`、`exit-kind-mapping.md`、`acp-a2a-architecture.md` |
| Freely 三 loop 与 gate | `docs/system/workspace/three-loop-capability-lifecycle.md` |
| Freely scan 阶段 | `docs/system/workspace/scan-lifecycle-design.md` |
| Freely 运行时监督面 | `docs/system/workspace/three-loop-capability-lifecycle.md` §Runtime 监督面机制真源 |
| 概念全量映射与同名不同义 | 本文目录 `concept-map.md` |
| 路由批处理、逐条拒绝、accept 幂等 | 原型 `src/app/tools/main.ts` |
| 六态 report、attention、relay 幂等 key | 原型 `src/app/notices.ts`、`src/executor/dsh.ts` |
| worker slot 与人优先槽位 | 原型 `src/executor/dsh.ts` |
| prompt 段序、Policy 置尾、revision | 原型 `src/app/prompts.ts`、`docs/004-prompts.md` |
| 插件/宿主绑定 | 原型 `package.json`、`cordis.patch.yml` |
| Freely ACP 会话/usage/cache | `docs/system/workspace/scripts/runtime/run-acp-prompt.py` |
| Freely harness 选择面 | `AGENT_AI_TOOL` 配置、`docs/system/workspace/session-lifecycle-protocol.md` |
| 协作拓扑对比图 | `super-agent-vs-freely-collaboration.html` / `.svg` |
| HarnessPort 与插件边界图 | `freely-harness-port-boundary.html` / `.svg` |
| 交接缺陷/A2A/AHP/ACP | `agent-handoff.md` |
| 两种部署形态 | `deployment-forms.md` |
| 角色级 harness 选择 | `harness-selection.md` |
| DSH 插件设计 | `dsh-freely-plugin-design.md` |
| 主意图逐条对齐 | `intent-alignment.md` |
| 讨论入口缺口 | `intent-alignment.md` §4.1 |
