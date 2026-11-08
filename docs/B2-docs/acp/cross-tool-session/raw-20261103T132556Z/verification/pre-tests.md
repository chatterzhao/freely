# Pre-Tests: ACP bridge 按 session 路由避免越权代答
- issue_id: I-20261103T132556Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 起一个 bridge + 两个 `run-acp-prompt.py`（session A/B），server 只向 A 发 `agent_message_chunk`：当前 B 的 stdout 也出现该文本；修复后 B 不得出现；向 A 发 `session/request_permission`，B 不得应答（当前以 allow 应答）。同时 `sessionId` 出现在 `run-acp-prompt.py` 入站过滤路径、`bypassPermissions` 裸默认不再为真；own-session / 无 sessionId / 未知 session / 空注册表 / 显式 opt-in / 权威 env 等健康路径零退化
- acceptance_target: 两层 session 路由 + 裸默认显式 opt-in，且不丢消息、不改生产权限行为
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: 隔离 mock（fake socket / fake transport / 构造的 JSON-RPC）+ 真实 `acp-bridge.py`/`run-acp-prompt.py` 模块 + develop HEAD 基线快照对比；不调用真实 ACP server、不调用真实平台、不依赖 acp SDK（强制 `FREELY_ACP_USE_SDK=0`）
- required_evidence: 4 项静态断言 + 15 项行为场景全 GREEN；相关回归基线对比退出码一致
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-acp-session-routing.py
- test_command: python3 docs/system/workspace/scripts/tests/test-acp-session-routing.py all
- expected_output: SUMMARY: 19 ok, 0 failed
- expected_RED_output: SUMMARY: 9 ok, 10 failed（4 静态 + 4 客户端/权限 + 1 bridge + 1 权限默认 = 10 项缺陷症状；9 项健康路径 PASS）
- actual_RED_output: develop `35ce56765` 基线快照内放入最终版 AT-001 —— `SUMMARY: 9 ok, 10 failed`（AT-001-RED.log）
- actual_output: 工位同一断言 —— `SUMMARY: 19 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261103T132556Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 客户端用 fake transport 直接驱动 `_handle_message`/`_handle_permission_request`，redirect_stdout 捕获 chunk 是否写入、记录 transport.send 是否应答权限；bridge 用 `AcpBridge.__new__` + fake socket 驱动 `_broadcast_notification`；权限默认用独立子进程按 3 组 env 导入模块读取 `ACP_PERMISSION_MODE`。静态断言绑定契约（入站 `sessionId`、过滤 helper、opt-in 门、session 注册表），行为断言覆盖缺陷矩阵 + 健康路径矩阵。
- red_how: fix RED — `git show develop:<两个真源>` 出基线快照 `/tmp/r14-baseline-runtime`，把最终版 AT-001 以 `--source-dir` 指向基线运行。

## Unit
- acceptance_target: 静态契约（入站 sessionId 过滤、过滤 helper、显式 opt-in 门、bridge session 注册表）+ 权限默认 3 组 env 取值
- testing_layer: unit
- target_environment: fix/raw-20261103T132556Z-acp-session-routing
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-acp-session-routing.py static

## Integration
- acceptance_target: `acp-bridge.py` / `run-acp-prompt.py` 的其他路径不退化（会话协商、prompt 分派、set_mode 保留）
- testing_layer: integration
- target_environment: 工位 + 未修改 develop 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-acp-session-routing.py behavior
2. python3 docs/system/workspace/scripts/tests/test-prompt-manifest-integration.py
3. bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args（预存红，基线对比退出码一致）
4. bash docs/system/workspace/scripts/tests/test-signal-intent-handler-cc（预存红，基线对比退出码一致）

## End-to-End
- acceptance_target: 两层路由对同一「A 通知 / A 权限请求」结论一致（B 不收 chunk、B 不越权代答），且无 sessionId/未知 session 回退广播不丢消息
- testing_layer: end-to-end
- target_environment: 隔离 mock（fake socket + fake transport）
- required_evidence: AT-001
- blocker_budget: 0
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-acp-session-routing.py behavior（客户端 + bridge + 权限默认全场景）

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本缺陷为 ACP bridge 多客户端并发路由，真实环境需 ≥2 个并发 worker + 真实 claude-agent-acp server + acp SDK；本机 SDK 不可 import、无真实 server、无真实平台凭证，按 issue 验收标准明确「隔离 mock server 验证，不调真实平台」。全链路使用真实 `acp-bridge.py`/`run-acp-prompt.py` 真源模块（非桩）+ develop 基线快照对比，覆盖两层实现；真实流量前提 U6（session/update 是否总带 sessionId）无法在本机抓取，故实现取 fail-open（缺失/未知 sessionId 一律保留旧行为），确保即使 U6 不成立也不丢消息。post-merge 若部署真实多 worker 环境，可复核 U6 后再考虑收紧为「未知 session 丢弃」（记入 review 残余风险）。
