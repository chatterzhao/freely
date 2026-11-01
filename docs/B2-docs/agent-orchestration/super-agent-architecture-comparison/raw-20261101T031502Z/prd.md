# PRD: Super-agent 架构对比研究与协作方向立项

- issue_id: I-20261101T031502Z-A
- source_raw: raw-20261101T031502Z
- milestone: M-20261101T031502Z-A

## Goal

用一份可复核的研究，回答“Super-agent 的协作设计与 Freely 有什么结构性差异、Freely 该吸收什么”，并把值得推进的方向登记为 B1 candidate。研究本身是本 issue 的交付物；实现由后续独立 issue 承接。

## 背景

Freely 当前以 Manager / Worker / Reviewer 三角色、A2A Task、文档驱动生命周期和 PR 门禁组织 agent 协作。DeepSeek Harness 的 Super-agent 提出另一套组合：常驻 Router + 隔离 Worker、事件驱动、Thread 订阅直通、存算分离、外部 Watchdog。

两套系统目标不同：前者是“项目所有者 + 治理闭环”，后者是“团队助手的注意力预算”。直接比较“谁更强”没有意义；需要比较的是同一批协作问题各自怎么解、代价是什么。

## 交付内容

1. 区分文章主张、原型实现、Freely 现状三类证据，避免把未实现的设计当成事实。
2. 逐维比较：角色拓扑、委派交接、授权、事件与状态、上下文、并发冲突、失败恢复、人机交互、可观测性、部署边界。
3. 给出五处结构性差异及影响：
   - 授权在运行时数据（Mandate）里 vs 在流程门禁里；
   - Thread 订阅直通 vs Manager 中转；
   - 无内建 Reviewer vs 独立 Reviewer；
   - 事件驱动状态机 vs 文档驱动生命周期；
   - 单仓/单机原型 vs 多项目 runtime。
4. 给出“可借鉴 / 可适配 / 不照搬”清单。
5. 用 archify 输出协作拓扑对比图（HTML + 静态 SVG）。
6. 登记两个 `needs_research` candidate：follow-up ownership/handback、Manager 注意力预算。

## 非目标

- 不实现任何 candidate。
- 不改 A2A、scan、three-loop、agent 提示词或 runtime。
- 不复制 Super-agent 的领域模型；不引入默认 `observe` 或单仓假设。
- 不做性能压测或文章实验复现。

## 验收映射

| 验收项 | 证据 |
| --- | --- |
| 七个比较维度齐全 | `brainstorms.md` §4 各小节 |
| ≥3 处结构性差异 | `brainstorms.md` §5 D1–D5 |
| 事实可回溯 | `brainstorms.md` Appendix 证据索引 + 引用路径 |
| candidate 不伪造 promote | `candidates.md` 两个 `needs_research` |
| 对比图可读 | `super-agent-vs-freely-collaboration.html` / `.svg` |
| 治理门禁 | `verification/test-evidence/acceptance-5.log` |

## 风险与边界

- 文章原文未直接获取：用两篇按原文结构复述的报道交叉核对，只在两者一致时引用；这是研究限制，已在文档中声明。
- 原型只做静态阅读，未运行真实 GitHub 仓库；因此“已实现”只表示代码/文档存在。
- 架构图是拓扑对比，不表达全部时序；`report`、`SSE`、`verdict` 等回流在文字与图注中说明。
- 两个 candidate 仍是研究项；若后续行为盘点证明缺口不存在，应按 `revisit_trigger` 降级或丢弃，不得为了凑数推进。

## Dev-Loop Handoff

本次不进入 dev-loop。`C-20261101T031502Z-A` 与 `C-20261101T031502Z-B` 各自在满足 `revisit_trigger` 后重新 `wt-create`，走独立 B1/B2/RED/dev/test。
