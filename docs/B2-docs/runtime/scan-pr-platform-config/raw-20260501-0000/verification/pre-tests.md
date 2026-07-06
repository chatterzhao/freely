# Pre-tests — scan-pr-platform-config

- issue_id: `I-20260501-0000-A`
- issue_path: `docs/B2-docs/runtime/scan-pr-platform-config/issues/I-20260501-0000-A.md`

## Unit

- acceptance target: `The freely runtime script passes shell syntax check.`
- testing layer: `unit`
- target environment: `hotfix/I-20260501-0000-A-scan-pr-platform-config`
- required evidence: `bash -n syntax check output`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash -n docs/system/workspace/scripts/runtime/freely`.

## Integration

- acceptance target: `PR scan function exists and governance-check passes.`
- testing layer: `integration`
- target environment: `hotfix/I-20260501-0000-A-scan-pr-platform-config`
- required evidence: `syntax validation and governance output`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash -n docs/system/workspace/scripts/runtime/freely`.
2. Run `./bin/governance-check`.

## End-to-End

- acceptance target: `PR scan surface is generated in task-source-scan JSON output.`
- testing layer: `end_to_end`
- target environment: `develop`
- required evidence: `scan JSON validation`
- blocker taxonomy: `execution_pending_or_failed`
1. Verify scan JSON includes open_pull_requests surface when FREELY_REPO_PLATFORMS is set.

## Real-Environment

- acceptance target: `The hotfix merge carries PR scan without regression.`
- testing layer: `real_environment`
- target environment: `develop`
- required evidence: `pr-merge-guarded completion plus governance-check`
- blocker taxonomy: `protected_environment_only`
- real_environment_status: `pass`
- real_environment_reason: `Hotfix merge to develop via pr-merge-guarded; governance-check verifies no regressions.`

## Acceptance Items

### Shell syntax is valid
- id: `scan-pr-shell-syntax-valid`
- requirement: `freely runtime script passes bash -n syntax check.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/scan-pr-platform-config/raw-20260501-0000/code-reviews/20260501-scan-pr-platform-config-verification.md`
- surface_kind: `unit`
- target_lane: `feature-local`
- promotion_gate: `completion`
- case_design: `Run bash -n on the modified runtime script.`

### Governance check passes
- id: `scan-pr-governance-check`
- requirement: `governance-check reports no new errors from this branch.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/scan-pr-platform-config/raw-20260501-0000/code-reviews/20260501-scan-pr-platform-config-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- case_design: `Run ./bin/governance-check and diff errors against origin/develop.`

### Shell syntax is valid (premerge-integration)
- id: `scan-pr-shell-syntax-premerge`
- requirement: `freely runtime script passes bash -n syntax check via merge flow.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/scan-pr-platform-config/raw-20260501-0000/code-reviews/20260501-scan-pr-platform-config-verification.md`
- surface_kind: `unit`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- case_design: `bash -n check passes as part of pr-merge-guarded workflow.`

### Governance check passes (premerge-integration)
- id: `scan-pr-governance-premerge`
- requirement: `governance-check passes during test-pre-merge -> develop merge.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/scan-pr-platform-config/raw-20260501-0000/code-reviews/20260501-scan-pr-platform-config-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- case_design: `Run governance-check in pr-merge-guarded flow to develop.`
