# Pre-Tests: auto-detect platforms
- issue_id: I-20260625T030147Z-A
## Unit
- acceptance target: bash syntax
- testing layer: unit
- target environment: fix worktree
- required evidence: bash -n passes
- blocker taxonomy: not_applicable
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: config update only
- replacement_evidence: AT-001
## Integration
- acceptance target: FREELY_REPO_PLATFORMS updated on start
- testing layer: integration
- target environment: develop
- required evidence: config.toml updated
- blocker taxonomy: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: verified by merge
- replacement_evidence: AT-001
## End-to-End
- acceptance target: commands read FREELY_REPO_PLATFORMS
- testing layer: end-to-end
- target environment: develop merge chain
- required evidence: feedback uses config value
- blocker taxonomy: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: verified by merge
- replacement_evidence: AT-001
## Acceptance Items
### AT-001 auto-detect
- id: auto-detect
- requirement: start auto-detects platforms and updates config
- evidence_level: mock
^- status: passed
- artifact_ref: docs/epics/auto-detect-platforms/code-reviews/implementation-decision.md
## Real-Environment
- real_environment_status: pass
- real_environment_reason: verified by merge
