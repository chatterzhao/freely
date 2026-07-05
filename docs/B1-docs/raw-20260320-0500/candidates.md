# Candidates - 20260320-0500--candidate-acceptance-review-governance

## Context
- Source brainstorm: `./brainstorms.md`
- Status: `promoted`

## Candidates

### C-20260320-0500-A
- title: Candidate acceptance review governance
- problem: Freely 的 candidate 过去更像“问题摘要 + next_action”，缺少 candidate-level acceptance boundary；同时，candidate promotion 到 IBM 前也缺少规范化的独立 acceptance review 记录，导致 promotion gate 与 IBM acceptance deepening 都不够稳定。
- why_now: 本轮已经把 future candidate 的 v2 schema、独立 acceptance review 记录、`governance-check` 门禁，以及 IBM acceptance deepening 真源一起补进仓库。当前缺口不再是 pre-brainstorm 边界，而是把这条能力正式 materialize 为 canonical issue。
- acceptance_hint:
  - future candidate 默认使用 `candidate_format_version: v2`
  - `v2` candidate 至少包含 `acceptance_criteria`、`promotion_gate`、`open_questions`、`acceptance_reviews`
  - `governance-check` 会拦截 future v2 candidate 缺字段或 promoted v2 candidate 缺 review 记录
  - `doc-ibm-execution` 明确 candidate acceptance 进入 IBM 后要深化为 issue-level acceptance
  - `test-governance-check-candidate-v2` 锁定上述门禁
- priority: `P0`
- status: `promoted`
- decision_reason: schema、review 语义、门禁与 IBM 真源都已实现并有脚本回归，继续保留在 `pending://...materialization` 会让 canonical issue 落后于真实能力状态。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/candidate-acceptance-review-governance/issues/candidate-acceptance-review-governance.md`
- legacy_id_mapping: `I-20260320-0500`
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]
