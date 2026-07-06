# Pre-tests — bash 3.2 daemon 兼容性修复

- issue_id: `I-20260429-1745-A`
- issue_path: `docs/B2-docs/runtime/bash32-daemon-compat-fix/issues/I-20260429-1745-A.md`

## Unit
- acceptance target: `The freely runtime script passes shell syntax check on macOS bash 3.2.`
- testing layer: `unit`
- target environment: `feature/fix-daemon-bash32-crash-20260429`
- required evidence: `bash -n syntax check output`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash -n docs/system/workspace/scripts/runtime/freely`.

## Integration
- acceptance target: `Daemon no longer self-terminates via supervisor.pid self-detection.`
- testing layer: `integration`
- target environment: `feature/fix-daemon-bash32-crash-20260429`
- required evidence: `focused regression for pid exclusion`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `daemon start on bash 3.2 survives beyond startup without restart loop.`
- testing layer: `end_to_end`
- target environment: `feature/fix-daemon-bash32-crash-20260429`
- required evidence: `lifecycle trace showing L010→L020→L040 passage`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `freely daemon start --project <path>` on bash 3.2 host and observe 30s stability.

## Real-Environment
- acceptance target: `The guarded promote lane carries the bash 3.2 daemon compat fixes without regression.`
- testing layer: `real_environment`
- target environment: `develop`
- required evidence: `guarded promote replay plus governance-check`
- blocker taxonomy: `protected_environment_only`
- real_environment_status: `pass`
- real_environment_reason: `Merged into develop via 83cd79eb (test-pre-merge) and 96ec25ea (fix code).`

## Acceptance Items

### Shell syntax is valid under bash 3.2
- id: `bash32-shell-syntax-valid`
- requirement: `freely runtime script passes bash -n syntax check on bash 3.2.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/bash32-daemon-compat-fix/code-reviews/20260429-bash32-daemon-compat-fix-verification.md`
- surface_kind: `unit`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1`
- case_design: `Run bash -n on the modified runtime script.`

### Daemon starts without self-termination on bash 3.2
- id: `daemon-bash32-no-self-terminate`
- requirement: `daemon start does not discover and kill itself via supervisor.pid.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/bash32-daemon-compat-fix/code-reviews/20260429-bash32-daemon-compat-fix-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2`
- case_design: `Verify resolve_active_supervisor_pid_for_start excludes $$ from the candidate pid set.`

### Governance check passes
- id: `bash32-governance-check`
- requirement: `governance-check reports no new errors.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/bash32-daemon-compat-fix/code-reviews/20260429-bash32-daemon-compat-fix-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2`
- case_design: `Run ./bin/governance-check.`
