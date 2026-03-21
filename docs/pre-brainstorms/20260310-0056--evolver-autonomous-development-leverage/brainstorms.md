# 研究：Evolver 对 Freely 自治开发闭环的促进与成本边界

## Context

- 日期：2026-03-10 00:56 UTC
- 触发：评估 `https://github.com/EvoMap/evolver/releases` 与 `https://github.com/EvoMap/evolver` 对 Freely 的实际价值，不再停留在泛泛的“生态接入”讨论，而是回答：
  - `evolver` 现在到底具备哪些能力
  - 它如何促进 Freely 作为“自治软件项目开发应用”的主流程
  - 接入是否会引入新增费用
- Freely 当前产品目标不是“又一个 agent runner”，而是一个 AI 作为项目所有者、能从意图一路推进到文档、开发、验证、恢复的自治闭环应用。
- 因此本次判断标准不是“能不能接”，而是“接入后是否直接增强 Freely 的主人能力、自治稳定性、经验沉淀与多轮运行质量”。

## 外部调研摘要

基于 2026-03-10 可见的 `EvoMap/evolver` README 与 releases，可确认的能力集中在以下几类：

### 1. 受控自我演化

- 使用 `signal -> mutation -> review -> solidify` 的演化路径，而不是直接把失败转成无约束改写。
- 把 prompt、策略、配置、资产视为可演化对象。
- 支持人工 review 后批准或拒绝演化结果。

### 2. 失败治理与安全回退

- 最近 releases 强调 rollback safety mode、失败处理、自动 GitHub issue 上报。
- 说明它不仅尝试改进，还关心失败后的留痕、回滚和再进入下一轮。

### 3. 多 worker / Hub 协作

- 最近 releases 强调 worker pool、poll-based heartbeat、atomic claim/complete、commitment/deadline tracking。
- 说明它在“多个自治 worker 领取任务、跟踪存活、避免任务失效”方面已有较明确的运行模型。

### 4. 资产化经验沉淀

- README 把 Gene / Capsule / protocol 作为一等概念。
- 这意味着它倾向于把“有效做法”沉淀成可复用资产，而不是仅保留在单次运行日志中。

## 对 Freely 主流程的直接促进点

Freely 的核心闭环是：

```text
项目意图 / chat / issue / test / review
-> 路由
-> 文档收敛
-> 开发实现
-> 验证
-> 恢复 / 下一轮
```

`evolver` 对这个闭环最可能产生收益的不是“替代编排器”，而是增强以下四个能力面。

### A. 让 Freely 具备系统化自我修正能力

Freely 现在强调自治与恢复，但“能继续跑”不等于“会持续变强”。

`evolver` 可以服务于这些反复出现的问题模式：

- 某类 issue 经常路由错误
- 某类恢复策略总是失败
- 某些 prompt 或 skill 容易触发分支/治理违规
- 某些代码改动套路经常引入回归

若把这些失败信号交给 `evolver` 类能力处理，Freely 不只是继续循环，而是更有机会减少重复犯错。

### B. 把运行经验从日志升级为资产

Freely 的长期价值不只是“把当次 issue 做完”，而是“让之后同类项目更快、更稳”。

`evolver` 的资产化思路可以映射到 Freely 的现有对象：

| Freely 对象 | 可演化/沉淀方向 |
|------------|----------------|
| routing 提示词 | 哪类来源应进入 pre-brainstorm / IBM / dev-loop |
| recovery 策略 | 哪类中断更适合 resume / restart / bridge |
| review 检查项 | 哪些变更最容易引发治理或质量问题 |
| skill 提示模板 | 哪种表述能更稳定地产出合规结果 |
| 验证套路 | 哪类改动最低成本的验证组合最有效 |

这类沉淀更接近“主人经验”，而不是一次性执行痕迹。

### C. 给自治开发加一道受控闸门

Freely 的目标是 AI 当项目主人，这天然带来高风险：

- 改 prompt 可能破坏治理
- 改核心 skill 可能破坏路由
- 改恢复逻辑可能让 supervisor 变得不可信

`evolver` 的 review / solidify / rollback 思路适合放在这些位置：

- 修改治理相关 prompt 前
- 修改核心 skill 前
- 采用新的自治策略前
- 推广一条“从历史中学来的经验”到多个项目之前

这使 Freely 的自治更像“带刹车的主人”，而不是裸奔式主人。

### D. 为未来多 agent 协作预留经验

Freely 中长期很可能出现分工化 agent：

- lead / route agent
- doc agent
- dev agent
- review / recovery agent

`evolver` 在 worker pool、heartbeat、claim、deadline 跟踪上的经验，对 Freely 的团队化自治具有参考价值。短期不一定直接复用实现，但中长期在运行模型上是同方向的。

## 不能夸大的地方

以下收益不能被误判：

### 1. 它不是 Freely 主编排器的直接替代

- `evolver` 更像演化层、自优化层、经验资产层。
- Freely 的核心仍然是 issue/doc/dev/recovery 闭环与治理执行。

### 2. 它不直接替代 Freely 的技术栈

- Freely 宪法要求核心运行时/编排器/监控/恢复用 Rust，桌面外壳用 Tauri。
- `evolver` 的可见使用方式偏 Node.js / CLI / Hub 网络。
- 因此更适合 sidecar 或 optional subagent，而不是主 runtime。

### 3. 它不自动解决“从意图到项目交付”

- `evolver` 擅长受控演化，不擅长替 Freely 完整定义自治软件工程闭环。
- 所以它能增强 Freely 的主人能力，但不是代替 Freely 当主人。

## 成本与费用边界

### 本地接入成本

本地把 `evolver` 作为 sidecar 使用时，主要成本来自：

- 新增 Node.js 运行依赖
- 新增与 Rust 主运行时的桥接复杂度
- 额外的治理门禁与审计路径设计
- 使用外部 LLM 时的 token 成本

结论：
- 本地接入不一定引入平台订阅费
- 但几乎一定引入工程复杂度和模型调用成本

### 网络接入成本

公开页面能确认 EvoMap 网络存在 `credits` 概念，并有初始 credits、任务取消可节省 credits、账户 credits 展示等提示。

保守判断：

- 若只是本地运行 `evolver`，主要承担自己的模型调用成本
- 若接入 EvoMap Hub / 网络协作，除模型成本外，可能还会受到 credits 或配额体系影响

当前未确认的信息：

- 未找到明确公开价格表
- 未确认 credits 单价、免费额度和超额计费模型

因此在没有进一步费用确认前，不应把网络接入视为零成本能力。

## 当前建议

### 建议一：只考虑本地 sidecar，不考虑核心替换

推荐把 `evolver` 放在 Freely 的“自治优化层”，而不是主循环核心中。

适合托管的对象：

- routing prompt / policy 优化
- recovery 策略优化
- review 检查项优化
- skill 提示模板优化

不建议由它直接接管的对象：

- 主 supervisor
- 主 issue 路由器
- 主状态机
- Freely 的 Rust/Tauri 核心 runtime

### 建议二：先不接 Hub

在 Freely 单机自治闭环还未稳定前，不应急于增加外部网络依赖。

原因：

- 先解决本地主人能力是否可信
- 避免同时引入外部 credits / quota / heartbeat 语义
- 减少架构边界混乱

### 建议三：把它定位成“经验固化子代理”

最合理的 day-1 定位是：

```text
Freely 主循环
  -> 发现重复失败/低质量模式
  -> 交给 evolver sidecar 分析与提出 mutation
  -> 经过 review / validation
  -> 若通过，再固化为新 prompt / policy / skill hint
```

这与 Freely 的治理取向更一致，也更容易做成可审计闭环。

## 结论

对于 Freely 这类“AI 当项目主人、自主开发软件项目”的应用，`evolver` 的最大价值不是帮它多跑一次任务，而是帮助它：

1. 从失败中提炼出可复用的主人经验
2. 让自治策略进入 review / rollback / solidify 的受控流程
3. 为多轮运行提供持续优化能力
4. 为未来多 agent 协作提供参考模型

当前阶段的最优策略不是“全面接入”，而是：

- 本地、可选、默认关闭
- 只承担自治优化层职责
- 不接管主 runtime
- 不提前绑定 Hub 计费/credits 模型

## Follow-up questions

- Freely 是否需要一个正式的“strategy asset”模型，用于保存被验证过的 routing / recovery / review 经验？
- Freely 是否应定义一个 `evolution review gate`，专门处理高风险策略变更？
- Freely 是否需要先在不依赖外部网络的前提下，完成单机自我优化闭环的原型验证？
