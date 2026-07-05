- issue_id: I-20260521T122729Z-A
- issue_path: docs/issues/I-20260521T122729Z-A/issue.md
## Implementation Decision Note
- decision: Replace bash regex with simple prefix matching for env var stripping
- why_this: Regex failed on quoted values like VAR="$HOME/path". Simple prefix detection + manual quote handling is more robust.
- alternatives_considered: Keep regex (fails), use eval (unsafe), use sed (complex)
- boundary_non_goals: Not changing --settings extraction. Not changing ACP bridge.
- residual_risk: None. Tested with Claude (--settings) and OpenCode (VAR=val) aliases.
