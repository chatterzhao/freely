# Issue: runtime-startup-root-cause-packet-governance

- issue_id: `I-20260413-0420-C`
- title: Runtime startup root-cause packet governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-startup-root-cause-packet-governance`
- issue-name: `runtime-startup-root-cause-packet-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260413/candidates.md#c-20260413-0420-c`
- source_brainstorm: `docs/B1-docs/raw-20260413/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-startup-root-cause-packet-governance.md`
- pre_tests_path: `docs/B2-docs/runtime/runtime-startup-root-cause-packet-governance/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/runtime/runtime-startup-root-cause-packet-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/gate/pretests-adequacy-item-schema-materialization-governance/issues/pretests-adequacy-item-schema-materialization-governance.md`
  - `docs/B2-docs/ibm/structured-closeout-gate-context-and-review-evidence-governance/issues/structured-closeout-gate-context-and-review-evidence-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

这轮 runtime 复盘已经把现象、根因、产品语义和三个 loop 影响都收敛清楚了，但 canonical `develop` 还只能看到 candidate-only truth。若不先把 split 本身 materialize 成一个真实 owner，后续实现 lane 会继续被“研究结论只存在于临时 worktree”拖住。

## Scope

1. 把 `20260413-0420` 预研 split 落成 canonical owner truth
2. 明确 `C-20260413-0420-A` 是 promote-ready 的 startup-authority implementation boundary
3. 明确 `C-20260413-0420-B` 继续保持 research-visible 的 manager-handoff follow-on boundary
4. 为这次 develop-bound absorb 提供 issue、progress、pre-tests、review 和 milestone writeback

## Non-Goals

1. 不在本 owner 内实现 startup authority 或 daemon readiness 修复
2. 不在本 owner 内实现 manager continuity contract
3. 不把 `C-20260413-0420-A` 提前 materialize 成 implementation issue
4. 不修改 runtime、CLI、gate、test 或 status 真源

## IBM Handoff

- implementation_scope_summary:
  - 这是一个 packet/routing owner，不是 runtime implementation owner。
  - 它的职责是把已经稳定的根因拆分和后续路由 canonicalize 到 `develop`。
- required_doc_refs:
  - `docs/B1-docs/raw-20260413/brainstorms.md`
  - `docs/B1-docs/raw-20260413/candidates.md`
  - `docs/B2-docs/runtime/runtime-startup-root-cause-packet-governance/prd.md`
  - `docs/B2-docs/runtime/runtime-startup-root-cause-packet-governance/pre-tests.md`
  - `docs/B2-docs/runtime/runtime-startup-root-cause-packet-governance/tasks.md`

## Completion

- `docs/B1-docs/raw-20260413/brainstorms.md`
- `docs/B1-docs/raw-20260413/candidates.md`
- `docs/B2-docs/runtime/runtime-startup-root-cause-packet-governance/issues/runtime-startup-root-cause-packet-governance.md`
- `docs/B2-docs/runtime/runtime-startup-root-cause-packet-governance/brainstorms/b-runtime-startup-root-cause-packet-governance.md`
- `docs/B2-docs/runtime/runtime-startup-root-cause-packet-governance/prd.md`
- `docs/B2-docs/runtime/runtime-startup-root-cause-packet-governance/pre-tests.md`
- `docs/B2-docs/runtime/runtime-startup-root-cause-packet-governance/tasks.md`
- `docs/B2-docs/runtime/runtime-startup-root-cause-packet-governance/code-reviews/20260413-runtime-startup-root-cause-packet-verification.md`
- `docs/progress/workspace-routing-foundation/p-runtime-startup-root-cause-packet-governance.md`
- `docs/milestones.md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-pretests-gate`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/governance-check`
- `git diff --check`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-pretests-gate`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/test-lane premerge-integration -- ./bin/governance-check`
- `freely pr-merge-guarded test-pre-merge-20260413-runtime-startup-authority-follow-on-packet feature/runtime-foreground-double-start-regression-20260413`
- `freely pr-merge-guarded develop test-pre-merge-20260413-runtime-startup-authority-follow-on-packet`

## Next

1. next_action: `Guarded-promote this packet to canonical develop, then retire the temporary feature and test-pre-merge worktrees.`
2. revisit_trigger: Re-open only if canonical develop still cannot absorb the split after concrete owner truth and develop-merge adequacy are present, or if a later implementation lane proves the split itself should change.
