# Candidates - 20260320-1628--claude-code-codex-mcp-tool-routing

## Context
- Source brainstorm: ./brainstorms.md
- Status: proposed

## Candidates

### C-20260320-1628-A: legacy issue
- title: Add a standard Claude Code install/provider/MCP workflow to Freely
- problem: Freely 当前把顶层 `tool` 视为主执行 CLI，但尚未表达“Claude Code 作为执行器、内部再挂 Codex MCP 能力”这类组合路径。若继续把这种组合硬塞成新的长名字 tool，会把执行器、模型和内部能力耦合成不可扩展的命名。
- why_now: 研究已验证 `Claude Code + Codex MCP` 在本机可正常使用，且前置条件已经收敛清楚：Claude 主 provider 必须先可用，Codex 作为其内部 MCP capability 被调用。这已经从概念讨论进入可实施的运行器接入问题。
- acceptance_hint:
  - 面向用户意图提供完整 workflow：`cc install -> provider setup -> codex mcp install -> verification`
  - 保留两个显式顶层工具：`cc` 与固定 profile 的 `cc-use-codex-cli`
  - 最终产物必须包含 `skill:tool-cc-codex-mcp-runtime`
  - `tool=cc` 的运行前提是 Claude 主 provider 已 ready；Codex MCP 不能替代该前提
  - `cc-use-codex-cli` 必须固定注入 `model/sandbox/approval-policy/cwd` 等 Codex MCP policy
  - runtime 必须定义 `Claude session-id -> Claude jsonl -> Codex threadId -> Codex jsonl` 的会话证据链
  - `auto/step` 模式需要分别映射到 Claude permission mode 与 Codex approval-policy
  - 默认 Codex 接法优先使用内置 `codex mcp-server`，第三方 wrapper 仅作为备选
- priority: P1
- status: promoted
- decision_reason: 这条路径已经在本机通过 `CCR + Claude Code + codex mcp-server` 跑通，并最终收敛成 `cc` / `cc-use-codex-cli` 两个显式工具、`skill:tool-cc-codex-mcp-runtime`、以及双层 session evidence runtime。早期 capability-only 命名建议已被后续实现与用户交互方式取代。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260320-1628-A/issue.md
- milestone: M-20260320-1628-A
- session_refs:
  - tool: cc-use-codex-cli
    session_id: 11111111-2222-4333-8444-555555555555
    jsonl_path: /Users/zhaoyu/.claude/projects/-private-tmp-freely-cc-codex-real-ed64yw-project/11111111-2222-4333-8444-555555555555.jsonl
    role: integration-smoke
  - tool: codex-cli
    session_id: 019d0f86-7c2e-7f50-999f-10cf4935e7ba
    jsonl_path: /Users/zhaoyu/.codex/sessions/2026/03/21/rollout-2026-03-21T01-27-02-019d0f86-7c2e-7f50-999f-10cf4935e7ba.jsonl
    role: integration-smoke
