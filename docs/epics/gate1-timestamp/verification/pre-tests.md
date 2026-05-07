# Pre-Tests: GATE 1 timestamp
- issue_id: raw-20260507T0300Z
## Unit
- acceptance target: `timestamp mismatch between branch and governance chain is caught`
- testing layer: `unit`
- target environment: `fix/raw-20260507T0300Z-gate1-timestamp-check`
- required evidence: `gate output`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `Gate logic change validated by governance-merge-gate self-check`
- replacement_evidence: `gate correctly rejects timestamp mismatches`
## Integration
- acceptance target: `governance-merge-gate passes`
- testing layer: `integration`
- target environment: `fix/raw-20260507T0300Z-gate1-timestamp-check`
- required evidence: `gate output`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `./bin/governance-merge-gate --range develop..HEAD`
## End-to-End
- acceptance target: `fix→test-pre-merge→develop merge passes`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `guarded merge receipts`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge fix into test-pre-merge
2. Merge test-pre-merge into develop
## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `Gate logic fix. Merge success is verification.`
## Acceptance Items
### AT-001 timestamp check
- id: `ts-check`
- requirement: `timestamp mismatch between branch and governance chain is rejected`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: ``
- case_design: `gate detects timestamp drift in raw/C/I chain`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/gate1-timestamp/code-reviews/review.md`
