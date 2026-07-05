# Pre-Tests: Skill rename + I→B→M

- issue_id: I-20260506T1200Z-A

## Unit
- acceptance target: `All old skill names replaced, no remaining references.`
- testing layer: `unit`
- target environment: `feature/raw-20260506T1200Z-ibm-skill-rename`
- required evidence: `grep for old names returns 0`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `Pure rename + documentation restructure. No executable code.`
- replacement_evidence: `grep -rn doc-pre-brainstorm-execution docs/ returns 0 in scope`

## Integration
- acceptance target: `governance-merge-gate passes with renamed skills.`
- testing layer: `integration`
- target environment: `feature/raw-20260506T1200Z-ibm-skill-rename`
- required evidence: `governance-merge-gate output`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `./bin/governance-merge-gate --range develop..HEAD`

## End-to-End
- acceptance target: `feature→test-pre-merge→develop merge passes all gates.`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `guarded merge receipts`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge feature into test-pre-merge via freely pr-merge-guarded.
2. Merge test-pre-merge into develop via freely pr-merge-guarded.

## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `Pure documentation rename. No runtime behavior change.`

## Acceptance Items

### AT-001 rename completeness
- id: `rename-complete`
- requirement: `All doc-pre-brainstorm-execution/doc-ibm-execution replaced in scope.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: ``
- case_design: `grep for old names returns 0 in non-historical dirs.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/ibm-skill-rename/code-reviews/review.md`

### AT-002 guarded merge
- id: `merge-chain`
- requirement: `feature→test-pre-merge→develop merge passes all gates.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: ``
- case_design: `Merge feature into test-pre-merge, then test-pre-merge into develop via pr-merge-guarded.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/ibm-skill-rename/code-reviews/review.md`
