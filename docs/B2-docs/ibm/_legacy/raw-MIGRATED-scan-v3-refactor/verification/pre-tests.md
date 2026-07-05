# Pre-Tests: task-lifecycle-scan v3
- issue_id: I-20260627T062554Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: Cat 1a 扫出新 raw issue
- testing_layer: unit
- target_environment: fix/raw-20260627T062554Z-scan-v3-refactor
- required_evidence: 创建测试平台 issue，scan 输出 Cat 1a
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py . | python3 -c "import json,sys; d=json.load(sys.stdin); cat1=[i for i in d['items'] if i['subcategory']=='1a_fresh']; print(f'1a_fresh={len(cat1)}')"
- expected_output: "1a_fresh=2"（至少 2 个测试 issue）
- actual_output: PASS
- evidence_file:
- blocker:
^- status: passed

### acceptance-2
- acceptance_target: Cat 2a 扫出非 terminal phase
- testing_layer: unit
- target_environment: fix/raw-20260627T062554Z-scan-v3-refactor
- required_evidence: 输出含 2a_non_terminal
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py . | python3 -c "import json,sys; d=json.load(sys.stdin); non=[i for i in d['items'] if i['subcategory']=='2a_non_terminal']; print(f'2a_non_terminal={len(non)}')"
- expected_output: "2a_non_terminal=39"
- actual_output: PASS
- evidence_file:
- blocker:
^- status: passed

### acceptance-3
- acceptance_target: Cat 3 扫出 agent 未绑定
- testing_layer: unit
- target_environment: fix/raw-20260627T062554Z-scan-v3-refactor
- required_evidence: 输出含 3a_never_bound
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py . | python3 -c "import json,sys; d=json.load(sys.stdin); dead=[i for i in d['items'] if i['subcategory']=='3a_never_bound']; print(f'3a_never_bound={len(dead)}')"
- expected_output: "3a_never_bound=1"
- actual_output: PASS
- evidence_file:
- blocker:
^- status: passed

### acceptance-4
- acceptance_target: 无 push=176 误报
- testing_layer: unit
- target_environment: fix/raw-20260627T062554Z-scan-v3-refactor
- required_evidence: scan 不含旧 platform_sync_batch
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py . | python3 -c "import json,sys; d=json.load(sys.stdin); batch=[i for i in d['items'] if 'platform_sync' in i.get('subcategory','')]; print(f'batch={len(batch)}'); assert len(batch)==0"
- expected_output: "batch=0"
- actual_output: PASS
- evidence_file:
- blocker:
^- status: passed

## Unit
- acceptance_target: 所有 8 个子类分叉正确

## Integration
- not_applicable_reason: pre-merge 阶段无法执行集成测试
- not_applicable_explanation: 需合入 develop 后启动 freely daemon 验证
- acceptance_target: scan 输出与手动统计一致（之前已验证 5 类测试全通过）
- testing_layer: integration
- target_environment: test-pre-merge-20260627T062554Z-scan-v3-refactor
- required_evidence: 三类分叉无遗漏

## End-to-End
- not_applicable_reason: pre-merge 阶段无法执行端到端测试
- not_applicable_explanation: 需合入 develop 后在真实环境验证
- acceptance_target: freely daemon 启动后可消费新 scan 结果
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: manager patrol 不再被 push=176 误报干扰

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: pre-merge 阶段
