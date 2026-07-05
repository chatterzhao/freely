# Brainstorm: frontend-backend-boundary-contract-v1-for-frontend-probe

## Focus

把 `I-20260308-1245` 的总体边界结论压缩成 Probe day-1 真正可调用、可订阅、可恢复的 boundary contract v1。

## Key Questions

1. Frontend Probe day-1 最少需要哪些 `ClientCommand`？
2. Backend 至少要发布哪些 `ServerEvent` 才足够支撑 probe 观察与中断？
3. `Snapshot` 需要覆盖哪些事实才能支持首屏和 resume？
4. sessions / stream / history / status 的字段边界该如何冻结，避免 transport 锁死？
5. request correlation、stream ordering、error surface、attach/resume 需要哪些最小语义？

## Working direction

- 直接复用 `I-20260308-1245` 的三层协议分层，不重开“是否前后端解耦”的争论。
- day-1 先允许 `tauri_adapter`，但 contract 字段命名和错误面不能依赖 Tauri 私有语义。
- `Frontend Probe v0` 只消费 boundary contract，不读取 runtime / workspace 内部结构。

## Initial contract slices

### ClientCommand

- `CreateOrResumeSession`
- `SendChatIntervention`
- `ControlRun`
- `AttachTerminal`
- `RequestSnapshot`

### ServerEvent

- `SessionUpserted`
- `RunStatusChanged`
- `AgentStatusChanged`
- `TerminalChunkAppended`
- `GovernanceDecisionRecorded`
- `InputArbitrationRecorded`
- `RecoveryStatusChanged`

### Snapshot

- project overview
- active sessions / runs / agents
- terminal attach target summary
- governance / recovery / blocker summary

## Boundary guard

- frontend 不直接读写 PTY、workspace、laws/routing 结果
- transport adapter 只能做承载转换，不能改字段语义
- errors 必须有稳定 surface，避免 UI 只能读日志猜状态
