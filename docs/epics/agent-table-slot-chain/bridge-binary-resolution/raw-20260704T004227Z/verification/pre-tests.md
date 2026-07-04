# Pre-Tests: ACP Bridge 启动链路修复

- issue_id: I-20260704T004227Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: monitor-ai-acp.sh `_bridge_ensure_running` tool name 对比用 base_tool
- acceptance_target: 当 .tool 文件存 "opencode-apikey-ds-flash-auto" 且 --tool 传 "opencode" 时，对比不应触发 bridge 重启
- testing_layer: unit
- target_environment: feature-local
- required_evidence: shell 测试脚本输出 PASS
- evidence_level: integration
- artifact_ref: test evidence from bin/test-acp-bridge-start-records
- test_command: bash docs/system/workspace/scripts/tests/test-acp-bridge-tool-name-comparison
- expected_output: 所有断言 PASS，bridge 未因 tool name mismatch 被误杀
- expected_RED_output: 断言 FAIL — "tool changed" 被触发
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 执行当前未修复的 monitor-ai-acp.sh，观察 bridge 被误杀重启，确认 RED

### acceptance-2
- id: AT-002
- requirement: monitor-ai-acp.sh `_bridge_ensure_running` 传 `--acp-bin` + `--acp-args`
- acceptance_target: bridge 进程使用正确的 ACP binary（如 opencode），而非默认 claude-agent-acp
- testing_layer: integration
- target_environment: feature-local
- required_evidence: bridge 进程命令行包含 `--acp-bin /path/to/expected/binary`
- evidence_level: integration
- artifact_ref: test evidence from bin/test-acp-bridge-start-records
- test_command: bash docs/system/workspace/scripts/tests/test-acp-bridge-start-records
- expected_output: bridge 启动参数包含正确的 --acp-bin 和 --acp-args
- expected_RED_output: bridge 启动参数中无 --acp-bin（当前 bug 行为）
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 启动 daemon 后检查 bridge 进程命令行，确认无 --acp-bin → RED

### acceptance-3
- id: AT-003
- requirement: `.bin` 文件在 bridge 启动后被正确写入
- acceptance_target: /tmp/freely-acp-<hash>.pid.bin 文件存在且内容等于实际 binary 路径
- testing_layer: unit
- target_environment: feature-local
- required_evidence: ls + cat 输出验证
- evidence_level: integration
- artifact_ref: test evidence from bin/test-acp-bridge-start-records
- test_command: bash docs/system/workspace/scripts/tests/test-acp-bridge-start-records --check-bin-file
- expected_output: .bin 文件存在且内容正确
- expected_RED_output: .bin 文件不存在或为空（monitor-ai-acp.sh 当前不写）
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — monitor-ai-acp.sh 启动 bridge 后检查 .bin 文件 → 不存在 → RED

### acceptance-4
- id: AT-004
- requirement: bridge 启动前清理 ANTHROPIC_* / CLAUDE_CODE_* / AI_AGENT 环境变量
- acceptance_target: bridge 进程环境中无父进程注入的 AI 工具变量
- testing_layer: integration
- target_environment: feature-local
- required_evidence: bridge 进程 environ 输出无 ANTHROPIC_MODEL 等污染变量
- evidence_level: integration
- artifact_ref: test evidence from bin/test-acp-bridge-env-sanitization
- test_command: bash docs/system/workspace/scripts/tests/test-acp-bridge-env-sanitization
- expected_output: bridge 进程环境中无 ANTHROPIC_*/CLAUDE_CODE_*/AI_AGENT（除 slot settings.json 显式声明者）
- expected_RED_output: bridge 进程环境中存在 ANTHROPIC_MODEL=deepseek-v4-pro[1m]
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 在父进程设置 ANTHROPIC_MODEL 后启动 daemon，检查 bridge 进程环境 → 存在 → RED

### acceptance-5
- id: AT-005
- requirement: agent-id 解析使用精确匹配而非子串匹配
- acceptance_target: develop 路径 (.../freely) 不会匹配 agent-id.env 中的 worktree 路径 (.../freely-worktrees/...)
- testing_layer: unit
- target_environment: feature-local
- required_evidence: 测试脚本输出 PASS
- evidence_level: integration
- artifact_ref: test evidence from bin/test-acp-bridge-start-records
- test_command: bash docs/system/workspace/scripts/tests/test-agent-id-grep-exact-match
- expected_output: develop 上 _my_id 解析为 manager_01，feature worktree 上解析为对应 worker_id
- expected_RED_output: develop 上 _my_id 错误解析为 worker_01
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 创建模拟 agent-id.env，develop 路径匹配到 worktree 行 → worker_01 → RED

### acceptance-6
- id: AT-006
- requirement: session JSONL 中 model 与 agent-table slot 配置一致
- acceptance_target: 启动 daemon 后第一个 cycle 的 session JSONL 中 model 字段匹配 slot settings.json
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260704T004227Z-agent-table-slot-resolution
- required_evidence: session JSONL 中 model 字段值
- evidence_level: real_env
- artifact_ref: session JSONL file
- test_command: bash docs/system/workspace/scripts/tests/test-acp-session-model-matches-config
- expected_output: model 与 agent-table slot 对应的 settings.json 一致
- expected_RED_output: model=deepseek-v4-pro (当前错误行为)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 启动当前未修复的 daemon，运行一个 cycle，读 session JSONL → deepseek-v4-pro → RED

## Unit

- acceptance_target: shell 函数单元测试覆盖 tool name 对比, ACP binary 解析, agent-id grep
- testing_layer: unit
- target_environment: feature-local
- required_evidence: 每个单元测试有明确的输入/预期输出
- blocker_taxonomy: execution_pending_or_failed

## Integration

- acceptance_target: daemon 启动后 bridge 使用正确的 binary + 干净的环境变量
- testing_layer: integration
- target_environment: test-pre-merge-20260704T004227Z-agent-table-slot-resolution
- required_evidence: AT-001 ~ AT-005 全部 pass
- blocker_taxonomy: execution_pending_or_failed

## End-to-End

- acceptance_target: 完整 daemon cycle 产生正确 model 的 session
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260704T004227Z-agent-table-slot-resolution → develop merge chain
- required_evidence: AT-006 pass + session JSONL model 字段验证
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本修复消除配置与实际行为的不一致，修复后验证 session JSONL model 与 agent-table slot 匹配即可
