# Candidates - 20260405-2055--restart-slot-switch-preflight-preserves-active-runtime

## C-20260405-2055-A

- candidate_format_version: `v2`
- title: Restart slot-switch preflight preserves active runtime governance
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/issues/restart-slot-switch-preflight-preserves-active-runtime-governance.md`
- promoted_issue_id: `I-20260405-2055-A`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: `freely restart` still follows `stop -> start` even when the next `start` would be blocked by an active shared codex slot-switch lock, so operators can lose a healthy current runtime before the bounded lock failure is surfaced.
- why_now:
  - `I-20260404-2148-A` closed with `freely start`-only startup preflight and explicitly did not absorb wider supervision semantics
  - `I-20260327-2006-A` closed the parent command taxonomy and requires future command-semantics changes to open a new lifecycle
  - dogfood restart behavior now has concrete regression evidence and a passing end-to-end test that shows the missing contract precisely
- acceptance_criteria:
  - `freely restart` runs the shared codex slot-switch preflight before `stop_project_runtime`
  - an active shared slot-switch lock causes restart to fail or defer without stopping the currently running project supervisor or AI child
  - restart followthrough keeps relaunch helpers anchored to the target project root so degraded ownership checks do not drift onto the wrong cwd
  - stop requests that arrive between restart cycles exit before the next AI relaunch instead of launching one more child after operator stop
  - session-state writes used by restart-adjacent runtime flow are atomic enough to avoid partially written state files during supervision churn
- promotion_gate:
  - keep this owner restart-scoped; do not widen back into all startup/status observability or global watchdog redesign
  - treat cwd anchoring, readiness polling, and stop-before-launch guards as restart-adjacent implementation support, not a new generic runtime refactor bucket
  - keep auth/account-switch fixture updates tied only to evidence needed by the current runtime contract
- open_questions:
  - should restart surface the same lock-timeout wording as `freely start`, or a restart-specific wording that explicitly says the existing runtime was preserved
  - are the new helper hardenings complete enough to stay in this owner, or is there any residual generic runtime durability gap that needs its own follow-on
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: The regression is bounded, reproducible, and sits between two completed owners that both explicitly reject reopening for this behavior.
- next_action: Materialize the owner, bind the current feature lane to it, and verify restart semantics plus the directly touched runtime regressions before guarded merge.
- revisit_trigger: Reopen only if canonical `develop` again stops a healthy project runtime before reporting that shared slot-switch preflight blocks restart, or if restart-adjacent supervision durability still regresses after this owner closes.
