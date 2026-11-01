---
pre_brainstorm_id: PB-20261101T231000Z
phase_state: completed
topic: Freely vs DeepSeek Super-agent
created_at: 2026-11-01
---

# B1 预研索引：Freely vs Super-agent

> 研究阶段已完成。本阶段不 promote、不写实现；B1 candidate 状态与缺口见 `candidates.md` / `pre-brainstorm-review.md`。

## 一句话结论

**Super-agent 强在“事件 → 准入 → 分派 → 交接 → 注意力”的运行时；Freely 强在“规格 → TDD → 独立评审 → 合并治理 → 多项目”的交付链。** Freely 不应变成 Super-agent，只吸收重叠意图的运行时 primitive。

## 主意图

> Freely 是 LLM 主动、自主、持久、连续的 code harness；scan 监控 issue/讨论/chat；遵循 intent/constitution/laws/gates/tool/skill/MCP；维护规格/测试文档；按 SDD/TDD 持续开发。

按此标准，Freely **意图层优秀、实现层部分不合格**：

- 优秀：角色分工、B1/B2、SDD/TDD 合同、独立 Reviewer、PR/merge gates、worktree、harness probe、多项目 registry。
- 缺口：scan 不监控 issue comment/PR review/CI；A2A task 行/交接丢消息；Reviewer 契约矛盾；MCP 未编排；无独立语义 Watchdog；SDD/TDD 门禁偏后。
- 拖后腿：A2A task 行、scan 只看 body、全局 adapter、无线程 owner。

## 最终文档

| 文档 | 回答什么 |
| --- | --- |
| [overlap-comparison.md](overlap-comparison.md) | 只比重叠意图：概念映射、逐项评审、吸收清单 |
| [intent-alignment.md](intent-alignment.md) | 主意图逐条对齐：优秀/部分/缺口/拖后腿 |
| [concept-map.md](concept-map.md) | Super-agent 全量概念 → Freely 对应物、同名不同义 |
| [delivery-model.md](delivery-model.md) | Freely 交付闭环：B1/B2、SDD/TDD、三角色、3 loop + 2 门禁 |
| [handoff.md](handoff.md) | 交接缺陷 + delegation protocol v0（envelope/ownership/handback） |
| [runtime-contracts.md](runtime-contracts.md) | 状态权威、事件准入、prompt/cache、注意力、可观测、TDD 政策 |
| [harness-strategy.md](harness-strategy.md) | HarnessPort、两种部署形态、DSH A/B1/B2/C 判定 |
| [harness-selection.md](harness-selection.md) | 三角色 UI/CLI/TUI 选择 harness 与配置落点 |
| [dsh-freely-plugin-design.md](dsh-freely-plugin-design.md) | Freely-host 插件详细设计、迁移、验收 |
| [failure-modes.md](failure-modes.md) | 漏单/重复/越权/交接丢失/缓存误判/文档漂移 |
| [pre-brainstorm-review.md](pre-brainstorm-review.md) | 独立评审、readiness matrix、B1 loop |
| [docs-directory-audit.md](docs-directory-audit.md) | 文档目录归位、遗留目录、既有门禁缺陷 |
| [super-agent-freely-overlap.html](super-agent-freely-overlap.html) | 重叠意图与吸收点架构图（SVG 同目录） |

## 关键事实（可复核）

1. **Super-agent 没有独立 Reviewer**：文章里的“代码审查评论”是 Trigger；内部实例是“响应 review”。Reviewer 是 Freely 额外设计。
2. **Freely 的 A2A 是本地 task 表**：`a2a_tasks` 没有 contextId/messageId/artifact 历史；自定义 REST；对外创建即 COMPLETED。
3. **交接确定 bug**：`acp_session_connect` 在 `session/new|fork` 不发送 message；首次 Reviewer/死亡 Worker 反馈会丢。
4. **Reviewer 契约矛盾**：agent 禁止 `a2a-exit`，watchdog 要求 `a2a-exit`，skill 要 JSON verdict。
5. **scan 不监控讨论**：`task-lifecycle-scan.py` 无 comment 处理；`pull_raw_issue` 只写 body；PR review/CI 无入口。
6. **状态是分域真相**：docs/A2A/git/test-gate/平台各有权威；scan 是派生视图，不是权威。
7. **I-* 双解析**：pretests-gate 只认 bullet，pr-merge 只认 YAML；必须双写。
8. **TDD**：GREEN 硬、RED 软；全 not_applicable 只由 skill 约束；历史 431 份 pre-tests 中 327 份有 not_applicable、247 份无 test_command。
9. **cache**：主项目 21 条 `[CACHE]` 全是 estimated、hit/miss=0。
10. **MCP**：ACP 传 `mcpServers: []`；Freely 不编排 MCP。
11. **可观测**：`live-status`/`baseline-status`/`status` 在 agent_working 空时 fail-closed；`fleet-status`/`harness-status` 正常。
12. **多项目**：`~/.freely/projects.tsv` 真实存在；`fleet-status` 是单项目工位视图。
13. **DSH 集成**：不做 adapter；B2 Freely-host 插件保留 Freely loop，DSH 只做 harness；需 spike。

## B1 candidate 状态

| Candidate | 状态 | 下一跳 |
| --- | --- | --- |
| C-A 对比研究+P0 | promoted | 保留 |
| **C-F 讨论入口** | needs_research | **第一优先**：issue comment/PR review/CI + 事件准入 |
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

本目录已合并/删除重复过程稿；保留的是结论、协议、证据与评审记录。
