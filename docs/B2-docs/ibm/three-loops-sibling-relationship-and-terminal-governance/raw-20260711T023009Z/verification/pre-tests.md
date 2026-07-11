# Pre-Tests
- issue_id: I-20260711T023009Z-A
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
## Unit: not_applicable (covered_by_more_realistic_required_surface)
## Integration: not_applicable (covered_by_more_realistic_required_surface)
## End-to-End: not_applicable (covered_by_more_realistic_required_surface)
## Real-Environment: pass
- real_environment_status: pass
- real_environment_reason: SVG 文档修改，无运行时影响
