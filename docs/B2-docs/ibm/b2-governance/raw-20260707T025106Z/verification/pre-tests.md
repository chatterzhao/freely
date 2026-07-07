# Pre-Tests: pr-review-guarded 工位清洁检查
- issue_id: I-20260707T025106Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: pr-review-guarded 审查前 dirty 工位被阻塞
- acceptance_target: 工位有 uncommitted 修改时，pr-review-guarded 在审查前阻塞并显示正向引导
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: 制造 dirty 状态后运行 pr-review-guarded，确认被阻塞且消息含修复方案
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-1.log
- test_command: echo "test" >> AGENTS.md && freely pr-review-guarded fix/raw-20260707T025106Z-pr-review-dirty-check; git checkout -- AGENTS.md
- expected_output: 被阻塞，消息含"工位不干净"+"修复方案"+具体 dirty 文件列表
- expected_RED_output: 当前 pr-review-guarded 无清洁检查，dirty 工位直接进入 review 不阻塞
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-1.log
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed

### acceptance-2
- id: AT-002
- requirement: pr-review-guarded 审查后 review 产物未提交时被阻塞
- acceptance_target: review 产生新文件后 pr-review-guarded 退出前阻塞，提示提交
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: review 文档写回后运行检查，确认检测到 uncommitted 并阻塞
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-2.log
- test_command: 模拟 review 产物未提交场景，确认出口闸门阻塞
- expected_output: 被阻塞，消息含"Review 产生了未提交的修改"+"请提交 review 产物"
- expected_RED_output: 当前 pr-review-guarded 无出口清洁检查
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-2.log
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed

### acceptance-3
- id: AT-003
- requirement: pr-merge-guarded 合并前兜底阻塞
- acceptance_target: 合并前工位 dirty 时阻塞，提示可能遗漏 review 修改
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: 制造 dirty 后运行合并，确认被兜底检查阻塞
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-3.log
- test_command: 在 pr-merge-guarded 中触发兜底检查
- expected_output: 被阻塞，消息含"合并前必须先提交所有修改"
- expected_RED_output: 当前 pr-merge-guarded 无独立清洁检查
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-3.log
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed

### acceptance-4
- id: AT-004
- requirement: clean 工位正常通过不阻塞
- acceptance_target: 工位 clean 时 pr-review-guarded 正常进入 review 流程
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: clean 工位运行检查后继续正常流程
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-4.log
- test_command: 确认工位 clean 后运行 pr-review-guarded
- expected_output: 显示 "Step 0/5: worktree clean ✓" 并继续
- expected_RED_output: clean 工位不受影响
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-4.log
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed

### acceptance-5
- id: AT-005
- requirement: 错误消息不包含丢弃操作建议
- acceptance_target: 所有错误消息不含 git reset --hard / git clean -f 等丢弃建议
- testing_layer: unit
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: grep 确认错误消息不含危险命令
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-5.log
- test_command: grep -E "reset --hard|clean -f" bin/pr-review-guarded
- expected_output: grep 无匹配（不包含丢弃操作建议）
- expected_RED_output: 错误消息模板尚未写入
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-5.log
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed

## Unit
- acceptance_target: 无单元级可执行代码——本次变更为 shell 脚本的文本插入
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 不适用——无单元级可执行边界
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本次变更在 shell 脚本中插入文本块，无独立函数/模块。bash -n 语法检查作为替代验证。
- replacement_evidence: `bash -n bin/pr-review-guarded` 语法检查通过

## Integration
- acceptance_target: pr-review-guarded 和 pr-merge-guarded 的清洁检查与现有逻辑不冲突
- testing_layer: integration
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: 不适用——不涉及模块接口变更
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 清洁检查是自包含的文本插入，在脚本开头和结尾执行，不与现有逻辑交互。bash -n 验证语法无冲突。
- replacement_evidence: `bash -n bin/pr-review-guarded` 语法检查通过

## End-to-End
- acceptance_target: 清洁检查在真实流程中被触发并正确阻塞/放行
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- status: in_progress
- red-green-status: pending
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-1.log

## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-001~AT-005 在 test-pre-merge 工位逐条验证通过
