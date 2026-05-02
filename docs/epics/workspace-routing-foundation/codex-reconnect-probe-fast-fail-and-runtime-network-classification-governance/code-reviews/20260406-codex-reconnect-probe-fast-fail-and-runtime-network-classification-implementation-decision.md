# Implementation Decision Note: codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance

- issue_id: `I-20260406-0901-A`
- issue_path: `docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/issues/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md`
- branch: `feature/codex-hi-fast-fail-and-runtime-availability`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-codex-hi-fast-fail-and-runtime-availability`
- decision_date: `2026-04-06`
- author: `codex`

## Implementation Decision Note

- decision: `Treat reconnect and equivalent connection-failure partial output as an immediate probe-level network failure, terminate the child process tree, write the artifact early, and propagate the bounded `network_failure` status through ai-cli and runtime classification surfaces.`
- why_this: `The observed dogfood failure is not that Freely lacks a timeout; it is that Freely continues waiting after the probe already emitted enough evidence to classify the incident. Early exit with artifact retention is the smallest behavior change that removes operator-facing hangs, preserves diagnosis, and keeps the failure in the existing network-local taxonomy instead of inventing a second recovery family. The same lane also needs runtime classification to consume only runtime error signals, otherwise reconnect/auth/network matchers can be accidentally tripped by arbitrary prompt or document text.`
- alternatives_considered: `Considered keeping reconnect output under generic timeout and only shortening the timeout budget; rejected because that still hides the real failure class and keeps launch behavior slow. Considered treating reconnect as auth-invalid or slot-invalid; rejected because the same live auth can later succeed and the evidence is closer to transient execution/network failure than credential corruption.`
- boundary_non_goals: `Do not redesign manager bootstrap around execution-only validation, do not reopen stale-slot/live-auth identity reconciliation, and do not widen this owner into upstream Codex root-cause diagnosis or standalone ai-switch-cli extraction.`
- residual_risk: `The current matcher still depends on upstream stderr vocabulary such as `ERROR: Reconnecting...`, so future Codex CLI wording changes could weaken detection until a follow-on narrows the signal source or upstream exposes machine-readable connectivity status. The new signal excerpt narrows classification to runtime `ERROR/WARN` surfaces and selected direct failures, so future log-shape changes that stop using those forms could require another bounded adjustment.`
