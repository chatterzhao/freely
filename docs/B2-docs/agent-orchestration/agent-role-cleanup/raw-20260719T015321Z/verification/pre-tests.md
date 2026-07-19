# Pre-Tests: lead-agent.md 引用清理 + governance-check 修复
- issue_id: I-20260719T015321Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: governance-check 不再因 lead-agent.md 缺失而 FAIL
- acceptance_target: governance-check 输出中无 lead-agent 相关 FAIL
- testing_layer: unit
- target_environment: test-pre-merge-20260719T015321Z-lead-agent-ref-cleanup
- required_evidence: governance-check 输出中 lead-agent 相关 FAIL 已消失
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/agent-role-cleanup/raw-20260719T015321Z/verification/test-evidence/acceptance-1.log
- test_command: freely governance-check 2>&1 | grep 'lead-agent'
- expected_output: (no output — grep exit 1, 无 lead-agent FAIL)
- expected_RED_output: "[FAIL] missing file: docs/system/workspace/agents/lead-agent.md"
- actual_RED_output: (develop HEAD 有此 FAIL)
- actual_output: (no grep hits — lead-agent FAIL removed)
- evidence_file: acceptance-1.log
- red-green-status: green
- status: pass
- blocker:
- red_how: 当前 develop HEAD governance-check 因 lead-agent.md 缺失 + skill 路径不存在而 FAIL

### acceptance-2
- id: AT-002
- requirement: 全项目无 lead-agent 悬空引用
- acceptance_target: grep 在 system/workspace 下无命中（排除 start-lead-agent.sh 脚本自身）
- testing_layer: unit
- target_environment: test-pre-merge-20260719T015321Z-lead-agent-ref-cleanup
- required_evidence: grep exit 1（无匹配）
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/agent-role-cleanup/raw-20260719T015321Z/verification/test-evidence/acceptance-2.log
- test_command: grep -rn 'lead-agent' docs/system/workspace/ --include="*.md" --include="*.sh" | grep -v 'start-lead-agent'
- expected_output: (no output — grep exit 1)
- expected_RED_output: 5 处悬空引用命中
- actual_RED_output: (develop HEAD 有 5 处命中)
- actual_output: (no hits — all references cleaned)
- evidence_file: acceptance-2.log
- red-green-status: green
- status: pass
- blocker:
- red_how: 当前有 5 处悬空引用（governance-check, start-lead-agent.sh, auto-loop-orchestrator, context-source-skill, project-agents-contract）

## Unit
- acceptance_target: governance-check 中 lead-agent.md 引用已删除，skill 路径指向实际存在的文件
- testing_layer: unit
- target_environment: fix-raw-20260719T015321Z-lead-agent-ref-cleanup
- required_evidence: AT-001/AT-002 覆盖此层
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/AT-002 直接验证引用清理，已覆盖单元层
- replacement_evidence: AT-001/AT-002 输出

## Integration
- acceptance_target: 全项目引用链一致，governance-check 可正常运行
- testing_layer: integration
- target_environment: test-pre-merge-20260719T015321Z-lead-agent-ref-cleanup
- required_evidence: AT-001 governance-check 无 lead-agent FAIL + AT-002 全项目无悬空引用覆盖此层
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 本 fix 为纯引用清理，无集成点代码。AT-001（governance-check）+ AT-002（grep 全项目引用）已覆盖集成层验证
- replacement_evidence: AT-001/AT-002 GREEN 输出

## End-to-End
- acceptance_target: pr-create-guarded 可通过 IBM governance gate，成功提 PR
- testing_layer: end-to-end
- target_environment: fix-raw-20260719T015321Z-lead-agent-ref-cleanup → develop merge chain
- required_evidence: pr-create-guarded governance gate pass
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 本 fix 无运行时行为变更，E2E 验证等价于 pr-create-guarded gate pass。AT-001/AT-002 的 test-pre-merge 验证已覆盖真实环境
- replacement_evidence: pr-create-guarded gate pass 记录

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 引用清理完成，governance-check 不再因 lead-agent.md 缺失而阻塞
