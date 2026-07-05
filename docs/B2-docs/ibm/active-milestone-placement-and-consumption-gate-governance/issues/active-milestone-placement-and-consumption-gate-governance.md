# Issue: active-milestone-placement-and-consumption-gate-governance

- issue_id: `I-20260331-2012-A`
- title: Active milestone placement and consumption gate governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `active-milestone-placement-and-consumption-gate-governance`
- issue-name: `active-milestone-placement-and-consumption-gate-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260331-2012/candidates.md#c-20260331-2012-a`
- source_brainstorm: `docs/B1-docs/raw-20260331-2012/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/code-reviews`
- depends_on:
  - `docs/B1-docs/raw-20260320-0908/candidates.md`
  - `docs/B1-docs/raw-20260321-1835/brainstorms.md`
  - `docs/B1-docs/raw-20260327-1003/brainstorms.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经把两条规则写成 canonical truth：

1. unresolved candidate 不能从 active scans 中消失
2. develop merge 需要 `C-* -> M-* -> I-*` 的可追踪 owner 链

但这之间仍有一个缺口：当前 gates 过去只检查“candidate 出现在某个 milestone 队列里”，没有证明这条 candidate 被放进了正确且仍 active、会继续消费它的 milestone。结果就是：

- `milestone: unassigned` 仍可能漏过
- `pending://milestone-binding` 会把 candidate 伪装成已排期
- completed milestone 也可能意外承接新的 unresolved candidate
- 当前 milestone 已确定不消费的 `needs_research` candidate 可能长期悬空

本 owner 的任务就是把这层 placement correctness 变成正式 gate，并补齐最小 rehome-or-drop contract。

## Scope

1. 冻结 active candidate placement correctness 的最小合同。
2. 让 `governance-check` 与 `governance-merge-gate` 共同拒绝：
   - `unassigned`
   - `pending://...`
   - wrong active milestone
   - completed milestone placement for unresolved candidates
3. 明确 `promoted` candidate 必须 materialize 成 formal `I-*` sequencing。
4. 把 `needs_research` 的 keep / cautious rehome / dropped 规则写回 `LAWS`、skills 与 agent truth。
5. 对齐当前 backlog 中已经暴露的 candidate placement drift。

## Non-Goals

1. 不实现新的 milestone 排期引擎。
2. 不要求仓库立刻全面采用 `M1.1 / M2.1` 级别子阶段编号。
3. 不在这条 issue 内实现 runtime 自动重排 candidate 的调度器。
4. 不借此扩写 multi-tool auto-switch、frontend 或其他无关候选的 owner scope。

## Acceptance

1. active candidate 不能保持 `milestone: unassigned` 或 `pending://...`。
2. unresolved `needs_research | proposed | blocked` candidates 必须位于 active milestone 的 `candidate_issues`。
3. candidate 文档中的 `milestone:` 必须与 `docs/milestones.md` 实际承接它的 `M-*` 一致。
4. completed milestone 默认不能继续承接新的 unresolved candidate。
5. `promoted` candidate 必须通过 formal `I-*` sequencing 出现在 milestone，而不是只剩 candidate entry。
6. `LAWS`、skills、agent、quality gates 与 focused tests 对 placement correctness 使用相同口径。

## Completion

- `docs/B1-docs/raw-20260331-2012/brainstorms.md`
- `docs/B1-docs/raw-20260331-2012/candidates.md`
- `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/brainstorms/b-active-milestone-placement-and-consumption-gate-governance.md`
- `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/issues/active-milestone-placement-and-consumption-gate-governance.md`
- `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/prd.md`
- `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/code-reviews/20260331-active-milestone-placement-gate-verification.md`
- `docs/progress/workspace-routing-foundation/p-active-milestone-placement-and-consumption-gate-governance.md`
- `docs/LAWS.md`
- `docs/milestones.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/scripts/quality/governance-check`
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`
- `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-pre-brainstorm-execution/references/candidate-recording.md`
- `docs/system/workspace/skills/doc-pre-brainstorm-execution/references/milestone-placement.md`
- `docs/system/workspace/skills/milestone-planning-state-maintenance/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/governance-check`

## Next

- `2026-04-01 09:55 PDT` canonical absorption is complete: placement correctness now lives in `develop`, verification has passed, and this owner is closed.
- Any future work that adds milestone scheduling heuristics, automatic rehome, or richer sequencing policy must open a new lifecycle instead of reopening this completed gate owner.
