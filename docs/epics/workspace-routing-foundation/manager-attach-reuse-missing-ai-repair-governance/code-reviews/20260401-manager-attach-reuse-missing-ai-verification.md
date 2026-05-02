# Verification: manager-attach-reuse-missing-ai-repair-governance

- issue_id: `I-20260330-2318-A`
- reviewed_branch: `develop`
- reviewed_commit: `9b89fb3`
- verification_date: `2026-04-01`
- verifier: `codex`

## Summary

The narrow repair is verified. Manager attach reuse no longer returns optimistic attach success when the reused supervisor lacks a confirmed live AI child, and the original worker attach-reuse contract remains green.

## Evidence

### Focused regression

- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `./bin/governance-check`

### Protected live validation

The `develop` runtime was temporarily configured with `AI_TOOL=\"kiro-cli\"` to hit the known monthly-limit path while preserving:

- `AUTO_SWITCH_TOOL=\"true\"`
- `AUTO_SWITCH_SLOT=\"true\"`
- `AI_FALLBACK_TOOLS=\"codex,cc,kiro-cli,iflow,opencode\"`

Observed runtime events:

1. `2026-04-01T08:13:51Z event=ai_cycle_finished ... tool=kiro-cli ... exit_reason=kiro_monthly_request_limit`
2. `2026-04-01T08:14:23Z event=tool_auto_switch_selected previous_tool=kiro-cli active_tool=codex reason=kiro_monthly_request_limit launch_kind=fresh_with_handoff`
3. `2026-04-01T08:14:29Z event=ai_launch_begin supervisor_pid=85814 tool=codex launch_kind=fresh ...`

Negative check:

- no `event=supervisor_attach_reuse ... ai_pid_state=missing ... role_hint=manager` appeared in the new runtime-event slice

Live-status during the post-switch launch showed:

- `desired_runtime_state: running`
- `last_supervisor_state: up`
- `last_ai_state: down`
- `last_exit_reason: starting`

That is the expected transitional truth while `codex` is launching, and it replaces the earlier false `running/up/up/already_running_attach` state.

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
