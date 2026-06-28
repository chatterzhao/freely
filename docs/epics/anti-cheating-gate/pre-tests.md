# Pre-Tests: anti-cheating gate
- issue_id: I-20260624T235907Z-A
## Unit
- acceptance target: Python syntax
- testing layer: unit
- target environment: fix worktree
- required evidence: compile passes
- blocker taxonomy: not_applicable
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: gate logic only
- replacement_evidence: AT-001
## Integration
- acceptance target: gate rejects all-mock pre-tests
- testing layer: integration
- target environment: test-pre-merge worktree
- required evidence: gate blocks with anti-cheating message
- blocker taxonomy: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: verified by merge
- replacement_evidence: AT-001
## End-to-End
- acceptance target: gate passes for real tests
- testing layer: end-to-end
- target environment: develop merge chain
- required evidence: pr-create passes with real tests
- blocker taxonomy: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: verified by merge
- replacement_evidence: AT-001
## Acceptance Items
### AT-001 anti-cheat
- id: anti-cheat
- requirement: gate hard-rejects all-mock/not_applicable pre-tests
- evidence_level: mock
- status: pass
- artifact_ref: docs/epics/anti-cheating-gate/code-reviews/implementation-decision.md
## Real-Environment
- real_environment_status: pass
- real_environment_reason: verified by merge
