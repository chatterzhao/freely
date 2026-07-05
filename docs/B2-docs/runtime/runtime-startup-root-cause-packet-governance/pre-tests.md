# Pre-Tests: runtime-startup-root-cause-packet-governance

## Unit
- acceptance target: `The packet split between startup-authority implementation and manager-handoff follow-on is explicit and deterministic.`
- testing layer: `unit`
- target environment: `feature/runtime-foreground-double-start-regression-20260413`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner only materializes document routing and owner truth; it does not add a smaller executable boundary below the governance packet itself.`
- replacement_evidence: `The owner issue, packet brainstorm, progress record, and verification artifact together are the smallest useful boundary for this documentation-only owner.`

## Integration
- acceptance target: `The packet lands as one bounded owner that writes canonical split truth without widening into runtime implementation.`
- testing layer: `integration`
- target environment: `feature/runtime-foreground-double-start-regression-20260413`
- required evidence: `governance/test command output plus owner review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-pretests-gate`.
2. Run `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`.
3. Run `./bin/governance-check`.
4. Run `git diff --check`.

## End-to-End
- acceptance target: `A guarded feature -> test-pre-merge -> develop chain accepts the packet as a concrete owner instead of rejecting it as candidate-only truth.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-20260413-runtime-startup-authority-follow-on-packet`
- required evidence: `guarded merge replay trace plus owner review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Replay the bounded `feature/runtime-foreground-double-start-regression-20260413 -> test-pre-merge-20260413-runtime-startup-authority-follow-on-packet -> develop` chain after the packet owner is materialized.

## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `This owner is documentation-only and does not change hosted/runtime execution surfaces; guarded promote and governance evidence are sufficient for its bounded scope.`

## Acceptance Items

### Packet split is frozen
- id: `startup-root-cause-packet-split-frozen`
- requirement: `Canonical docs freeze that startup authority is the promote-ready implementation lane and manager handoff remains a separate research-visible follow-on.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-startup-root-cause-packet-governance/code-reviews/20260413-runtime-startup-root-cause-packet-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1,tasks.md#task-2`
- case_design: `Review the pre-brainstorm packet, owner docs, and milestone writeback together and confirm the split freezes A as the implementation boundary, B as the research boundary, and C as the packet owner only.`

### No premature implementation claim
- id: `no-premature-runtime-fix-claim`
- requirement: `The packet owner does not claim fake-supervisor, daemon-ready, or manager continuity behavior is already repaired.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-startup-root-cause-packet-governance/code-reviews/20260413-runtime-startup-root-cause-packet-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Audit the new owner docs and milestone changes for routing-only language, and confirm no runtime/system files changed in the packet diff.`

### Develop promote has concrete owner truth
- id: `develop-promote-concrete-owner-truth`
- requirement: `The guarded develop promote consumes issue/progress/review truth for this packet instead of failing as candidate-only evidence.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-startup-root-cause-packet-governance/code-reviews/20260413-runtime-startup-root-cause-packet-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-3,tasks.md#task-4`
- case_design: `Replay the guarded test-pre-merge batch after materializing the packet owner and confirm the merge path is now evaluated against concrete owner artifacts rather than candidate-only truth.`
