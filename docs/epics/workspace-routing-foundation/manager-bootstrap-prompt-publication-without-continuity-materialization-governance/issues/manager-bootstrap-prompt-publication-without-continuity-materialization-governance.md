# Issue: manager-bootstrap-prompt-publication-without-continuity-materialization-governance

- issue_id: `I-20260404-1405-A`
- title: Manager bootstrap prompt publication without continuity materialization governance
- phase_state: `in_ibm`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-bootstrap-prompt-publication-without-continuity-materialization-governance`
- issue-name: `manager-bootstrap-prompt-publication-without-continuity-materialization-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260404-1405--manager-bootstrap-prompt-publication-without-continuity-materialization/candidates.md#c-20260404-1405-a`
- source_brainstorm: `docs/pre-brainstorms/20260404-1405--manager-bootstrap-prompt-publication-without-continuity-materialization/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- progress_path: `docs/progress/workspace-routing-foundation/p-manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- depends_on: `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/issues/sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Current canonical `develop` can reach manager prompt publication during `freely start`, but it does not hold the runtime long enough to materialize new manager continuity or worker prompt consumption. The result is a false-looking steady state: `live-status` reports `stalled_without_runtime` and `operator_stop`, but the evidence looks more like bootstrap/control-plane failure than a real explicit stop.

## Scope

1. Freeze the exact bootstrap path from dispatcher-ready to prompt publication, continuity materialization, and steady-state runtime survival.
2. Distinguish explicit stop semantics from internal early-exit and recovery-driven stop paths during startup.
3. Repair the prompt-publication-to-continuity contract so fresh manager startup either publishes durable continuity or records a bounded failure artifact with the right reason.
4. Align `live-status`, runtime events, and prompt/continuity artifacts so they expose the true boundary.

## Acceptance

- `freely start` on canonical `develop` no longer stops after prompt publication without either durable continuity materialization or explicit bounded failure evidence.
- `live-status` differentiates human/operator stop from bootstrap/control-plane failure.
- runtime events and prompt/continuity artifacts are sufficient to explain whether the manager actually launched, consumed continuity, or exited before ownership transfer.
- the lane remains focused on manager bootstrap and continuity materialization, not broader watchdog or unrelated supervision redesign.

## Verification

- `./bin/freely live-status --project <project-root>`
- `./bin/freely start --project <project-root>`
- inspect `.freely/logs/runtime-events.log`
- inspect `.freely/run/prompt-*.txt` and latest manager continuity artifacts

## Next

- Record the exact bootstrap failure evidence in canonical progress truth.
- Then repair the runtime/control-plane path in a dedicated implementation batch.
