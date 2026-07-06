# Issue: runtime-concurrent-start-stop-followthrough-governance

- issue_id: `I-20260408-0231-A`
- title: `Runtime concurrent start-stop followthrough governance`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-concurrent-start-stop-followthrough-governance`
- issue-name: `runtime-concurrent-start-stop-followthrough-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260408T120500Z/candidates.md#c-20260408-0231-a`
- source_brainstorm: `docs/B1-docs/raw-20260408T120500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/raw-20260408-0231/verification/pre-tests.md
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-concurrent-start-stop-followthrough-governance.md`
- verification_artifact_dir: docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/raw-20260408-0231/code-reviews
- depends_on:
  - `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
  - `docs/B2-docs/ibm/project-command-semantics-and-restore-work-governance/issues/project-command-semantics-and-restore-work-governance.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/tests/test-freely-status-latest-generated-manager-continuity-surface`
- created_at: `2026-04-11`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`C-20260408-0231-A` started as a two-part packet:

1. align `status` / `fleet-status` generated continuity truth with the latest continuity on disk
2. prevent same-project duplicate-supervisor churn across degraded bootstrap attach, stop followthrough, and stop-marker cleanup

The first half is already absorbed on canonical `develop`. The remaining open work is narrower and operationally real:

- degraded process inspection can still mis-handle a healthy same-project supervisor that is within bootstrap grace
- `freely stop --project` previously targeted only the pid-file owner instead of every discovered same-project supervisor
- supervisor cleanup could clear the project stop marker too early while another same-project supervisor was still alive

That remaining work needs a bounded develop-bound owner instead of staying as candidate-only closeout notes on the old mixed packet.

## Scope

1. Preserve attach/reuse when a same-project supervisor is still inside bootstrap grace under degraded inspection.
2. Ensure `freely stop --project` terminates all discovered same-project supervisors for the target project, not only the pid-file owner.
3. Preserve the stop marker until the last same-project supervisor exits.
4. Keep the already-landed generated-truth status half explicitly out of scope except as adjacent regression evidence.
5. Carry a lawful issue/pre-tests/progress/verification chain so the remaining runtime followthrough can merge to `develop`.

## Non-Goals

1. Do not reopen the generated status-surface alignment half already absorbed by canonical `develop`.
2. Do not widen into broader watchdog, worker recovery, or runtime provenance governance.
3. Do not redesign generic process-discovery policy beyond the bounded same-project bootstrap/stop followthrough.
4. Do not mix the separate checkpoint-risk preflight capability discussion into this owner.

## Acceptance

1. Same-project bootstrap grace under degraded process inspection prefers attach/reuse over duplicate repair.
2. `freely stop --project` terminates every discovered same-project supervisor and does not leave sibling supervisors alive.
3. Stop-marker cleanup only clears the marker once no other same-project supervisor remains alive.
4. The already-landed generated-truth read-path remains green on adjacent regression replay.
5. The develop-bound diff is backed by a concrete issue/progress/review chain rather than candidate-only notes.

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-project-start-lock`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-does-not-double-launch-during-degraded-starting-grace`
- `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `bash docs/system/workspace/scripts/tests/test-freely-status-latest-generated-manager-continuity-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-restart-storm-status-surface`
- `git diff --check`
- `./bin/governance-check`

## Completion

- `docs/B1-docs/raw-20260408T120500Z/candidates.md`
- `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/issues/runtime-concurrent-start-stop-followthrough-governance.md`
- `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/brainstorms/b-runtime-concurrent-start-stop-followthrough-governance.md`
- `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/prd.md`
- `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/pre-tests.md`
- `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/tasks.md`
- `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/code-reviews/20260411-runtime-concurrent-start-stop-followthrough-implementation-decision.md`
- `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/code-reviews/20260411-runtime-concurrent-start-stop-followthrough-verification.md`
- `docs/progress/workspace-routing-foundation/p-runtime-concurrent-start-stop-followthrough-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-does-not-double-launch-during-degraded-starting-grace`
- `docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
- `docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-project-start-lock`

## Next

- Completed on canonical `develop` via guarded merge `bf7e5a16`.
- Post-merge closeout verification is recorded in `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/code-reviews/20260411-runtime-concurrent-start-stop-followthrough-canonical-closeout-verification.md`.
- Reopen only if canonical `develop` again regresses same-project bootstrap attach reuse, project-scoped stop breadth, or stop-marker preservation.
