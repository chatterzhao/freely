- issue_id: I-20260521T095313Z-A
- issue_path: docs/issues/I-20260521T095313Z-A/issue.md

## Implementation Decision Note

- decision: Use `type` command instead of `alias` for unified shell alias resolution
- why_this: `type` works for aliases, functions, and binaries uniformly across zsh/bash. Eliminates hardcoded prefix matching. More robust output format than `alias`.
- alternatives_considered: |
    1. Hardcoded cc-* prefix matching — fragile, requires code change for every new alias pattern
    2. Keep using `alias` command — only works for aliases (not functions/binaries), fragile sed parsing
    3. Python-based shell detection — adds complexity without benefit
- boundary_non_goals: Not changing the adapter/session/capability layer. Not changing the ACP bridge. Not adding AI_TOOL_FAMILY override.
- residual_risk: Aliases defined only in .zshrc won't be found if daemon's SHELL is bash. Mitigated by FREELY_PROJECT_SHELL config or by ensuring daemon inherits SHELL=zsh.
