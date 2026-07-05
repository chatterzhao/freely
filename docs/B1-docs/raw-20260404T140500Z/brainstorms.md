# Brainstorm - 20260404-1405--manager-bootstrap-prompt-publication-without-continuity-materialization

## Problem

`freely start` on canonical `develop` can reach dispatcher-ready and manager prompt generation, but then falls back to `activity_state=stalled_without_runtime` with `last_exit_reason=operator_stop` before new manager continuity or worker-prompt consumption is materialized.

## Observed Runtime Facts

- `freely live-status --project <project-root>` reported `activity_state: stalled_without_runtime`, `desired_runtime_state: stopped`, and `last_exit_reason: operator_stop` on `2026-04-04`.
- `.freely/run/prompt-20260404-134336.txt` was generated, but no new manager continuity or worker prompt consumption followed.
- `runtime-events.log` showed prompt-generation-era startup activity but the control plane did not stay alive long enough to consume the new supervision turn.
- This boundary is not covered by `I-20260403T224500Z-A`; that issue is scoped to sandbox-home / `ps` degraded bootstrap, not manager continuity publication failure after prompt generation.

## Routing Judgment

- This is a new `workspace-routing-foundation` runtime/control-plane lifecycle gap.
- It should not be stuffed back into completed owners such as `latest-manager-continuity-worker-consumption-governance` or `manager-supervision-quiet-period-stall-signal-governance`.
- The next owner should freeze whether the failure is bootstrap lifecycle exit, prompt-to-continuity contract breakage, or false `operator_stop` control-plane semantics.
