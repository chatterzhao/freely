# 前序研究对账（predecessor reconciliation）

> 目的：把 `raw-20261101T031502Z`（第一轮，已 absorbed）的六条 candidate 与本轮证据逐条对齐，避免重复立项，也避免把“已交付”与“未接线”混为一谈。
>
> 证据口径：`031502Z` 的 B1/B2 文档 + develop 代码现状（`ceaa8c1f2`）。

## 1. 两轮研究的关系

| 维度 | 第一轮 `031502Z` | 本轮 `140415Z` |
|---|---|---|
| 来源 | 未获取原文，依赖智东西/IT之家/驱动中国三篇二手报道 | 抓取并归档原文（`source.html`）+ 15 张图 + 逐节笔记 |
| 原型 | 只做静态阅读，未运行仓库 | 读 `docs/000-008` + `prompts/` + `src/`，逐条核对实现 |
| 产物 | brainstorms/candidates（A–F）+ `comparison/concept-map.md` + `assets/super-agent-freely-overlap.html` | 原文归档 + 意图矩阵 + 本对账 + 两张运行层图（架构 / 目标交接回路） |
| 定位 | 概念层对照 + 方向立项 | 实现层对照 + 交接缺陷定位 + P0 修复候选 |

第一轮不是“错”，是**来源不足且停在概念层**；本轮不是“重复”，是**补证据并把结论落到运行时**。两者是继承关系，不是替代关系。

## 2. 六条 candidate 的对账

| Candidate | 第一轮承诺 | 实际交付 | 本轮判定 | 证据 |
|---|---|---|---|---|
| `C-A` 对比研究 + P0 `harness-status` | 七维对比、概念全量对照、重叠图、五条后续 candidate | 文档与重叠图已交付；`harness-status` 已落地 | **成立**（概念层）；**不足**（未用原文，未运行原型） | `research/comparison/*`、`assets/super-agent-freely-overlap.html`、decision note 自述“原文未直接获取” |
| `C-B` follow-up ownership 与 handback | 五类后续消息 owner 判定、handback 一次、runtime 行为符合协议 | 三张 append-only 表 + `agent_working` 首条 message 修复；**无 runtime 调用方** | **部分交付**：协议只在库里 | `handoff_store.py` 仅被 tests 引用；B2 PRD 非目标写“最小接线” |
| `C-C` report/attention + prompt 前缀 | 六态 report、单问题 attention、批量决策、真实 patrol 对照 | `agent_protocol.py` + `a2a-report`/`a2a-decide` + manifest | **部分交付**：schema/CLI 有，真实 patrol 对照与自动批量路由未证 | `agent_protocol.py`；Manager 文档要求使用但无强制 |
| `C-D` HarnessPort 与角色级 harness | 统一 HarnessPort 生命周期 + 三角色 probe | `harness_select.py` / `harness_status.py` + `agent-table` slot | **部分交付**：选择器与 probe 有，session 生命周期契约未统一 | `harness_select.py`、`run-acp-prompt.py` |
| `C-E` DSH 插件 | 另立 | `dropped`，转入 `120027Z`/`124657Z` | **已由邻线承接** | `dsh-plugin/freely-host/` |
| `C-F` 讨论入口（comment/review/CI） | 评论/评审/CI 进入 scan 或事件流 | `discussion_events.py`（normalize/admit/store）+ scan `collect()`；**无生产 writer** | **部分交付**：schema 与准入有，入口未接 | `discussion_events.collect()` 读 `.freely/run/discussion-events.json`，无写入方；`platform-adapter` 三个 list 方法零调用 |

## 3. 结论

1. 第一轮的六条 candidate **没有一条需要重开**；需要的是把 `C-B/C-C/C-F` 从“库/schema”推进到“生命周期”，这正是本轮 P0 的由来。
2. 本轮新增两条第一轮完全没有的判断：
   - **席位与工作身份混用**（`worker_01..10` 是凭证槽，却被当作 raw 的 owner），导致绑定漂移；
   - **投递层没有队列**（写库 + 内存 SSE，不重放），所以“补 poller”并不能解决交接丢失。
3. 因此本轮不再产出“再研究一遍”的 candidate，只产出**运行时修复**与**后续协议**两类候选。
