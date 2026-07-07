# Pre-Tests: cd 路径表述
- issue_id: I-20260707T085628Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 10 个命令执行位置改为 cd 路径
- acceptance_target: grep 确认 cd 路径格式
- testing_layer: unit
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T085628Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c 'cd <' docs/system/workspace/commands.md
- expected_output: ">=7"
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前无 cd 路径表述
## Unit
- acceptance_target: 纯文档
- testing_layer: unit
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯 Markdown 文档修改
- replacement_evidence: AT-001 grep
## Integration
- acceptance_target: 无集成面
- testing_layer: integration
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯文档
- replacement_evidence: AT-001
## End-to-End
- acceptance_target: 门禁链
- testing_layer: end-to-end
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 门禁链覆盖
- replacement_evidence: pr-create-guarded gate chain
## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-001 GREEN
