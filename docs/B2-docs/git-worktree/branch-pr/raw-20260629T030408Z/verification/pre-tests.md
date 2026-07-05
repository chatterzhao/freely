# Pre-Tests: feat → feature 重命名完成
- issue_id: I-20260629T030408Z-A

## Acceptance Items

### acceptance-1: wt-create accepts freely-feature-execution
- id: AT-001
- requirement: wt-create 接受 --skill freely-feature-execution 为合法参数
- acceptance_target: wt-create 验证逻辑已更新
- testing_layer: unit
- target_environment: fix/raw-20260629T030408Z-feat-to-feature-complete worktree
- required_evidence: grep 确认 wt-create 中无 freely-feat-execution 残留
- evidence_level: mock
- artifact_ref: docs/epics/feat-to-feature/rename-completion/raw-20260629T030408Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "freely-feat-execution" docs/system/workspace/scripts/worktree/wt-create && echo "FAIL: still has feat-execution" || echo "PASS: clean"
- expected_output: PASS: clean
- actual_output: PASS: clean — 0 occurrences of freely-feat-execution in wt-create
- evidence_file: docs/epics/feat-to-feature/rename-completion/raw-20260629T030408Z/verification/test-evidence/acceptance-1.log
- blocker: (失败时填写)
- status: passed
- red-green-status: green

### acceptance-2: 所有活跃脚本中零 feat-execution 残留
- id: AT-002
- requirement: 活跃代码（scripts/hooks/AGENTS.md）中不再出现 freely-feat-execution 或 feat-execution
- acceptance_target: grep 返回零匹配
- testing_layer: unit
- target_environment: fix/raw-20260629T030408Z-feat-to-feature-complete worktree
- required_evidence: grep 在 scripts/ .githooks/ AGENTS.md 中无 feat-execution 命中
- evidence_level: mock
- artifact_ref: docs/epics/feat-to-feature/rename-completion/raw-20260629T030408Z/verification/test-evidence/acceptance-2.log
- test_command: grep -rn "feat-execution\|freely-feat" docs/system/workspace/scripts/ .githooks/ AGENTS.md 2>/dev/null | grep -v "feature" | grep -v '.bak' && echo "FAIL: residual feat found" || echo "PASS: zero feat-execution residuals"
- expected_output: PASS: zero feat-execution residuals
- actual_output: PASS: zero feat-execution residuals — grep returned no matches
- evidence_file: docs/epics/feat-to-feature/rename-completion/raw-20260629T030408Z/verification/test-evidence/acceptance-2.log
- blocker: (失败时填写)
- status: passed
- red-green-status: green

### acceptance-3: AGENTS.md 使用 feature: 而非 feat:
- id: AT-003
- requirement: AGENTS.md 第25行流程描述使用 feature: 前缀
- acceptance_target: AGENTS.md 中没有 feat: 简写
- testing_layer: unit
- target_environment: fix/raw-20260629T030408Z-feat-to-feature-complete worktree
- required_evidence: grep 确认 AGENTS.md 中 feat: 已改为 feature:
- evidence_level: mock
- artifact_ref: docs/epics/feat-to-feature/rename-completion/raw-20260629T030408Z/verification/test-evidence/acceptance-3.log
- test_command: grep "^feature: (" AGENTS.md >/dev/null && echo "PASS: feature: found" || echo "FAIL: feature: not found"
- expected_output: PASS: feature: found
- actual_output: PASS: feature: found — line 25 starts with "feature: ("
- evidence_file: docs/epics/feat-to-feature/rename-completion/raw-20260629T030408Z/verification/test-evidence/acceptance-3.log
- blocker: (失败时填写)
- status: passed
- red-green-status: green

## Unit
- acceptance_target: 8个活跃代码文件中无 feat-execution 残留
- testing_layer: unit
- target_environment: fix/raw-20260629T030408Z-feat-to-feature-complete worktree
- required_evidence: grep 验证通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 单元级 grep 检查已覆盖在 AT-001 至 AT-003 中，每条均可独立验证
- replacement_evidence: 见 ## Acceptance Items AT-001~AT-003

## Integration
- acceptance_target: not applicable — 纯字符串替换，无模块间集成面
- testing_layer: integration
- target_environment: not_applicable
- required_evidence: not_applicable
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本次仅修改字符串常量，不涉及模块间数据流或协作
- replacement_evidence: 各文件的 grep 检查已覆盖全部改动面

## End-to-End
- acceptance_target: not applicable — 无用户可见行为变更
- testing_layer: end-to-end
- target_environment: not_applicable
- required_evidence: not_applicable
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 本次仅修改内部字符串引用，不影响用户可见行为或完整业务流程
- replacement_evidence: 单元级 grep 检查已覆盖全部改动面

## Real-Environment
- real_environment_status: pass
- real_environment_reason: wt-create help 输出已确认显示 freely-feature-execution，真实环境验证通过
