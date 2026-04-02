# Progress: codex-acp-fresh-path-prototype

- issue_id: `I-20260401-1545-A-01`
- title: Codex ACP fresh-path prototype
- phase_state: `in_verification`
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

## Current Focus

- 保留 verification evidence，准备后续 merge/closeout。
- 继续维持当前 contract：`codex + adapter=acp` 已验证 fresh-path 可行；explicit `resume` 仍不得假装 parity。
- 不把 runtime-level dogfood、resume parity 或额外 ACP tool rollout 偷渡进本 owner；这些若需要，必须另开后续 lifecycle。

## Verification

- `bash -n docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `bash -n docs/system/workspace/scripts/monitor-ai-cli.sh`
- `python3 -m py_compile docs/system/workspace/scripts/runtime/run-acp-prompt.py`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-acp-fresh`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-adapter-dispatch`
- `bash docs/system/workspace/scripts/tests/test-freely-tool-adapter-policy-resolution`
- `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
- `FREELY_CODEX_ACP_BIN=\"$HOME/.cache/freely/acp/codex-acp/0.11.1/aarch64-apple-darwin/codex-acp\" bash docs/system/workspace/scripts/monitor-ai-cli.sh --project /tmp/freely-real-codex-acp.k6v8y7/project --tool codex --tool-adapter acp --model gpt-5.4 --reasoning-effort medium --mode auto --prompt-file /tmp/freely-real-codex-acp.k6v8y7/prompt.txt --pid-file /tmp/freely-real-codex-acp.k6v8y7/ai.pid --log-file /tmp/freely-real-codex-acp.k6v8y7/ai.log --launch-kind fresh`
- `./bin/governance-check`
- `docs/epics/workspace-routing-foundation/codex-acp-fresh-path-prototype/code-reviews/20260401-codex-acp-fresh-path-prototype-verification.md`

## Closure Prep

- closeout_status: `merge_ready_pending_develop_absorption`
- closeout_evidence:
  - `docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-acp-fresh`
  - `docs/system/workspace/scripts/tests/test-monitor-ai-cli-adapter-dispatch`
  - `docs/epics/workspace-routing-foundation/codex-acp-fresh-path-prototype/code-reviews/20260401-codex-acp-fresh-path-prototype-verification.md`
  - `docs/progress/workspace-routing-foundation/p-codex-acp-fresh-path-prototype.md`
  - `./bin/governance-check`

## Next Action

- 当前 owner 的 scope-level verification 已完成；下一步是 merge/closeout，而不是继续扩 scope。
- 若后续要追 `codex + adapter=acp` 的 explicit resume parity，必须新开后续 owner，不在本条完成面里偷渡。
