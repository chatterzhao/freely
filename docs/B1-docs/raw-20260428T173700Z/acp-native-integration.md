# ACP 原生集成设计

## 原则

ACP 模式就要用 ACP 最佳实践，不做中间态。

```
direct 模式：claude -p → 进程退出 → PID 检测完成
ACP 模式：  claude-agent-acp 常驻 → session/prompt stopReason → 协议检测完成
```

两个模式互不妥协——配置哪种就用哪种的最佳路径。

## ACP 原生架构

```
Freely daemon
  │
  ├─ ACP Server Manager（管理 claude-agent-acp 进程生命周期）
  │   └─ 启动/重启/健康检查 claude-agent-acp 进程
  │
  ├─ ACP Session（每个 AI 角色一个 session）
  │   ├─ Manager session: 持久化，跨主管周期 resume
  │   └─ Worker session:  持久化，跨 worker 周期 resume
  │
  └─ ACP Completion Detector（替代 PID 监控）
      └─ 监听 session/prompt 响应 → stopReason = "end_turn" → 完成
```

## 完成检测对比

| | direct 模式 | ACP 原生模式 |
|---|---|---|
| 启动 | `claude -p < prompt_file` | ACP server 已常驻，只需 `session/prompt` |
| 运行中 | `while kill -0 $pid` 轮询 | 等待 JSON-RPC 响应 |
| 完成 | 进程退出 + rc | `session/prompt` 返回 `stopReason: "end_turn"` |
| Stall | debug log mtime + process state | ACP session 超时 / heartbeat |
| 错误 | rc != 0 | JSON-RPC error response |
| 缓存 | 每次重建（--resume 部分命中） | session 常驻内存 → 全命中 |

## monitor-ai-cli.sh 改造

```
当前（direct）:
  claude -p < prompt_file &
  child_pid=$!
  while kill -0 $child_pid; do ... done
  exit $child_rc

ACP 原生:
  # ACP server 已在运行，只需通信
  session_id=$(session/resume 或 session/new)
  response=$(session/prompt $session_id $prompt_text)
  # response.stopReason == "end_turn" → 完成
  # response 中的 tool calls 已由 ACP server 自动处理
  # 只需等待最终文本响应
```

## ACP Server 生命周期

```
daemon 启动:
  ├─ 启动 claude-agent-acp 进程（如果没有运行）
  ├─ 验证 server 响应（initialize handshake）
  └─ server 常驻，daemon 停止时关闭

每个 AI 周期:
  ├─ session/resume（续接上次会话）或 session/new（首次）
  ├─ session/prompt（发送 prompt）
  ├─ 等待响应（stopReason = "end_turn"）
  └─ 提取 session_id 用于下次 resume
```

## Session 模型（ACP 原生）

```
Manager:
  fresh:  session/new → M-sid
  resume: session/resume M-sid → 上下文保留 → 缓存命中

Worker-A（fork from manager 上下文）:
  fresh:  session/new → WA-sid
          首条 prompt 包含 manager 的任务描述
  resume: session/resume WA-sid

Worker-B（并行）:
  fresh:  session/new → WB-sid
  resume: session/resume WB-sid
```

## 需要改动的文件

| 文件 | 改动 |
|------|------|
| monitor-ai-cli.sh | 新增 ACP 分支：JSON-RPC 通信替代 PID 轮询 |
| freely | `_ai_shows_liveness` ACP 分支：session heartbeat 替代 process state |
| freely | `select_launch_kind` ACP 模式：总是 resume（session 持久） |
| run-acp-prompt.py | 重构为持久 session 管理（不再每次新建进程） |
| tool-launchers.sh | ACP 启动改为 server manager |
