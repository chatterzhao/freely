# Issue: tasks-closeout-completion-and-adequacy-gate-governance

- issue_id: `I-20260413-1640-A`
- title: Tasks closeout completion and adequacy gate governance
- phase_state: `completed`
- completed_at: `2026-04-28`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `tasks-closeout-completion-and-adequacy-gate-governance`
- issue-name: `tasks-closeout-completion-and-adequacy-gate-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260413T020800Z/candidates.md#c-20260413-1640-a`
- source_brainstorm: `docs/B1-docs/raw-20260413T020800Z/brainstorms.md`
- reopen_of_issue: `docs/B2-docs/ibm/structured-closeout-gate-context-and-review-evidence-governance/issues/structured-closeout-gate-context-and-review-evidence-governance.md`
- reopen_reason: `a real owner audit proved closeout hardening still omitted tasks.md, letting completed lifecycle truth drift from unchecked execution closeout boxes`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/pre-tests.md`
- tasks_path: `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-tasks-closeout-completion-and-adequacy-gate-governance.md`
- verification_artifact_dir: `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/ibm/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
  - `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/issues/pre-tests-cleanup-and-retirement-enforcement-governance.md`
  - `docs/B2-docs/ibm/structured-closeout-gate-context-and-review-evidence-governance/issues/structured-closeout-gate-context-and-review-evidence-governance.md`
  - `docs/system/workspace/scripts/quality/pretests-gate`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Canonical repo truth showed a narrow closeout drift: `I-20260413-0420-B` and `I-20260413-0420-C` were already marked completed in milestone and progress records even though their sibling `tasks.md` files still carried unchecked closeout items.

The missing contract was not in merge orchestration. `pretests-gate` already owned completion and guarded adequacy evaluation through bound `pre-tests.md`, while `governance-merge-gate` simply delegated to that owner gate. The gap was that execution closeout truth from sibling `tasks.md` never participated in the same decision, so completed lifecycle truth could outrun unfinished task checkboxes.

## Scope

1. Derive an owner-bound `tasks.md` path alongside the existing `pre-tests.md` contract, using explicit `tasks_path` when present and the sibling default otherwise.
2. Fail closed when completion or guarded adequacy checks cannot read the bound `tasks.md`.
3. Reject completion and `--require-adequacy` verdicts when the owner still has unchecked tasks.
4. Add focused regressions for direct `pretests-gate` enforcement and inherited `governance-merge-gate` behavior.
5. Record the lawful lifecycle evidence for the already-bounded repair.

## Non-Goals

1. Do not replace `pre-tests.md` as the canonical verification truth.
2. Do not add a second `tasks.md` parser in `governance-merge-gate`.
3. Do not widen this owner into generic issue-doc closeout auditing beyond the bound owner tasks ledger.
4. Do not reopen unrelated startup-routing implementation owners beyond citing the audit that surfaced the gap.

## Completion

- `docs/B1-docs/raw-20260413T020800Z/candidates.md`
- `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/issues/tasks-closeout-completion-and-adequacy-gate-governance.md`
- `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/brainstorms/b-tasks-closeout-completion-and-adequacy-gate-governance.md`
- `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/prd.md`
- `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/pre-tests.md`
- `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/tasks.md`
- `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/code-reviews/20260413-tasks-closeout-completion-and-adequacy-gate-verification.md`
- `docs/progress/workspace-routing-foundation/p-tasks-closeout-completion-and-adequacy-gate-governance.md`
- `docs/system/workspace/scripts/quality/pretests-gate`
- `docs/system/workspace/scripts/tests/test-pretests-gate`
- `docs/system/workspace/scripts/tests/test-governance-merge-gate`

## Verification

- `bash -n docs/system/workspace/scripts/quality/pretests-gate`
- `bash docs/system/workspace/scripts/tests/test-pretests-gate`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/governance-check`
- `git diff --check`
- `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/code-reviews/20260413-tasks-closeout-completion-and-adequacy-gate-verification.md`

## Next

1. next_action: `use this owner evidence to complete the guarded feature -> test-pre-merge -> develop replay for feature/tasks-closeout-gate-20260413.`
2. revisit_trigger: Re-open only if completion and guarded adequacy later need to consume a broader execution-closeout contract than the current owner-bound `tasks.md`, or if same-line merge delegation starts bypassing this check again.
