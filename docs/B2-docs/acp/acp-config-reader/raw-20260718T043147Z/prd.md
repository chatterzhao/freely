# PRD: Worker ACP bridge initialize 超时修复

- issue_id: I-20260718T043147Z-A
- epic: acp
- story: worker-slot-acp-protocol-compat

## Goal

修复 worker 完全无法启动的 P0 问题。Worker ACP bridge 因协议不兼容（opencode HTTP vs acp-bridge.py stdio）永远无法完成 `initialize` handshake。

## 实现方案

**变更范围**：仅修改 `.freely/agent-table.toml`，一行配置。

```toml
# 改前
worker_slot = "opencode-apikey-ds-flash-auto"

# 改后
worker_slot = "claude-apikey-ds-pro-auto"
```

**原因**：`claude-agent-acp`（claude 家族）与 `acp-bridge.py` 使用相同的 stdio JSON-RPC 协议栈。

**不做的事**：
- 不修改 `acp-bridge.py`
- 不为 opencode 添加 HTTP ACP 支持（独立 feature issue）
- 不改变 Manager slot

## Dev-Loop Handoff

- 修改文件：`.freely/agent-table.toml`（项目根目录，worktree 内已有副本）
- 改动：`worker_slot` 值替换，1 行
- 验证：重启 daemon，观察 worker bridge initialize 日志
