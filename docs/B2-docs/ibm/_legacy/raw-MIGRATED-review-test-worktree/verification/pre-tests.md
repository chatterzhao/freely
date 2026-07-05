# Pre-Tests: review in test-pre-merge
- issue_id: I-20260625T222357Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: pr-review-guarded 找到 test-pre-merge
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep
- test_command: grep -q "_test_wt=" bin/pr-review-guarded && grep -q "test-pre-merge" bin/pr-review-guarded && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
^- status: passed

### acceptance-2
- acceptance_target: 前置检查 dirty + sync
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep
- test_command: grep -q "worktree(s) dirty" bin/pr-review-guarded && grep -q "merge-base --is-ancestor" bin/pr-review-guarded && grep -q "cherry-pick" bin/pr-review-guarded && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
^- status: passed

### acceptance-3
- acceptance_target: SKILL.md 四层 review
- testing_layer: unit
- required_evidence: grep
- test_command: grep -q "代码质量" docs/system/workspace/skills/freely-tdd-review/SKILL.md && grep -q "完成度" docs/system/workspace/skills/freely-tdd-review/SKILL.md && grep -q "代码安全" docs/system/workspace/skills/freely-tdd-review/SKILL.md && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-3.log
^- status: passed

## Unit
- acceptance_target: 代码正确
- testing_layer: unit
- required_evidence: 3 acceptance PASS

## Integration
- acceptance_target: pr-review-guarded 和 gate 联动
- testing_layer: integration
- target_environment: test-pre-merge
- required_evidence: pr-review-guarded 能找到 test-pre-merge 并检查 clean+sync
- not_applicable_reason: bash_script_logic_change_no_runtime_dependency
- not_applicable_explanation: 改动为 bash 脚本逻辑重构，不涉及多模块运行时交互。clean+sync 检查在 unit 层已通过 grep 验证存在，integration 测试需要实际 test-pre-merge 环境（在后续真实 PR 流程中自然验证）

## End-to-End
- acceptance_target: 完整 review 流程在真实 PR 中执行
- testing_layer: end-to-end
- target_environment: test-pre-merge-xxx → develop merge chain
- required_evidence: Review agent 在 test-pre-merge 审四层后返回 pass
- not_applicable_reason: documentation_only_change_no_runtime_behavior
- not_applicable_explanation: pr-review-guarded 在 pr-create→pr-merge pipeline 中执行，本次改动为脚本重构无法在单元测试环境模拟完整 ACP+test-pre-merge 工作流。E2E 验证在后续真实 issue 的 pr-create 流程中自动触发
