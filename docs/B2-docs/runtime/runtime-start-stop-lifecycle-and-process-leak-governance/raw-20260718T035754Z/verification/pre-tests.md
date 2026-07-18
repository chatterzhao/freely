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
- actual_RED_output: 主仓 config FREELY_ACP_CLAUDE_BIN = ""（bridge 启动后不回写）→ AT001_RESULT: FAIL
- actual_output: daemon 启动后 config 从空→/Users/zhaoyu/.nvm/versions/node/v22.19.0/bin/claude-agent-acp（$S/docs/system/workspace/scripts/runtime/freely 生产实证）→ AT001_RESULT: PASS `/Users/zhaoyu/.nvm/versions/node/v22.19.0/bin/claude-agent-acp`(可执行) → AT001_RESULT: PASS
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260718T035754Z/verification/test-evidence/acceptance-1.log（RED: acceptance-1-RED.log）
- red-green-status: green
- status: passed
- blocker:
- red_how: 主仓 config 多轮启停后始终为空（已实证）

## Unit
- acceptance_target: N/A
- testing_layer: unit
- target_environment: N/A
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 新增 5 行 bash（command -v + upsert_config_key），无独立可测试单元边界——整体行为由 daemon start 触发 bridge 初始化链中的单点回写，最真实验证层在 real_env（主仓 daemon start 实证）
- replacement_evidence: AT-001 real_env 实证（config 从空→绝对路径，bridge event 日志确认）

## Integration
- acceptance_target: bridge 启动流程内自愈回写（AT-001）
- testing_layer: integration
- target_environment: test-pre-merge-20260718T035754Z-acp-bin-self-heal
- required_evidence: AT001_RESULT: PASS
- blocker_taxonomy: execution_pending_or_failed
1. at001-self-heal-writeback.sh — config 路径断言

## End-to-End
- acceptance_target: feature→test-pre-merge→develop merge chain + 主仓首次 daemon start 后自愈
- testing_layer: end-to-end
- target_environment: develop bound guarded merge chain
- required_evidence: guarded merge receipts + config 写回实证
- blocker_taxonomy: execution_pending_or_failed
1. pr-create/review/merge-guarded 链路收据
2. 主仓 daemon start 后 config.toml 确认写入

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 主仓（/Users/zhaoyu/Downloads/code/my-freely/freely）直接应用修复版脚本，daemon start 后 FREELY_ACP_CLAUDE_BIN 从 ""→"/Users/zhaoyu/.nvm/versions/node/v22.19.0/bin/claude-agent-acp"（绝对路径，-x 成立），bridge event: acp_bridge_started binary=/Users/zhaoyu/.nvm/.../claude-agent-acp，production 实证完成
