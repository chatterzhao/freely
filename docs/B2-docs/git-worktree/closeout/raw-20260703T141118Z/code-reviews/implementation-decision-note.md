- issue_id: I-20260703T141118Z-A
## IDN
- decision: basename compare + short name in file + declare guard + direct query
- why_this: root cause is config.toml full path vs registry short name mismatch after comparison
- alternatives_considered: move config override before comparison (fragile); keep full path (wrong)
- boundary_non_goals: does not change config.toml or registry format
- residual_risk: new tools with different binary names may still trigger restart
