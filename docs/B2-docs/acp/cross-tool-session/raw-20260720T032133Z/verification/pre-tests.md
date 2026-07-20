# Pre-Tests: Manager prompt 委派决策规则
- issue_id: I-20260720T032133Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: Manager prompt包含决策规则表格（含task_id列）和委派vs插话三段式指引
- acceptance_target: Manager看到agent_working视图后能正确选择prompt vs submitted
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260720T032133Z-manager-prompt-decision-rules
- required_evidence: Manager cycle log显示对已委派raw_key使用a2a_task.py prompt而非a2a-exit --state submitted
- evidence_level: real_env
- artifact_ref: docs/B2-docs/acp/cross-tool-session/raw-20260720T032133Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "a2a_task.py prompt" /tmp/freely-daemon.log
- expected_output: "1" 或更大（Manager使用了prompt而非submitted）
- expected_RED_output: "0"（修复前无prompt使用）
- actual_RED_output: 同raw_key重复submitted，prompt使用为0
- actual_output: (GREEN阶段填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- red_how: 上一轮daemon运行显示同raw_key各2条submitted，Manager从未使用prompt

## Unit
- acceptance_target: N/A — prompt模板修改，无可单元测试边界
- testing_layer: unit
- target_environment: test-pre-merge-20260720T032133Z-manager-prompt-decision-rules
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: prompt模板字符串修改，无独立可测函数边界
- replacement_evidence: 端到端AT-001覆盖

## Integration
- acceptance_target: N/A
- testing_layer: integration
- target_environment: test-pre-merge-20260720T032133Z-manager-prompt-decision-rules
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: prompt模板注入的Python查询是shell函数内嵌代码，无可分离集成边界
- replacement_evidence: AT-001覆盖

## End-to-End
- acceptance_target: Manager对新raw_key正常委派，对已有worker使用prompt跟进
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260720T032133Z-manager-prompt-decision-rules → develop
- required_evidence: guarded merge receipts + daemon运行验证
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001提供daemon级别验证
- replacement_evidence: AT-001 acceptance item

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 纯prompt模板修改，不改变代码逻辑。真实环境验证将在merge后daemon重启自动完成
