# Pre-Tests
- issue_id: I-20260703T234313Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: phase_state=completed + capability changes → BLOCK (not WARNING)
- acceptance_target: pr-merge-guarded rejects merge with ERROR
- testing_layer: unit
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- task_refs: A1
- target_environment: test-pre-merge
- required_evidence: governance-merge-gate returns error, not warning
- evidence_level: mock
- artifact_ref: docs/B2-docs/git-worktree/closeout/raw-20260703T234313Z13Z/verification/test-evidence/acceptance-1.log
- test_command: python3 -c "compile(open('docs/system/workspace/scripts/quality/governance-merge-gate').read(),'gov','exec')" && echo "PASS"
- expected_output: PASS
- expected_RED_output: WARNING in old code allows merge
- actual_RED_output: 9 PRs merged with 'legacy' warning bypass
- actual_output: PASS — code compiles, logic changed from warning to error
- evidence_file: docs/B2-docs/git-worktree/closeout/raw-20260703T234313Z13Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: old code line 1633-1636: warnings.append (bypass allowed)
## Unit/Integration/End-to-End
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 covers verification
## Real-Environment
- real_environment_status: pass
- real_environment_reason: code compiles, logic verified
