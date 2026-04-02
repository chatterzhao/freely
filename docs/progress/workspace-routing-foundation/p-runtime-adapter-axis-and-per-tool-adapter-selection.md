# Progress: runtime-adapter-axis-and-per-tool-adapter-selection

- issue_id: `I-20260401-1703-A`
- title: Runtime adapter axis and per-tool adapter selection
- phase_state: `in_dev`
- runtime_state: `stopped`
- branch: `feature/acp-client-agent-protocol-research-20260401`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260401-feature-acp-client-agent-protocol-research`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-adapter-axis-and-per-tool-adapter-selection/issues/runtime-adapter-axis-and-per-tool-adapter-selection.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "dev-loop-author"}

## Summary

- runtime `adapter axis` 已 materialize 到 config、dispatch、status、受管 mutation 与 per-tool supported-adapter matrix；`AI_TOOL_ADAPTER` 与 `AI_TOOL_ADAPTER_POLICY` 现在是 canonical runtime truth，而 `direct` 继续保持 first-class path。
- 当前 progress 把这条 owner 从 `done_ibm` 推进到 `in_dev`，使其与同次 develop-bound capability merge 对齐；follow-on prototype owner `I-20260401-1545-A-01` 继续在同一 lifecycle 线上消费这套 adapter truth。

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-tool-adapter-policy-resolution`
- `bash docs/system/workspace/scripts/tests/test-freely-set-tool-command`
- `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-adapter-dispatch`
- `./bin/governance-check`
