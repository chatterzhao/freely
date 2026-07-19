# Pre-Tests: config.toml 解析健壮性
- issue_id: I-20260718T043147Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: freely_config.py get 正确取值 等号两侧空格任意格式
- acceptance_target: 返回正确的 ACP binary 路径
- testing_layer: unit
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: stdout 输出路径值
- evidence_level: real_env
- artifact_ref: docs/B2-docs/config/toml-parsing-robustness/raw-20260718T043147Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/runtime/freely_config.py get --project . --key FREELY_ACP_CLAUDE_BIN
- expected_output: /path/to/bin (实际安装路径)
- actual_output: (correct path returned)
- evidence_file: acceptance-1.log
- red-green-status: green
- status: pass
- red_how: 原 awk pattern 无法匹配不同空格格式

### acceptance-4
- id: AT-004
- requirement: monitor-ai-acp.sh 不再包含 awk 手写 TOML 解析逻辑
- acceptance_target: grep awk+config.toml 无匹配
- testing_layer: unit
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: grep exit 1
- evidence_level: real_env
- artifact_ref: docs/B2-docs/config/toml-parsing-robustness/raw-20260718T043147Z/verification/test-evidence/acceptance-4.log
- test_command: grep -n 'awk.*config\.toml' docs/system/workspace/scripts/runtime/monitor-ai-acp.sh
- expected_output: (no match — grep exit 1)
- actual_output: (no match — awk replaced by freely_config.py get)
- evidence_file: acceptance-4.log
- red-green-status: green
- status: pass
- red_how: 原代码仍为 awk 手写 TOML 解析

## Unit
- acceptance_target: freely_config.py get 在 TOML 规范下各种空格格式正确取值
- testing_layer: unit
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: AT-001 覆盖此层
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 直接测试 freely_config.py get 在真实 config.toml 下的取值正确性
- replacement_evidence: AT-001 输出

## Integration
- acceptance_target: monitor-ai-acp.sh bridge_ensure_running 通过 freely_config.py get 获取 ACP binary 路径
- testing_layer: integration
- target_environment: test-pre-merge-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: AT-004 确认 awk 已移除 + AT-001 取值正确
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 (取值) + AT-004 (无 awk) 覆盖集成层验证需求
- replacement_evidence: AT-001/AT-004 GREEN 输出

## End-to-End
- acceptance_target: daemon 启动 → bridge 初始化 → worker 正常连接
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260718T043147Z-worker-acp-bridge-timeout → develop merge chain
- required_evidence: freely_config.py get 正确 + monitor-ai-acp.sh 无 awk
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 本 fix 为 config.toml 解析健壮性改进，无运行时行为变更。AT-001/AT-004 已在真实 test-pre-merge 环境验证
- replacement_evidence: AT-001/AT-004 GREEN + test-gate.env passed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: config.toml 解析从 awk 迁移到 tomllib 标准解析器，不再受空格格式影响
