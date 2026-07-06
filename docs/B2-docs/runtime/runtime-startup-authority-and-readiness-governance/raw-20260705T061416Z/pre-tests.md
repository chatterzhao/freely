# Pre-Tests: runtime-startup-authority-and-readiness-governance

## Unit
- acceptance target: `Supervisor validation rejects fake argv processes unless runtime startup authority was actually published.`
- testing layer: `unit`
- target environment: `feature/runtime-startup-authority-and-readiness-governance-20260413`
- required evidence: `focused runtime ownership regression`
- blocker taxonomy: `definition_missing`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-fake-supervisor-argv-does-not-validate`.

## Integration
- acceptance target: `Same-project start, daemon ready, and stop followthrough all honor authoritative startup truth.`
- testing layer: `integration`
- target environment: `feature/runtime-startup-authority-and-readiness-governance-20260413`
- required evidence: `verification artifact plus focused runtime regressions`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-ignores-fake-supervisor-argv`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-start-serializes-same-project-concurrent-starts`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`.
6. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `No separate end-to-end harness is required because the bounded executable seam is the local runtime startup control plane already exercised by the focused start/daemon/stop regressions.`
- testing layer: `end_to_end`
- target environment: `local runtime boundary`
- required evidence: `verification artifact records the local daemon-ready and same-project-start replay`
- blocker taxonomy: `definition_missing`
1. Record the local startup-authority replay in the verification artifact instead of creating a second external harness.

## Real-Environment
- acceptance target: `No separate hosted environment is required because the bounded defect is local runtime authority publication and readiness truth.`
- testing layer: `real_environment`
- target environment: `local runtime boundary`
- required evidence: `local daemon-ready and same-project-start replay recorded in verification artifact`
- blocker taxonomy: `definition_missing`
- real_environment_status: `pass`
- real_environment_reason: `The executable seam is the local runtime startup control plane, and it is exercised directly by the focused start/daemon/stop regressions.`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner does not depend on an external hosted surface beyond the local runtime control plane.`
- replacement_evidence: `Focused local runtime regressions plus verification review are sufficient for this bounded owner.`

## Acceptance Items

### Fake supervisor hints stay non-authoritative
- id: `fake-supervisor-rejected`
- requirement: `A process with supervisor-like argv alone does not validate as the project supervisor.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Replace argv-only supervisor truth with runtime-published authority.`
- case_design: `Start a fake argv process, run supervisor validation, and assert it is rejected without published identity truth.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/code-reviews/20260413-runtime-startup-authority-and-readiness-verification.md`

### Daemon ready waits for published startup truth
- id: `daemon-ready-requires-published-truth`
- requirement: `Daemon start does not report running until the current launch has published startup truth.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Gate daemon ready semantics on authoritative supervisor truth.`
- case_design: `Seed a fake supervisor-like process first, then verify daemon start ignores it and returns the actual published supervisor.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/code-reviews/20260413-runtime-startup-authority-and-readiness-verification.md`

### Same-project start serializes through startup publication
- id: `same-project-start-publishes-before-unlock`
- requirement: `Concurrent same-project start paths do not reopen the attach or repair race before startup truth is published.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Hold the start lock through startup truth publication.`
- case_design: `Replay the concurrent-start regression and confirm startup truth serializes the project launch.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/code-reviews/20260413-runtime-startup-authority-and-readiness-verification.md`

### Guarded promote proves premerge adequacy
- id: `develop-promote-startup-authority-proof`
- requirement: `A guarded test-pre-merge replay proves this owner carries explicit premerge-integration adequacy before develop promotion.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `Replay the startup-authority regressions and governance gate from a disposable test-pre-merge branch before guarded promote to develop.`
- case_design: `Merge the feature lane into a disposable test-pre-merge batch, rerun the startup-authority regression set plus governance-check there, and record the replay in a closeout verification artifact that the develop gate can consume.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/code-reviews/20260413-runtime-startup-authority-and-readiness-closeout-verification.md`
