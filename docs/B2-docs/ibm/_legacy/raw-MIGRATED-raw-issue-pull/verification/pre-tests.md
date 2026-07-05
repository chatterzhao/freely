# Pre-Tests: raw-issue-pull
- issue_id: I-20260507T0600Z-A
## Unit
- acceptance target: `raw-issue-pull finds and materializes platform raw issue`
- testing layer: `unit`
- target environment: `feature/raw-20260507T0600Z-raw-issue-pull`
- required evidence: `pull output with platform_ids`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `Script tested via CLI invocation`
- replacement_evidence: `raw-issue-pull --raw-key 20260506T1000Z returns issue #231`
## Integration
- acceptance target: `governance-merge-gate passes`
- testing layer: `integration`
- target environment: `feature/raw-20260507T0600Z-raw-issue-pull`
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
### AT-001 pull works
- id: `pull-works`
- requirement: `raw-issue-pull finds and materializes platform raw issue with platform_ids`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: ``
- case_design: `raw-issue-pull --raw-key 20260506T1000Z returns github issue_id: "231"`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/raw-issue-pull/code-reviews/review.md`
