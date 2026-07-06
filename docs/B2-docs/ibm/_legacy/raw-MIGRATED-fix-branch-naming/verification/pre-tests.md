# Pre-Tests: fix-execution branch naming
- issue_id: I-20260507T0100Z-A

## Unit
- acceptance target: `fix-execution SKILL.md uses fix/* in all 5 changed locations`
- testing layer: `unit`
- target environment: `fix/raw-20260507T010000Z-fix-execution-branch-naming`
- required evidence: `grep confirms fix/* prefix`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `Doc-only change. Validation is text-based grep.`
- replacement_evidence: `grep confirms all 5 locations use fix/*`

## Integration
- acceptance target: `governance-merge-gate passes`
- testing layer: `integration`
- target environment: `fix/raw-20260507T010000Z-fix-execution-branch-naming`
- required evidence: `gate output`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `./bin/governance-merge-gate --range develop..HEAD`

## End-to-End
- acceptance target: `fix→test-pre-merge→develop merge passes`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `guarded merge receipts`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge fix into test-pre-merge via pr-merge-guarded
2. Merge test-pre-merge into develop via pr-merge-guarded

## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `Doc-only change. Merge success is verification.`

## Acceptance Items
### AT-001 fix naming
- id: `fix-naming`
- requirement: `fix-execution SKILL.md uses fix/* in all branch references`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: ``
- case_design: `grep fix/ in fix-execution SKILL.md confirms 5 locations`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/fix-branch-naming/code-reviews/review.md`
