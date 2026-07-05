# Issue: pre-tests-cleanup-and-retirement-enforcement-governance

- issue_id: `I-20260411-1416-A`
- title: Pre-tests cleanup and retirement enforcement governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `pre-tests-cleanup-and-retirement-enforcement-governance`
- issue-name: `pre-tests-cleanup-and-retirement-enforcement-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260411/candidates.md#c-20260411-1416-a`
- source_brainstorm: `docs/B1-docs/raw-20260411/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/ibm/pre-tests-evidence-binding-and-completion-gate-governance/issues/pre-tests-evidence-binding-and-completion-gate-governance.md`
  - `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

当前系统已经把 `pre-tests.md` 用于 completion 和 guarded promote，但 cleanup / retirement 还没有消费同一真源，因此 lifecycle closure 与测试真源仍未闭环。

## Scope

1. 在 cleanup / retirement 前读取 issue `pre_tests_path`
2. 用 machine-readable 方式阻止证据未闭环的 retirement
3. 输出 item-level blocker
4. 保持 completion / merge 行为不变

## Non-Goals

1. 不把 adequacy schema v2 混进本 owner
2. 不把 launch hard gate 混进本 owner
3. 不新增 `tests.md`
4. 不把历史 deferred 叙事误写成 regression

## IBM Handoff

- implementation_scope_summary:
  - 本 owner 只补 cleanup / retirement gate。
  - 第一阶段只要求最小字段集合，不强推 adequacy schema 扩展。
- required_doc_refs:
  - `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/prd.md`
  - `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/pre-tests.md`
  - `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/tasks.md`
  - `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`

## Completion

- `docs/B1-docs/raw-20260411/candidates.md`
- `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/issues/pre-tests-cleanup-and-retirement-enforcement-governance.md`
- `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/brainstorms/b-pre-tests-cleanup-and-retirement-enforcement-governance.md`
- `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/prd.md`
- `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/pre-tests.md`
- `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/tasks.md`
- `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/code-reviews/20260411-pre-tests-cleanup-and-retirement-enforcement-verification.md`
- `docs/progress/workspace-routing-foundation/p-pre-tests-cleanup-and-retirement-enforcement-governance.md`
- `bin/pretests-retirement-gate`
- `docs/system/workspace/scripts/quality/pretests-retirement-gate`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
- `docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-pretests-retain`
- `docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-retained-continuation`

## Verification

- `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-pretests-retain`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-retained-continuation`
- `./bin/governance-check`
- `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/code-reviews/20260411-pre-tests-cleanup-and-retirement-enforcement-verification.md`

## Next

1. next_action: `completed on canonical develop; the guarded premerge replay, develop promotion, and dedicated-lane retirement are already closed and this issue now remains only as canonical delivered truth.`
2. revisit_trigger: Re-open only if guarded premerge replay shows cleanup followthrough can still retire a worktree without reading its bound pre-tests truth or without surfacing item-level retirement blockers.
