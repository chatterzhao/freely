# Verification: codex-verified-resume-evidence-governance

- issue_id: `I-20260328-2105-A`
- verification_scope: feature-lane verification on canonical merge-prep branch before develop merge judgement
- verified_in_worktree: `feature/runtime-closeout-merge-prep-20260330`
- depends_on:
  - `I-20260319-0018`
  - `I-20260321-0217`

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
2. `bash -n docs/system/workspace/scripts/runtime/freely`
3. `./bin/governance-check`

## Result

- `docs/system/workspace/scripts/runtime/freely` no longer upgrades a bare observed `session_id` into resumable truth on the proven `codex` path unless Freely can also resolve rollout/jsonl evidence for that target.
- `tool_runtime_resume_target_after_cycle()` and `tool_has_resume_evidence()` now agree on the same evidence boundary: `LAST_TOOL_RESUME_TARGET` alone is insufficient when rollout/jsonl evidence is missing.
- `docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract` now locks both sides of the contract:
  - observed `session_id` plus rollout/jsonl keeps explicit `resume`
  - observed `session_id` without rollout/jsonl downgrades away from `resume`
- `./bin/governance-check` passed on the merge-prep lane with only the repository's pre-existing 10 legacy pre-brainstorm naming warnings.
- `feature/runtime-closeout-merge-prep-20260330` is the canonical absorption owner for this repair. The earlier isolated repro worktree remains provenance only, and `feature/runtime-auth-repro-closeout-20260330` is a superseded duplicate closeout lane rather than a separate active owner.

## Residual Risk

1. This owner intentionally stays `codex`-scoped; cross-tool explicit session-addressed resume audit remains follow-on work unless another issue proves shared failure shape.
2. The verification set is deliberately narrow and does not reclassify auth/watchdog or broader observability behavior into this owner.

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
