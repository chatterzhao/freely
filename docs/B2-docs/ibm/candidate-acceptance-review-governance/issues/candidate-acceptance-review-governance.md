# Issue: candidate-acceptance-review-governance

- issue_id: `I-20260320-0500`
- title: Candidate acceptance review governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `candidate-acceptance-review-governance`
- issue-name: `candidate-acceptance-review-governance`
- source_candidate: `docs/B1-docs/raw-20260320T174500Z/candidates.md#c-20260320-0500-a`
- source_brainstorm: `docs/B1-docs/raw-20260320T174500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `none`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 已经要求 pre-brainstorm candidate 进入 milestone，但 candidate 过去缺少稳定的 acceptance boundary，也缺少 promotion 前的规范化独立 review 记录。这样会导致 candidate promotion、IBM materialization 与后续验收边界都依赖临场判断。

本轮已经把 v2 candidate schema、独立 acceptance review、`governance-check` 门禁，以及 IBM acceptance deepening 真源落盘。现在需要把这条能力正式写成 canonical issue，而不是继续停在 pre-brainstorm 候选。

## Scope

1. future candidate 默认进入 `candidate_format_version: v2`。
2. `v2` candidate 至少包含 `acceptance_criteria`、`promotion_gate`、`open_questions`、`acceptance_reviews`。
3. `governance-check` 强制 future v2 candidate 的字段存在，并强制 promoted v2 candidate 至少一条 review 记录。
4. `skill:candidate-acceptance-review` 明确独立 review 的角色与写回格式。
5. `doc-ibm-execution` 与相关 checklist/gate 明确 candidate acceptance deepening 到 issue-level acceptance。

## Acceptance

- `candidate-recording.md` 与 `doc-pre-brainstorm-execution/SKILL.md` 明确 v2 candidate fields。
- `skill:candidate-acceptance-review` 明确 review 输出结构。
- `governance-check` 能拦截 future v2 candidate 缺字段与 promoted review 缺失。
- `doc-ibm-execution`、`issue-materialization-checklist.md`、`ibm-completion-gate.md` 明确 IBM acceptance deepening。
- `bash docs/system/workspace/scripts/tests/test-governance-check-candidate-v2` 通过。

## Completion

- `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-pre-brainstorm-execution/references/candidate-recording.md`
- `docs/system/workspace/skills/candidate-acceptance-review/SKILL.md`
- `docs/system/workspace/scripts/quality/governance-check`
- `docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`
- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`

## Completion

- candidate acceptance review governance 已落盘并通过回归，future candidate 的 v2 schema、独立 review 记录、IBM acceptance deepening 与治理门禁都已稳定。
- canonical owner 继续保留历史 issue identity `I-20260320-0500`；对应 candidate `C-20260320-0500-A` 通过 `legacy_id_mapping` 回绑这条已物化的 issue lineage，而不是重命名旧 issue。
- 高风险 candidate 是否需要双审，保留为后续策略判断，不阻塞当前 canonical issue 完成。
