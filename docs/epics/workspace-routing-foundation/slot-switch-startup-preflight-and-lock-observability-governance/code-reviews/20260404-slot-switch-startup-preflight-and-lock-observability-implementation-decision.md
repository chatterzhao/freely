# Implementation Decision: slot-switch-startup-preflight-and-lock-observability-governance

- issue_id: `I-20260404-2148-A`
- author: `codex`
- date: `2026-04-04`
- disposition: `accepted_for_implementation`

## decision

Add one shared slot-switch lock snapshot helper layer inside `docs/system/workspace/scripts/runtime/freely`, use it to gate `freely start` before supervisor bootstrap, and reuse the same snapshot in `doctor`, `baseline-status`, and `live-status`.

## why_this

- The observed root startup failure was `auth_failure`, not a live slot-switch lock, so the owner should stay narrow: startup preflight plus observability.
- The stale shared lock hazard is still real and already exists at lower layers (`ai-cli`, `tool-launchers.sh`), so `freely` needs a runtime-facing truth source instead of ad hoc startup behavior.
- A single snapshot taxonomy keeps cleanup and reporting aligned:
  - `idle`: lock absent
  - `active`: numeric live `owner_pid`
  - `stale`: missing owner pid or dead numeric owner pid
  - `ambiguous`: lock dir exists but `state.env` is missing or the pid is malformed
- This lets startup auto-clean only the clearly safe case (`stale`), wait for real in-flight switches (`active`), and fail closed on ambiguous state.

## alternatives_considered

- Reuse only the lower-layer launch wait helper.
  This was rejected because it does not expose the full lock truth to `freely doctor/status`, and it collapses ambiguous startup evidence into launch-time behavior.
- Fold the work into the broader websocket/intake supervision candidate.
  This was rejected because the current evidence does not require reopening blocked-intake supervision ownership.
- Force-delete any lock that is not clearly active.
  This was rejected because malformed or partially written lock state should block and surface evidence, not be silently destroyed.

## boundary_non_goals

- Do not treat slot-switch lock handling as the root cause of the current auth failure.
- Do not widen this owner into runtime websocket recovery, blocked intake claim, or broader manager/watchdog control-plane behavior.
- Do not change the lower-layer lock acquisition protocol in `ai-cli`; this owner only governs startup preflight and observability in `freely`.

## residual_risk

- `freely` now reasons about the shared lock by snapshotting a filesystem contract it does not own, so future `ai-cli` lock schema drift would require a follow-on owner.
- `ambiguous` still requires operator repair rather than self-healing; that is intentional, but it means malformed lock directories can still block startup until diagnosed.
