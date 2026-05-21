# Brainstorm: permission unification
## Context
Permissions scattered across alias flags, bridge hardcode, and JSON config. bypassPermissions caused Internal error on opencode.
## Decision
All permissions in JSON config files. Bridge is tool-agnostic. Alias only passes tool+config.
