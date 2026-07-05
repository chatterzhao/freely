# Brainstorm
## Context
run-acp-prompt.py was the last remaining bypassPermissions injection point after acp-bridge.py fix.
## Fix
Remove the session/set_mode bypassPermissions block; permissions are in JSON config.
