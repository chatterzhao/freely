# Brainstorm
## Context
active_running_workers>0 blocked scan in all paths. Original backlog≥5 design (41c60594) was finer-grained.
## Fix
Guard moved to function parameter; only prompt(delta) path passes skip_if_active.
