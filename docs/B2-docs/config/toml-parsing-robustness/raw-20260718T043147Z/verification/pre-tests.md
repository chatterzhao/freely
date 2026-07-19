# Pre-Tests: config.toml 解析健壮性
- issue_id: I-20260718T043147Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `freely_config.py get` 在 `=` 两侧有空格时正确取值
- acceptance_target: `FREELY_ACP_CLAUDE_BIN = "/path"` 格式返回 `/path`
- testing_layer: unit
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: stdout 输出预期路径值
- evidence_level: real_env
- artifact_ref: docs/B2-docs/config/toml-parsing-robustness/raw-20260718T043147Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/runtime/freely_config.py get --project . --key FREELY_ACP_CLAUDE_BIN
- expected_output: /usr/local/bin/claude-agent-acp（或实际安装路径）
- expected_RED_output: (exit 1 或无输出 — awk pattern 不匹配时静默失败)
- actual_RED_output:
- actual_output:
- evidence_file:
- red-green-status: pending
- status: pending
- blocker:
- red_how: 人为在 config.toml 中写入 `FREELY_ACP_CLAUDE_BIN= "/path"`（等号前无空格），原 awk 无法匹配

### acceptance-2
- id: AT-002
- requirement: `freely_config.py get` 在 `=` 无空格时正确取值
- acceptance_target: `FREELY_ACP_CLAUDE_BIN="/path"` 格式返回 `/path`
- testing_layer: unit
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: stdout 输出预期路径值
- evidence_level: real_env
- artifact_ref: docs/B2-docs/config/toml-parsing-robustness/raw-20260718T043147Z/verification/test-evidence/acceptance-2.log
- test_command: python3 docs/system/workspace/scripts/runtime/freely_config.py get --project . --key FREELY_ACP_CLAUDE_BIN
- expected_output: /path/to/bin
- expected_RED_output: (exit 1 — awk 无法匹配无空格格式)
- actual_RED_output:
- actual_output:
- evidence_file:
- red-green-status: pending
- status: pending
- blocker:
- red_how: 人为在 config.toml 中写入 `FREELY_ACP_CLAUDE_BIN="/path"`（等号无空格），原 awk 无法匹配

### acceptance-3
- id: AT-003
- requirement: `freely_config.py get` 对不存在的 key 返回 exit 1
- acceptance_target: 不存在的 key → exit 1，shell 侧 `|| true` 兜底不崩溃
- testing_layer: unit
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: exit code = 1，shell 变量为空
- evidence_level: real_env
- artifact_ref: docs/B2-docs/config/toml-parsing-robustness/raw-20260718T043147Z/verification/test-evidence/acceptance-3.log
- test_command: val=$(python3 docs/system/workspace/scripts/runtime/freely_config.py get --project . --key NOT_EXIST 2>/dev/null || true); echo "val=[$val]"
- expected_output: val=[]
- expected_RED_output: awk 不存在的 key → $1 == k 不匹配 → 无输出但 exit 0（awk 总是 exit 0，静默空值）
- actual_RED_output:
- actual_output:
- evidence_file:
- red-green-status: pending
- status: pending
- blocker:
- red_how: 当前 awk 对不存在的 key 静默返回空值且 exit 0，无法区分"key 不存在"与"value 为空"

### acceptance-4
- id: AT-004
- requirement: `monitor-ai-acp.sh` 不再包含 awk 手写 TOML 解析
- acceptance_target: monitor-ai-acp.sh 中无 `awk` + `config.toml` 组合
- testing_layer: unit
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: grep 无匹配
- evidence_level: real_env
- artifact_ref: docs/B2-docs/config/toml-parsing-robustness/raw-20260718T043147Z/verification/test-evidence/acceptance-4.log
- test_command: grep -n 'awk.*config\.toml\|config\.toml.*awk' docs/system/workspace/scripts/runtime/monitor-ai-acp.sh
- expected_output: (no output — grep exit 1)
- expected_RED_output: 仍包含 awk + config.toml 行
- actual_RED_output:
- actual_output:
- evidence_file:
- red-green-status: pending
- status: pending
- blocker:
- red_how: 当前代码中仍为 awk 手写解析

## Unit
- acceptance_target: `freely_config.py get` 在 TOML 规范下等号两侧各种空格格式均正确取值
- testing_layer: unit
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: AT-001/AT-002/AT-003 覆盖此层
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001~003 直接通过命令行测试覆盖所有单元层验证需求
- replacement_evidence: AT-001/AT-002/AT-003 输出

## Integration
- acceptance_target: `monitor-ai-acp.sh` 的 `_bridge_ensure_running` 函数通过 `freely_config.py get` 获取 ACP binary 路径，bridge 正常启动
- testing_layer: integration
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: AT-004 确认 awk 已移除
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: daemon 启动 → bridge 初始化成功 → worker 可被 Manager 委派
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260718T043147Z-worker-acp-bridge-timeout → develop merge chain
- required_evidence: freely fleet-status 显示 worker working 状态
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: fail
- real_environment_reason: 当前 monitor-ai-acp.sh 使用 awk 手写解析 config.toml，格式依赖，遇非标准空格即静默失败
