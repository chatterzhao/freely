---
local_id: I-20260321-0217
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '31'
    url: https://github.com/chatterzhao/freely/issues/31
    synced_at: '2026-04-27T11:14:48Z'
  gitee:
    issue_id: IJFO5R
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5R
    synced_at: '2026-04-27T13:14:24Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/claude-code-codex-mcp-runtime-governance/issues/claude-code-codex-mcp-runtime-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:14:48Z'
hash: ''
created_at: '2026-04-27T11:14:48Z'
updated_at: '2026-04-27T11:14:48Z'
platform_state: closed
---

Freely 已经支持多个顶层 AI tool，但 `Claude Code` 仍缺两类关键治理能力：

- 明确区分纯 `cc` 与固定 profile 的 `cc-use-codex-cli`
- 在 `cc-use-codex-cli` 下把 `Claude session-id -> Claude jsonl -> Codex threadId -> Codex jsonl` 收敛为可恢复、可并发验证的双层证据模型

如果缺这两层能力，Freely 无法稳定把 `Claude Code` 作为顶层 agent/context manager，同时让仓库实现默认下沉到 `Codex MCP`。

canonical: docs/B2-docs/config/claude-code-codex-mcp-runtime-governance/issues/claude-code-codex-mcp-runtime-governance.md
