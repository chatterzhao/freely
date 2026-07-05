---
b1_id: B1-20260703T121233Z
phase_state: completed
source_raw: raw-20260703T121233Z33Z
produced_candidate: C-20260703T121233Z-A
---

# B1_IBM: 进程清理 + watchdog 重复启动 + bridge 误重启

## Problem

### Bug 1: `freely stop` 后子进程遗留

**现象**：执行 `freely stop` 后以下进程仍在运行，多次启停导致堆积：

| 进程 | 080443Z 工位堆积数 | 原因 |
|------|:--:|------|
| `watchdog_sse.py` | 7 | 不在 pkill 列表中 |
| `sse-watchdog.sh` | 1 | 不在 pkill 列表中 |
| `a2a_server.py` | 1 | 不在 pkill 列表中（只通过 PID 文件杀） |
| `opencode` | 1 | 不在 pkill 列表中 |

**根因**：`stop_project_runtime` 的 `_cleanup_patterns`（freely:21462）缺了上述 4 种进程。

### Bug 2: `_start_watchdog_sse_py` 无重复检查，每次启动 +1 实例

**职责区分**（二者不重叠）：

| 进程 | 监听事件 | 做什么 | 启动路径 |
|------|---------|--------|---------|
| `watchdog_sse.py` | `input-required` | 创建 agent（needs-manager/worker/reviewer） | `_start_watchdog_sse_py`（无重复检查） |
| `sse-watchdog.sh` | `state_update` | 写 JSONL + 注入 Manager session | `cmd_ensure_sse_watchdog_watch`（有 pid 检查） |

**根因**：`_start_watchdog_sse_py`（freely:19877）直接 `nohup python3 watchdog_sse.py &` + `disown`，
不检查是否已有实例。每次 daemon 启动/重启都创建一个新 `watchdog_sse.py`，
旧实例变成孤儿。7 次重启 = 7 个实例。

**修复**：`_start_watchdog_sse_py` 启动前检查 pid 文件，已有活进程则跳过。
使用 `${run_dir}/watchdog-sse.pid` 记录 PID。

### Bug 3: ACP bridge 每个 cycle 重启

**现象**：loop.log 每个 cycle：
`[bridge] tool changed (opencode-apikey-ds-flash-auto → opencode), restarting bridge`

**根因**：比较逻辑（freely:14079）用全 slot 名 `AGENT_AI_TOOL`，
该值在 cycle 间被归一化为 base name `opencode`（via `AI_TOOL="${AGENT_AI_TOOL%%-*}"` at freely:4310
或 `start-lead-agent.sh` 的环境传递），而 `acp_tool_file` 中存的是全名 `opencode-apikey-ds-flash-auto`，
每次比较都不匹配。

**修复**：比较时提取 base name 再比——slot 不变时不重启。

## Decision

三个修复均在同一文件，独立但同属进程生命周期管理。

### Fix 1：补全 `_cleanup_patterns`

```
"watchdog_sse.py.*--project.*${project}"
"sse-watchdog.sh.*--project.*${project}"
"a2a_server.py.*--project.*${project}"
"opencode"
```

### Fix 2：`_start_watchdog_sse_py` 加 pid 检查

```bash
_start_watchdog_sse_py() {
  local project="$1"
  local pid_file; pid_file="$(run_dir_for_project "$project")/watchdog-sse.pid"
  # 已有活进程则跳过
  if [[ -f "$pid_file" ]]; then
    local _pid; _pid=$(cat "$pid_file" 2>/dev/null || true)
    if [[ -n "$_pid" ]] && kill -0 "$_pid" 2>/dev/null; then
      return 0
    fi
  fi
  # 启动并记录 PID
  nohup python3 ... &
  echo $! > "$pid_file"
  disown $!
}
```

### Fix 3：bridge 比较归一化

```bash
# 提取 base name 比较，允许同 tool 不同 slot
_base_tool="${AGENT_AI_TOOL%%-*}"
_running_base="${running_tool%%-*}"
if [[ "$_running_base" != "$_base_tool" ]]; then
  log_info "ACP bridge tool changed ($running_tool → ${AGENT_AI_TOOL})"
  ...
fi
```

## Candidate
- candidate_id: C-20260703T121233Z-A
- status: promoted
- milestone: M-20260703T121233Z-A
