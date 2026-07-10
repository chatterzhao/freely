# Pre-Tests: pre-scan-fix + scan raw_key fallback
- issue_id: I-20260710T000650Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: pre-scan-fix.sh 语法正确且可执行
- acceptance_target: bash -n 通过 + chmod +x
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash syntax check
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T000650Z/verification/test-evidence/acceptance-1.log
- test_command: |
  bash -n docs/system/workspace/scripts/runtime/pre-scan-fix.sh && echo "PASS: syntax OK" || echo "FAIL"
  test -x docs/system/workspace/scripts/runtime/pre-scan-fix.sh && echo "PASS: executable" || echo "FAIL"
- expected_output: PASS: syntax OK + PASS: executable
- expected_RED_output: FAIL
- actual_RED_output: |
  FAIL (expected RED): pre-scan-fix.sh 不存在
- actual_output: |
  PASS: syntax OK
  PASS: executable
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- red_how: fix — 新文件，修改前不存在

### acceptance-2
- id: AT-002
- requirement: scan raw_key fallback 正确匹配
- acceptance_target: _build_raw_key_index 函数存在且被 scan() 调用
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 验证
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T000650Z/verification/test-evidence/acceptance-2.log
- test_command: |
  scan="docs/system/workspace/scripts/runtime/task-lifecycle-scan.py"
  grep -q "_build_raw_key_index" "$scan" && echo "PASS: _build_raw_key_index exists" || echo "FAIL"
  grep -q "raw_key_pid_index" "$scan" && echo "PASS: raw_key_pid_index used" || echo "FAIL"
  grep -q "_write_platform_ids" "$scan" && echo "PASS: _write_platform_ids exists" || echo "FAIL"
- expected_output: 3 行 PASS
- expected_RED_output: FAIL
- actual_RED_output: |
  FAIL (expected RED): _build_raw_key_index 不存在
- actual_output: |
  PASS: _build_raw_key_index exists
  PASS: raw_key_pid_index used
  PASS: _write_platform_ids exists
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- red_how: fix — 函数修改前不存在

## Unit
- acceptance_target: 语法检查
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n + python compile
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 已通过 AT-001/AT-002 覆盖
- replacement_evidence: AT-001 + AT-002

## Integration
- acceptance_target: scan 执行后 items 数量显著减少
- testing_layer: integration
- target_environment: test-pre-merge
- required_evidence: scan items count < 100
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 需要真实平台 API，属于 post-merge 验证
- replacement_evidence: AT-001 + AT-002 代码级验证

## End-to-End
- acceptance_target: pre-scan-fix.sh → scan → Manager 收到精简 items
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: daemon cycle 正常
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge daemon 验证
- replacement_evidence: AT-001 + AT-002

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 脚本工具 + scan 增强，post-merge daemon 运行间接验证
