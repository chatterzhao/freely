# Issue: incremental-dogfooding-gate-for-backend-increments

- issue_id: `I-20260317-1003`
- title: Incremental Dogfooding Gate for Backend Increments
- phase_state: `completed`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- epic-name: `frontend-probe-dogfooding-loop`
- story-name: `incremental-dogfooding-gate-for-backend-increments`
- issue-name: `incremental-dogfooding-gate-for-backend-increments`
- source_candidate: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md#c-20260308-1244-04`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/frontend-probe-dogfooding-loop/incremental-dogfooding-gate-for-backend-increments/pre-tests.md`
- progress_path: `docs/progress/frontend-probe-dogfooding-loop/p-incremental-dogfooding-gate-for-backend-increments.md`
- verification_artifact_dir: `docs/epics/frontend-probe-dogfooding-loop/incremental-dogfooding-gate-for-backend-increments/code-reviews`
- depends_on: `none`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}

## Why

即使 boundary contract 与 Probe v0 已完成最小 IBM 收敛，如果没有正式门禁，团队仍可能回到“先堆后端、最后才补前端验证”的旧路径。

## Scope

1. 定义后端增量进入完成态前必须具备的 Probe 验证证据。
2. 明确验证证据的最小回写位置与阻断条件。
3. 明确当 Probe 验证缺失时，后端增量不得宣告完成。
4. 明确该门禁同样适用于 Freely 自举开发 Freely。

## Acceptance

- 文档明确“没有 Probe 验证证据的后端增量不算完成”。
- 文档明确最小验证证据至少覆盖：可触发、可观察、可中断、可回放。
- 文档明确证据写回位置与最小字段。
- 文档明确缺失 Probe 验证时的阻断语义。

## Minimal verification evidence

- `probe_entry`
  - 哪个 UI 入口触发了该后端能力
- `probe_observation`
  - 哪个 panel / stream / snapshot 证明人能观察到它
- `probe_interruptibility`
  - 哪个控制动作证明它可中断或重试
- `probe_replayability`
  - 哪个 snapshot / history / event log 证明它可回放

## Evidence write-back

- issue / code-review:
  - 记录该后端增量对应的 Probe 验证摘要
- milestone:
  - 只保留下一动作与当前阶段，不保存完整验证细节
- progress 或研究阶段等价 continuity:
  - 记录当前 run、验证结果、阻断原因与 session_refs

## Blocking rule

- 若缺少 `probe_entry`、`probe_observation`、`probe_interruptibility`、`probe_replayability` 任一项：
  - 后端增量不得进入完成态
  - milestone 不得推进到 `completed`
  - 若能力已实现但缺门禁证据，应保持在当前 issue / progress 中并显式记录 blocker

## IBM Handoff

- implementation_scope_summary:
  - 基于已冻结的 boundary contract 与 Probe v0，继续把“每个后端增量必须被 Probe 验证”收敛为正式门禁。
  - 当前阶段仍是 issue-bound IBM 收敛，不进入实现代码。
- required_doc_refs:
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/issues/frontend-backend-boundary-contract-v1-for-frontend-probe.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/epics/frontend-probe-dogfooding-loop/incremental-dogfooding-gate-for-backend-increments/brainstorms/b-incremental-dogfooding-gate-for-backend-increments.md`
  - `docs/epics/frontend-probe-dogfooding-loop/incremental-dogfooding-gate-for-backend-increments/prd.md`
  - `docs/epics/frontend-probe-dogfooding-loop/incremental-dogfooding-gate-for-backend-increments/pre-tests.md`
  - `docs/epics/frontend-probe-dogfooding-loop/incremental-dogfooding-gate-for-backend-increments/tasks.md`

## Closeout

- This owner is now explicitly closed as reusable gate truth rather than left parked between `done_ibm` and milestone `committed`.
- Future backend increment owners should consume this gate directly instead of reopening the gate definition.
- Reopen only if the minimal probe evidence set or blocking semantics become insufficient for real backend increment review.
