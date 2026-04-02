# Pre-Tests: implementation-decision-notes-in-issue-review-artifacts-governance

## Acceptance Items

### AT-1 owner-bound review artifact required for implementation-bearing merge
- id: `decision-note-owner-review-required`
- requirement: `When a develop-bound merge materializes implementation-bearing paths, the merge gate resolves the owner issue and rejects the batch if no staged review artifact exists under that issue's verification_artifact_dir.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/implementation-decision-notes-in-issue-review-artifacts-governance/code-reviews/20260401-implementation-decision-notes-in-review-artifacts-verification.md`

### AT-2 decision note structure required
- id: `decision-note-structure-required`
- requirement: `A staged owner review artifact must contain the implementation decision note fields decision, why_this, alternatives_considered, boundary_non_goals, and residual_risk before the merge gate passes.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/implementation-decision-notes-in-issue-review-artifacts-governance/code-reviews/20260401-implementation-decision-notes-in-review-artifacts-verification.md`

### AT-3 laws and execution guidance stay aligned
- id: `decision-note-governance-alignment`
- requirement: `LAWS, dev-loop execution guidance, and IBM materialization checklist all point to the same canonical landing surface and minimum decision-note fields.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/implementation-decision-notes-in-issue-review-artifacts-governance/code-reviews/20260401-implementation-decision-notes-in-review-artifacts-verification.md`

## Acceptance Matrix

1. pre-merge focused regression / smoke
   - environment: `feature worktree`
   - evidence: `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`, `./bin/governance-check`
   - failure signal: merge gate tests fail or governance-check reports lifecycle inconsistency
   - failure handling / replay expectation: repair gate or governance truth in the feature worktree, rerun tests, and keep the owner out of completion until the artifact is green

2. post-merge integration acceptance
   - target environment: `develop`
   - environment type: `protected verification worktree`
   - evidence: first real develop-bound branch using the note can merge without ambiguity and the gate still rejects missing-note repros
   - failure signal: develop-side usage shows false positives / false negatives around owner review resolution or path detection
   - failure handling / replay expectation: reopen from a feature worktree and narrow the detection / review requirements without replacing the canonical landing surface

3. post-merge application-native real-environment acceptance
   - why_not_applicable: `This owner changes governance artifacts and merge-time enforcement only; no runtime process or long-lived supervisor behavior is introduced.`
   - replacement_evidence: `merge-gate regression plus the first real develop-bound usage`

4. post-merge end-to-end dogfood acceptance
   - target environment: `develop`
   - environment type: `protected verification worktree`
   - evidence: a later implementation lane touches `bin/`, `docs/system/`, or `src/`, writes a decision note under its owner review artifact, and the gate passes only with the note present
   - failure signal: dogfood merge bypasses the note or forces duplicate truth in multiple artifact families
   - failure handling / replay expectation: reopen a focused follow-on from a dedicated feature worktree and keep dogfood evidence anchored to the offending owner issue

## Blocker Taxonomy

- `definition_missing`: owner issue lacks `verification_artifact_dir` or the note contract is not written clearly enough to execute
- `commands_only`: review artifact exists but only lists commands / verdicts and does not contain the required decision-note fields
- `evidence_plan_missing`: tests or verification artifact refs are absent, so the owner cannot prove the gate behavior
- `execution_pending_or_failed`: gate implementation or regression tests are not yet passing
