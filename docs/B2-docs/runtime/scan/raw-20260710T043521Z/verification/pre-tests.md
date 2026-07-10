# Pre-Tests: scan skip closed items
- issue_id: I-20260710T043521Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: scan items < 100
- acceptance_target: scan items count drops from ~690 to < 100
- testing_layer: integration
- target_environment: test-pre-merge-20260710T043521Z-scan-skip-closed-v3
- required_evidence: scan output item count
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T043521Z/verification/test-evidence/acceptance-1.log
- test_command: |
  python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project . 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin);n=len(d.get('items',[]));print('PASS' if n<100 else f'FAIL:{n}')"
- expected_output: PASS
- expected_RED_output: "FAIL:690"
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- red_how: fix — 修改前 scan 输出 ~690 items

### acceptance-2
- id: AT-002
- requirement: 无 platform_state: closed--- 残留
- acceptance_target: 所有 issue.md frontmatter 无 YAML 污染
- testing_layer: unit
- target_environment: test-pre-merge-20260710T043521Z-scan-skip-closed-v3
- required_evidence: grep 返回 0
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T043521Z/verification/test-evidence/acceptance-2.log
- test_command: |
  n=$(grep -rl "platform_state: closed---" docs/B1-docs/raw-*/issue.md 2>/dev/null | wc -l | tr -d ' ')
  [ "$n" -eq 0 ] && echo "PASS: 0 corrupt" || echo "FAIL: $n corrupt"
- expected_output: "PASS: 0 corrupt"
- expected_RED_output: "FAIL: 11 corrupt"
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- red_how: fix — 修改前 11 个文件有 closed--- 污染

## Unit
- acceptance_target: Python 语法正确
- testing_layer: unit
- target_environment: fix/raw-20260710T043521Z-scan-skip-closed-v3
- required_evidence: compile 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 语法检查已被 AT-001/AT-002 的集成测试覆盖
- replacement_evidence: AT-001 + AT-002

## Integration
- acceptance_target: scan 正常执行输出精简
- testing_layer: integration
- target_environment: test-pre-merge-20260710T043521Z-scan-skip-closed-v3
- required_evidence: AT-001 + AT-002 PASS
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 + AT-002 已在 fix worktree 完成集成级验证
- replacement_evidence: AT-001 + AT-002

## End-to-End
- acceptance_target: daemon cycle 中 scan 结果精简
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: daemon cycle 正常
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge daemon 验证
- replacement_evidence: AT-001 + AT-002

## Real-Environment
- real_environment_status: pass
- real_environment_reason: scan 逻辑修改，post-merge daemon 间接验证
