# Issue: backend-service-contract-and-adapter-taxonomy

- issue_id: `I-20260312-0011`
- title: Backend Service Contract and Adapter Taxonomy
- phase_state: `done_ibm`
- milestone: `M-20260312-control-surface-runtime-convergence`
- epic-name: `control-surface-runtime-convergence`
- story-name: `backend-service-contract-and-adapter-taxonomy`
- issue-name: `backend-service-contract-and-adapter-taxonomy`
- source_candidate: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md#c-20260312-0011-a`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/issues/internal-frontend-backend-architecture-review.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}

## Why

Freely 已经接受 `ClientCommand`、`ServerEvent`、`Snapshot` 的方向，但仍缺一份正式 issue，把 backend service contract 与 adapter taxonomy 冻结成单一真源，避免后续把 protocol 语义和 transport 承载混成一层。

## Scope

1. 冻结 backend service contract 的职责边界。
2. 定义 adapter taxonomy，并区分 `tauri_adapter`、`ws_adapter`、`local_process_adapter` 与 `openclaw_adapter/profile`。
3. 明确 adapter 只负责承载与映射，不改业务语义。
4. 约束后续 control surface、probe 与 runtime 设计必须引用同一 contract 真源。

## Acceptance

- 文档明确 backend service contract 与 adapter 的分层边界。
- 文档明确 `tauri_adapter`、`ws_adapter`、`local_process_adapter`、`openclaw_adapter/profile` 的角色差异。
- 文档明确 `ClientCommand`、`ServerEvent`、`Snapshot` 是业务语义层，不依赖单一 transport。
- 文档明确 OpenClaw 只能作为 optional adapter/profile，不是 Freely 主定义。
- 后续 UI / runtime issue 可以直接引用本 issue，而不需要重新争论 contract 所属边界。

## Minimal contract frame

- contract layer:
  - `ClientCommand`
  - `ServerEvent`
  - `Snapshot`
- adapter layer:
  - `tauri_adapter`
  - `ws_adapter`
  - `local_process_adapter`
  - `openclaw_adapter/profile`
- rule:
  - adapter 可以转换承载，不可以变更业务语义

## IBM Handoff

- implementation_scope_summary:
  - 先把 Freely 的 contract 真源与 adapter taxonomy 冻结下来，为后续 control surface、runtime baseline 与 human intervention issue 提供统一边界。
- required_doc_refs:
  - `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
  - `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
  - `docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/issues/internal-frontend-backend-architecture-review.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/issues/frontend-backend-boundary-contract-v1-for-frontend-probe.md`

## Next

- IBM 已完成，下一步按 sequencing 拆到后续 control surface / runtime / intervention issue，而不是再回头扩写 pre-brainstorm 或重复争论 contract/adaptor 边界。
