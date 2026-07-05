# Issue: runtime-closeout-selfhost-validation-followthrough-governance

- issue_id: `I-20260419-0333-A`
- title: `Runtime closeout selfhost validation followthrough governance`
- phase_state: `completed`
- completed_at: `2026-04-28`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-closeout-selfhost-validation-followthrough-governance`
- issue-name: `runtime-closeout-selfhost-validation-followthrough-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260419-0333/candidates.md#c-20260419-0333-a`
- source_brainstorm: `docs/B1-docs/raw-20260419-0333/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/pre-tests.md`
- tasks_path: `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-closeout-selfhost-validation-followthrough-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-lifecycle-receipt-followthrough-governance/issues/runtime-lifecycle-receipt-followthrough-governance.md`
  - `docs/epics/freely-product-architecture/worktree-tool-boundary-bootstrap-governance/issues/worktree-tool-boundary-bootstrap-governance.md`
- created_at: `2026-04-19`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

The receipt-only closeout followthrough lane already proved that the main runtime lifecycle implementation had landed. But the preserved checkpoint on `feature/checkpoint-runtime-closeout-selfhost-validation-20260419` still carried real follow-on behavior that was not bound to any lawful owner:

1. `freely daemon start` should reuse a healthy same-project supervisor instead of launching a duplicate detached chain during closeout/self-host replay.
2. Ambiguous `project-start.lock` directories with missing `state.env` should be cleaned when no runtime is actually active.
3. `interruption-manager-handler` should fast-path the closeout/self-host prompts that repeatedly appear during worktree retirement and supervisor continuation routing, while leaving the generic AI fallback path intact.

Those changes share one trigger surface: post-merge closeout and self-host validation on the same bounded runtime lane. They are too concrete to leave as an undocumented checkpoint and too narrow to reopen broader runtime or routing architecture work.

## Scope

1. Reuse an already healthy same-project supervisor from `freely daemon start` instead of relaunching another daemon-run process.
2. Clean ambiguous `project-start.lock` directories with missing state when no runtime is active, without relaxing lawful active-lock waiting.
3. Add bounded interruption-manager fast paths for cleanup-oriented worker handoff and manager/worker continuation prompts surfaced during closeout/self-host validation.
4. Preserve explicit regression coverage for both the new fast-path behavior and the generic codex/cc fallback path.
5. Carry this checkpoint through a lawful issue/progress/pre-tests/review chain instead of treating the branch as execution truth by fiat.

## Non-Goals

1. Do not reopen the already-merged runtime lifecycle receipt-ledger repair scope.
2. Do not redesign generic interruption intent classification beyond the bounded closeout/self-host prompts preserved in this checkpoint.
3. Do not widen into unrelated runtime startup authority, manager continuity, or broader self-host observability work.
4. Do not retire the checkpoint worktree as if it were pure archive state before this bounded follow-on is merged or explicitly dropped.

## Acceptance

1. Repeated `freely daemon start` on a healthy same-project runtime reuses the live supervisor and does not launch an extra daemon-run process.
2. Ambiguous missing-state start locks are cleaned only when there is no active runtime to preserve.
3. Closeout-oriented and broad-manager-supervision interruption prompts take the new bounded fast paths, while generic prompts still invoke the AI fallback path for both `codex` and `cc`.
4. The owner carries concrete issue, pre-tests, tasks, progress, and verification truth in this worktree.
5. Guarded promotion can later evaluate this checkpoint as one bounded owner instead of an undocumented branch-local stash.

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-start-lock-cleans-ambiguous-missing-state`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-releases-start-lock-when-launch-fails`
- `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler`
- `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler-cc`
- `git diff --check`
- `./bin/governance-check`

## Closeout

1. Keep the current checkpoint worktree as the bounded implementation lane for this owner.
2. Add a focused verification artifact from the already-passing regressions in this worktree.
3. After governance truth is complete, decide whether this owner can move directly toward guarded premerge replay or needs one real-repo self-host replay first.
