# Issue: protected-branch-ref-only-entrypoint-enforcement-governance

- issue_id: `I-20260419-0210-A`
- title: `Protected-branch ref-only entrypoint enforcement governance`
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `protected-branch-ref-only-entrypoint-enforcement-governance`
- issue-name: `protected-branch-ref-only-entrypoint-enforcement-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260419/candidates.md#c-20260419-0210-a`
- source_brainstorm: `docs/B1-docs/raw-20260419/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- prd_path: `docs/B2-docs/ibm/protected-branch-ref-only-entrypoint-enforcement-governance/prd.md`
- pre_tests_path: `docs/B2-docs/ibm/protected-branch-ref-only-entrypoint-enforcement-governance/pre-tests.md`
- tasks_path: `docs/B2-docs/ibm/protected-branch-ref-only-entrypoint-enforcement-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-protected-branch-ref-only-entrypoint-enforcement-governance.md`
- verification_artifact_dir: `docs/B2-docs/ibm/protected-branch-ref-only-entrypoint-enforcement-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/ibm/develop-guarded-merge-entrypoint-enforcement-governance/issues/develop-guarded-merge-entrypoint-enforcement-governance.md`
  - `docs/system/workspace/hooks/reference-transaction.sh`
  - `.githooks/reference-transaction`
  - `docs/system/workspace/scripts/tests/test-reference-transaction-hook`
- created_at: `2026-04-19`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely already declares `freely pr-merge-guarded` as the canonical protected-merge entrypoint, but the current enforcement only covers merge-commit creation and merge completion. A real protected-root replay on `2026-04-19` proved that `git merge --ff-only` can still advance `develop` directly to a feature commit because no merge commit is created and `pre-merge-commit` never runs.

That means the protected-branch entrypoint contract is still incomplete.

## Scope

1. Add a protected-branch ref-update gate that runs even when Git performs a ref-only fast-forward.
2. Fail protected-branch ref advances unless the new head is a receipt-bearing protected merge commit.
3. Preserve canonical receipt-bearing protected merge commits on `main`, `develop`, and `test-pre-merge-*`.
4. Cover the narrow repair with focused regression proof for the blocked `ff-only` case and an allowed receipt-bearing merge case.

## Non-Goals

1. Do not reopen server-side enforcement.
2. Do not redesign merge receipts, break-glass policy, or push governance.
3. Do not widen this owner into a generic protected-branch rewrite policy.
4. Do not reopen the completed merge-commit-only entrypoint owner except as explicit dependency context.

## Acceptance

1. `git merge --ff-only` or equivalent ref-only updates cannot advance a protected branch to a non-receipted commit.
2. The ref gate fails before the protected ref is updated, not only later at push time.
3. Receipt-bearing protected merge commits still update protected branches successfully.
4. The owner documents why `reference-transaction` is the chosen narrow enforcement point.

## Verification

- `bash docs/system/workspace/scripts/tests/test-reference-transaction-hook`
- `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
- `git diff --check`
- `./bin/governance-check`

## Success Criteria

1. Protected-root local `develop` can no longer be fast-forwarded to a feature commit without a canonical protected merge receipt.
2. Canonical receipt-bearing protected merge commits still succeed under the local hook stack.
3. Verification evidence is written back in this owner, then the branch is merged to `develop`, pushed, and the dedicated worktree is retired.
