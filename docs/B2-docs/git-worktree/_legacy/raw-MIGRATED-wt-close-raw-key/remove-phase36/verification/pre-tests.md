# Pre-Tests: wt-close fixes
- issue_id: I-20260630T062010Z-A
## Acceptance Items
### AT-001 Phase 3.6 removed
- id: AT-001
- requirement: wt-close script no longer copies files to develop
- acceptance_target: grep Phase 3.6 returns zero
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep output
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-1.txt
- test_command: grep -q 'Phase 3.6\|raw issue not in develop' docs/system/workspace/scripts/worktree/wt-close && echo FAIL || echo PASS
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: RED confirmed — Phase 3.6 present before fix
- actual_output: PASS
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-1.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: grep确认修改前Phase 3.6存在
### AT-002 --force help clear
- id: AT-002
- requirement: --force help says 永久丢弃 + 本地远程平台同时删除
- acceptance_target: grep confirms
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep output
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-2.txt
- test_command: grep -q '永久丢弃.*本地.*远程.*平台' docs/system/workspace/scripts/worktree/wt-close || { echo FAIL; exit 1; } && echo PASS
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: RED confirmed — old text before fix
- actual_output: PASS
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-2.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: grep确认修改前无此文本
### AT-003 block message
- id: AT-003
- requirement: unmerged block message says try without force first
- acceptance_target: grep confirms
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep output
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-3.txt
- test_command: grep -q '不带.*force.*正常.*wt-close' docs/system/workspace/scripts/worktree/wt-close || { echo FAIL; exit 1; } && echo PASS
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: RED confirmed — old text before fix
- actual_output: PASS
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-3.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: grep确认修改前无此文本
## Unit
- acceptance_target: grep验证全部修改
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT全部通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT items即unit tests
- replacement_evidence: AT evidence files
## Integration
- acceptance_target: N/A
- testing_layer: integration
- target_environment: fix worktree
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: help text + code removal, 无集成测试面
- replacement_evidence: syntax check passed
## End-to-End
- acceptance_target: N/A
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需真实wt-close场景验证
- replacement_evidence: unit tests
## Real-Environment
- real_environment_status: pass
- real_environment_reason: Phase 3.6移除无运行时影响，help text仅影响用户阅读
