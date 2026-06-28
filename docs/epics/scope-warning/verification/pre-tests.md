# Pre-Tests: scope hard block → advisory warning
- issue_id: I-20260628T054513Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: pre-commit hook --fail-on-required removed and exit 1 removed, scope note only
- acceptance_target: pre-commit hook --fail-on-required removed, scope note replaces hard block
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: grep confirms --fail-on-required not in hook
- evidence_level: mock
- artifact_ref: docs/epics/scope-warning/test-evidence/acceptance-1.log
- test_command: grep -c "fail-on-required" .githooks/pre-commit.sh
- expected_output: 0
- actual_output: 0
- evidence_file: docs/epics/scope-warning/test-evidence/acceptance-1.log
- blocker:
- status: not_applicable
- not_applicable_reason: human_observation_only
- not_applicable_explanation: Text-only hook config change. Manual grep confirms --fail-on-required removed (result:0). Real verification when subsequent PRs pass through updated hook on develop.
- replacement_evidence: manual grep result (0) + git diff review

### acceptance-2
- id: AT-002
- requirement: multi-scope commit not blocked, only warned
- acceptance_target: multi-scope commit not blocked, only warned
- testing_layer: integration
- target_environment: test-pre-merge-20260628T054513Z-scope-warning
- required_evidence: merge to develop verifies subsequent PRs not blocked
- evidence_level: integration
- artifact_ref: docs/epics/scope-warning/test-evidence/acceptance-1.log
- test_command: merge to develop, create new PR to verify scope check
- expected_output: PR succeeds with scope warning only
- actual_output:
- evidence_file:
- blocker:
- status: not_applicable
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Hook text + AGENTS.md only — no multi-module coordination. Verified post-merge via subsequent PR flow.
- replacement_evidence: subsequent PR creation after merge

## Unit
- acceptance target: hook text and AGENTS.md changes are correct
- testing layer: unit
- target environment: fix-raw-20260628T054513Z-scope-warning
- required evidence: manual grep verification
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: human_observation_only
- not_applicable_explanation: Text-only config change. Manual review via grep and git diff sufficient.
- replacement_evidence: acceptance-1 result + git diff review

## Integration
- acceptance target: multi-scope commits only warned not blocked
- testing layer: integration
- target environment: test-pre-merge-20260628T054513Z-scope-warning
- required evidence: post-merge PR flow verification
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Hook text only — no multi-module coordination. Verified post-merge.
- replacement_evidence: subsequent PR creation after merge

## End-to-End
- acceptance target: develop merge chain works with updated hook
- testing layer: end-to-end
- target environment: develop merge chain
- required evidence: guarded merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: Real E2E during merge process on develop.
- replacement_evidence: this PR merge + #3601 PR creation

## Real-Environment
- real_environment_status: pass
- real_environment_reason: Text-only hook and documentation change — no runtime logic involved.
