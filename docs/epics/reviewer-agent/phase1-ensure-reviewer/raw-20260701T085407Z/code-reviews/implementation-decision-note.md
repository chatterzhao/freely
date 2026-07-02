# Implementation Decision Note: A2A Reviewer Agent

- issue_id: I-20260701T085407Z-A

## Implementation Decision Note

- decision: 基于 ACP session/fork + A2A SSE 事件驱动架构，实现三角色(Manager/Worker/Reviewer)的session复用和消息投递系统。ACP session/fork from Manager 作为默认路径继承治理上下文（~80%缓存命中），session/resume+prompt 作为同阶段多轮审查的消息投递机制。agent_working SQLite表替代 agent-id.env，通过 raw_key 主键实现 UPSERT(Worker) + UPDATE_ONLY(Reviewer) 的写入约束。

- why_this: ACP session/fork 是业界验证的模式（Claude Code、Qwen Code均使用），继承Manager的CONSTITUTION/LAWS/代码库上下文但不继承Worker的实现偏见。A2A SSE推送是Agent-to-Agent协议的标准通知机制，避免轮询开销。SQLite单表设计比agent-id.env文件更可靠（事务、索引、并发安全）。

- alternatives_considered: (1) fork from Worker — 否决：会继承Worker的实现思路导致自我审查偏见。(2) 每次都session/new — 否决：6次冷启动浪费~80% token。(3) Postgres替代SQLite — 否决：增加运维复杂度，当前规模SQLite足够。(4) 轮询替代SSE — 已作为fallback保留（freely-cycle），主路径用SSE。

- boundary_non_goals: (1) 不实现分布式session存储。(2) 不替换ACP bridge的idle timeout逻辑。(3) 不修改claude-agent-acp的协议层。(4) 不改变现有的IBM Framework四节点链路（raw→candidate→milestone→I-*）。(5) Agent间消息不经过Runtime mediator——走A2A直连。

- residual_risk: (1) `__manager__`首次自举依赖_handle_needs_manager触发——daemon启动到首个needs-manager事件之间的窗口期fork不可用。(2) 多reviewer逗号分隔格式依赖写入串行保证——并发写入可能覆盖。(3) test_worktree/test_branch字段当前未填充——僵死检测的worktree定位不完整。(4) Real-environment集成测试未覆盖——依赖post-merge dogfood。
