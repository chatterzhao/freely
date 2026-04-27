# Brainstorms - 20260426-0001--ai-tool-alias-support

## Problem
Freely hardcodes tool binaries and their launch conventions. Users with shell aliases (e.g. ccds for Claude Code with custom settings) cannot use them directly. Config changes (model, auth, settings) require both shell alias AND freely config updates.

## Decision
Let AI_TOOL accept any shell alias name. Freely resolves aliases via zsh, extracts the binary for tool family detection, and injects alias-defined extra args. AI_TOOL_FAMILY optionally overrides detected family for resume/session conventions.
