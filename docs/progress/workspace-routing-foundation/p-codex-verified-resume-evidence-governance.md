# Progress: codex-verified-resume-evidence-governance

- issue_id: `I-20260328-2105-A`
- title: Codex verified resume evidence governance
- phase_state: `in_verification`
- runtime_state: `stopped`
- branch: `feature/runtime-closeout-merge-prep-20260330`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260330-feature-runtime-closeout-merge-prep`
- issue_path: `docs/epics/workspace-routing-foundation/codex-verified-resume-evidence-governance/issues/codex-verified-resume-evidence-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "verification-writeback"}

## Summary

- The lane has completed dev-loop and is now in verification on the canonical merge-prep branch.
- The current implementation narrows the repair to the proven `codex` chain: a bare observed `session_id` no longer becomes resumable truth unless Freely can also trace rollout/jsonl evidence for that target.
- Healthy explicit `resume` remains allowed when persisted or newly observed rollout/jsonl evidence is present.
- `2026-03-30 18:18 PDT` the repaired lane was absorbed into develop-based merge-prep branch `feature/runtime-closeout-merge-prep-20260330`, so the canonical owner truth no longer lives only in the earlier isolated repro worktree.
- The separate closeout branch `feature/runtime-auth-repro-closeout-20260330` is now superseded by this merge-prep lane and should not become a competing absorption path.

## Implemented slice

1. `docs/system/workspace/scripts/runtime/freely` now treats `codex` resume evidence as verified only when the target has a traceable jsonl artifact.
2. `tool_runtime_resume_target_after_cycle()` no longer upgrades session-id-only observations into next-cycle `resume_target`.
3. `tool_has_resume_evidence()` now rejects stale `codex` state when only `LAST_TOOL_RESUME_TARGET` exists and rollout/jsonl evidence is missing.
4. `docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract` now covers both sides of the contract:
   - observed `session_id` plus rollout/jsonl keeps explicit `resume`
   - observed `session_id` without rollout/jsonl downgrades away from `resume`

## Verification

1. `bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
2. `bash -n docs/system/workspace/scripts/runtime/freely`
3. `./bin/governance-check`
4. verification artifact written to `docs/epics/workspace-routing-foundation/codex-verified-resume-evidence-governance/code-reviews/20260330-codex-verified-resume-evidence-feature-verification.md`

## Next Action

1. Keep `feature/runtime-closeout-merge-prep-20260330` as the active absorption owner until develop merge judgement.
2. Treat the earlier isolated repro worktree as source provenance only; further continuity cleanup should route through merge-prep instead of reviving the isolated branch-local lane.
3. Retire the duplicate closeout lane after this merge-prep branch is absorbed.
