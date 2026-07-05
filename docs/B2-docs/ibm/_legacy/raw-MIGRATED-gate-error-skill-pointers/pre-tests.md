# Pre-Tests: gate error skill guidance
- issue_id: I-20260625T020000Z-A
## Unit
- acceptance target: bash syntax check
- testing layer: unit
- target environment: fix worktree
- required evidence: bash -n passes
- blocker taxonomy: not_applicable
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: error text change only
- replacement_evidence: AT-001
## Integration
- acceptance target: fix branch error shows new message
- testing layer: integration
- target environment: fix worktree
- required evidence: error block contains skill guidance
- blocker taxonomy: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: verified by pr-create run
- replacement_evidence: AT-001
## End-to-End
- acceptance target: user sees fix/feat-specific guidance
- testing layer: end-to-end
- target environment: develop merge chain
- required evidence: error block renders correctly
- blocker taxonomy: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: verified by pr-create run
- replacement_evidence: AT-001
## Acceptance Items
### AT-001 error-guidance
- id: error-guidance
- requirement: gate error block shows fix/feat detection and skill guidance
- evidence_level: mock
^- status: passed
- artifact_ref: docs/epics/gate-error-skill-pointers/code-reviews/implementation-decision.md
## Real-Environment
- real_environment_status: pass
- real_environment_reason: pr-create run verifies error block renders
