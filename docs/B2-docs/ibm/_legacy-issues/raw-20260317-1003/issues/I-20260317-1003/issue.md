---
local_id: I-20260317-1003
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '12'
    url: https://github.com/chatterzhao/freely/issues/12
    synced_at: '2026-04-27T11:12:42Z'
  gitee:
    issue_id: IJFO50
    url: https://gitee.com/zhaoquan/freely/issues/IJFO50
    synced_at: '2026-04-27T13:13:53Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/human/tui/issues/incremental-dogfooding-gate-for-backend-increments.md
last_synced_comment_at:
  github: '2026-04-27T11:12:42Z'
hash: ''
created_at: '2026-04-27T11:12:42Z'
updated_at: '2026-04-27T11:12:42Z'
platform_state: closed
---

# Issue: incremental-dogfooding-gate-for-backend-increments

- issue_id: `I-20260317-1003`
- title: Incremental Dogfooding Gate for Backend Increments
- phase_state: `completed`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- epic-name: `frontend-probe-dogfooding-loop`
- story-name: `incremental-dogfooding-gate-for-backend-increments`
- issue-name: `incremental-dogfooding-gate-for-backend-increments`
- source_candidate: `docs/B1-docs/raw-20260308T163000Z/candidates.md#c-20260308-1244-04`
- source_brainstorm: `docs/B1-docs/raw-20260308T163000Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/human/tui/pre-tests.md`
- progress_path: `docs/progress/frontend-probe-dogfooding-loop/p-incremental-dogfooding-gate-for-backend-increments.md`
- verification_artifact_dir: `docs/B2-docs/human/tui/code-reviews`
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
  - 记录当前 run、验证结果、阻断
