# Candidates - 20260320-1628--claude-code-codex-mcp-tool-routing

## Context
- Source brainstorm: ./brainstorms.md
- Status: proposed

## Candidates

### C-20260320-1628-A
- title: Add a standard Claude Code install/provider/MCP workflow to Freely
- problem: Freely 当前把顶层 `tool` 视为主执行 CLI，但尚未表达“Claude Code 作为执行器、内部再挂 Codex MCP 能力”这类组合路径。若继续把这种组合硬塞成新的长名字 tool，会把执行器、模型和内部能力耦合成不可扩展的命名。
- why_now: 研究已验证 `Claude Code + Codex MCP` 在本机可正常使用，且前置条件已经收敛清楚：Claude 主 provider 必须先可用，Codex 作为其内部 MCP capability 被调用。这已经从概念讨论进入可实施的运行器接入问题。
- acceptance_hint:
  - 面向用户意图提供完整 workflow：`cc install -> provider setup -> codex mcp install -> verification`
  - skill 命名必须表达“在 `cc` 中调用 `codex`”，而不是把两者误建模为并列顶层工具
  - 宪法与 runtime 支持新增顶层 `tool=cc`
  - 保持 `tool:model:mode` 只描述主执行器契约
  - 新增 `tool-capability` 或 `cc-mcp-profile` 这类侧向配置，不把 MCP profile 塞进 `tool` 名
  - Claude Code project-scoped MCP server 配置可由 runtime / GUI / TUI 一致管理
  - 明确 `tool=cc` 的运行前提是 Claude 主 provider 已 ready；Codex MCP 不能替代该前提
  - 在 `tool=cc` 且启用 `codex-cli` 时，runtime 必须定义 `codex` / `codex-reply` 的自动路由与 `threadId` continuity 规则
  - `auto/step` 模式需要分别映射到 Claude permission mode 与 Codex approval-policy
  - 默认 Codex 接法优先使用内置 `codex mcp-server`，第三方 wrapper 仅作为备选
- priority: P1
- status: proposed
- decision_reason: 这条路径已经在本机通过 `CCR + Claude Code + codex mcp-server` 跑通。下一步不应只做零散文档说明，而应把它固化成 Freely 可重复执行的标准 workflow 和 tool skill，并把 `codex` / `codex-reply` 两个 MCP 调用面映射成 Freely 的自动运行时策略。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
