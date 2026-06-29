---
name: freely-tool-cc-codex-mcp-runtime
description: >- 安装并配置 Claude Code 主 provider。在 Claude Code 中注册 Codex MCP，
  为 tool=cc 模式定义 codex/codex-reply 的自动路由和验证步骤。

  Use when: 首次配置或切换 AI 工具，需要注册 MCP server。
  触发词："配置工具"、"MCP"、"codex"、"切换 AI"、"安装 provider"。
---

# skill:freely-tool-cc-codex-mcp-runtime

## 何时使用

- 用户要求安装 `Claude Code`
- 用户要求配置 `CCR` 或其他 provider 让 `Claude Code` 正常工作
- 用户要求在 `Claude Code` 中安装 `Codex MCP`
- 用户要求让 `cc` 模式默认以“在 CC 中调用 Codex”的方式工作
- 用户要求验证 `cc + codex mcp` 是否真的可用

## 目标

- 让 `Claude Code` 主请求先可用
- 在 `Claude Code` 中注册 `codex-cli` MCP
- 为 `tool=cc` 模式提供默认的 Codex capability / runtime policy
- 明确 `mcp__codex-cli__codex` 与 `mcp__codex-cli__codex-reply` 的使用边界

## 工作流

1. 先读 [provider-setup.md](references/provider-setup.md)，确认主 provider 路径。
2. 再读 [mcp-install.md](references/mcp-install.md)，安装或校验 `codex-cli` MCP。
3. 再读 [runtime-policy.md](references/runtime-policy.md)，决定 `auto/step` 模式下的权限映射和 `codex` / `codex-reply` 路由。
4. 最后按 [verification-checklist.md](references/verification-checklist.md) 做端到端验证。

## 不负责

- 不把 Codex 伪装成 `Claude Code` 的底层模型 provider
- 不替代 `tool=codex` 的原生运行路径
- 不负责实现 Freely runtime 本身的代码改动；本 skill 先定义 setup / policy / verification contract

## 关键边界

- `Codex MCP` 不能替代 `Claude Code` 主 provider
- `tool=cc` 的主请求必须先可工作
- `Codex` 在这里是 `cc` 的内部能力，不是 `cc` 的 `model`
- `auto` 模式要同时映射：
  - Claude: `--permission-mode bypassPermissions`
  - Codex MCP: `approval-policy=never`

## References

- [provider-setup.md](references/provider-setup.md)
- [mcp-install.md](references/mcp-install.md)
- [runtime-policy.md](references/runtime-policy.md)
- [verification-checklist.md](references/verification-checklist.md)
