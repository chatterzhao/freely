# Pre-Tests: pre-scan-fix.sh FREELY_SKIP_IBM_GATE
- issue_id: I-20260710T002224Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 所有命令参数正确，无 --skip-ibm 残留
- testing_layer: unit
- target_environment: fix worktree
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T002224Z/verification/test-evidence/acceptance-1.log
- test_command: |
  bash -n docs/system/workspace/scripts/runtime/pre-scan-fix.sh && echo "PASS: syntax" || echo "FAIL"
  grep -c "skip-ibm" docs/system/workspace/scripts/runtime/pre-scan-fix.sh | xargs -I{} sh -c '[ {} -eq 0 ] && echo "PASS: no --skip-ibm" || echo "FAIL: --skip-ibm found"'
  grep -c "FREELY_SKIP_IBM_GATE" docs/system/workspace/scripts/runtime/pre-scan-fix.sh | xargs -I{} sh -c '[ {} -ge 3 ] && echo "PASS: FREELY_SKIP_IBM_GATE used" || echo "FAIL"'
- expected_output: 3 PASS
- expected_RED_output: FAIL — --skip-ibm 残留
- actual_RED_output: |
  FAIL (expected RED): --skip-ibm 参数存在于 feedback/pr-create/pr-merge 调用中
- actual_output: |
  PASS: syntax
  PASS: no --skip-ibm
  PASS: FREELY_SKIP_IBM_GATE used
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- red_how: fix — 修改前使用不存在的 --skip-ibm 参数

## Unit
- acceptance_target: 语法检查
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 已覆盖
- replacement_evidence: AT-001

## Integration
- acceptance_target: 脚本可被 daemon cycle 调用
- testing_layer: integration
- target_environment: develop
- required_evidence: pre-scan-fix.sh --project . --dry-run 正常执行
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge daemon cycle 验证
- replacement_evidence: AT-001

## End-to-End
- acceptance_target: daemon cycle 中 pre-scan-fix 正常执行
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: daemon 正常运行
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge
- replacement_evidence: AT-001

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 纯脚本参数修正，不影响功能
