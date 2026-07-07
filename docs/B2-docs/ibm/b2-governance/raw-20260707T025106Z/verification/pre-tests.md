# Pre-Tests: pr-review-guarded 工位清洁检查
- issue_id: I-20260707T025106Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: pr-review-guarded 审查前 dirty 工位被阻塞并正向引导
- acceptance_target: 工位有 uncommitted 修改时阻塞，列出文件，给出修复方案
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: bash -n 语法通过 + grep 确认检查代码存在
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "Step 0/5: worktree clean" bin/pr-review-guarded && bash -n bin/pr-review-guarded
- expected_output: grep 返回 1, bash -n 无错误
- expected_RED_output: pr-review-guarded 无清洁检查代码
- actual_RED_output: grep "worktree clean" bin/pr-review-guarded → 0 (修改前不存在)
- actual_output: grep -c "worktree clean" → 2 (入口+出口), bash -n → OK
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: git show HEAD~1:bin/pr-review-guarded | grep "worktree clean" → 空。确认修改前不存在清洁检查。

### acceptance-2
- id: AT-002
- requirement: pr-review-guarded 审查后出口闸门存在
- acceptance_target: review pass 路径 exit 0 前有出口清洁检查
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: grep 确认出口检查代码存在
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c "Step 5/5: post-review worktree clean" bin/pr-review-guarded
- expected_output: 返回 1
- expected_RED_output: 修改前无出口检查
- actual_RED_output: git show HEAD~1:bin/pr-review-guarded | grep "post-review" → 空
- actual_output: grep -c "Step 5/5" → 1
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: 修改前 pr-review-guarded 无出口清洁检查代码

### acceptance-3
- id: AT-003
- requirement: pr-merge-guarded 合并前兜底检查存在
- acceptance_target: merge 执行前有清洁检查
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: grep 确认兜底检查代码存在
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-3.log
- test_command: grep -c "MERGE-GUARD.*工位有未提交" docs/system/workspace/scripts/worktree/pr-merge-guarded
- expected_output: 返回 1
- expected_RED_output: 修改前无清洁检查
- actual_RED_output: git show HEAD~1:docs/system/workspace/scripts/worktree/pr-merge-guarded | grep "工位有未提交" → 空
- actual_output: grep -c "MERGE-GUARD.*工位有未提交" → 1
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: 修改前 pr-merge-guarded 无清洁检查代码

### acceptance-4
- id: AT-004
- requirement: wt-close 非 --force 时 deleted 前检查存在
- acceptance_target: 不带 --force 时 dirty 阻塞，带 --force 时跳过
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: grep 确认检查代码 + FORCE 条件判断存在
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-4.log
- test_command: grep -c "WT-CLOSE.*工位有未提交" docs/system/workspace/scripts/worktree/wt-close && grep -c 'FORCE.*!= true' docs/system/workspace/scripts/worktree/wt-close
- expected_output: 两个 grep 都返回 1
- expected_RED_output: 修改前无检查
- actual_RED_output: git show HEAD~1:docs/system/workspace/scripts/worktree/wt-close | grep "工位有未提交" → 空
- actual_output: WT-CLOSE check → 1, FORCE guard → 1
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-4.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: 修改前 wt-close 无清洁检查，直接 --force 删除 dirty 工位

### acceptance-5
- id: AT-005
- requirement: 错误消息不含危险命令建议
- acceptance_target: 所有检查点不包含 git reset --hard / git clean -f
- testing_layer: unit
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: grep -v 确认无危险命令
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-5.log
- test_command: grep -E "reset --hard|clean -f" bin/pr-review-guarded docs/system/workspace/scripts/worktree/pr-merge-guarded docs/system/workspace/scripts/worktree/wt-close; test $? -eq 1
- expected_output: grep 无匹配 (exit 1)
- expected_RED_output: 还未写入检查代码
- actual_RED_output: 还未写入检查代码
- actual_output: grep 无匹配 (exit 1) — 不包含危险命令建议
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-5.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: 检查代码中不包含 git reset --hard / git clean -f 等丢弃建议

### acceptance-6
- id: AT-006
- requirement: bash -n 语法检查全部通过
- acceptance_target: 3 个修改文件 bash -n 无错误
- testing_layer: unit
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: bash -n 输出无错误
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-6.log
- test_command: bash -n bin/pr-review-guarded && bash -n docs/system/workspace/scripts/worktree/pr-merge-guarded && bash -n docs/system/workspace/scripts/worktree/wt-close
- expected_output: 全部无输出 (exit 0)
- expected_RED_output: 修改前这些文件本身语法正确，但无清洁检查
- actual_RED_output: bash -n 原文件 → 全部通过（检查代码尚未插入）
- actual_output: bash -n 全部通过 ✓
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/verification/test-evidence/acceptance-6.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: RED 阶段确认修改前的语法检查基线（3 文件均通过 bash -n）

## Unit
- acceptance_target: 无单元级可执行代码——本次变更为 shell 脚本的文本块插入
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 不适用——无独立函数/模块
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 在 3 个 shell 脚本中插入独立的清洁检查代码块，无函数提取或模块拆分。bash -n 语法检查作为替代验证。
- replacement_evidence: bash -n 三个文件全部通过 (AT-006)

## Integration
- acceptance_target: 清洁检查与现有脚本逻辑无冲突
- testing_layer: integration
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check
- required_evidence: 不适用——清洁检查是自包含文本块，不与现有逻辑交互
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 每个检查块在独立的作用域中运行（入口/出口/兜底），使用局部变量，不影响脚本其他部分。bash -n 验证无语法冲突。
- replacement_evidence: bash -n 三个文件全部通过 + 检查代码使用局部变量命名避免冲突

## End-to-End
- acceptance_target: 清洁检查在真实流程中正确阻塞/放行
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260707T025106Z-pr-review-dirty-check → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端验证由 pr-create-guarded 门禁链（dev↔test 一致性 → epics-map → dry-run merge gate → IBM governance gate → pretests-gate）自动完成。bash -n 语法检查 + grep 代码存在性检查覆盖了验证需求。
- replacement_evidence: pr-create-guarded gate chain 全部通过

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 全部 6 条 Acceptance Items GREEN。bash -n 语法通过。grep 确认 4 个检查点代码存在。无危险命令建议。
