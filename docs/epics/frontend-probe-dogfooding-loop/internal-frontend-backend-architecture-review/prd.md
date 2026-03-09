# PRD: internal-frontend-backend-architecture-review

## Goal

为 Freely 的 day-1 桌面工具形态建立可演进的内部前后端边界和可插拔协议模型。

## Requirements

1. 明确 frontend / backend 的职责边界与状态归属。
2. 协议层分离为 frontend contract、transport adapter、backend service contract。
3. 定义 `ClientCommand`、`ServerEvent`、`Snapshot` 三类核心协议对象。
4. 第一阶段实现允许基于 Tauri 内部桥接，但不得把协议语义绑定到单一 transport。
5. 保持技术栈为 Rust + Tauri + Bun + React + TypeScript，不引入 Node.js 产品运行时。
6. 定义 `MVP autonomy milestone`，明确 Freely 何时可以开始自治开发并狗粮开发自己。
7. 定义 human interaction policy：人类默认不阻塞主循环，但 chat input 与控制命令拥有高优先级纠偏语义。
8. 定义 AI team visibility UI：用户能够看到多个 agent / run 的状态、阶段、进展与阻塞。
9. 定义 day-1 主入口为应用内终端 / 控制台，而不是外部 shell。

## Product rules

1. Frontend 只拥有 view-local state，不拥有 session/run/governance 的事实状态。
2. Backend 必须作为 session、run、agent、terminal、governance 的唯一事实源。
3. 协议面固定为 `ClientCommand`、`ServerEvent`、`Snapshot` 三类对象，transport adapter 只能做承载转换。
4. `tauri_adapter` 是 day-1 实现策略，不是产品协议定义。
5. `human chat input` 与显式控制命令必须进入 input arbitration，并留下可追溯结果。
6. team visibility UI 只消费 backend 已发布的事实，不从零散日志推断主状态。

## Required protocol surface

- Commands:
  - `CreateOrResumeSession`
  - `SendChatIntervention`
  - `ControlRun`
  - `AttachTerminal`
  - `RequestSnapshot`
- Events:
  - `SessionUpserted`
  - `RunStatusChanged`
  - `AgentStatusChanged`
  - `TerminalChunkAppended`
  - `GovernanceDecisionRecorded`
  - `InputArbitrationRecorded`
  - `RecoveryStatusChanged`
- Snapshot domains:
  - project overview
  - active sessions/runs/agents
  - terminal attachment summary
  - governance/recovery summary

## MVP autonomy milestone

Freely 达到以下能力闭环时，视为具备最小自治开发能力：

1. Frontend Probe 可发起和观察一次真实 run。
2. Backend boundary contract 可承接 command / event / snapshot。
3. Governance 规则在应用内作为能力执行，而不是只停留在文档。
4. 能在正确 worktree 中完成一次最小 single-issue dev loop。
5. 人类可实时观察、打断和续接。
6. 人类可通过高优先级 chat input 纠偏，且 UI 可见 AI 团队态势。
