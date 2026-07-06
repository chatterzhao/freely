# Implementation Decision Note: cli-wrapper-packaging-and-regression-surface-governance

- issue_id: `I-20260405-2358-C`
- issue_path: `docs/B2-docs/config/cli-wrapper-packaging-and-regression-surface-governance/raw-20260405-2358issues/cli-wrapper-packaging-and-regression-surface-governance.md`
- decision_date: `2026-04-06`
- author: `codex`

## Implementation Decision Note

- decision: `Treat the first post-audit repair lane as a packaging-and-regression-surface owner: fix the audited runnable wrapper executable gaps, clean the ai help surface, and make auth-change wake regression coverage deterministic before widening back into bootstrap/status or runtime control-plane owners.`
- why_this: `The command audit showed the highest-leverage breakage was at the CLI entry surface itself. As long as direct-exec wrappers can fail with permission denied, help output leaks shell noise, or a regression depends on async timing, later bootstrap/runtime testing still sits on an untrustworthy command surface.`
- alternatives_considered: `Considered opening the project-target bootstrap/status owner first, and considered jumping directly into runtime control-plane instability. Both were rejected because they would deepen testing on top of a still-drifting wrapper layer, making failures harder to classify and easier to misattribute.`
- boundary_non_goals: `This owner does not fix baseline-status/status --project drift, sync-tooling/.githooks bootstrap gaps, stale-pid/runtime readiness instability, chat hangs, or intake counter reconciliation. Those remain separate follow-on owners from the same audit.`
- residual_risk: `A wrapper can be executable yet still fail later because of missing environment prerequisites such as node_modules; this owner only restores the packaging contract so those later failures surface as the real preflight errors instead of command-launch failures.`
