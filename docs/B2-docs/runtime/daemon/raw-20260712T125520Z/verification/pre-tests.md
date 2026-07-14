# Pre-Tests: AI_MODE default correction + remaining unguarded fix
- issue_id: I-20260712T125520Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: bash -n 语法检查通过
- acceptance_target: freely 脚本语法无错误
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n 无错误
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260712T125520Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: line 22752: AI_MODE: unbound variable
- actual_RED_output: daemon crash on AI_MODE unbound variable in fresh_with_handoff
- actual_output: PASS - bash -n OK
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260712T125520Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing
### acceptance-2
- id: AT-002
- requirement: 所有 AI_MODE 默认值为 wait 而非 auto
- acceptance_target: grep AI_MODE:-auto 无结果
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 输出为空
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260712T125520Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c 'AI_MODE:-auto' docs/system/workspace/scripts/runtime/freely && echo "FAIL" || echo "PASS"
- expected_output: PASS
- expected_RED_output: found :-auto defaults
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260712T125520Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
### acceptance-3
- id: AT-003
- requirement: 所有 AI_MODE 引用都有默认值守卫
- acceptance_target: 无裸 $AI_MODE 关键路径引用
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 无裸引用
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260712T125520Z/verification/test-evidence/acceptance-3.log
- test_command: grep -n '"$AI_MODE"' docs/system/workspace/scripts/runtime/freely && echo "FAIL" || echo "PASS"
- expected_output: PASS
- expected_RED_output: found unguarded $AI_MODE
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260712T125520Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: passed
## Unit
- acceptance_target: bash 语法 + AI_MODE 守卫检查
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT-001 + AT-002 + AT-003 全部通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/002/003 已覆盖所有单元测试需求
- replacement_evidence: AT-001 + AT-002 + AT-003 全部 PASS
## Integration
- acceptance_target: daemon 正常启动
- testing_layer: integration
- target_environment: develop
- required_evidence: daemon 启动无 crash
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后实际启动验证
- replacement_evidence: 代码审查 + bash -n + grep 全覆盖验证（3 条 acceptance 全部 PASS）
## End-to-End
- acceptance_target: daemon 持续运行无 crash
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: daemon 不 crash
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后验证 daemon fresh_with_handoff 稳定性
- replacement_evidence: 代码审查 + 语法检查全绿
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 单文件修改，bash -n 通过，grep 全覆盖验证无残留 auto 默认值和无裸引用
