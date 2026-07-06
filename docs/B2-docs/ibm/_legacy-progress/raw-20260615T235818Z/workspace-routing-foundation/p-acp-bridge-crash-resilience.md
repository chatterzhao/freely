# ACP Bridge Crash Resilience

- issue: `I-20260503-0000-A`
- issue_path: `docs/B2-docs/acp/acp-bridge-crash-resilience/raw-20260503-0000issues/I-20260503-0000-A.md`
- candidate: `C-20260503-0000-A`
- candidate_path: `docs/B1-docs/raw-20260503/candidates.md`
- milestone: `M-20260306-workspace-routing-foundation`
- phase_state: `done_ibm`
- runtime_state: `verified_on_develop`
- updated_at: `2026-05-03T00:50:00Z`
- next_action: `merge_to_develop_via_merge_guarded`

## Verification

- Daemon start → bridge health check → session/resume → set_mode bypassPermissions applied
- AI cycle completes in 5.2s (was 904s timeout before fix)
- Write tool calls execute normally (was pending→timeout before fix)
- Self-healing: broken bridge detected and restarted at startup
- All five root cause layers addressed
