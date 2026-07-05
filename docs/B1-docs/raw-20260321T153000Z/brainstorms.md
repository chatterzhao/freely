# 20260321-1530 AI 时代的 Agent-Ready PRD 研究

## 背景

用户提供了两篇微信公众号文章和一篇 Anthropic 官方文章，希望判断：

1. 在 Freely 的流程里，`B` 过程是否就是“产出 PRD”
2. 如果由 AI 来生成和消费 PRD，那么 PRD 在 AI 时代应当长成什么样
3. 如何用 Freely 的 `pre-brainstorm -> IBM -> dev-loop` 方法把这件事落盘

## 研究问题

### Q1. `B` 过程是否单独生产 PRD？

结论：不是。

在 Freely 里，chat 输入属于 `discovery`，必须先进入 `pre-brainstorm`。只有当 candidate 被 milestone 接纳、`epic-name / story-name / issue-name` 稳定后，才进入 `IBM`。

而在 `IBM` 中：

- `I` 负责冻结 issue scope、acceptance 与边界
- `B` 负责 issue-bound brainstorm，收敛设计分歧、方案和 reroute 判断
- `IBM` doc-loop 的整体输出才是：
  - issue
  - `brainstorms/b-*.md`
  - `prd.md`
  - `pre-tests.md`
  - `tasks.md`

所以，`B` 不是脱离 issue 独立生产 PRD；是 `IBM` 整体共同把 PRD 收敛出来。

## 外部证据

### Source A

- title: 面向Agent的PRD架构：从“人类可读 PRD”到“Agent 可编译 PRD”
- url: https://mp.weixin.qq.com/s/40wtEu3tWlbUEPVxNGWbIg
- fetch_method: `skill:url-content-intake`
- fetch_date: 2026-03-21

关键信号：

- PRD 不再只是“给人看的说明文”，而是要能被 Agent 稳定拆解、理解、执行、验证
- 好的 Agent-ready PRD 要满足：
  - 边界清晰
  - 低耦合
  - 可验证
  - 可编译
- 文中把 PRD 定义成“领域树 / 分解树”，强调从业务目标逐级收敛到原子、自包含、跨度可控的任务单元

### Source B

- title: Anthropic 产品经理：PRD 已死，原型万岁
- url: https://mp.weixin.qq.com/s/PE6E7Wos8Yi2e9t4k_Sqhg
- fetch_method: `skill:url-content-intake`
- fetch_date: 2026-03-21

关键信号：

- 文章是对 Anthropic `Product management on the AI exponential` 的中文解读
- 它强调 PM 产物的重心正在从“文档交付”转向：
  - 可运行原型
  - 可衡量 eval
- 它进一步指出：在 AI 时代，真正稀缺的不是“能不能做”，而是“该不该做、先做哪个”

### Source C

- title: Product management on the AI exponential
- url: https://claude.com/blog/product-management-on-the-ai-exponential
- source_date: March 19, 2026

关键信号：

- 传统 PM 默认“项目开始时的技术边界，到结束时基本不变”，但指数级进步的模型打破了这个前提
- 新节奏不是长路线图 + 文档交接，而是：
  - short sprints
  - side quests
  - demos over docs
  - evals over vague confidence
- 文章明确建议：写完 spec 后，把 spec 发给 Claude Code，看它能不能直接做出原型
- 每次模型升级都应重新审视既有功能和 workaround，PRD 不应把旧模型时代的补丁固化成永久结构

## 对 Freely 的判断

### 1. 现在很多 `prd.md` 还更像“人类摘要”，不是“Agent 控制面”

当前仓库中的许多 `prd.md` 很短，往往只包含：

- Goal
- Product Surface

这对于人类回忆上下文够用，但对 AI 来说信息仍然过稀：

- 缺非目标与禁区
- 缺可执行的任务拆分
- 缺原型路径
- 缺 eval / failure mode
- 缺模型升级后要重跑什么判断

### 2. AI 时代的 PRD 应从“说明文”升级为“可编译执行包”

对 Freely 来说，PRD 的主要消费者不只是人，而是：

- doc-loop 内继续收敛的 AI
- dev-loop 中切任务的 AI
- review / recovery / handoff 时重新读取上下文的 AI

因此 PRD 必须至少提供：

1. `Outcome`
- 这轮真正想让产品发生什么变化

2. `Non-negotiables`
- 哪些边界、约束、治理规则不能被 AI 为了“做出来”而擅自突破

3. `Context Pack`
- 必要输入、事实来源、证据链接、已有实现、已有限制

4. `Decomposition Tree`
- 把目标拆成子问题、子域、子任务，直到能进入 dev-loop

5. `Prototype Path`
- 在写大量实现前，最小演示或最小可验证原型是什么

6. `Eval Plan`
- 成功、失败、退化、不可接受行为分别如何判定

7. `Execution Slices`
- 哪些 slice 可以独立实现、独立验证、独立回写

8. `Revisit Triggers`
- 哪些外部变化出现时必须回头重写或重跑 PRD 判断
  - 新模型
  - 新工具
  - 新用户行为
  - workaround 已不再必要

### 3. Freely 的 PRD 不应追求“大而全”，而应追求“AI 可继续工作”

从 Anthropic 的经验看，AI 时代不是文档越厚越好，而是：

- 信息密度高
- 决策边界清楚
- 能直接拿去做 prototype / eval
- 能把失败回流到 issue，而不是让 AI 自由发挥

所以 Freely 下的 PRD 更像：

- 一份可执行 contract
- 一张任务/验证地图
- 一份给后续 agent 的上下文压缩包

而不是传统意义上的“大需求文档”。

## 对 IBM 产物边界的建议

### Issue

冻结这轮到底要解决什么，以及不解决什么。

### B-issue brainstorm

记录为什么这么拆、有哪些外部证据、有哪些备选结构、为什么当前选择是最小闭环。

### PRD

把“该做什么”写成 agent-ready 的执行控制面。

### Pre-tests

在写代码前先约束最小验证门，防止 AI 一路写到偏航。

### Tasks

把 PRD 中的执行切片进一步变成可排序的工作清单。

## 结论

如果用 Freely 流程来做，AI 时代的 PRD 应该被定义为：

> 一个给 AI 使用的、可编译的执行控制面，而不是只给人阅读的交接文档。

它的最小结构应至少覆盖：

- outcome
- non-goals / non-negotiables
- context pack
- decomposition tree
- prototype path
- eval plan
- execution slices
- revisit triggers

## 决定

本轮判断已足够稳定，可以 materialize 为 milestone-owned IBM issue：

- epic-name: `ai-native-doc-loop`
- story-name: `agent-ready-prd-for-freely-flow`
- issue-name: `agent-ready-prd-for-freely-flow`

下一跳：

- 将本研究转成正式 issue-bound IBM 文档
- 在 `prd.md` 中给出 Freely 使用的 AI-ready PRD 结构
