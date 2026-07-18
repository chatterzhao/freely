# Pre-Tests: ACP binary 自愈回写
- issue_id: I-20260718T035754Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: bridge 首次启动后 config.toml FREELY_ACP_CLAUDE_BIN 从空变为正确可执行路径
- acceptance_target: candidate AC1
- testing_layer: integration
- target_environment: 主仓 develop（真实生产 config）
- required_evidence: config 读到的值为绝对路径且 -x 成立
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260718T035754Z/verification/harness/at001-self-heal-writeback.sh
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260718T035754Z/verification/harness/at001-self-heal-writeback.sh <freely_script> <project_root>
- expected_output: AT001_RESULT: PASS
- expected_RED_output: config 行读回空字符串 → AT001_RESULT: FAIL
- actual_RED_output: 主仓 config.toml FREELY_ACP_CLAUDE_BIN = ""（多轮 daemon 启停后不变）→ AT001_RESULT: FAIL
- actual_output: daemon 1 次启动后 config 值为 `/Users/zhaoyu/.nvm/versions/node/v22.19.0/bin/claude-agent-acp`(可执行) → AT001_RESULT: PASS
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260718T035754Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker:
- red_how: 主仓 config 多轮启停后始终为空（已实证）
