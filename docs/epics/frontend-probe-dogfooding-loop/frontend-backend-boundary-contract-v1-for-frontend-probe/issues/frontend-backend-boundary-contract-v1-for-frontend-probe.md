# Issue: frontend-backend-boundary-contract-v1-for-frontend-probe

- issue_id: `I-20260317-1001`
- title: Frontend/Backend Boundary Contract v1 for Frontend Probe
- phase_state: `completed`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- epic-name: `frontend-probe-dogfooding-loop`
- story-name: `frontend-backend-boundary-contract-v1-for-frontend-probe`
- issue-name: `frontend-backend-boundary-contract-v1-for-frontend-probe`
- verification_artifact_dir: `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/code-reviews`
- source_candidate: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md#c-20260308-1244-02`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `none`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}

## Why

在 `I-20260308-1245` 已冻结总体 frontend/backend 边界后，Probe day-1 仍缺少一个更细的 boundary contract：

- frontend 到 backend 的最小调用面还未收敛到对象级别
- sessions / stream / history / status 的事件语义尚未冻结为 v1
- `tauri_adapter` 与未来 `ws_adapter` 的兼容原则尚未落到字段面
- `Frontend Probe v0` 仍缺少稳定验收面

## Scope

1. 冻结 Frontend Probe day-1 所需的最小 boundary contract。
2. 明确 sessions / stream / history / status 的 command / event / snapshot 语义。
3. 明确 day-1 `tauri_adapter` 承载方式与未来 `ws_adapter` 的兼容原则。
4. 明确错误面、request correlation、stream ordering、resume/attach 的最小字段。
5. 约束 frontend 只能通过 boundary contract 访问 backend，不直接侵入 runtime/workspace。

## Acceptance

- 文档明确 `ClientCommand`、`ServerEvent`、`Snapshot` 在 Probe v1 中的最小对象族。
- sessions / stream / history / status 至少各有一个明确的 contract 入口。
- contract 语义不绑定单一 transport；`tauri_adapter` 与未来 `ws_adapter` 共享同一业务字段。
- 文档明确错误面、request correlation、stream ordering、resume/attach 的最小语义。
- `Frontend Probe v0` 可以直接基于本 issue 进入后续 IBM / dev-loop，不需重新争论 boundary contract。

## Minimal contract v1

### ClientCommand

- `CreateOrResumeSession`
  - required: `project_id`
  - optional: `session_id`, `resume_hint`, `command_source`
- `SendChatIntervention`
  - required: `project_id`, `session_id`, `message_id`, `content`
  - optional: `run_id`, `target_agent_id`
- `ControlRun`
  - required: `project_id`, `run_id`, `action`
  - optional: `reason`
- `AttachTerminal`
  - required: `project_id`, `session_id`, `terminal_target`
  - optional: `run_id`, `cursor`
- `RequestSnapshot`
  - required: `project_id`
  - optional: `session_id`, `snapshot_scope`

### ServerEvent

所有事件至少带：
- `event_id`
- `occurred_at`
- `project_id`
- `session_id`
- `source`

最小对象族：
- `SessionUpserted`
- `RunStatusChanged`
- `AgentStatusChanged`
- `TerminalChunkAppended`
- `GovernanceDecisionRecorded`
- `InputArbitrationRecorded`
- `RecoveryStatusChanged`

### Snapshot

最小恢复面：
- `project_summary`
- `active_sessions`
- `active_runs`
- `active_agents`
- `terminal_targets`
- `governance_summary`
- `recovery_summary`
- `last_event_id`

## Domain entry mapping

- sessions:
  - command: `CreateOrResumeSession`
  - events: `SessionUpserted`, `RunStatusChanged`
  - snapshot: `active_sessions`
- stream:
  - command: `AttachTerminal`
  - events: `TerminalChunkAppended`, `RunStatusChanged`
  - snapshot: `terminal_targets`
- history:
  - command: `RequestSnapshot`
  - events: `SessionUpserted`, `GovernanceDecisionRecorded`, `InputArbitrationRecorded`
  - snapshot: `last_event_id`, `governance_summary`, `recovery_summary`
- status:
  - command: `RequestSnapshot`, `ControlRun`
  - events: `RunStatusChanged`, `AgentStatusChanged`, `RecoveryStatusChanged`
  - snapshot: `active_runs`, `active_agents`

## Error and ordering rules

- request correlation:
  - 每条 command 必须可通过 `message_id`、`run_id` 或 `session_id` 追溯到结果事件
- stream ordering:
  - 同一 `terminal_target` 下 `TerminalChunkAppended` 必须保持追加顺序
- error surface:
  - 至少区分 `validation_error`、`not_found`、`conflict`、`governance_rejected`、`transport_unavailable`
- attach/resume:
  - `AttachTerminal` 与 `CreateOrResumeSession` 必须允许 UI 重新附着到既有 session/run，而不是只支持 fresh start

## Adapter compatibility

- `tauri_adapter` 只负责把命令、事件和快照桥接进桌面应用内部 transport
- 未来 `ws_adapter` 复用同一业务对象族与错误面，不重命名核心字段
- adapter 可以改变承载方式，不得改变 `ClientCommand` / `ServerEvent` / `Snapshot` 的业务语义

## IBM Handoff

- implementation_scope_summary:
  - 基于 `I-20260308-1245` 已完成的总体边界收敛，把 Probe 真正依赖的 sessions / stream / history / status contract 冻结到 v1。
  - 当前 issue 已具备进入 `Frontend Probe v0` 所需的最小文档包，不进入实现代码。
- required_doc_refs:
  - `docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/issues/internal-frontend-backend-architecture-review.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/brainstorms/b-frontend-backend-boundary-contract-v1-for-frontend-probe.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/prd.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/pre-tests.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/tasks.md`

## Verification

- `rg -n "CreateOrResumeSession|SendChatIntervention|ControlRun|AttachTerminal|RequestSnapshot|SessionUpserted|RunStatusChanged|AgentStatusChanged|TerminalChunkAppended|GovernanceDecisionRecorded|InputArbitrationRecorded|RecoveryStatusChanged|project_summary|active_sessions|active_runs|active_agents|terminal_targets|governance_summary|recovery_summary|last_event_id" docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0 docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1 -g '*.md'`
- `rg -n "I-20260317-1001|frontend-backend-boundary-contract-v1-for-frontend-probe" docs -g '*.md'`
- `./bin/governance-check`

## Closure Judgment

- 本 issue 的交付物是 Probe day-1 boundary contract v1 本身，不是 Probe host integration 或 Rust/Tauri bridge 实装；当前 issue 已把 command、event、snapshot、ordering、error surface 与 adapter compatibility 冻结到对象级别。
- 下游 `Frontend Probe v0` 与 `Rust/Tauri Probe Bridge v1` 已直接消费这套 object family 和字段面，说明它已经成为 canonical contract source，而不是停留在 issue-bound IBM 草案。
- 因此 `I-20260317-1001` 可以按真实写回推进到 `completed`；后续实现与联调继续由 `I-20260317-1002` / `I-20260317-1005` 承接。

## Next

- 当前 issue 已完成 canonical closeout，后续 Probe v0 与 bridge work 继续复用该 v1 contract；若未来需要 v2 schema、额外 domain object 或 transport 扩展，另开新的 lifecycle。
