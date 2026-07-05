# Issue: story-level-pre-tests-quality-gate-governance

- issue_id: `I-20260325-0333-B`
- title: Story-level pre-tests quality gate governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- completion_date: 2026-03-31
- epic-name: `workspace-routing-foundation`
- story-name: `story-level-pre-tests-quality-gate-governance`
- issue-name: `story-level-pre-tests-quality-gate-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260325/candidates.md#c-20260325-0333-b`
- source_brainstorm: `docs/B1-docs/raw-20260325/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/story-level-pre-tests-quality-gate-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/story-level-pre-tests-quality-gate-governance/code-reviews`
- depends_on:
  - `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
  - `docs/epics/workspace-routing-foundation/integration-acceptance-first-verification-governance/issues/integration-acceptance-first-verification-governance.md`
  - `docs/epics/workspace-routing-foundation/application-native-runtime-observation-contract-and-observability-planes/issues/application-native-runtime-observation-contract-and-observability-planes.md`
  - `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经明确 `pre-tests.md` 是 issue-level acceptance 控制面，但还没有冻结 story-level 质量门禁。结果就是：

- `pre-tests.md` 可以“形式存在”，却仍然无法恢复 acceptance contract
- 后续 integration / end-to-end / real-environment 测试即使跑了，也可能建立在不稳定目标上
- completion verification 与 worktree retirement 仍然容易退化成“命令跑过一些、文档也有一份”，而不是“验收定义先站稳”

在更大的 testing evidence ladder 能力完成前，最先必须硬化的是 story-level `pre-tests.md` 质量 gate。

## Scope

1. 冻结 story-level `pre-tests.md` 的最低质量线，使其成为可拒绝、可恢复的硬门禁。
2. 明确 `pre-tests.md` 至少必须表达：
   - acceptance target
   - testing layer
   - target environment
   - required evidence
   - blocker taxonomy
3. 冻结 blocker taxonomy 的最小枚举：
   - `definition_missing`: `pre-tests.md` 缺少 acceptance target / testing layer / target environment / required evidence / blocker taxonomy 之一
   - `commands_only`: 只有命令，没有可恢复的 acceptance contract
   - `evidence_plan_missing`: 有测试对象但没有 required evidence 或 acceptance 留痕要求
   - `execution_pending_or_failed`: acceptance 已定义，但测试尚未执行、执行失败或证据未产生
3. 明确以下两类失败不能混淆：
   - 测试尚未执行
   - `pre-tests.md` 自身不足以定义 acceptance
4. 把这一质量线写回 Freely 的 IBM / lifecycle 真源，让后续 issue 在 doc-loop 即可被拒绝，而不是等到 verification 才补救。

## Acceptance

- Freely 真源明确：每个 story 下的 `pre-tests.md` 若不能恢复 acceptance contract，则不得视为合格的 issue-level acceptance 控制面。
- 真源明确：`pre-tests.md` 至少要覆盖 acceptance target、testing layer、target environment、required evidence、blocker taxonomy。
- 真源明确：commands-only 的 `pre-tests.md` 不合格，不能被视为“测试已定义”。
- 真源明确：story-level `pre-tests.md` 质量 gate 至少冻结 `definition_missing`、`commands_only`、`evidence_plan_missing`、`execution_pending_or_failed` 这四类 blocker taxonomy。
- 真源明确区分：
  - `pre-tests.md` 质量失败
  - 测试执行失败或未执行
- 这条质量线与既有 `integration-acceptance-first`、artifact-plane acceptance evidence、protected/post-merge verification 口径兼容，不另造平行 truth。

## Ready For Dev

当前 IBM 已冻结：

1. 本 issue 只处理 story-level `pre-tests.md` 质量 gate，不在同一批次同时完成完整 testing ladder / harness contract。
2. `pre-tests.md` 质量线要优先进入 IBM truth 与 lifecycle truth，而不是先发明新的测试 runner。
3. commands-only、definition-missing、evidence-plan-missing 与 execution-pending-or-failed 这四类 `pre-tests.md` / testing blocker 必须能被真源明确区分并拒绝误判。
4. 真实测试证据仍由 artifact plane 承载，status surface 继续只镜像最小摘要与 `acceptance_ref`。

## Implementation References

- `docs/epics/workspace-routing-foundation/story-level-pre-tests-quality-gate-governance/brainstorms/b-story-level-pre-tests-quality-gate-governance.md`
- `docs/epics/workspace-routing-foundation/story-level-pre-tests-quality-gate-governance/prd.md`
- `docs/epics/workspace-routing-foundation/story-level-pre-tests-quality-gate-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/story-level-pre-tests-quality-gate-governance/tasks.md`
- `docs/B1-docs/raw-20260325/inventory.md`
- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/pre-tests.md`
- `docs/LAWS.md`

## Completion

- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/LAWS.md`
- `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/pre-tests.md`
- `docs/progress/workspace-routing-foundation/p-story-level-pre-tests-quality-gate-governance.md`
- `docs/epics/workspace-routing-foundation/story-level-pre-tests-quality-gate-governance/code-reviews/20260325-story-level-pre-tests-quality-gate-governance-verification.md`

## Verification

- `./bin/governance-check`
- parallel review of issue materialization, truth-source consistency, and milestone routing consistency

## Next

- next_action: 当前 dev-loop 已在 dedicated feature worktree 写回 capability truth，当前保持 `in_verification`，等待 manager merge review / canonical absorption；不在本 issue 内继续扩写 testing ladder、gate mapping 或 real-environment harness scope。
- revisit_trigger: 当 `I-20260325-0333-B` 被 manager 视为 completed / absorbed 后，再回到 `C-20260325-0333-A` 判断 ladder / gate mapping / real-environment harness 的下一跳；若 merge review 指出 story-level `pre-tests.md` 质量线与 `LAWS.md` / `three-loop-capability-lifecycle.md` 仍有冲突，先回 doc-loop 修正，不进入新 dev 扩写。
