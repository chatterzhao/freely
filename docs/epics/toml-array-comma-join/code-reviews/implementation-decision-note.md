---
issue_id: I-20260626T150328Z-A
issue_path: docs/issues/I-20260626T150328Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260626T150328Z-A
- issue_path: docs/issues/I-20260626T150328Z-A/issue.md

## Implementation Decision Note

- decision: Change `tool-registry-query.py` to join TOML arrays with commas instead of spaces. Update `tool-launchers.sh` alias loop to split on commas. Add title/body format validation to `cmd_feedback`. Guard empty array `for` loop in `_ensure_acp_bridge_running` with length check.
- why_this: The Python-to-bash data contract was ambiguous (space vs comma delimiter). Comma is the correct choice because: (1) bash consumers already use `tr ',' '\n'`, (2) commas can't appear in adapter names or aliases, (3) spaces in values would break word splitting. The feedback validation prevents malformed issues from being created. The bash 3.2 guard fixes a real crash on macOS.
- alternatives_considered: (A) Fix only Python join — breaks alias loop. (B) Fix only bash side to also split on spaces — fragile, doesn't fix root cause. (C) Fix both sides + add validation + bash 3.2 guard — comprehensive fix, chosen.
- boundary_non_goals: Not changing TOML schema, not changing other bash array patterns (they work because arrays are populated before iteration), not changing platform-adapter.py.
- residual_risk: Other Python TOML array consumers might exist — verified none do. The `_resolve_tool_by_binary` function is rarely called (only when `_tool_is_registered` fails), so the comma-split alias change has low blast radius.
