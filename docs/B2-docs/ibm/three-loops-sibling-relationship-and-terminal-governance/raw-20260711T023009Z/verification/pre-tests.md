# Pre-Tests
- issue_id: I-20260711T023009Z-A
## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: SVG 无旧 skill 名残留
- testing_layer: unit
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/three-loops-sibling-relationship-and-terminal-governance/raw-20260711T023009Z/verification/test-evidence/acceptance-1.log
- test_command: |
  ! grep -q "fix-execution\|auto-loop-orchestrator\|900s\|fork 不是" docs/system/workspace/three-loop-lifecycle.svg && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: FAIL — SVG contains fix-execution, auto-loop-orchestrator, 900s, fork不是
- actual_output: PASS — all outdated refs removed
- red-green-status: green
- status: pass
- red_how: fix
### acceptance-2
- id: AT-002
- requirement: SVG 新内容正确
- testing_layer: unit
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/three-loops-sibling-relationship-and-terminal-governance/raw-20260711T023009Z/verification/test-evidence/acceptance-2.log
- test_command: |
  grep -q "workflow-guarded-execution" docs/system/workspace/three-loop-lifecycle.svg && grep -q "180s" docs/system/workspace/three-loop-lifecycle.svg && grep -q "per-tool" docs/system/workspace/three-loop-lifecycle.svg && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: FAIL
- actual_output: PASS
- red-green-status: green
- status: pass
- red_how: fix
## Unit
- acceptance_target: SVG correctness
- testing_layer: unit
- target_environment: develop
- required_evidence: AT-001/AT-002
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 代码级验证已被 AT-001/AT-002 的 grep 检查覆盖
- replacement_evidence: AT-001/AT-002
## Integration
- acceptance_target: SVG correctness
- testing_layer: integration
- target_environment: develop
- required_evidence: AT-001/AT-002
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 代码级验证已被 AT-001/AT-002 的 grep 检查覆盖
- replacement_evidence: AT-001/AT-002
## End-to-End
- acceptance_target: SVG correctness
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: AT-001/AT-002
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 代码级验证已被 AT-001/AT-002 的 grep 检查覆盖
- replacement_evidence: AT-001/AT-002
## Real-Environment
- real_environment_status: pass
- real_environment_reason: SVG 文档修改，无运行时影响
