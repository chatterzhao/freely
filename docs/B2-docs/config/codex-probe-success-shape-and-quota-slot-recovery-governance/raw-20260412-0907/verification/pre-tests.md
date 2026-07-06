# Pre-Tests: codex-probe-success-shape-and-quota-slot-recovery-governance

- issue_id: `I-20260412-0907-A`
- issue_path: `docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/issues/codex-probe-success-shape-and-quota-slot-recovery-governance.md`
- acceptance target: `codex hi probe success shape and reconnect-plus-quota slot recovery`

## Unit
- acceptance target: `The Codex hi probe only recognizes the fixed structural success transcript.`
- testing layer: `unit`
- target environment: `feature/runtime-slot-recovery-network-failure`
- required evidence: `focused probe contract regression`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-requires-expected-success-shape`.

## Integration
- acceptance target: `Reconnect-plus-403/quota evidence routes to slot-local recovery while pure reconnect/TLS evidence remains network-local.`
- testing layer: `integration`
- target environment: `feature/runtime-slot-recovery-network-failure`
- required evidence: `focused runtime classification regressions`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-log-defers-to-watchdog`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-active-runtime-reconnect-stays-network-local`.

## End-to-End
- acceptance target: `A bad current slot no longer stalls the manager path; the runtime advances to the next usable slot.`
- testing layer: `end_to_end`
- target environment: `dedicated feature worktree runtime replay`
- required evidence: `real bounded startup replay`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `./bin/ai switch codex account-worahe1001@outlook-com-1 --yes`.
2. Run `freely start --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-runtime-slot-recovery-network-failure`.
3. Capture `tail -n 80 .freely/logs/runtime-events.log`.
4. Confirm `~/.codex/active-slot` advances to `account-worahe1000@outlook-com-1`.
5. Run `freely stop --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-runtime-slot-recovery-network-failure`.

## Real-Environment
- acceptance target: `The guarded promote lane preserves the same owner-bound verification evidence without inventing a broader scheduler policy owner.`
- testing layer: `real_environment`
- target environment: `test-pre-merge-runtime-slot-recovery-20260412-1004`
- required evidence: `guarded promote replay plus governance-check`
- blocker taxonomy: `protected_environment_only`
- real_environment_status: `pass`
- real_environment_reason: `Merged into develop via 3ded2a09. Guarded promote replay confirmed owner-bound verification evidence is preserved.`
1. Run `./bin/governance-check`.

## Acceptance Items

### Probe success contract is fixed
- id: `probe-success-shape-frozen`
- requirement: `The watchdog probe only returns usable when the transcript matches user -> hi -> codex -> response -> tokens used.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/raw-20260412-0907/code-reviews/20260412-codex-probe-success-shape-and-quota-slot-recovery-verification.md`
- surface_kind: `unit`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `owner-bounded`
- case_design: `Exercise the probe helper against the canonical success shape and several false-positive transcript shapes so rc=0 alone can no longer pass.`

### Mixed reconnect-plus-quota logs defer to slot recovery
- id: `mixed-reconnect-quota-is-slot-local`
- requirement: `Reconnect text must not hide explicit 403/quota evidence behind execution_network classification.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/raw-20260412-0907/code-reviews/20260412-codex-probe-success-shape-and-quota-slot-recovery-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `owner-bounded`
- case_design: `Feed the runtime classifier reconnect plus 403 quota/precharge evidence and confirm the failure is treated as slot exhaustion instead of network-local retry.`

### Pure network evidence stays bounded
- id: `pure-network-remains-network-local`
- requirement: `Reconnect/TLS-only evidence still remains on the bounded execution-network retry path.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/raw-20260412-0907/code-reviews/20260412-codex-probe-success-shape-and-quota-slot-recovery-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `owner-bounded`
- case_design: `Run the existing reconnect/TLS regression to verify the owner does not widen into generic network policy changes.`

### Real bad-slot replay shows forward progress
- id: `bad-slot-runtime-replay-advances`
- requirement: `A bad current account slot should trigger bounded same-tool recovery to the next usable slot during freely start.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/raw-20260412-0907/code-reviews/20260412-codex-probe-success-shape-and-quota-slot-recovery-verification.md`
- surface_kind: `real_environment`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `owner-bounded`
- case_design: `Replay freely start from a known bad account slot, inspect runtime-events, and verify active-slot moves to the next usable account slot before stopping the runtime.`

### Guarded promote remains owner-scoped
- id: `develop-promote-owner-scope-preserved`
- requirement: `The develop-bound merge uses the same bounded owner evidence and does not rely on missing pre-tests metadata or incomplete review notes.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/raw-20260412-0907/code-reviews/20260412-codex-probe-success-shape-and-quota-slot-recovery-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `owner-bounded`
- case_design: `Replay governance-check in the guarded premerge lane and confirm the owner carries complete acceptance items, execution-phase lifecycle, and implementation decision fields before promote.`
