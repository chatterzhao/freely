# Codex MCP Install

## 目标

在 `Claude Code` 中注册可用的 `codex-cli` MCP server。

## 优先接法

优先使用 Codex CLI 内置 server：

```bash
claude mcp add codex-cli -s user -- /Users/zhaoyu/.bun/bin/codex mcp-server
```

说明：

- 优先内置 `codex mcp-server`
- 第三方 wrapper 只作备选

## 验证

```bash
claude mcp get codex-cli
```

至少应显示：

- `Status: ✓ Connected`

## 失败归类

- `codex_not_installed`
- `mcp_not_registered`
- `mcp_connect_failed`
