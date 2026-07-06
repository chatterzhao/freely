# Pre-Tests: runtime-start-stop-lifecycle-and-process-leak-governance

## Unit
- acceptance target: `No separate unit seam is required because the bounded executable surface is the integrated runtime shell contract around start, daemon start, stop, and runtime failure cleanup.`
- testing layer: `unit`
- target environment: `feature/runtime-process-leak-20260417`
- required evidence: `focused runtime shell regressions plus owner verification artifacts`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The contract lives in integrated runtime script behavior across start-lock truth, repeated-start rejection, process discovery, and AI failure cleanup, so the focused shell regressions are already the smallest stable executable boundary.`
- replacement_evidence: `Focused runtime shell regressions, governance-check, and owner verification artifacts cover the bounded executable seam without inventing a fake narrower unit.`

## Integration
- acceptance target: `The bounded runtime lifecycle contract rejects repeated user starts, cleans lawful start-lock edge cases, converges stop on discovered same-project relaunchers, and materializes AI fast-exit failures as runtime failures.`
- testing layer: `integration`
- target environment: `feature/runtime-process-leak-20260417`
- required evidence: `focused regression output plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-precheck-ignores-self-owned-start-lock`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-rejects-when-runtime-already-running`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-releases-start-lock-when-launch-fails`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-interruption-manager-fast-path-control-validation`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-lifecycle-trace-log`.
6. Run `bash docs/system/workspace/scripts/tests/test-freely-start-lock-cleans-stalled-active-owner`.
7. Run `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`.
8. Run `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-self-owned-start-lock`.
9. Run `bash docs/system/workspace/scripts/tests/test-freely-start-rejects-when-runtime-already-running`.
10. Run `bash docs/system/workspace/scripts/tests/test-freely-start-releases-start-lock-when-startup-fails`.
11. Run `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-discovered-watchers-and-dispatchers`.
12. Run `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-detects-codex-session-permission-failure`.
13. Run `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-detects-fast-exit-iflow-local-state-failure`.
14. Run `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-iflow-descendants-on-runtime-failure`.
15. Run `git diff --check`.
16. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `A guarded feature -> test-pre-merge -> develop chain can evaluate this owner against explicit premerge-integration adequacy instead of candidate-only runtime notes.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-runtime-lifecycle-20260417`
- required evidence: `guarded merge replay plus premerge verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `freely pr-merge-guarded test-pre-merge-runtime-lifecycle-20260417 feature/runtime-process-leak-20260417`.
2. Re-run the focused regression set in `premerge-integration` on the disposable batch.
3. Run `./bin/test-lane premerge-integration -- ./bin/governance-check`.

## Real-Environment
- acceptance target: `Canonical develop preserves the bounded runtime lifecycle contract after guarded promote, and Freely can still start, surface runtime state, and stop cleanly from the protected worktree.`
- testing layer: `real_environment`
- target environment: `develop`
- required evidence: `post-merge followthrough commands plus canonical closeout verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `The real protected-branch execution surface is explicitly reserved for the immediate post-merge followthrough replay on canonical develop; premerge adequacy for guarded promote is already proven by the disposable test-pre-merge batch and closeout verification artifact, so no separate hosted environment is missing before the guarded merge.`
- not_applicable_reason: `post_merge_only`
- not_applicable_explanation: `This owner's protected worktree runtime replay is lawful only after guarded promote to canonical develop; the required post-merge acceptance happens immediately after that merge rather than as a missing pre-merge environment.`
- replacement_evidence: `Premerge focused regressions, governance-check, and the guarded closeout verification artifact prove develop-merge adequacy, while canonical develop followthrough closes the protected-worktree runtime surface immediately after merge.`

## Acceptance Items

### Repeated user start rejects while runtime is active
- id: `repeat-start-rejects-active-runtime`
- requirement: `Repeated user-facing start rejects instead of silently attaching to an already running same-project runtime.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#1`
- case_design: `Start or simulate an active same-project runtime, rerun freely start, and assert the command rejects without spawning an extra runtime chain.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260417-0445/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-verification.md`

### Repeated daemon start rejects while runtime is active
- id: `repeat-daemon-start-rejects-active-runtime`
- requirement: `Repeated user-facing daemon start rejects instead of relaunching a duplicate runtime.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#1`
- case_design: `Simulate an already running same-project runtime, rerun freely daemon start, and assert the command rejects without creating a second daemon/runtime chain.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260417-0445/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-verification.md`

### Start-lock edge cases remain lawful
- id: `start-lock-edge-cases-stay-lawful`
- requirement: `Start-lock handling tolerates self-owned and orphaned hints, cleans stale active owners, and releases the lock on launch failure.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#2`
- case_design: `Replay self-owned lock, orphaned ai pid, stale active-owner lock, and launch-failure cleanup regressions and confirm the runtime keeps only lawful start-lock truth.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260417-0445/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-verification.md`

### Stop converges on discovered same-project relaunchers
- id: `stop-converges-on-discovered-relaunchers`
- requirement: `Stop followthrough terminates discovered same-project watchdog and interruption-dispatcher processes.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#3`
- case_design: `Seed multiple same-project watcher and dispatcher processes, run freely stop, and confirm the discovered relaunch-capable processes are terminated.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260417-0445/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-verification.md`

### AI fast-exit failures stay contained
- id: `ai-fast-exit-failures-stay-contained`
- requirement: `Local .iflow state failures are materialized as runtime failures and the whole AI descendant tree is terminated.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#4`
- case_design: `Replay local .iflow fast-exit failure fixtures and assert monitor-ai-cli records runtime failure truth while terminating the full descendant tree.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260417-0445/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-verification.md`

### Guarded promote proves runtime lifecycle adequacy
- id: `develop-promote-runtime-lifecycle-adequacy`
- requirement: `A guarded test-pre-merge replay proves this owner carries explicit premerge-integration adequacy before guarded promotion to develop.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#6`
- case_design: `Merge feature/runtime-process-leak-20260417 into test-pre-merge-runtime-lifecycle-20260417 with pr-merge-guarded, rerun the focused regression set plus governance-check there, and record the replay in a closeout verification artifact the develop gate can consume.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260417-0445/code-reviews/20260419-runtime-start-stop-lifecycle-and-process-leak-develop-promote-verification.md`
