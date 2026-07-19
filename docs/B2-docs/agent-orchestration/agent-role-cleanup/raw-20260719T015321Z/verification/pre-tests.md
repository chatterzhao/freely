# Pre-Tests: lead-agent.md 引用清理 + governance-check 修复
- issue_id: I-20260719T015321Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: governance-check 全绿，无 lead-agent.md 缺失错误，无 skill 路径不存在错误
- acceptance_target: `freely governance-check` exit 0
- testing_layer: unit
- target_environment: fix-raw-20260719T015321Z-lead-agent-ref-cleanup
- required_evidence: governance-check 输出无 FAIL
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/agent-role-cleanup/raw-20260719T015321Z/verification/test-evidence/acceptance-1.log
- test_command: freely governance-check 2>&1
- expected_output: "Governance check passed" 或仅 warnings
- expected_RED_output: "[FAIL] missing file: docs/system/workspace/agents/lead-agent.md"
- red-green-status: pending
- status: pending
- red_how: 当前 develop HEAD governance-check 因 lead-agent.md 缺失 + skill 路径不存在而 FAIL

### acceptance-2
- id: AT-002
- requirement: 全项目无 lead-agent 悬空引用（除历史文档/commit message）
- acceptance_target: grep 仅命中历史引用
- testing_layer: unit
- target_environment: fix-raw-20260719T015321Z-lead-agent-ref-cleanup
- required_evidence: grep 结果仅含 B1-docs 和 B2-docs 引用描述（合法）
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/agent-role-cleanup/raw-20260719T015321Z/verification/test-evidence/acceptance-2.log
- test_command: grep -rn 'lead-agent' docs/system/workspace/ --include="*.md" --include="*.sh" | grep -v 'start-lead-agent'
- expected_output: (no output)
- expected_RED_output: 5 处悬空引用
- red-green-status: pending
- status: pending
- red_how: 当前有 5 处悬空引用
