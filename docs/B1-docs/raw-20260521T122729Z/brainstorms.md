# Brainstorm: env var prefix in alias expansion
## Context
OpenCode aliases use VAR=val binary format. Regex-based stripping failed on quoted values.
## Fix
Simple prefix matching: detect VAR=, strip quote-wrapped or bare value, repeat.
