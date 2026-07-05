# Issue: governance-check-protected-merge-history-source-policy-governance

- issue_id: `I-20260406-0045-A`
- title: Governance-check protected-merge history source policy governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `governance-check-protected-merge-history-source-policy-governance`
- issue-name: `governance-check-protected-merge-history-source-policy-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260406-0045--governance-check-protected-merge-history-source-policy/candidates.md#c-20260406-0045-a`
- source_brainstorm: `docs/pre-brainstorms/20260406-0045--governance-check-protected-merge-history-source-policy/brainstorms.md`
- execution_base: `feature/governance-check-protected-merge-history-20260406-0045`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-governance-check-protected-merge-history-source-policy-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md`
  - `docs/epics/workspace-routing-foundation/test-pre-merge-family-promotion-gate-enforcement-governance/issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

一次真实的 `feature/* -> test-pre-merge-* -> develop` promote 后，`./bin/governance-check` 在 canonical `develop` 上误报：

1. 它把 `test-pre-merge-*` 批次内部的 merge commit 也当成了 `develop` 的 protected merge 历史。
2. 因此 `Freely-Source-Branch: feature/*` 在 batch 内是合法的，却被拿到 `develop` 的规则下重新校验。
3. 结果是有效的 guarded merge 刚完成，post-merge followthrough 反而立即失败。

## Scope

1. 仅修复 protected-branch receipt 审计的 merge-history selection。
2. 保持 direct invalid source-policy rejection 不变。
3. 增加 focused regression 覆盖 nested `test-pre-merge-*` ancestry。

## Non-Goals

1. 不重写 merge receipt schema。
2. 不改 `pr-merge-guarded` 的 receipt 内容。
3. 不在本 owner 内顺手修 `pr-merge-guarded` 的 already-up-to-date return-path 问题。

## Acceptance

1. `./bin/governance-check` 在 canonical `develop` 上不再因 nested `test-pre-merge-*` merge commit 误报 invalid source branch。
2. `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt` 覆盖该场景并通过。
3. 直接 `feature/* -> develop` 的 invalid receipt 仍然被拒绝。

## Verification

- `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
- `./bin/governance-check`

## Next

- Completed on canonical `develop` through `test-pre-merge-20260406-0045-governance-check-history-source-policy` and guarded merge `f58cf65`.
- Post-merge followthrough on canonical `develop` passed `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt` and `./bin/governance-check`; no reopen is needed unless protected-branch ancestry auditing regresses again.
