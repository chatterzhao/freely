---
pre_brainstorm_id: PB-20261101T231000Z
phase_state: completed
topic: Freely vs DeepSeek Super-agent
created_at: 2026-11-01
---

# B1 研究包：分类索引

> B1 标准产物在上一级：`issue.md`、`brainstorms.md`、`candidates.md`、`pre-brainstorm-review.md`。本目录只放研究结论/协议/证据，按问题分类，避免跨度混在一起。

## 一句话结论

**Super-agent 强在“事件 → 准入 → 分派 → 交接 → 注意力”的运行时；Freely 强在“规格 → TDD → 独立评审 → 合并治理 → 多项目”的交付链。** Freely 只吸收重叠意图的运行时 primitive，不整体迁移领域模型。

## 分类

| 类别 | 回答什么 | 文档 |
| --- | --- | --- |
| **A. 对比研究** | Super-agent 与 Freely 的重叠意图、概念映射、逐项判定、失效模式 | [comparison/overlap-comparison.md](comparison/overlap-comparison.md)、[concept-map.md](comparison/concept-map.md)、[intent-alignment.md](comparison/intent-alignment.md)、[failure-modes.md](comparison/failure-modes.md) |
| **B. Freely 交付/运行时** | Freely 自身怎么交付：B1/B2、SDD/TDD、三角色、交接协议、状态/准入/缓存/TDD 契约 | [delivery/delivery-model.md](delivery/delivery-model.md)、[handoff.md](delivery/handoff.md)、[runtime-contracts.md](delivery/runtime-contracts.md) |
| **C. Harness 策略** | harness 可插拔、两种部署形态、角色级选择 UI/CLI/配置 | [harness/harness-strategy.md](harness/harness-strategy.md)、[harness-selection.md](harness/harness-selection.md) |
| **D. DSH 插件（相邻课题）** | Freely 是否/如何作为 DSH 插件；与 Super-agent 插件形态的关系 | [dsh-plugin/README.md](dsh-plugin/README.md)、[dsh-freely-plugin-design.md](dsh-plugin/dsh-freely-plugin-design.md) |
| **E. 运维/证据** | 目录归位、遗留目录、既有门禁缺陷、研究债台账 | [ops/docs-directory-audit.md](ops/docs-directory-audit.md)、[research-debt.md](ops/research-debt.md)、[decisions.md](ops/decisions.md) |
| 图 | 重叠意图与吸收点 | [assets/super-agent-freely-overlap.html](assets/super-agent-freely-overlap.html)（SVG 同目录） |

### 为什么 DSH 插件单独一类

Super-agent 是 DSH 的一个插件（`dsh-superagent`），不是 DSH core。它的插件形态可以借鉴“一个 loop 一个 owner”“插件边界/生命周期/配置真源”，但**不代表** Freely 的 Manager/Worker 对比结论，也不改变 C-F/C-B 的优先级。详见 [dsh-plugin/README.md](dsh-plugin/README.md)。

## 关键结论

1. **主意图**：Freely 是 LLM 主动、自主、持久、连续的 code harness；scan 监控 issue/讨论/chat，遵循 intent/constitution/laws/gates/tool/skill/MCP，维护规格/测试，按 SDD/TDD 持续开发。
2. **意图层优秀、实现层部分不合格**：角色分工/B1/B2/Reviewer/gates/worktree/harness probe 是优势；讨论入口、交接、语义 Watchdog、MCP、逐步 SDD/TDD 是缺口。
3. **最高优先级缺口**：scan 不处理 issue comment/PR review/CI（C-F）。
4. **交接缺陷**：A2A 是 task 行；`session/new|fork` 丢 message；Reviewer 契约矛盾（C-B）。
5. **运行时契约**：状态是分域真相；事件准入缺 actor/event id；prompt 有排序无 manifest；cache 多估算；TDD GREEN 硬/RED 软。
6. **Harness**：主应用选 ACP tool+slot，写 `agent-table.toml`；DSH 插件选 preset+model，写 DSH settings；不做 DSH-as-harness adapter。
7. **DSH 插件**：若做，做 Freely-host 插件，保留 Freely loop；不加载 `dsh-superagent`；先 spike。

## B1 candidate 状态

| Candidate | 状态 | 下一跳 |
| --- | --- | --- |
| C-A 对比研究+P0 | promoted | 保留 |
| **C-F 讨论入口** | needs_research | 第一优先：issue comment/PR review/CI + 事件准入 |
| C-B ownership/handback | needs_research | 行为盘点 + 真实回放；协议 v0 已有 |
| C-C report/attention/prompt | needs_research | prompt manifest/基线 + patrol 对照 |
| C-D HarnessPort/角色选择 | needs_research | 接口草案 + per-role probe |
| C-E DSH 插件 | needs_research | P0/P1 spike；依赖 B/D/F |

优先级：**C-F → C-B/C → C-D → C-E**。任一 readiness gap 未关闭，不 promote。

## 证据

- 智东西：https://www.zhidx.com/p/606311.html
- IT之家：https://m.ithome.com/html/1020615.htm
- 驱动中国：https://app.qudong.com/article/528135.html
- 原型：https://github.com/deepseek-ai/dsh-superagent-prototype @ 6337fc823ce20251c8de8085948165c81aaa701e
- 原型 `docs/000-008`、`prompts/`、`src/app/{tools,notices,prompts}.ts`、`src/executor/dsh.ts`
- Freely：`agents/*`、`a2a/*`、`task-lifecycle-scan.py`、`platform-adapter.py`、`run-acp-prompt.py`、`agent_working.py`

## 研究 loop

```
研究 → acceptance_criteria 自检 → 缺口 → 回研究
     → promotion_gate → 独立 acceptance review → B2
```
