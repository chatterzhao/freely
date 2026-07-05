# Implementation Decision: codex-interactive-login-and-apikey-input-flow-governance

- issue_id: `I-20260406-1851-A`
- issue_path: `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/issues/codex-interactive-login-and-apikey-input-flow-governance.md`
- decided_in_branch: `feature/codex-apikey-login-interactive`
- decided_in_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-codex-apikey-login-interactive`
- decided_at: `2026-04-06`
- decision_maker: `codex`

- decision: `Keep the Codex API-key login follow-on inside the existing ai-cli surface, with one bounded interactive mode selector plus an API-key prompt flow that preserves direct-arg parity and machine-readable output continuity.`
- why_this: `The dirty implementation already proved the missing surface is a first-hop UX contract, not a runtime/watchdog problem. Keeping the work inside ai-cli preserves the existing command surface, lets the four issue-bound regressions fully bound the owner, and avoids reopening bundle/probe or bootstrap semantics.`
- alternatives_considered: `Rejected widening into generic multi-tool interactive login because only Codex has a verified concrete gap. Rejected routing the work into current-live bootstrap or reconnect owners because those owners solve different contracts and would increase ai-cli overlap.`
- boundary_non_goals: `This owner does not absorb old residual current-live/bootstrap semantics, does not change watchdog behavior, and does not start standalone ai-switch-cli extraction.`
- residual_risk: `The prompt defaults still embed Codex-oriented provider values. If provider-registry truth later becomes canonical, that should land in a separate owner rather than widening this UX lane.`
