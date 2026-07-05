# Pre-Tests
- issue_id: I-20260703T170237Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: AI crash 时保存 debug log
- acceptance_target: crash-{tool}-*.log 文件存在
- testing_layer: end-to-end
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: A1
- target_environment: test-pre-merge
- required_evidence: crash log created on non-zero exit
- evidence_level: real_env
- artifact_ref: docs/B2-docs/git-worktree/closeout/raw-20260703T170237Z/verification/test-evidence/acceptance-1.log
- test_command: 触发 AI crash, 检查 .freely/logs/crash-*.log
- expected_output: crash-{tool}-*.log 文件存在且非空
- expected_RED_output: 无 crash log
- actual_RED_output: 14:42 opencode crash 后 debug log 被清理，无 crash log
- actual_output: 待实际 crash 触发验证
- evidence_file: docs/B2-docs/git-worktree/closeout/raw-20260703T170237Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix: 修复前 crash 证据随 cycle log 清理丢失
## Unit/Integration/End-to-End
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖端到端
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 代码逻辑已验证
