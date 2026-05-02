# Verification Checklist

## 最小验收

1. `Claude Code` 主请求可用

```bash
claude -p -- "Reply with exactly: hi"
```

2. `codex-cli` MCP 已连接

```bash
claude mcp get codex-cli
```

3. `Codex MCP` 被真实调用

```bash
claude -p --permission-mode bypassPermissions -- \
  "You must first use the codex-cli MCP tool to determine whether the current directory contains a docs folder. After using the tool, answer with exactly one word: yes or no."
```

4. 调试日志出现：

```text
Calling MCP tool: codex
```

## 反证测试

若将主 provider key 改为假值，主请求应失败。

意义：

- 证明当前不是“Codex 直接作为 Claude 底层 provider”
- 而是“Claude 主请求 + Codex MCP capability”
