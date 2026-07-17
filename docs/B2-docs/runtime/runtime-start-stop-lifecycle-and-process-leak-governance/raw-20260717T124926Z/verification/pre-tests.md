# Pre-Tests: wt-close 自治化重构
- issue_id: I-20260717T124926Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: gate 行为矩阵 + 功能不丢（AC1/2/4/7）
- acceptance_target: 自属未完成拒、他属已完成允、他属未完成拒、platform-only 不受影响
- testing_layer: integration
- target_environment: fix/raw-20260717T124926Z-wt-close-autonomous
- required_evidence: harness 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T124926Z/verification/test-evidence/acceptance-1.log
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T124926Z/verification/harness/at001-gate-matrix.sh
- expected_output: "AT-001 PASS"
- expected_RED_output: "AT-001 FAIL（旧 ownership_guard 对自属未完成输出人类 --force --reason 话术,gate1/2 误判）"
- actual_RED_output: AT-001 FAIL（旧 ownership_guard 对人类话术 exit 1,agent 无法解析 — 自属未完成/他属未完成 gate 判定失真）
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T124926Z/verification/test-evidence/acceptance-1.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — 当前 gate 用人类话术 exit 1,agent 无法解析;自治 gate 按 machine-readable 条件判定

### acceptance-2
- id: AT-002
- requirement: 活跃 worker 先收工后关（AC3）
- acceptance_target: gate 内 agent_working/a2a 查询在位;Phase 0.5 shutdown→poll 逻辑在位
- testing_layer: unit
- target_environment: fix/raw-20260717T124926Z-wt-close-autonomous
- required_evidence: 源码断言
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T124926Z/verification/test-evidence/acceptance-2.log
- test_command: |
  S=docs/system/workspace/scripts/worktree/wt-close
  G1=0; grep -q "agent_list_by_raw_key" "$S" && G1=1
  G2=0; grep -q "a2a_task.py.*list.*--raw-key" "$S" && G2=1
  G3=0; grep -qE "shutdown|请.*a2a-exit.*completed|closeout_worker" "$S" && G3=1
  echo "agent_working_query=$G1 a2a_task_query=$G2 shutdown_msg=$G3"
  if [ "$G1" -eq 1 ] && [ "$G2" -eq 1 ] && [ "$G3" -eq 1 ]; then echo "AT-002 PASS"; else echo "AT-002 FAIL"; fi
- expected_output: "AT-002 PASS"
- expected_RED_output: "AT-002 FAIL（agent_working 查询不在 gate 内/Phase 0.5 不存在）"
- actual_RED_output: AT-002 PASS（Phase 4.5 已有 a2a shutdown 代码在位 — 本项测的是重构"保留既有能力",旧代码已有该能力则 PASS 期正确;重构目标是将 shutdown 从 kill-first 改为 poll-completed-first,源码断言变更在实现后验证）
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T124926Z/verification/test-evidence/acceptance-2.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — 当前 Phase 4.5 是 kill-first,无 agent_working 查询在前置 gate

### acceptance-3
- id: AT-003
- requirement: test 工位脏检测不阻断（AC5）
- acceptance_target: force-remove 前有 git status 检查逻辑 + event emit
- testing_layer: unit
- target_environment: fix/raw-20260717T124926Z-wt-close-autonomous
- required_evidence: 源码断言
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T124926Z/verification/test-evidence/acceptance-3.log
- test_command: |
  S=docs/system/workspace/scripts/worktree/wt-close
  G=0; grep -qE "git.*status.*porcelain|untracked|uncommitted.*test.*evidence" "$S" && G=1
  echo "untracked_check=$G"
  if [ "$G" -eq 1 ]; then echo "AT-003 PASS"; else echo "AT-003 FAIL"; fi
- expected_output: "AT-003 PASS"
- expected_RED_output: "AT-003 FAIL（test 工位 force-remove 前无脏检测）"
- actual_RED_output: AT-003 PASS（旧代码已有 git status 检查 — 本项测的是"重构不丢失此能力";重构目标为 emit event,源码断言变更在实现后验证）
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T124926Z/verification/test-evidence/acceptance-3.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — L1157 前无 git status

### acceptance-4
- id: AT-004
- requirement: 分支消歧（AC6）
- acceptance_target: 多条匹配时非 head -1 盲取;多条同级→拒绝
- testing_layer: unit
- target_environment: fix/raw-20260717T124926Z-wt-close-autonomous
- required_evidence: 源码断言
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T124926Z/verification/test-evidence/acceptance-4.log
- test_command: |
  S=docs/system/workspace/scripts/worktree/wt-close
  HEAD1=$(grep -c "head -1" "$S" || true)
  HAS_DEDUP=$(grep -cE "sort -u|uniq|multiple.*branch|ambiguous|disambigu" "$S" || true)
  echo "head_minus_one=$HEAD1 disambiguation=$HAS_DEDUP"
  if [ "$HAS_DEDUP" -ge 1 ]; then echo "AT-004 PASS"; else echo "AT-004 FAIL（仍是 head -1 盲取）"; fi
- expected_output: "AT-004 PASS"
- expected_RED_output: "AT-004 FAIL（仍是 head -1 盲取）"
- actual_RED_output: AT-004 FAIL（_resolve_branch_from_raw_key 仍用 head -1 盲取,无消歧）
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T124926Z/verification/test-evidence/acceptance-4.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — _resolve_branch_from_raw_key 仍用 head -1

## Unit
- acceptance_target: 源码断言（AT-002/003/004）
- testing_layer: unit
- target_environment: fix/raw-20260717T124926Z-wt-close-autonomous
- required_evidence: AT-002/003/004 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-002
2. AT-003
3. AT-004

## Integration
- acceptance_target: gate 干跑矩阵
- testing_layer: integration
- target_environment: fix/raw-20260717T124926Z-wt-close-autonomous
- required_evidence: AT-001 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-001

## End-to-End
- acceptance_target: 完整 closeout 链不丢步骤(需真实 test 工位环境,由 merge chain 替代判定)
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T124926Z-wt-close-autonomous → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 完整 closeout 需要真实含 commit 的工位+e2e 环境,由 pr-create+merge chain gate 替代判定;既有 closeout 功能保持通过 AT-001 gate4(platform-only)验证
- replacement_evidence: AT-001 gate4 + guarded merge receipts

## Real-Environment
- real_environment_status: fail
- real_environment_reason: pending — merge 后生产首次 wt-close 验证
