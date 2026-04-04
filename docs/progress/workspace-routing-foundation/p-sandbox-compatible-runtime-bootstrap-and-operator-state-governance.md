# Progress: sandbox-compatible-runtime-bootstrap-and-operator-state-governance

- issue_id: `I-20260403-2245-A`
- issue_path: `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/issues/sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
- phase_state: `in_dev`
- runtime_state: `in_feature_worktree`
- branch: `feature/sandbox-compatible-runtime-bootstrap-and-operator-state-20260403-2245`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-2245-feature-sandbox-compatible-runtime-bootstrap-and-operator-state`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "materialization-and-dev-loop"}

## Summary

- This owner was split out from the `2026-04-03` governance-chain salvage cleanup after a real sandbox dead-end proved sibling worktree tool boundaries alone are insufficient.
- The first implementation slice is narrow: fallback operator-state bootstrap when default `$FREELY_HOME` is unwritable, plus ps-less degraded readiness/status evidence.

## Current Focus

- Materialize the runtime contract into `docs/system/workspace/scripts/runtime/freely`.
- Add focused regressions for fallback operator-state root and degraded process evidence.

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-sandbox-operator-state-bootstrap-fallback`
- `bash docs/system/workspace/scripts/tests/test-freely-status-degrades-when-ps-is-unavailable`
- `bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready`
- `./bin/governance-check`

## Next Action

- Implement the fallback/degraded runtime slice and keep the owner narrow enough to close without reopening parent umbrellas.
