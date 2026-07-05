---
local_id: I-20260312-0011
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '8'
    url: https://github.com/chatterzhao/freely/issues/8
    synced_at: '2026-04-27T11:12:23Z'
  gitee:
    issue_id: IJFO4U
    url: https://gitee.com/zhaoquan/freely/issues/IJFO4U
    synced_at: '2026-04-27T13:13:48Z'
primary_platform: github
canonical_issue_path: docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy/issues/backend-service-contract-and-adapter-taxonomy.md
last_synced_comment_at:
  github: '2026-04-27T11:12:23Z'
hash: ''
created_at: '2026-04-27T11:12:23Z'
updated_at: '2026-04-27T11:12:23Z'
platform_state: closed
---

# Issue: backend-service-contract-and-adapter-taxonomy

- issue_id: `I-20260312-0011`
- title: Backend Service Contract and Adapter Taxonomy
- phase_state: `completed`
- milestone: `M-20260312-control-surface-runtime-convergence`
- epic-name: `control-surface-runtime-convergence`
- story-name: `backend-service-contract-and-adapter-taxonomy`
- issue-name: `backend-service-contract-and-adapter-taxonomy`
- verification_artifact_dir: `docs/epics/- epic-name: `control-surface-runtime-convergence`/- story-name: `backend-service-contract-and-adapter-taxonomy`/code-reviews`
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
  - `ClientC
