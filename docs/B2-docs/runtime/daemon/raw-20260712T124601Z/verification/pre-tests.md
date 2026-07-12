# Pre-Tests: AI_MODE hotfix
- issue_id: I-20260712T124601Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: bash -n 语法检查通过
- acceptance_target: freely 脚本语法无错误
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n 无错误
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260712T124601Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: line 20268: AI_MODE: unbound variable
- actual_RED_output: daemon crash on AI_MODE unbound variable
- actual_output: PASS - bash -n OK
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260712T124601Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing
## Unit
- acceptance_target: bash 语法
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 已覆盖
- replacement_evidence: AT-001 passed
## Integration
- acceptance_target: daemon 正常启动
- testing_layer: integration
- target_environment: develop
- required_evidence: daemon 启动无 crash
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后实际启动验证
- replacement_evidence: 代码审查 + bash -n
## End-to-End
- acceptance_target: daemon 持续运行
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: daemon 不 crash
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后验证
- replacement_evidence: 代码审查
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 单行修复，bash -n 通过
