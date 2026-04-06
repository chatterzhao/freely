# Candidates - 20260406-0715--codex-live-auth-identity-and-probe-lock-boundary

## Candidate

- `codex-live-auth-identity-reconciliation`
  - problem: stale saved-slot metadata can override live `apikey` truth and prevent correct watchdog probing
  - immediate_slice:
    - reconcile current slot from live auth bundle instead of trusting stale active-slot pointers
    - allow watchdog to probe unsaved live auth
    - preserve slot-switch lock serialization during probes
    - ensure probe timeout cleanup does not orphan `codex exec` descendants
  - expected_evidence:
    - `ai whoami/status` stop surfacing stale slot names
    - watchdog probes current live `apikey` auth even with zero matching saved slots
    - timeout probe cleanup leaves no lingering `codex exec` child process
