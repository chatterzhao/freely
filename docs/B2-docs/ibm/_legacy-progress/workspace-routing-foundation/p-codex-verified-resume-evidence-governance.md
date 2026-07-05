# Progress: codex-verified-resume-evidence-governance

- issue_id: `I-20260328-2105-A`
- title: Codex verified resume evidence governance
- phase_state: `completed`
- runtime_state: `stopped`
- branch: `develop`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely`
- issue_path: `docs/B2-docs/config/codex-verified-resume-evidence-governance/issues/codex-verified-resume-evidence-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "verification-writeback"}

## Summary

- The lane has completed dev-loop and verification; the repair is already absorbed into `develop`.
- The current implementation narrows the repair to the proven `codex` chain: a bare observed `session_id` no longer becomes resumable truth unless Freely can also trace rollout/jsonl evidence for that target.
- Healthy explicit `resume` remains allowed when persisted or newly observed rollout/jsonl evidence is present.
- The repair is present on `develop` via commit `20574fa`, so the earlier merge-prep and repro branches are provenance only and should not be revived as active owners.

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
4. verification artifact written to `docs/B2-docs/config/codex-verified-resume-evidence-governance/code-reviews/20260330-codex-verified-resume-evidence-feature-verification.md`

## Closure Evidence

- closure_status: `merged-and-verified`
- closure_evidence:
  - `develop` commit `20574fa`
  - `bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
  - `./bin/governance-check`
  - `docs/B2-docs/config/codex-verified-resume-evidence-governance/code-reviews/20260330-codex-verified-resume-evidence-feature-verification.md`

## Next Action

1. Keep this owner closed; any future resume-evidence changes should open a new lifecycle instead of reviving the old merge-prep lane.
2. Treat the earlier isolated repro and merge-prep worktrees as source provenance only.
