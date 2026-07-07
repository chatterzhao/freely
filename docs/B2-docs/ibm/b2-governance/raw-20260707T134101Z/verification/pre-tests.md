# Pre-Tests: 平台硬编码清理
- issue_id: I-20260707T134101Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 所有硬编码 repo 名已清除 + issue-sync 顺序修复
- acceptance_target: grep 确认 0 个 hardcoded repo + test sync 逻辑存在
- testing_layer: unit
- target_environment: test-pre-merge-20260707T134101Z-platform-adapter-audit
- required_evidence: grep 确认
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T134101Z/verification/test-evidence/acceptance-1.log
- test_command: grep -rn "chatterzhao\|zhaoquan" bin/ docs/system/workspace/scripts/worktree/ --include="*.sh" | grep -v ".bak\|README\|#"
- expected_output: "(no output)"
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前多处 hardcoded repo
## Unit
- acceptance_target: bash -n 全部通过
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: bash -n 3 文件通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: shell 文本修改，bash -n 验证
- replacement_evidence: bash -n 全部通过
## Integration
- acceptance_target: 无集成面
- testing_layer: integration
- target_environment: test-pre-merge-20260707T134101Z-platform-adapter-audit
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯文本替换
- replacement_evidence: AT-001 grep
## End-to-End
- acceptance_target: pr-create-guarded 门禁链
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 门禁链覆盖
- replacement_evidence: pr-create-guarded gate chain
## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-001 GREEN + bash -n 通过
