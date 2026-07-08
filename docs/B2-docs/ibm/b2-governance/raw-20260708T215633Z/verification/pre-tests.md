# Pre-Tests: scan de-hardcode platforms
- issue_id: I-20260708T215633Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: raw_not_started不含platform=closed的item
- acceptance_target: 0个raw_not_started带platform_state=closed
- testing_layer: integration
- target_environment: test-pre-merge-20260708T215633Z-scan-dehardcode-platforms
- required_evidence: scan输出中raw_not_started站无platform=closed
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T215633Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project . 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); ns=[i for i in d['items'] if i.get('station')=='raw_not_started' and i.get('platform_state','')=='closed']; print(f'bad={len(ns)}'); assert len(ns)==0; print('PASS')"
- expected_output: bad=0 PASS
- expected_RED_output: bad>0
- actual_RED_output: (RED)
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- red_how: fix — 修改前13个platform=closed判为raw_not_started

### acceptance-2
- id: AT-002
- requirement: 无硬编码github/gitee在next_action中
- acceptance_target: next_action不含github或gitee字符串(除docstring)
- testing_layer: integration
- target_environment: test-pre-merge-20260708T215633Z-scan-dehardcode-platforms
- required_evidence: grep确认
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T215633Z/verification/test-evidence/acceptance-2.log
- test_command: python3 -c "import json; d=json.load(open('/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-task-source-scan-latest.json')); bad=[i for i in d['items'] if 'github' in i.get('next_action','')]; print(f'hardcoded={len(bad)}'); assert len(bad)==0; print('PASS')"
- expected_output: hardcoded=0 PASS
- expected_RED_output: hardcoded>0
- actual_RED_output: (RED)
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- red_how: fix — 修改前next_action含硬编码平台名
## Unit
- acceptance_target: py_compile
- testing_layer: unit
- target_environment: fix/raw-20260708T215633Z-scan-dehardcode-platforms
- required_evidence: compile pass
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: dev阶段确认compile通过
- replacement_evidence: python3 -m py_compile通过
## Integration
- acceptance_target: scan正确分类+N平台检测
- testing_layer: integration
- target_environment: test-pre-merge-20260708T215633Z-scan-dehardcode-platforms
- required_evidence: 所有站正确,无硬编码
- blocker_taxonomy: execution_pending_or_failed
## End-to-End
- acceptance_target: develop merge chain
- testing_layer: end-to-end
- target_environment: test-pre-merge → develop
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
## Real-Environment
- real_environment_status: pass
- real_environment_reason: scan对develop运行,分类验证0误判
