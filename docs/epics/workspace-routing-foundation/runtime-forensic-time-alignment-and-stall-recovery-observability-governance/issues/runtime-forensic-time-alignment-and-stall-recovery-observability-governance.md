# Issue: runtime-forensic-time-alignment-and-stall-recovery-observability-governance

- issue_id: `I-20260412-1845-A`
- title: Runtime forensic time alignment and stall recovery observability governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-forensic-time-alignment-and-stall-recovery-observability-governance`
- issue-name: `runtime-forensic-time-alignment-and-stall-recovery-observability-governance`
- priority: `P1`
- source_candidate: `docs/pre-brainstorms/20260412-1845--runtime-forensic-time-alignment-and-stall-observability/candidates.md#c-20260412-1845-a`
- source_brainstorm: `docs/pre-brainstorms/20260412-1845--runtime-forensic-time-alignment-and-stall-observability/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-forensic-time-alignment-and-stall-recovery-observability-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-human-readable-time-display-governance/issues/runtime-human-readable-time-display-governance.md`
  - `docs/epics/workspace-routing-foundation/application-native-runtime-observation-contract-and-observability-planes/issues/application-native-runtime-observation-contract-and-observability-planes.md`
  - `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
- created_at: `2026-04-12`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

The 2026-04-12 self-host manager stall investigation first looked ambiguous because the evidence planes used different time expressions:

1. `runtime-events.log` recorded UTC RFC3339
2. prompt / cycle log / session jsonl were first inspected through host-local file mtime
3. stall recovery left state-file residue but no explicit runtime event

After absolute-time alignment, the incident proved to be one run, not mixed historical runs:

- startup at `2026-04-13T01:12:03Z` matched local `2026-04-12 18:12:03 PDT`
- the manager stopped making progress around `18:15:19~18:15:23 PDT`
- `preemption-state.env` showed `runtime-stalled-ai-recovery` at `18:17:03 PDT`
- the operator stop happened in that same second

So the real gap is not human-readable time-display policy. The gap is runtime forensic alignment and stall-recovery observability across evidence planes.

## Scope

1. Keep the existing display-time boundary intact: UTC naming truth, RFC3339/epoch storage truth, host-local human display truth.
2. Materialize explicit runtime event emission when stall recovery triggers, so runtime-owned recovery is visible in the canonical event ledger.
3. Bind the current manager-continuity fallback repair to an issue-owned verification chain instead of leaving it as an unowned feature-branch fix.
4. Freeze the governance conclusion that forensic alignment is a runtime observation / observability follow-on, not a reopen of the display-time owner.

## Non-Goals

1. Do not redesign all timestamp formatting or dual-surface every runtime artifact in UTC and local time.
2. Do not reopen `runtime-human-readable-time-display-governance`.
3. Do not rewrite filename timestamps, stored RFC3339 values, or watchdog cooldown truth.
4. Do not widen this owner into generic runtime restart orchestration or a full cross-plane run-id redesign.

## Acceptance

1. The owner explicitly records that this incident was one run after UTC/local alignment, not mixed historical evidence.
2. `runtime_stalled_ai_recovery_triggered` is emitted to `runtime-events.log` when manager or worker stall recovery triggers.
3. Focused regressions prove both:
   - stop-time fallback materializes the missing manager continuity required by the latest prompt
   - stall recovery leaves visible runtime-event evidence instead of only state-file residue
4. The owner remains in runtime observation / observability scope and does not claim to change display-time policy.

## Verification

- `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews/20260412-runtime-forensic-time-alignment-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews/20260412-runtime-forensic-time-alignment-verification.md`
- `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews/20260412-runtime-forensic-time-alignment-closeout-verification.md`

## Completion

- `docs/pre-brainstorms/20260412-1845--runtime-forensic-time-alignment-and-stall-observability/brainstorms.md`
- `docs/pre-brainstorms/20260412-1845--runtime-forensic-time-alignment-and-stall-observability/candidates.md`
- `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/issues/runtime-forensic-time-alignment-and-stall-recovery-observability-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/brainstorms/b-runtime-forensic-time-alignment-and-stall-recovery-observability-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/prd.md`
- `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews/20260412-runtime-forensic-time-alignment-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews/20260412-runtime-forensic-time-alignment-verification.md`
- `docs/progress/workspace-routing-foundation/p-runtime-forensic-time-alignment-and-stall-recovery-observability-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery`
- `docs/system/workspace/scripts/tests/test-freely-stop-materializes-missing-manager-continuity`

## Next

- `2026-04-12` closeout: canonical `develop` absorbed the bounded runtime repair through merge `480d839a`, and this closeout lane only writes back completed lifecycle truth.
- Keep this owner closed as the forensic-alignment and stall-observability record for the 2026-04-12 incident; future broader cross-plane correlation or restart-policy work must reopen as a new owner on current `develop`.
