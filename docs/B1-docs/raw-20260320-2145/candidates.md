# Candidates

- id: C-20260320-2145-001
  title: Add explicit `cc` and `cc-use-codex-cli` top-level Freely tools
  status: promoted
  why_now:
    - 当前 `cc` 语义需要和 `cc-use-codex-cli` 固定 profile 拆开，避免 capability 参数泄漏到用户侧。
  promoted_issue_path: docs/B2-docs/config/claude-code-codex-mcp-runtime-governance/issues/claude-code-codex-mcp-runtime-governance.md
  legacy_id_mapping: I-20260321-0217  # 历史遗留的 issue id
  milestone: M-20260306-workspace-routing-foundation
  session_refs:
    - tool: cc-use-codex-cli
      session_id: unavailable://freely-runtime-uses-claude-session-id-state
      jsonl_path: unavailable://claude-code-does-not-expose-codex-jsonl
      role: worker
  acceptance_hint:
    - `freely init --ai cc:auto` 生成纯 `Claude Code` profile
    - `freely init --ai cc-use-codex-cli:auto` 生成固定 `Codex MCP` profile
    - 中断链和 monitor 不再硬编码 `codex exec`

- id: C-20260320-2145-002
  title: Use per-workcell Claude session-id as cc concurrency anchor
  status: absorbed
  why_now:
    - 多 worker / 多 worktree 并发必须立即稳定，不能阻塞在隐藏 `Codex threadId` 可见性上。
  promoted_issue_path: docs/B2-docs/config/claude-code-codex-mcp-runtime-governance/issues/claude-code-codex-mcp-runtime-governance.md
  decision_reason: 当前并发 continuity 语义已经由 `I-20260321-0217` 作为 canonical owner 吸收，并在该 issue 的 `additional_source_candidates` 中显式记录；不再单独 materialize 平行 issue。
  milestone: M-20260306-workspace-routing-foundation
  session_refs:
    - tool: cc
      session_id: unavailable://generated-at-runtime-and-persisted-in-session-state
      jsonl_path: unavailable://claude-session-has-no-jsonl-path
      role: worker
  acceptance_hint:
    - `cc` / `cc-use-codex-cli` 都必须通过 `session-id` 实现 workcell continuity
    - 缺少 `LAST_TOOL_SESSION_ID` 不得再让 `cc` 误触发 `missing_resume_evidence`
