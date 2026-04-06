# Candidates - 20260406-0715--codex-live-auth-identity-and-probe-lock-boundary

## Context
- Source brainstorm: `./brainstorms.md`
- Status: active

## Candidates

### C-20260406-0715-A
- candidate_format_version: `v2`
- title: `Codex live auth identity reconciliation and probe timeout boundary`
- problem: stale saved-slot metadata can override live `apikey` truth, cause `whoami/status/switch --dry-run` to surface the wrong current slot, and prevent watchdog/bootstrap flows from treating an unsaved live API-key auth as a probeable current identity.
- why_now: dogfooding exposed a real machine state where Codex is authenticated by API key outside Freely's own `login/save` flow, leaving no matching saved slot. That surfaced two distinct failures: stale slot identity reconciliation inside Freely, and a separate real-world `codex exec` stall that must not be misdiagnosed as slot mismatch.
- immediate_slice:
  - reconcile current slot from live auth bundle instead of trusting stale active-slot pointers
  - allow watchdog to probe unsaved live auth
  - preserve slot-switch lock serialization during probes
  - ensure probe timeout cleanup does not orphan `codex exec` descendants
- expected_evidence:
  - `ai whoami/status` stop surfacing stale slot names
  - watchdog probes current live `apikey` auth even with zero matching saved slots
  - timeout probe cleanup leaves no lingering `codex exec` child process
  - real API-key auth that has no saved slot reports `slot=null` while still exposing `slot_kind=apikey`
- follow_up_boundary:
  - persistent `current_auth_probe.status=timeout` in the live environment remains a separate issue and should be materialized independently if evidence shows upstream `codex exec` is banner-stalling
- priority: `P1`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- next_action: `If this slice needs continued lifecycle tracking beyond the current fix, materialize a dedicated follow-on issue instead of reopening the completed 20260405 Codex API-key slot bundle owner.`
- session_refs:
  - tool: `codex`
  - session_id: `current-thread`
  - jsonl_path: `unavailable://codex-thread-only`
  - role: `author`
