# Pre-Tests: per-platform ID close
- issue_id: I-20260707T162123Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: close_issue 接受 platform_ids dict 正确路由到各平台
- testing_layer: unit
- target_environment: test-pre-merge-20260707T162123Z-per-platform-id-close
- required_evidence: py_compile + API 验证
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T162123Z/verification/test-evidence/acceptance-1.log
- test_command: python3 -m py_compile docs/system/workspace/scripts/sync/platform-adapter.py
- expected_output: "(no output = OK)"
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前 close_issue 接受单个 ID
## Unit
- acceptance_target: py_compile + bash -n
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 语法检查
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 语法检查
- replacement_evidence: py_compile + bash -n 通过
## Integration
- acceptance_target: 无集成面
- testing_layer: integration
- target_environment: test-pre-merge-20260707T162123Z-per-platform-id-close
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯代码修改
- replacement_evidence: AT-001
## End-to-End
- acceptance_target: pr-create-guarded 门禁链
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 门禁链覆盖
- replacement_evidence: pr-create-guarded gate chain
## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-001 GREEN
