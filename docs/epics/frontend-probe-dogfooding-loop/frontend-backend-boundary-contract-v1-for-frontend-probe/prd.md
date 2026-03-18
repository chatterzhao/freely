# PRD: frontend-backend-boundary-contract-v1-for-frontend-probe

## Goal

为 `Frontend Probe v0` 冻结一个 transport-agnostic 的 boundary contract v1，使 Probe 能在不侵入 runtime/workspace 的前提下稳定驱动和观察 Freely。

## Requirements

1. 定义 day-1 必需的 `ClientCommand`、`ServerEvent`、`Snapshot` 对象族。
2. 覆盖 sessions / stream / history / status 的最小 contract 面。
3. 明确 request correlation、stream ordering、error surface、attach/resume 的最小语义。
4. 保持 `tauri_adapter` 为 day-1 adapter，而不是业务协议本体。
5. 为后续 `Frontend Probe v0` 和 `Incremental Dogfooding Gate` 提供稳定验收面。

## Product rules

1. frontend 只通过 boundary contract 访问 backend。
2. backend 继续作为 session/run/agent/terminal/governance 的唯一事实源。
3. `Snapshot` 用于首屏和恢复，不替代完整 event history。
4. event 语义必须独立于 Tauri / WS / 其他 transport。
5. contract 中所有实体必须带足够的标识字段以支持 correlation 与 resume。

## Required contract surface

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
  - active sessions / runs / agents
  - terminal attachment summary
  - governance / recovery / blocker summary

## Minimal field rules

- every command:
  - `project_id` required
- every event:
  - `event_id`, `occurred_at`, `project_id`, `session_id`, `source`
- correlation:
  - command/result 必须能通过 `message_id`、`run_id` 或 `session_id` 关联
- ordering:
  - terminal stream 事件在单一 attach target 内必须单调追加
- resume:
  - `CreateOrResumeSession` 与 `AttachTerminal` 必须支持重新附着现有实体
- errors:
  - 至少区分 `validation_error`、`not_found`、`conflict`、`governance_rejected`、`transport_unavailable`

## Exit criteria for `done_ibm`

1. `Frontend Probe v0` 所需最小 contract 已冻结到对象级别。
2. sessions / stream / history / status 的入口与事件语义已可验收。
3. `tauri_adapter` 与未来 `ws_adapter` 的兼容原则已明确。
4. 后续实现 issue 不需要重新争论 contract 所属边界。
