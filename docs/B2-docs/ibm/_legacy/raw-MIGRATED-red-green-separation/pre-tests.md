# Pre-Tests: RED/GREEN separation
- issue_id: I-20260624T235907Z-A
## Unit
- acceptance target: Python syntax
- testing layer: unit
- target environment: fix worktree
- required evidence: compile passes
- blocker taxonomy: not_applicable
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: logic change in gate only
- replacement_evidence: AT-001
## Integration
- acceptance target: gate fails on missing actual_output
- testing layer: integration
- target environment: test-pre-merge worktree
- required evidence: gate correctly rejects placeholder actual_output
- blocker taxonomy: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: verified by merge
- replacement_evidence: AT-001
## End-to-End
- acceptance target: wt-close without --force when GREEN evidence present
- testing layer: end-to-end
- target environment: develop merge chain
- required evidence: normal wt-close passes
- blocker taxonomy: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: verified by merge
- replacement_evidence: AT-001
## Acceptance Items
### AT-001 green-check
- id: green-check
- requirement: gate checks actual_output not file existence
- evidence_level: mock
^- status: passed
- artifact_ref: docs/B2-docs/red-green-separation/code-reviews/implementation-decision.md
## Real-Environment
- real_environment_status: pass
- real_environment_reason: verified by merge
