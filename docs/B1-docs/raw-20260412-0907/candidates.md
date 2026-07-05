# Candidates - 20260412-0907--codex-probe-success-shape-and-quota-slot-recovery

## Context

- Source brainstorm: `docs/pre-brainstorms/20260412-0907--codex-probe-success-shape-and-quota-slot-recovery/brainstorms.md`
- Status: promoted
- Reopens: the completed Codex slot-recovery family through a new bounded follow-on owner

## Candidates

### C-20260412-0907-A
- candidate_format_version: `v2`
- title: Codex probe success shape and quota slot recovery governance
- problem: `freely start` could still stall on a bad Codex slot because reconnect-plus-403/quota logs were being misclassified as `execution_network_*`, while the watchdog probe still treated almost any `codex exec "hi"` `rc=0` output as usable.
- why_now: Real dogfooding on 2026-04-12 reproduced both a bad apikey slot and a bad account slot. The bad account path proved recovery only worked once the failure classified to `primary_rate_limit_exhausted`, and the weak `hi` probe shape remained an independent false-positive risk.
- acceptance_criteria:
  - `codex exec "hi"` probe success requires the fixed transcript shape `user -> hi -> codex -> response -> tokens used`
  - any transcript that misses that shape is treated as failure even when `rc=0`
  - reconnect-plus-403/quota evidence classifies to slot-local exhaustion and triggers slot recovery instead of in-place network retry
  - pure reconnect/TLS evidence without auth/quota signals remains `execution_network_*`
  - real bad-account `freely start` replay auto-switches forward to the next usable slot
- fix_approach: Tighten the probe success contract to one structural positive match, expand quota/auth log detection to include 403 precharge/balance failures, add focused regressions, and replay `freely start` against a known-bad account slot.
- priority: `P1`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260412-0907-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/codex-probe-success-shape-and-quota-slot-recovery-governance/issues/codex-probe-success-shape-and-quota-slot-recovery-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260412-0907--codex-probe-success-shape-and-quota-slot-recovery/brainstorms.md`
- session_refs: []
- follow_on_to: `I-20260410-1835-B`
- next_action: Land the bounded follow-on owner, verify the real bad-account replay, and merge through `test-pre-merge-runtime-slot-recovery-20260412-0916`.
