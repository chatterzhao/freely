---
b1_id: B1-20260718T043147Z
phase_state: completed
source_raw: raw-20260718T043147Z
source_url: https://github.com/chatterzhao/freely/issues/3992
produced_candidate: C-20260718T043147Z-A
created_at: '2026-07-18'
---

# B1_IBM: Worker ACP bridge 初始化超时导致所有 Worker 无法启动

## Input

- raw issue: raw-20260718T043147Z
- 症状：所有 submitted worker tasks 永远不会进入 working 状态，exit_reason=`manager_worker_launch_verification_blocked`
- worker_slot: `opencode-apikey-ds-flash-auto`（10 slots）

## Problem

Worker 无法启动的根因：**协议层不兼容**。

`acp-bridge.py` 使用 PTY + stdio JSON-RPC 通信模型：
- 它 fork 子进程，通过子进程的 stdin 发送 JSON-RPC 请求，从 stdout 读取响应
- 第一步就是 `initialize` handshake，timeout=30s

`opencode acp` 是 **HTTP server 模式**：
- 启动后监听 HTTP port（`--port 0` = 随机端口）
- 它不从 stdin 读取任何内容
- JSON-RPC 通信走 HTTP，不走 stdio

两者的 I/O 模型完全不相交：bridge 在向 opencode 的 stdin 写 JSON，opencode 完全无视 stdin，只等 HTTP 连接。所以 `initialize` response 永远不会出现在 stdout，30s 后超时，worker 无法启动。

经手动验证（`opencode acp --print-logs` 输出）：opencode acp 确实以 HTTP server 方式启动，log 显示 "setup connection" / "global event connected"，表明它在等待 HTTP 连接，而非读取 stdin。

## Brainstorm

### Option A: 换 Worker slot 为 stdio-based claude ACP tool（最小修复）

将 `agent-table.toml` 的 `worker_slot` 从 `opencode-apikey-ds-flash-auto` 改为 `claude-apikey-ds-pro-auto`。

`claude-agent-acp`（claude 家族的 ACP binary）使用 stdio JSON-RPC，与 `acp-bridge.py` 完全兼容，是当前 Manager 正在使用的同一协议栈。

- 改动极小：仅一行配置
- 无需修改任何 Python 代码
- 立即可验证：daemon 重启后 worker bridge 可以正常 initialize
- 不影响 opencode 作为工具的其他功能

风险：
- `claude-apikey-ds-pro-auto` 是否有足够的 rate limit 承载 10 个 worker 并发？
- 如果需要保留 opencode 作为 worker，此方案不解决根本协议问题

**判断**：当前 P0 是 Worker 完全无法运行，最小可验证修复是换 slot。这是正确的 scope。

### Option B: 给 acp-bridge.py 添加 HTTP-based ACP 支持

为 opencode 增加 HTTP 客户端模式：启动 `opencode acp`，解析其 stdout 获取监听端口，然后通过 HTTP 发送 ACP 请求。

- 范围大：需要修改 acp-bridge.py 的连接架构
- 需要：端口发现机制、HTTP client、请求/响应映射
- 无法在当前 P0 阻塞状态下快速验证
- 不是此 issue 应承接的 scope——应作为独立 feature issue

**判断**：超出当前修复 scope，留作后续功能增强。

### Option C: 换 Worker slot 为 kiro-cli-default-1

`kiro-cli` 属于 claude ACP family（按 registry alias 进入 claude-agent-acp），同样使用 stdio JSON-RPC。

但当前没有明确的 kiro-cli worker 配置验证，不如直接用 `claude-apikey-ds-pro-auto`。

**判断**：次选，`claude-apikey-ds-pro-auto` 更直接。

## Decision: Option A

换 `agent-table.toml` 的 `worker_slot` 为 `claude-apikey-ds-pro-auto`。

理由：
1. **根因明确**：问题是协议不兼容，不是 opencode 配置问题
2. **最小修复**：一行配置改动，可立即验证
3. **正确 scope**：P0 的目标是让 Worker 能运行，不是支持所有 tool 的 HTTP ACP 模式
4. `claude-apikey-ds-pro-auto` slot 已存在且已知可用（与 Manager 同家族）

opencode HTTP ACP 支持作为独立 feature issue 跟踪。

## Candidate

- candidate_id: C-20260718T043147Z-A
- status: promoted
- milestone: M-20260718T043147Z-A
