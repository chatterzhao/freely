# Brainstorm
## Context
Scan CHAIN_STATIONS produced stages (platform_open, local_only, etc.) not in prompt builder whitelist.
619+ items silently skipped → Manager saw empty scan → stop_ai.
## Fix
Dynamic stage ordering from scan summary. Ready-first sort, 30 per stage.
