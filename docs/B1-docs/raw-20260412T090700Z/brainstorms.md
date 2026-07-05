# Brainstorms: codex-probe-success-shape-and-quota-slot-recovery

## Context

- Date: `2026-04-12`
- Trigger: dogfooding showed `freely start` could stall on a bad Codex slot even though ordered recovery had looked correct in earlier focused tests.

## Findings

1. The runtime was not actually handling "all failures move forward". It still preserved a `network-local` branch where `execution_network_transient|persistent` retried the current `tool + slot`.
2. Real bad-slot logs mixed two signals in one cycle:
   - `ERROR: Reconnecting...`
   - `403 Forbidden` / `预扣费额度失败` / remaining-balance failures
3. Because the auth/quota matchers were too weak, the reconnect line won first and the runtime stayed on the bad slot.
4. The watchdog probe contract was also too weak:
   - `codex exec "hi"` with `rc=0` was treated as `usable`
   - this did not verify the transcript shape humans actually rely on when checking whether Codex truly answered
5. The stable success shape for `codex exec "hi"` in the current environment is structural, not reply-text-specific:
   - `user`
   - `hi`
   - `codex`
   - some response content
   - `tokens used`

## Decision

1. Tighten probe success to a single positive contract:
   - only the fixed transcript shape counts as success
   - everything else is failure-first, then classified into quota/auth/network/generic buckets
2. Treat reconnect-plus-403/quota evidence as slot-local exhaustion rather than execution-network retry.
3. Preserve pure reconnect/TLS/network evidence as `execution_network_*` so true environment failures still retry locally instead of burning through slots.

## Scope Boundary

1. Do not widen this owner into generic runtime network-taxonomy policy.
2. Do not reopen the older completed Codex exec-truth owner directly; this is a narrower follow-on regression on current dogfood evidence.
3. Do not claim all successful Codex replies must literally equal `hi`; only the transcript structure is canonicalized.
