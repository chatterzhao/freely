---
issue_id: I-20260718T043147Z-A
issue_path: docs/B2-docs/acp/worker-slot-acp-protocol-compat/raw-20260718T043147Z/issues/I-20260718T043147Z-A.md
phase_state: in_dev
---

- issue_id: I-20260718T043147Z-A
- issue_path: docs/B2-docs/acp/worker-slot-acp-protocol-compat/raw-20260718T043147Z/issues/I-20260718T043147Z-A.md

## Implementation Decision Note

- decision: 将 `.freely/agent-table.toml` 的 `worker_slot` 从 `opencode-apikey-ds-flash-auto` 改为 `claude-apikey-ds-pro-auto`
- why_this: opencode acp 是 HTTP server 模式，无法通过 stdio 响应 acp-bridge.py 的 JSON-RPC initialize handshake。claude-agent-acp（claude 家族）与 acp-bridge.py 使用相同的 stdio JSON-RPC 协议栈，是唯一一行配置可验证的最小修复路径。
- alternatives_considered: (A) 修改 acp-bridge.py 为 opencode 添加 HTTP client 模式——scope 过大，不是 P0 范围；(B) 编写 stdio↔HTTP 转换 shim——引入额外运行时组件，风险更高
- boundary_non_goals: 不为 opencode HTTP ACP 模式添加支持（独立 feature issue）；不修改 acp-bridge.py 代码；不改变 Manager slot
- residual_risk: claude-apikey-ds-pro-auto 的并发 rate limit 是否足以支撑 pool=10 worker 同时工作——目前 pool=10 是配置上限，实际并发取决于任务量，暂不调整
