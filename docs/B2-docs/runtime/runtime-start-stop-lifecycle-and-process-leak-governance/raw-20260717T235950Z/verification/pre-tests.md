# Pre-Tests: commands.md wt-close --force 文案同步
- issue_id: I-20260717T235950Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: commands.md §wt-close 选项表 --force 行含"自治门禁"语义，与 wt-close --help 判据（at005-usage-sync.sh 同关键词）一致
- acceptance_target: raw 验收标准（--force 行含自治门禁且与 --help 一致）
- testing_layer: integration
- target_environment: test-pre-merge-20260717T235950Z-commands-force-doc-sync
- required_evidence: harness 输出 AT001_RESULT: PASS
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T235950Z/verification/harness/at001-commands-force-sync.sh
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T235950Z/verification/harness/at001-commands-force-sync.sh <root>
- expected_output: AT001_RESULT: PASS
- expected_RED_output: 旧文案行无"自治门禁" → AT001_RESULT: FAIL
- actual_RED_output: row='| `--force` | 永久丢弃（不可恢复）。有未合并提交时需同时 `--discard-unmerged` |' 无自治门禁 → AT001_RESULT: FAIL
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T235950Z/verification/test-evidence/acceptance-1-RED.log
- red-green-status: red
- status: pending
- blocker:
- red_how: 对未修改的 commands.md 跑 harness，--force 行为旧文案（无自治门禁关键词）→ FAIL 即 RED

## Unit
- acceptance_target: N/A
- testing_layer: unit
- target_environment: N/A
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 纯文档一行修改，无可执行单元边界
- replacement_evidence: AT-001 grep 断言即全部验证面

## Integration
- acceptance_target: 文档行与 --help 真源语义一致（AT-001）
- testing_layer: integration
- target_environment: test-pre-merge-20260717T235950Z-commands-force-doc-sync
- required_evidence: AT001_RESULT: PASS
- blocker_taxonomy: execution_pending_or_failed
1. at001-commands-force-sync.sh — --force 行关键词断言

## End-to-End
- acceptance_target: feature→test-pre-merge→develop merge chain
- testing_layer: end-to-end
- target_environment: develop-bound guarded merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. pr-create/review/merge-guarded 链路收据

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 文档修改的真实消费面即 agent 阅读 commands.md，grep 断言与 --help 同判据即真实一致性验证
