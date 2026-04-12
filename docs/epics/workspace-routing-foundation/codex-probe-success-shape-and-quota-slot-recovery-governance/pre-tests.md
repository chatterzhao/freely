# Pre-Tests: codex-probe-success-shape-and-quota-slot-recovery-governance

- issue_id: `I-20260412-0907-A`
- issue_path: `docs/epics/workspace-routing-foundation/codex-probe-success-shape-and-quota-slot-recovery-governance/issues/codex-probe-success-shape-and-quota-slot-recovery-governance.md`
- acceptance target: `codex hi probe success shape and reconnect-plus-quota slot recovery`

## Required checks

1. Probe success only passes on the fixed `hi` transcript shape.
2. Reconnect-plus-403/quota logs defer to slot recovery, not execution-network backoff.
3. Pure reconnect/TLS evidence still stays network-local.
4. Real bad-slot replay confirms forward progress to the next usable slot.
