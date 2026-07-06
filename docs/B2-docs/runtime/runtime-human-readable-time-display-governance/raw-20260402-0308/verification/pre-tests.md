# Pre-Tests: runtime-human-readable-time-display-governance

## Unit
- acceptance target: `Do not invent a fake unit seam for a shell-runtime display contract whose truthful boundary is command-level behavior and guarded promotion.`
- testing layer: `unit`
- target environment: `feature/runtime-time-format-unification-20260423`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The timestamp helpers live inside the runtime shell and are exercised truthfully through focused command regressions rather than isolated pure-unit seams.`
- replacement_evidence: `Focused runtime integration regressions plus guarded promotion cover the bounded executable surface.`

## Integration
- acceptance target: `Runtime human-readable time display stays host-local for people and UTC/RFC3339 for machine truth, with current-time minting routed through shared helpers.`
- testing layer: `integration`
- target environment: `feature/runtime-time-format-unification-20260423`
- required evidence: `focused runtime regressions plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-current-timestamp-local-display-format`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-human-display-time-format-uses-shared-helper`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-machine-time-format-uses-shared-helper`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-startup-continuity-stub-materialization`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-stop-materializes-missing-manager-continuity`.
6. Run `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260423-feature-runtime-time-format-unification --issue docs/B2-docs/runtime/runtime-human-readable-time-display-governance/raw-20260402-0308/issues/runtime-human-readable-time-display-governance.md`.
7. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `Protected promotion must carry the same owner chain and keep the time-display contract intact on canonical develop.`
- testing layer: `end_to_end`
- target environment: `guarded feature -> test-pre-merge -> develop replay`
- required evidence: `merge receipts plus protected-lane verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/runtime-time-format-unification-20260423` into a fresh `test-pre-merge-*` lane via `freely pr-merge-guarded`.
2. On the protected lane, rerun the bounded time-helper regressions and stage a fresh owner review artifact.
3. Merge the protected lane into `develop` via `freely pr-merge-guarded`.
4. Confirm canonical `develop` still renders human display timestamps in host-local time while machine timestamps remain UTC-backed.

## Real-Environment
- acceptance target: `This bounded runtime formatter followthrough does not require a separate hosted environment before protected replay.`
- testing layer: `real_environment`
- target environment: `local runtime boundary`
- required evidence: `local command replay plus owner verification artifact`
- blocker taxonomy: `definition_missing`
- real_environment_status: `pass`
- real_environment_reason: `The executable boundary here is the local runtime shell contract. Local focused regressions truthfully exercise the helper unification before protected replay; no distinct hosted environment adds signal for this owner.`
- not_applicable_reason: `no_distinct_hosted_boundary`
- not_applicable_explanation: `There is no separate remote environment that would test this helper extraction more truthfully than local runtime command replays plus guarded promotion.`
- replacement_evidence: `Local command regressions and protected-lane replay provide the real executable evidence.`

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `freely ai status preserves refresh truth and adds host-local human-readable refresh output`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ai-account-switch`

### PT-2
- id: `PT-2`
- requirement: `baseline and live status surfaces render human-facing timestamps in host-local time with timezone label`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-baseline-status`

### PT-3
- id: `PT-3`
- requirement: `live-status renders runtime update and intake timestamps in host-local time without mutating stored truth`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-live-status`

### PT-4
- id: `PT-4`
- requirement: `develop-push and execution-boundary surfaces render local display timestamps`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`

### PT-5
- id: `PT-5`
- requirement: `direct develop-push status command renders defer timestamps in host-local time`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-develop-push-status-time-display`

### PT-6
- id: `PT-6`
- requirement: `intake status renders created_at in host-local time`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-human-chat-intake`

### PT-7
- id: `PT-7`
- requirement: `runtime current local display timestamps are emitted through a single shared helper`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-current-timestamp-local-display-format`

### PT-8
- id: `PT-8`
- requirement: `runtime current UTC machine timestamps are emitted through a single shared helper`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-machine-time-format-uses-shared-helper`

### Protected premerge replay preserves runtime time helper unification
- id: `premerge-runtime-time-helper-unification-proof`
- requirement: `Before guarded develop merge, the protected lane must rerun the bounded helper regressions and stage a fresh owner verification artifact for the replay.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#runtime-time-helper-unification`
- case_design: `Replay the helper-unification slice on test-pre-merge, rerun the five bounded regressions plus owner gates there, and stage a fresh premerge verification artifact before promoting into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-human-readable-time-display-governance/raw-20260402-0308/code-reviews/20260423-runtime-human-readable-time-display-helper-unification-premerge-verification.md`
