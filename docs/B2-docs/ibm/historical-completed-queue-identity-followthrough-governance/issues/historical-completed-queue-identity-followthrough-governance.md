# Issue: historical-completed-queue-identity-followthrough-governance

- issue_id: `I-20260412-1230-A`
- title: Historical completed-queue identity followthrough governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `historical-completed-queue-identity-followthrough-governance`
- issue-name: `historical-completed-queue-identity-followthrough-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260412/candidates.md#c-20260412-1230-a`
- source_brainstorm: `docs/B1-docs/raw-20260412/brainstorms.md`
- reopen_of_issue: `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/issues/milestone-completed-queue-closeout-governance.md`
- reopen_reason: `guarded develop replay still warns because docs/milestones.md carries the completed watchdog owner under legacy candidate identity C-20260324-0405-A instead of canonical issue identity I-20260324-0405`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/historical-completed-queue-identity-followthrough-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-historical-completed-queue-identity-followthrough-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/historical-completed-queue-identity-followthrough-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/issues/milestone-completed-queue-closeout-governance.md`
  - `docs/epics/workspace-routing-foundation/watchdog-restart-storm-and-process-churn-governance/issues/watchdog-restart-storm-and-process-churn-governance.md`
  - `docs/system/workspace/scripts/quality/governance-check`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Canonical milestone queue policy is already frozen, but one historical completed owner still survives in `docs/milestones.md` under its old candidate identity. That keeps guarded develop replays noisy and makes it harder to distinguish a real new governance regression from stale historical queue drift.

## Scope

1. Replace the completed watchdog queue item's legacy `C-*` identity with its canonical `I-*` issue identity.
2. Preserve the original watchdog owner issue/progress/review evidence instead of reopening its implementation scope.
3. Record this as a narrow followthrough of completed-queue closeout governance.
4. Prove guarded develop replay no longer emits the legacy-identity warning.

## Non-Goals

1. Do not reopen watchdog runtime signal behavior.
2. Do not redesign milestone queue format or add queue auto-repair.
3. Do not reopen the broader completed-queue governance owner beyond this historical identity drift.
4. Do not modify unrelated completed queue items.

## Acceptance

1. The affected completed queue item uses canonical issue identity `I-20260324-0405`.
2. The queue item still points to the same canonical watchdog owner evidence.
3. `./bin/governance-check` passes in the dedicated followthrough worktree.
4. A guarded develop replay no longer emits the completed watchdog legacy-identity warning.

## Completion

- `docs/B1-docs/raw-20260412/brainstorms.md`
- `docs/B1-docs/raw-20260412/candidates.md`
- `docs/epics/workspace-routing-foundation/historical-completed-queue-identity-followthrough-governance/issues/historical-completed-queue-identity-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/historical-completed-queue-identity-followthrough-governance/prd.md`
- `docs/epics/workspace-routing-foundation/historical-completed-queue-identity-followthrough-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/historical-completed-queue-identity-followthrough-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/historical-completed-queue-identity-followthrough-governance/code-reviews/20260412-historical-completed-queue-identity-followthrough-verification.md`
- `docs/progress/workspace-routing-foundation/p-historical-completed-queue-identity-followthrough-governance.md`
- `docs/milestones.md`

## Verification

- `./bin/governance-check`
- `freely wt-create test-pre-merge-20260412-watchdog-completed-identity-followthrough --base develop`
- `freely pr-merge-guarded test-pre-merge-20260412-watchdog-completed-identity-followthrough feature/watchdog-completed-identity-followthrough-20260412`
- `freely pr-merge-guarded develop test-pre-merge-20260412-watchdog-completed-identity-followthrough`

## Next

- Completed once canonical `develop` absorbs this narrow identity writeback and the warning disappears from guarded replay.
