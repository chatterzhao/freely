# Pre-Tests: wt-create --source
- issue_id: I-20260507T0730Z-A
## Unit
- acceptance target: `--source missing shows clear error with scan file path`
- testing layer: `unit`
- target environment: `feature/raw-20260507T0730Z-source-param`
- required evidence: `CLI parsing tests`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `Script change validated by CLI invocation`
- replacement_evidence: `wt-create --raw-key X --skill Y --slug Z shows --source error`
## Integration
- acceptance target: `scan matching validates source_family`
- testing layer: `integration`
- target environment: `feature/raw-20260507T0730Z-source-param`
- required evidence: `gate output`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `./bin/governance-merge-gate --range develop..HEAD`
## End-to-End
- acceptance target: `feature→test-pre-merge→develop merge passes`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `guarded merge receipts`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge feature into test-pre-merge via pr-merge-guarded
2. Merge test-pre-merge into develop via pr-merge-guarded
## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `Script change. Merge success is verification.`
## Acceptance Items
### AT-001 source required
- id: `source-required`
- requirement: `wt-create requires --source, error points to scan file`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: ``
- case_design: `missing --source shows scan file path, --source mismatch blocked by gate`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/source-param/code-reviews/review.md`
