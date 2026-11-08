# PRD: ACP bridge 按 session 路由避免越权代答

- issue_id: I-20261103T132556Z-A
- source_raw: raw-20261103T132556Z
- workflow_kind: fix
- milestone: M-20261103T132556Z-A
- story: acp/cross-tool-session

## 目标

一个 (project, base_tool) 单 bridge 把 ACP server 通知广播给所有客户端、客户端又不校验 session，导致两个并发 worker 相互污染 stdout、并越权代答彼此的权限请求。目标：每条 session 通知只被它所属的客户端消费；权限请求只由所属 session 应答；裸默认不放大权限面——且全程不丢消息、不改生产权限行为。

## 改动范围（2 个真源 + 1 个测试）

1. `docs/system/workspace/scripts/runtime/run-acp-prompt.py`（权威修复）：`session_id` 绑定、`_inbound_session_mismatch`、入站过滤、权限守卫。
2. `docs/system/workspace/scripts/runtime/acp-bridge.py`（纵深防御）：`client_sessions` 注册表 + 定向投递（fail-open 回退）+ 裸默认显式 opt-in。
3. 新增 `docs/system/workspace/scripts/tests/test-acp-session-routing.py`（AT-001）。
4. `docs/milestones.md` 追加 `M-20261103T132556Z-A`。

## 不退化边界

- 缺失/未知 `sessionId`、未知自身 session、空注册表一律保留旧行为（U6：绝不丢消息）。
- `CLAUDE_CODE_PERMISSION_MODE` 显式配置时逐字节不变；`FREELY_ACP_BYPASS_PERMISSIONS=1` 保留旧 bypass 能力。
- 其余会话协商 / prompt 分派 / set_mode / server 存活 / stdout 解析逻辑未改。
- `docs/epics-map.svg` 不改（复用既有 `acp/cross-tool-session` story，check-epics-map 对齐）。

## 功能需求

- FR-1: client B 不打印 session A 的 `agent_message_chunk`；own-session / 无 sessionId / 未知自身 session 仍打印。
- FR-2: client B 不应答 session A 的 `session/request_permission`（auto 与 step 皆然）；own-session 仍自动应答。
- FR-3: `sessionId` 出现在 `run-acp-prompt.py` 入站过滤路径（pre-main 区）。
- FR-4: bridge 对已知 session 定向投递；未知/缺失回退广播；断开清理注册表。
- FR-5: `bypassPermissions` 裸默认不再为真，显式 opt-in 可恢复，权威 env 不变。

## 验收

AT-001 develop 基线快照 RED `9 ok / 10 failed` → GREEN `19 ok / 0 failed`；`test-prompt-manifest-integration.py` PASS；4 个 cc 预存红测试基线对比退出码一致（归 #4151）。
