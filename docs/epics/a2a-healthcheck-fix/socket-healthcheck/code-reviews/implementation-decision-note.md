---
issue_id: I-20260630T085809Z-A
issue_path: docs/issues/I-20260630T085809Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260630T085809Z-A
- issue_path: docs/issues/I-20260630T085809Z-A/issue.md

## Implementation Decision Note

- decision: 改造 `ensure_a2a_server_running()` 的健康检查机制，从发送 HTTP 请求改为 Unix socket connect 检查；同步修复 h11 日志抑制、Shell 注入、超时和日志格式
- why_this:
  1. **协议不匹配是根因**: 健康检查发送原始 HTTP GET，但 A2A Server 的 `/` 路由是 JSON-RPC（POST），h11 在启动瞬间将 HTTP 字节识别为无效请求
  2. **socket connect 是 Unix domain socket 的标准健康信号**: 文件存在 + connect 成功足以证明 uvicorn 在监听
  3. **Shell 注入是安全漏洞**: 变量直接拼接到 `python -c` 字符串，与之前修复的 freely-cycle 同类
  4. **超时 10 秒不足**: `_restore_tasks()` 恢复历史 task 需要 5-15 秒
  5. **无时间戳无法排障**: 45,870 行日志无一条有时间信息
- alternatives_considered:
  - Option B: 改用 `/.well-known/agent.json` 端点 — 仍需要 HTTP 请求，启动瞬间仍可能触发 h11 警告
  - Option C: 只改日志抑制 + 修复副效应 — 不解决根本的协议不匹配
- boundary_non_goals:
  - 不修改 A2A 协议本身（JSON-RPC、路由结构不变）
  - 不修改 `_restore_tasks()` 恢复逻辑
  - 不修改 `a2a_task.py` 客户端
  - 不修改 `task_mode` 降级逻辑（那是另一个独立 issue）
- residual_risk:
  - socket connect 成功但 ASGI app 未完全初始化的情况极罕见（uvicorn 在 bind socket 后立即启动 app），概率低
  - 若未来 A2A 改用 TCP only（无 Unix socket），健康检查需重新设计
