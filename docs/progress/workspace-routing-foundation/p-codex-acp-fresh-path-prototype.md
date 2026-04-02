# Progress: codex-acp-fresh-path-prototype

- issue_id: `I-20260401-1545-A-01`
- title: Codex ACP fresh-path prototype
- phase_state: `completed`
- runtime_state: `stopped`
- branch: `feature/acp-client-agent-protocol-research-20260401`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260401-feature-acp-client-agent-protocol-research`
- issue_path: `docs/epics/workspace-routing-foundation/codex-acp-fresh-path-prototype/issues/codex-acp-fresh-path-prototype.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "dev-loop-author"}
  - {tool: shell, session_id: "51019", jsonl_path: "unavailable://pty-download-session", role: "binary-acquisition-exec"}
  - {tool: codex, session_id: "019d4c11-0bc0-7492-a63f-e9bbc1962d5b", jsonl_path: "unavailable://codex-acp-binary-session", role: "real-acp-fresh-sample"}

## Summary

- `codex + adapter=acp` 的 first real fresh-path prototype 已实现到 runtime truth：launcher dispatch、one-shot ACP client、Codex ACP binary resolution/cache、fake ACP end-to-end regression、direct-path non-regression coverage 都已落地。
- fake ACP focused coverage 现在已同时锁住 `fresh` 与 `fresh_with_handoff`，当前 owner scope 内最后一个明确的验证缺口已补齐。
- 真实环境 viability evidence 现在已补齐：pinned `codex-acp` binary acquisition 成功，最小 fresh task 返回 `ACP_OK`，真实 ACP session id 为 `019d4c11-0bc0-7492-a63f-e9bbc1962d5b`。

- summary: `The first real codex + adapter=acp prototype is now merged and verified on develop. Canonical develop keeps the ACP bridge green for fresh and fresh_with_handoff while direct path remains the strongest explicit resume surface.`
- closure_status: `merged-and-verified`
- closure_evidence:
  - `merge_commit: a0f9a48`
  - `tests: bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-acp-fresh`
  - `tests: bash docs/system/workspace/scripts/tests/test-freely-tool-adapter-policy-resolution`
  - `review: docs/epics/workspace-routing-foundation/codex-acp-fresh-path-prototype/code-reviews/20260401-codex-acp-fresh-path-prototype-verification.md`
  - `governance: ./bin/governance-check`
