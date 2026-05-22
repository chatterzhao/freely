- issue_id: I-20260522T030835Z-A
## Implementation Decision Note
- decision: Add apikey mode to cmd_login (generate settings) and cmd_switch (update config.env)
- why_this: Existing apikey only worked for codex. Claude/opencode needed alias-based approach
- alternatives_considered: Copy existing settings (wrong: should generate from params), modify freely runtime (unnecessary: already works)
- residual_risk: switch --project only updates config.env; daemon must restart to pick up new AI_TOOL
