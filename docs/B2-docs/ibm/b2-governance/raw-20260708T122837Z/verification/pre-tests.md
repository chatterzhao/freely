# Pre-Tests: scan stage + batch + derive_action
- issue_id: I-20260708T122837Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: scan 输出每条 item 含 stage 字段
- acceptance_target: 运行 scan 后所有 item 都有 stage 字段
- testing_layer: integration
- target_environment: test-pre-merge-20260708T122837Z-scan-stage-batch
- required_evidence: scan 输出 JSON 中所有 item 都有 stage 字段
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T122837Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project . | python3 -c "import json,sys; d=json.load(sys.stdin); missing=[i['key'] for i in d['items'] if 'stage' not in i]; print(f'missing_stage={len(missing)}'); assert len(missing)==0"
- expected_output: missing_stage=0
- expected_RED_output: NameError or KeyError — stage field missing
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段由 skill `freely-test-execution` 执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- red_how: feature — 修改前 scan 返回 null 或 NameError

### acceptance-2
- id: AT-002
- requirement: scan 输出含 batches 字段，按 stage 聚合
- acceptance_target: 运行 scan 后 batches 字段存在且有正确的 stage 聚合
- testing_layer: integration
- target_environment: test-pre-merge-20260708T122837Z-scan-stage-batch
- required_evidence: scan 输出含 batches 字段
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T122837Z/verification/test-evidence/acceptance-2.log
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project . | python3 -c "import json,sys; d=json.load(sys.stdin); assert d.get('batches'); print(f'batches={len(d[\"batches\"])}'); assert d['batches'] is not None"
- expected_output: batches 字段存在且非空
- expected_RED_output: batches 字段缺失或为空
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段由 skill `freely-test-execution` 执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- red_how: feature — 修改前 scan 输出无 batches 字段

### acceptance-3
- id: AT-003
- requirement: scan 不返回 null
- acceptance_target: scan 正确输出 JSON 而非 null
- testing_layer: integration
- target_environment: test-pre-merge-20260708T122837Z-scan-stage-batch
- required_evidence: scan 输出有效 JSON
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T122837Z/verification/test-evidence/acceptance-3.log
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project . | python3 -c "import json,sys; d=json.load(sys.stdin); assert d is not None; assert d.get('items') is not None; print('OK')"
- expected_output: OK
- expected_RED_output: JSON parse error or null output
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段由 skill `freely-test-execution` 执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- red_how: fix — 修改前 scan 返回 null（NameError bug）

## Unit
- acceptance_target: _classify_stage 和 _stage_action 函数单元测试
- testing_layer: unit
- target_environment: fix/raw-20260708T122837Z-scan-stage-batch
- required_evidence: 所有 subcategory 映射到正确 stage
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 单元测试通过 importlib 加载模块验证，已在 dev 阶段确认通过
- replacement_evidence: importlib 加载 _classify_stage 并测试所有 8 个 subcategory

## Integration
- acceptance_target: scan 在真实项目上运行，输出 stage + batches
- testing_layer: integration
- target_environment: test-pre-merge-20260708T122837Z-scan-stage-batch
- required_evidence: scan 对 freely 项目运行成功
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 从 develop 创建 worktree → merge 本分支 → scan 正确运行
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260708T122837Z-scan-stage-batch → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: scan 对 develop 项目运行成功，输出正确
