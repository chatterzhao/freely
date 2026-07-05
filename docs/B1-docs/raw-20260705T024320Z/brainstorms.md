---
b1_id: B1-20260705T024320Z
phase_state: completed
source_raw: raw-20260705T024320Z
source_url: https://github.com/chatterzhao/freely/issues/3737
produced_candidate: C-20260705T024320Z-A
created_at: 2026-07-05
---

# B1_IBM: 全链路 per-agent tool/slot 支持

## Input
- raw-20260705T024320Z (GitHub #3737)
- agent-table: manager=claude, worker=opencode, reviewer=cline（三个不同 base_tool）

## 10 维度全链路审计结果

| # | 维度 | 结果 | 问题 |
|---|------|:--:|------|
| 1 | Agent Identity | ✅ | agent-id.env + agent_working 正确 |
| 2 | Slot Resolution | ✅ | watchdog `_get_agent_slot` 正确 |
| 3 | base_tool 提取 | ✅ | `%%-*` / `split('-')[0]` 正确 |
| 4 | Bridge Lifecycle | ⚠️ | `_acp_session_close` 无 base_tool；`_ensure_acp_bridge_running` 用全局 AGENT_AI_TOOL 组装 env |
| 5 | Session 路由 | ✅ | `acp_session_connect` + `_resolve_bridge_socket` 正确 |
| 6 | Watchdog 事件 | ✅ | 三个 handler 均按 agent 查询 slot |
| 7 | Worker Launch | ❌ | socket 无 base_tool → 找不到 bridge → 回退硬编码 `--agent opencode` |
| 8 | Tool Switch | ⚠️ | `_stop_acp_bridge` 无 base_tool 时杀全部 bridge |
| 9 | Session Close | ❌ | `_acp_session_close` 无 base_tool → 连错 socket |
| 10 | Config/Env | ✅ | `ai_cli_tool_with_auth_assemble` 按 slot 正确 |

## 缺陷清单（按优先级）

### Bug 1: worker launch 硬编码 `--agent opencode`
- `line 13180`: `_acp_bridge_socket "$manager_project"` 无 base_tool → 找不到带后缀的 socket
- `line 13191`: fallback 硬编码 `--agent opencode`，无视 agent-table 的 worker_slot
- **影响**: worker 永远用 opencode，agent-table 配置无效

### Bug 2: `_acp_session_close` 连错 bridge
- `line 14237`: `_acp_bridge_socket "$project"` 无 base_tool → 连到无后缀 socket
- 所有非默认 tool 的 session close 静默失败
- 调用点: `_ensure_acp_bridge_running:14088,14098`（tool 切换时关旧 session）

### Bug 3: Bridge env 用全局 AGENT_AI_TOOL
- `line 14133`: `tool_name="${AGENT_AI_TOOL:-claude}"` → 所有 bridge 用 manager slot 的 env
- `line 14209`: `.tool` 文件写 manager slot 而非当前 bridge 的 slot
- opencode bridge 得不到 `OPENCODE_CONFIG`，cline bridge 得不到 `--config`
- **影响**: opencode/cline bridge 用 claude 凭据启动，功能异常

### Bug 4: `_stop_acp_bridge` 无差别杀全部
- `line 5684,5701,14287-14299`: 不传 base_tool 时 pkill 所有 ACP 进程
- tool switch 时不应影响其他 agent 的 bridge

### Bug 5: `stop_project_runtime` 只清理默认 bridge
- `line 21453`: `_acp_bridge_pid_file "$project"` 无 base_tool
- daemon stop 后非默认 tool 的 bridge 成为孤儿进程

### Bug 6: `sse-watchdog.sh:36` bridge socket 无 base_tool
- SSE watchdog 连到无后缀 socket，manager 用非默认 tool 时找不到

## Decision: 逐项修复

全部为参数遗漏——需要 base_tool 或 slot 的地方用了全局变量或不传参。
改动集中在 `freely` 单文件（除 sse-watchdog.sh 一处）。

### 修复方案

| # | 位置 | 改动 |
|---|------|------|
| 1 | `_ensure_acp_bridge_running` | 接受 `slot` 参数，内部用 `$slot` 替代 `$AGENT_AI_TOOL` |
| 2 | daemon start bridge loop | 传 slot: `_ensure_acp_bridge_running "$project" "$_bt" "$_slot"` |
| 3 | `_acp_session_close` | 接受 `base_tool` 参数，传 `_acp_bridge_socket "$project" "$base_tool"` |
| 4 | worker launch ~13180 | 从 agent-table 查 worker slot → base_tool → 传 socket |
| 5 | worker launch ~13191 | `--agent` 用查到的 base_tool 而非硬编码 opencode |
| 6 | `_stop_acp_bridge` caller | 传 base_tool，不影响其他 bridge |
| 7 | `stop_project_runtime` | 扫描所有 base_tool，逐个停 bridge |
| 8 | `sse-watchdog.sh:36` | 传 base_tool |

### 不改的
- 同 base_tool 不同 slot 的 fork 继承（需 ACP 协议支持，属远期）
- daemon 初始化 `AGENT_AI_TOOL` 导出（manager 自身标识，正确）

## Candidate
- candidate_id: C-20260705T024320Z-A
- status: promoted
- milestone: M-20260705T024320Z-A
