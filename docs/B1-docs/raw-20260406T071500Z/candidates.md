# Candidates - 20260406-0715--codex-live-auth-identity-and-probe-lock-boundary

## C-20260406T071500Z-A: legacy issue

- candidate_format_version: `v2`
- title: `Codex live auth identity reconciliation and probe timeout boundary`
- status: `absorbed`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- promoted_issue_id: `I-20260405T002700Z-A`
- source_brainstorm: `docs/B1-docs/raw-20260406-0715/brainstorms.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: stale saved-slot metadata can override live `apikey` truth, cause `whoami/status/switch --dry-run` to surface the wrong current slot, and prevent watchdog/bootstrap flows from treating an unsaved live API-key auth as a probeable current identity.
- why_now:
  - dogfooding exposed a real machine state where Codex is authenticated by API key outside Freely's own `login/save` flow, leaving no matching saved slot
  - the failure initially looked like lock or slot materialization drift, but the evidence split it into two separate families: Freely was reconciling current identity against stale slot pointers, and real `codex exec` was independently banner-stalling in the live environment
  - without making that distinction explicit, watchdog/bootstrap would keep misreporting stale slot identity and operators would keep chasing the wrong root cause
- acceptance_criteria:
  - `ai whoami/status/switch --dry-run` stop surfacing stale slot names when live auth does not match any saved slot
  - watchdog/bootstrap still probe a live unsaved `apikey` auth while preserving slot-switch serialization
  - probe timeout cleanup leaves no lingering `codex exec` child process
  - live API-key auth with no saved slot reports `slot=null` while still exposing `slot_kind=apikey`
- promotion_gate:
  - keep the change inside the existing Codex API-key slot bundle / provider-aware probe owner rather than reopening a second parallel owner for the same contract family
  - do not misclassify the remaining real `codex exec` banner-stall as a Freely slot-identity bug once stale-pointer reconciliation is fixed
  - do not widen the slice into generic cross-tool auth parity or a full upstream Codex failure investigation
- open_questions:
  - should a future follow-on surface the latest probe artifact path directly in `ai status` / `live-status` when `current_auth_probe.status=timeout`
  - if real `codex exec` continues to create empty session jsonl files plus banner-only stderr, does that need a dedicated runtime/operator-facing diagnosis owner
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports_absorb`
    note: the implemented fix at `HEAD` commit `c8338a6` stays fully inside the already-owned Codex API-key bundle/probe contract, while the remaining live `codex exec` timeout is upstream/external evidence that should only open a new owner if Freely needs extra observability or operator guidance.
- priority: `P1`
- decision_reason: `I-20260405T002700Z-A` already owns Codex API-key slot identity, provider-aware probe routing, and watchdog/bootstrap truth boundaries. This follow-on narrowed one missed edge inside that same completed contract, and `HEAD` commit `c8338a6` plus the added regressions close the Freely-side gap without requiring a new owner. The remaining live `codex exec` timeout is real but belongs to a separate follow-on only if Freely needs new diagnostic or UX handling for banner-stall evidence.
- next_action: treat this candidate as absorbed provenance for the follow-on fix now committed on this branch. If the live environment still needs better timeout artifact surfacing or upstream Codex banner-stall diagnosis after this branch lands, materialize a new narrow owner for operator-facing observability instead of reopening `I-20260405T002700Z-A`.
- revisit_trigger: reopen only if canonical Freely again misidentifies a live unsaved Codex API-key auth as a stale saved slot, or if persistent banner-stall timeouts require new Freely-owned diagnosis/reporting surfaces beyond the already-fixed reconciliation and cleanup path.
