# Pre-Tests
- issue_id: I-20260625T020333Z-A
## Unit
- acceptance target: help text only, no logic changes
- testing layer: unit
- target environment: fix worktree
- required evidence: bash -n passes
- blocker taxonomy: not_applicable
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: text-only change
- replacement_evidence: AT-001
## Integration
- acceptance target: error messages render correctly
- testing layer: integration
- target environment: fix worktree
- required evidence: all sections show
- blocker taxonomy: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: text rendering verified
- replacement_evidence: AT-001
## End-to-End
- acceptance target: help output shows abandon-only guidance
- testing layer: end-to-end
- target environment: develop merge chain
- required evidence: --help text updated
- blocker taxonomy: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: verified by --help output
- replacement_evidence: AT-001
## Acceptance Items
### AT-001 force-semantics
- id: force-semantics
- requirement: --force described as abandon-only with counter-examples
- evidence_level: mock
^- status: passed
- artifact_ref: docs/epics/force-abandon-only/code-reviews/implementation-decision.md
## Real-Environment
- real_environment_status: pass
- real_environment_reason: --help output verified
