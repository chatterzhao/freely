---
b1_id: B1-20260708T100854Z
phase_state: completed
source_raw: raw-20260708T100854Z
source_url: https://github.com/chatterzhao/freely/issues/3818
produced_candidate: C-20260708T100854Z-A
---

# B1: A2A/SSE 通信故障——多 agent 协作瘫痪根因分析

## Discovery

### value_check: P0 阻塞
Manager 启动成功（ACP bridge 正常），但 8 分钟 session 零产出。根因是 A2A 通信层故障导致 Manager 无法委派 Worker。

### 架构现状

```
freely daemon-run
  ├─ DB daemon ✅ (socket 正常)
  ├─ A2A server ✅ (uvicorn 绑定 /tmp/freely-a2a-{hash}.sock)
  ├─ ACP bridge ✅ (claude-agent-acp, socket 正常)
  ├─ SSE watchdog ⚠️ (日志无时间戳，无法确认)
  ├─ monitor-ai-acp.sh (监控 AI session)
  ├─ sse-watchdog.sh (ACP bridge SSE 连接)
  └─ Manager AI session (通过 ACP bridge fork)
```

### 逐层诊断

**Layer 1: A2A server → uvicorn 绑定**
- 日志确认: `Uvicorn running on unix socket /tmp/freely-a2a-{hash}.sock` ✅
- socket 路径: 带 `.sock`，与 client 一致

**Layer 2: a2a_task.py → HTTP client**
- socket 路径: `/tmp/freely-a2a-{hash}.sock` ✅
- 与 server 一致

**Layer 3: SSE watchdog (watchdog_sse.py)**
- 启动检查: `freely` shell 用 `_a2a_socket_path` 返回路径**无 `.sock`**
- `[[ -S "$_a2a_socket" ]]` → 无 `.sock` 的路径不存在 → watchdog **未被 `_start_watchdog_sse_py` 启动**
- 但 `watchdog-sse.log` 有输出 → 可能是 sse-watchdog.sh 通过另一路径启动的
- 日志无时间戳 → 无法确认是否为本次运行

**Layer 4: Manager AI session**
- 通过 ACP bridge fork 启动 ✅
- 8 分钟 session，0 个 A2A task 被创建
- 无法确认 Manager 是否尝试了 patrol loop

### 三个核心问题

**问题 1: `_a2a_socket_path` 返回值与 server 实际路径不一致**
```
freely shell:    /tmp/freely-a2a-{hash}        ← 无 .sock
A2A server:      /tmp/freely-a2a-{hash}.sock   ← 有 .sock
a2a_task.py:     /tmp/freely-a2a-{hash}.sock   ← 有 .sock
watchdog_sse.py: /tmp/freely-a2a-{hash}.sock   ← 有 .sock
```
`_a2a_socket_path` 用于: 日志消息、socket 存在性检查 (`-S`)、清理 (`rm -f`)。
因为无 `.sock`，`-S` 检查永远返回 false → `_start_watchdog_sse_py` 永远不启动。

**问题 2: 日志无时间戳——可观测性为零**
watchdog-sse.log 无时间戳，无法确认错误来自哪个运行周期。daemon stop 后 socket 被清理，丢失所有现场证据。

**问题 3: Manager session 输出丢失——无 cycle log**
Manager AI session 的 Claude Code 输出没有被捕获到 cycle log 文件。无法知道 Manager 是否尝试读 scan、是否尝试委派 Worker。

## Brainstorm

### 子问题 1: socket 路径统一

**Option A: 改 `_a2a_socket_path` 加上 `.sock` ✅**
- 优点: 最小改动，一行修复
- 缺点: 无

**Option B: 改 server 和 client 去掉 `.sock`**
- 优点: 无
- 缺点: 改动面大

**Decision: Option A** — 改 freely shell 的 `_a2a_socket_path`。

### 子问题 2: 日志时间戳

**Option A: watchdog 日志加时间戳**
- 优点: 可追踪每次连接到哪个运行周期
- 缺点: 需要改 Python

**Option B: 日志文件名带时间戳**
- 优点: 不丢历史
- 缺点: 文件累积

**Decision: Option A** — 加时间戳。

### 子问题 3: Manager 输出

**Option A: 确认 cycle log 生成机制是否工作**
- 需要排查 `monitor-ai-acp.sh` 是否正确捕获输出

**Decision**: 先修 socket，再验证 cycle log。

## Decision: 最小改动——修复 socket 路径 + 日志时间戳

## Candidate: C-20260708T100854Z-A, promoted

### 子问题 4: 可观测性增强

**问题**: 
- watchdog-sse.log 无时间戳，无法关联到运行周期
- cycle log 未生成，AI session 输出丢失
- socket 连接失败时错误信息不明确

**Option A: 每行日志加 ISO8601 时间戳 ✅**
- watchdog_sse.py: 所有 print → print(f"[{timestamp}] ...")
- sse-watchdog.sh: Python 内嵌代码加时间戳

**Option B: 结构化日志 (JSON)**
- 优点: 可机器解析
- 缺点: 改动大，人工阅读不便

**Option C: 日志文件按启动时间命名**
- 优点: 不丢历史
- 缺点: 文件累积，需清理策略

**Decision: Option A + C 组合** — 加时间戳 + 日志文件 rotation 保留最近 3 个历史。
