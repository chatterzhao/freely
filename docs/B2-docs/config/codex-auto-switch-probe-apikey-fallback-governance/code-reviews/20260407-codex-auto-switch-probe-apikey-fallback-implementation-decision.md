# Implementation Decision: codex-auto-switch-probe-apikey-fallback-governance

- issue_id: `I-20260407-0023-A`
- issue_path: `docs/B2-docs/config/codex-auto-switch-probe-apikey-fallback-governance/issues/codex-auto-switch-probe-apikey-fallback-governance.md`
- branch: `feature/codex-auto-switch-probe-apikey-fallback-20260406-2138`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-2138-feature-codex-auto-switch-probe-apikey-fallback`
- decision_date: `2026-04-07`
- author: `codex`

## Implementation Decision Note

- decision: `Treat all_unavailable account-sweep results the same as oauth_unreachable for the narrow case where saved apikey slots still exist, so both manual auto-switch and watchdog recovery continue into exec-only slot probing instead of stopping early.`
- why_this: `Codex apikey slots already use exec-based truth. Returning early on all_unavailable:* incorrectly treats an account-only inventory result as if it ruled out saved apikey slots too, which breaks no-arg switch behavior and the shared watchdog path.`
- alternatives_considered: `Considered reopening the completed Codex bundle/probe owner or leaving the switch path alone and only patching watchdog recovery. Reopening the old owner would violate the completed-owner closeout rule, while patching only watchdog would leave manual auto-switch inconsistent with the same slot inventory.`
- boundary_non_goals: `Do not widen this lane into unsaved current-live auth, interactive login UX, reconnect fast-fail classification, or upstream account-mode TLS diagnostics.`
- residual_risk: `Live account-mode codex exec on this machine still shows external TLS/certificate failures after switching to account. This lane intentionally treats that as environment evidence because the regression here is the missing apikey fallback after an all-unavailable account sweep.`

## Why

- `account-*` and `apikey-*` slots do not share the same availability source, so an account sweep result cannot be allowed to suppress apikey exec probing.
- Auto switch and watchdog already share the same probing path; the follow-on fix keeps them aligned rather than letting their behavior drift again.

## Non-Goals

- no new multi-tool parity work
- no standalone backend extraction work
- no new runtime observability surface for external TLS failures
