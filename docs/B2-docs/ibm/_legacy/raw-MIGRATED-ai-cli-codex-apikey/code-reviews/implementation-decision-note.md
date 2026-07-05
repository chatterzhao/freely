- issue_id: I-20260522T035043Z-A
- issue_path: docs/issues/I-20260522T035043Z-A/issue.md
## Implementation Decision Note
- decision: codex apikey uses cd-to-slot-dir alias so codex reads auth.json+config.toml natively
- why_this: codex has no --settings flag, but reads .codex/config.toml from CWD
- alternatives_considered: env var CODEX_HOME (untested), copy files to ~/.codex (old approach)
- boundary_non_goals: not changing codex account mode
- residual_risk: cd in alias may fail if slot dir is deleted
