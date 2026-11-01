# PRD: Super-agent 架构对比、实现质量评估与协作方向立项

- issue_id: I-20261101T031502Z-A
- source_raw: raw-20261101T031502Z
- milestone: M-20261101T031502Z-A

## Goal

用一份可复核的研究，回答三个问题：

1. Super-agent 与 Freely 在 agent 协作上的结构性差异是什么？
2. 在路由、交接、缓存命中、harness 抽象这些具体实现上，谁做得更扎实，Freely 差在哪？
3. Freely 该吸收什么、该把 agent harness 放在什么位置、哪些能力适合做 DSH 插件？

研究 + P0 探针是本 issue 的交付物；P1/P2 实现由后续独立 issue 承接。

## 背景

Freely 当前以 Manager / Worker / Reviewer 三角色、A2A Task、文档驱动生命周期和 PR 门禁组织 agent 协作。DeepSeek Harness 的 Super-agent 提出另一套组合：常驻 Router + 隔离 Worker、事件驱动、Thread 订阅直通、存算分离、外部 Watchdog。

两套系统目标不同：前者是“项目所有者 + 治理闭环”，后者是“团队助手的注意力预算”。直接比较“谁更强”没有意义；需要比较的是同一批协作问题各自怎么解、实现质量如何、代价是什么。

## 交付内容

1. **证据分级**：区分文章主张、原型实现、Freely 现状，避免把未实现的设计当成事实。
2. **逐维比较**：角色拓扑、委派交接、授权、事件与状态、上下文、并发冲突、失败恢复、人机交互、可观测性、部署边界。
3. **实现质量评估**：路由（准入、批处理、逐条拒绝、幂等）、交接（六态 report、attention、handoff、followup ownership）、缓存（session/fork、prompt 段序、cache 度量）。
4. **概念全量对照**：把 Super-agent 的 Source/Trigger/Thread/Correlation/Channel/Policy/Eval/Gate/Assessment/Decision/Mandate/Ticket/Assignment/Subscription/Report/Attention/Disposition/Input/Scope/Strength/Executor/Effects/Outbox/Health 等逐项映射到 Freely 的叫法，标出同名不同义与双向缺口。
5. **结构性差异**：授权在运行时数据 vs 流程门禁、订阅直通 vs Manager 中转、独立 Reviewer vs 无内建审查、事件状态机 vs 文档生命周期、单仓原型 vs 多项目 runtime、基座绑定 vs harness-agnostic、prefix 纪律 vs fork 复用。
6. **Harness/插件边界**：ACP、A2A、MCP、Cordis 插件各自连接谁；DSH 没有 ACP 服务端的事实；三种集成模式的优先级；可外溢为 DSH 插件的 Freely 能力清单。
7. **候选登记**：`C-A` 作为研究+P0 交付本身 promote 到本 issue；`C-B/C/D` 是 `proposed` 的下一阶段任务（follow-up ownership、路由/交接/cache 契约、HarnessPort）。
8. **P0 实现**：新增 `harness_status.py` + `bin/harness-status` + `freely harness-status`，输出角色 harness 能力矩阵、二进制健康、`[CACHE]` 聚合；`--require` 可让缺 fork/usage 的配置失败。

## 非目标

- 不实现 C-B/C/D 的完整 P1/P2；本次只落地 P0 探针。
- 不改 A2A、scan、three-loop、agent 提示词、runtime 或 harness adapter。
- 不复制 Super-agent 的领域模型；不引入默认 `observe`、单仓假设或双 Router。
- 不做性能压测或文章实验复现。

## 验收映射

| 验收项 | 证据 |
| --- | --- |
| 七个比较维度齐全 | `brainstorms.md` §4 各小节 |
| ≥3 处结构性差异 | `brainstorms.md` §5 D1–D7 |
| 实现级差距 | `brainstorms.md` §4.12 评分表 |
| 全量概念映射 | `concept-map.md` §1–§10 |
| candidate 不伪造 promote | `candidates.md`：C-A promoted 到本 issue，C-B/C/D 为 `proposed` 且带实现任务 |
| 两张图可读 | `super-agent-vs-freely-collaboration.*`、`freely-harness-port-boundary.*` |
| P0 单测 | `verification/test-evidence/acceptance-6.log` |
| P0 CLI | `verification/test-evidence/acceptance-7.log` |
| 治理门禁 | `verification/test-evidence/acceptance-5.log` |

## 风险与边界

- 文章原文未直接获取：用两篇按原文结构复述的报道交叉核对，只在两者一致时引用；这是研究限制，已在文档中声明。
- 原型只做静态阅读，未运行真实 GitHub 仓库；因此“已实现”只表示代码/文档存在。
- 架构图是拓扑对比，不表达全部时序；`report`、`SSE`、`verdict` 等回流在文字与图注中说明。
- DSH adapter 的可行性只做设计判断，不在本 issue 写代码；in-process/子进程的选择留给 C-C 的 spike。
- 三个后续 candidate 仍是研究项；若后续行为盘点/度量证明缺口不存在，应按 `revisit_trigger` 降级或丢弃。

## Dev-Loop Handoff

P0 已在本 issue 内实现并验证；`C-20261101T031502Z-B/C/D` 在满足 `revisit_trigger` 后重新 `wt-create`，按 §10 的任务拆分走独立 B2/RED/dev/test。
