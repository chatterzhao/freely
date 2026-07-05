# Pre-tests: codex-verified-resume-evidence-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `codex verified resume evidence boundary`
- testing layer: `isolated repro + focused regression`
- target environment: `feature worktree`
- required evidence: invalid-target repro, focused runtime regression, and verification artifact
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. Reproduce the invalid target in an isolated worktree: `codex exec resume <bad-session-id>` must fail with `no rollout found for thread id`.
2. Freeze the field contract: a cycle that ends with `session_id` but `jsonl_path=unavailable` is not sufficient resume evidence.
3. Add a focused regression: `observed session id + missing rollout/jsonl` must not select next-cycle `resume`.
4. Preserve the healthy path: valid rollout-backed `codex` resume evidence still selects `resume`.
5. Preserve orthogonal behavior: auth/watchdog recovery semantics remain unchanged by this issue.

### Post-merge canonical truth acceptance

- acceptance target: `develop carries the repaired codex continuity truth`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: progress closeout, verification artifact, and develop commit provenance
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. The owner must not remain `in_verification` once `develop` already contains the rollout/jsonl evidence repair.
2. Verification and progress truth must point at the canonical develop absorption, not stale merge-prep or repro-only branches.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `invalid resume targets without rollout/jsonl evidence fail in isolation`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/config/codex-verified-resume-evidence-governance/code-reviews/20260330-codex-verified-resume-evidence-feature-verification.md`

### PT-2
- id: `PT-2`
- requirement: `observed session id without rollout/jsonl evidence does not select explicit resume next cycle`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/config/codex-verified-resume-evidence-governance/code-reviews/20260330-codex-verified-resume-evidence-feature-verification.md`

### PT-3
- id: `PT-3`
- requirement: `healthy rollout-backed codex resume remains available`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`

### PT-4
- id: `PT-4`
- requirement: `canonical closeout points at develop commit 20574fa instead of stale merge-prep provenance`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/progress/workspace-routing-foundation/p-codex-verified-resume-evidence-governance.md`
