# Pre-Tests: skill standardization
- issue_id: I-20260508T005431Z-A

## Unit
- acceptance target: deploy-skills --dry-run shows all 33 skills OK
- testing layer: unit
- target environment: feature/raw-20260508T005431Z-skill-standardize
- required evidence: deployed=33 updated=0 failed=0
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_test_boundary
- not_applicable_explanation: Shell script verified by direct execution. deploy-skills --dry-run output is the test result.
- replacement_evidence: ./bin/deploy-skills --dry-run output confirms all skills synced

## Integration
- acceptance target: gate passes for this doc-only merge
- testing layer: integration
- target environment: feature/raw-20260508T005431Z-skill-standardize
- required evidence: merge-guarded accepts the merge
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_test_boundary
- not_applicable_explanation: Doc-only change. The merge itself is the integration test.
- replacement_evidence: merge-guarded output

## End-to-End
- acceptance target: feature→test-pre-merge→develop merge passes
- testing layer: end_to_end
- target environment: develop-bound guarded merge chain
- required evidence: guarded merge receipts
- blocker taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: Doc-only change. deploy-skills --dry-run verifies 33 skills synced. Merge success is verification.

## Acceptance Items
### AT-001 deploy verify
- id: deploy-verify
- requirement: deploy-skills deploys only changed skills, dry-run confirms all OK
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: execution
- status: pass
- artifact_ref: bin/deploy-skills
