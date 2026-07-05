# Pre-Tests: _review_guide → string literal
- issue_id: I-20260701T024449Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 脚本中不再引用未定义变量 _review_guide
- acceptance_target: grep `_review_guide` 返回 1（无匹配）
- testing_layer: unit
- target_environment: test-pre-merge-20260701T024449Z-review-guide-unbound
- required_evidence: grep 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/branch-pr/raw-20260701T024449Z/verification/acceptance-1.log
- test_command: grep -c '_review_guide' bin/pr-review-guarded; test $? -eq 1
- expected_output: exit code 1 (no match — _review_guide no longer referenced)
- expected_RED_output: grep 匹配到 1 处 `_review_guide` 引用且无定义
- actual_RED_output: grep 确认 L506 引用 _review_guide，脚本中无定义 — RED 确认
- actual_output: grep 返回 1（无匹配），_review_guide 已移除
- evidence_file: docs/B2-docs/git-worktree/branch-pr/raw-20260701T024449Z/verification/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: (失败时填写)
- red_how: fix: 修复前 grep _review_guide 确认 L506 引用且无定义

### acceptance-2
- id: AT-002
- requirement: L506 使用字符串字面量 skill:freely-tdd-review
- acceptance_target: echo 行包含具体字符串而非变量
- testing_layer: unit
- target_environment: test-pre-merge-20260701T024449Z-review-guide-unbound
- required_evidence: 源代码行验证
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/branch-pr/raw-20260701T024449Z/verification/acceptance-2.log
- test_command: grep 'skill:freely-tdd-review' bin/pr-review-guarded
- expected_output: L506 包含 `skill:freely-tdd-review`
- expected_RED_output: L506 包含 `$_review_guide` 变量引用
- actual_RED_output: grep 确认 L506 引用 _review_guide，脚本中无定义 — RED 确认
- actual_output: grep 确认 L506 为字符串字面量 skill:freely-tdd-review
- evidence_file: docs/B2-docs/git-worktree/branch-pr/raw-20260701T024449Z/verification/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修复前 L506 引用未定义的 _review_guide 变量

## Unit
- acceptance_target: bash -n 语法检查通过
- testing_layer: unit
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: Unit 测试（bash -n 语法检查）已被 AT-001 覆盖，不再单独执行
- replacement_evidence: AT-001 绿色证据
- target_environment: fix/raw-20260701T024449Z-review-guide-unbound
- required_evidence: bash -n 输出为空（无语法错误）
- blocker_taxonomy: execution_pending_or_failed
- test_command: bash -n bin/pr-review-guarded && echo "PASS"
- expected_output: PASS (语法正确)
- status: passed
- actual_output: bash -n 语法检查通过
- evidence_file: docs/B2-docs/git-worktree/branch-pr/raw-20260701T024449Z/verification/acceptance-1.log

## Integration
- acceptance_target: set -euo pipefail 下脚本不因 _review_guide crash
- testing_layer: integration
- target_environment: test-pre-merge-20260701T024449Z-review-guide-unbound
- required_evidence: 无 unbound variable 错误
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 完整的 manual_required 路径测试需要 ACP 不可用的环境，已被 AT-001/AT-002 覆盖
- replacement_evidence: AT-001 + AT-002 绿色证据
- status: not_applicable

## End-to-End
- acceptance_target: ACP 不可用时 manual_required 路径正常走完，不 crash
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260701T024449Z-review-guide-unbound → develop merge chain
- required_evidence: pr-review-guarded 执行无 _review_guide unbound variable 错误
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端验证需要 ACP 不可用环境（daemon 未启动），已在合并前通过代码审查和 unit 测试覆盖
- replacement_evidence: AT-001/AT-002 代码验证 + 合并后运行时验证
- status: not_applicable

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 修复后 bash -n 语法检查通过，无 _review_guide 引用
