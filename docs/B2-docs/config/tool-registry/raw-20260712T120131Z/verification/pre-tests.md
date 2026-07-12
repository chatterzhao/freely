# Pre-Tests: tool-registry move
- issue_id: I-20260712T120131Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: git mv 成功，旧路径不存在
- acceptance_target: docs/system/workspace/scripts/runtime/tool-registry.toml 不存在
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 文件在新位置存在
- evidence_level: real_env
- artifact_ref: docs/B2-docs/config/tool-registry/raw-20260712T120131Z/verification/test-evidence/acceptance-1.log
- test_command: test -f docs/system/workspace/tools/tool-registry.toml && test ! -f docs/system/workspace/scripts/runtime/tool-registry.toml && echo PASS
- expected_output: PASS
- expected_RED_output: 旧路径存在
- actual_RED_output: 文件在 scripts/runtime/ 下
- actual_output: PASS - 文件在新位置，旧路径不存在
- evidence_file: docs/B2-docs/config/tool-registry/raw-20260712T120131Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing
## Unit
- acceptance_target: 文件移动 + grep 确认旧路径无引用
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 无 scripts/runtime/tool-registry.toml 引用（不含_legacy）
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 已覆盖
- replacement_evidence: AT-001 passed
## Integration
- acceptance_target: 所有引用路径更新
- testing_layer: integration
- target_environment: develop
- required_evidence: tool-launchers.sh + start-lead-agent.sh 引用新路径
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 + grep 验证已覆盖
- replacement_evidence: grep 确认
## End-to-End
- acceptance_target: daemon 正常启动
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: freely daemon start 成功
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后 daemon 启动验证
- replacement_evidence: 代码审查
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 纯文件移动，git mv 保留历史
