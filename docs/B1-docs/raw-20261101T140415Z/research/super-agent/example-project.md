# 示例项目：dsh-superagent-prototype 分析

- 仓库：`https://github.com/deepseek-ai/dsh-superagent-prototype`
- 本地克隆：`/Users/zhaoyu/src/dsh-superagent-prototype`
- commit：`6337fc8 feat: add the dsh-superagent research prototype`
- 性质：research prototype，不是正式产品；README 明确“可能含 bug、工程实践不一致、使用前需审查”，且“文章部分设计是未来方向，原型未实现”。
- 规模：`src` 约 11k 行 TypeScript；9 篇设计文档；大量 vitest 测试；本地 SQLite；DSH bundle + web panel。

## 1. 它到底实现了什么

### 领域模型（不只是 Router/Worker）

`docs/001-domain.md` 定义了比文章更细的领域：

- Source → Trigger → Thread → Eval → Decision → Ticket → Mandate → Assignment → Subscription → Channel → Report/Attention。
- Source 保存读取位置；Trigger 不可变、幂等；Thread 串行 Eval、可多 Ticket；Subscription 多对多 fan-out；Ticket 自己拥有状态，不跟随 Executor Session；Mandate 记录策略版本/范围/强度/来源。
- 这回答了文章只有概念图、没展开的“任务/授权/交接”细节。

### Router 与 Worker

- Main Session（`orchestrator`）负责 eval、accept、dispatch、reply；文档明确“只路由，不做技术决策”，路由 note ≤30 词。
- 每个 Ticket 一个 Executor Session（`worker-<ticket>`）和一个目录；Worker 工具集完整，但不含 `ask_user_question`/`present`/profile 修改等面向人的工具。
- Worker 不直接对外说话；报告经 Main Session relay。
- Worker 内部可用 subagent；背景 shell/job 会保留 worker slot，结束后唤醒。

### 事件/准入

- GitHub：notifications、订阅的 Issue/PR、CI 变化、PR merged/closed；可选 receive-all 新 Issue/PR/comment/default branch CI。
- Feishu：live events、历史恢复、订阅 topic 轮询。
- 两级：程序 gate（Source 的 admission table、白名单、bot 列表、接收范围）+ LLM assessment。
- 有 Policy version、Mandate 重验证、stop/resume、handback、context-only subscription。

### 执行/恢复

- Effects durable queue：assessment/launch/delivery/relay/notice/reply，带重试/退避/幂等。
- Worker slots：并发上限 + 给人消息额外 slot；背景 work 结束唤醒；30 分钟上限。
- Outbox：消息先存后发，按 Ticket/会话保序；失败重试，Source 关/会话消失时等待/丢弃。
- 重启：运行中的 Assignment 以 recovery note 重启；未读消息重投；保留 Session/目录/订阅/DB。
- 失败/blocked/failed：自动 Input 暂停，等人消息/retry；模型/网络 transient 重试。

### 面向人的交互

- 后台 shell 命令 5 秒后转 background，Worker 下一步可接新消息；主 Session 禁止 `sleep`/长 job wait，避免阻塞新候选。
- 这是“异步执行”的一个实现，但**不是完整的 model-level `start()/stop()` ReAct 协议**。
- Web panel：Overview/Source/Trigger/Eval/Execution/Settings；显示需要人的 Ticket、系统问题、24h 活动、Executor 负载。
- 多信道：GitHub 评论/PR review 回复、Feishu topic 回复；IM 100 词限制、GitHub 结构化交付在 prompts 中。

## 2. 文章有、原型没有/只做了一部分的

| 文章模块 | 原型状态 | 证据/边界 |
|---|---|---|
| 云端无状态 Agent Loop + Session DB | **未实现** | 原型是本地 DSH bundle；SQLite 在本地；无云端控制面 |
| 端侧 daemon / BYOM / 跨设备执行环境 | **未实现** | 本地执行；一个 stateDir、一个执行根；无 daemon 协议 |
| 外部独立 Watchdog Session | **未实现** | 只有 health/retry/restart/recovery；没有独立 Watchdog Agent 判断语义进展 |
| 投机执行 | **未实现** | 没有 speculative branch/后台候选丢弃机制；proactive 是 Policy/规则驱动，不是“先做再决定是否交付” |
| 完整异步 ReAct `start()/stop()` | **部分** | shell 命令 5s 后 background、job 结束唤醒、主 Session 不等待；但没有模型级 start/stop 工具契约，subagent 也有独立生命周期 |
| 多实例 A2A | **未实现** | 单实例、单 repo；跨实例 A2A 是开放问题 |
| 安全/凭据隔离 | **未实现/简化** | Worker 以 operator OS 用户跑；CLI wrapper 只是默认不是安全边界；凭据仍可能进环境 |
| 长期记忆/链式召回跨月 | **部分** | SQLite + Thread/Trigger 记录；没有文章式统一 ID 引用图/链式召回；有界上下文窗口 |
| Panel | **实现** | 比文章描述更完整（6 tabs、settings/prompts/history/search） |

## 3. 文章没有、原型额外做的

- 详细 Mandate/Policy/Admission 领域模型与版本化。
- Source kind 插件协议（`SourceKind`/`SourceRegistry`/`SourceContext`）。
- Effects/Outbox 持久队列、重试/幂等/保序。
- Settings/Prompts 版本化、覆盖/回滚、模板占位符校验。
- Web panel 和 management API。
- 单元/集成/面板测试、模拟 DSH host。
- Worker slots、background jobs/subagents、recovery note。
- 这些是“示例项目额外的东西”，不应全部搬进 Freely；它们是 DSH host 的实现细节。

## 4. 对 Freely 的启示（先不 decision）

### 可学

- **Ticket 与 Assignment 分离**：Ticket 拥有状态，Assignment 只是执行绑定；Freely 的 A2A task 目前压得太扁。
- **Subscription fan-out + ownership**：后续消息直接到 owner，跨范围 handback 一次；这正是 C-B 想做的。
- **Report/Attention 结构化**：六态 + 单问题 + 目标角色，不靠 summary 自由文本。
- **Outbox/Effects 持久化**：外部副作用先存后做，重试/保序；Freely 的 issue-sync/PR 操作可借鉴。
- **Worker slot + background job**：长命令不阻塞下一步；但 Freely 的 harness 是否支持要单独验证。
- **Panel 的“现在需要我什么”**：Freely 的 live-status 可以做成类似聚合，但不必先做 Web UI。

### 不能直接学

- 单 repo/单实例假设、云端/BYOM、完整 Mandate、Panel 全量、DSH 专属 services。
- 完整的 11k 行 TS 领域实现不应复制到 Freely Python runtime；应按 Freely 的 docs/gates/worktree 重新表达。

## 5. 对“示例项目不完善/有额外东西”的判断

- **不完善**：文章的五模块中，云端/daemon/Watchdog/投机/A2A/安全都未实现或简化；单 repo、本地、单实例。
- **额外**：领域模型、Policy/Mandate、Effects/Outbox、Panel、Prompts 版本化，比文章多。
- **仍然有价值**：它把“事件→准入→授权→Ticket→Assignment→Report→Channel”跑成了可测试的完整纵切；比文章的概念图更能指导 Freely 的 C-B/C-C。
- **风险**：不要把“原型有”当成“文章架构已证明”；也不要把“文章有”当成“原型已实现”。
