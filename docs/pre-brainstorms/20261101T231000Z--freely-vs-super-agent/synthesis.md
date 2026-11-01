---
analysis_id: SYN-20261101T231000Z
phase_state: in_progress
topic: Freely vs Super-agent 逐项判定
created_at: 2026-11-01
---

# 逐项判定：问题、方案、谁更优、为什么、代价

> 这张表是预头脑风暴的收敛页。每一行只回答五个问题，不重复架构描述。判定不是“谁更先进”，而是“在这个问题上谁更合适”。

## 0. 先定需求层级

两个系统最终都在服务同一个目标：

> **把人的注意力从“操作 Session/执行任务”上移到“表达意图、做决策、验收结果”；让 agent 在可信边界内自主运行。**

拆成六个子需求：

1. **注意力**：少打扰、打扰得准。
2. **连续性**：跨渠道/跨天/跨任务不丢上下文。
3. **信任**：谁知道能做什么、做到哪、凭什么。
4. **质量**：产出可验证，不是 agent 自证。
5. **恢复**：长跑中死机/卡住/跑偏能回来。
6. **审计与移植**：出了问题能追溯；换模型/CLI 不重写。

## 1. 逐项判定表

| # | 维度 | 解决什么问题 | Super-agent 方案 | Freely 方案 | 判定 | 为什么 | 代价 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 注意力 | 人被打断太多/太少 | 默认沉默；结构化 attention；IM ≤100 词；批量路由 | Manager 主动汇报；scan needs_human；chat/issue/PR 多入口 | **Super-agent 更优** | 有“默认不打扰”的硬约束；Freely 没有消息预算 | Freely 漏报少但噪音风险高；DSH 可能漏掉该报的 |
| 2 | 主动发现 | 人不主动提，agent 能否发现 | 规则+推断候选；observe/auto；投机执行 | scan + 治理漂移 + runtime 异常 + watchdog | **Freely 更广，DSH 更稳** | Freely 覆盖文档/治理/多工位；DSH 的事件级推断更克制 | Freely 误报/噪音；DSH 依赖事件源质量 |
| 3 | 人插话 | 人从熟悉入口补充/纠偏 | IM、GitHub 评论；Thread 订阅；回原会话 | issue/comment、chat、PR review；chat 入 Manager prompt | **分裂** | DSH 归属/直通更顺；Freely 入口多但 PR review 未闭环 | Freely 后续消息可能没人拥有；DSH 渠道接入成本 |
| 4 | 事件准入 | 这条事件凭什么进入/处理 | 代码 gate + 模型 assessment；准入表；机器人过滤 | 无 per-event gate；scan + Manager/B1 判断 | **Super-agent 更优** | 先判后做，噪音不进上下文；Freely 靠模型自律 | Freely 浪费上下文/越权风险；DSH gate 误杀/维护成本 |
| 5 | 授权 | 谁能做什么、做到哪 | Policy 版本 + Mandate（scope/strength）+ 复活重校验 | 宪法/法律 + 角色 + phase + IBM/TDD/PR/merge gates | **分层不同** | 单事件 DSH 强；合并治理 Freely 强 | DSH 不管 merge；Freely 越权只能在 review 发现 |
| 6 | SDD | 做什么、为什么、边界、验收 | 无规格层；Ticket 承载任务 | B1 candidate + B2 I-*/PRD/pre-tests/tasks | **Freely 更优** | 有可审计的规格与验收；DSH 缺这一层 | 文档多、更新慢、易漂移；小任务过重 |
| 7 | TDD | 怎么证明真的做了 | 无 TDD；Worker 自测 + 外部 CI | pre-tests；RED→实现→GREEN；test-pre-merge；pretests gate | **Freely 更优** | 有终态证据门禁；DSH 无强制 | GREEN 硬、RED 软；全 not_applicable 仅 skill 约束；流程重 |
| 8 | 交接 | 阶段之间/后续消息归谁 | Report 六态 + attention + handback + followupOwners + relay key | A2A state + summary/evidence；SSE 广播；Reviewer verdict | **Super-agent 消息级更优** | 有 ownership/幂等/单问题 attention；Freely 只有任务级 | Freely 后续讨论丢失/重复；DSH 模型复杂 |
| 9 | 路由 | 下一步做什么、派给谁 | 代码 gate + 1–20 批量决策 + 逐条拒绝 | scan 推导 stage/next_action + Manager 派工 | **分裂** | DSH 事件吞吐/幂等强；Freely 生命周期 stage 更准 | Freely 无批量/幂等；DSH 不懂 B1/B2/TDD |
| 10 | 上下文 | 跨会话/跨任务不丢 | Inline/Spill + Chain of Recall；每 Ticket 独立 Session | 文档长期记忆 + session resume/fork + worktree | **分裂** | DSH 单会话更精；Freely 跨天/跨项目更久 | DSH 长程记忆未解；Freely prompt 拼接无稳定前缀 |
| 11 | 缓存 | 能否复用前缀、命中多少 | 段序固定、Policy 置尾、revision 绑定；无 cache 指标 | fork/resume；`[CACHE]` 日志；input 常估算 | **都不足** | DSH 有纪律但不可见；Freely 有入口但数据不可信 | DSH 冷启动；Freely 以为命中实际没有 |
| 12 | 并发 | 多任务并行不互相踩 | Worker slot + 人优先槽位 + Thread 共享 | 每 issue worktree + test 工位 + worker pool | **仓库内 DSH 细；跨项目 Freely 广** | DSH 事件级调度细；Freely 环境隔离强 | DSH 单仓；Freely 工位/分支管理成本 |
| 13 | 失败恢复 | 死机/卡住/跑偏能回来 | effect 队列 + 恢复提示 + 未读 Input 重投 + Watchdog（文章） | supervisor/watchdog/continuation + session resume + gate 对账 | **分裂** | DSH 外部副作用强；Freely 进程/工位恢复强 | DSH 原型 watchdog 未落地；Freely 无通用 effect 队列 |
| 14 | 可观测 | 出了事能查 | 单写 DB + health board + panel + Decision/reason | docs 证据 + CLI status + DB + review verdict | **分裂** | DSH 实时性强；Freely 审计性强 | DSH 文档弱；Freely 实时性弱、数据分散 |
| 15 | Harness | 换模型/CLI 是否重写 | 绑定 Cordis/DSH；深度集成；无 ACP | ACP 多 CLI；HarnessPort 方向；契约未显式 | **Freely 更优** | 可替换基座；DSH 换宿主=重写 | Freely 能力差异靠分支兜底；DSH 无 ACP |
| 16 | 规模/移植 | 单仓还是多项目 | 单仓单团队；云端/本地 daemon | 项目 registry + 独立 runtime + 多工位；跨项目调度未产品化 | **Freely 更广但有边界** | Freely 可多项目登记；DSH 单仓更深 | Freely 跨项目视图未成熟；DSH 扩展难 |

## 2. 最佳组合（按需求）

| 需求 | 最佳来源 | 具体借什么 | 不借什么 |
| --- | --- | --- | --- |
| 注意力 | Super-agent | 默认沉默、消息预算、结构化 attention、批量路由 | 不把“默认 observe”照搬到 Freely |
| 连续性 | 两者 | Chain of Recall/Inline-Spill + Freely 文档长期记忆 | 不把文档全塞进 prompt |
| 信任 | 两者 | DSH 运行时 admission + Freely 合并治理 | 不照抄 Mandate 全量 |
| 质量 | Freely | SDD、TDD、阶段 Reviewer、PR 四问、merge gate | 不把 gate 降成提示词 |
| 恢复 | 两者 | DSH effect 队列/恢复提示 + Freely supervisor/watchdog/continuation | 不假设外部 API 幂等 |
| 审计 | Freely | 文档证据链 + phase/milestone | 不把过程文档当 runtime 组件 |
| 移植 | Freely | ACP/HarnessPort | 不把 DSH 当 ACP CLI |

## 3. Freely 的 adopt / adapt / reject

| 判定 | 机制 | 理由 |
| --- | --- | --- |
| **adopt** | 事件准入（权威判断，不是价值判断） | 补 Freely 最弱的运行时边界；但先补平台 actor/event 数据 |
| **adopt** | 消息级 report/attention/ownership/handback | 补后续讨论丢失/重复开单 |
| **adopt** | 路由批处理 + 逐条拒绝 + 幂等键 | Manager 上下文与吞吐的现实解 |
| **adopt** | prompt 稳定前缀/可变尾部 + usage/estimated | 让 cache 可度量、可回归 |
| **adapt** | Thread 订阅直通 | 先做“同一工单线程 ownership”，不做事件总线 |
| **adapt** | Policy 版本 | 记录“依据哪版规则批准”，不做运行时 Mandate |
| **adapt** | DSH adapter | 作为 HarnessPort 的一个实现；不让 DSH 接管 three-loop |
| **adapt** | Freely 工具作为 DSH 插件 | 只外溢 gates/worktree/issue，不起第二套调度 |
| **reject** | 默认 observe / 默认不做 | 与 Freely“项目所有者”目标冲突 |
| **reject** | 单仓/单机假设 | 与多项目 registry 冲突 |
| **reject** | 移除 Reviewer | 削弱质量分离 |
| **reject** | 事件溯源重写 | 治理证据在文档与平台，不在事件流 |
| **reject** | 双 Router/Ticket | 插件化最大陷阱 |

## 4. DSH 可以从 Freely 学的（公平起见）

- SDD 规格层：Ticket 有任务但没有“为什么/怎么验/边界”的文档合同。
- TDD 证据：Worker 自测 + 外部 CI 不足以防 AI 自证。
- 独立 Reviewer：外部 bot 不能替代“不站在任何一方”的审查。
- 合并治理：事件级授权不等于交付治理。
- 多项目登记：DSH 单仓是明确边界，不是缺陷；但如果要扩展，Freely 的 registry 可参考。

## 5. 结论

**在“团队助手的注意力与事件响应”问题上，Super-agent 的方案更合适；在“项目所有者的交付治理”问题上，Freely 的方案更合适。**

Freely 不应变成 Super-agent；应保留 SDD/TDD/Reviewer/gates 四个差异优势，只借 Super-agent 的五个运行时 primitive（admission、report/attention/ownership、批量路由+幂等、稳定前缀+usage、effect 队列/恢复提示）。

## 6. 证据等级

| 结论 | 证据 |
| --- | --- |
| DSH 默认沉默/消息预算/订阅/handback/Mandate | 文章 + 原型 docs/prompts/tests |
| DSH 无独立 Reviewer、无 ACP、单仓 | 原型 docs/README/package |
| Freely B1/B2/Reviewer 阶段/PR 硬门禁 | skills + agents + scripts 代码 |
| Freely phase 多写者/I-* 双解析 | 代码路径 + 实测 |
| cache estimated/hit=0 | 主项目日志实测 |
| scan station/next_action 不一致 | 主项目 scan 实测 |
| 注意力数据不足 | DB 采样（chats=0, reviews 空, input-required 4） |

## 7. 未解

- 事件准入的数据前提（actor/event id）还没补。
- 状态 schema/单写者还没定。
- TDD 分级的 `change_surface` 还没定。
- 注意力指标还没有基线。
- DSH adapter 的宿主所有权还没定。
- 多项目是否产品化还没定。
