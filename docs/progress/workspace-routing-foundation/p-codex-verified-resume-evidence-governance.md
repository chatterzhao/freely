# Progress: codex-verified-resume-evidence-governance

- issue_id: `I-20260328-2105-A`
- title: Codex verified resume evidence governance
- phase_state: `in_dev`
- runtime_state: `stopped`
- branch: `feature/runtime-invalid-resume-repro-20260328-2020`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260328-2020-feature-runtime-invalid-resume-repro`
- issue_path: `docs/epics/workspace-routing-foundation/codex-verified-resume-evidence-governance/issues/codex-verified-resume-evidence-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "dev-loop-implementation"}

## Summary

- The lane has now moved from IBM into dev-loop.
- The current implementation narrows the repair to the proven `codex` chain: a bare observed `session_id` no longer becomes resumable truth unless Freely can also trace rollout/jsonl evidence for that target.
- Healthy explicit `resume` remains allowed when persisted or newly observed rollout/jsonl evidence is present.

## Implemented slice

1. `docs/system/workspace/scripts/runtime/freely` now treats `codex` resume evidence as verified only when the target has a traceable jsonl artifact.
2. `tool_runtime_resume_target_after_cycle()` no longer upgrades session-id-only observations into next-cycle `resume_target`.
3. `tool_has_resume_evidence()` now rejects stale `codex` state when only `LAST_TOOL_RESUME_TARGET` exists and rollout/jsonl evidence is missing.
4. `docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract` now covers both sides of the contract:
   - observed `session_id` plus rollout/jsonl keeps explicit `resume`
   - observed `session_id` without rollout/jsonl downgrades away from `resume`

## Verification

1. `bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
2. `bash docs/system/workspace/scripts/tests/test-freely-session-rotation`
   - the run still passes the earlier rotation/continuity assertions up to the pre-existing late failure `expected local runtime to defer rate-limit recovery instead of sleeping locally`

## Next Action

1. Restack this lane onto current `develop` so the materialized candidate / issue / progress truth stops living only in a behind worktree.
2. Re-run the narrow resume-evidence regressions after restack.
3. If the restacked lane stays green, add the checkpoint commit that canonically materializes `I-20260328-2105-A` plus the runtime/test repair.
