---
b1_id: B1-20260710T110249Z
phase_state: completed
source_raw: raw-20260710T110249Z
source_url: https://github.com/chatterzhao/freely/issues/3871
produced_candidate: C-20260710T110249Z-A
created_at: 2026-07-10
---

# B1_IBM: Manager AI rc=143 根因分析

## Input
raw #3871: Manager AI cycle 持续被 rc=143 (SIGTERM) 杀死，idle timeout fix 已生效但问题未解决。

## Problem

观察到的现象：
- Claude bridge 在活跃 session/prompt 期间**不再 idle-shutdown**（PR #3870 fix 生效）
- Manager 正常执行 tool calls（Read File, Skill, Terminal, Find）
- 但 cycle 仍然以 `rc=143 (SIGTERM)` 结束，`stopReason=unknown`

## Discovery

### 价值判断
值得修。Manager 无法完成完整 patrol cycle → 无法委派 Worker → 整个 agent 协作系统瘫痪。

### 完整 kill 链路追踪

monitor-ai-acp.sh 有两个 kill 路径：

**路径 A: 失败检测 (line 414-419)**
```
_detect_acp_failure → 检查 marker file → kill child_pid
```
4 层检测：
- Layer 0 (idle shutdown): 检查 `_bridge_log` = 默认 `acp-bridge.log`（无 base_tool 后缀）
- Layer 1 (network): 检查 cycle log
- Layer 2 (auth): 检查 cycle log
- Layer 3 (bridge fatal): 检查 `_bridge_log`（默认 log）→ fallback 检查 cycle log

**路径 B: Bridge 死亡检测 (line 422-432)**
```
_bridge_pid_file "$project" → 检查默认 PID 文件（无 base_tool 后缀）→ 进程死亡 → kill
```

### 根因：per-tool 日志/PID 导致检测盲区

PR #3842 (lazy-start bridge) 和 PR #3849 (per-tool logging) 引入 per-tool 命名：
- PID: `/tmp/freely-acp-{hash}-{base_tool}.pid`
- Log: `.freely/run/acp-bridge-{base_tool}.log`
- Socket: `/tmp/freely-acp-{hash}-{base_tool}.sock`

但 `monitor-ai-acp.sh` 和 `freely` 中**大量调用仍使用默认路径（无 base_tool 后缀）**。

**monitor-ai-acp.sh 中 4 处未更新：**

| 行号 | 代码 | 问题 |
|------|------|------|
| 181 | `_bridge_log=".../acp-bridge.log"` | 硬编码默认 log，Layer 0/3 检测盲区 |
| 403 | `_bridge_pid_file "$project"` | 无 base_tool，读不存在的默认 PID |
| 427 | `_bridge_pid_file "$project"` | bridge-dead 检查盲区 |
| 441 | `_bridge_socket "$project"` | ping 使用错误 socket |

**freely 中 7 处未更新：**

| 行号 | 代码 | 问题 |
|------|------|------|
| 18863 | `_acp_bridge_socket "$PROJECT_ROOT"` | Supervisor 操作错误 socket |
| 18904 | `_acp_bridge_socket "$project"` | 同上 |
| 18935 | `_acp_bridge_socket "$project"` | 同上 |
| 18965 | `_acp_bridge_socket "$project"` | 同上 |
| 18998 | `_acp_bridge_socket "$project"` | 同上 |
| 21527 | `_acp_bridge_pid_file "$project"` | 清理错误 PID 文件 |
| 21535 | `_acp_bridge_socket "$project"` | 清理错误 socket |

**总计 11 处仍使用默认路径，覆盖三大功能域：bridge 健康检测、Supervisor 启停管理、资源清理。**

这意味着：
- monitor 的所有 bridge 级检测（idle/fatal/PID/socket）全部盲区
- Supervisor 启停 bridge 时操作不存在的默认 socket/PID
- 资源清理删错文件，per-tool 文件残留

## Brainstorm

### Option A: 同步 per-tool 命名到 monitor（推荐）
更新 monitor-ai-acp.sh 中所有硬编码的默认路径为 per-tool 路径：
1. `_bridge_log` → 使用 `_bridge_log_file "$project" "$base_tool"`
2. `_bridge_pid_file "$project"` → `_bridge_pid_file "$project" "$base_tool"`
3. `_detect_acp_failure` 传入 base_tool 参数

### Option B: 统一 bridge 管理为单一路径
回退 per-tool 命名，使用统一的默认路径。

**缺点**: 回退 PR #3842 和 #3849 的所有改动，回到多 bridge 日志互相覆盖的问题。

### Option C: monitor 完全重写
重写 monitor-ai-acp.sh 的检测逻辑，基于 ACP protocol 状态而非文件检查。

**缺点**: 改动面过大，风险高。

## Decision: Option A + 需要先确认第三个 kill 路径

1. 首先同步 per-tool 命名到 monitor-ai-acp.sh（修复已知的检测盲区）
2. 如果 rc=143 仍然发生 → 深入追踪第三个 kill 路径（可能需要添加 signal handler tracing）

## Candidate
- candidate_id: C-20260710T110249Z-A
- status: promoted
- milestone: M-20260710T110249Z-A
