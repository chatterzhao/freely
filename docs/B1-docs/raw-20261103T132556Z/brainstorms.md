# Brainstorms: ACP bridge 按 session 路由避免越权代答

- raw_key: 20261103T132556Z
- GitHub: #4152 / Gitee: IKSPQ7
- workflow_kind: fix

## 问题复述

一个 `(project, base_tool)` 只有一个 bridge 进程，它把 ACP server 的每条通知广播给所有已连接客户端；客户端也从不比对 `params.sessionId`。两个 worker 并发时，A 的 `agent_message_chunk` 被写进 B 的 stdout，且任一客户端会替别的 session 回答权限请求（答案是 allow）——「并发正确性 + 权限越界」双料缺陷。

## 复核（本轮真实核对过的事实）

- `acp-bridge.py` 顶部：当 `acp` SDK 可 import 时会 `os.execv` 到 `acp_bridge_v2.py`。本机 SDK 不可 import（`import acp` 失败），且 `acp_bridge_v2.py` 不存在 → 真正运行的是本文件内的 legacy 实现，即 issue 证据所指的 `_broadcast_notification` / `handle_client`。测试里显式 `FREELY_ACP_USE_SDK=0` 固定这一路径，避免 execv 把测试进程替换掉。
- `_broadcast_notification`（:497→本轮 :516）确为 `for sock in self.clients: sock.send(data)` 全广播；`self.clients` 是纯 socket 列表，没有任何 session 归属信息。
- `run-acp-prompt.py` 的 `ACPClient` 没有 `session_id` 字段；`sessionId` 只出现在 `main()` 的出站请求参数里（pre-main 区 0 处）。`_handle_message` 只按 `method` 分派，不看 session；`_handle_permission_request` 在 `mode=auto` 时优先选 `allow_always/allow_once`，不看 session。
- `acp-bridge.py:35` 的 `bypassPermissions` 是**服务端** `session/set_mode` 的 modeId（不是 client 的 `--mode`）。代码自带告警：非 bypass 模式「Tool calls may require approval and could hang」。生产通过 `monitor-ai-acp.sh`→`_load_slot_env_vars` 从 slot 的 settings.json 读 `permissionMode`（`ai-cli` 生成模板里为 `bypassPermissions`）注入 `CLAUDE_CODE_PERMISSION_MODE`。

## 被否决 / 收窄的方案（证伪，不写成 candidate）

1. **每 session 一个 bridge/连接**（issue 方案 4，彻底修法）：会显著增加常驻进程数（当前一个项目 ≥6），且与「一个 (project,base_tool) 一个 bridge」的存量设计冲突。评估成本与收益后不采用；本轮用「定向投递 + 客户端过滤」两层收口，行为等价且零新增进程。
2. **bridge 对「未知 session」直接丢弃**（issue 方案 1 字面）：issue 自己的前置条件 U6 已警告「先抓真实流量确认 `session/update` 总带 `sessionId`，否则过滤会丢消息」。本机无法抓真实 ACP 流量（无 SDK、无真实 server）。**收窄为 fail-open**：未知/缺失 `sessionId` → 按旧行为广播并记日志，绝不丢消息。真正的正确性由客户端入站过滤保证（每个 client 只认自己的 session），所以回退广播不会重新引入泄漏。
3. **直接把 `bypassPermissions` 默认值翻成 `default`**（issue 方案 3 字面，无 opt-in）：会让未显式配置 `CLAUDE_CODE_PERMISSION_MODE` 的部署进入需审批模式，可能 hang——属用户明令「不要退化」。**收窄**：保留 `CLAUDE_CODE_PERMISSION_MODE` 权威（生产逐字节不变），仅把「未配置时的裸默认」改为 `default`，并提供 `FREELY_ACP_BYPASS_PERMISSIONS=1` 显式 opt-in 逃生开关。权限请求的 session 匹配由客户端守卫保证（方案 2 的实质）。

## Related findings（已被现有 open issue 覆盖，不新建）

- `run-acp-prompt.py` 在 subprocess(`--agent`) 模式下 `_perm_mode` 默认已是 `default`——本轮把 bridge 裸默认对齐到它，方向与存量一致。
- 4 个 `test-*-cc-args` / `current_project: unbound variable` 预存红测试：develop 基线 `35ce56765` 与本轮退出码/输出逐字节一致（仅 mktemp 随机后缀与绝对路径前缀不同），归 #4151，非本轮引入。
- `acp-session-architecture.md:41-43` 声称「Worker-A/B 各自独立 session，互不干扰」——本轮修复后才与实现一致；文档本身无需改（是目标态描述）。

## 决策

采用单一 promoted candidate：客户端入站 session 过滤（权威修复）+ bridge 定向投递（纵深防御，fail-open 回退）+ 裸默认显式 opt-in。见 candidates.md。
