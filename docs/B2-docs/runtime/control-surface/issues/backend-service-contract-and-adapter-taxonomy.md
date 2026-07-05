# Issue: backend-service-contract-and-adapter-taxonomy

- issue_id: `I-20260312-0011`
- title: Backend Service Contract and Adapter Taxonomy
- phase_state: `completed`
- milestone: `M-20260312-control-surface-runtime-convergence`
- epic-name: `control-surface-runtime-convergence`
- story-name: `backend-service-contract-and-adapter-taxonomy`
- issue-name: `backend-service-contract-and-adapter-taxonomy`
- verification_artifact_dir: `docs/B2-docs/- epic-name: `control-surface-runtime-convergence`/- story-name: `backend-service-contract-and-adapter-taxonomy`/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260312/candidates.md#c-20260312-0011-a`
- source_brainstorm: `docs/B1-docs/raw-20260312/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/B2-docs/human/tui/issues/internal-frontend-backend-architecture-review.md`
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
  - `docs/B1-docs/raw-20260312/brainstorms.md`
  - `docs/B1-docs/raw-20260312/candidates.md`
  - `docs/B2-docs/human/tui/issues/internal-frontend-backend-architecture-review.md`
  - `docs/B2-docs/human/tui/issues/frontend-backend-boundary-contract-v1-for-frontend-probe.md`

## Verification

- `rg -n "ClientCommand|ServerEvent|Snapshot|tauri_adapter|ws_adapter|local_process_adapter|openclaw_adapter|openclaw_adapter/profile" docs/B2-docs/runtime/backend-service-contract-and-adapter-taxonomy docs/B2-docs/frontend-probe-dogfooding-loop -g '*.md'`
- `rg -n "I-20260312-0011|backend-service-contract-and-adapter-taxonomy" docs -g '*.md'`
- `./bin/governance-check`

## Closure Judgment

- 本 issue 的交付物是 contract freeze 本身，不是后续 adapter 或 runtime 实现；当前 issue、PRD、pre-tests 与 IBM review 已把 contract layer、adapter layer 与 OpenClaw optional profile 的边界冻结为单一真源。
- 下游 probe / frontend backend boundary 文档已经在消费同一组 `ClientCommand`、`ServerEvent`、`Snapshot` 与 adapter 兼容原则，说明这条 contract 不再停留在孤立 IBM 包，而是已成为 canonical 引用边界。
- 当前 milestone 中待推进的是基于这条真源的后续候选 materialization，而不是继续让 `I-20260312-0011` 停在 `done_ibm`。

## Next

- 后续 control surface、standalone runtime、human intervention transport 等 issue 直接复用这条 contract 真源；若未来需要上升到更高层系统拓扑或新增 adapter family，另开新的 lifecycle。
