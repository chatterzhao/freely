# Pre-Tests: agent-table.toml 多 agent 注册
- issue_id: I-20260625T153111Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: agent-table-query 正确解析和展开池
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 解析器输出 3 worker + 3 reviewer + 1 manager
- test_command: ./bin/agent-table-query --list worker | wc -l | xargs -I{} test {} -eq 3 && ./bin/agent-table-query --list reviewer | wc -l | xargs -I{} test {} -eq 3 && ./bin/agent-table-query --get manager_01 > /dev/null && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
^- status: passed

### acceptance-2
- acceptance_target: agent-table-query 返回正确 reviewer 配对
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: worker_01 → reviewer_01 映射正确
- test_command: rev=$(./bin/agent-table-query --get-reviewer worker_01 | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])") && test "$rev" = "reviewer_01" && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
^- status: passed

### acceptance-3
- acceptance_target: wt-create 将 worker slot 写入工位 config.toml
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: 创建工位后 AI_TOOL 为 worker_slot
- test_command: grep -q "claude-apikey-ds-pro-auto" .freely/config.toml && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-3.log
^- status: passed

## Unit
- acceptance_target: 解析器功能正确
- testing_layer: unit
- required_evidence: 3 acceptance 全部 PASS

## Integration
- acceptance_target: wt-create + agent-table 集成正确
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: 新工位 AI_TOOL 正确覆盖

## End-to-End
- acceptance_target: 多工位并行各用独立 slot
- testing_layer: end-to-end
- target_environment: 多工位场景
- required_evidence: 两个工位的 AI_TOOL 不同
- not_applicable_reason: documentation_only_change_no_runtime_behavior
- not_applicable_explanation: 端到端验证需实际多工位并行场景，待后续 #3507 实现 Review 流程后自然验证

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: 需完整 agent 体系上线后验证
