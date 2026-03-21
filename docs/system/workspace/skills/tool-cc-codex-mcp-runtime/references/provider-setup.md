# Provider Setup

## 目标

在安装 Codex MCP 之前，先让 `Claude Code` 主请求可用。

## 支持路径

1. `official`
- Claude 官方登录

2. `ccr`
- `Claude Code Router`
- 例如 `CCR -> ModelScope`

3. `other`
- 任何能让 `Claude Code` 主请求正常完成的兼容 provider / router / proxy

## CCR 最小要求

1. `~/.claude-code-router/config.json` 存在
2. `api_base_url` 指向正确的 completion endpoint
3. `ccr activate` 可注入：
   - `ANTHROPIC_AUTH_TOKEN`
   - `ANTHROPIC_BASE_URL`
4. 本地端口可监听

## 验证

```bash
claude -p -- "Reply with exactly: hi"
```

返回 `hi` 才能继续下一阶段。

## 失败归类

- `cc_not_installed`
- `provider_not_ready`
- `ccr_not_running`
- `provider_auth_failed`
