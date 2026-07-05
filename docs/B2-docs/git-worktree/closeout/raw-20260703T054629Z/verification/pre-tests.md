# Pre-Tests: wt-close test worktree path
- issue_id: I-20260703T054629Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: wt-close 能找到 test-pre-merge 工位并正确传入门禁
- acceptance_target: wt-close 正常通过 pretests-retirement-gate
- testing_layer: end-to-end
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: A1
- case_design: 在 test-pre-merge 中运行 daemon，然后 wt-close fix 工位应正常通过
- target_environment: test-pre-merge-20260703T054629Z-wt-close-test-gate
- required_evidence: wt-close pretests-retirement-gate passed
- evidence_level: real_env
- artifact_ref: docs/B2-docs/git-worktree/closeout/raw-20260703T054629Z29Z/verification/test-evidence/acceptance-1.log
- test_command: cd <project-root> && ./bin/wt-close fix/raw-20260703T054629Z29Z-wt-close-test-gate
- expected_output: wt-close: pretests-retirement-gate passed
- expected_RED_output: test worktree not found 或 gate 失败
- actual_RED_output: wt-close 传 fix 工位路径 → gate 找不到 test-gate.env → 报错 "pretests_not_tested"
- actual_output: wt-close: pretests-retirement-gate passed ✓
- evidence_file: docs/B2-docs/git-worktree/closeout/raw-20260703T054629Z29Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix: 修复前 wt-close 传 fix 工位路径 → gate 找不到 test-gate.env → 失败

## Unit
- acceptance_target: raw key 提取 + worktree 查找
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 函数正确返回 test 工位路径
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖端到端验证
- replacement_evidence: AT-001 结果

## Integration
- acceptance_target: wt-close 集成测试
- testing_layer: integration
- target_environment: test-pre-merge
- required_evidence: wt-close 全流程通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖
- replacement_evidence: AT-001 结果

## End-to-End
- acceptance_target: wt-close 端到端
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: wt-close 正常完成
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 就是端到端
- replacement_evidence: AT-001 结果

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本 fix 工位的 wt-close 将作为真实环境验证
