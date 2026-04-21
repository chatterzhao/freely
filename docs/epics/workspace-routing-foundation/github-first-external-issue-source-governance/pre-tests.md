# Pre-Tests: github-first-external-issue-source-governance

## Unit
- acceptance target: `The owner freezes a bounded GitHub-first external-source contract without widening into runtime API automation.`
- testing layer: `unit`
- target environment: `feature/external-issue-source-lifecycle-governance-20260420`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner freezes routing and contract truth, but does not yet add runtime API behavior.`
- replacement_evidence: `The owner issue, brainstorm, PRD, candidate, and verification review are the smallest useful unit for this bounded governance freeze.`

## Integration
- acceptance target: `Source-routing truth adopts the GitHub-first external-issue family contract without reintroducing GitHub as canonical owner truth.`
- testing layer: `integration`
- target environment: `feature/external-issue-source-lifecycle-governance-20260420`
- required evidence: `routing/test command output plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`.
2. Run `bash docs/system/workspace/scripts/tests/test-human-chat-routing`.
3. Run `./bin/governance-check`.
4. Run `git diff --check`.

## End-to-End
- acceptance target: `A guarded feature -> test-pre-merge -> develop chain accepts the bounded external-source governance owner as canonical truth.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-20260420-external-issue-source-governance`
- required evidence: `guarded merge replay trace plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Replay the bounded `feature/external-issue-source-lifecycle-governance-20260420 -> test-pre-merge-20260420-external-issue-source-governance -> develop` chain after the owner package is complete.

## Real-Environment
- acceptance target: `The owner remains justified by current self-host task-source needs without pretending runtime automation already exists.`
- testing layer: `real_environment`
- target environment: `develop`
- required evidence: `current self-host source-governance evidence plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `Current self-host analysis already shows external-source task discovery and closeout need a bounded contract before runtime implementation, and gh remains available for the future GitHub-first slice. The truthful protected-branch surface remains guarded premerge replay plus canonical develop absorption rather than a separate hosted runtime.`
- not_applicable_reason: `post_merge_only`
- not_applicable_explanation: `No new external API behavior is validated before merge; the real-environment obligation is to keep the contract tied to current self-host intake needs.`
- replacement_evidence: `The source brainstorm, candidate, and owner verification artifact capture the current self-host source-governance gap and the still-live GitHub-first boundary.`

## Acceptance Items

### Raw source scan stays narrow
- id: `external-source-scan-narrow`
- requirement: `Canonical docs define raw external source scan as open and unconsumed only, not all open GitHub issues.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/code-reviews/20260420-github-first-external-issue-source-governance-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1,tasks.md#task-2`
- case_design: `Review the source brainstorm, candidate, and owner issue together and confirm the scan rule is explicitly bounded to open and unconsumed source issues.`
- testcase_derivation: `The bounded contract changed only documentation and source-routing truth, so the executable derivation is a document-backed contract audit tied to the staged owner verification artifact rather than a new runtime API probe.`

### Canonical linkage stays decisive
- id: `canonical-linkage-decisive`
- requirement: `Canonical docs define repo-native linkage as decisive dedupe authority and external labels/comments as hints only.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/code-reviews/20260420-github-first-external-issue-source-governance-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Audit the source contract docs and source-routing skill docs, and confirm the language consistently keeps canonical repo-native linkage above stale external mirrors.`
- testcase_derivation: `This item derives from the owner's dedupe boundary change: verify the bounded contract and its consumer-facing routing docs stay aligned, because there is no narrower truthful runtime seam in this owner.`

### Source family term is corrected
- id: `external-issue-family-term-adopted`
- requirement: `Source-routing consumer docs use the external issue durable source-family term and keep GitHub scoped to the first platform slice.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/code-reviews/20260420-github-first-external-issue-source-governance-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-3,tasks.md#task-4`
- case_design: `Review context-source-skill, source-classification, lead-agent, and the startup prompt template, then confirm they now speak in terms of the external-issue family rather than the looser github-issue term.`
- testcase_derivation: `The changed consumer surfaces are `context-source-skill`, `source-classification`, `lead-agent`, and the startup prompt template, so the bounded derivation is a targeted wording audit anchored to the same staged verification artifact.`

### Guarded promote carries the external-source owner chain
- id: `external-source-guarded-promote`
- requirement: `The guarded test-pre-merge -> develop path carries this owner's issue, pre-tests, tasks, and review evidence instead of leaving the source contract in candidate-only state.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/code-reviews/20260420-github-first-external-issue-source-governance-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-4,tasks.md#task-5`
- case_design: `Use the authoritative test-pre-merge-20260420-autonomous-task-governance batch as the guarded promote surface, rerun the focused doc/routing checks there, and stage this owner review artifact with the same merge so develop no longer sees candidate-only evidence.`
- testcase_derivation: `The develop gate failure itself proved the missing seam: this owner needed a lane-bound adequacy item for premerge-integration/develop_merge. The derivation is therefore the guarded replay that stages the owner review artifact inside the canonical premerge batch.`
