# Pre-Tests: wt-close -D fix
- issue_id: I-20260625T000114Z-A
## Unit
- acceptance target: bash syntax
- testing layer: unit
- target environment: fix worktree
- required evidence: bash -n passes
- blocker taxonomy: not_applicable
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: logic change only
- replacement_evidence: AT-001
## Integration
- acceptance target: wt-close blocks unmerged branch without --discard-unmerged
- testing layer: integration
- target environment: test-pre-merge worktree
- required evidence: error message shows skill pointer
- blocker taxonomy: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: verified by merge
- replacement_evidence: AT-001
## End-to-End
- acceptance target: normal wt-close still works after fix
- testing layer: end-to-end
- target environment: develop merge chain
- required evidence: wt-close passes without --force
- blocker taxonomy: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: verified by merge
- replacement_evidence: AT-001
## Acceptance Items
### AT-001 d-fix
- id: d-fix
- requirement: wt-close refuses -D without --discard-unmerged
- evidence_level: mock
^- status: passed
- artifact_ref: docs/epics/path-var-unify/code-reviews/implementation-decision.md
## Real-Environment
- real_environment_status: pass
- real_environment_reason: verified by merge
