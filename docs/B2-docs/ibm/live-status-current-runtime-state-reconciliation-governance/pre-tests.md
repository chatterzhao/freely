# Pre-Tests: live-status-current-runtime-state-reconciliation-governance

1. Active-AI status read should show:
   - `activity_state: ai_active`
   - `last_supervisor_state: up`
   - `last_ai_state: up`
   - `last_exit_reason: none`
2. Watchdog-only control-plane status should still surface `supervising_with_pending_intake`, not `stalled_without_runtime`.
3. Manager runtime recovery should still auto-recover an expected-running worker supervisor.
4. The read path must stay side-effect free with respect to `workcell-state.env`.

## Acceptance Items

### active-ai-surface-reconciled
- id: `active-ai-surface-reconciled`
- requirement: live-status must not report activity_state ai_active together with stale last_ai_state down for the same project-owned runtime.
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/live-status-current-runtime-state-reconciliation-governance/code-reviews/20260328-live-status-current-runtime-state-reconciliation-verification.md`

### watchdog-only-surface-preserved
- id: `watchdog-only-surface-preserved`
- requirement: watchdog-only control-plane visibility must still surface supervising_with_pending_intake rather than regressing to stalled_without_runtime.
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/live-status-current-runtime-state-reconciliation-governance/code-reviews/20260328-live-status-current-runtime-state-reconciliation-verification.md`

### manager-recovery-preserved
- id: `manager-recovery-preserved`
- requirement: manager runtime recovery must still auto-recover expected-running worker supervisors after the status-surface reconciliation change.
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/live-status-current-runtime-state-reconciliation-governance/code-reviews/20260328-live-status-current-runtime-state-reconciliation-verification.md`
