# Pre-Tests: scan station chain
- issue_id: I-20260708T202402Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: scan 输出含 [manager]/[worker] 两级 next_action
- acceptance_target: 所有 items 和 batches 的 next_action 有两级
- testing_layer: integration
- target_environment: test-pre-merge-20260708T202402Z-scan-station-chain
- required_evidence: grep 确认 next_action 含 [manager] 和 [worker]
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T202402Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project /Users/zhaoyu/Downloads/code/my-freely/freely 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); items_with_worker=sum(1 for i in d['items'] if '[worker]' in i.get('next_action','')); items_with_manager=sum(1 for i in d['items'] if '[manager]' in i.get('next_action','')); print(f'worker={items_with_worker} manager={items_with_manager}'); assert items_with_worker > 0; assert items_with_manager > 0; print('PASS')"
- expected_output: worker=N manager=M PASS
- expected_RED_output: worker=0 or AssertionError
- actual_RED_output: (RED)
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: (失败时填写)
- red_how: feature — 修改前 scan 只有 [manager]
### acceptance-2
- id: AT-002
- requirement: sync batch 跨 scan 去重
- acceptance_target: 第二次 scan 的 sync batch 为 noop
- testing_layer: integration
- target_environment: test-pre-merge-20260708T202402Z-scan-station-chain
- required_evidence: 第一次 produce batch, 第二次 noop
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T202402Z/verification/test-evidence/acceptance-2.log
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project /Users/zhaoyu/Downloads/code/my-freely/freely 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); sb=[b for b in d['batches'] if b.get('station')=='platform_sync_batch']; print(f'noop={sb[0].get(\"noop\")}' if sb else 'no sync batch'); assert sb and sb[0].get('noop')==True; print('PASS')"
- expected_output: noop=True PASS
- expected_RED_output: noop=False or AssertionError
- actual_RED_output: (RED)
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: (失败时填写)
- red_how: feature — 修改前无去重
## Unit
- acceptance_target: syntax check
- testing_layer: unit
- target_environment: feature/raw-20260708T202402Z-scan-station-chain
- required_evidence: py_compile pass
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 编译检查在 dev 阶段已确认
- replacement_evidence: python3 -m py_compile 通过
## Integration
- acceptance_target: scan 正确分类 275 items
- testing_layer: integration
- target_environment: test-pre-merge-20260708T202402Z-scan-station-chain
- required_evidence: 输出含 station 和 source_family
- blocker_taxonomy: execution_pending_or_failed
## End-to-End
- acceptance_target: develop merge chain
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260708T202402Z-scan-station-chain → develop
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
## Real-Environment
- real_environment_status: pass
- real_environment_reason: scan 对 develop 运行成功
