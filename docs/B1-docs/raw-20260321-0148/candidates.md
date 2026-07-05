# Candidates

- id: C-20260321-0148-001
  title: Add exact Claude/Codex session evidence resolution for cc-based tools
  status: promoted
  why_now:
    - 当前 `cc-use-codex-cli` 已可用，但恢复与多并发证据仍偏弱，应该升级为精确 jsonl 解析。
  promoted_issue_path: docs/B2-docs/config/claude-code-codex-mcp-runtime-governance/issues/claude-code-codex-mcp-runtime-governance.md
  milestone: M-20260306-workspace-routing-foundation
  session_refs:
    - tool: cc-use-codex-cli
      session_id: 11111111-2222-4333-8444-555555555555
      jsonl_path: /Users/zhaoyu/.claude/projects/-private-tmp-freely-cc-codex-real-ed64yw-project/11111111-2222-4333-8444-555555555555.jsonl
      role: worker
    - tool: codex-cli
      session_id: 019d0f86-7c2e-7f50-999f-10cf4935e7ba
      jsonl_path: pending://runtime-should-resolve-from-thread-id
      role: worker
  acceptance_hint:
    - runtime 必须优先使用 `Claude session-id` 定位 `Claude jsonl`
    - `Codex threadId` 必须从 `Claude jsonl` 提取，而不是只靠 debug log
    - `Codex jsonl path` 必须用 `threadId` 精确反查，不再默认 `unavailable://...`
