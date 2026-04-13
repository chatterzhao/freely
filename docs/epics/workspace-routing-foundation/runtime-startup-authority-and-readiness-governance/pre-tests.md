# Pre-Tests: runtime-startup-authority-and-readiness-governance

## Unit

- acceptance target: `Runtime startup authority is no longer inferred from fake or ghost supervisor argv strings.`
- testing layer: `unit`
- target environment: `feature/runtime-startup-authority`
- required evidence: `focused startup-authority regression output`
- blocker taxonomy: `definition_missing`
1. Add and run a fake-supervisor rejection regression.
2. Add and run a launch-truth-ready regression for daemon start.

## Integration

- acceptance target: `Same-project startup, attach-or-wait, and stop cleanup all consult one authoritative launch model.`
- testing layer: `integration`
- target environment: `feature/runtime-startup-authority`
- required evidence: `runtime regression output plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-does-not-double-launch-during-degraded-starting-grace`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`.
3. Add and run a focused bootstrap-publication-boundary regression.
4. Run `./bin/governance-check`.

## End-to-End

- acceptance target: `Real-repo foreground and daemon bounded starts obey the same launch-authority model.`
- testing layer: `end_to_end`
- target environment: `local Freely dogfood repo`
- required evidence: `real-repo replay captured in verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Capture one bounded foreground replay showing one authoritative launch during startup.
2. Capture one bounded daemon replay showing ready only after current-launch startup truth exists.

## Real-Environment

- acceptance target: `Canonical dogfood replay must confirm that startup-authority truth matches real Freely runtime behavior.`
- testing layer: `real_environment`
- target environment: `local self-hosting Freely repository`
- required evidence: `artifact-backed local replay`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pending`
- real_environment_reason: `Synthetic acceptance is not sufficient for this owner because the bug was discovered on the real self-hosting repository.`
- not_applicable_reason: `none`
- not_applicable_explanation: `none`
- replacement_evidence: `none`

## Acceptance Items

### Fake supervisor is rejected

- id: `fake-supervisor-rejected`
- requirement: `A process that only imitates supervisor argv must not validate as authoritative runtime ownership.`
- surface_kind: `unit`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Replace argv resemblance as the decisive supervisor-validation contract.`
- case_design: `Spawn a fake argv process, attempt validation, and assert rejection.`
- evidence_level: `unit`
- status: `pending`
- artifact_ref: `pending://verification`

### One launch becomes authoritative during bootstrap

- id: `single-authoritative-bootstrap`
- requirement: `Same-project bootstrap yields one authoritative launch and later starters attach, wait, or boundedly repair against that truth.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Publish startup truth before later starters classify the launch.`
- case_design: `Trigger bounded concurrent startup during the bootstrap window and assert one authoritative launch plus lawful attach-or-wait behavior.`
- evidence_level: `integration`
- status: `pending`
- artifact_ref: `pending://verification`

### Daemon ready follows current launch truth

- id: `daemon-ready-follows-launch-truth`
- requirement: `Daemon start reports ready only after the current launch has published startup truth.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Rework daemon-ready checks to depend on launch truth instead of PID resemblance.`
- case_design: `Replay daemon startup and assert ready is withheld until current-launch truth is published.`
- evidence_level: `integration`
- status: `pending`
- artifact_ref: `pending://verification`

### Real-repo replay matches the repaired model

- id: `real-repo-startup-authority-parity`
- requirement: `The repaired startup-authority model holds on the real self-hosting Freely repository, not only on synthetic fixtures.`
- surface_kind: `real_env`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Replay bounded foreground and daemon starts on the real repo and record the resulting authority truth.`
- case_design: `Use the real self-hosting repo as the project target and compare runtime events, live-status, and cleanup behavior against the repaired model.`
- evidence_level: `real_env`
- status: `pending`
- artifact_ref: `pending://verification`
