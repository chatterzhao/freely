---
analysis_id: ART-20261101T231000Z
phase_state: in_progress
topic: IT之家 Super-agent 解读与 Freely 概念映射
created_at: 2026-11-01
source: https://m.ithome.com/html/1020615.htm
prototype: https://github.com/deepseek-ai/dsh-superagent-prototype @ 6337fc823ce20251c8de8085948165c81aaa701e
---

# 先把文章读准：Router/Worker/Reviewer 不是一一对应

## 0. 文章说了什么

IT之家 2026-10-31 的解读把 DeepSeek Harness 的 Super-agent 归纳为：

**四项特征**：

1. 连续：IM、GitHub 评论等不同渠道，与同一个 agent 交互。
2. 高效：并行处理多个复杂任务。
3. 主动：持续观察环境事件，自行推进值得处理的事项。
4. 持久：始终在线，长期运行中能从异常恢复。

**五个组成部分**：

1. 双层架构：Router 承接人类交互、维护全局上下文、分派任务；Worker 隔离并发执行；Worker 不直接回复用户。
2. 事件驱动：群聊、邮件/日程、代码审查评论、CI 结果都是 Trigger；先程序规则过滤，再模型判断；已分配任务的 Thread 可让 Worker 订阅，后续事件直达 Worker。
3. 面向人的交互：异步 ReAct（start/stop，未默认开启）、投机执行、Inline & Spill、Chain of Recall。
4. 计算/状态/环境分离：计算与状态在云端，执行环境可在本地 daemon，支持 BYOM。
5. Watchdog：独立 Session，监控基础设施、Worker 进展/方向，异常时介入。

**实验**：约 300 条消息、20 条工作请求、5 次重复；Super-agent p50 12.4 分钟、p95 15.7 分钟；单 Session 中性提示 p95 29.5 分钟。合成负载，只评估调度/协作，不评估单任务执行能力。

**待解**：Router 扩展、跨月记忆、脱离 Session 的人机协作、A2A、安全隐私（提示词注入、端侧凭据、跨设备权限）。

## 1. 用户给的映射，哪些成立、哪些不成立

| 用户映射 | 成立度 | 说明 |
| --- | --- | --- |
| Router ≈ Manager | **部分成立** | 都承接人、维护全局上下文、分派任务。但 Freely Manager 还负责巡检、建 raw issue/工位、收口、治理；Router 不做实现，也不管 merge。Manager 的职责更宽。 |
| Worker ≈ Worker | **基本成立** | 都是隔离执行。区别：DSH Worker 只做任务；Freely Worker 要按 B1/B2/SDD/TDD 文档走完实现、测试、PR。 |
| Reviewer ≈ Reviewer | **不成立** | 文章没有 Reviewer 角色。“代码审查评论”是 Trigger；内部实例是“响应 code review”，不是独立 Reviewer。Freely 的 Reviewer 是额外设计。 |
| 事件 ≈ scan/issue/comment/chat | **部分成立** | DSH Trigger 是事件级；issue/comment/chat 是事件来源；scan 是批量派生，不是事件本身。Freely 没有 Trigger 对象。 |
| Watchdog ≈ watchdog | **意图成立** | 文章是外部 Watchdog Session；原型未实现。Freely 有 supervisor/watchdog/continuation，机制不同但意图相近。 |

**最重要的纠正**：不要把“Super-agent 有 Reviewer”当成事实。它没有独立审查角色；它的“review”是外部评论/CI 事件，以及 Worker 自审 + 外部 bot。Freely 的独立 Reviewer 是差异优势，不是对应关系。

## 2. 四特征与 Freely 的对应

| 特征 | Super-agent 机制 | Freely 机制 | 差异 |
| --- | --- | --- | --- |
| 连续 | IM/GitHub 同一 agent；Thread 订阅 | 文档跨会话；chat/issue/PR 入口；session resume | DSH 跨渠道更顺；Freely 跨会话更久 |
| 高效 | 多 Worker 并发；Router 批处理 | worktree 隔离；worker pool；test lane | DSH 单仓事件吞吐更强；Freely 交付链更重 |
| 主动 | 观察事件；observe/auto；投机执行 | scan + watchdog + 治理漂移 | DSH 更克制；Freely 更广 |
| 持久 | 云端状态 + 本地 daemon；Watchdog | supervisor/watchdog/continuation；本地 worktree | DSH 面向云端/多设备；Freely 面向本地多项目 |

## 3. 核心需求/痛点，而不是机制清单

从文章和 Freely 的共同目标里，能抽出六个真实痛点：

1. **人的注意力不够**：一个人只能同时跟 3-5 个活跃 Session；等待和上下文切换是主要成本。
2. **上下文会断**：跨渠道、跨任务、跨天，Session 一换就丢。
3. **信任/授权不足**：agent 能做什么、做到哪、凭谁授权，必须可判定。
4. **质量不可控**：AI 写代码容易自证；需要独立验证，不是“跑一下”。
5. **失败不可恢复**：长跑系统会死、会卡、会跑偏；需要外部 watchdog/恢复。
6. **不可审计/不可移植**：出了问题要能追溯；换模型/换 CLI 不能重写。

两个系统的取舍：

- DSH 把 1/2/3/5 做成**运行时事实**：Trigger、Thread、Mandate、Watchdog、单写 DB。
- Freely 把 2/4/6 做成**文档与门禁事实**：B1/B2、SDD、TDD、Reviewer、PR/merge gates。
- 两者都不完整：DSH 缺 4/6；Freely 缺 1/3 的运行时硬边界。

## 4. 最佳组合（按需求，不按阵营）

| 需求 | 最佳来源 | 具体借什么 |
| --- | --- | --- |
| 注意力 | Super-agent | 默认沉默、消息长度预算、结构化 attention、批量路由 |
| 上下文连续 | 两者 | DSH 的 Chain of Recall/Inline-Spill + Freely 的文档长期记忆 |
| 授权 | Super-agent 的运行时 + Freely 的合并治理 | admission + 记录；不照抄 Mandate 全量 |
| 质量 | Freely | SDD 规格、TDD 证据、独立 Reviewer、PR/merge gate |
| 失败恢复 | 两者 | DSH effect 队列/恢复提示 + Freely supervisor/watchdog/continuation |
| 可审计 | Freely | 文档证据链 + phase/milestone |
| 可移植 | Freely | ACP/HarnessPort；DSH 的深度只做工具插件 |

## 5. 文章没回答、Freely 必须自己回答的

1. **Reviewer 从哪来？** DSH 没有；Freely 有，但 review gate 依赖 agent 身份，手工工位会 fail-closed。
2. **B1/B2 的规格由谁保证不漂移？** 文章没有文档层；Freely 有，但 phase 多写者、I-* 双解析。
3. **事件准入放在哪？** DSH 在 gate；Freely 目前没有，需要补 admission。
4. **消息级 ownership 怎么做？** DSH 有 followupOwners/handback；Freely 没有。
5. **TDD 的 RED 是否硬？** Freely 的 GREEN 硬，RED 主要是 skill。
6. **多项目是否真需求？** DSH 单仓；Freely 有 registry，但跨项目调度未产品化。

## 6. 结论

文章的核心不是“Router/Worker 两层”本身，而是：

> 把人的注意力从“操作 Session”上移到“表达意图/验收结果”，让系统用事件、授权、上下文和 Watchdog 自己维持运行。

Freely 的核心不是“多 agent 编排”，而是：

> 把“做什么、怎么验、凭什么合并”变成可审计的规格与证据，让 Manager/Worker/Reviewer 按文档闭环。

两者解决的是同一组痛点里的不同段：DSH 强在“事件到执行”，Freely 强在“规格到合并”。最佳方案不是选边，而是把 DSH 的运行时协作 primitive 嵌进 Freely 的交付治理链。
