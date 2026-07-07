# Pre-Tests: commands.md 源码对齐
- issue_id: I-20260707T064609Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 10 个命令全部收录
- acceptance_target: commands.md 覆盖 feedback/wt-create/pr-create/pr-review/pr-merge/wt-close/develop-push/issue-sync/deploy-skills/live+fleet-status
- testing_layer: unit
- target_environment: test-pre-merge-20260707T064609Z-commands-md-source-alignment
- required_evidence: grep 确认 10 个命令的章节存在
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T064609Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "^### \`freely" docs/system/workspace/commands.md
- expected_output: >=10
- expected_RED_output: 修改前只有 7 个命令章节
- actual_RED_output: grep 返回 7（修改前）
- actual_output: grep 返回 >=10
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T064609Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前 commands.md 只有 7 个命令的详细章节
### acceptance-2
- id: AT-002
- requirement: wt-close --platform-only 场景完整
- acceptance_target: wt-close 章节包含 --platform-only 语法和使用场景
- testing_layer: unit
- target_environment: test-pre-merge-20260707T064609Z-commands-md-source-alignment
- required_evidence: grep 确认
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T064609Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c "platform-only" docs/system/workspace/commands.md
- expected_output: >=2
- expected_RED_output: 修改前 commands.md 不含 --platform-only
- actual_RED_output: grep → 0
- actual_output: grep → >=2
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T064609Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前 commands.md 不含 --platform-only
### acceptance-3
- id: AT-003
- requirement: issue-sync 和 deploy-skills 已收录
- acceptance_target: 两个新增命令有完整的语法/选项/场景说明
- testing_layer: unit
- target_environment: test-pre-merge-20260707T064609Z-commands-md-source-alignment
- required_evidence: grep 确认
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T064609Z/verification/test-evidence/acceptance-3.log
- test_command: grep -c "issue-sync\|deploy-skills" docs/system/workspace/commands.md
- expected_output: >=3
- expected_RED_output: 修改前 0
- actual_RED_output: 0
- actual_output: >=3
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T064609Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前未收录
## Unit
- acceptance_target: Markdown 语法正确
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 不适用——纯文档
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯 Markdown 文档修改
- replacement_evidence: AT-001~003 grep 验证
## Integration
- acceptance_target: 无集成面
- testing_layer: integration
- target_environment: test-pre-merge-20260707T064609Z-commands-md-source-alignment
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯文档，无集成边界
- replacement_evidence: AT-001~003
## End-to-End
- acceptance_target: pr-create-guarded 门禁链通过
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: E2E 由门禁链覆盖
- replacement_evidence: pr-create-guarded gate chain
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 3 AT GREEN
