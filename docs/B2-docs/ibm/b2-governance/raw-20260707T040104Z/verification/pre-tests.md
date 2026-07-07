# Pre-Tests: pre-commit.sh git update-ref 禁止项
- issue_id: I-20260707T040104Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: pre-commit.sh develop 拦截消息包含 git update-ref 禁止项
- acceptance_target: 1 行文本插入正确
- testing_layer: unit
- target_environment: test-pre-merge-20260707T040104Z-pre-commit-blocked-update-ref
- required_evidence: grep 确认新行存在
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T040104Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "git update-ref develop" .githooks/pre-commit.sh
- expected_output: 返回 >0
- expected_RED_output: develop 分支 pre-commit.sh 无此禁止项
- actual_RED_output: grep "git update-ref develop" .githooks/pre-commit.sh → 0
- actual_output: grep "git update-ref develop" → 1
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T040104Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: grep 确认修改前 pre-commit.sh 缺少该禁止项

## Unit
- acceptance_target: 1 行文本插入无语法影响
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 不适用——纯文本行插入
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 在 heredoc 文本块中插入 1 行，不涉及任何可执行代码。grep 确认文本存在即可。
- replacement_evidence: grep 确认文本存在 (AT-001)

## Integration
- acceptance_target: 无集成面
- testing_layer: integration
- target_environment: test-pre-merge-20260707T040104Z-pre-commit-blocked-update-ref
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 1 行文本插入，无集成交互
- replacement_evidence: AT-001 grep 验证

## End-to-End
- acceptance_target: pr-create-guarded 门禁链通过
- testing_layer: end-to-end
- target_environment: test-pre-merge → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: E2E 由 pr-create-guarded 门禁链覆盖
- replacement_evidence: pr-create-guarded gate chain 全部通过

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 1 行 GREP 验证通过
