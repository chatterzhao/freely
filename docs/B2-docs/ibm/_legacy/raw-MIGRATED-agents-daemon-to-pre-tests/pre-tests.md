# Pre-Tests: AGENTS.md daemon test refs → pre-tests.md
- issue_id: I-20260624T104233Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: AGENTS.md 中无 hardcoded "stop/start daemon" 或 "启动 daemon" 或 "daemon start" 等测试指令
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 全项目确认无残留
- test_command: grep -rn "stop daemon\|start daemon\|启动 daemon\|daemon start\|daemon stop" AGENTS.md 2>/dev/null; echo "exit=$?"
- expected_output: exit=1 (无匹配)
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: pending

### acceptance-2
- acceptance_target: AGENTS.md 中 "验证方式由 pre-tests.md 中的测试用例决定" 存在，测试步骤委托给 pre-tests.md
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AGENTS.md 包含 pre-tests.md 委托语句
- test_command: grep -c "验证方式由 pre-tests.md 中的测试用例决定" AGENTS.md
- expected_output: 1
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: pending

### acceptance-3
- acceptance_target: Freely 自举上下文保留且标注为 "daemon 型项目参考"
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AGENTS.md 包含 daemon 型项目参考标注
- test_command: grep -c "daemon 型项目参考" AGENTS.md
- expected_output: 1
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: pending

## Unit
- acceptance_target: AGENTS.md 修改
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: git diff 确认修改正确
- not_applicable_reason: (如不适用填写)
- not_applicable_explanation: (如不适用填写)

## Integration
- acceptance_target: B1/B2 治理文档完整
- testing_layer: integration
- target_environment: fix worktree
- required_evidence: milestones.md、pre-brainstorms、I-* issue 存在

## End-to-End
- acceptance_target: PR 合并到 develop 后 AGENTS.md 内容正确
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: PR merge receipt

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: 文档修改，无需真实环境验证
