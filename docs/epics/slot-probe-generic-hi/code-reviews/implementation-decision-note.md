- issue_id: I-20260522T044515Z-A
- issue_path: docs/issues/I-20260522T044515Z-A/issue.md
## Implementation Decision Note
- decision: slot_probe(project, tool, slot_dir) replaces codex_probe_current_slot_now
- why_this: Watchdog/probe was codex-only; apikey slots for claude/opencode had no probe path
- alternatives_considered: Per-tool probe functions (duplication), alias-based probe (requires .zshrc loaded)
- residual_risk: opencode run may hang without --print-logs; codex probe retains original behavior
