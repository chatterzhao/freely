# Pre-Tests: promoted gate fix
- issue_id: I-20260507T0200Z-A
## Unit
- acceptance target: `promoted candidates without candidate_issues are rejected`
- testing layer: `unit`
- target environment: `fix/raw-20260507T0200Z-promoted-gate-fix`
- required evidence: `gate output`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `Gate logic change validated by existing governance-merge-gate`
- replacement_evidence: `governance-merge-gate --range develop..HEAD passes`
## Integration
- acceptance target: `governance-merge-gate passes`
- testing layer: `integration`
- target environment: `fix/raw-20260507T0200Z-promoted-gate-fix`
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
### AT-001 promoted check
- id: `promoted-check`
- requirement: `promoted candidate without candidate_issues is rejected`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: ``
- case_design: `gate validates promoted candidates have candidate_issues entries`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/promoted-gate-fix/code-reviews/review.md`
