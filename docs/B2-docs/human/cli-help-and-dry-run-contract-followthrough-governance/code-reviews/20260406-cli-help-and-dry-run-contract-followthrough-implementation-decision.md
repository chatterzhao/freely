# Implementation Decision Note: cli-help-and-dry-run-contract-followthrough-governance

- issue_id: `I-20260405-2358-D`
- issue_path: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/issues/cli-help-and-dry-run-contract-followthrough-governance.md`
- decision_date: `2026-04-06`
- author: `codex`

## Implementation Decision Note

- decision: `Repair the audited help contracts with explicit top-level --help early returns, and handle Codex auto-switch dry-run through a read-only saved-slot inventory summary instead of the normal probe-and-switch path.`
- why_this: `The broken behavior was not deep business logic; it was command-surface ambiguity. Early help handling is the smallest change that makes usage-only invocations deterministic and side-effect free. For ai dry-run, a saved-slot summary is enough to satisfy the machine-readable contract without reopening runtime probing semantics or mutating auth state.`
- alternatives_considered: `Considered treating direct-exec sourced-helper help as an error and only fixing sourced invocations; rejected because a help request is non-mutating and should not require shell-mode knowledge. Considered running the full auto-probe path in dry-run with timeouts; rejected because that keeps the contract slow, environment-sensitive, and unsuitable for automation.`
- boundary_non_goals: `This owner does not change bootstrap/status scoping, runtime control-plane behavior, executable-bit packaging policy, or the full Codex slot-selection algorithm under real switching.`
- residual_risk: `The new dry-run JSON reports saved inventory, not verified live slot usability. That is intentional for bounded dry-run semantics, but operators still need the non-dry-run path or status/whoami evidence to confirm live availability.`
