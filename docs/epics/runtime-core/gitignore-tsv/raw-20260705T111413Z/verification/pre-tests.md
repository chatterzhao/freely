# Pre-Tests
- issue_id: I-20260705T111413Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: .gitignore 包含 projects.tsv
- acceptance_target: grep 确认
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep
- evidence_level: integration
- artifact_ref: docs/epics/runtime-core/gitignore-tsv/raw-20260705T111413Z/verification/test-evidence/at-001.log
- test_command: grep -q "projects.tsv" .gitignore && echo PASS
- expected_output: PASS
- expected_RED_output: not found
- actual_RED_output: not in gitignore
- actual_output: PASS
- evidence_file: at-001.log
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed
- red_how: fix — .gitignore 无此条目
## Unit
- acceptance_target: AT-001
- testing_layer: unit
- target_environment: feature-local
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary
- not_applicable_explanation: gitignore check
- replacement_evidence: AT-001
## Integration
- acceptance_target: git status 无 projects.tsv untracked
- testing_layer: integration
- target_environment: test-pre-merge-*
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: trivially verified
- replacement_evidence: AT-001
## End-to-End
- acceptance_target: N/A
- testing_layer: end_to_end
- target_environment: test-pre-merge-*
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: trivial
- replacement_evidence: AT-001
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 文件已确认是机器相关全局状态
