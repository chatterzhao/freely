---
b1_id: B1-20260703T121233Z
phase_state: completed
source_raw: raw-20260703T121233Z
produced_candidate: C-20260703T121233Z-A
---

# B1_IBM: freely stop 进程清理 + bridge 重复重启 + SSE watchdog 堆积

## Problem

### Bug 1: `freely stop` 执行后子进程遗留

执行 `freely stop` 后，以下进程未被清理：
- `watchdog_sse.py`（多个实例堆积）
- `sse-watchdog.sh`
- `a2a_server.py`
- `freely_db_manager.py`
- `opencode` ACP 进程

**根因**：`cleanup_supervisor()`（freely:21928）调用 `terminate_pid_with_graceful_wait`
杀 watchdog、dispatcher、SSE watchdog。但这些进程的 PID 是从 pid 文件读的——
如果 pid 文件已被覆盖（新实例覆盖旧 PID），旧实例就无法被追踪和清理。

### Bug 2: sse-watchdog.sh 多实例堆积

`sse-watchdog.sh --watch` 循环 `while true; do ... sleep $INTERVAL; done`。
`_sse_watchdog_cycle` 调用 `watchdog_sse.py` 并等待其返回。
但 `watchdog_sse.py` 有时会因 ACP bridge 不可用而退出，然后 `sse-watchdog.sh`
再次启动它。问题在于：

1. `ensure-manager` 守护脚本（nohup 启动）可能启动多个 sse-watchdog.sh
2. 旧 sse-watchdog.sh 的 PID 文件被新实例覆盖 → 旧实例变成孤儿

**实际操作中**：080443Z 工位积了 7 个 watchdog_sse.py + 1 个 sse-watchdog.sh。

### Bug 3: ACP bridge 每个 cycle 重启

```
[INFO] ACP bridge binary changed (/Users/zhaoyu/.opencode/bin/opencode → opencode)
```

**根因**：`_ensure_acp_bridge_running` 检测"binary changed"时比较：
- `running_bin`：从 `{pid_file}.bin` 文件读出的上一次存储值（config.toml 的全路径）
- `acp_bin`：从 registry 查到的值（`opencode`）

config.toml 中的 `FREELY_ACP_OPENCODE_BIN=/Users/zhaoyu/.opencode/bin/opencode`
（全路径）与 registry 的 `acp.binary=opencode`（短名）不一致，每个 cycle 都
触发"binary changed"→ 重启 bridge。

**影响**：每个 AI cycle 浪费 ~10s 重启 bridge + 丢失 session context（mode=fresh 而非 resume）。

### Bug 4: 多 project daemon 并存（设计问题，非 bug）

同一仓库的不同 worktree 各自启动 daemon——这是设计行为（每个 worktree 独立运行）。
但 `freely stop` 只停当前 project，其他 worktree 的 daemon 继续运行。
严格来说不算 bug，但实际体验差：多个 daemon 竞争资源，进程堆积。

## Decision

本 fix scope 聚焦 Bug 1-3（进程清理 + bridge 误重启），Bug 4 是独立的设计决策。

### Fix 1: stop 时杀进程组而非逐 PID

当前：`cleanup_supervisor` → `terminate_pid_with_graceful_wait $pid`（单个 PID）
改为：记录 supervisor 启动时的 PGID（进程组 ID），stop 时 `kill -TERM -$pgid` 杀整个进程组。
子进程（watchdog、SSE、a2a）都在同一个进程组中，一批清理。

**风险**：`nohup` 启动的 ensure-manager 不在进程组中——需额外处理。

### Fix 2: sse-watchdog.sh 启动前检查已有实例

在 `sse-watchdog.sh --watch` 启动 loop 前，检查是否已有 sse-watchdog.sh 在运行。
有则退出（不启动重复实例）。用 pid 文件 + `kill -0` 验证。

### Fix 3: bridge binary 比较归一化

`_ensure_acp_bridge_running` 比较 binary 时：
- 写入 `acp_bin_file` 时用 registry 的短名（`opencode`），不用 config.toml 的全路径
- 或者在比较时用 `basename` 归一化

**推荐**：写入时用 registry 短名 `acp_bin`（`opencode`），但实际启动时用 `command -v` 或
config.toml 的全路径。存储名和比较用短名，启动用全路径。

同时修复：写 `acp_bin_file` 的时机——当前在 `_ensure_acp_bridge_running` 中
先检查旧值、再启动新 bridge、最后写新值。时序上有窗口导致误判。

## Candidate
- candidate_id: C-20260703T121233Z-A
- status: promoted
- milestone: M-20260703T121233Z-A
