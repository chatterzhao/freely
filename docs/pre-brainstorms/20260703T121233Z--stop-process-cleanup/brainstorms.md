---
b1_id: B1-20260703T121233Z
phase_state: completed
source_raw: raw-20260703T121233Z
produced_candidate: C-20260703T121233Z-A
---

# B1_IBM: 进程清理 + bridge 重复重启

## Problem

### Bug 1: `freely stop` 后子进程遗留

**现象**：执行 `freely stop` 后 `watchdog_sse.py`、`sse-watchdog.sh`、`a2a_server.py`、
`opencode` 等进程仍在运行。多次启停导致堆积（080443Z 工位积了 7 个 watchdog_sse.py）。

**根因**：`stop_project_runtime` 的 `_cleanup_patterns`（freely:21462-21473）
缺少以下进程的 pkill 模式：
- `watchdog_sse.py` — 不在任何 pkill 列表中
- `sse-watchdog.sh` — 不在任何 pkill 列表中
- `a2a_server.py` — 不在任何 pkill 列表中（只通过 PID 文件杀）
- `opencode`（ACP binary 进程）— 不在任何 pkill 列表中

**修复**：在 `_cleanup_patterns` 中添加缺失的进程模式。

### Bug 2: SSE watchdog 多实例堆积

**现象**：同一工位 7 个 `watchdog_sse.py` 同时运行。

**根因**：有两个启动路径各自创建实例，互不可见：

1. `start_project_runtime` → `_start_watchdog_sse_py`（freely:18073 → 19877）
   — 直接 `nohup python3 watchdog_sse.py &` + `disown`
   — **无重复检查**，每次 daemon 启动都创建新实例

2. `ensure-manager` → `cmd_ensure_sse_watchdog_watch`（freely:19888）
   — 通过 pid 文件检查已有实例（line 19893-19898），已正确
   — 但`_start_watchdog_sse_py` 不经过 pid 文件检查

**修复**：`_start_watchdog_sse_py` 启动前检查 pid 文件是否有活进程，
已有则跳过。与 `cmd_ensure_sse_watchdog_watch` 共用同一个 pid 文件。

### Bug 3: ACP bridge 每个 cycle 重启

**现象**：loop.log 每个 cycle 显示
`[bridge] tool changed (opencode-apikey-ds-flash-auto → opencode), restarting bridge`

**根因**：`AGENT_AI_TOOL` 的值在 daemon 生命周期中不一致。

`AGENT_AI_TOOL` 在 daemon 启动时设为 `opencode-apikey-ds-flash-auto`（freely:4287），
写入 `acp_tool_file`（freely:14172）。但后续 cycle 中 `AGENT_AI_TOOL` 被归一化为
base tool name `opencode`（可能经由 `AI_TOOL="${AGENT_AI_TOOL%%-*}"` at freely:4310
或 `start-lead-agent.sh` 的环境变量传递），导致与文件中存储的全名不匹配。

**直接原因**：比较逻辑（freely:14079）用全 slot 名比较，但
`AGENT_AI_TOOL` 在 cycle 间被覆盖为 base name。

**修复**：比较时提取 base tool name 再比较，而非用全 slot 名。
在 `_ensure_acp_bridge_running` 中：
```bash
_base="${AGENT_AI_TOOL%%-*}"
_running_base="${running_tool%%-*}"
[[ "$_running_base" != "$_base" ]] && restart
```

## Decision

三个修复独立但同属进程生命周期管理边界，一次修完。

- Bug 1：`_cleanup_patterns` 补全 4 个模式
- Bug 2：`_start_watchdog_sse_py` 加重复检查
- Bug 3：bridge 比较归一化为 base tool name

## Candidate
- candidate_id: C-20260703T121233Z-A
- status: promoted
- milestone: M-20260703T121233Z-A
