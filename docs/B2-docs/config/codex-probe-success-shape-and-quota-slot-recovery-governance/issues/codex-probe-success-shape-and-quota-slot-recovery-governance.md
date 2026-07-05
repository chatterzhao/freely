# Issue: codex-probe-success-shape-and-quota-slot-recovery-governance

- issue_id: `I-20260412-0907-A`
- title: Codex probe success shape and quota slot recovery governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `codex-probe-success-shape-and-quota-slot-recovery-governance`
- issue-name: `codex-probe-success-shape-and-quota-slot-recovery-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260412T184500Z/candidates.md#c-20260412-0907-a`
- source_brainstorm: `docs/B1-docs/raw-20260412T184500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-probe-success-shape-and-quota-slot-recovery-governance.md`
- verification_artifact_dir: `docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/code-reviews`
- follow_on_to: `I-20260410-1835-B`
- created_at: `2026-04-12`
- session_refs: []

## Why

Real dogfooding on 2026-04-12 exposed a narrower follow-on regression in the already completed Codex recovery family:

1. `codex exec "hi"` probe success was too weak and could still produce false positives
2. runtime failure classification still let reconnect-plus-403/quota evidence fall into `execution_network_*`, which kept the bad current slot alive instead of moving forward

This is not a new generic network-taxonomy owner. It is a bounded closeout of the specific mismatch between real `hi` transcript truth and slot-local quota/auth failure handling.

## Scope

1. Tighten Codex `hi` probe success to a single structural success transcript.
2. Route reconnect-plus-403/quota evidence into slot-local exhaustion recovery.
3. Keep pure reconnect/TLS/network evidence on the bounded execution-network retry path.
4. Freeze the real bad-account startup replay as owner evidence.

## Non-Goals

1. Do not remove the execution-network taxonomy for true environment failures.
2. Do not widen this owner into generic scheduler or cross-tool fallback policy.
3. Do not require the actual Codex reply text to equal `hi`; only the transcript structure is canonicalized.

## Acceptance

1. The watchdog probe only returns `usable` when the `hi` transcript matches `user -> hi -> codex -> response -> tokens used`.
2. Any other `hi` transcript shape is treated as failure-first, regardless of `rc`.
3. Runtime classification treats reconnect-plus-403/quota evidence as slot-local exhaustion and triggers same-tool slot recovery.
4. Pure reconnect/TLS evidence still remains `execution_network_*` and does not authorize slot recovery.
5. A real bad-account `freely start` replay auto-switches to the next usable slot.

## Verification

- `docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/code-reviews/20260412-codex-probe-success-shape-and-quota-slot-recovery-verification.md`

## Completion

- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-codex-probe-requires-expected-success-shape`
- `docs/system/workspace/scripts/tests/test-freely-rate-limit-log-defers-to-watchdog`
- `docs/system/workspace/scripts/tests/test-freely-active-runtime-reconnect-stays-network-local`

## Next

- Feature implementation and focused verification are complete in the dedicated feature worktree. Promote through `test-pre-merge-runtime-slot-recovery-20260412-1004` and guarded merge to `develop`, then close out the owner on canonical `develop`.
