---
b1_id: B1-20261101T031502Z
phase_state: completed
source_raw: raw-20261101T031502Z
source_url: https://github.com/chatterzhao/freely/issues/4110
produced_candidate: C-20261101T031502Z-A, C-20261101T031502Z-B, C-20261101T031502Z-C, C-20261101T031502Z-D, C-20261101T031502Z-E, C-20261101T031502Z-F
created_at: 2026-11-01
---

# B1_IBM: Super-agent 与 Freely code harness 对比研究

> 最终研究包入口：[`research-index.md`](research-index.md)。本文只保留 B1 决策记录；详细对比、协议、运行时契约、harness 策略分别在最终文档中。

## 1. Input

- raw issue：`raw-20261101T031502Z`（GitHub #4110 / Gitee IKS0MD）。
- 文章：DeepSeek Harness《Exploring Super-agent Design: Towards a More Autonomous Agent System》（2026-10-31）。
- 三篇解读：智东西、IT之家、驱动中国；智东西最完整，IT之家/驱动中国更概览。
- 原型：`deepseek-ai/dsh-superagent-prototype` @ `6337fc823ce20251c8de8085948165c81aaa701e`（MIT，TypeScript；研究原型，非正式产品）。
- Freely 侧：`PROJECT_INTENT/CONSTITUTION/LAWS`、three-loop、agents、a2a、scan、gates、ACP/runtime。

## 2. Problem

要回答的不是“谁功能多”，而是：

> Freely 作为 **LLM 主动、自主、持久、连续的 code harness**，与 Super-agent 在**意图重叠部分**（主动发现、分派、执行隔离、连续、交接、授权、持久、上下文）各自怎么解、谁更合适、代价是什么；哪些该吸收，哪些会拖后腿。

Freely 多出来的 SDD/TDD、B1/B2、Reviewer、PR/merge gate、worktree、多项目，不拿来证明“Freely 赢”；Super-agent 的 IM/云端/BYOM/投机执行，也不算 Freely 的缺口。

## 3. Boundary

- 只比较重叠意图，不做全量领域模型迁移。
- 不因为 Super-agent 有 Router 就丢掉 Freely 的 SDD/TDD/Reviewer/gates。
- 不因为 Freely 有文档就拒绝吸收事件准入/ownership/report/attention。
- 不先做 DSH 全量插件；先补主意图缺口（讨论入口、交接、持久、约束）。
- 研究阶段不 promote、不写实现。

## 4. Discovery

1. **共同意图**：人的注意力上移；Agent 主动/自主/持久/连续；多个隔离 Worker + 全局连续性。
2. **智东西的增量**：Router 可轻量、批处理扛突发；Fast/Slow filter；订阅直通；Inline/Spill；链式召回；投机执行；存算分离；外部 Watchdog。实验基于合成负载，只评调度。
3. **三篇共同点**：四特征/五模块；Worker 不直接对外；订阅直通；持久靠状态/计算/环境分离 + Watchdog。
4. **关键差异**：智东西明确把 A2A 列为开放问题；Freely 现在用 A2A 做内部交接，是超前尝试，但必须自己补 message/context/artifact/ownership。
5. **Freely 实现的关键缺口**：
   - scan 只处理 issue body，不处理 issue comment/PR review/CI；
   - A2A 是 task 行，没有 message/artifact 历史；`session/new|fork` 丢 message；
   - Reviewer 契约矛盾；
   - MCP 未编排；LAWS 未自动注入；SDD/TDD 门禁偏后；无独立语义 Watchdog；
   - 全局 adapter，角色级 harness 选择未落地。
6. **Freely 的强项**：角色分工、B1/B2、SDD/TDD 合同、独立 Reviewer、PR/merge gates、worktree/test lane、harness probe、多项目 registry。

## 5. Brainstorm

### Option A：整体迁移 Super-agent 领域模型

- 引入 Trigger/Thread/Ticket/Mandate/Report/Attention/Disposition/Effects 全套。
- 优点：运行时协作对象完整。
- 缺点：与 Freely 文档/SDD/TDD/Reviewer/gates 双状态；事件溯源重写；单仓/云端假设；成本高。
- 结论：**不采用**。

### Option B：不吸收，保持现状

- 只修 bug，不引入事件准入/ownership/report。
- 优点：改动小。
- 缺点：scan 讨论入口、交接丢消息、注意力/持久缺口仍在；主意图不闭环。
- 结论：**不采用**。

### Option C：只吸收重叠意图的运行时 primitive，保留 Freely core

- 吸收：事件准入、Thread/ownership/handback、Report/Attention、批量路由+幂等、prompt manifest/usage、轻量语义 Watchdog。
- 保留：B1/B2、SDD/TDD、Reviewer、PR/merge gates、worktree、多项目、ACP/HarnessPort。
- 不吸收：Mandate 全量、默认 observe、单仓/单机、移除 Reviewer、事件溯源、双 Router/Ticket、云端/BYOM/投机执行。
- 结论：**采用**。

## 6. Decision

- Freely 是 code harness，主意图比 Super-agent 更大；对比只取重叠段。
- 意图层优秀，实现层部分不合格：讨论入口、交接、持久、约束、逐步 SDD/TDD 未闭环。
- 当前不 promote、不写实现；C-B/C/C-D/E 全部 `needs_research`，新增 C-F（讨论入口）为第一优先。
- 吸收顺序：**C-F 讨论入口 → C-B/C 交接 → C-D harness → C-E 插件**。
- 明确不做：per-ticket Mandate 运行时、默认 observe、单仓绑定、移除 Reviewer、事件溯源重写、双 Router/双 Ticket。

## 7. Candidate

| Candidate | 状态 | 下一跳 |
| --- | --- | --- |
| C-A 对比研究+P0 | promoted | 保留 |
| C-F 讨论入口 | needs_research | 六类来源 schema + 真实 issue 评论/PR review 回放 |
| C-B ownership/handback | needs_research | 五类消息行为盘点 + 真实回放；协议 v0 已有 |
| C-C report/attention/prompt | needs_research | prompt manifest/基线 + patrol 对照 |
| C-D HarnessPort/角色选择 | needs_research | 接口草案 + per-role probe |
| C-E DSH 插件 | needs_research | P0/P1 spike；依赖 B/D/F |

Milestone：`M-20261101T031502Z-A`。Readiness matrix 见 [`pre-brainstorm-review.md`](pre-brainstorm-review.md)。

## 8. 预研 loop

```
研究 → acceptance_criteria 自检 → 缺口 → 回研究
     → promotion_gate → 独立 acceptance review → B2
```

任一 readiness gap 未关闭，status 保持 `needs_research`，不得 promote。

## 9. 未来实现路线（未批准）

| 优先级 | 任务 | 验收 |
| --- | --- | --- |
| P0 | C-F 讨论入口 + 事件准入 | issue comment/PR review/CI 进入 scan；真实回放 |
| P1 | C-B 交接修复 + handoff envelope | new/fork 收到 message+role；ownership/handback |
| P1 | C-C report/attention + prompt manifest | 六态/attention 可查询；prefix 稳定；usage 可区分 |
| P2 | C-D HarnessPort + 角色级选择 | per-role probe；UI/CLI 同后端 |
| P3 | C-E DSH 插件 spike | 首次 session 消息、handoff、gate、无 ACP |

## 10. 证据

- [`overlap-comparison.md`](overlap-comparison.md)：只比重叠意图、逐项判定、吸收清单。
- [`intent-alignment.md`](intent-alignment.md)：主意图逐条对齐、优秀/部分/缺口/拖后腿。
- [`concept-map.md`](concept-map.md)：全量概念映射、同名不同义。
- [`delivery-model.md`](delivery-model.md)：B1/B2、SDD/TDD、三角色、3 loop + 2 门禁。
- [`handoff.md`](handoff.md)：交接缺陷 + delegation protocol v0。
- [`runtime-contracts.md`](runtime-contracts.md)：状态、准入、prompt/cache、注意力、可观测、TDD。
- [`harness-strategy.md`](harness-strategy.md)、[`harness-selection.md`](harness-selection.md)、[`dsh-freely-plugin-design.md`](dsh-freely-plugin-design.md)：harness 策略/选择/插件。
- [`failure-modes.md`](failure-modes.md)、[`pre-brainstorm-review.md`](pre-brainstorm-review.md)、[`docs-directory-audit.md`](docs-directory-audit.md)。
- 图：[`super-agent-freely-overlap.html`](super-agent-freely-overlap.html) / `.svg`。
