# 按功能/意图映射到 Freely（初版）

> 原则：不按名字对齐。先写 Super-agent 这个模块**解决什么问题**，再看 Freely 有没有对应问题、现在靠什么、够不够，最后给态度。
>
> 状态：`同构` / `更强` / `部分` / `缺失` / `不同问题` / `不适用`
> 态度：`吸收` / `改造后吸收` / `保持差异` / `暂缓` / `不吸收`

## 0. 总判断

Super-agent 是一个完整系统架构，五个模块互相支撑；不能只挑“事件表”或“ReAct”单点抄。Freely 的主意图是“项目所有者 + SDD/TDD + 独立评审 + 合并治理”，因此：

- **该吸收的是运行时 primitive**：事件准入、Thread/ownership、report/attention、上下文注入、harness 能力。
- **不该整体迁移的是领域模型与部署形态**：Router/Worker 双层的具体实现、云端/BYOM、全双工 ReAct、投机执行、Panel。
- **Freely 已有的强项不能为了“像 Super-agent”削弱**：gates、Reviewer、worktree、B1/B2、PR 治理。

## 1. 意图矩阵

| # | Super-agent 解决的问题 | Super-agent 机制 | Freely 现有机制 | 证据 | 状态 | 设计判断 | 态度 |
|---|---|---|---|---|---|---|---|
| 1 | 人的注意力是瓶颈，一个人只能盯 3–5 个活跃 Session | Router 统一交互 + 多 Worker 隔离并发；用户不必管理 Session | Manager 统一巡检/派工；多 worktree/多 Worker；人通过 chat/intake 介入 | `agents/manager-agent.md`、`wt-create`、多 worktree、`freely chat` | 部分同构 | Freely 的并发单位是 worktree/session，不是单个聊天 Session；更贴合项目交付，但人仍要理解多个工位 | 保持差异，补“一个入口看所有工位”的注意力面 |
| 2 | 跨信道连续性：IM 方案 A、PR 改方案 B，Agent 要接住 | Router 全局上下文 + Thread/Trigger 统一 | docs/DB/worktree 持久；issue/PR 评论入口在 C-F；IM 未接 | `docs/B1.../research/delivery/intake.md`、`discussion_events.py` | 部分 | 文档/工单连续性强；IM 与 PR 评论进入 runtime 的链路未闭环 | 改造后吸收：先接 GitHub 评论/PR review/CI，再谈 IM |
| 3 | 多任务吞吐：单 ReAct Loop 串行，任务互相阻塞 | Router 批处理 + Worker 并发 + 订阅直通 | 多 worktree；Manager 轮询；Worker session 独立；无 Router 批处理 | 多工位、`task-lifecycle-scan.py`、A2A | 部分同构 | 并发模型不同但方向一致；Freely 没有事件级批处理/直通，Manager 可能成为串行点 | 保持差异；用真实 patrol 数据决定是否补批处理 |
| 4 | 主动性：不等指令，持续观察环境事件 | Trigger + 两级过滤 + 订阅直通 | scan 轮询 open issue/body；C-F 事件表/准入；无平台 poller | `task-lifecycle-scan.py`、`discussion_events.py`、`platform-adapter.py` | 部分 | 事件 schema/admission 有；生产入口未接，主动性仍靠 scan 的 body/工位 | 改造后吸收：补 C-F poller，而不是重写 scan |
| 5 | 高噪音/低触发率：不能每个事件都调 LLM | 程序 Fast Path + LLM Slow Path | `discussion_events.admit` 确定性准入；scan 预筛 | `discussion_events.py` | 部分 | admission 规则存在；没有真实事件流验证；Manager prompt 是否消费未闭环 | 吸收：把 admission 接到真实来源 |
| 6 | Thread 后续事件归属：同一 PR/IM 话题不再重新开单 | Thread + Subscription 多对多 fan-out；Worker 直接收后续 | C-B `handoff_store`：task/handoff/message、followup/handback；但 runtime 未调用 | `handoff_store.py`、tests | 部分/未接线 | 领域模型比 Freely 现有 A2A task 更干净；但只在库里，生产 ownership 没生效 | 改造后吸收：接 Manager/Worker 生命周期，不另造事件总线 |
| 7 | 上下文窗口是稀缺资源：注入太多/太少都差 | Inline & Spill + 链式召回（ID 引用图） | 文档/DB 长期存储；prompt manifest 分段/hash；Manager 读 PRD/pre-tests/artifacts | `prompt_manifest.py`、docs、`run-acp-prompt.py` | 部分 | Freely 的长期上下文强，但缺“按需逐跳召回”的统一对象 ID/读取协议；prompt 仍靠人工选文档 | 改造后吸收：先做 artifact 引用/摘要协议，不急着做图数据库 |
| 8 | 经典 ReAct Loop 阻塞：长工具调用时前台不能接新指令 | 异步 ReAct：`start()` 立即返回、后台执行、结果作为新事件投递；`stop()` 取消 | ACP `session/prompt` 一次跑完；`sse-watchdog` 可向 Manager 注入 `session/prompt`；无统一 start/stop/cancel 契约 | `run-acp-prompt.py`、`acp-bridge.py`、`sse-watchdog.sh` | 部分/未证明 | **高层意图 Freely 也在解决**（session/worktree 并发 + Manager 注入），但单 session 内阻塞、改向、取消未闭环 | 暂缓实现；先研究/实验，若需要只补 HarnessPort async job/steer/cancel，不引入 ReAct runtime |
| 9 | 多信道输出：不同信道带宽/习惯不同 | Router 统一对外；IM ≤100 词；GitHub/邮件结构化 | GitHub/Gitee issue/PR 评论；无双层 Router 统一回复；无 IM | `platform-adapter.py`、Manager 文档 | 部分/不同 | GitHub 结构化交付是强项；IM 低打扰、统一语气/长度尚未系统化 | 保持差异；先定义“对外消息契约”，不急着接 IM |
| 10 | 单机离线就停：计算/状态/环境绑定 | 云端无状态 Agent Loop + Session DB + 端侧 daemon（BYOM） | 本地 CLI/daemon + worktree + SQLite；无云端控制面/端侧 daemon 分离 | runtime、worktree、`.freely` DB | 不同问题/不适用 | Freely 当前主意图是本地项目所有者；引入云端控制面会显著增加安全/运维复杂度 | 不吸收（当前）；未来多设备再评估 |
| 11 | 执行环境重、难复制：未提交修改/凭据/内网 | 环境留在原地，端侧轻 daemon 按需执行 | worktree 就在本地；命令在本机执行；无跨设备 | `wt-create`、runtime | 同构（本地） | 本地 worktree 已经满足“环境不复制”；缺的是跨设备/BYOM，不是当前主意图 | 保持差异；不做跨设备 daemon |
| 12 | 持久在线要自愈：进程活着不等于任务有进展 | 外部 Watchdog Session，模型判断 Worker 实质进展/方向 | supervisor heartbeat、`watchdog_sse.py`、continuation watchdog、Loop Guard L0–L3 | runtime watchdog 文档/脚本 | 部分 | Freely 偏进程/SSE/循环检测；缺“语义进展/方向偏离”的独立 Agent 判断 | 改造后吸收：先做语义 watchdog 的只读观察，不直接让它改主系统 |
| 13 | 授权：谁可以发起工作、工作范围多大 | Source Policy + 准入表 + Mandate（版本/范围/强度）| Constitution/Laws/gates/worktree/branch；B1/B2 流程授权；无事件级 Mandate | 治理文档、gates | 不同/部分 | Freely 的项目治理更强；事件级“谁能触发/多大范围”没有统一模型；C-B 的 ownership 也未接 | 保持差异；只吸收事件级准入，不复制 Mandate 全量 |
| 14 | 交接要类型化：六态 report + 单问题 attention，不靠自由文本 | Report/Attention/Decision 结构化 | C-C `agent_protocol` 六态/attention/decisions + `a2a-report`/`a2a-decide`；Manager 文档要求使用 | `agent_protocol.py`、`manager-agent.md` | 部分 | schema/CLI 有；真实 patrol 对照/自动批量路由未证明；pre-tests 还有重复 pending 证据 | 吸收并补真实闭环；不新增平行模型 |
| 15 | 多实例/组织边界：A2A 只在隔离上下文之间发生 | 单实例内共享上下文；跨组织才 A2A | 多 project/多 raw/worktree；A2A 主要是 task 状态，不是跨实例协议 | `a2a_server.py`、`a2a_task.py` | 部分/不同 | Freely 的多项目是隔离的；没有跨实例 Agent 协作协议 | 暂缓；不为了架构图造 A2A |
| 16 | 安全隐私：云端 Agent 接入不可信事件 + 端侧凭据 | 云端信任边界、凭据不进模型、daemon 隔离 | 本地执行、worktree、gates；凭据仍在本地环境；无云端控制面 | 本地 runtime | 不同/部分 | Freely 的本地模型降低了云端入侵面，但 prompt injection/凭据仍存在 | 吸收“不可信输入/凭据不进上下文”的原则，不复制云架构 |
| 17 | 可观测：人要知道“现在需要我什么” | Panel：Overview/Source/Trigger/Eval/Execution/Settings | `live-status`/`fleet-status`/scan/milestones；无 Web Panel | CLI、docs | 部分/不同 | CLI 对开发者够用；对“注意力瓶颈”不如 Panel | 暂缓；先把状态契约稳定，Panel 另立 raw |
| 18 | 用实验证明架构，而不是只讲理念 | 消融 + Router 批处理，合成负载 | 无对应 benchmark；只有单测/gate | tests | 缺失 | Freely 没有多任务调度 benchmark；无法证明“比单 Session 好” | 需要补最小实验，但不套用 300 条消息合成负载 |

## 2. 结论（初版，待原型分析后修正）

**已经解决/更强**：

- 项目生命周期与治理：B1/B2、gates、Reviewer、worktree、PR/merge。
- 长期状态：docs/DB/worktree。
- 多工位并发：session/worktree 级。

**部分解决/未接线**：

- 事件入口（C-F）：schema/admission 有，poller 没有。
- ownership/fanout（C-B）：库有，runtime 没接。
- report/attention（C-C）：CLI/schema 有，真实 patrol 闭环弱。
- harness 角色选择（C-D）：配置/probe 有，HarnessPort 生命周期没有。
- ReAct 全双工：session 级异步有，单 session 内 start/stop/steer/cancel 没有。

**明确不吸收（当前）**：

- 云端无状态 Agent Loop + 端侧 daemon（BYOM）。
- 全双工 ReAct runtime / 投机执行。
- 完整 Mandate/Policy 领域模型。
- Panel/多客户端（先 CLI/文档）。
- 跨实例 A2A。

**需要研究后再决定**：

- Router 批处理/订阅直通是否值得在 Freely 的 Manager/事件层实现（不是照搬 Router）。
- Inline & Spill/链式召回是否值得做成 artifact 引用协议。
- 语义 Watchdog 是否值得做只读观察器。
- 多信道输出契约（GitHub/IM）。
