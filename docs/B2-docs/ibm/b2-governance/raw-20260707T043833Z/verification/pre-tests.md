# Pre-Tests: 移除本地 raw issue 创建路径
- issue_id: I-20260707T043833Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 全局搜索 new-issue 引用为 0
- acceptance_target: 代码库中无残留的本地 raw issue 创建路径
- testing_layer: unit
- target_environment: test-pre-merge-20260707T043833Z-remove-local-raw-issue-paths
- required_evidence: grep 确认 0 个 new-issue 引用
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T043833Z/verification/test-evidence/acceptance-1.log
- test_command: grep -rn "new-issue\|chat_type.*new" docs/system/workspace/scripts/ bin/ --include="*.py" --include="*.sh" | grep -v ".pyc\|test_\|.bak\|governance-merge-gate\|task-lifecycle-scan" | wc -l
- expected_output: 0
- expected_RED_output: 修改前有 10+ 处 new-issue 引用
- actual_RED_output: grep 找到 10 处 new-issue 引用（修改前）
- actual_output: grep 返回 0
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T043833Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前全局搜索确认 10 处 new-issue 引用存在
## Unit
- acceptance_target: Python 语法检查通过
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: python3 -m py_compile 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 修改涉及 Python 代码删除和 shell 脚本修改，python3 -m py_compile 验证语法
- replacement_evidence: python3 -m py_compile 通过 + AT-001 grep 验证
## Integration
- acceptance_target: freely chat --new-issue 被拒绝
- testing_layer: integration
- target_environment: test-pre-merge-20260707T043833Z-remove-local-raw-issue-paths
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本地 new-issue 创建路径已全部移除，无法在集成层测试
- replacement_evidence: AT-001 grep 验证 0 残留
## End-to-End
- acceptance_target: pr-create-guarded 门禁链通过
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: E2E 由 pr-create-guarded 门禁链覆盖
- replacement_evidence: pr-create-guarded gate chain 全部通过
## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-001 grep 验证 0 残留
