# Pre-Tests: pre-tests-cleanup-and-retirement-enforcement-governance

## Unit
- acceptance target: `Retirement gate reads issue-bound pre-tests binding without widening into repository-wide scan behavior.`
- testing layer: `unit`
- target environment: `feature/pretests-cleanup-retirement-enforcement-20260411`
- required evidence: `focused gate/runtime regression output`
- blocker taxonomy: `definition_missing`
1. Run `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`.

## Integration
- acceptance target: `Cleanup or retire flow refuses retirement when required pre-tests evidence is still pending or insufficient.`
- testing layer: `integration`
- target environment: `feature/pretests-cleanup-retirement-enforcement-20260411`
- required evidence: `command output plus verification review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run the focused cleanup/retirement regression set added by this owner.
2. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `A completed or merged worktree can still be retained when cleanup evidence is not closed, and can retire only after the bound pre-tests contract is satisfied.`
- testing layer: `end_to_end`
- target environment: `cleanup followthrough lane`
- required evidence: `retained-versus-retired decision capture in verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-pretests-retain`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-retained-continuation`.

## Real-Environment
- acceptance target: `This owner consumes local lifecycle and cleanup truth; no separate hosted environment is introduced.`
- testing layer: `real_environment`
- target environment: `local cleanup lifecycle boundary`
- required evidence: `lawful replacement evidence recorded in verification artifact`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The bounded surface is cleanup and retirement governance within the local lifecycle system.`
- replacement_evidence: `Focused lifecycle regressions and retained-versus-retired captures are sufficient for this owner.`

## Acceptance Items

### Retirement reads issue pre-tests binding
- id: `retirement-reads-pre-tests-binding`
- requirement: `Cleanup and retirement flows consume the issue-bound pre_tests_path instead of relying on implicit lifecycle heuristics alone.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Read owner issue metadata from recorded worker state before retirement and route retirement checks through a dedicated pretests-retirement gate.`
- case_design: `Use a fixture worktree whose recorded owner issue and pre-tests path are consumed by the retirement gate, then prove missing or ambiguous bindings fail closed.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/code-reviews/20260411-pre-tests-cleanup-and-retirement-enforcement-verification.md`

### Pending items block retirement
- id: `pending-pretests-block-retirement`
- requirement: `Pending acceptance items or insufficient evidence block retirement and identify the failing item ids machine-readably.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Block cleanup retirement when required acceptance items remain pending or evidence is unavailable, and surface blocker item ids in the retained resolution artifact.`
- case_design: `Replay cleanup followthrough once with pending acceptance items and once with the retirement gate itself unavailable, then verify both cases retain the merged worktree with explicit blocked reasons.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/code-reviews/20260411-pre-tests-cleanup-and-retirement-enforcement-verification.md`

### Existing gates stay intact
- id: `completion-merge-no-regression`
- requirement: `Completion and develop-merge pre-tests gates remain unchanged while cleanup and retirement gain the missing closure gate.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Keep completion and merge gates untouched while adding cleanup-followthrough retention and continuation escalation on top of the same issue-owned pre-tests truth.`
- case_design: `Verify a clean merged worktree still retires, while a dirty merged worktree escalates to manager continuation rather than being force-retired or ignored.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/code-reviews/20260411-pre-tests-cleanup-and-retirement-enforcement-verification.md`

### Guarded develop promote stays adequate
- id: `develop-promote-cleanup-adequacy`
- requirement: `The develop-bound guarded merge for this owner keeps an explicit adequacy item tied to premerge replay instead of relying on feature-local completion evidence alone.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `Replay the owner on its test-pre-merge lane, rerun the focused premerge checks, and prove the resulting develop-bound diff still carries adequate owner evidence.`
- case_design: `Merge the feature lane into its test-pre-merge batch, run the focused premerge cleanup/governance regressions plus governance-check, then require guarded develop promote to consume this owner-bound verification artifact from the staged diff.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/code-reviews/20260411-pre-tests-cleanup-and-retirement-enforcement-verification.md`
