# Pre-Tests: Enforce Test-Pre-Merge Gate

- issue_id: I-20260503T0915Z-enforce-test-pre-merge

## Unit
- acceptance target: `Keep the governance-merge-gate parser/validator narrow enough that missing C/M/I lifecycle links are surfaced as structured errors rather than silent omissions.`
- testing layer: `unit`
- target environment: `feature/raw-20260503T0915Z-enforce-test-pre-merge`
- required evidence: `./bin/governance-merge-gate --range develop..HEAD or explicit lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner introduces three doc-system scripts (governance-merge-gate, pr-merge-guarded changes, test-pr-merge-guarded) plus governance artifacts. The smallest executable boundary validated at the integration layer (test-pr-merge-guarded in an isolated temp repo) covers the script behavior, while the governance docs are validated by governance-merge-gate itself. There is no separately callable unit boundary in this work.`
- replacement_evidence: `The governance-merge-gate --range develop..HEAD self-validates the C/M/I chain on every run, which is the narrowest automated check that exists at this owner's layer.`

## Integration
- acceptance target: `Prove pr-merge-guarded enforces correct merge direction, produces guarded receipts, handles conflict completion, and supports break-glass for hotfix→develop merges.`
- testing layer: `integration`
- target environment: `test-pre-merge-enforce-gate-20260503`
- required evidence: `test-pr-merge-guarded script output plus verification review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded` in an isolated temp repo.
2. Run `./bin/governance-merge-gate --range develop..HEAD` in the feature worktree.
3. Run `./bin/governance-check` in the feature worktree.

## End-to-End
- acceptance target: `The guarded feature→test-pre-merge→develop merge chain passes the governance-merge-gate and produces canonical guarded merge receipts.`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `guarded feature→test-pre-merge→develop merge receipts plus owner review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/raw-20260503T0915Z-enforce-test-pre-merge` into `test-pre-merge-enforce-gate-20260503` via `freely pr-merge-guarded`.
2. Merge `test-pre-merge-enforce-gate-20260503` into `develop` via `freely pr-merge-guarded`.
3. Verify `Freely-Merge-Path`, `Freely-Bypass-Mode`, `Freely-Source-Branch` trailers in merge commit messages.

## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `This owner does not require an additional dedicated real-environment test beyond the guarded develop-bound verification path. The governance-merge-gate, pr-merge-guarded, and test-pr-merge-guarded are tooling scripts validated at integration and end-to-end layers. Post-merge observation remains a separate acceptance surface.`

## Acceptance Items

### AT-001 pr-merge-guarded direction enforcement
- id: `pr-merge-guarded-direction-enforcement`
- requirement: `pr-merge-guarded rejects invalid merge directions (feature→develop, hotfix→develop, feature→main) and allows valid ones (feature→test-pre-merge, test-pre-merge→develop).`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/test-pre-merge-enforcement/code-reviews/rev-20260503-enforce-test-pre-merge.md`

### AT-002 pr-merge-guarded receipt production
- id: `pr-merge-guarded-receipt-production`
- requirement: `Each guarded merge produces canonical Freely-* trailers in the merge commit message.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/test-pre-merge-enforcement/code-reviews/rev-20260503-enforce-test-pre-merge.md`

### AT-003 pr-merge-guarded conflict completion
- id: `pr-merge-guarded-conflict-completion`
- requirement: `Textual merge conflicts leave merge state intact and pr-merge-guarded complete finishes the merge with correct receipt trailers.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/test-pre-merge-enforcement/code-reviews/rev-20260503-enforce-test-pre-merge.md`

### AT-004 pr-merge-guarded break-glass support
- id: `pr-merge-guarded-break-glass-support`
- requirement: `Hotfix→develop break-glass merge produces Freely-Break-Glass-Reason, Freely-Evidence-Ref, and Freely-Follow-On-Issue trailers.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/test-pre-merge-enforcement/code-reviews/rev-20260503-enforce-test-pre-merge.md`

### AT-005 governance-merge-gate lifecycle validation
- id: `governance-merge-gate-lifecycle-validation`
- requirement: `governance-merge-gate blocks merges that lack proper candidate→milestone→issue lifecycle evidence.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/test-pre-merge-enforcement/code-reviews/rev-20260503-enforce-test-pre-merge.md`

### AT-006 guarded premerge self-bootstrap
- id: `guarded-premerge-self-bootstrap`
- requirement: `The guarded feature→test-pre-merge→develop path preserves governance lifecycle evidence and produces canonical guarded merge receipts.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `T-005 in docs/B2-docs/test-pre-merge-enforcement/tasks.md`
- case_design: `Merge feature/raw-20260503T0915Z-enforce-test-pre-merge into test-pre-merge-enforce-gate-20260503 via pr-merge-guarded, then merge into develop via pr-merge-guarded, verifying each step produces guarded receipts and passes governance gates.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/test-pre-merge-enforcement/code-reviews/rev-20260503-enforce-test-pre-merge.md`
