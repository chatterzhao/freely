# Pre-Tests: commands.md 执行位置
- issue_id: I-20260707T065926Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 10 命令各有执行位置
- acceptance_target: grep 确认 10 个 "执行位置" 字段
- testing_layer: unit
- target_environment: test-pre-merge-20260707T065926Z-commands-md-worktree-requirements
- required_evidence: grep -c "执行位置" ≥ 10
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T065926Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "执行位置" docs/system/workspace/commands.md
- expected_output: 10
- expected_RED_output: 修改前 0
- actual_RED_output: 0
- actual_output: 10
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T065926Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前无执行位置字段
## Unit
- acceptance_target: 纯文档修改
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯 Markdown 文档修改
- replacement_evidence: AT-001 grep 验证
## Integration
- acceptance_target: 无集成面
- testing_layer: integration
- target_environment: test-pre-merge-20260707T065926Z-commands-md-worktree-requirements
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯文档
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
