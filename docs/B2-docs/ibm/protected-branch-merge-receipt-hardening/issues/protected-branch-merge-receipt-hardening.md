# Issue: protected-branch-merge-receipt-hardening

- issue_id: `I-20260402-1912-A`
- title: Protected-branch merge receipt hardening
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `protected-branch-merge-receipt-hardening`
- issue-name: `protected-branch-merge-receipt-hardening`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260402T191200Z/candidates.md#c-20260402-1912-a`
- source_brainstorm: `docs/B1-docs/raw-20260402T191200Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-protected-branch-merge-receipt-hardening.md`
- verification_artifact_dir: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/code-reviews`
- depends_on:
  - `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/issues/protected-branch-hook-bypass-breakglass-governance.md`
  - `docs/system/workspace/scripts/worktree/pr-merge-guarded`
  - `docs/system/workspace/scripts/quality/governance-check`
  - `docs/system/workspace/scripts/quality/governance-merge-gate`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`I-20260402-0020-A` 已经把 protected-branch break-glass 的 phase-1 contract 合入 canonical `develop`，但 closeout 后仍有 residual hardening 没有 owner：

1. merge completion boundary
   - 仍需证明 break-glass short-circuit 不会扩张到初始 clean merge
2. receipt parity
   - `governance-check` 目前审计 trailer 与 ledger 的存在，但还没有更硬地校验字段一致性
3. staged / touched relevance
   - `governance-merge-gate` 已经出现过 staged-view / sibling-context false-negative 争议，必须冻结后续 hardening 边界

同时，canonical `develop` 根目录出现的一组 staged patch 已证明这个 residual signal 真实存在，但那组 patch 本身掺杂了 regression：

- 它试图删除 `test-pr-merge-guarded-hooked-initial-merge-receipt`
- 它试图删除 `governance-merge-gate` 的 staged-view coverage
- 它还混入了对已吸收 watchdog 修复的回退

因此这条 owner 的首要任务不是“吸收那组 patch”，而是把真正值得保留的 hardening 需求和应丢弃的 regression 切开。

## Scope

1. 冻结 protected-branch merge residual hardening 的更窄 contract：
   - `merge_completion_only`
   - `guarded_completion_handshake_hardening`
   - `receipt_ledger_parity_audit`
   - `merge_gate_false_negative_regression_coverage`
2. 明确根目录 staged patch 中哪些变化是：
   - keep-as-signal
   - already-absorbed
   - drop-as-regression
3. 设计最小实现切片，只针对 protected-branch merge hardening，而不 reopen break-glass policy owner。

## Non-Goals

1. 不 reopen `I-20260402-0020-A`。
2. 不回退或重做 break-glass whitelist。
3. 不把 watchdog repo-root resolution 混进这条 owner。
4. 不顺手删除 staged-view 或 initial-receipt regression tests 以换取 gate “更容易通过”。
5. 不设计 host-side / server-side absolute enforcement。

## Acceptance

1. IBM 产物必须明确这条 owner 只承接 residual hardening，而不是重新定义 bypass policy。
2. issue-bound artifact 必须把 root staged patch 分成 `keep-as-signal`、`already-absorbed`、`drop-as-regression` 三类。
3. `merge_completion_only` 的 boundary 必须写成可测试 contract，确保 break-glass 不扩张到 clean initial merge。
4. `receipt_ledger_parity_audit` 的最小字段与 failure semantics 必须冻结并通过回归测试。
5. guarded completion handshake 必须要求 canonical state 与当前 branch / `MERGE_HEAD` 一致，env-only spoof 不得放行。
6. `governance-merge-gate` 的 staged/touched relevance 边界必须重新写清，避免 sibling candidate 与 staged-only owner 误伤或漏检。
7. watchdog revert 必须被明确判定为 out-of-scope，且不得通过此 owner 吸收。

## Current Artifact Set

- `docs/B1-docs/raw-20260402T191200Z/brainstorms.md`
- `docs/B1-docs/raw-20260402T191200Z/candidates.md`
- `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`
- `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/brainstorms/b-protected-branch-merge-receipt-hardening.md`
- `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/prd.md`
- `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/pre-tests.md`
- `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/tasks.md`
- `docs/progress/workspace-routing-foundation/p-protected-branch-merge-receipt-hardening.md`

## Current Evidence

- `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/issues/protected-branch-hook-bypass-breakglass-governance.md`
- `docs/system/workspace/scripts/worktree/pr-merge-guarded`
- `docs/system/workspace/scripts/quality/governance-check`
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/hooks/protected-branch-breakglass-receipts.md`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
- `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
- `docs/system/workspace/scripts/tests/test-pre-commit-hook`
- `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded`
- `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/governance-check`

## Verification

- `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
- `bash docs/system/workspace/scripts/tests/test-pre-commit-hook`
- `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `git diff --check`
- `./bin/governance-check`
- `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/code-reviews/20260402-protected-branch-merge-receipt-hardening-verification.md`

## Next

- Closed on canonical `develop` through guarded merge absorption.
- Treat any later protected-branch merge receipt gap beyond parity audit, guarded completion handshake hardening, and the already-frozen staged merge-gate regression boundary as a fresh narrow follow-on.

## Completion Status

- canonical_merge_commit: `see develop history`
- canonical_merge_target: `develop`
- post_merge_acceptance:
  - `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
  - `bash docs/system/workspace/scripts/tests/test-pre-commit-hook`
  - `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
  - `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
  - `./bin/governance-check`
