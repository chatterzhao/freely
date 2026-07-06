# Pre-Tests: unified platform layer
- issue_id: I-20260507T0700Z-A
## Unit
- acceptance target: `Gitee title search finds orphaned issues`
- testing layer: `unit`
- target environment: `feature/raw-20260507T070000Z-unified-platform`
- required evidence: `issue-sync Gitee resolve`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `Script change validated by CLI invocation`
- replacement_evidence: `issue-sync tests`
## Integration
- acceptance target: `governance-merge-gate passes`
- testing layer: `integration`
- target environment: `feature/raw-20260507T070000Z-unified-platform`
- required evidence: `gate output`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `./bin/governance-merge-gate --range develop..HEAD`
## End-to-End
- acceptance target: `feature→test-pre-merge→develop merge passes`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `guarded merge receipts`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge feature into test-pre-merge
2. Merge test-pre-merge into develop
## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `Script change. Merge success is verification.`
## Acceptance Items
### AT-001 unified platform
- id: `unified`
- requirement: `All platforms synced via single entry point`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: ``
- case_design: `issue-sync with Gitee fallback, raw-issue-pull auto-sync`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/unified-platform/code-reviews/review.md`
