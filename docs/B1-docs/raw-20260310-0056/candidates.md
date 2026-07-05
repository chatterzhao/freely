# Candidates - 20260310-0056--evolver-autonomous-development-leverage

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260310-0056-A: legacy issue
- title: Evolver Sidecar for Freely Strategy Evolution
- problem: Freely 目前强调自治执行与恢复，但还缺少一个受控、自我修正、可审计的“策略进化层”，难以系统性减少重复错误。
- why_now: 随着 Freely 把 AI 定位为项目主人，routing / recovery / review / skill prompt 的质量会直接决定自治开发是否稳定。若没有经验固化机制，Freely 容易停留在“能继续跑，但不一定越跑越强”。
- acceptance_hint: 把 `evolver` 明确定位为本地可选 sidecar；只负责分析失败信号并提出 routing / recovery / review / skill hint 的 mutation；变更必须经过 review / validation / rollback gate；默认关闭，不接管主 runtime。
- priority: P1
- status: needs_research
- decision_reason: 与 Freely 的治理取向一致，能增强主人能力，但不应破坏 Rust/Tauri 主架构或过早引入外部网络依赖。
- next_action: 继续收敛 sidecar 的最小职责边界与验证门，优先判断是否需要在本地自治优化层落地，而不是扩展为主 runtime 或 Hub 依赖。
- revisit_trigger: 当 Freely 需要系统性减少重复失败、且已有明确可审计的策略进化输入输出时，再推进到 IBM materialization。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260310-0056-A
- session_refs:
  - tool: codex
  - session_id: unavailable://chat-session
  - jsonl_path: unavailable://codex-cli-session-jsonl-not-exposed
  - role: researcher

### C-20260310-0056-A: legacy issue
- title: Delay EvoMap Hub Integration Until Single-Node Autonomy Is Stable
- problem: 若在 Freely 单机自治闭环尚未稳定前就接入 EvoMap Hub / worker 网络，会同时引入 credits、heartbeat、claim、deadline 等外部语义，放大系统复杂度与成本不确定性。
- why_now: 这类网络能力看起来诱人，但若过早接入，容易把“主人能力未稳”与“外部协作复杂度”混在一起，导致收益难以归因、成本难以控制。
- acceptance_hint: 在单机自我优化原型、review gate 和本地策略资产模型成形前，不进入 Hub 集成实现；仅保留为后续研究方向，并补充费用确认。
- priority: P1
- status: proposed
- next_action: 调研 evolver 自主开发能力的利用方式
- revisit_trigger: 当有新的 evolver 集成需求时
- decision_reason: 先把本地自治质量跑稳，比提早连接外部 worker 网络更符合当前产品阶段。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260310-0056-A
- session_refs:
  - tool: codex
  - session_id: unavailable://chat-session
  - jsonl_path: unavailable://codex-cli-session-jsonl-not-exposed
  - role: researcher
