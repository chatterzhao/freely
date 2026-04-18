# Issue: runtime-lifecycle-receipt-followthrough-governance

- issue_id: `I-20260418-1900-A`
- title: `Runtime lifecycle receipt followthrough governance`
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-lifecycle-receipt-followthrough-governance`
- issue-name: `runtime-lifecycle-receipt-followthrough-governance`
- priority: `P1`
- source_candidate: `docs/pre-brainstorms/20260418-1900--runtime-lifecycle-receipt-followthrough/candidates.md#c-20260418-1900-a`
- source_brainstorm: `docs/pre-brainstorms/20260418-1900--runtime-lifecycle-receipt-followthrough/brainstorms.md`
- reopen_of_issue: `docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
- reopen_reason: `post-merge governance replay proved two historical receipt-gap entries for the absorbed runtime lifecycle test-pre-merge batch were still missing from the protected-branch backfill ledger`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-lifecycle-receipt-followthrough-governance/pre-tests.md`
- tasks_path: `docs/epics/workspace-routing-foundation/runtime-lifecycle-receipt-followthrough-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-lifecycle-receipt-followthrough-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-lifecycle-receipt-followthrough-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
- created_at: `2026-04-18`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Canonical `develop` already absorbed the runtime lifecycle implementation owner and pushed it upstream. The remaining defect is governance-only: post-merge replay found two missing receipt-gap backfills for historical merges inside `test-pre-merge-runtime-lifecycle-20260417`.

Because direct protected-root edits are forbidden and candidate-only closure is not lawful for a develop-bound diff, this receipt-ledger repair needs its own narrow followthrough owner instead of silently extending the completed implementation owner.

## Scope

1. Add the missing receipt-gap entries for `dc436573e5f3f995ed936e7b21c65f9440fffae9` and `f7145cc889c3919cbe21b1162f96d14d736b83b7`.
2. Carry the minimal candidate -> issue -> progress -> verification lifecycle needed for guarded develop replay.
3. Keep the main runtime lifecycle implementation owner closed; this lane is governance-only closeout.
4. Retire the temporary followthrough feature and test-pre-merge worktrees after canonical develop absorbs the ledger repair.

## Non-Goals

1. Do not reopen runtime start/stop implementation scope.
2. Do not widen this lane into generic receipt-gap automation redesign.
3. Do not keep the temporary followthrough worktrees alive after the repair lands.
4. Do not change runtime behavior, tests, or protected-branch source policy semantics.

## Acceptance

1. The develop-bound followthrough diff carries concrete issue, pre-tests, progress, tasks, and review artifacts.
2. `protected-branch-merge-receipt-backfills.md` contains the missing `dc436573...` and `f7145cc...` entries with bounded owner evidence.
3. `./bin/pretests-gate --project <worktree> --issue docs/epics/workspace-routing-foundation/runtime-lifecycle-receipt-followthrough-governance/issues/runtime-lifecycle-receipt-followthrough-governance.md` passes.
4. `./bin/governance-check` passes.
5. Canonical develop absorbs the ledger repair through guarded replay and the temporary followthrough worktrees are retired after merge.

## Verification

- `./bin/pretests-gate --project <worktree> --issue docs/epics/workspace-routing-foundation/runtime-lifecycle-receipt-followthrough-governance/issues/runtime-lifecycle-receipt-followthrough-governance.md`
- `git diff --check`
- `./bin/governance-check`
- `git worktree list`

## Completion

- `docs/pre-brainstorms/20260418-1900--runtime-lifecycle-receipt-followthrough/brainstorms.md`
- `docs/pre-brainstorms/20260418-1900--runtime-lifecycle-receipt-followthrough/candidates.md`
- `docs/epics/workspace-routing-foundation/runtime-lifecycle-receipt-followthrough-governance/issues/runtime-lifecycle-receipt-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-lifecycle-receipt-followthrough-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/runtime-lifecycle-receipt-followthrough-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-runtime-lifecycle-receipt-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-lifecycle-receipt-followthrough-governance/code-reviews/20260418-runtime-lifecycle-receipt-followthrough-verification.md`
- `docs/system/workspace/hooks/protected-branch-merge-receipt-backfills.md`
