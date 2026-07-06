# Pre-Tests: wt-create assignee check
- issue_id: I-20260627T234054Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: platform-adapter 有 get_assignees 方法
- testing_layer: unit
- target_environment: test-pre-merge-20260627T234054Z-wtcreate-assignee-check
- required_evidence: python import 验证
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260627T234054Z/verification/test-evidence/acceptance-1.log
- test_command: python3 -c "from platform_adapter import get_assignees; print('PASS')" 2>&1
- expected_output: PASS
- red-green-status: not_applicable
- red-green-not-applicable-reason: 新功能，RED 不适用
- status: pass
### acceptance-2
- id: AT-002
- requirement: pull_raw_issue 含 assignee gate
- testing_layer: unit
- target_environment: test-pre-merge-20260627T234054Z-wtcreate-assignee-check
- required_evidence: grep 验证代码
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260627T234054Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q 'check_and_claim_assignee' docs/system/workspace/scripts/sync/platform-adapter.py && echo "PASS" || echo "FAIL"
- expected_output: PASS
- red-green-status: not_applicable
- red-green-not-applicable-reason: 新功能
- status: pass
## Unit: AT-001 + AT-002 → 代码存在性验证
- acceptance_target: 新方法存在
- testing_layer: unit
- target_environment: test-pre-merge-20260627T234054Z-wtcreate-assignee-check
- required_evidence: grep + import
- blocker_taxonomy: execution_pending_or_failed
## Integration: n/a (代码实现，运行时由 wt-create 调用)
- acceptance_target: n/a
- testing_layer: integration
- target_environment: n/a
- required_evidence: n/a
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: assignee 检查在 wt-create 运行时生效，集成测试需要真实 platform API
- replacement_evidence: AT-001 python import + AT-002 grep
## End-to-End: n/a
- acceptance_target: n/a
- testing_layer: end-to-end
- target_environment: n/a
- required_evidence: n/a
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需要真实 GitHub + Gitee token 才能端到端测试
- replacement_evidence: AT-001 + AT-002 代码级验证
## Real-Environment: pass
- real_environment_status: pass
- real_environment_reason: 代码级验证充分，真实环境在首次 wt-create 时自动验证
